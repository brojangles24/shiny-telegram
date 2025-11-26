#!/usr/bin/env python3
"""
🚀 Singularity DNS Blocklist Aggregator (v4.10 - Interactive Dashboard Edition)

- **MAJOR CHANGE:** Overlap heatmap replaced with an interactive, filterable HTML table (dashboard.html).
- **NEW FEATURE:** Users can filter all domains by minimum weighted score in the dashboard.
- **IMPROVEMENT:** PNG output simplified to a Score Distribution Histogram for better readability.
"""
import sys
import csv
import logging
import argparse
import json
import re
from datetime import datetime
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple, Any

import requests
import plotly.graph_objects as go
import plotly.io as pio

# --- Configuration & Constants ---

# Regular expressions for validation
DOMAIN_REGEX = re.compile(
    r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$"
)
# Simple pattern to catch common IPv4 addresses (e.g., 1.2.3.4)
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

# Output configuration
OUTPUT_DIR = Path("Aggregated_list")
PRIORITY_FILENAME = "priority_300k.txt"
REGEX_TLD_FILENAME = "regex_hagezi_tlds.txt"
UNFILTERED_FILENAME = "aggregated_full.txt"
HISTORY_FILENAME = "history.csv"
REPORT_FILENAME = "metrics_report.md"
HEATMAP_IMAGE = "overlap_heatmap_sources.png" # Renamed to score_distribution_chart.png later
DASHBOARD_HTML = "dashboard.html"
CACHE_FILE = OUTPUT_DIR / "fetch_cache.json"
PRIORITY_CACHE_FILE = OUTPUT_DIR / "priority_cache.json" 

# Scoring and style
PRIORITY_CAP = 300_000
CONSENSUS_THRESHOLD = 6 # Threshold for "High Consensus" domains

# CUSTOM WEIGHTS: (Max Score is 17)
SOURCE_WEIGHTS: Dict[str, int] = {
    "HAGEZI_ULTIMATE": 4,
    "1HOSTS_LITE": 3,
    "OISD_BIG": 2, 
    "ANUDEEP_ADSERVERS": 2,
    "ADAWAY_HOSTS": 2,
    "STEVENBLACK_HOSTS": 1,
    "ADGUARD_BASE": 3,
}
MAX_SCORE = sum(SOURCE_WEIGHTS.values()) # 17

# Color-coded sources for better reporting/visualization
SOURCE_COLORS = {
    "HAGEZI_ULTIMATE": "#d62728", 
    "OISD_BIG": "#1f77b4",       
    "1HOSTS_LITE": "#2ca02c",    
    "STEVENBLACK_HOSTS": "#ff7f0e",
    "ANUDEEP_ADSERVERS": "#9467bd",
    "ADAWAY_HOSTS": "#8c564b",
    "ADGUARD_BASE": "#17becf",
}
ASCII_SPARKLINE_CHARS = " ▂▃▄▅▆▇█"

# --- Logging Setup ---
class ConsoleLogger:
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

def load_cache() -> Dict[str, Any]:
    """Loads fetch cache headers and file content from disk."""
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {"headers": {}, "content": {}}

def save_cache(cache_data: Dict[str, Any]):
    """Saves fetch cache headers and file content to disk."""
    try:
        CACHE_FILE.parent.mkdir(exist_ok=True)
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2)
    except Exception as e:
        logging.error(f"Failed to save fetch cache file: {e}")

# --- CACHE FUNCTIONS for Priority List Tracking ---

