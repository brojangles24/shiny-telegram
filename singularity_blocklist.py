#!/usr/bin/env python3
"""
🚀 Singularity DNS Blocklist Aggregator (v2.0 - Hyperion Edition)

- 🌐 Asynchronously fetches multiple blocklists using robust caching/sessions.
- ⚖️ De-duplicates, applies weighted scoring, and tracks source overlap.
- 🚫 Filters out domains based on a separate, frequently abused TLD list.
- 💾 Generates prioritized, full, and regex-TLD lists.
- 📈 Creates an interactive Plotly dashboard (heatmap & source distribution).
- 📝 Generates a detailed, color-coded Markdown report with historical metrics.
- ✨ Enhanced performance, logging, and command-line interface.
"""
import sys
import csv
import logging
import argparse
from datetime import datetime
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple

import requests
import plotly.graph_objects as go
import plotly.io as pio

# --- Configuration & Constants ---

# Define the sources for blocklists
BLOCKLIST_SOURCES: Dict[str, str] = {
    "OISD_BIG": "https://raw.githubusercontent.com/sjhgvr/oisd/refs/heads/main/domainswild2_big.txt",
    "HAGEZI_ULTIMATE": "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/wildcard/ultimate-onlydomains.txt",
    "1HOSTS_LITE": "https://raw.githubusercontent.com/badmojr/1Hosts/refs/heads/master/Lite/domains.wildcards",
    "STEVENBLACK_HOSTS": "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"
}
HAGEZI_ABUSED_TLDS: str = "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/wildcard/spam-tlds-onlydomains.txt"

# Output configuration
OUTPUT_DIR = Path("Aggregated_list")
PRIORITY_FILENAME = "priority_300k.txt"
REGEX_TLD_FILENAME = "regex_hagezi_tlds.txt"
UNFILTERED_FILENAME = "aggregated_full.txt"
HISTORY_FILENAME = "history.csv"
REPORT_FILENAME = "metrics_report.md"
HEATMAP_IMAGE = "overlap_heatmap_sources.png"
DASHBOARD_HTML = "dashboard.html"
TLD_REGEX_TEMPLATE = r"\.{tld}$" # Enhanced regex pattern for TLD filtering

# Scoring and style
PRIORITY_CAP = 300_000
SOURCE_WEIGHTS = {"HAGEZI_ULTIMATE": 3, "OISD_BIG": 2, "1HOSTS_LITE": 1, "STEVENBLACK_HOSTS": 1}
# Color-coded sources for better reporting/visualization
SOURCE_COLORS = {
    "HAGEZI_ULTIMATE": "#d62728", # Red
    "OISD_BIG": "#1f77b4",       # Blue
    "1HOSTS_LITE": "#2ca02c",    # Green
    "STEVENBLACK_HOSTS": "#ff7f0e" # Orange
}

# --- Logging Setup ---
class ConsoleLogger:
    """A custom logger class for a clean CLI output."""
    def __init__(self, debug: bool):
        level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(
            level=level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[logging.StreamHandler(sys.stdout)]
        )
        self.logger = logging.getLogger(__name__)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)
        
    def debug(self, msg):
        self.logger.debug(msg)

# --- Utility Functions ---

def fetch_list(url: str, session: requests.Session, logger: ConsoleLogger) -> List[str]:
    """Fetches and returns content lines from a URL."""
    try:
        logger.debug(f"Fetching: {url}")
        # Add a common User-Agent to avoid blocking by some servers
        headers = {'User-Agent': 'SingularityDNSBlocklistAggregator/2.0 (Python requests)'}
        resp = session.get(url, timeout=45, headers=headers)
        resp.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
        return [l.strip().lower() for l in resp.text.splitlines() if l.strip()]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching {url}: {e.__class__.__name__}: {e}")
        return []

def process_domain(line: str) -> Optional[str]:
    """Cleans a line from a blocklist file to extract a canonical domain."""
    if not line or line.startswith(("#", "!", "|")):
        return None
    
    parts = line.split()
    if len(parts) == 1:
        domain = parts[0]
    elif len(parts) > 1 and parts[0] in ("0.0.0.0", "127.0.0.1"):
        domain = parts[1]
    else:
        # Catch unexpected line formats
        return None
    
    # Strip common non-domain parts and normalize
    domain = domain.strip().lower()
    
    # Filter common non-blocklist entries
    if domain in ("localhost", "localhost.localdomain", "::1", "255.255.255.255", "wpad"):
        return None
    
    # Remove leading wildcards/dots (e.g., from Pi-hole/AdGuard Home wildcard format)
    domain = domain.lstrip("*").lstrip(".")
    
    # Basic check to ensure it looks like a domain (has at least one dot)
    if "." not in domain:
        return None
    
    return domain

