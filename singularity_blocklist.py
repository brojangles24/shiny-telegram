#!/usr/bin/env python3
"""
🚀 Singularity DNS Blocklist Aggregator (v5.3 - Ultimate Report Edition)

- **FINALIZED:** All advanced features (Async, Verbose, Dynamic Cap, IDN, Archiving) integrated.
- **IMPROVEMENT:** Enhanced Metric Readability and Insight in Markdown Report (Top Excluded Domains).
"""
import sys
import csv
import logging
import argparse
import json
import re
import asyncio
from datetime import datetime, timedelta # Added timedelta for cleanup
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple, Any, Union

import requests
import aiohttp 
import plotly.graph_objects as go
import plotly.io as pio
import idna 

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
DASHBOARD_HTML = "dashboard.html"
DATA_CACHE_FILE = OUTPUT_DIR / "data_cache.json" 
VERBOSE_EXCLUSION_FILE = "excluded_domains_report.csv" 

# Scoring and style
PRIORITY_CAP_DEFAULT = 300_000 
MAX_WORKERS_DEFAULT = 8
CONSENSUS_THRESHOLD = 6 
MAX_FETCH_RETRIES = 3 
CACHE_CLEANUP_DAYS = 30 # For the new cleanup feature

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

# --- Consolidated Cache Functions ---

