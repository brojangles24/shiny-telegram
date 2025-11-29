"""
Handles all file I/O operations:
- Cleanup of old cache/archive files.
- Archiving the new priority list.
- Writing all final output files (priority, regex, full, verbose).
- Loading the last priority list from the archive.
"""
import csv
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Set, Any

# Import settings from our config module
from . import config
from .utils import ConsoleLogger # Import logger for type hinting

# --- File Writing, Archiving, and Cleanup Functions ---

def cleanup_old_files(logger: ConsoleLogger):
    """Deletes old files from cache and archive folders based on CACHE_CLEANUP_DAYS."""
    cutoff_date = datetime.now() - timedelta(days=config.CACHE_CLEANUP_DAYS)
    deleted_count = 0
    
    dirs_to_clean = [config.OUTPUT_DIR, config.ARCHIVE_DIR]
    
    for directory in dirs_to_clean:
        if not directory.exists(): continue
        
        for item in directory.iterdir():
            if item.is_file():
                # Archive files are cleaned by the new size-based function
                if directory == config.ARCHIVE_DIR and item.name.startswith("priority_"):
                    continue
                    
                if item.name.endswith((".txt", ".json", ".csv")):
                    mod_time = datetime.fromtimestamp(item.stat().st_mtime)
                    if mod_time < cutoff_date:
                        try:
                            item.unlink()
                            deleted_count += 1
                        except OSError as e:
                            logger.error(f"Failed to delete old file {item.name}: {e}")

    if deleted_count > 0:
        logger.info(f"🧹 Cleaned up {deleted_count} old cache/history files (> {config.CACHE_CLEANUP_DAYS} days old).")