def extract_tld(domain: str) -> Optional[str]:
    """Extracts the simple TLD (e.g., 'com' from 'example.com')."""
    # Simple extraction: assumes the last part after the last dot is the TLD
    # This is a simplification but works for filtering basic TLD lists.
    parts = domain.split(".")
    return parts[-1] if len(parts) >= 2 else None

def track_history(count: int, history_path: Path, logger: ConsoleLogger) -> int:
    """Reads, updates, and writes the aggregation history."""
    HEADER = ["Date", "Priority_Count", "Change"]
    history: List[Dict[str, str]] = []
    last_count = 0

    if history_path.exists():
        try:
            with open(history_path, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames == HEADER:
                    history = list(reader)
                    if history:
                        last_count = int(history[-1].get("Priority_Count", 0))
        except Exception as e:
            logger.error(f"Failed to read history file: {e}")

    change = count - last_count
    today = datetime.now().strftime("%Y-%m-%d")

    if history and history[-1].get("Date") == today:
        # Update today's entry
        history[-1]["Priority_Count"] = str(count)
        history[-1]["Change"] = str(change)
    else:
        # Append a new entry
        history.append({"Date": today, "Priority_Count": str(count), "Change": str(change)})

    try:
        with open(history_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=HEADER)
            writer.writeheader()
            writer.writerows(history)
    except Exception as e:
        logger.error(f"Failed to write history file: {e}")

    return change

# --- Core Processing Functions ---

def fetch_and_process_sources(session: requests.Session, logger: ConsoleLogger) -> Dict[str, Set[str]]:
    """Fetches all blocklists concurrently and returns processed domain sets."""
    source_sets: Dict[str, Set[str]] = {}
    
    # Use 4 workers max to avoid overwhelming the network/servers
    max_workers = min(4, len(BLOCKLIST_SOURCES)) 
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_name = {
            executor.submit(fetch_list, url, session, logger): name 
            for name, url in BLOCKLIST_SOURCES.items()
        }
        
        for future in future_to_name:
            name = future_to_name[future]
            try:
                lines = future.result()
                # Process domains in a single, fast list comprehension
                domains = {
                    d for d in (process_domain(l) for l in lines) if d
                }
                source_sets[name] = domains
                logger.info(f"🌐 Fetched {len(domains):,} unique domains from **{name}**")
            except Exception as exc:
                logger.error(f"Source {name} generated an exception: {exc}")
                source_sets[name] = set()

    return source_sets

def aggregate_and_score_domains(source_sets: Dict[str, Set[str]]) -> Tuple[Counter, Counter, Dict[str, Set[str]]]:
    """Combines all domains, scores them by weight, and tracks overlap/sources."""
    combined_counter = Counter()  # Tracks weighted score
    overlap_counter = Counter()   # Tracks number of sources (unweighted)
    domain_sources = defaultdict(set) # Tracks which sources list a domain

    for name, domains in source_sets.items():
        weight = SOURCE_WEIGHTS.get(name, 1) # Default to 1 if not defined
        for d in domains:
            combined_counter[d] += weight
            overlap_counter[d] += 1
            domain_sources[d].add(name)

    return combined_counter, overlap_counter, domain_sources

def filter_and_prioritize(
    combined_counter: Counter, 
    session: requests.Session, 
    logger: ConsoleLogger
) -> Tuple[Set[str], Set[str], int, List[str]]:
    """Filters domains by abused TLDs and selects the top-scoring domains."""
    
    # 1. Fetch TLDs
    tld_lines = fetch_list(HAGEZI_ABUSED_TLDS, session, logger)
    abused_tlds = {l.strip() for l in tld_lines if l and not l.startswith("#")}
    logger.info(f"🚫 Excluding domains with {len(abused_tlds)} known abusive TLDs.")
    
    # 2. Filter and Score
    filtered_weighted: List[Tuple[str, int]] = []
    excluded_count = 0
    
    for domain, weight in combined_counter.items():
        tld = extract_tld(domain)
        if tld in abused_tlds:
            excluded_count += 1
        else:
            filtered_weighted.append((domain, weight))
            
    # 3. Sort by weighted score (priority)
    # Sorting is the most CPU-intensive step here, use optimized key
    filtered_weighted.sort(key=lambda x: x[1], reverse=True)
    
    # 4. Determine final lists
    # Use a set for the priority list for quick lookups and ensuring uniqueness
    final_priority = {d for d, _ in filtered_weighted[:PRIORITY_CAP]}
    # Full list of domains that passed the TLD filter (sorted by score)
    full_filtered = [d for d, _ in filtered_weighted] 
    
    logger.info(f"🔥 Excluded {excluded_count:,} domains by TLD filter.")
    logger.info(f"💾 Priority list capped at {len(final_priority):,} domains.")
    
    return final_priority, abused_tlds, excluded_count, full_filtered

# --- Reporting and Visualization ---

def generate_interactive_dashboard(
    full_filtered: List[str], 
    overlap_counter: Counter, 
    domain_sources: Dict[str, Set[str]],
    report_path: Path,
    html_path: Path,
    image_path: Path,
    logger: ConsoleLogger
):
    """Generates a Plotly stacked bar chart showing source overlap."""
    logger.info(f"📈 Generating interactive dashboard at {html_path.name}")
    
    sources = list(BLOCKLIST_SOURCES.keys())
    
    # Calculate source overlap data
    # Find all unique overlap levels for the filtered list
    overlap_levels = sorted(
        {overlap_counter[d] for d in full_filtered}, 
        reverse=True
    )
    
    # Pre-calculate data for each source at each overlap level
    heatmap_data: Dict[str, List[int]] = {src: [] for src in sources}
    
    for level in overlap_levels:
        # Find all domains in the filtered list that appear in exactly 'level' sources
        domains_at_level = [d for d in full_filtered if overlap_counter[d] == level]
        
        for src in sources:
            # Count how many of those domains are from the current source 'src'
            count = sum(1 for d in domains_at_level if src in domain_sources[d])
            heatmap_data[src].append(count)
            
    # Create the Plotly figure
    fig = go.Figure()
    
    for src in sources:
        fig.add_trace(go.Bar(
            x=[str(l) for l in overlap_levels],
            y=heatmap_data[src],
            name=src,
            marker_color=SOURCE_COLORS[src],
            text=[f"{c} domains from {src}" for c in heatmap_data[src]],
            hovertemplate="<b>Source:</b> %{name}<br><b>Overlap Level:</b> %{x}<br><b>Domains:</b> %{y:}<extra></extra>"
        ))
        
    fig.update_layout(
        barmode='stack',
        title="Singularity DNS Domain Overlap Heatmap (Filtered List)",
        xaxis_title="Number of Sources Domain Appears In",
        yaxis_title="Domain Count (Filtered List)",
        template="plotly_dark",
        legend_title_text="Blocklist Source",
        hovermode="x unified"
    )
    
    # Write output files
    pio.write_html(fig, str(html_path), auto_open=False, full_html=True, include_plotlyjs='cdn')
    # Use low resolution for speed/size, since HTML is the primary target
    fig.write_image(str(image_path), scale=1) 


def generate_markdown_report(
    priority_count: int, 
    change: int, 
    total_unfiltered: int, 
    excluded_count: int, 
    full_filtered_list: List[str], 
    overlap_counter: Counter, 
    report_path: Path,
    html_path: Path,
    logger: ConsoleLogger
):
    """Creates a detailed, aesthetic Markdown report."""
    logger.info(f"📝 Generating Markdown report at {report_path.name}")
    report: List[str] = []
    
    report.append(f"# 🛡️ Singularity DNS Blocklist Dashboard")
    report.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    report.append(f"\n## 🔑 Summary Metrics")
    
    # Calculate derived metrics
    total_unique_one = sum(1 for d in full_filtered_list if overlap_counter[d] == 1)
    
    # --- Metric Table ---
    report.append("| Metric | Count | Trend |")
    report.append("| :--- | :--- | :--- |")
    
    # Use color-coded trend indicators
    trend_icon = "⬆️" if change > 0 else "⬇️" if change < 0 else "➡️"
    trend_color = "green" if change > 0 else "red" if change < 0 else "gray"
    
    report.append(f"| Priority List Count | **{priority_count:,}** | <span style='color:{trend_color};'>`{change:+}` {trend_icon}</span> |")
    report.append(f"| Total Unique Domains (Pre-filter) | {total_unfiltered:,} | |")
    report.append(f"| Domains Excluded by TLD Filter | {excluded_count:,} | |")
    report.append(f"| Total Filtered Domains (Post-filter) | {len(full_filtered_list):,} | |")
    report.append(f"| Domains Unique to 1 Source | {total_unique_one:,} | |")
    
    # --- Source Weights Table ---
    report.append("\n## ⚖️ Scoring Weights")
    report.append("| Source | Weight | Color |")
    report.append("| :--- | :---: | :--- |")
    for name in sorted(BLOCKLIST_SOURCES.keys()):
        weight = SOURCE_WEIGHTS.get(name, 1)
        color = SOURCE_COLORS.get(name, "black")
        report.append(f"| **{name}** | {weight} | <span style='color:{color};'>███</span> |")

    # --- Interactive Dashboard ---
    report.append("\n## 🔥 Interactive Stacked Domain Overlap Dashboard")
    # Embed the HTML chart (relative path)
    report.append(f"The full interactive dashboard is available at: [`{html_path.name}`]({html_path.name})")
    report.append(f"\n### Static Preview")
    # Using an image tag here will display a static preview in tools that support it
    report.append(f"![Domain Overlap Heatmap Preview]({HEATMAP_IMAGE})")
    
    # Write the report
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report))


