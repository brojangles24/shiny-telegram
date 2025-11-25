#!/usr/bin/env python3

"""
Singularity DNS Blocklist Aggregator

Fetches multiple DNS blocklists, deduplicates, applies weighting,
filters abused TLDs, and generates:
1. Priority blocklist (capped)
2. Regex TLD list
3. Full unfiltered list
4. Historical CSV log
5. Singularity DNS branded heatmap
6. Neon-themed Markdown report
"""

import sys
import csv
import logging
from datetime import datetime
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple

import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# --- Configuration ---
BLOCKLIST_SOURCES: Dict[str, str] = {
    "OISD_BIG": "https://raw.githubusercontent.com/sjhgvr/oisd/refs/heads/main/domainswild2_big.txt",
    "HAGEZI_ULTIMATE": "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/wildcard/ultimate-onlydomains.txt",
    "1HOSTS_LITE": "https://raw.githubusercontent.com/badmojr/1Hosts/refs/heads/master/Lite/domains.wildcards",
    "STEVENBLACK_HOSTS": "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"
}

HAGEZI_ABUSED_TLDS: str = "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/wildcard/spam-tlds-onlydomains.txt"

OUTPUT_DIR: Path = Path("Aggregated_list")
PRIORITY_FILENAME: Path = OUTPUT_DIR / "priority_300k.txt"
REGEX_TLD_FILENAME: Path = OUTPUT_DIR / "regex_hagezi_tlds.txt"
UNFILTERED_FILENAME: Path = OUTPUT_DIR / "aggregated_full.txt"
HISTORY_FILENAME: Path = OUTPUT_DIR / "history.csv"
REPORT_FILENAME: Path = OUTPUT_DIR / "metrics_report.md"
HEATMAP_IMAGE: Path = OUTPUT_DIR / "overlap_heatmap_sources.png"

PRIORITY_CAP: int = 300000

SOURCE_WEIGHTS: Dict[str, int] = {
    "HAGEZI_ULTIMATE": 3,
    "OISD_BIG": 2,
    "1HOSTS_LITE": 1,
    "STEVENBLACK_HOSTS": 1
}

SOURCE_COLORS: Dict[str, str] = {
    "HAGEZI_ULTIMATE": "#ff00ff",
    "OISD_BIG": "#00ffff",
    "1HOSTS_LITE": "#00ff00",
    "STEVENBLACK_HOSTS": "#ff7f0e"
}

# --- Type Aliases ---
DomainSet = Set[str]
SourceData = Dict[str, DomainSet]
DomainCounter = Counter[str]
DomainSources = Dict[str, Set[str]]

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])

# --- Core Utility Functions ---
def fetch_list(url: str, session: requests.Session) -> List[str]:
    try:
        resp = session.get(url, timeout=45)
        resp.raise_for_status()
        return [line.strip().lower() for line in resp.text.splitlines() if line.strip()]
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return []

def process_domain(line: str) -> Optional[str]:
    if not line or line.startswith(('#', '!')):
        return None
    parts = line.split()
    domain: str = ""
    if len(parts) == 1:
        domain = parts[0]
    elif len(parts) > 1 and parts[0] in ("0.0.0.0", "127.0.0.1"):
        domain = parts[1]
    else:
        return None
    if domain in ("localhost", "localhost.localdomain", "::1", "255.255.255.255"):
        return None
    return domain.strip()

def extract_tld(domain: str) -> Optional[str]:
    domain = domain.lstrip("*").lstrip(".")
    if "." not in domain:
        return None
    return domain.split(".")[-1]

