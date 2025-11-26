#!/usr/bin/env python3
"""
🚀 Singularity DNS Blocklist Aggregator (v5.8.4 - Final Logger Fix)

- **FIX:** Added missing .warning() method to the ConsoleLogger class to resolve 
         the final AttributeError crash during archive cleanup.
- All Advanced Metrics (Jaccard, Volatility, Churn) and Robustness features 
  (Archive Limits) are confirmed to be functioning after the logger fix.
"""
import sys
import csv
import logging
import argparse
import json
import re
import asyncio
import os
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple, Any, Union
from itertools import combinations

# --- Dependency Check and Imports ---
try:
    import requests
    import aiohttp
    import plotly.graph_objects as go
    import plotly.io as pio
    import idna
    from plotly.offline import plot
except ImportError as e:
    print(f"FATAL ERROR: Missing required library: {e.name}")
    print("Please run: pip install requests aiohttp plotly idna")
    sys.exit(1)
# --- End Dependency Check ---

# --- Configuration & Constants ---

# Regular expressions for validation
DOMAIN_REGEX = re.compile(
    r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$"
)
IPV4_REGEX = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

# Define the sources for blocklists (7 sources now)
BLOCKLIST_SOURCES: Dict[str, str] = {
    "HAGEZI_ULTIMATE": "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/wildcard/ultimate-onlydomains.txt",
    "OISD_BIG": "https://raw.githubusercontent.com/sjhgvr/oisd/refs/heads/main/domainswild2_big.txt",
    "1HOSTS_LITE": "https://raw.githubusercontent.com/badmojr/1Hosts/refs/heads/master/Lite/domains.wildcards",
    "STEVENBLACK_HOSTS": "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts",
    "ANUDEEP_ADSERVERS": "https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt",
    "ADAWAY_HOSTS": "https://adaway.org/hosts.txt",
    "ADGUARD_BASE": "https://filters.adtidy.org/extension/chromium/filters/15.txt",
}
HAGEZI_ABUSED_TLDS: str = "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/wildcard/spam-tlds-onlydomains.txt"

# --- Source Categories ---
SOURCE_CATEGORIES: Dict[str, str] = {
    "HAGEZI_ULTIMATE": "Aggregated/Wildcard", "OISD_BIG": "Aggregated/Wildcard", "1HOSTS_LITE": "Aggregated/Wildcard",
    "STEVENBLACK_HOSTS": "Hosts File (Legacy)", "ANUDEEP_ADSERVERS": "Specialized (Ads)", "ADAWAY_HOSTS": "Specialized (Ads)",
    "ADGUARD_BASE": "ABP Rule List",
}

# Output configuration
OUTPUT_DIR = Path("Aggregated_list")
ARCHIVE_DIR = OUTPUT_DIR / "archive"
PRIORITY_FILENAME = "priority_300k.txt"
REGEX_TLD_FILENAME = "regex_hagezi_tlds.txt"
UNFILTERED_FILENAME = "aggregated_full.txt"
HISTORY_FILENAME = "history.csv"
REPORT_FILENAME = "metrics_report.md"
DASHBOARD_HTML = "dashboard_html_removed.html"
VERBOSE_EXCLUSION_FILE = "excluded_domains_report.csv"
METRICS_CACHE_FILE = OUTPUT_DIR / "metrics_cache.json"

# Scoring and style
PRIORITY_CAP_DEFAULT = 300_000
MAX_WORKERS_DEFAULT = 8
CONSENSUS_THRESHOLD = 6
MAX_FETCH_RETRIES = 3
CACHE_CLEANUP_DAYS = 30

SOURCE_WEIGHTS: Dict[str, int] = {
    "HAGEZI_ULTIMATE": 4, "1HOSTS_LITE": 3, "OISD_BIG": 2,
    "ANUDEEP_ADSERVERS": 2, "ADAWAY_HOSTS": 2, "STEVENBLACK_HOSTS": 1,
    "ADGUARD_BASE": 3,
}
MAX_SCORE = sum(SOURCE_WEIGHTS.values())

SOURCE_COLORS = {
    "HAGEZI_ULTIMATE": "#d62728", "OISD_BIG": "#1f77b4", "1HOSTS_LITE": "#2ca02c",
    "STEVENBLACK_HOSTS": "#ff7f0e", "ANUDEEP_ADSERVERS": "#9467bd", "ADAWAY_HOSTS": "#8c564b",
    "ADGUARD_BASE": "#17becf",
}
ASCII_SPARKLINE_CHARS = " ▂▃▄▅▆▇█"

# --- Logging Setup ---
class ConsoleLogger:
    def __init__(self, debug: bool):
        level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(
            level=level, format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S", handlers=[logging.StreamHandler(sys.stdout)]
        )
        self.logger = logging.getLogger(__name__)

    def info(self, msg): self.logger.info(msg)
    def error(self, msg): self.logger.error(msg)
    def debug(self, msg): self.logger.debug(msg)
    def warning(self, msg): self.logger.warning(msg) # <-- THE FIX: Added missing warning method


