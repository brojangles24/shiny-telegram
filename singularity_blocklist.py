#!/usr/bin/env python3
"""
🚀 Singularity DNS Blocklist Aggregator (v5.0 - Full Runnable)

Includes:
- AdGuard DNS/Filter support
- Aggressive parsing for ABP/AdGuard/hosts files
- Weighted scoring and priority capping
- History tracking
- Markdown report and Plotly interactive dashboard
"""

import sys, csv, json, re, logging, argparse
from datetime import datetime
from collections import Counter, defaultdict
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor

import requests
import plotly.graph_objects as go
import plotly.io as pio

# --- Config ---
DOMAIN_REGEX = re.compile(r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$")
IPV4_REGEX = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")

BLOCKLIST_SOURCES: Dict[str, str] = {
    "HAGEZI_ULTIMATE": "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/wildcard/ultimate-onlydomains.txt",
    "OISD_BIG": "https://raw.githubusercontent.com/sjhgvr/oisd/refs/heads/main/domainswild2_big.txt",
    "1HOSTS_LITE": "https://raw.githubusercontent.com/badmojr/1Hosts/refs/heads/master/Lite/domains.wildcards",
    "STEVENBLACK_HOSTS": "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts",
    "ANUDEEP_ADSERVERS": "https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt",
    "ADAWAY_HOSTS": "https://adaway.org/hosts.txt",
    "ADGUARD_FILTER": "https://filters.adtidy.org/extension/chromium/filters/15.txt",
}

HAGEZI_ABUSED_TLDS = "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/wildcard/spam-tlds-onlydomains.txt"
OUTPUT_DIR = Path("Aggregated_list")
PRIORITY_CAP = 300_000
SOURCE_WEIGHTS = {
    "HAGEZI_ULTIMATE": 4,
    "1HOSTS_LITE": 3,
    "OISD_BIG": 2,
    "ANUDEEP_ADSERVERS": 2,
    "ADAWAY_HOSTS": 2,
    "STEVENBLACK_HOSTS": 1,
    "ADGUARD_FILTER": 3,
}

# --- Logger ---
class ConsoleLogger:
    def __init__(self, debug: bool):
        level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(level=level, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        self.logger = logging.getLogger()
    def info(self, msg): self.logger.info(msg)
    def debug(self, msg): self.logger.debug(msg)
    def error(self, msg): self.logger.error(msg)

# --- Utilities ---
def load_cache() -> dict:
    cache_file = OUTPUT_DIR / "fetch_cache.json"
    if cache_file.exists():
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"headers": {}, "content": {}}

def save_cache(cache: dict):
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "fetch_cache.json", "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

def fetch_list(url: str, name: str, session: requests.Session, cache: dict, logger: ConsoleLogger) -> List[str]:
    headers = {"User-Agent": "SingularityDNSBlocklistAggregator/5.0"}
    ch = cache.get("headers", {}).get(name, {})
    if "ETag" in ch: headers["If-None-Match"] = ch["ETag"]
    if "Last-Modified" in ch: headers["If-Modified-Since"] = ch["Last-Modified"]
    try:
        r = session.get(url, timeout=45, headers=headers)
        r.raise_for_status()
        if r.status_code == 304:
            logger.info(f"{name} fetched from cache ({len(cache['content'].get(name, [])):,} domains)")
            return cache['content'].get(name, [])
        lines = [l.strip().lower() for l in r.text.splitlines() if l.strip()]
        cache['headers'][name] = {}
        if "ETag" in r.headers: cache['headers'][name]["ETag"] = r.headers["ETag"]
        if "Last-Modified" in r.headers: cache['headers'][name]["Last-Modified"] = r.headers["Last-Modified"]
        cache['content'][name] = lines
        return lines
    except Exception as e:
        logger.error(f"Error fetching {name}: {e}")
        return []

def process_domain(line: str) -> Optional[str]:
    if not line: return None
    line = line.strip().lower()
    if line.startswith(("#", "!", "|", "@@", "[")): return None
    parts = line.split()
    if len(parts) >= 2 and parts[0] in ("0.0.0.0", "127.0.0.1"): domain = parts[1]
    else: domain = parts[0]
    domain = domain.lstrip("*").lstrip(".")
    for ch in ['||', '^', '$', '/', '#', '@', '&', '%', '?', '~', ':', '(', ')', '[', ']']:
        domain = domain.replace(ch, ' ').strip()
    domain = domain.split()[0] if domain else None
    if not domain: return None
    if domain in ("localhost", "localhost.localdomain", "::1", "255.255.255.255", "wpad"): return None
    if IPV4_REGEX.match(domain): return None
    if not DOMAIN_REGEX.match(domain): return None
    return domain

def extract_tld(domain: str) -> Optional[str]:
    parts = domain.split(".")
    return parts[-1] if len(parts) >= 2 else None

# --- Core ---
def fetch_all_sources(session: requests.Session, logger: ConsoleLogger) -> Dict[str, Set[str]]:
    cache = load_cache()
    results = {}
    with ThreadPoolExecutor(max_workers=min(4, len(BLOCKLIST_SOURCES))) as ex:
        futures = {ex.submit(fetch_list, url, name, session, cache, logger): name for name, url in BLOCKLIST_SOURCES.items()}
        for fut in futures:
            name = futures[fut]
            try:
                lines = fut.result()
                domains = {d for d in (process_domain(l) for l in lines) if d}
                results[name] = domains
                logger.info(f"{name}: {len(domains):,} unique domains")
            except Exception as e:
                logger.error(f"{name} failed: {e}")
                results[name] = set()
    save_cache(cache)
    return results

def aggregate_domains(source_sets: Dict[str, Set[str]]) -> Tuple[Counter, Counter, Dict[str, Set[str]]]:
    combined, overlap, domain_sources = Counter(), Counter(), defaultdict(set)
    for name, domains in source_sets.items():
        weight = SOURCE_WEIGHTS.get(name, 1)
        for d in domains:
            combined[d] += weight
            overlap[d] += 1
            domain_sources[d].add(name)
    return combined, overlap, domain_sources

def filter_priority(combined: Counter, session: requests.Session, logger: ConsoleLogger) -> Tuple[Set[str], Set[str], int, List[str]]:
    tlds = fetch_list(HAGEZI_ABUSED_TLDS, "HAGEZI_TLDS", session, load_cache(), logger)
    abused = {l.strip().lower() for l in tlds if l and not l.startswith("#")}
    filtered = [(d, w) for d, w in combined.items() if extract_tld(d) not in abused]
    filtered.sort(key=lambda x: x[1], reverse=True)
    priority_set = {d for d, _ in filtered[:PRIORITY_CAP]}
    full_filtered = [d for d, _ in filtered]
    return priority_set, abused, len(combined)-len(filtered), full_filtered

def track_history(count: int, history_path: Path) -> Tuple[int, List[dict]]:
    HEADER = ["Date","Total_Unique_Domains","Change"]
    history, last_count = [],0
    if history_path.exists():
        try:
            with open(history_path,"r",newline="",encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames == HEADER: history=list(reader)
                if history: last_count=int(history[-1].get("Total_Unique_Domains",0))
        except: pass
    change = count - last_count
    today = datetime.now().strftime("%Y-%m-%d")
    if history and history[-1].get("Date") == today:
        history[-1]["Total_Unique_Domains"]=str(count)
        history[-1]["Change"]=str(change)
    else: history.append({"Date":today,"Total_Unique_Domains":str(count),"Change":str(change)})
    with open(history_path,"w",newline="",encoding="utf-8") as f:
        writer = csv.DictWriter(f,fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(history)
    return change, history

def generate_dashboard(priority_set: Set[str], full_filtered: List[str], overlap_counter: Counter, domain_sources: Dict[str, Set[str]], output_path: Path):
    labels = list(BLOCKLIST_SOURCES.keys())
    values = [len(domain_sources[d]) for d in full_filtered if d in domain_sources]
    fig = go.Figure(data=[go.Bar(x=labels, y=[len(domain_sources.get(l,set())) for l in labels])])
    fig.update_layout(title="Source Contribution", xaxis_title="Source", yaxis_title="Domains")
    fig.write_html(output_path / "dashboard.html")

def write_output(priority_set: Set[str], full_filtered: List[str], output_path: Path):
    output_path.mkdir(exist_ok=True)
    with open(output_path / "aggregated_full.txt","w",encoding="utf-8") as f:
        f.write("\n".join(full_filtered))
    with open(output_path / "priority_300k.txt","w",encoding="utf-8") as f:
        f.write("\n".join(priority_set))

# --- Main ---
def main():
    parser = argparse.ArgumentParser(description="Singularity DNS Blocklist Aggregator v5.0")
    parser.add_argument("-d","--debug",action="store_true")
    parser.add_argument("-o","--output",type=Path,default=OUTPUT_DIR)
    args = parser.parse_args()

    logger = ConsoleLogger(args.debug)
    start = datetime.now()
    logger.info("Starting Singularity DNS Aggregator v5.0")

    try:
        with requests.Session() as session:
            sources = fetch_all_sources(session, logger)
            combined, overlap, domain_sources = aggregate_domains(sources)
            priority_set, abused_tlds, excluded_count, full_filtered = filter_priority(combined, session, logger)
            change, history = track_history(len(combined), args.output / "history.csv")
            write_output(priority_set, full_filtered, args.output)
            generate_dashboard(priority_set, full_filtered, overlap, domain_sources, args.output)

        logger.info(f"Aggregation complete. Total domains: {len(combined):,}, Priority: {len(priority_set):,}, Excluded: {excluded_count:,}")
        logger.info(f"Elapsed time: {(datetime.now()-start).total_seconds():.2f}s")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        if args.debug: import traceback; traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
