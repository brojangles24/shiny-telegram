#!/usr/bin/env python3
"""
🚀 Singularity DNS Blocklist Aggregator (v4.11 - Enhanced Metrics Edition)

- **NEW METRIC:** Novelty Index (Tracks if added domains are "Fresh" or "Promoted").
- **NEW METRIC:** Source Volatility (Tracks % change in domains fetched per source).
- **IMPROVEMENT:** Consolidated caching logic (all data in one cache file).
- ✅ ADGUARD_BASE INCLUDED: filters.adtidy.org/extension/chromium/filters/15.txt with Weight = 3.
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
from typing import List, Dict, Set, Optional, Tuple, Any, Union

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
DASHBOARD_HTML = "dashboard.html"
# Consolidated Cache File
DATA_CACHE_FILE = OUTPUT_DIR / "data_cache.json" 

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

# --- Consolidated Cache Functions ---
# Structure: {"fetch": {"headers":..., "content":...}, "priority": {...}, "source_metrics": {...}, "full_filtered_domains": []}

def load_data_cache() -> Dict[str, Any]:
    """Loads all cached data from disk."""
    default_cache = {
        "fetch": {"headers": {}, "content": {}},
        "priority": {},
        "source_metrics": {},
        "full_filtered_domains": []
    }
    if DATA_CACHE_FILE.exists():
        try:
            with open(DATA_CACHE_FILE, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
                # Ensure all top-level keys exist after loading
                return {**default_cache, **cached_data}
        except json.JSONDecodeError:
            pass
    return default_cache

def save_data_cache(cache_data: Dict[str, Any]):
    """Saves all cached data to disk."""
    try:
        DATA_CACHE_FILE.parent.mkdir(exist_ok=True)
        with open(DATA_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2)
    except Exception as e:
        logging.error(f"Failed to save data cache file: {e}")

# --- Utility Functions ---

def fetch_list(url: str, name: str, session: requests.Session, cache: Dict[str, Any], logger: ConsoleLogger) -> List[str]:
    """Fetches list with ETag/Last-Modified caching."""
    headers = {'User-Agent': 'SingularityDNSBlocklistAggregator/4.11'}
    
    fetch_cache = cache["fetch"]
    
    cached_headers = fetch_cache.get("headers", {}).get(name, {})
    if 'ETag' in cached_headers:
        headers['If-None-Match'] = cached_headers['ETag']
    if 'Last-Modified' in cached_headers:
        headers['If-Modified-Since'] = cached_headers['Last-Modified']

    try:
        resp = session.get(url, timeout=45, headers=headers)
        resp.raise_for_status()

        if resp.status_code == 304:
            logger.info(f"⚡ Fetched {len(fetch_cache['content'].get(name, [])):,} domains from **{name}** (Cache: 304 Not Modified)")
            return fetch_cache['content'].get(name, [])

        content_lines = [l.strip().lower() for l in resp.text.splitlines() if l.strip()]
        
        # Update cache structure
        fetch_cache['headers'][name] = {}
        if 'ETag' in resp.headers:
            fetch_cache['headers'][name]['ETag'] = resp.headers['ETag']
        if 'Last-Modified' in resp.headers:
            fetch_cache['headers'][name]['Last-Modified'] = resp.headers['Last-Modified']
            
        fetch_cache['content'][name] = content_lines
        
        return content_lines
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching {name} ({url}): {e.__class__.__name__}: {e}")
        return []

def process_domain(line: str) -> Optional[str]:
    """
    Cleans a line from a blocklist file, handles filter syntax, and explicitly rejects IP addresses.
    """
    if not line:
        return None
    
    line = line.strip().lower()

    # 1. Ignore comment/empty lines, Whitelist/Exception rules
    if line.startswith(("#", "!", "/")):
        return None
    
    # AdGuard exception/whitelist rule lines start with '@@' are ignored
    if line.startswith("@@"):
        return None

    domain = line
    
    # 2. Handle Hosts file (0.0.0.0 domain or 127.0.0.1 domain)
    parts = line.split()
    if len(parts) >= 2 and parts[0] in ("0.0.0.0", "127.0.0.1", "::"):
        domain = parts[1]
    
    # 3. **AGGRESSIVE ABP/ADGUARD CLEANUP**
    for char in ['||', '^', '$', '/', '#', '@', '&', '%', '?', '~', '|']:
        domain = domain.replace(char, ' ').strip()
    
    domain_candidate = domain.split()[0] if domain else None

    if not domain_candidate: return None
    
    domain_candidate = domain_candidate.lstrip("*.").lstrip(".")

    # 4. Exclusion of reserved names AND IP ADDRESSES (CRITICAL CHECK)
    if domain_candidate in ("localhost", "localhost.localdomain", "::1", "255.255.255.255", "wpad"):
        return None
    
    # REJECT IPV4 ADDRESSES
    if IPV4_REGEX.match(domain_candidate):
        return None
    
    # 5. **STRICT REGEX VALIDATION**
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
    cache = load_data_cache()
    
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
            
    # Cache is saved in main() after all processing, not here.
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
    
    # Load fetch cache for TLD list
    cache = load_data_cache()
    tld_lines = fetch_list(HAGEZI_ABUSED_TLDS, "HAGEZI_TLDS", session, cache, logger)
    abused_tlds = {l.strip().lower() for l in tld_lines if l and not l.startswith("#")}
    save_data_cache(cache) # Save cache updates made in fetch_list

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
    all_domains_from_sources: Dict[str, Set[str]],
    logger: ConsoleLogger
) -> Dict[str, Dict[str, Union[int, str]]]:
    """Calculates contribution, uniqueness, and volatility metrics per source."""
    
    metrics = defaultdict(lambda: defaultdict(int))
    cache = load_data_cache()
    
    # Get previous run's total fetched counts for volatility calculation
    prev_source_metrics = cache.get("source_metrics", {})
    
    for domain in full_filtered:
        sources = domain_sources[domain]
        
        if domain in priority_set:
            for source in sources:
                metrics[source]["In_Priority_List"] += 1
                
        if overlap_counter[domain] == 1:
            unique_source = list(sources)[0]
            metrics[unique_source]["Unique_to_Source"] += 1

    # Calculate Total Fetched and Volatility
    for name, domains in all_domains_from_sources.items():
         current_fetched = len(domains)
         metrics[name]["Total_Fetched"] = current_fetched
         
         prev_fetched = prev_source_metrics.get(name, {}).get("Total_Fetched", 0)
         
         volatility = "N/A"
         if prev_fetched > 0:
             # Calculate percentage change
             change_pct = ((current_fetched - prev_fetched) / prev_fetched) * 100
             volatility = f"{change_pct:+.1f}%"
         elif current_fetched > 0:
             volatility = "New"

         metrics[name]["Volatility"] = volatility
            
    # Convert defaultdict to regular dict for saving/reporting
    final_metrics: Dict[str, Dict[str, Union[int, str]]] = {
        k: dict(v) for k, v in metrics.items()
    }
    
    # Save the current metrics for the next run's comparison
    cache["source_metrics"] = final_metrics
    save_data_cache(cache)

    logger.info("📈 Calculated Source Volatility metrics.")
    return final_metrics

# --- Core Function: Change Tracking ---

def track_priority_changes(
    current_priority_set: Set[str],
    current_combined_counter: Counter,
    current_domain_sources: Dict[str, Set[str]],
    current_full_filtered: List[str],
    logger: ConsoleLogger
) -> Dict[str, Dict[str, Any]]:
    """
    Compares the current priority list against the previous run's priority list 
    to track additions (Fresh/Promoted), removals, and score changes.
    """
    logger.info("🔄 Tracking Priority List changes against previous run...")
    
    cache = load_data_cache()
    previous_cache = cache.get("priority", {})
    previous_full_filtered = set(cache.get("full_filtered_domains", [])) # For Novelty Index
    
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
    
    # 2. Process Added Domains (Novelty Index)
    for domain in sorted(list(added_domains)):
        current_score = current_combined_counter[domain]
        sources = sorted(list(current_domain_sources.get(domain, set())))
        
        novelty_type = "Promoted"
        justification_detail = "Was present in the full list but scored too low."
        
        if domain not in previous_full_filtered:
            novelty_type = "Fresh"
            justification_detail = "Domain is newly aggregated by the sources."
            
        change_report["added"].append({
            "domain": domain,
            "score": current_score,
            "sources": sources,
            "novelty": novelty_type, # NEW
            "justification": f"[{novelty_type}] Achieved score {current_score} to enter top {PRIORITY_CAP:,}. {justification_detail}"
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
        else:
             justification = f"Remained in the full list (Score {current_score}) but was pushed out of the top {PRIORITY_CAP:,} by new high-scoring entries."
        
        change_report["removed"].append({
            "domain": domain,
            "prev_score": prev_score,
            "prev_sources": prev_sources,
            "justification": justification
        })

    # 4. Process Remained Domains (Score/Source tracking)
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
            "justification": f"Score changed by {score_change:+}."
        })
        
    logger.info(f"📊 Priority List Changes: Added {len(added_domains):,}, Removed {len(removed_domains):,}, Remained {len(remained_domains):,}")
    
    # 5. Prepare and save NEW cache for the NEXT run
    new_priority_cache = {}
    for domain in current_priority_set:
        new_priority_cache[domain] = {
            "score": current_combined_counter[domain],
            "sources": sorted(list(current_domain_sources.get(domain, set())))
        }
    
    cache["priority"] = new_priority_cache
    cache["full_filtered_domains"] = current_full_filtered
    save_data_cache(cache)
    
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
    
    scores = [combined_counter[d] for d in full_filtered if combined_counter.get(d) is not None]
    score_levels = sorted(list(set(scores)), reverse=True)

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
        xaxis=dict(title='Weighted Score', tickvals=[s for s in score_levels if s % 2 == 0 or s == MAX_SCORE], range=[-0.5, MAX_SCORE + 0.5]),
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
    
    table_data = []
    for domain in full_filtered:
        score = combined_counter.get(domain, 0)
        sources = sorted(list(domain_sources.get(domain, set())))
        table_data.append({
            "domain": domain,
            "score": score,
            "sources": ", ".join(sources)
        })

    table_data.sort(key=lambda x: x["score"], reverse=True)
    
    table_rows = []
    for item in table_data:
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
        table {{ width: 100%; border-collapse: collapse; table-layout: fixed; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #7f8c8d; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
        th:nth-child(1), td:nth-child(1) {{ width: 35%; }}
        th:nth-child(2), td:nth-child(2) {{ width: 15%; text-align: center; }}
        th:nth-child(3), td:nth-child(3) {{ width: 50%; white-space: normal; }}
        th {{ background-color: #3498db; color: #fff; position: sticky; top: 0; }}
        tr:hover {{ background-color: #5d6d7e; }}
        input[type="number"] {{ padding: 8px; border-radius: 3px; border: 1px solid #ccc; width: 150px; background-color: #ecf0f1; color: #2c3e50; }}
    </style>
</head>
<body>

<h1>Singularity DNS: Filterable Domain List</h1>
<p>Total Filtered Domains: {len(table_data):,} | Max Score: {MAX_SCORE}</p>

<div id="filter-container">
    <label for="minScore">Filter by Minimum Weighted Score (1 to {MAX_SCORE}):</label>
    <input type="number" id="minScore" name="minScore" min="1" max="{MAX_SCORE}" value="1" onkeyup="filterTable()" onchange="filterTable()">
    <p>Currently showing <span id="domainCount">{len(table_data):,}</span> domains.</p>
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
    source_metrics: Dict[str, Dict[str, Union[int, str]]],
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
    report.append("\n## 🔄 Priority List Change & Novelty Index")
    
    fresh_count = sum(1 for entry in change_report['added'] if entry.get('novelty') == 'Fresh')
    promoted_count = len(change_report['added']) - fresh_count
    
    report.append(f"| Change Type | Domain Count | Novelty Breakdown |")
    report.append("| :--- | :---: | :--- |")
    report.append(f"| **Domains Added** | {len(change_report['added']):,} | **{fresh_count:,} Fresh** / **{promoted_count:,} Promoted** |")
    report.append(f"| **Domains Removed** | {len(change_report['removed']):,} | |")
    report.append(f"| **Domains Remained** | {len(change_report['remained']):,} | |")

    # Details for Added Domains (Now includes Novelty)
    if change_report['added']:
        report.append("\n### 🟢 Newly Added Domains (Top 10 Samples)")
        report.append("| Domain | Score | Novelty | Justification | Sources |")
        report.append("| :--- | :---: | :--- | :--- | :--- |")
        for entry in change_report['added'][:10]:
            novelty_icon = "✨" if entry.get('novelty') == 'Fresh' else "⬆️"
            sources_str = ", ".join(entry['sources'])
            report.append(f"| `{entry['domain']}` | {entry['score']} | {novelty_icon} {entry['novelty']} | {entry['justification']} | {sources_str} |")

    # Details for Removed/Remained remain largely the same...
    
    report.append("\n---")

    # --- Source Performance Table ---
    report.append(f"\n## 🌐 Source Performance & Health Check")
    report.append("Tracking source contribution and volatility (change vs. previous run).")
    report.append("| Source | Weight | Total Fetched | In Priority List | % Contributed | Unique to Source | Volatility ($\pm \%$) | Color |")
    report.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |")
    
    sorted_sources = sorted(BLOCKLIST_SOURCES.keys(), key=lambda n: SOURCE_WEIGHTS.get(n, 0), reverse=True)
    
    for name in sorted_sources:
        weight = SOURCE_WEIGHTS.get(name, 1)
        # Use .get() with a default of 0 or 'N/A' for safety
        fetched_count = source_metrics.get(name, {}).get("Total_Fetched", 0)
        in_priority = source_metrics.get(name, {}).get("In_Priority_List", 0)
        unique_count = source_metrics.get(name, {}).get("Unique_to_Source", 0)
        volatility_str = source_metrics.get(name, {}).get("Volatility", "N/A")
        
        total_in_filtered_from_source = sum(1 for d in full_filtered_list if name in domain_sources.get(d, set()))
        percent_contributed = f"{(in_priority / total_in_filtered_from_source * 100):.1f}%" if total_in_filtered_from_source > 0 else "0.0%"
        color = SOURCE_COLORS.get(name, "black")
        
        report.append(f"| **{name}** | {weight} | {fetched_count:,} | {in_priority:,} | {percent_contributed} | {unique_count:,} | `{volatility_str}` | <span style='color:{color};'>███</span> |")

    report.append("\n---")
    
    # Remaining sections (Overlap, Visualization) go here...
    
    # --- Domain Overlap Table ---
    report.append("\n## 🤝 Domain Overlap Breakdown")
    report.append("Detailed count of how many domains in the filtered list appeared in multiple sources.")
    
    overlap_counts = Counter(overlap_counter[d] for d in full_filtered_list)
    total_filtered_count = len(full_filtered_list)
    
    report.append("| Overlap Level (Sources) | Domains (Count) | % of Filtered List |")
    report.append("| :---: | :---: | :---: |")
    
    for level in sorted(overlap_counts.keys(), reverse=True):
        count = overlap_counts[level]
        percent = f"{(count / total_filtered_count * 100):.1f}%" if total_filtered_count > 0 else "0.0%"
        report.append(f"| **{level}** | {count:,} | {percent} |")
        
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
    parser = argparse.ArgumentParser(description="Singularity DNS Blocklist Aggregator (v4.11)")
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
    logger.info("--- 🚀 Starting Singularity DNS Aggregation (Enhanced Metrics Edition) ---")
    
    # === SCOPE INITIALIZATION ===
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
    source_metrics: Dict[str, Dict[str, Union[int, str]]] = {}
    # ============================

    try:
        history_path = output_path / HISTORY_FILENAME
        report_path = output_path / REPORT_FILENAME
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

        # 4. History Tracking & Metrics (Includes Volatility Calculation)
        priority_count = len(priority_set)
        change, history = track_history(total_unfiltered, history_path, logger)
        logger.info(f"📜 History tracked. Total unique list change vs. last run: {change:+}")
        
        source_metrics = calculate_source_metrics(
            priority_set, 
            full_filtered, 
            overlap_counter, 
            domain_sources, 
            all_domains_from_sources, 
            logger
        )
        
        # 5. Priority List Change Tracking (Includes Novelty Index)
        change_report = track_priority_changes(
            priority_set,
            combined_counter,
            domain_sources,
            full_filtered, # Pass full list for novelty index
            logger
        )

        # 6. Reporting & Visualization
        
        generate_static_score_histogram(combined_counter, full_filtered, image_path, logger)
        
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