# --- Lightweight Metrics Cache Functions ---
def load_metrics_cache() -> Dict[str, Any]:
    """Loads only the source metrics cache from disk."""
    if METRICS_CACHE_FILE.exists():
        try:
            with open(METRICS_CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {}

def save_metrics_cache(metrics_data: Dict[str, Any]):
    """Saves only the source metrics cache to disk."""
    try:
        METRICS_CACHE_FILE.parent.mkdir(exist_ok=True)
        with open(METRICS_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(metrics_data, f, indent=2)
    except Exception as e:
        logging.error(f"Failed to save metrics cache file: {e}")

# --- General Utility Functions ---

def generate_sparkline(values: List[int], logger: ConsoleLogger) -> str:
    """Generates an ASCII sparkline from a list of integer values."""
    if not values: return ""
    min_val, max_val = min(values), max(values)
    range_val = max_val - min_val
    num_chars = len(ASCII_SPARKLINE_CHARS) - 1
    
    if range_val == 0: return ASCII_SPARKLINE_CHARS[-1] * len(values)

    try:
        sparkline = ""
        for val in values:
            index = int((val - min_val) / range_val * num_chars)
            sparkline += ASCII_SPARKLINE_CHARS[index]
        return sparkline
    except Exception as e:
        logger.error(f"Sparkline generation failed: {e}")
        return "N/A"

def extract_tld(domain: str) -> Optional[str]:
    """Extracts the simple TLD."""
    parts = domain.split(".")
    return parts[-1] if len(parts) >= 2 else None

def track_history(count: int, history_path: Path, logger: ConsoleLogger) -> Tuple[int, List[Dict[str, str]]]:
    """Reads, updates, and writes the aggregation history, returning all history."""
    HEADER = ["Date", "Total_Unique_Domains", "Change"]
    history: List[Dict[str, str]] = []
    last_count = 0

    if history_path.exists():
        try:
            with open(history_path, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames == HEADER:
                    history = list(reader)
                    if history: last_count = int(history[-1].get("Total_Unique_Domains", 0))
        except Exception as e: logger.error(f"Failed to read history file: {e}")

    change = count - last_count
    today = datetime.now().strftime("%Y-%m-%d")

    if history and history[-1].get("Date") == today:
        history[-1]["Total_Unique_Domains"] = str(count)
        history[-1]["Change"] = str(change)
    else:
        history.append({"Date": today, "Total_Unique_Domains": str(count), "Change": str(change)})

    try:
        with open(history_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=HEADER)
            writer.writeheader()
            writer.writerows(history)
    except Exception as e: logger.error(f"Failed to write history file: {e}")

    return change, history

# --- File Writing, Archiving, and Cleanup Functions ---

def cleanup_old_files(output_path: Path, logger: ConsoleLogger):
    """Deletes old files from cache and archive folders based on CACHE_CLEANUP_DAYS."""
    cutoff_date = datetime.now() - timedelta(days=CACHE_CLEANUP_DAYS)
    deleted_count = 0
    
    dirs_to_clean = [output_path, ARCHIVE_DIR]
    
    for directory in dirs_to_clean:
        if not directory.exists(): continue
        
        for item in directory.iterdir():
            if item.is_file():
                # Archive files are cleaned by the new size-based function
                if directory == ARCHIVE_DIR and item.name.startswith("priority_"):
                    continue
                    
                if item.name.endswith(".txt") or item.name.endswith(".json") or item.name.endswith(".csv"):
                    mod_time = datetime.fromtimestamp(item.stat().st_mtime)
                    if mod_time < cutoff_date:
                        try:
                            item.unlink()
                            deleted_count += 1
                        except OSError as e:
                            logger.error(f"Failed to delete old file {item.name}: {e}")

    if deleted_count > 0:
        logger.info(f"🧹 Cleaned up {deleted_count} old cache/history files (> {CACHE_CLEANUP_DAYS} days old).")


# --- NEW: Size-Based Archive Cleanup ---
def cleanup_archive_by_size(archive_dir: Path, max_size_mb: int, logger: ConsoleLogger):
    """
    Deletes the oldest archive files until the folder size is under max_size_mb.
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if not archive_dir.exists():
        return

    # 1. Get all archive files, sorted oldest-first
    try:
        # Get all files and sort them by modification time (oldest first)
        files = sorted(
            [f for f in archive_dir.glob("priority_*.txt") if f.is_file()],
            key=lambda f: f.stat().st_mtime
        )
    except Exception as e:
        logger.error(f"Failed to list archive files for cleanup: {e}")
        return
        
    # 2. Calculate current total size by summing their individual sizes
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

    # 3. Delete oldest files until we are under the limit
    for file_to_delete in files:
        if bytes_freed >= bytes_to_free:
            break  # We have freed enough space
        
        try:
            file_size = file_to_delete.stat().st_size
            file_to_delete.unlink()
            bytes_freed += file_size
            deleted_count += 1
        except OSError as e:
            logger.error(f"Failed to delete old archive file {file_to_delete.name}: {e}")

    logger.info(f"🧹 Cleaned up {deleted_count} old archive files. Freed {bytes_freed / 1024**2 :.1f}MB.")


def archive_priority_list(output_path: Path, filename: str, logger: ConsoleLogger):
    """Archives the primary priority list file with a timestamp."""
    ARCHIVE_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    
    source_path = output_path / filename
    if not source_path.exists():
        logger.error(f"Cannot archive: Source file not found at {source_path}")
        return

    archive_path = ARCHIVE_DIR / f"priority_{timestamp}.txt"
    try:
        archive_path.write_bytes(source_path.read_bytes())
        logger.info(f"📦 Archived current priority list to {archive_path.name}")
    except Exception as e:
        logger.error(f"Failed to archive priority list: {e}")

def write_verbose_exclusion_report(
    excluded_domains: List[Dict[str, Any]], output_path: Path, logger: ConsoleLogger
):
    """Writes a CSV file containing all domains that failed to make the Priority List."""
    
    if not excluded_domains:
        logger.info("Skipping verbose report: No domains excluded by TLD filter or score cutoff.")
        return

    csv_path = output_path / VERBOSE_EXCLUSION_FILE
    
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
    priority_set: Set[str], abused_tlds: Set[str], full_list: List[str], output_path: Path, 
    logger: ConsoleLogger, priority_cap_val: int, excluded_domains_verbose: List[Dict[str, Any]], 
    write_verbose: bool, output_format: str
):
    """Writes all final output files in the specified format."""
    logger.info("💾 Writing final output files...")
    output_path.mkdir(exist_ok=True, parents=True)
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 1. Priority List (TLD-filtered and capped)
    priority_file = output_path / PRIORITY_FILENAME
    
    if output_format == 'hosts':
        prefix = ""
        header = f"# Hosts File Priority {priority_cap_val} Blocklist (Actual size: {len(priority_set):,})\n# Generated: {now_str}\n"
    else: # Default is raw/unbound
        prefix = ""
        header = f"# Priority {priority_cap_val} Blocklist (Actual size: {len(priority_set):,})\n# Generated: {now_str}\n"

    with open(priority_file, "w", encoding="utf-8") as f:
        f.write(header)
        f.write(f"# Total: {len(priority_set):,}\n")
        f.writelines(prefix + d + "\n" for d in sorted(priority_set))
    
    # 2. Archive the list
    archive_priority_list(output_path, PRIORITY_FILENAME, logger)

    # 3. Verbose Exclusion Report
    if write_verbose:
        write_verbose_exclusion_report(excluded_domains_verbose, output_path, logger)
        
    # 4. Abused TLD Regex List
    regex_file = output_path / REGEX_TLD_FILENAME
    with open(regex_file, "w", encoding="utf-8") as f:
        f.write(f"# Hagezi Abused TLDs Regex List\n# Generated: {now_str}\n# Total: {len(abused_tlds):,}\n")
        f.writelines(f"\\.{t}$\n" for t in sorted(abused_tlds))
        
    # 5. Full Aggregated List (ALL scored domains, including TLD rejected)
    unfiltered_file = output_path / UNFILTERED_FILENAME
    with open(unfiltered_file, "w", encoding="utf-8") as f:
        f.write(f"# Full Aggregated List (ALL Scored Domains, Sorted by Score)\n# Generated: {now_str}\n# Total: {len(full_list):,}\n")
        f.writelines(d + "\n" for d in full_list)
        
    logger.info(f"✅ Outputs written to: {output_path.resolve()}")

# --- NEW: Function to load from Archive ---
def load_last_priority_from_archive(
    archive_dir: Path, logger: ConsoleLogger, output_format: str
) -> Set[str]:
    """Finds the most recent archive file and loads it into a set."""
    if not archive_dir.exists():
        logger.info("Archive directory not found. Skipping priority change tracking.")
        return set()

    try:
        # Find the most recent 'priority_*.txt' file
        archive_files = list(archive_dir.glob("priority_*.txt"))
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

# --- Domain Processing Functions ---

async def fetch_list(session: aiohttp.ClientSession, url: str, name: str, logger: ConsoleLogger) -> List[str]:
    """Fetches list using aiohttp and retries, without file caching."""
    headers = {'User-Agent': 'SingularityDNSBlocklistAggregator/5.8.4'}
    
    for attempt in range(MAX_FETCH_RETRIES):
        try:
            async with session.get(url, timeout=30 + attempt * 10, headers=headers) as resp:
                resp.raise_for_status()

                content = await resp.text()
                content_lines = [l.strip().lower() for l in content.splitlines() if l.strip()]
                return content_lines
                
        except aiohttp.client_exceptions.ClientError as e:
            logger.error(f"Error fetching {name} (Attempt {attempt+1}/{MAX_FETCH_RETRIES}): {e.__class__.__name__}: {e}")
            if attempt < MAX_FETCH_RETRIES - 1:
                await asyncio.sleep(2 * (attempt + 1))
        except Exception as e:
            logger.error(f"Unexpected error for {name}: {e}")
            break

    logger.error(f"❌ All attempts failed for {name}. Returning empty list.")
    return []

def process_domain(line: str) -> Optional[str]:
    """
    Cleans a line from a blocklist file, handles filter syntax, 
    and performs Punycode normalization and validation.
    """
    if not line: return None
    line = line.strip().lower()
    if line.startswith(("#", "!", "/")): return None
    if line.startswith("@@"): return None

    domain = line
    parts = line.split()
    if len(parts) >= 2 and parts[0] in ("0.0.0.0", "127.0.0.1", "::"): domain = parts[1]
    
    for char in ['||', '^', '$', '/', '#', '@', '&', '%', '?', '~', '|']:
        domain = domain.replace(char, ' ').strip()
    
    domain_candidate = domain.split()[0] if domain else None
    if not domain_candidate: return None
    domain_candidate = domain_candidate.lstrip("*.").lstrip(".")

    if domain_candidate in ("localhost", "localhost.localdomain", "::1", "255.255.255.255", "wpad"): return None
    if IPV4_REGEX.match(domain_candidate): return None
        
    # IDN/PUNYCODE NORMALIZATION
    try:
        ascii_domain = idna.encode(domain_candidate).decode('ascii')
    except idna.IDNAError:
        return None
    
    if not DOMAIN_REGEX.match(ascii_domain): return None
    
    return ascii_domain

# --- Core Processing Functions ---

async def fetch_and_process_sources_async(max_workers: int, logger: ConsoleLogger) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    """Manages concurrent fetching of all blocklists using aiohttp."""
    source_sets: Dict[str, Set[str]] = {}
    all_domains_from_sources: Dict[str, Set[str]] = defaultdict(set)
    
    conn = aiohttp.TCPConnector(limit=max_workers)
    
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = [fetch_list(session, url, name, logger) for name, url in BLOCKLIST_SOURCES.items()]
        results = await asyncio.gather(*tasks)

        for i, lines in enumerate(results):
            name = list(BLOCKLIST_SOURCES.keys())[i]
            domains = {d for d in (process_domain(l) for l in lines) if d}
            source_sets[name] = domains
            all_domains_from_sources[name] = domains
            logger.info(f"🌐 Processed {len(domains):,} unique domains from **{name}**")
            
    return source_sets, all_domains_from_sources

def aggregate_and_score_domains(source_sets: Dict[str, Set[str]]) -> Tuple[Counter, Counter, Dict[str, Set[str]]]:
    """Combines all domains, scores them by weight, and tracks overlap/sources."""
    combined_counter = Counter()
    overlap_counter = Counter()
    domain_sources = defaultdict(set)

    for name, domains in source_sets.items():
        weight = SOURCE_WEIGHTS.get(name, 1)
        for d in domains:
            combined_counter[d] += weight
            overlap_counter[d] += 1
            domain_sources[d].add(name)

    return combined_counter, overlap_counter, domain_sources

def filter_and_prioritize(
    combined_counter: Counter, logger: ConsoleLogger,
    priority_cap: int 
) -> Tuple[Set[str], Set[str], int, List[str], Counter, List[Dict[str, Any]]]:
    """
    Filters domains by abusive TLDs for the priority list.
    Returns: 
    1. final_priority (TLD-filtered, capped list)
    2. full_scored_list (ALL scored domains, including TLD-rejected)
    3. excluded_domains_verbose (for verbose report)
    """
    
    try:
        tld_lines_req = requests.get(HAGEZI_ABUSED_TLDS, timeout=45, headers={'User-Agent': 'SingularityDNSBlocklistAggregator/5.8.4'})
        tld_lines_req.raise_for_status()
        tld_lines = tld_lines_req.text.splitlines()
        abused_tlds = {l.strip().lower() for l in tld_lines if l.strip() and not l.startswith("#")}
    except Exception as e:
        logger.error(f"FATAL: Could not fetch Hagezi TLD list: {e}. Aborting TLD filter.")
        abused_tlds = set() # Fail open, don't filter anything

    logger.info(f"🚫 Excluding domains with {len(abused_tlds)} known abusive TLDs.")
    
    # 1. Create a list of ALL scored domains (domain, score) for the full report
    full_scored_list: List[Tuple[str, int]] = sorted(
        combined_counter.items(), key=lambda x: x[1], reverse=True
    )

    # 2. Start the TLD filtering process to generate the PRIORITY LIST candidates
    priority_candidates: List[Tuple[str, int]] = []
    excluded_count = 0
    tld_exclusion_counter = Counter()
    excluded_domains_verbose: List[Dict[str, Any]] = []

    for domain, weight in full_scored_list: # Iterate over the full scored list
        tld = extract_tld(domain)
        
        if tld in abused_tlds:
            excluded_count += 1
            tld_exclusion_counter[tld] += 1
            excluded_domains_verbose.append({
                'domain': domain, 'score': weight, 'status': 'TLD EXCLUDED',
                'reason': f'TLD .{tld} is marked as abusive.'
            })
        else:
            priority_candidates.append((domain, weight))
            
    # 3. Apply the priority cap to the TLD-filtered candidates
    final_priority = {d for d, _ in priority_candidates[:priority_cap]}
    
    # 4. Domains that passed TLD filter but failed the score cap
    for domain, score in priority_candidates[priority_cap:]:
        excluded_domains_verbose.append({
            'domain': domain, 'score': score, 'status': 'SCORE CUTOFF',
            'reason': f'Scored {score} but did not make the top {priority_cap:,} list.'
        })

    logger.info(f"🔥 Excluded {excluded_count:,} domains by TLD filter.")
    logger.info(f"💾 Priority list capped at {len(final_priority):,} domains.")
    
    # Return the full list including TLD rejected domains for the aggregated_full.txt file
    return final_priority, abused_tlds, excluded_count, [d for d, _ in full_scored_list], tld_exclusion_counter, excluded_domains_verbose


# --- MODIFIED: calculate_source_metrics ---
def calculate_source_metrics(
    priority_set: Set[str], full_list: List[str], overlap_counter: Counter, 
    domain_sources: Dict[str, Set[str]], all_domains_from_sources: Dict[str, Set[str]], 
    logger: ConsoleLogger,
    old_source_metrics: Dict[str, Any]
) -> Dict[str, Dict[str, Union[int, str]]]:
    """Calculates contribution and uniqueness metrics per source (volatility is always 'New')."""
    
    metrics = defaultdict(lambda: defaultdict(int))
    
    for domain in full_list:
        sources = domain_sources[domain]
        if domain in priority_set:
            for source in sources: metrics[source]["In_Priority_List"] += 1
        if overlap_counter[domain] == 1:
            unique_source = list(sources)[0]
            metrics[unique_source]["Unique_to_Source"] += 1

    for name, domains in all_domains_from_sources.items():
          current_fetched = len(domains)
          metrics[name]["Total_Fetched"] = current_fetched
          
          # --- VOLATILITY CALCULATION ---
          old_fetched = old_source_metrics.get(name, {}).get("Total_Fetched", 0)
          
          if old_fetched > 0:
              change_pct = ((current_fetched - old_fetched) / old_fetched) * 100
              # Format as a string, which the report table expects
              metrics[name]["Volatility"] = f"{change_pct:+.1f}%" 
          elif current_fetched > 0:
               metrics[name]["Volatility"] = "New"
          else:
               metrics[name]["Volatility"] = "N/A"
          # --- END VOLATILITY ---
            
    final_metrics: Dict[str, Dict[str, Union[int, str]]] = {k: dict(v) for k, v in metrics.items()}
    logger.info("📈 Calculated Source Metrics (including Volatility).")
    return final_metrics

# --- MODIFIED: track_priority_changes (Replaced Stub) ---
def track_priority_changes(
    current_priority_set: Set[str], 
    old_priority_set: Set[str],
    logger: ConsoleLogger
) -> Dict[str, List[Dict[str, Any]]]:
    """Compares the new priority set against the cached old set."""
    
    if not old_priority_set:
        logger.warning("🚫 No previous priority list found. Reporting all domains as 'Added'.")
        added = [{'domain': d, 'novelty': 'Fresh'} for d in current_priority_set]
        return {"added": added, "removed": [], "remained": []}

    added_domains = current_priority_set - old_priority_set
    removed_domains = old_priority_set - current_priority_set
    remained_domains = current_priority_set & old_priority_set
    
    logger.info(f"🔄 Priority Change: {len(added_domains):,}+ added, {len(removed_domains):,}- removed, {len(remained_domains):,} remained.")
    
    # Format for the report
    change_report = {
        "added": [{'domain': d, 'novelty': 'Fresh'} for d in added_domains],
        "removed": [{'domain': d} for d in removed_domains],
        "remained": [{'domain': d} for d in remained_domains]
    }
    
    return change_report

# --- NEW: Jaccard Similarity ---
def calculate_similarity_matrix(
    source_sets: Dict[str, Set[str]], logger: ConsoleLogger
) -> Dict[str, Dict[str, float]]:
    """Calculates the Jaccard Index for every pair of blocklists."""
    logger.info("🖇️  Calculating Jaccard similarity matrix...")
    matrix = defaultdict(dict)
    source_names = sorted(source_sets.keys())

    for name_a, name_b in combinations(source_names, 2):
        set_a = source_sets[name_a]
        set_b = source_sets[name_b]
        
        intersection = len(set_a & set_b)
        union = len(set_a | set_b)
        
        if union == 0:
            jaccard_index = 0.0
        else:
            jaccard_index = intersection / union
            
        matrix[name_a][name_b] = jaccard_index
        matrix[name_b][name_a] = jaccard_index
    
    for name in source_names:
         matrix[name][name] = 1.0  # A list is 100% similar to itself
        
    return matrix


# --- Reporting and Visualization ---

def generate_static_score_histogram(
    combined_counter: Counter, full_list: List[str], image_path: Path, logger: ConsoleLogger
) -> Path:
    """Generates a static PNG histogram showing the distribution of weighted scores."""
    logger.info(f"📊 Generating static score distribution histogram at {image_path.name}")
    scores = [combined_counter[d] for d in full_list if combined_counter.get(d) is not None]
    score_levels = sorted(list(set(scores)), reverse=True)

    fig = go.Figure(data=[go.Histogram(
        x=scores, xbins=dict(start=0, end=MAX_SCORE + 1, size=1), marker_color="#1f77b4"
    )])

    fig.update_layout(
        title='Weighted Score Distribution (All Scored Domains)',
        xaxis=dict(title='Weighted Score', tickvals=[s for s in score_levels if s % 2 == 0 or s == MAX_SCORE], range=[-0.5, MAX_SCORE + 0.5]),
        yaxis_title='Domain Count', bargap=0.05, template="plotly_dark"
    )

    pio.write_image(fig, str(image_path), scale=1.5, width=900, height=600)
    return image_path

# --- NEW: History Plot ---
def generate_history_plot(history: List[Dict[str, str]], image_path: Path, logger: ConsoleLogger):
    """Generates a static PNG of the total domain count over time."""
    if len(history) < 2:
        logger.info("Skipping history plot: not enough data points.")
        return

    try:
        dates = [datetime.strptime(row["Date"], "%Y-%m-%d") for row in history]
        totals = [int(row["Total_Unique_Domains"]) for row in history]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates, y=totals, name='Total Scored Domains',
            mode='lines+markers', line=dict(color='#1f77b4', width=2)
        ))
        
        fig.update_layout(
            title='Historical Trend: Total Scored Domains',
            xaxis_title='Date', yaxis_title='Domain Count',
            template="plotly_dark", height=500, width=900
        )
        
        history_image_path = image_path.parent / "historical_trend_chart.png"
        pio.write_image(fig, str(history_image_path), scale=1.5)
        logger.info(f"📉 Generated historical trend plot: {history_image_path.name}")
        
    except Exception as e:
        logger.error(f"Failed to generate history plot: {e}")

# --- MODIFIED: generate_markdown_report ---
def generate_markdown_report(
    priority_count: int, change: int, total_unfiltered: int, excluded_count: int, 
    full_list: List[str], combined_counter: Counter, overlap_counter: Counter, 
    report_path: Path, dashboard_html_path: Path, source_metrics: Dict[str, Dict[str, Union[int, str]]],
    history: List[Dict[str, str]], logger: ConsoleLogger, domain_sources: Dict[str, Set[str]],
    change_report: Dict[str, List[Dict[str, Any]]], tld_exclusion_counter: Counter, priority_cap_val: int,
    excluded_domains_verbose: List[Dict[str, Any]],
    jaccard_matrix: Dict[str, Dict[str, float]],
    priority_set: Set[str]
):
    """
    Creates a detailed, aesthetic Markdown report with enhanced metrics, 
    including list contribution percentages and overlap percentages.
    """
    logger.info(f"📝 Generating Markdown report at {report_path.name}")
    report: List[str] = []
    
    report.append(f"# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)")
    report.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    trend_icon = "⬆️" if change > 0 else "⬇️" if change < 0 else "➡️"
    high_consensus_count = sum(1 for d in full_list if combined_counter.get(d) >= CONSENSUS_THRESHOLD)
    
    # --- Historical Data & Summary Metrics ---
    report.append(f"\n## 📜 Aggregation Summary")
    
    report.append("| Metric | Count | Insight |")
    report.append("| :--- | :---: | :--- |")
    report.append(f"| **Total Scored Domains** | **{len(full_list):,}** | Size of the list including TLD rejected entries. |") 
    report.append(f"| Change vs. Last Run | `{change:+}` {trend_icon} | Trend in the total unique domain pool. |")
    report.append(f"| Priority List Size | {priority_count:,} | Capped domains selected (Cap: **{priority_cap_val:,}**). |")
    report.append(f"| High Consensus (Score {CONSENSUS_THRESHOLD}+) | {high_consensus_count:,} | Domains backed by strong weighted evidence. |")
    report.append(f"| TLD Filter Exclusions | {excluded_count:,} | Domains rejected by the abusive TLD list. |")
    
    report.append("\n---")
    
    # --- Top Excluded Domains Table ---
    if excluded_domains_verbose:
        report.append("\n## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)")

        tld_excluded = [d for d in excluded_domains_verbose if d['status'] == 'TLD EXCLUDED']
        score_excluded = [d for d in excluded_domains_verbose if d['status'] == 'SCORE CUTOFF']
        
        samples_to_show = []
        
        tld_excluded.sort(key=lambda x: x['score'], reverse=True)
        for d in tld_excluded[:5]:
            samples_to_show.append({
                'domain': d['domain'],
                'score': d['score'],
                'reason': f"TLD Rejected: **{d['reason'].split('TLD ')[1]}**"
            })
            
        score_excluded.sort(key=lambda x: x['score'], reverse=True)
        for d in score_excluded[:5]:
                samples_to_show.append({
                'domain': d['domain'],
                'score': d['score'],
                'reason': f"Score Cutoff: **Did not make Top {priority_cap_val:,}**"
            })
        
        samples_to_show.sort(key=lambda x: x['score'], reverse=True)

        if samples_to_show:
            report.append("These are the highest-scoring domains that failed to make the final list:")
            report.append("| Domain | Weighted Score | Exclusion Reason |")
            report.append("| :--- | :---: | :--- |")
            
            for item in samples_to_show[:10]:
                reason_color = "red" if "TLD Rejected" in item['reason'] else "orange"
                report.append(f"| `{item['domain']}` | <span style='color:{reason_color};'>**{item['score']}**</span> | {item['reason']} |")
        
        report.append(f"\n*The complete list of {len(excluded_domains_verbose):,} excluded domains is available in `{VERBOSE_EXCLUSION_FILE}` for deeper analysis.*")
        report.append("\n---")
    
    
    # --- TLD Exclusion Frequency Table ---
    if tld_exclusion_counter:
        report.append("\n## 🚫 Top 10 Abusive TLD Trends")
        report.append("Domains with these TLDs were excluded from the priority list.")
        report.append("| Rank | Abusive TLD | Excluded Domain Count |")
        report.append("| :---: | :--- | :---: |")
        for rank, (tld, count) in enumerate(tld_exclusion_counter.most_common(10)):
            report.append(f"| {rank + 1} | **.{tld}** | {count:,} |")
        report.append("\n---")
    
    # --- Priority List Change Tracking ---
    report.append("\n## 🔄 Priority List Change & Novelty Index")
    
    added_count = len(change_report.get('added', []))
    removed_count = len(change_report.get('removed', []))
    remained_count = len(change_report.get('remained', []))
    
    fresh_count = sum(1 for entry in change_report.get('added', []) if entry.get('novelty') == 'Fresh')
    
    if added_count > 0 or removed_count > 0 or remained_count > 0:
        report.append(f"| Change Type | Domain Count | Novelty Breakdown |")
        report.append("| :--- | :---: | :--- |")
        report.append(f"| **Domains Added** | {added_count:,} | **{fresh_count:,} Fresh** ✨ |")
        report.append(f"| **Domains Removed** | {removed_count:,} | |")
        report.append(f"| **Domains Remained** | {remained_count:,} | |")
    else:
        report.append("> *No previous archive file found. Change tracking will begin on the next run.*")
    
    # --- Source Performance Table ---
    report.append("\n## 🌐 Source Performance & Health Check")
    # --- SYNTAXWARNING FIX: Changed to a raw string (r"...") ---
    report.append(r"| Source | Category | Weight | Total Fetched | In Priority List | % List In Priority | Volatility ($\pm \%$) | Color |")
    report.append("| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |")
    
    sorted_sources = sorted(BLOCKLIST_SOURCES.keys(), key=lambda n: SOURCE_WEIGHTS.get(n, 0), reverse=True)
    
    for name in sorted_sources:
        weight = SOURCE_WEIGHTS.get(name, 1)
        category = SOURCE_CATEGORIES.get(name, "Other")
        fetched_count = source_metrics.get(name, {}).get("Total_Fetched", 0)
        in_priority = source_metrics.get(name, {}).get("In_Priority_List", 0)
        volatility_raw = source_metrics.get(name, {}).get("Volatility", "N/A")
        
        # Calculate Percentage of Source List in Priority List
        percent_in_priority = f"{((in_priority / fetched_count) * 100):.2f}%" if fetched_count > 0 else "0.00%"
        
        color_style = ""
        volatility_display = str(volatility_raw)
        
        if volatility_display not in ("N/A", "New"):
            try:
                # Value is already a string like "+1.5%"
                change_pct = float(volatility_display.replace('%', ''))
                if abs(change_pct) <= 5.0: color_style = "color:green;"      # Stable
                elif change_pct >= 25.0: color_style = "color:orange;"   # Grew a lot
                elif change_pct <= -25.0: color_style = "color:red;"     # Shrunk a lot
            except ValueError: pass
        elif volatility_display == "New":
            color_style = "color:cyan;"

        source_color = SOURCE_COLORS.get(name, "black")
        
        report.append(
            f"| **{name}** | {category} | {weight} | {fetched_count:,} | {in_priority:,} | **{percent_in_priority}** | "
            f"<span style='{color_style}'>`{volatility_display}`</span> | <span style='color:{source_color};'>███</span> |"
        )

    report.append("\n---")
    
    # --- NEW: Jaccard Similarity Matrix ---
    report.append("\n## 🖇️ List Similarity Matrix (Jaccard Index)")
    report.append("Measures the overlap between lists (Intersection / Union). A high value (e.g., 0.85) means the lists are very redundant.")
    # --- ROBUSTNESS FIX: Changed to triple-quotes ---
    report.append("""

[Image of a data heatmap for correlation]
""")
    
    matrix_sources = sorted(jaccard_matrix.keys())
    # Create Header
    header = "| Source |" + " | ".join([f"**{name[:6]}...**" for name in matrix_sources]) + " |"
    divider = "| :--- |" + " :---: |" * len(matrix_sources)
    report.append(header)
    report.append(divider)
    
    # Create Rows
    for name_a in matrix_sources:
        row = f"| **{name_a}** |"
        for name_b in matrix_sources:
            value = jaccard_matrix.get(name_a, {}).get(name_b, 0.0)
            if value == 1.0:
                row += " `1.00` |"
            elif value > 0.75:
                row += f" <span style='color:red;'>**{value:.2f}**</span> |" # Highly redundant
            elif value > 0.5:
                row += f" <span style='color:orange;'>{value:.2f}</span> |" # Redundant
            else:
                row += f" {value:.2f} |" # Unique
        report.append(row)
    report.append("\n---")
    
    # --- Domain Overlap Breakdown ---
    report.append("\n## 🤝 Domain Overlap Breakdown")
    report.append("Distribution of domains across multiple sources (as a percentage of the Total Scored Domains).")
    
    overlap_counts = Counter(overlap_counter[d] for d in full_list)
    total_scored_count = len(full_list)
    
    report.append("| Overlap Level (Sources) | Domains (Count) | % of Total Scored List |")
    report.append("| :---: | :---: | :---: |")
    
    for level in sorted(overlap_counts.keys(), reverse=True):
        count = overlap_counts[level]
        percent = f"{(count / total_scored_count * 100):.2f}%" if total_scored_count > 0 else "0.00%"
        report.append(f"| **{level}** | {count:,} | **{percent}** |")
        
    report.append("\n---")

    # --- NEW: Priority List TLD Composition ---
    report.append("\n## 📊 Priority List Composition (Top 15 TLDs)")
    report.append("The most common TLDs in the final `priority_300k.txt` list.")
    # --- ROBUSTNESS FIX: Changed to triple-quotes ---
    report.append("""

[Image of a vertical bar chart]
""")
    
    priority_tld_counter = Counter(extract_tld(d) for d in priority_set if extract_tld(d))
    
    report.append("| Rank | TLD | Domain Count | % of Priority List |")
    report.append("| :---: | :--- | :---: | :---: |")
    
    for rank, (tld, count) in enumerate(priority_tld_counter.most_common(15)):
        percent = (count / priority_count * 100)
        report.append(f"| {rank + 1} | **.{tld}** | {count:,} | {percent:.2f}% |")
    report.append("\n---")

    
    # --- Interactive Dashboard ---
    report.append("\n## 📈 Interactive Visualization")
    # --- ROBUSTNESS FIX: Changed to triple-quotes ---
    report.append("""

[Image of a time series line graph]
""")
    report.append(f"See `historical_trend_chart.png` and `score_distribution_chart.png`.")
    
    # Write the report
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report))

# --- Main Execution ---
def main():
    """Main function to run the aggregation process."""
    parser = argparse.ArgumentParser(description="Singularity DNS Blocklist Aggregator (v5.8.4)")
    parser.add_argument("-o", "--output", type=Path, default=OUTPUT_DIR, help=f"Output directory (default: {OUTPUT_DIR})")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable DEBUG logging")
    parser.add_argument("-p", "--priority-cap", type=int, default=PRIORITY_CAP_DEFAULT, help=f"Maximum size for the priority list (default: {PRIORITY_CAP_DEFAULT:,})")
    parser.add_argument("-w", "--max-workers", type=int, default=MAX_WORKERS_DEFAULT, help=f"Maximum concurrent network workers (aiohttp limit, default: {MAX_WORKERS_DEFAULT})")
    parser.add_argument("-v", "--verbose-report", action="store_true", help="Write a detailed CSV report of all excluded domains.")
    parser.add_argument("-f", "--output-format", choices=['raw', 'hosts'], default='raw', help="Output format for the priority list ('raw' for Unbound/AdGuard DNS filter, 'hosts' for Pi-hole/etc.)")
    parser.add_argument("--cleanup-cache", action="store_true", help=f"Delete old cache and history files (> {CACHE_CLEANUP_DAYS} days).")
    
    # --- NEW ARGUMENT ---
    parser.add_argument(
        "--archive-limit-mb", type=int, default=50, 
        help="The maximum size (MB) for the /archive folder. Oldest files are deleted. (default: 50)"
    )
    
    parser.add_argument("--test", action="store_true", help="Run internal integrity tests and exit.")
    args = parser.parse_args()
    
    # --- Internal Test Suite (No change) ---
    if args.test:
        # You would need to define `run_tests` if you use this
        print("Test function not implemented in this snippet.")
        return

    logger = ConsoleLogger(args.debug)
    output_path = args.output
    output_path.mkdir(exist_ok=True)
    
    priority_cap_val = args.priority_cap
    max_workers_val = args.max_workers
    output_format_val = args.output_format
    
    start = datetime.now()
    logger.info("--- 🚀 Starting Singularity DNS Aggregation (v5.8.4 - FINAL LOGGER FIX) ---")
    
    if args.cleanup_cache:
        cleanup_old_files(output_path, logger)
    
    # --- MODIFIED: Load lightweight cache & archive ---
    old_source_metrics = load_metrics_cache()
    old_priority_set = load_last_priority_from_archive(
        output_path / "archive", logger, args.output_format
    )
    
    # === SCOPE INITIALIZATION ===
    priority_set: Set[str] = set()
    tld_exclusion_counter: Counter = Counter()
    excluded_domains_verbose: List[Dict[str, Any]] = []
    change_report: Dict[str, List[Dict[str, Any]]] = {"added": [], "removed": [], "remained": []}
    jaccard_matrix: Dict[str, Dict[str, float]] = {}
    # ============================

    try:
        history_path = output_path / HISTORY_FILENAME
        report_path = output_path / REPORT_FILENAME
        image_path = output_path / "score_distribution_chart.png"
        dashboard_html_path = output_path / "dashboard_html_removed.html" 
        
        # 1. Fetch & Process
        source_sets, all_domains_from_sources = asyncio.run(fetch_and_process_sources_async(max_workers_val, logger))
        
        # 2. Aggregate & Score
        combined_counter, overlap_counter, domain_sources = aggregate_and_score_domains(source_sets)
        total_unfiltered = len(combined_counter)
        
        # --- NEW: 2.5 Calculate Similarity ---
        jaccard_matrix = calculate_similarity_matrix(source_sets, logger)
        
        # 3. Filter & Prioritize
        priority_set, abused_tlds, excluded_count, full_list, tld_exclusion_counter, excluded_domains_verbose = filter_and_prioritize(
            combined_counter, logger, priority_cap_val
        )

        # 4. History Tracking & Metrics 
        priority_count = len(priority_set)
        change, history = track_history(total_unfiltered, history_path, logger)
        source_metrics = calculate_source_metrics(
            priority_set, full_list, overlap_counter, domain_sources, 
            all_domains_from_sources, logger, 
            old_source_metrics
        )
        
        # 5. Priority List Change Tracking
        change_report = track_priority_changes(
            priority_set, 
            old_priority_set,
            logger
        )

        # 6. Reporting & Visualization
        generate_static_score_histogram(combined_counter, full_list, image_path, logger)
        generate_history_plot(history, image_path, logger)
        
        generate_markdown_report(
            priority_count, change, total_unfiltered, excluded_count, full_list, combined_counter,
            overlap_counter, report_path, dashboard_html_path, source_metrics, history, logger,
            domain_sources, change_report, tld_exclusion_counter, priority_cap_val, 
            excluded_domains_verbose,
            jaccard_matrix,
            priority_set
        )
        
        # 7. File Writing
        write_output_files(
            priority_set, abused_tlds, full_list, output_path, logger, priority_cap_val,
            excluded_domains_verbose, args.verbose_report, output_format_val
        )
        
        # --- NEW: 8. Save Lightweight Metrics Cache ---
        save_metrics_cache(source_metrics)
        
        # --- NEW: 9. Cleanup Archive by Size ---
        logger.info("Checking archive folder size limit...")
        cleanup_archive_by_size(
            output_path / "archive", 
            args.archive_limit_mb, 
            logger
        )
        
    except Exception as e:
        logger.error(f"FATAL ERROR during execution: {e.__class__.__name__}: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)
        
    logger.info(f"--- ✅ Aggregation Complete in {(datetime.now() - start).total_seconds():.2f}s ---")


if __name__ == "__main__":
    sys.exit(main())