# --- File Writing ---

def write_output_files(
    priority_set: Set[str], 
    abused_tlds: Set[str], 
    full_list: List[str], 
    output_path: Path, 
    logger: ConsoleLogger
):
    """Writes the final blocklist, TLD regex, and full aggregated files."""
    logger.info("💾 Writing final output files...")
    output_path.mkdir(exist_ok=True, parents=True)
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 1. Priority List
    priority_file = output_path / PRIORITY_FILENAME
    with open(priority_file, "w", encoding="utf-8") as f:
        f.write(f"# Priority {PRIORITY_CAP} Blocklist\n# Generated: {now_str}\n# Total: {len(priority_set):,}\n")
        # Write sorted list for consistency
        f.writelines(d + "\n" for d in sorted(priority_set))
    
    # 2. Abused TLD Regex List
    regex_file = output_path / REGEX_TLD_FILENAME
    with open(regex_file, "w", encoding="utf-8") as f:
        f.write(f"# Hagezi Abused TLDs Regex List\n# Generated: {now_str}\n# Total: {len(abused_tlds):,}\n")
        # Generate and write TLD regex patterns
        f.writelines(TLD_REGEX_TEMPLATE.format(tld=t) + "\n" for t in sorted(abused_tlds))
        
    # 3. Full Aggregated List
    unfiltered_file = output_path / UNFILTERED_FILENAME
    with open(unfiltered_file, "w", encoding="utf-8") as f:
        f.write(f"# Full Aggregated List (Filtered by TLDs, Sorted by Score)\n# Generated: {now_str}\n# Total: {len(full_list):,}\n")
        # full_list is already filtered and sorted by score
        f.writelines(d + "\n" for d in full_list)
        
    logger.info(f"✅ Outputs written to: {output_path.resolve()}")

