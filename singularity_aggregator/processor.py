"""
Core processing logic and main application entry point.
- process_domain: Cleans and validates a single domain.
- aggregate_and_score_domains: Combines lists and applies weights.
- filter_and_prioritize: Applies TLD blocking and priority cap.
- calculate_...: All metrics functions (Jaccard, volatility, etc.)
- main: The main function that orchestrates the entire pipeline.
"""
import sys
import argparse
import asyncio
import requests
from datetime import datetime
from collections import Counter, defaultdict
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple, Any, Union
from itertools import combinations

# Import settings from our config module
from . import config
# Import other modules from our package
from .utils import ConsoleLogger, load_metrics_cache, save_metrics_cache, track_history, extract_tld
from .file_handler import (
    cleanup_old_files, load_last_priority_from_archive, write_output_files, 
    cleanup_archive_by_size
)
from .fetcher import fetch_and_process_sources_async
from .reporting import generate_markdown_report, generate_static_score_histogram, generate_history_plot

# --- Core Aggregation & Scoring ---

def aggregate_and_score_domains(
    source_sets: Dict[str, Set[str]]
) -> Tuple[Counter, Counter, Dict[str, Set[str]]]:
    """Combines all domains, scores them by weight, and tracks overlap/sources."""
    combined_counter = Counter()
    overlap_counter = Counter()
    domain_sources = defaultdict(set)

    for name, domains in source_sets.items():
        weight = config.SOURCE_WEIGHTS.get(name, 1)
        for d in domains:
            combined_counter[d] += weight
            overlap_counter[d] += 1
            domain_sources[d].add(name)

    return combined_counter, overlap_counter, domain_sources

def filter_and_prioritize(
    combined_counter: Counter, logger: ConsoleLogger,
    priority_cap: int,
    args_block_tlds: List[str],      # TLDs from --block-tlds
    args_custom_tld_file: Optional[Path], # Path from --custom-tld-file
    args_no_hagezi_tlds: bool             # Flag from --no-hagezi-tlds
) -> Tuple[Set[str], Set[str], int, List[str], Counter, List[Dict[str, Any]]]:
    """
    Filters domains by abusive TLDs (from config and args) for the priority list.
    """
    abused_tlds: Set[str] = set()

    # 1. --- Load Hagezi TLDs (if not disabled by args) ---
    if not args_no_hagezi_tlds and config.HAGEZI_ABUSED_TLDS_URL:
        try:
            logger.info(f"Fetching Hagezi Abused TLD list from: {config.HAGEZI_ABUSED_TLDS_URL}")
            tld_lines_req = requests.get(
                config.HAGEZI_ABUSED_TLDS_URL, timeout=45, 
                headers={'User-Agent': 'SingularityDNSBlocklistAggregator/5.8.4'}
            )
            tld_lines_req.raise_for_status()
            tld_lines = tld_lines_req.text.splitlines()
            hagezi_set = {l.strip().lower() for l in tld_lines if l.strip() and not l.startswith("#")}
            abused_tlds.update(hagezi_set)
            logger.info(f"Loaded {len(hagezi_set):,} TLDs from Hagezi.")
        except Exception as e:
            logger.error(f"WARNING: Could not fetch Hagezi TLD list: {e}. Continuing...")
    elif args_no_hagezi_tlds:
        logger.info("Skipping Hagezi TLD list fetch as requested by --no-hagezi-tlds.")
    
    # 2. --- Load Custom TLDs from File (if provided by args) ---
    if args_custom_tld_file:
        if args_custom_tld_file.exists():
            try:
                with open(args_custom_tld_file, 'r', encoding='utf-8') as f:
                    file_tlds = {l.strip().lower().lstrip('.') for l in f if l.strip() and not l.startswith("#")}
                abused_tlds.update(file_tlds)
                logger.info(f"Loaded {len(file_tlds):,} TLDs from custom file: {args_custom_tld_file.name}")
            except Exception as e:
                logger.error(f"Failed to read custom TLD file {args_custom_tld_file.name}: {e}")
        else:
            logger.warning(f"Custom TLD file not found: {args_custom_tld_file}")
    
    # 3. --- Load Custom TLDs from CLI (if provided by args) ---
    if args_block_tlds:
        cli_tlds = {t.lower().lstrip('.') for t in args_block_tlds}
        abused_tlds.update(cli_tlds)
        logger.info(f"Loaded {len(cli_tlds):,} TLDs from --block-tlds arguments.")
        
    # 4. --- Load Custom TLDs from config.toml ---
    if config.CUSTOM_BLOCK_TLDS:
        config_tlds = {t.lower().lstrip('.') for t in config.CUSTOM_BLOCK_TLDS}
        abused_tlds.update(config_tlds)
        logger.info(f"Loaded {len(config_tlds):,} TLDs from config.toml [tlds.custom_block_tlds].")

    logger.info(f"🚫 Total unique TLDs for exclusion: {len(abused_tlds):,}")
    
    # --- Start Filtering ---
    full_scored_list: List[Tuple[str, int]] = sorted(
        combined_counter.items(), key=lambda x: x[1], reverse=True
    )
    priority_candidates: List[Tuple[str, int]] = []
    excluded_count = 0
    tld_exclusion_counter = Counter()
    excluded_domains_verbose: List[Dict[str, Any]] = []

    for domain, weight in full_scored_list:
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
            
    final_priority = {d for d, _ in priority_candidates[:priority_cap]}
    
    for domain, score in priority_candidates[priority_cap:]:
        excluded_domains_verbose.append({
            'domain': domain, 'score': score, 'status': 'SCORE CUTOFF',
            'reason': f'Scored {score} but did not make the top {priority_cap:,} list.'
        })

    logger.info(f"🔥 Excluded {excluded_count:,} domains by TLD filter.")
    logger.info(f"💾 Priority list capped at {len(final_priority):,} domains.")
    
    return (
        final_priority, abused_tlds, excluded_count, 
        [d for d, _ in full_scored_list], # full_list (domain strings only)
        tld_exclusion_counter, excluded_domains_verbose
    )