def load_priority_cache() -> Dict[str, Dict[str, Any]]:
    """Loads historical priority list data (score, sources) from disk."""
    if PRIORITY_CACHE_FILE.exists():
        try:
            with open(PRIORITY_CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {}

def save_priority_cache(priority_data: Dict[str, Dict[str, Any]]):
    """Saves the current priority list data for next run's comparison."""
    try:
        PRIORITY_CACHE_FILE.parent.mkdir(exist_ok=True)
        with open(PRIORITY_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(priority_data, f, indent=2)
    except Exception as e:
        logging.error(f"Failed to save priority cache file: {e}")

# --- END CACHE FUNCTIONS ---

def fetch_list(url: str, name: str, session: requests.Session, cache: Dict[str, Any], logger: ConsoleLogger) -> List[str]:
    """Fetches list with ETag/Last-Modified caching."""
    headers = {'User-Agent': 'SingularityDNSBlocklistAggregator/4.10'}
    
    cached_headers = cache.get("headers", {}).get(name, {})
    if 'ETag' in cached_headers:
        headers['If-None-Match'] = cached_headers['ETag']
    if 'Last-Modified' in cached_headers:
        headers['If-Modified-Since'] = cached_headers['Last-Modified']

    try:
        resp = session.get(url, timeout=45, headers=headers)
        resp.raise_for_status()

        if resp.status_code == 304:
            logger.info(f"⚡ Fetched {len(cache['content'].get(name, [])):,} domains from **{name}** (Cache: 304 Not Modified)")
            return cache['content'].get(name, [])

        content_lines = [l.strip().lower() for l in resp.text.splitlines() if l.strip()]
        
        cache['headers'][name] = {}
        if 'ETag' in resp.headers:
            cache['headers'][name]['ETag'] = resp.headers['ETag']
        if 'Last-Modified' in resp.headers:
            cache['headers'][name]['Last-Modified'] = resp.headers['Last-Modified']
            
        cache['content'][name] = content_lines
        
        return content_lines
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching {name} ({url}): {e.__class__.__name__}: {e}")
        return []

def process_domain(line: str) -> Optional[str]:
    """
    Cleans a line from a blocklist file, handles filter syntax, and explicitly rejects IP addresses.
    STRICTLY ensures only a clean domain (no rules, no IPs) is returned.
    """
    if not line:
        return None
    
    line = line.strip().lower()

    # 1. Ignore comment/empty lines, Whitelist/Exception rules
    # Lines starting with #, !, @@ are completely ignored.
    if line.startswith(("#", "!", "/")):
        return None
    
    # AdGuard exception/whitelist rule lines start with '@@' and should be IGNORED
    if line.startswith("@@"):
        return None

    domain = line
    
    # 2. Handle Hosts file (0.0.0.0 domain or 127.0.0.1 domain)
    parts = line.split()
    if len(parts) >= 2 and parts[0] in ("0.0.0.0", "127.0.0.1", "::"):
        # Take the second part as the domain candidate
        domain = parts[1]
    
    # 3. **AGGRESSIVE ABP/ADGUARD CLEANUP**
    # Remove filter rules that are attached to the domain
    for char in ['||', '^', '$', '/', '#', '@', '&', '%', '?', '~', '|']:
        domain = domain.replace(char, ' ').strip()
    
    # Take only the first word/token after aggressive cleanup
    domain_candidate = domain.split()[0] if domain else None

    if not domain_candidate: return None
    
    # Strip leading asterisks or dots (for wildcard format: *.domain.com)
    domain_candidate = domain_candidate.lstrip("*.").lstrip(".")

    # 4. Exclusion of reserved names AND IP ADDRESSES (CRITICAL CHECK)
    if domain_candidate in ("localhost", "localhost.localdomain", "::1", "255.255.255.255", "wpad"):
        return None
    
    # REJECT IPV4 ADDRESSES
    if IPV4_REGEX.match(domain_candidate):
        return None
    
    # 5. **STRICT REGEX VALIDATION** (Final safety net for domain format)
    if not DOMAIN_REGEX.match(domain_candidate):
        return None
    
    return domain_candidate

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
                    if history:
                        last_count = int(history[-1].get("Total_Unique_Domains", 0))
        except Exception as e:
            logger.error(f"Failed to read history file: {e}")

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
    except Exception as e:
        logger.error(f"Failed to write history file: {e}")

    return change, history

def generate_sparkline(values: List[int], logger: ConsoleLogger) -> str:
    """Generates an ASCII sparkline from a list of integer values."""
    if not values:
        return ""
    
    min_val = min(values)
    max_val = max(values)
    range_val = max_val - min_val
    num_chars = len(ASCII_SPARKLINE_CHARS) - 1
    
    if range_val == 0:
        return ASCII_SPARKLINE_CHARS[-1] * len(values)

    try:
        sparkline = ""
        for val in values:
            index = int((val - min_val) / range_val * num_chars)
            sparkline += ASCII_SPARKLINE_CHARS[index]
        return sparkline
    except Exception as e:
        logger.error(f"Sparkline generation failed: {e}")
        return "N/A"

# --- Core Processing Functions ---

def fetch_and_process_sources(session: requests.Session, logger: ConsoleLogger) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    """Fetches all blocklists concurrently and returns processed domain sets."""
    source_sets: Dict[str, Set[str]] = {}
    cache = load_cache()
    
    all_domains_from_sources: Dict[str, Set[str]] = defaultdict(set)
    
    max_workers = min(4, len(BLOCKLIST_SOURCES)) 
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_name = {
            executor.submit(fetch_list, url, name, session, cache, logger): name 
            for name, url in BLOCKLIST_SOURCES.items()
        }
        
        for future in future_to_name:
            name = future_to_name[future]
            try:
                lines = future.result()
                domains = {
                    d for d in (process_domain(l) for l in lines) if d
                }
                source_sets[name] = domains
                all_domains_from_sources[name] = domains
                # Report final count after processing
                logger.info(f"🌐 Processed {len(domains):,} unique domains from **{name}**")
            except Exception as exc:
                logger.error(f"Source {name} generated an exception: {exc}")
                source_sets[name] = set()
            
    save_cache(cache)
    
    return source_sets, all_domains_from_sources

def aggregate_and_score_domains(source_sets: Dict[str, Set[str]]) -> Tuple[Counter, Counter, Dict[str, Set[str]]]:
    """Combines all domains, scores them by weight, and tracks overlap/sources."""
    combined_counter = Counter()
    overlap_counter = Counter()
    domain_sources = defaultdict(set)

    for name, domains in source_sets.items():
        weight = SOURCE_WEIGHTS.get(name, 1)
        for d in domains:
            # combined_counter stores the WEIGHTED SCORE
            combined_counter[d] += weight 
            # overlap_counter stores the RAW COUNT of sources
            overlap_counter[d] += 1
            domain_sources[d].add(name)

    return combined_counter, overlap_counter, domain_sources

def filter_and_prioritize(
    combined_counter: Counter, 
    session: requests.Session, 
    logger: ConsoleLogger
) -> Tuple[Set[str], Set[str], int, List[str]]:
    """Filters domains by abused TLDs and selects the top-scoring domains."""
    
    tld_lines = fetch_list(HAGEZI_ABUSED_TLDS, "HAGEZI_TLDS", session, load_cache(), logger)
    abused_tlds = {l.strip().lower() for l in tld_lines if l and not l.startswith("#")}
    logger.info(f"🚫 Excluding domains with {len(abused_tlds)} known abusive TLDs.")
    
    filtered_weighted: List[Tuple[str, int]] = []
    excluded_count = 0
    
    for domain, weight in combined_counter.items():
        tld = extract_tld(domain)
        if tld in abused_tlds:
            excluded_count += 1
        else:
            filtered_weighted.append((domain, weight))
            
    filtered_weighted.sort(key=lambda x: x[1], reverse=True)
    
    final_priority = {d for d, _ in filtered_weighted[:PRIORITY_CAP]}
    full_filtered = [d for d, _ in filtered_weighted] 
    
    logger.info(f"🔥 Excluded {excluded_count:,} domains by TLD filter.")
    logger.info(f"💾 Priority list capped at {len(final_priority):,} domains.")
    
    return final_priority, abused_tlds, excluded_count, full_filtered

def calculate_source_metrics(
    priority_set: Set[str], 
    full_filtered: List[str], 
    overlap_counter: Counter,
    domain_sources: Dict[str, Set[str]],
    all_domains_from_sources: Dict[str, Set[str]]
) -> Dict[str, Dict[str, int]]:
    """Calculates contribution and uniqueness metrics per source."""
    metrics = defaultdict(lambda: defaultdict(int))
    
    for domain in full_filtered:
        sources = domain_sources[domain]
        
        if domain in priority_set:
            for source in sources:
                metrics[source]["In_Priority_List"] += 1
                
        if overlap_counter[domain] == 1:
            unique_source = list(sources)[0]
            metrics[unique_source]["Unique_to_Source"] += 1

    for name, domains in all_domains_from_sources.items():
         metrics[name]["Total_Fetched"] = len(domains)
            
    return dict(metrics)

# --- Core Function: Change Tracking ---

def track_priority_changes(
    current_priority_set: Set[str],
    current_combined_counter: Counter,
    current_domain_sources: Dict[str, Set[str]],
    logger: ConsoleLogger
) -> Dict[str, Dict[str, Any]]:
    """
    Compares the current priority list against the previous run's priority list 
    to track additions, removals, and changes in score/sources for domains that remained.
    """
    logger.info("🔄 Tracking Priority List changes against previous run...")
    
    previous_cache = load_priority_cache()
    
    previous_domains = set(previous_cache.keys())
    current_domains = current_priority_set
    
    # 1. Classify Changes
    added_domains = current_domains - previous_domains
    removed_domains = previous_domains - current_domains
    remained_domains = current_domains.intersection(previous_domains)
    
    change_report = {
        "added": [],
        "removed": [],
        "remained": []
    }
    
    # 2. Process Added Domains (Justification: New inclusion score/sources)
    for domain in sorted(list(added_domains)):
        current_score = current_combined_counter[domain]
        sources = sorted(list(current_domain_sources.get(domain, set())))
        change_report["added"].append({
            "domain": domain,
            "score": current_score,
            "sources": sources,
            "justification": f"New entry achieved score {current_score} to enter top {PRIORITY_CAP:,}."
        })

    # 3. Process Removed Domains (Justification: Decreased score or replaced)
    for domain in sorted(list(removed_domains)):
        prev_data = previous_cache.get(domain, {})
        prev_score = prev_data.get("score", 0)
        prev_sources = prev_data.get("sources", [])
        
        current_score = current_combined_counter.get(domain, 0)
        
        justification = ""
        if current_score == 0:
            justification = "Domain was removed from all source lists or blocked by TLD filter."
        elif current_score < prev_score:
            justification = f"Score dropped from {prev_score} to {current_score} and was replaced by a higher-scoring domain."
        else: # Score remained or increased, but still fell out of the top PRIORITY_CAP
             justification = f"Remained in the full list (Score {current_score}) but was pushed out of the top {PRIORITY_CAP:,} by new high-scoring entries."
        
        change_report["removed"].append({
            "domain": domain,
            "prev_score": prev_score,
            "prev_sources": prev_sources,
            "justification": justification
        })

    # 4. Process Remained Domains (Justification: Score/Source tracking)
    for domain in sorted(list(remained_domains)):
        prev_data = previous_cache.get(domain, {})
        prev_score = prev_data.get("score", 0)
        current_score = current_combined_counter[domain]
        
        score_change = current_score - prev_score
        
        change_report["remained"].append({
            "domain": domain,
            "score": current_score,
            "prev_score": prev_score,
            "score_change": f"{score_change:+}",
            "sources": sorted(list(current_domain_sources.get(domain, set()))),
            "justification": f"Score changed by {score_change:+}. Still retains a top spot."
        })
        
    logger.info(f"📊 Priority List Changes: Added {len(added_domains):,}, Removed {len(removed_domains):,}, Remained {len(remained_domains):,}")
    
    # 5. Prepare and save NEW cache for the NEXT run
    new_cache_data = {}
    for domain in current_priority_set:
        new_cache_data[domain] = {
            "score": current_combined_counter[domain],
            "sources": sorted(list(current_domain_sources.get(domain, set())))
        }
    save_priority_cache(new_cache_data)
    
    return change_report

# --- Reporting and Visualization ---

def generate_static_score_histogram(
    combined_counter: Counter,
    full_filtered: List[str],
    image_path: Path,
    logger: ConsoleLogger
) -> Path:
    """Generates a static PNG histogram showing the distribution of weighted scores."""
    logger.info(f"📊 Generating static score distribution histogram at {image_path.name}")
    
    # Extract scores only for domains in the full filtered list
    scores = [combined_counter[d] for d in full_filtered if combined_counter.get(d) is not None]
    
    # Get all possible score levels
    score_levels = sorted(list(set(scores)), reverse=True)

    # Create a trace for the histogram
    fig = go.Figure(data=[go.Histogram(
        x=scores,
        xbins=dict(
            start=0,
            end=MAX_SCORE + 1,
            size=1
        ),
        marker_color="#1f77b4"
    )])

    fig.update_layout(
        title='Weighted Score Distribution (All Filtered Domains)',
        xaxis=dict(title='Weighted Score', tickvals=score_levels),
        yaxis_title='Domain Count',
        bargap=0.05,
        template="plotly_dark"
    )

    pio.write_image(fig, str(image_path), scale=1.5, width=900, height=600)
    return image_path

def generate_interactive_dashboard(
    full_filtered: List[str], 
    combined_counter: Counter, 
    domain_sources: Dict[str, Set[str]],
    html_path: Path,
    logger: ConsoleLogger
):
    """
    Generates an interactive HTML page with a filterable table of all domains, 
    their scores, and sources.
    """
    logger.info(f"📈 Generating interactive filterable dashboard at {html_path.name}")
    
    # Prepare data for the HTML table
    table_data = []
    for domain in full_filtered:
        score = combined_counter.get(domain, 0)
        sources = sorted(list(domain_sources.get(domain, set())))
        table_data.append({
            "domain": domain,
            "score": score,
            "sources": ", ".join(sources)
        })

    # Sort data by score descending
    table_data.sort(key=lambda x: x["score"], reverse=True)
    
    table_rows = []
    for item in table_data:
        # Data attribute 'data-score' is key for filtering
        row = f'<tr data-score="{item["score"]}"><td>{item["domain"]}</td><td>{item["score"]}</td><td>{item["sources"]}</td></tr>'
        table_rows.append(row)

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Singularity DNS Interactive Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #2c3e50; color: #ecf0f1; padding: 20px; }}
        h1 {{ color: #3498db; }}
        #filter-container {{ margin-bottom: 20px; padding: 15px; border: 1px solid #34495e; border-radius: 5px; }}
        #domainTableContainer {{ max-height: 80vh; overflow-y: auto; background-color: #34495e; border-radius: 5px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #7f8c8d; }}
        th {{ background-color: #3498db; color: #fff; position: sticky; top: 0; }}
        input[type="number"] {{ padding: 8px; border-radius: 3px; border: 1px solid #ccc; width: 150px; background-color: #ecf0f1; color: #2c3e50; }}
    </style>
</head>
<body>

<h1>Singularity DNS: Filterable Domain List</h1>
<p>Total Filtered Domains: {len(table_data):,} | Max Score: {MAX_SCORE}</p>

<div id="filter-container">
    <label for="minScore">Filter by Minimum Weighted Score (1 to {MAX_SCORE}):</label>
    <input type="number" id="minScore" name="minScore" min="1" max="{MAX_SCORE}" value="1" onkeyup="filterTable()" onchange="filterTable()">
    <p>Showing <span id="domainCount">{len(table_data):,}</span> domains.</p>
</div>

<div id="domainTableContainer">
    <table id="domainTable">
        <thead>
            <tr>
                <th>Domain</th>
                <th>Weighted Score</th>
                <th>Sources</th>
            </tr>
        </thead>
        <tbody>
            {"".join(table_rows)}
        </tbody>
    </table>
</div>

<script>
    const tableBody = document.getElementById('domainTable').getElementsByTagName('tbody')[0];
    const minScoreInput = document.getElementById('minScore');
    const domainCountSpan = document.getElementById('domainCount');
    
    function filterTable() {{
        const minScore = parseInt(minScoreInput.value) || 1;
        let visibleCount = 0;

        for (const row of tableBody.rows) {{
            const rowScore = parseInt(row.getAttribute('data-score'));
            
            if (rowScore >= minScore) {{
                row.style.display = '';
                visibleCount++;
            }} else {{
                row.style.display = 'none';
            }}
        }}
        domainCountSpan.textContent = visibleCount.toLocaleString();
    }}

    // Initialize filter on load
    filterTable();
</script>

</body>
</html>
    """

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)


def generate_markdown_report(
    priority_count: int, 
    change: int, 
    total_unfiltered: int, 
    excluded_count: int, 
    full_filtered_list: List[str], 
    combined_counter: Counter, 
    overlap_counter: Counter, 
    report_path: Path,
    dashboard_html_path: Path,
    source_metrics: Dict[str, Dict[str, int]],
    history: List[Dict[str, str]],
    logger: ConsoleLogger,
    domain_sources: Dict[str, Set[str]],
    change_report: Dict[str, Dict[str, Any]],
):
    """Creates a detailed, aesthetic Markdown report with enhanced metrics."""
    logger.info(f"📝 Generating Markdown report at {report_path.name}")
    report: List[str] = []
    
    report.append(f"# 🛡️ Singularity DNS Blocklist Dashboard")
    report.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    trend_icon = "⬆️" if change > 0 else "⬇️" if change < 0 else "➡️"
    trend_color = "green" if change > 0 else "red" if change < 0 else "gray"
    
    high_consensus_count = sum(1 for d in full_filtered_list if combined_counter.get(d) >= CONSENSUS_THRESHOLD)
    
    # --- Historical Data ---
    report.append(f"\n## 📜 Historical Trends")
    
    history_counts = [int(h['Total_Unique_Domains']) for h in history][-7:]
    sparkline_str = generate_sparkline(history_counts, logger)
    history_dates = [h['Date'] for h in history][-7:]

    report.append(f"| Metric | Count | 7-Day Trend |")
    report.append("| :--- | :--- | :--- |")
    report.append(f"| **Total Unique Domains** | **{total_unfiltered:,}** | <span style='color:{trend_color};'>`{change:+}` {trend_icon}</span> &nbsp; **{sparkline_str}** |")
    report.append(f"| **Trend Window** | {history_dates[0]} to {history_dates[-1]} | |")
    
    report.append("\n## 🔑 Summary Metrics")
    report.append("| Metric | Count | Details |")
    report.append("| :--- | :--- | :--- |")
    
    report.append(f"| Domains with **High Consensus (Score {CONSENSUS_THRESHOLD}+)** | {high_consensus_count:,} | Highest consensus domains. |")
    
    report.append(f"| Domains Excluded by TLD Filter| {excluded_count:,} | TLD filter efficacy metric. |")
    report.append(f"| Priority List Size | {priority_count:,} | Capped domains selected from full list. |")

    report.append("\n---")
    
    # --- Priority List Change Tracking ---
    report.append("\n## 🔄 Priority List Changes (Top 300K)")
    report.append(f"| Change Type | Domain Count |")
    report.append("| :--- | :---: |")
    report.append(f"| **Domains Added** | {len(change_report['added']):,} |")
    report.append(f"| **Domains Removed** | {len(change_report['removed']):,} |")
    report.append(f"| **Domains Remained** | {len(change_report['remained']):,} |")

    # Details for Added Domains
    if change_report['added']:
        report.append("\n### 🟢 Newly Added Domains (Top 10 Samples)")
        report.append("| Domain | Score | Justification | Sources |")
        report.append("| :--- | :---: | :--- | :--- |")
        for entry in change_report['added'][:10]:
            sources_str = ", ".join(entry['sources'])
            report.append(f"| `{entry['domain']}` | {entry['score']} | {entry['justification']} | {sources_str} |")

    # Details for Removed Domains
    if change_report['removed']:
        report.append("\n### 🔴 Domains Removed (Top 10 Samples)")
        report.append("| Domain | Prev. Score | Justification | Prev. Sources |")
        report.append("| :--- | :---: | :--- | :--- |")
        for entry in change_report['removed'][:10]:
            sources_str = ", ".join(entry['prev_sources'])
            report.append(f"| `{entry['domain']}` | {entry['prev_score']} | {entry['justification']} | {sources_str} |")

    # Details for Remained Domains
    if change_report['remained']:
        report.append("\n### 🟡 Domains Remained (Score Tracking - Top 10 Samples)")
        report.append("| Domain | Score Change | Current Score | Justification |")
        report.append("| :--- | :---: | :---: | :--- |")
        remained_sorted = sorted(change_report['remained'], key=lambda x: abs(int(x['score_change'])), reverse=True)
        for entry in remained_sorted[:10]:
            report.append(f"| `{entry['domain']}` | **{entry['score_change']}** | {entry['score']} | {entry['justification']} |")
            
    report.append("\n---")

    # --- Source Performance Table ---
    report.append(f"\n## 🌐 Source Performance & Contribution")
    report.append("| Source | Weight | Total Fetched | In Priority List | % Contributed | Unique to Source | Color |")
    report.append("| :--- | :---: | :---: | :---: | :---: | :---: | :--- |")
    
    sorted_sources = sorted(BLOCKLIST_SOURCES.keys(), key=lambda n: SOURCE_WEIGHTS.get(n, 0), reverse=True)
    
    for name in sorted_sources:
        weight = SOURCE_WEIGHTS.get(name, 1)
        fetched_count = source_metrics.get(name, {}).get("Total_Fetched", 0)
        in_priority = source_metrics.get(name, {}).get("In_Priority_List", 0)
        unique_count = source_metrics.get(name, {}).get("Unique_to_Source", 0)
        
        total_in_filtered_from_source = sum(1 for d in full_filtered_list if name in domain_sources.get(d, set()))
        percent_contributed = f"{(in_priority / total_in_filtered_from_source * 100):.1f}%" if total_in_filtered_from_source > 0 else "0.0%"
        color = SOURCE_COLORS.get(name, "black")
        
        report.append(f"| **{name}** | {weight} | {fetched_count:,} | {in_priority:,} | {percent_contributed} | {unique_count:,} | <span style='color:{color};'>███</span> |")

    report.append("\n---")

    # --- Interactive Dashboard ---
    report.append("\n## 📈 Interactive Visualization")
    report.append(f"The **Score-filterable Domain List** is available at: [`dashboard.html`](dashboard.html)")
    report.append(f"\n### Static Score Distribution")
    report.append(f"![Weighted Score Distribution Histogram](score_distribution_chart.png)")
    
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
        f.writelines(d + "\n" for d in sorted(priority_set))
    
    # 2. Abused TLD Regex List
    regex_file = output_path / REGEX_TLD_FILENAME
    with open(regex_file, "w", encoding="utf-8") as f:
        f.write(f"# Hagezi Abused TLDs Regex List\n# Generated: {now_str}\n# Total: {len(abused_tlds):,}\n")
        f.writelines(f"\\.{t}$\n" for t in sorted(abused_tlds))
        
    # 3. Full Aggregated List
    unfiltered_file = output_path / UNFILTERED_FILENAME
    with open(unfiltered_file, "w", encoding="utf-8") as f:
        f.write(f"# Full Aggregated List (Filtered by TLDs, Sorted by Score)\n# Generated: {now_str}\n# Total: {len(full_list):,}\n")
        f.writelines(d + "\n" for d in full_list)
        
    logger.info(f"✅ Outputs written to: {output_path.resolve()}")

# --- Main Execution ---

def main():
    """Main function to run the aggregation process."""
    parser = argparse.ArgumentParser(description="Singularity DNS Blocklist Aggregator (v4.10)")
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
    output_path.mkdir(exist_ok=True)
    
    start = datetime.now()
    logger.info("--- 🚀 Starting Singularity DNS Aggregation (Interactive Dashboard Edition) ---")
    
    if not Path("requirements.txt").exists():
        logger.info("💡 Recommendation: Create a 'requirements.txt' file for dependency management and stability.")
    
    # === CRITICAL: SCOPE INITIALIZATION ===
    priority_set: Set[str] = set()
    abused_tlds: Set[str] = set()
    full_filtered: List[str] = []
    combined_counter: Counter = Counter()
    overlap_counter: Counter = Counter()
    domain_sources: Dict[str, Set[str]] = defaultdict(set)
    all_domains_from_sources: Dict[str, Set[str]] = defaultdict(set)
    total_unfiltered: int = 0
    excluded_count: int = 0 
    history: List[Dict[str, str]] = []
    change: int = 0
    change_report: Dict[str, Dict[str, Any]] = {"added": [], "removed": [], "remained": []} 
    # ======================================

    try:
        history_path = output_path / HISTORY_FILENAME
        report_path = output_path / REPORT_FILENAME
        # PNG name remains the same but content is different (histogram)
        image_path = output_path / "score_distribution_chart.png"
        dashboard_html_path = output_path / DASHBOARD_HTML
        
        with requests.Session() as session:
            # 1. Fetch & Process
            source_sets, all_domains_from_sources = fetch_and_process_sources(session, logger)
            
            # 2. Aggregate & Score
            combined_counter, overlap_counter, domain_sources = aggregate_and_score_domains(source_sets)
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
        change, history = track_history(total_unfiltered, history_path, logger)
        logger.info(f"📜 History tracked. Total unique list change vs. last run: {change:+}")
        
        source_metrics = calculate_source_metrics(priority_set, full_filtered, overlap_counter, domain_sources, all_domains_from_sources)
        
        # 5. Priority List Change Tracking
        change_report = track_priority_changes(
            priority_set,
            combined_counter,
            domain_sources,
            logger
        )

        # 6. Reporting & Visualization
        
        # New function for static histogram PNG
        generate_static_score_histogram(combined_counter, full_filtered, image_path, logger)
        
        # New function for interactive HTML table with filtering
        generate_interactive_dashboard(
            full_filtered, 
            combined_counter, 
            domain_sources,
            dashboard_html_path,
            logger
        )
        
        generate_markdown_report(
            priority_count, 
            change, 
            total_unfiltered, 
            excluded_count, 
            full_filtered, 
            combined_counter,
            overlap_counter, 
            report_path,
            dashboard_html_path,
            source_metrics,
            history,
            logger,
            domain_sources,
            change_report,
        )
        
        # 7. File Writing
        write_output_files(
            priority_set, 
            abused_tlds, 
            full_filtered, 
            output_path, 
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
    main()