# --- Main Execution ---

def main():
    """Main function to run the aggregation process."""
    parser = argparse.ArgumentParser(description="Singularity DNS Blocklist Aggregator (v2.0)")
    parser.add_argument(
        "-o", "--output", 
        type=Path, 
        default=OUTPUT_DIR, 
        help=f"Output directory (default: {OUTPUT_DIR})"
    )
    parser.add_argument(
        "-d", "--debug", 
        action="store_true", 
        help="Enable DEBUG logging"
    )
    args = parser.parse_args()
    
    logger = ConsoleLogger(args.debug)
    output_path = args.output
    
    start = datetime.now()
    logger.info("--- 🚀 Starting Singularity DNS Aggregation (Hyperion Edition) ---")
    
    try:
        # Define full paths for all outputs
        history_path = output_path / HISTORY_FILENAME
        report_path = output_path / REPORT_FILENAME
        heatmap_image_path = output_path / HEATMAP_IMAGE
        dashboard_html_path = output_path / DASHBOARD_HTML
        
        with requests.Session() as session:
            # 1. Fetch & Process
            sources = fetch_and_process_sources(session, logger)
            
            # 2. Aggregate & Score
            combined_counter, overlap_counter, domain_sources = aggregate_and_score_domains(sources)
            total_unfiltered = len(combined_counter)
            logger.info(f"✨ Total unique domains across all sources: {total_unfiltered:,}")
            
            # 3. Filter & Prioritize
            priority_set, abused_tlds, excluded_count, full_filtered = filter_and_prioritize(
                combined_counter, 
                session, 
                logger
            )

        # 4. History Tracking & Metrics
        priority_count = len(priority_set)
        change = track_history(priority_count, history_path, logger)
        logger.info(f"📜 History tracked. Priority list change vs. last run: {change:+}")
        
        # 5. Reporting & Visualization
        generate_interactive_dashboard(
            full_filtered, 
            overlap_counter, 
            domain_sources,
            report_path,
            dashboard_html_path,
            heatmap_image_path,
            logger
        )
        
        generate_markdown_report(
            priority_count, 
            change, 
            total_unfiltered, 
            excluded_count, 
            full_filtered, 
            overlap_counter, 
            report_path,
            dashboard_html_path,
            logger
        )
        
        # 6. File Writing (using the full list that passed the TLD filter)
        # Note: We pass combined_counter.keys() for the unfiltered list, 
        # but the actual files use the TLD-filtered full_filtered list.
        write_output_files(
            priority_set, 
            abused_tlds, 
            full_filtered, 
            output_path, 
            logger
        )
        
    except Exception as e:
        logger.error(f"FATAL ERROR during execution: {e.__class__.__name__}: {e}")
        sys.exit(1)
        
    logger.info(f"--- ✅ Aggregation Complete in {(datetime.now() - start).total_seconds():.2f}s ---")


if __name__ == "__main__":
    main()