def load_data_cache() -> Dict[str, Any]:
    """Loads all cached data from disk."""
    default_cache = {
        "fetch": {"headers": {}, "content": {}}, "priority": {},
        "source_metrics": {}, "full_filtered_domains": []
    }
    if DATA_CACHE_FILE.exists():
        try:
            with open(DATA_CACHE_FILE, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
                return {**default_cache, **cached_data}
        except json.JSONDecodeError: pass
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

# SMART FALLBACK/RETRY LOGIC implemented here
async def fetch_list(session: aiohttp.ClientSession, url: str, name: str, cache: Dict[str, Any], logger: ConsoleLogger) -> List[str]:
    """Fetches list with ETag/Last-Modified caching using aiohttp and retries."""
    headers = {'User-Agent': 'SingularityDNSBlocklistAggregator/5.3'}
    fetch_cache = cache["fetch"]
    
    cached_headers = fetch_cache.get("headers", {}).get(name, {})
    if 'ETag' in cached_headers: headers['If-None-Match'] = cached_headers['ETag']
    if 'Last-Modified' in cached_headers: headers['If-Modified-Since'] = cached_headers['Last-Modified']

    for attempt in range(MAX_FETCH_RETRIES):
        try:
            async with session.get(url, timeout=30 + attempt * 10, headers=headers) as resp:
                resp.raise_for_status()

                if resp.status == 304:
                    logger.info(f"⚡ Fetched {len(fetch_cache['content'].get(name, [])):,} domains from **{name}** (Cache: 304 Not Modified)")
                    return fetch_cache['content'].get(name, [])

                content = await resp.text()
                content_lines = [l.strip().lower() for l in content.splitlines() if l.strip()]
                
                # Update cache structure
                fetch_cache['headers'][name] = {}
                if 'ETag' in resp.headers: fetch_cache['headers'][name]['ETag'] = resp.headers['ETag']
                if 'Last-Modified' in resp.headers: fetch_cache['headers'][name]['Last-Modified'] = resp.headers['Last-Modified']
                    
                fetch_cache['content'][name] = content_lines
                return content_lines
                
        except aiohttp.client_exceptions.ClientError as e:
            logger.error(f"Error fetching {name} (Attempt {attempt+1}/{MAX_FETCH_RETRIES}): {e.__class__.__name__}: {e}")
            if attempt < MAX_FETCH_RETRIES - 1:
                await asyncio.sleep(2 * (attempt + 1)) # Exponential backoff
        except Exception as e:
            logger.error(f"Unexpected error for {name}: {e}")
            break # Exit retry loop on unexpected errors

    # Fallback if all retries fail
    cached_content = fetch_cache['content'].get(name, [])
    if cached_content:
        logger.error(f"❌ All attempts failed for {name}. Falling back to cached content ({len(cached_content):,} domains).")
        return cached_content
    
    logger.error(f"❌ All attempts failed for {name}. No cached content found. Returning empty list.")
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

# --- Core Processing Functions ---

async def fetch_and_process_sources_async(max_workers: int, logger: ConsoleLogger) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    """Manages concurrent fetching of all blocklists using aiohttp."""
    source_sets: Dict[str, Set[str]] = {}
    all_domains_from_sources: Dict[str, Set[str]] = defaultdict(set)
    cache = load_data_cache()
    
    conn = aiohttp.TCPConnector(limit=max_workers)
    
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = [fetch_list(session, url, name, cache, logger) for name, url in BLOCKLIST_SOURCES.items()]
        results = await asyncio.gather(*tasks)

        for i, lines in enumerate(results):
            name = list(BLOCKLIST_SOURCES.keys())[i]
            domains = {d for d in (process_domain(l) for l in lines) if d}
            source_sets[name] = domains
            all_domains_from_sources[name] = domains
            logger.info(f"🌐 Processed {len(domains):,} unique domains from **{name}**")
            
    save_data_cache(cache)
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
    """Filters domains by abused TLDs, selects top-scoring domains, and tracks excluded TLDs."""
    
    tld_lines = requests.get(HAGEZI_ABUSED_TLDS, timeout=45, headers={'User-Agent': 'SingularityDNSBlocklistAggregator/5.3'}).text.splitlines()
    abused_tlds = {l.strip().lower() for l in tld_lines if l.strip() and not l.startswith("#")}

    logger.info(f"🚫 Excluding domains with {len(abused_tlds)} known abusive TLDs.")
    
    filtered_weighted: List[Tuple[str, int]] = []
    excluded_count = 0
    tld_exclusion_counter = Counter() 
    excluded_domains_verbose: List[Dict[str, Any]] = []

    for domain, weight in combined_counter.items():
        tld = extract_tld(domain)
        
        if tld in abused_tlds:
            excluded_count += 1
            tld_exclusion_counter[tld] += 1 
            excluded_domains_verbose.append({
                'domain': domain, 'score': weight, 'status': 'TLD EXCLUDED',
                'reason': f'TLD .{tld} is marked as abusive.'
            })
        else:
            filtered_weighted.append((domain, weight))
            
    filtered_weighted.sort(key=lambda x: x[1], reverse=True)
    
    final_priority = {d for d, _ in filtered_weighted[:priority_cap]}
    full_filtered = [d for d, _ in filtered_weighted] 
    
    for domain, score in filtered_weighted[priority_cap:]:
        excluded_domains_verbose.append({
            'domain': domain, 'score': score, 'status': 'SCORE CUTOFF',
            'reason': f'Scored {score} but did not make the top {priority_cap:,} list.'
        })

    logger.info(f"🔥 Excluded {excluded_count:,} domains by TLD filter.")
    logger.info(f"💾 Priority list capped at {len(final_priority):,} domains.")
    
    return final_priority, abused_tlds, excluded_count, full_filtered, tld_exclusion_counter, excluded_domains_verbose

def calculate_source_metrics(
    priority_set: Set[str], full_filtered: List[str], overlap_counter: Counter,
    domain_sources: Dict[str, Set[str]], all_domains_from_sources: Dict[str, Set[str]], logger: ConsoleLogger
) -> Dict[str, Dict[str, Union[int, str]]]:
    """Calculates contribution, uniqueness, and volatility metrics per source."""
    
    metrics = defaultdict(lambda: defaultdict(int))
    cache = load_data_cache()
    prev_source_metrics = cache.get("source_metrics", {})
    
    for domain in full_filtered:
        sources = domain_sources[domain]
        if domain in priority_set:
            for source in sources: metrics[source]["In_Priority_List"] += 1
        if overlap_counter[domain] == 1:
            unique_source = list(sources)[0]
            metrics[unique_source]["Unique_to_Source"] += 1

    for name, domains in all_domains_from_sources.items():
         current_fetched = len(domains)
         metrics[name]["Total_Fetched"] = current_fetched
         prev_fetched = prev_source_metrics.get(name, {}).get("Total_Fetched", 0)
         
         volatility = "N/A"
         if prev_fetched > 0:
             change_pct = ((current_fetched - prev_fetched) / prev_fetched) * 100
             volatility = f"{change_pct:+.1f}"
         elif current_fetched > 0:
             volatility = "New"

         metrics[name]["Volatility"] = volatility
            
    final_metrics: Dict[str, Dict[str, Union[int, str]]] = {k: dict(v) for k, v in metrics.items()}
    
    cache["source_metrics"] = final_metrics
    save_data_cache(cache)

    logger.info("📈 Calculated Source Volatility metrics.")
    return final_metrics

# --- Core Function: Change Tracking ---

def track_priority_changes(
    current_priority_set: Set[str], current_combined_counter: Counter,
    current_domain_sources: Dict[str, Set[str]], current_full_filtered: List[str], logger: ConsoleLogger
) -> Dict[str, Dict[str, Any]]:
    """Compares the current priority list against the previous run's priority list."""
    logger.info("🔄 Tracking Priority List changes against previous run...")
    
    cache = load_data_cache()
    previous_cache = cache.get("priority", {})
    previous_full_filtered = set(cache.get("full_filtered_domains", [])) 
    
    previous_domains = set(previous_cache.keys())
    current_domains = current_priority_set
    
    added_domains = current_domains - previous_domains
    removed_domains = previous_domains - current_domains
    remained_domains = current_domains.intersection(previous_domains)
    
    change_report = {"added": [], "removed": [], "remained": []}
    
    for domain in sorted(list(added_domains)):
        current_score = current_combined_counter[domain]
        sources = sorted(list(current_domain_sources.get(domain, set())))
        novelty_type = "Promoted" if domain in previous_full_filtered else "Fresh"
        justification_detail = "Was present in the full list but scored too low." if novelty_type == "Promoted" else "Domain is newly aggregated by the sources."
            
        change_report["added"].append({
            "domain": domain, "score": current_score, "sources": sources, "novelty": novelty_type,
            "justification": f"[{novelty_type}] Achieved score {current_score} to enter top {len(current_priority_set):,}."
        })

    for domain in sorted(list(removed_domains)):
        prev_data = previous_cache.get(domain, {})
        prev_score = prev_data.get("score", 0)
        prev_sources = prev_data.get("sources", [])
        current_score = current_combined_counter.get(domain, 0)
        
        justification = ""
        if current_score == 0: justification = "Domain was removed from all source lists or blocked by TLD filter."
        elif current_score < prev_score: justification = f"Score dropped from {prev_score} to {current_score} and was replaced by a higher-scoring domain."
        else: justification = f"Remained in the full list (Score {current_score}) but was pushed out of the top {len(current_priority_set):,} by new high-scoring entries."
        
        change_report["removed"].append({
            "domain": domain, "prev_score": prev_score, "prev_sources": prev_sources, "justification": justification
        })

    for domain in sorted(list(remained_domains)):
        prev_score = previous_cache.get(domain, {}).get("score", 0)
        current_score = current_combined_counter[domain]
        score_change = current_score - prev_score
        
        change_report["remained"].append({
            "domain": domain, "score": current_score, "prev_score": prev_score, "score_change": f"{score_change:+}",
            "sources": sorted(list(current_domain_sources.get(domain, set()))), "justification": f"Score changed by {score_change:+}. Still retains a top spot."
        })
        
    logger.info(f"📊 Priority List Changes: Added {len(added_domains):,}, Removed {len(removed_domains):,}, Remained {len(remained_domains):,}")
    
    new_priority_cache = {d: {"score": current_combined_counter[d], "sources": sorted(list(current_domain_sources.get(d, set())))} 
                          for d in current_priority_set}
    
    cache["priority"] = new_priority_cache
    cache["full_filtered_domains"] = current_full_filtered
    save_data_cache(cache)
    
    return change_report

# --- Reporting and Visualization ---

def generate_static_score_histogram(
    combined_counter: Counter, full_filtered: List[str], image_path: Path, logger: ConsoleLogger
) -> Path:
    """Generates a static PNG histogram showing the distribution of weighted scores."""
    logger.info(f"📊 Generating static score distribution histogram at {image_path.name}")
    scores = [combined_counter[d] for d in full_filtered if combined_counter.get(d) is not None]
    score_levels = sorted(list(set(scores)), reverse=True)

    fig = go.Figure(data=[go.Histogram(
        x=scores, xbins=dict(start=0, end=MAX_SCORE + 1, size=1), marker_color="#1f77b4"
    )])

    fig.update_layout(
        title='Weighted Score Distribution (All Filtered Domains)',
        xaxis=dict(title='Weighted Score', tickvals=[s for s in score_levels if s % 2 == 0 or s == MAX_SCORE], range=[-0.5, MAX_SCORE + 0.5]),
        yaxis_title='Domain Count', bargap=0.05, template="plotly_dark"
    )

    pio.write_image(fig, str(image_path), scale=1.5, width=900, height=600)
    return image_path

def generate_interactive_dashboard(
    full_filtered: List[str], combined_counter: Counter, domain_sources: Dict[str, Set[str]],
    html_path: Path, logger: ConsoleLogger
):
    """Generates an interactive HTML page with a filterable table, including Source Category."""
    logger.info(f"📈 Generating interactive filterable dashboard at {html_path.name}")
    
    table_data = []
    for domain in full_filtered:
        score = combined_counter.get(domain, 0)
        sources = sorted(list(domain_sources.get(domain, set())))
        categories = [SOURCE_CATEGORIES.get(s, "Other") for s in sources]
        
        table_data.append({
            "domain": domain, "score": score, "sources": ", ".join(sources),
            "categories": ", ".join(sorted(list(set(categories))))
        })

    table_data.sort(key=lambda x: x["score"], reverse=True)
    
    table_rows = []
    for item in table_data:
        row = (
            f'<tr data-score="{item["score"]}"><td>{item["domain"]}</td><td>{item["score"]}</td>'
            f'<td>{item["categories"]}</td><td>{item["sources"]}</td></tr>'
        )
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
        th:nth-child(1), td:nth-child(1) {{ width: 30%; }} /* Domain */
        th:nth-child(2), td:nth-child(2) {{ width: 10%; text-align: center; }} /* Score */
        th:nth-child(3), td:nth-child(3) {{ width: 25%; }} /* Category */
        th:nth-child(4), td:nth-child(4) {{ width: 35%; white-space: normal; }} /* Sources */
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
                <th>Score</th>
                <th>Categories</th>
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

    filterTable();
</script>

</body>
</html>
    """

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

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

def generate_markdown_report(
    priority_count: int, change: int, total_unfiltered: int, excluded_count: int, 
    full_filtered_list: List[str], combined_counter: Counter, overlap_counter: Counter, 
    report_path: Path, dashboard_html_path: Path, source_metrics: Dict[str, Dict[str, Union[int, str]]],
    history: List[Dict[str, str]], logger: ConsoleLogger, domain_sources: Dict[str, Set[str]],
    change_report: Dict[str, Dict[str, Any]], tld_exclusion_counter: Counter, priority_cap_val: int,
    excluded_domains_verbose: List[Dict[str, Any]] # ADDED ARGUMENT
):
    """Creates a detailed, aesthetic Markdown report with enhanced metrics."""
    logger.info(f"📝 Generating Markdown report at {report_path.name}")
    report: List[str] = []
    
    report.append(f"# 🛡️ Singularity DNS Blocklist Dashboard")
    report.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    trend_icon = "⬆️" if change > 0 else "⬇️" if change < 0 else "➡️"
    trend_color = "green" if change > 0 else "red" if change < 0 else "gray"
    high_consensus_count = sum(1 for d in full_filtered_list if combined_counter.get(d) >= CONSENSUS_THRESHOLD)
    
    # --- Historical Data & Summary Metrics ---
    report.append(f"\n## 📜 Aggregation Summary")
    
    # Combined Summary/Historical Table
    report.append("| Metric | Count | Insight |")
    report.append("| :--- | :---: | :--- |")
    report.append(f"| **Total Unique Domains** | **{total_unfiltered:,}** | Overall size of the unfiltered, validated pool. |")
    report.append(f"| Change vs. Last Run | `{change:+}` {trend_icon} | Trend in the total unique domain pool. |")
    report.append(f"| Priority List Size | {priority_count:,} | Capped domains selected (Cap: **{priority_cap_val:,}**). |")
    report.append(f"| High Consensus (Score {CONSENSUS_THRESHOLD}+) | {high_consensus_count:,} | Domains backed by strong weighted evidence. |")
    report.append(f"| TLD Filter Exclusions | {excluded_count:,} | Domains rejected by the abusive TLD list. |")
    
    report.append("\n---")
    
    # --- NEW: Top Excluded Domains Table (Readability Fix) ---
    if excluded_domains_verbose:
        report.append("\n## ⚠️ Top Excluded Domains for Audit (High Score / TLD Rejection)")

        tld_excluded = [d for d in excluded_domains_verbose if d['status'] == 'TLD EXCLUDED']
        score_excluded = [d for d in excluded_domains_verbose if d['status'] == 'SCORE CUTOFF']
        
        samples_to_show = []
        
        # Take up to 5 highest-scoring TLD-excluded domains
        for d in tld_excluded:
            samples_to_show.append({
                'domain': d['domain'],
                'score': d['score'],
                'reason': f"TLD Rejected: **{d['reason'].split('TLD ')[1]}**"
            })
            
        # Take up to 5 highest-scoring domains that missed the cutoff
        for d in score_excluded:
             samples_to_show.append({
                'domain': d['domain'],
                'score': d['score'],
                'reason': f"Score Cutoff: **Needed >{priority_cap_val:,}**"
            })
        
        # Sort by score and take the absolute top 10
        samples_to_show.sort(key=lambda x: x['score'], reverse=True)

        if samples_to_show:
            report.append("These are the highest-scoring domains that failed to make the final list:")
            report.append("| Domain | Weighted Score | Exclusion Reason |")
            report.append("| :--- | :---: | :--- |")
            
            for item in samples_to_show[:10]:
                # Apply color based on reason for immediate attention
                reason_color = "red" if "TLD Rejected" in item['reason'] else "orange"
                report.append(f"| `{item['domain']}` | <span style='color:{reason_color};'>**{item['score']}**</span> | {item['reason']} |")
        
        report.append(f"\n*The complete list of {len(excluded_domains_verbose):,} excluded domains is available in `{VERBOSE_EXCLUSION_FILE}` for deeper analysis.*")
        report.append("\n---")
    
    
    # --- TLD Exclusion Frequency Table ---
    if tld_exclusion_counter:
        report.append("\n## 🚫 Top 10 Abusive TLD Trends")
        report.append("| Rank | Abusive TLD | Excluded Domain Count |")
        report.append("| :---: | :--- | :---: |")
        for rank, (tld, count) in enumerate(tld_exclusion_counter.most_common(10)):
            report.append(f"| {rank + 1} | **.{tld}** | {count:,} |")
        report.append("\n---")
    
    # --- Priority List Change Tracking ---
    report.append("\n## 🔄 Priority List Change & Novelty Index")
    
    fresh_count = sum(1 for entry in change_report['added'] if entry.get('novelty') == 'Fresh')
    promoted_count = len(change_report['added']) - fresh_count
    
    report.append(f"| Change Type | Domain Count | Novelty Breakdown |")
    report.append("| :--- | :---: | :--- |")
    report.append(f"| **Domains Added** | {len(change_report['added']):,} | **{fresh_count:,} Fresh** ✨ / **{promoted_count:,} Promoted** ⬆️ |")
    
    # --- Source Performance Table (Category & Color-Coded Volatility) ---
    report.append("\n## 🌐 Source Performance & Health Check")
    report.append("| Source | Category | Weight | Total Fetched | In Priority List | Volatility ($\pm \%$) | Color |")
    report.append("| :--- | :--- | :---: | :---: | :---: | :---: | :--- |")
    
    sorted_sources = sorted(BLOCKLIST_SOURCES.keys(), key=lambda n: SOURCE_WEIGHTS.get(n, 0), reverse=True)
    
    for name in sorted_sources:
        weight = SOURCE_WEIGHTS.get(name, 1)
        category = SOURCE_CATEGORIES.get(name, "Other")
        fetched_count = source_metrics.get(name, {}).get("Total_Fetched", 0)
        in_priority = source_metrics.get(name, {}).get("In_Priority_List", 0)
        volatility_raw = source_metrics.get(name, {}).get("Volatility", "N/A")
        
        color_style = ""
        volatility_display = str(volatility_raw)
        
        if volatility_raw not in ("N/A", "New"):
            try:
                change_pct = float(volatility_raw)
                volatility_display = f"{change_pct:+.1f}%"
                if abs(change_pct) <= 5.0: color_style = "color:green;"
                elif change_pct >= 25.0: color_style = "color:orange;" 
                elif change_pct <= -25.0: color_style = "color:red;"
            except ValueError: pass
        
        source_color = SOURCE_COLORS.get(name, "black")
        
        report.append(
            f"| **{name}** | {category} | {weight} | {fetched_count:,} | {in_priority:,} | "
            f"<span style='{color_style}'>`{volatility_display}`</span> | <span style='color:{source_color};'>███</span> |"
        )

    report.append("\n---")
    
    # --- Interactive Dashboard ---
    report.append("\n## 📈 Interactive Visualization")
    report.append(f"The **Score-filterable Domain List** is available at: [`dashboard.html`](dashboard.html)")
    
    # Write the report
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report))


# --- File Writing & Cleanup ---

def cleanup_old_files(output_path: Path, logger: ConsoleLogger):
    """Deletes old files from cache and archive folders based on CACHE_CLEANUP_DAYS."""
    cutoff_date = datetime.now() - timedelta(days=CACHE_CLEANUP_DAYS)
    deleted_count = 0
    
    # Directories to clean
    dirs_to_clean = [output_path, ARCHIVE_DIR]
    
    for directory in dirs_to_clean:
        if not directory.exists(): continue
        
        for item in directory.iterdir():
            if item.is_file():
                # Get last modification time
                if item.name.endswith(".json") or item.name.startswith("priority_"):
                    mod_time = datetime.fromtimestamp(item.stat().st_mtime)
                    if mod_time < cutoff_date:
                        try:
                            item.unlink()
                            deleted_count += 1
                        except OSError as e:
                            logger.error(f"Failed to delete old file {item.name}: {e}")

    if deleted_count > 0:
        logger.info(f"🧹 Cleaned up {deleted_count} old cache/archive files (> {CACHE_CLEANUP_DAYS} days old).")

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

def write_output_files(
    priority_set: Set[str], abused_tlds: Set[str], full_list: List[str], output_path: Path, 
    logger: ConsoleLogger, priority_cap_val: int, excluded_domains_verbose: List[Dict[str, Any]], 
    write_verbose: bool, output_format: str
):
    """Writes all final output files in the specified format."""
    logger.info("💾 Writing final output files...")
    output_path.mkdir(exist_ok=True, parents=True)
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 1. Priority List
    priority_file = output_path / PRIORITY_FILENAME
    
    if output_format == 'hosts':
        prefix = "0.0.0.0 "
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
        
    # 5. Full Aggregated List 
    unfiltered_file = output_path / UNFILTERED_FILENAME
    with open(unfiltered_file, "w", encoding="utf-8") as f:
        f.write(f"# Full Aggregated List (Filtered by TLDs, Sorted by Score)\n# Generated: {now_str}\n# Total: {len(full_list):,}\n")
        f.writelines(d + "\n" for d in full_list)
        
    logger.info(f"✅ Outputs written to: {output_path.resolve()}")

# --- Main Execution ---

def main():
    """Main function to run the aggregation process."""
    parser = argparse.ArgumentParser(description="Singularity DNS Blocklist Aggregator (v5.3)")
    parser.add_argument("-o", "--output", type=Path, default=OUTPUT_DIR, help=f"Output directory (default: {OUTPUT_DIR})")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable DEBUG logging")
    parser.add_argument("-p", "--priority-cap", type=int, default=PRIORITY_CAP_DEFAULT, help=f"Maximum size for the priority list (default: {PRIORITY_CAP_DEFAULT:,})")
    parser.add_argument("-w", "--max-workers", type=int, default=MAX_WORKERS_DEFAULT, help=f"Maximum concurrent network workers (aiohttp limit, default: {MAX_WORKERS_DEFAULT})")
    parser.add_argument("-v", "--verbose-report", action="store_true", help="Write a detailed CSV report of all excluded domains.")
    parser.add_argument("-f", "--output-format", choices=['raw', 'hosts'], default='raw', help="Output format for the priority list ('raw' for Unbound/AdGuard DNS filter, 'hosts' for Pi-hole/etc.)")
    parser.add_argument("--cleanup-cache", action="store_true", help=f"Delete old cache and archive files (> {CACHE_CLEANUP_DAYS} days).") # ADDED ARG
    parser.add_argument("--test", action="store_true", help="Run internal integrity tests and exit.") # ADDED ARG
    args = parser.parse_args()
    
    # --- Internal Test Suite ---
    if args.test:
        return run_tests(args.output, ConsoleLogger(args.debug))
    # --- End Test Suite ---

    logger = ConsoleLogger(args.debug)
    output_path = args.output
    output_path.mkdir(exist_ok=True)
    
    priority_cap_val = args.priority_cap
    max_workers_val = args.max_workers
    output_format_val = args.output_format
    
    start = datetime.now()
    logger.info("--- 🚀 Starting Singularity DNS Aggregation (v5.3 - FINALIZED) ---")
    
    if args.cleanup_cache:
        cleanup_old_files(output_path, logger)
    
    # === SCOPE INITIALIZATION ===
    priority_set: Set[str] = set()
    tld_exclusion_counter: Counter = Counter()
    excluded_domains_verbose: List[Dict[str, Any]] = []
    # ============================

    try:
        history_path = output_path / HISTORY_FILENAME
        report_path = output_path / REPORT_FILENAME
        image_path = output_path / "score_distribution_chart.png"
        dashboard_html_path = output_path / DASHBOARD_HTML
        
        # 1. Fetch & Process (Run the async function)
        source_sets, all_domains_from_sources = asyncio.run(fetch_and_process_sources_async(max_workers_val, logger))
        
        # 2. Aggregate & Score
        combined_counter, overlap_counter, domain_sources = aggregate_and_score_domains(source_sets)
        total_unfiltered = len(combined_counter)
        
        # 3. Filter & Prioritize
        priority_set, abused_tlds, excluded_count, full_filtered, tld_exclusion_counter, excluded_domains_verbose = filter_and_prioritize(
            combined_counter, logger, priority_cap_val
        )

        # 4. History Tracking & Metrics 
        priority_count = len(priority_set)
        change, history = track_history(total_unfiltered, history_path, logger)
        source_metrics = calculate_source_metrics(
            priority_set, full_filtered, overlap_counter, domain_sources, all_domains_from_sources, logger
        )
        
        # 5. Priority List Change Tracking 
        change_report = track_priority_changes(
            priority_set, combined_counter, domain_sources, full_filtered, logger
        )

        # 6. Reporting & Visualization
        generate_static_score_histogram(combined_counter, full_filtered, image_path, logger)
        generate_interactive_dashboard(
            full_filtered, combined_counter, domain_sources, dashboard_html_path, logger
        )
        generate_markdown_report(
            priority_count, change, total_unfiltered, excluded_count, full_filtered, combined_counter,
            overlap_counter, report_path, dashboard_html_path, source_metrics, history, logger,
            domain_sources, change_report, tld_exclusion_counter, priority_cap_val, excluded_domains_verbose
        )
        
        # 7. File Writing
        write_output_files(
            priority_set, abused_tlds, full_filtered, output_path, logger, priority_cap_val,
            excluded_domains_verbose, args.verbose_report, output_format_val
        )
        
    except Exception as e:
        logger.error(f"FATAL ERROR during execution: {e.__class__.__name__}: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)
        
    logger.info(f"--- ✅ Aggregation Complete in {(datetime.now() - start).total_seconds():.2f}s ---")

# --- Test Functions (Placeholder for future development) ---
def run_tests(output_path, logger):
    logger.info("--- 🧪 Running Internal Integrity Tests ---")
    
    # Test 1: Punycode normalization
    test_domains = {
        "xn--fzc.com": "xn--fzc.com", # Already punycode
        "bücher.de": "xn--bcher-kva.de", # Unicode
        "google.com^$script": "google.com", # ABP cleanup
        "1.2.3.4": None, # IPv4 rejection
        "0.0.0.0 bad.com": "bad.com" # Hosts file format
    }
    
    passed = 0
    total = len(test_domains)
    for input_line, expected in test_domains.items():
        result = process_domain(input_line)
        if result == expected:
            passed += 1
            logger.debug(f"PASS: '{input_line}' -> '{result}'")
        else:
            logger.error(f"FAIL: '{input_line}' -> Expected '{expected}', Got '{result}'")
            
    if passed == total:
        logger.info(f"✅ All {total} process_domain tests passed.")
        return 0
    else:
        logger.error(f"❌ {passed}/{total} tests passed. Check logs for failures.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