def cleanup_archive_by_size(max_size_mb: int, logger: ConsoleLogger):
    """
    Deletes the oldest archive files until the folder size is under max_size_mb.
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if not config.ARCHIVE_DIR.exists():
        return

    try:
        files = sorted(
            [f for f in config.ARCHIVE_DIR.glob("priority_*.txt") if f.is_file()],
            key=lambda f: f.stat().st_mtime
        )
    except Exception as e:
        logger.error(f"Failed to list archive files for cleanup: {e}")
        return
        
    try:
        current_size_bytes = sum(f.stat().st_size for f in files)
    except OSError as e:
        logger.error(f"Failed to calculate archive size: {e}")
        return

    if current_size_bytes <= max_size_bytes:
        logger.info(f"Archive size ({current_size_bytes / 1024**2 :.1f}MB) is within the {max_size_mb}MB limit. No cleanup needed.")
        return

    logger.warning(f"Archive size ({current_size_bytes / 1024**2 :.1f}MB) exceeds {max_size_mb}MB limit. Cleaning up old files...")
    
    deleted_count = 0
    bytes_to_free = current_size_bytes - max_size_bytes
    bytes_freed = 0

    for file_to_delete in files:
        if bytes_freed >= bytes_to_free:
            break
        
        try:
            file_size = file_to_delete.stat().st_size
            file_to_delete.unlink()
            bytes_freed += file_size
            deleted_count += 1
        except OSError as e:
            logger.error(f"Failed to delete old archive file {file_to_delete.name}: {e}")

    logger.info(f"🧹 Cleaned up {deleted_count} old archive files. Freed {bytes_freed / 1024**2 :.1f}MB.")


def archive_priority_list(logger: ConsoleLogger):
    """Archives the primary priority list file with a timestamp."""
    config.ARCHIVE_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    
    source_path = config.OUTPUT_DIR / config.PRIORITY_FILENAME
    if not source_path.exists():
        logger.error(f"Cannot archive: Source file not found at {source_path}")
        return

    archive_path = config.ARCHIVE_DIR / f"priority_{timestamp}.txt"
    try:
        archive_path.write_bytes(source_path.read_bytes())
        logger.info(f"📦 Archived current priority list to {archive_path.name}")
    except Exception as e:
        logger.error(f"Failed to archive priority list: {e}")

def write_verbose_exclusion_report(
    excluded_domains: List[Dict[str, Any]], logger: ConsoleLogger
):
    """Writes a CSV file containing all domains that failed to make the Priority List."""
    
    if not excluded_domains:
        logger.info("Skipping verbose report: No domains excluded by TLD filter or score cutoff.")
        return

    csv_path = config.OUTPUT_DIR / config.VERBOSE_EXCLUSION_FILE
    
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['domain', 'score', 'status', 'reason']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(excluded_domains)
        logger.info(f"💾 Verbose exclusion report written: {csv_path.name} ({len(excluded_domains):,} entries)")
    except Exception as e:
        logger.error(f"Failed to write verbose exclusion report: {e}")

def write_output_files(
    priority_set: Set[str], abused_tlds: Set[str], full_list: List[str], 
    logger: ConsoleLogger, priority_cap_val: int, excluded_domains_verbose: List[Dict[str, Any]], 
    write_verbose: bool, output_format: str
):
    """Writes all final output files in the specified format."""
    logger.info("💾 Writing final output files...")
    config.OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M%S')

    # 1. Priority List
    priority_file = config.OUTPUT_DIR / config.PRIORITY_FILENAME
    
    prefix = "0.0.0.0 " if output_format == 'hosts' else ""
    header = (
        f"# Hosts File Priority {priority_cap_val} Blocklist (Actual size: {len(priority_set):,})\n"
        if output_format == 'hosts'
        else f"# Priority {priority_cap_val} Blocklist (Actual size: {len(priority_set):,})\n"
    )
    header += f"# Generated: {now_str}\n"

    with open(priority_file, "w", encoding="utf-8") as f:
        f.write(header)
        f.write(f"# Total: {len(priority_set):,}\n")
        f.writelines(prefix + d + "\n" for d in sorted(priority_set))
    
    # 2. Archive the list
    archive_priority_list(logger)

    # 3. Verbose Exclusion Report
    if write_verbose:
        write_verbose_exclusion_report(excluded_domains_verbose, logger)
        
    # 4. Abused TLD Regex List
    regex_file = config.OUTPUT_DIR / config.REGEX_TLD_FILENAME
    with open(regex_file, "w", encoding="utf-8") as f:
        f.write(f"# Hagezi Abused TLDs Regex List (and custom additions, if any)\n# Generated: {now_str}\n# Total: {len(abused_tlds):,}\n")
        f.writelines(f"\\.{t}$\n" for t in sorted(abused_tlds))
        
    # 5. Full Aggregated List
    unfiltered_file = config.OUTPUT_DIR / config.UNFILTERED_FILENAME
    with open(unfiltered_file, "w", encoding="utf-8") as f:
        f.write(f"# Full Aggregated List (ALL Scored Domains, Sorted by Score)\n# Generated: {now_str}\n# Total: {len(full_list):,}\n")
        f.writelines(d + "\n" for d in full_list)
        
    logger.info(f"✅ Outputs written to: {config.OUTPUT_DIR.resolve()}")

def load_last_priority_from_archive(
    logger: ConsoleLogger, output_format: str
) -> Set[str]:
    """Finds the most recent archive file and loads it into a set."""
    if not config.ARCHIVE_DIR.exists():
        logger.info("Archive directory not found. Skipping priority change tracking.")
        return set()

    try:
        archive_files = list(config.ARCHIVE_DIR.glob("priority_*.txt"))
        if not archive_files:
            logger.info("No archive files found. Skipping priority change tracking.")
            return set()
            
        latest_file = max(archive_files, key=lambda f: f.stat().st_mtime)
        logger.info(f"Loading previous priority list from: {latest_file.name}")
        
        old_priority_set = set()
        prefix_to_strip = "0.0.0.0 " if output_format == 'hosts' else ""
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if prefix_to_strip and line.startswith(prefix_to_strip):
                        old_priority_set.add(line[len(prefix_to_strip):])
                    else:
                        old_priority_set.add(line)
                        
        logger.info(f"Loaded {len(old_priority_set):,} domains from previous archive.")
        return old_priority_set
        
    except Exception as e:
        logger.error(f"Failed to load from archive: {e}")
        return set()