# --- Metrics Calculation ---

def calculate_source_metrics(
    priority_set: Set[str], full_list: List[str], overlap_counter: Counter, 
    domain_sources: Dict[str, Set[str]], all_domains_from_sources: Dict[str, Set[str]], 
    logger: ConsoleLogger,
    old_source_metrics: Dict[str, Any]
) -> Dict[str, Dict[str, Union[int, str]]]:
    """Calculates contribution and uniqueness metrics per source."""
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
            old_fetched = old_source_metrics.get(name, {}).get("Total_Fetched", 0)
            
            if old_fetched > 0:
                change_pct = ((current_fetched - old_fetched) / old_fetched) * 100
                metrics[name]["Volatility"] = f"{change_pct:+.1f}%" 
            elif current_fetched > 0:
                metrics[name]["Volatility"] = "New"
            else:
                metrics[name]["Volatility"] = "N/A"
            
    final_metrics: Dict[str, Dict[str, Union[int, str]]] = {k: dict(v) for k, v in metrics.items()}
    logger.info("📈 Calculated Source Metrics (including Volatility).")
    return final_metrics

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
    
    change_report = {
        "added": [{'domain': d, 'novelty': 'Fresh'} for d in added_domains],
        "removed": [{'domain': d} for d in removed_domains],
        "remained": [{'domain': d} for d in remained_domains]
    }
    return change_report

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
        jaccard_index = (intersection / union) if union > 0 else 0.0
            
        matrix[name_a][name_b] = jaccard_index
        matrix[name_b][name_a] = jaccard_index
    
    for name in source_names:
        matrix[name][name] = 1.0
        
    return matrix


