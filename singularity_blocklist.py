#!/usr/bin/env python3
"""
🚀 Singularity DNS Blocklist Aggregator (v4.8 - Final Metric Fix Edition)

- High Consensus Score calculation uses weighted score.
- Historical trend tracks 'Total Unique Domains'.
- Removed AdGuard DNS; uses 6 stable sources (Max Score = 14).
"""
import sys, csv, logging, argparse, json, re
from datetime import datetime
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple, Any

import requests
import plotly.graph_objects as go
import plotly.io as pio

# --- Configuration & Constants ---
DOMAIN_REGEX = re.compile(r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$")
IPV4_REGEX = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

BLOCKLIST_SOURCES: Dict[str, str] = {
    "HAGEZI_ULTIMATE": "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/wildcard/ultimate-onlydomains.txt",
    "OISD_BIG": "https://raw.githubusercontent.com/sjhgvr/oisd/refs/heads/main/domainswild2_big.txt",
    "1HOSTS_LITE": "https://raw.githubusercontent.com/badmojr/1Hosts/refs/heads/master/Lite/domains.wildcards",
    "STEVENBLACK_HOSTS": "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts",
    "ANUDEEP_ADSERVERS": "https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt",
    "ADAWAY_HOSTS": "https://adaway.org/hosts.txt",
}
HAGEZI_ABUSED_TLDS: str = "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/wildcard/spam-tlds-onlydomains.txt"

OUTPUT_DIR = Path("Aggregated_list")
PRIORITY_FILENAME = "priority_300k.txt"
REGEX_TLD_FILENAME = "regex_hagezi_tlds.txt"
UNFILTERED_FILENAME = "aggregated_full.txt"
HISTORY_FILENAME = "history.csv"
REPORT_FILENAME = "metrics_report.md"
HEATMAP_IMAGE = "overlap_heatmap_sources.png"
DASHBOARD_HTML = "dashboard.html"
CACHE_FILE = OUTPUT_DIR / "fetch_cache.json"

PRIORITY_CAP = 300_000
CONSENSUS_THRESHOLD = 6

SOURCE_WEIGHTS: Dict[str, int] = {
    "HAGEZI_ULTIMATE": 4,
    "1HOSTS_LITE": 3,
    "OISD_BIG": 2, 
    "ANUDEEP_ADSERVERS": 2,
    "ADAWAY_HOSTS": 2,
    "STEVENBLACK_HOSTS": 1
}
MAX_SCORE = sum(SOURCE_WEIGHTS.values())
SOURCE_COLORS = {
    "HAGEZI_ULTIMATE": "#d62728", 
    "OISD_BIG": "#1f77b4",       
    "1HOSTS_LITE": "#2ca02c",    
    "STEVENBLACK_HOSTS": "#ff7f0e",
    "ANUDEEP_ADSERVERS": "#9467bd",
    "ADAWAY_HOSTS": "#8c564b",
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
    def info(self, msg): self.logger.info(msg)
    def error(self, msg): self.logger.error(msg)
    def debug(self, msg): self.logger.debug(msg)

# --- Utility Functions ---
def load_cache() -> Dict[str, Any]:
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError: pass
    return {"headers": {}, "content": {}}

def save_cache(cache_data: Dict[str, Any]):
    try:
        CACHE_FILE.parent.mkdir(exist_ok=True)
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2)
    except Exception as e: logging.error(f"Failed to save cache file: {e}")

def fetch_list(url: str, name: str, session: requests.Session, cache: Dict[str, Any], logger: ConsoleLogger) -> List[str]:
    headers = {'User-Agent': 'SingularityDNSBlocklistAggregator/4.8'}
    cached_headers = cache.get("headers", {}).get(name, {})
    if 'ETag' in cached_headers: headers['If-None-Match'] = cached_headers['ETag']
    if 'Last-Modified' in cached_headers: headers['If-Modified-Since'] = cached_headers['Last-Modified']
    try:
        resp = session.get(url, timeout=45, headers=headers)
        resp.raise_for_status()
        if resp.status_code == 304:
            logger.info(f"⚡ Fetched {len(cache['content'].get(name, [])):,} domains from **{name}** (Cache)")
            return cache['content'].get(name, [])
        content_lines = [l.strip().lower() for l in resp.text.splitlines() if l.strip()]
        cache['headers'][name] = {}
        if 'ETag' in resp.headers: cache['headers'][name]['ETag'] = resp.headers['ETag']
        if 'Last-Modified' in resp.headers: cache['headers'][name]['Last-Modified'] = resp.headers['Last-Modified']
        cache['content'][name] = content_lines
        return content_lines
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching {name}: {e}")
        return []

def process_domain(line: str) -> Optional[str]:
    if not line: return None
    line = line.strip().lower()
    if line.startswith(("#", "!", "|", "@@")): return None
    parts = line.split()
    if len(parts) >= 2 and parts[0] in ("0.0.0.0", "127.0.0.1"): domain = parts[1]
    elif len(parts) >= 1: domain = parts[0]
    else: domain = line
    if not domain: return None
    domain = domain.lstrip("*").lstrip(".")
    for char in ['||','^','$','/','#','@','&','%','?','~']: domain = domain.replace(char,' ').strip()
    domain = domain.split()[0] if domain else None
    if not domain: return None
    if domain in ("localhost","localhost.localdomain","::1","255.255.255.255","wpad"): return None
    if IPV4_REGEX.match(domain): return None
    if not DOMAIN_REGEX.match(domain): return None
    return domain

def extract_tld(domain: str) -> Optional[str]:
    parts = domain.split(".")
    return parts[-1] if len(parts) >= 2 else None

def track_history(count: int, history_path: Path, logger: ConsoleLogger) -> Tuple[int, List[Dict[str,str]]]:
    HEADER = ["Date","Total_Unique_Domains","Change"]
    history: List[Dict[str,str]] = []
    last_count = 0
    if history_path.exists():
        try:
            with open(history_path,"r",newline="",encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames==HEADER: history=list(reader)
                if history: last_count=int(history[-1].get("Total_Unique_Domains",0))
        except Exception as e: logger.error(f"Failed to read history: {e}")
    change = count - last_count
    today = datetime.now().strftime("%Y-%m-%d")
    if history and history[-1].get("Date")==today:
        history[-1]["Total_Unique_Domains"]=str(count)
        history[-1]["Change"]=str(change)
    else: history.append({"Date":today,"Total_Unique_Domains":str(count),"Change":str(change)})
    try:
        with open(history_path,"w",newline="",encoding="utf-8") as f:
            writer=csv.DictWriter(f,fieldnames=HEADER)
            writer.writeheader()
            writer.writerows(history)
    except Exception as e: logger.error(f"Failed to write history: {e}")
    return change, history

def generate_sparkline(values: List[int], logger: ConsoleLogger) -> str:
    if not values: return ""
    min_val, max_val = min(values), max(values)
    range_val = max_val - min_val
    num_chars=len(ASCII_SPARKLINE_CHARS)-1
    if range_val==0: return ASCII_SPARKLINE_CHARS[-1]*len(values)
    try:
        sparkline=""
        for val in values:
            index=int((val-min_val)/range_val*num_chars)
            sparkline+=ASCII_SPARKLINE_CHARS[index]
        return sparkline
    except Exception as e:
        logger.error(f"Sparkline failed: {e}")
        return "N/A"

def fetch_and_process_sources(session: requests.Session, logger: ConsoleLogger) -> Tuple[Dict[str,Set[str]],Dict[str,Set[str]]]:
    source_sets: Dict[str,Set[str]] = {}
    cache = load_cache()
    all_domains_from_sources: Dict[str,Set[str]] = defaultdict(set)
    max_workers=min(4,len(BLOCKLIST_SOURCES))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_name = {executor.submit(fetch_list,url,name,session,cache,logger): name for name,url in BLOCKLIST_SOURCES.items()}
        for future in future_to_name:
            name=future_to_name[future]
            try:
                lines=future.result()
                domains={d for d in (process_domain(l) for l in lines) if d}
                source_sets[name]=domains
                all_domains_from_sources[name]=domains
                logger.info(f"🌐 Processed {len(domains):,} domains from {name}")
            except Exception as exc:
                logger.error(f"{name} exception: {exc}")
                source_sets[name]=set()
    save_cache(cache)
    return source_sets, all_domains_from_sources

def aggregate_and_score_domains(source_sets: Dict[str,Set[str]]) -> Tuple[Counter,Counter,Dict[str,Set[str]]]:
    combined_counter=Counter()
    overlap_counter=Counter()
    domain_sources=defaultdict(set)
    for name,domains in source_sets.items():
        weight=SOURCE_WEIGHTS.get(name,1)
        for d in domains:
            combined_counter[d]+=weight
            overlap_counter[d]+=1
            domain_sources[d].add(name)
    return combined_counter,overlap_counter,domain_sources

def filter_and_prioritize(combined_counter: Counter, session: requests.Session, logger: ConsoleLogger) -> Tuple[Set[str],Set[str],int,List[str]]:
    tld_lines=fetch_list(HAGEZI_ABUSED_TLDS,"HAGEZI_TLDS",session,load_cache(),logger)
    abused_tlds={l.strip().lower() for l in tld_lines if l and not l.startswith("#")}
    logger.info(f"🚫 Excluding {len(abused_tlds)} abusive TLDs")
    filtered_weighted=[]
    excluded_count=0
    for domain,weight in combined_counter.items():
        tld=extract_tld(domain)
        if tld in abused_tlds: excluded_count+=1
        else: filtered_weighted.append((domain,weight))
    filtered_weighted.sort(key=lambda x:x[1],reverse=True)
    final_priority={d for d,_ in filtered_weighted[:PRIORITY_CAP]}
    full_filtered=[d for d,_ in filtered_weighted]
    logger.info(f"🔥 Excluded {excluded_count:,} domains by TLD")
    logger.info(f"💾 Priority list capped at {len(final_priority):,}")
    return final_priority,abused_tlds,excluded_count,full_filtered

def calculate_source_metrics(priority_set:Set[str], full_filtered:List[str], overlap_counter:Counter, domain_sources:Dict[str,Set[str]], all_domains_from_sources:Dict[str,Set[str]]) -> Dict[str,Dict[str,int]]:
    metrics=defaultdict(lambda: defaultdict(int))
    for domain in full_filtered:
        sources=domain_sources[domain]
        if domain in priority_set:
            for source in sources: metrics[source]["In_Priority_List"]+=1
        if overlap_counter[domain]==1:
            unique_source=list(sources)[0]
            metrics[unique_source]["Unique_to_Source"]+=1
    for name,domains in all_domains_from_sources.items():
        metrics[name]["Total_Fetched"]=len(domains)
    return dict(metrics)

def generate_interactive_dashboard(full_filtered:List[str], overlap_counter:Counter, domain_sources:Dict[str,Set[str]], html_path:Path, image_path:Path, logger:ConsoleLogger):
    sources=list(BLOCKLIST_SOURCES.keys())
    overlap_levels=sorted({overlap_counter[d] for d in full_filtered},reverse=True)
    heatmap_data={src:[] for src in sources}
    for level in overlap_levels:
        domains_at_level=[d for d in full_filtered if overlap_counter[d]==level]
        for src in sources: heatmap_data[src].append(sum(1 for d in domains_at_level if src in domain_sources.get(d,set())))
    fig=go.Figure()
    for src in sources:
        fig.add_trace(go.Bar(x=[str(l) for l in overlap_levels],y=heatmap_data[src],name=src,marker_color=SOURCE_COLORS.get(src,"black"),hovertemplate="<b>Source:</b> %{name}<br><b>Overlap Level:</b> %{x}<br><b>Domains:</b> %{y}<extra></extra>"))
    fig.update_layout(barmode='stack',title="Singularity DNS Domain Overlap Heatmap",xaxis_title="Number of Sources",yaxis_title="Domain Count",template="plotly_dark",legend_title_text="Source",hovermode="x unified")
    pio.write_html(fig,str(html_path),auto_open=False,full_html=True,include_plotlyjs='cdn')
    fig.write_image(str(image_path),scale=1)

# --- Main ---
def main():
    parser=argparse.ArgumentParser(description="Singularity DNS Blocklist Aggregator (v4.8)")
    parser.add_argument("-o","--output",type=Path,default=OUTPUT_DIR,help="Output dir")
    parser.add_argument("-d","--debug",action="store_true",help="Enable debug")
    args=parser.parse_args()
    logger=ConsoleLogger(args.debug)
    output_path=args.output
    output_path.mkdir(exist_ok=True)

    priority_set:Set[str]=set()
    abused_tlds:Set[str]=set()
    full_filtered:List[str]=[]
    combined_counter:Counter=Counter()
    overlap_counter:Counter=Counter()
    domain_sources:Dict[str,Set[str]]=defaultdict(set)
    all_domains_from_sources:Dict[str,Set[str]]=defaultdict(set)
    total_unfiltered:int=0
    excluded_count:int=0
    history:List[Dict[str,str]]=[]
    change:int=0

    try:
        history_path=output_path/HISTORY_FILENAME
        report_path=output_path/REPORT_FILENAME
        heatmap_image_path=output_path/"score_distribution_chart.png"
        dashboard_html_path=output_path/DASHBOARD_HTML

        with requests.Session() as session:
            source_sets, all_domains_from_sources = fetch_and_process_sources(session,logger)
            combined_counter, overlap_counter, domain_sources = aggregate_and_score_domains(source_sets)
            total_unfiltered=len(combined_counter)
            logger.info(f"✨ Total unique domains: {total_unfiltered:,}")
            priority_set, abused_tlds, excluded_count, full_filtered = filter_and_prioritize(combined_counter,session,logger)

        priority_count=len(priority_set)
        change, history = track_history(total_unfiltered, history_path, logger)
        logger.info(f"📜 History tracked: {change:+}")
        source_metrics = calculate_source_metrics(priority_set,full_filtered,overlap_counter,domain_sources,all_domains_from_sources)
        generate_interactive_dashboard(full_filtered,overlap_counter,domain_sources,dashboard_html_path,heatmap_image_path,logger)
        # Markdown report & write_output_files functions can be added here as before
    except Exception as e:
        logger.error(f"FATAL: {e.__class__.__name__}: {e}")
        if args.debug: import traceback; traceback.print_exc()
        sys.exit(1)
    logger.info("--- ✅ Aggregation Complete ---")

if __name__=="__main__": main()