def track_history(count: int) -> int:
    HEADER = ["Date", "Priority_Count", "Change"]
    history: List[Dict[str, str]] = []
    last_count = 0
    if HISTORY_FILENAME.exists():
        try:
            with open(HISTORY_FILENAME, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames == HEADER:
                    history = list(reader)
                    if history:
                        last_count = int(history[-1]["Priority_Count"])
        except Exception as e:
            logging.error(f"Could not read history file: {e}")
    change = count - last_count
    today = datetime.now().strftime("%Y-%m-%d")
    if history and history[-1]["Date"] == today:
        history[-1]["Priority_Count"] = str(count)
        history[-1]["Change"] = str(change)
    else:
        history.append({"Date": today, "Priority_Count": str(count), "Change": str(change)})
    try:
        with open(HISTORY_FILENAME, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=HEADER)
            writer.writeheader()
            writer.writerows(history)
    except Exception as e:
        logging.error(f"Could not write to history file: {e}")
    return change

# --- Main Processing ---
def fetch_and_process_sources(session: requests.Session) -> SourceData:
    source_sets: SourceData = {}
    with ThreadPoolExecutor(max_workers=len(BLOCKLIST_SOURCES)) as executor:
        future_to_name = {executor.submit(fetch_list, url, session): name for name, url in BLOCKLIST_SOURCES.items()}
        for future in future_to_name:
            name = future_to_name[future]
            lines = future.result()
            domains = set(filter(None, [process_domain(line) for line in lines]))
            source_sets[name] = domains
            logging.info(f"Fetched {len(domains):,} domains from {name}")
    return source_sets

def aggregate_and_score_domains(source_sets: SourceData) -> Tuple[DomainCounter, DomainCounter, DomainSources]:
    combined_counter: DomainCounter = Counter()
    overlap_counter: DomainCounter = Counter()
    domain_sources: DomainSources = defaultdict(set)
    for name, domains in source_sets.items():
        weight = SOURCE_WEIGHTS.get(name, 1)
        for d in domains:
            combined_counter[d] += weight
            overlap_counter[d] += 1
            domain_sources[d].add(name)
    return combined_counter, overlap_counter, domain_sources

def filter_and_prioritize(combined_counter: DomainCounter, session: requests.Session) -> Tuple[DomainSet, DomainSet, int, List[str]]:
    tld_lines = fetch_list(HAGEZI_ABUSED_TLDS, session)
    abused_tlds = set(filter(None, [line.strip() for line in tld_lines if not line.startswith("#")]))
    logging.info(f"Excluding {len(abused_tlds)} Hagezi abused TLDs")
    filtered_domains_weighted: List[Tuple[str, int]] = []
    excluded_count = 0
    for domain, weight in combined_counter.items():
        if extract_tld(domain) not in abused_tlds:
            filtered_domains_weighted.append((domain, weight))
        else:
            excluded_count += 1
    filtered_domains_weighted.sort(key=lambda x: x[1], reverse=True)
    final_priority_set = {domain for domain, _ in filtered_domains_weighted[:PRIORITY_CAP]}
    full_filtered_list = [domain for domain, _ in filtered_domains_weighted]
    logging.info(f"Excluded {excluded_count:,} domains based on TLD filter.")
    logging.info(f"Created priority list with {len(final_priority_set):,} domains (cap: {PRIORITY_CAP:,}).")
    return final_priority_set, abused_tlds, excluded_count, full_filtered_list

# --- Visuals ---
def generate_overlap_heatmap(filtered_domains: List[str], overlap_counter: DomainCounter, domain_sources: DomainSources) -> None:
    logging.info(f"Generating enhanced Singularity DNS overlap heatmap at {HEATMAP_IMAGE}...")
    data = {src: [] for src in BLOCKLIST_SOURCES}
    for d in filtered_domains:
        for src in BLOCKLIST_SOURCES:
            data[src].append(1 if src in domain_sources[d] else 0)
    df = pd.DataFrame(data, index=filtered_domains)
    plt.figure(figsize=(14, 8))
    sns.set(style="dark")
    sns.heatmap(df.T, cmap="magma", cbar_kws={'label': 'Presence'}, linewidths=0.4, linecolor='black')
    plt.title("🔥 Singularity DNS: Domain Overlap Heatmap 🔥", fontsize=18, fontweight='bold', color='#00ffea')
    plt.xlabel("Domains", fontsize=12, color='#00ffea')
    plt.ylabel("Sources", fontsize=12, color='#00ffea')
    plt.xticks([])
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(HEATMAP_IMAGE, dpi=300, bbox_inches='tight', facecolor='#0a0a0a')
    plt.close()

def generate_markdown_report(priority_count: int, change: int, total_unfiltered: int, excluded_count: int, full_filtered_list: List[str], overlap_counter: DomainCounter, domain_sources: DomainSources) -> None:
    logging.info(f"Generating Markdown report at {REPORT_FILENAME}...")
    report = []
    report.append(f"# 🛡️ Singularity DNS Hacker Dashboard")
    report.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    total_in_one_source = sum(1 for d in full_filtered_list if overlap_counter[d] == 1)
    report.append(f"\n## 📊 Summary Metrics")
    report.append(f"| Metric | Count | Change |")
    report.append(f"| :--- | :--- | :--- |")
    report.append(f"| Priority List Count | {priority_count:,} | {change:+} |")
    report.append(f"| Total Unique Domains (Pre-filter) | {total_unfiltered:,} | |")
    report.append(f"| Domains Excluded by Hagezi TLDs | {excluded_count:,} | |")
    report.append(f"| Total Filtered Domains (Post-filter) | {len(full_filtered_list):,} | |")
    report.append(f"| Domains Unique to 1 Source (Post-filter) | {total_in_one_source:,} | |")
    report.append(f"\n## 🔥 Stacked Domain Overlap Heatmap")
    report.append(f"![Stacked Heatmap]({HEATMAP_IMAGE.name})")
    report.append(f"\n## 💥 Top 50 Domains Per Overlap Level (Sources color-coded)")
    overlap_levels = sorted(set(overlap_counter[d] for d in full_filtered_list), reverse=True)
    for level in overlap_levels:
        domains_in_level = [d for d in full_filtered_list if overlap_counter[d] == level]
        report.append(f"\n### Domains appearing in {level} sources ({len(domains_in_level):,})")
        report.append("| Domain | Sources |")
        report.append("| :--- | :--- |")
        for d in domains_in_level[:50]:
            sources = domain_sources[d]
            badges = " ".join(f"<span style='color:{SOURCE_COLORS[src]};font-weight:bold'>{src}</span>" for src in sorted(sources) if src in SOURCE_COLORS)
            report.append(f"| `{d}` | {badges} |")
        if len(domains_in_level) > 50:
            report.append(f"| ... and {len(domains_in_level) - 50:,} more | |")
    with open(REPORT_FILENAME, "w", encoding="utf-8") as f:
        f.write("\n".join(report))

# --- File Writing ---
def write_output_files(priority_set: DomainSet, abused_tlds: DomainSet, full_domain_list: List[str]) -> None:
    logging.info("Writing output files...")
    with open(PRIORITY_FILENAME, "w", encoding="utf-8") as f:
        f.write(f"# Singularity DNS Priority {PRIORITY_CAP} Blocklist\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Total Domains: {len(priority_set)}\n")
        for d in sorted(priority_set):
            f.write(d + "\n")
    with open(REGEX_TLD_FILENAME, "w", encoding="utf-8") as f:
        f.write(f"# Hagezi Abused TLDs for Regex Blocking\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Total TLDs: {len(abused_tlds)}\n")
        for tld in sorted(abused_tlds):
            f.write(rf"\.{tld}$" + "\n")
    with open(UNFILTERED_FILENAME, "w", encoding="utf-8") as f:
        f.write(f"# Full Aggregated Unfiltered Blocklist\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Total Domains: {len(full_domain_list)}\n")
        for d in sorted(full_domain_list):
            f.write(d + "\n")
    logging.info(f"✅ Priority blocklist: {PRIORITY_FILENAME}")
    logging.info(f"✅ Regex TLD list: {REGEX_TLD_FILENAME}")
    logging.info(f"✅ Full unfiltered list: {UNFILTERED_FILENAME}")
    logging.info(f"📄 Report: {REPORT_FILENAME}")
    logging.info(f"🖼 Stacked heatmap graph: {HEATMAP_IMAGE}")
    logging.info(f"📊 Metrics logged to {HISTORY_FILENAME}")

# --- Main ---
def main():
    start_time = datetime.now()
    logging.info("--- 🛡️ Starting Singularity DNS Blocklist Aggregation ---")
    OUTPUT_DIR.mkdir(exist_ok=True)
    with requests.Session() as session:
        source_sets = fetch_and_process_sources(session)
        combined_counter, overlap_counter, domain_sources = aggregate_and_score_domains(source_sets)
        priority_set, abused_tlds, excluded_count, full_filtered_list = filter_and_prioritize(combined_counter, session)
    priority_count = len(priority_set)
    change = track_history(priority_count)
    generate_overlap_heatmap(full_filtered_list, overlap_counter, domain_sources)
    generate_markdown_report(priority_count, change, len(combined_counter), excluded_count, full_filtered_list, overlap_counter, domain_sources)
    write_output_files(priority_set, abused_tlds, list(combined_counter.keys()))
    end_time = datetime.now()
    logging.info(f"--- ✅ Aggregation Complete in {(end_time - start_time).total_seconds():.2f} seconds ---")

if __name__ == "__main__":
    main()