# --- Main Execution ---
def main():
    """Main function to run the aggregation process."""
    parser = argparse.ArgumentParser(description="Singularity DNS Blocklist Aggregator (v5.8.4)")
    
    # Use defaults from config.py
    parser.add_argument(
        "-o", "--output", type=Path, default=config.OUTPUT_DIR, 
        help=f"Output directory (default: {config.OUTPUT_DIR})"
    )
    parser.add_argument("-d", "--debug", action="store_true", help="Enable DEBUG logging")
    parser.add_argument(
        "-p", "--priority-cap", type=int, default=config.PRIORITY_CAP_DEFAULT, 
        help=f"Maximum size for the priority list (default: {config.PRIORITY_CAP_DEFAULT:,})"
    )
    parser.add_argument(
        "-w", "--max-workers", type=int, default=config.MAX_WORKERS_DEFAULT, 
        help=f"Maximum concurrent network workers (default: {config.MAX_WORKERS_DEFAULT})"
    )
    parser.add_argument("-v", "--verbose-report", action="store_true", help="Write a detailed CSV report of all excluded domains.")
    parser.add_argument(
        "-f", "--output-format", choices=['raw', 'hosts'], default=config.OUTPUT_FORMAT_DEFAULT, 
        help="Output format for the priority list (default: 'raw')"
    )
    parser.add_argument(
        "--cleanup-cache", action="store_true", 
        help=f"Delete old cache and history files (> {config.CACHE_CLEANUP_DAYS} days)."
    )
    parser.add_argument(
        "--archive-limit-mb", type=int, default=config.ARCHIVE_LIMIT_MB_DEFAULT, 
        help=f"Maximum size (MB) for the /archive folder. (default: {config.ARCHIVE_LIMIT_MB_DEFAULT})"
    )
    
    # TLD Arguments
    parser.add_argument(
        "--block-tlds", nargs='+', default=[],
        help="A space-separated list of custom TLDs to block (e.g., --block-tlds xyz ru cn)."
    )
    parser.add_argument(
        "--custom-tld-file", type=Path, default=config.CUSTOM_TLD_FILE_DEFAULT,
        help="Path to a custom text file of TLDs to exclude (one per line)."
    )
    parser.add_argument(
        "--no-hagezi-tlds", action="store_true", default=config.NO_HAGEZI_TLDS_DEFAULT,
        help="Do not fetch the Hagezi abused TLD list."
    )
    
    args = parser.parse_args()
    
    # --- Setup ---
    logger = ConsoleLogger(args.debug)
    # Set output dir based on args, and update config paths dynamically
    config.OUTPUT_DIR = args.output
    config.ARCHIVE_DIR = config.OUTPUT_DIR / config.ARCHIVE_DIR_NAME
    config.METRICS_CACHE_FILE = config.OUTPUT_DIR / config.PATHS.get("metrics_cache_file", "metrics_cache.json")
    
    config.OUTPUT_DIR.mkdir(exist_ok=True)
    
    start = datetime.now()
    logger.info("--- 🚀 Starting Singularity DNS Aggregation (v5.8.4 - Modular) ---")
    
    if args.cleanup_cache:
        cleanup_old_files(logger)
    
    old_source_metrics = load_metrics_cache()
    old_priority_set = load_last_priority_from_archive(logger, args.output_format)
    
    # === Main Pipeline ===
    try:
        # 1. Fetch & Process
        source_sets, all_domains_from_sources = asyncio.run(
            fetch_and_process_sources_async(args.max_workers, logger)
        )
        
        # 2. Aggregate & Score
        combined_counter, overlap_counter, domain_sources = aggregate_and_score_domains(source_sets)
        total_unfiltered = len(combined_counter)
        
        # 2.5 Calculate Similarity
        jaccard_matrix = calculate_similarity_matrix(source_sets, logger)
        
        # 3. Filter & Prioritize
        priority_set, abused_tlds, excluded_count, full_list, tld_exclusion_counter, excluded_domains_verbose = filter_and_prioritize(
            combined_counter, logger, args.priority_cap,
            args.block_tlds, args.custom_tld_file, args.no_hagezi_tlds
        )

        # 4. History Tracking & Metrics 
        priority_count = len(priority_set)
        change, history = track_history(total_unfiltered, logger)
        source_metrics = calculate_source_metrics(
            priority_set, full_list, overlap_counter, domain_sources, 
            all_domains_from_sources, logger, old_source_metrics
        )
        
        # 5. Priority List Change Tracking
        change_report = track_priority_changes(priority_set, old_priority_set, logger)

        # 6. Reporting & Visualization
        generate_static_score_histogram(combined_counter, full_list, logger)
        generate_history_plot(history, logger)
        
        generate_markdown_report(
            priority_count, change, total_unfiltered, excluded_count, full_list, combined_counter,
            overlap_counter, source_metrics, history, logger, domain_sources, change_report, 
            tld_exclusion_counter, args.priority_cap, excluded_domains_verbose,
            jaccard_matrix, priority_set
        )
        
        # 7. File Writing
        write_output_files(
            priority_set, abused_tlds, full_list, logger, args.priority_cap,
            excluded_domains_verbose, args.verbose_report, args.output_format
        )
        
        # 8. Save Metrics Cache
        save_metrics_cache(source_metrics)
        
        # 9. Cleanup Archive by Size
        logger.info("Checking archive folder size limit...")
        cleanup_archive_by_size(args.archive_limit_mb, logger)
        
    except Exception as e:
        logger.error(f"FATAL ERROR during execution: {e.__class__.__name__}: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1  # Exit with error
        
    logger.info(f"--- ✅ Aggregation Complete in {(datetime.now() - start).total_seconds():.2f}s ---")
    return 0 # Exit successfully
