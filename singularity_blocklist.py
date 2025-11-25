#!/usr/bin/env python3
"""
Singularity DNS Blocklist Aggregator
- Fetches multiple blocklists
- De-duplicates and scores with weights
- Filters TLDs
- Generates priority/capped list, full list, regex list
- Interactive Plotly heatmap
- Markdown report with color-coded sources
"""

import sys, csv, logging
from datetime import datetime
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple

import requests
import plotly.graph_objects as go
import plotly.io as pio

# --- Configuration ---
BLOCKLIST_SOURCES: Dict[str, str] = {
    "OISD_BIG": "https://raw.githubusercontent.com/sjhgvr/oisd/refs/heads/main/domainswild2_big.txt",
    "HAGEZI_ULTIMATE": "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/wildcard/ultimate-onlydomains.txt",
    "1HOSTS_LITE": "https://raw.githubusercontent.com/badmojr/1Hosts/refs/heads/master/Lite/domains.wildcards",
    "STEVENBLACK_HOSTS": "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"
}
HAGEZI_ABUSED_TLDS: str = "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/wildcard/spam-tlds-onlydomains.txt"

OUTPUT_DIR = Path("Aggregated_list")
PRIORITY_FILENAME = OUTPUT_DIR / "priority_300k.txt"
REGEX_TLD_FILENAME = OUTPUT_DIR / "regex_hagezi_tlds.txt"
UNFILTERED_FILENAME = OUTPUT_DIR / "aggregated_full.txt"
HISTORY_FILENAME = OUTPUT_DIR / "history.csv"
REPORT_FILENAME = OUTPUT_DIR / "metrics_report.md"
HEATMAP_IMAGE = OUTPUT_DIR / "overlap_heatmap_sources.png"
DASHBOARD_HTML = OUTPUT_DIR / "dashboard.html"

PRIORITY_CAP = 300_000
SOURCE_WEIGHTS = {"HAGEZI_ULTIMATE":3,"OISD_BIG":2,"1HOSTS_LITE":1,"STEVENBLACK_HOSTS":1}
SOURCE_COLORS = {"HAGEZI_ULTIMATE":"#d62728","OISD_BIG":"#1f77b4","1HOSTS_LITE":"#2ca02c","STEVENBLACK_HOSTS":"#ff7f0e"}

# --- Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.StreamHandler(sys.stdout)])

# --- Utility ---
def fetch_list(url:str, session:requests.Session)->List[str]:
    try: resp=session.get(url,timeout=45); resp.raise_for_status(); return [l.strip().lower() for l in resp.text.splitlines() if l.strip()]
    except requests.exceptions.RequestException as e: logging.error(f"Error fetching {url}: {e}"); return []

def process_domain(line:str)->Optional[str]:
    if not line or line.startswith(("#","!")): return None
    parts=line.split(); domain=""
    if len(parts)==1: domain=parts[0]
    elif len(parts)>1 and parts[0] in ("0.0.0.0","127.0.0.1"): domain=parts[1]
    else: return None
    if domain in ("localhost","localhost.localdomain","::1","255.255.255.255"): return None
    return domain.strip()

def extract_tld(domain:str)->Optional[str]:
    domain=domain.lstrip("*").lstrip(".")
    if "." not in domain: return None
    return domain.split(".")[-1]

def track_history(count:int)->int:
    HEADER=["Date","Priority_Count","Change"]; history=[]; last_count=0
    if HISTORY_FILENAME.exists():
        try:
            with open(HISTORY_FILENAME,"r",newline="",encoding="utf-8") as f:
                reader=csv.DictReader(f)
                if reader.fieldnames==HEADER: history=list(reader); last_count=int(history[-1]["Priority_Count"]) if history else 0
        except: pass
    change=count-last_count; today=datetime.now().strftime("%Y-%m-%d")
    if history and history[-1]["Date"]==today: history[-1]["Priority_Count"]=str(count); history[-1]["Change"]=str(change)
    else: history.append({"Date":today,"Priority_Count":str(count),"Change":str(change)})
    try:
        with open(HISTORY_FILENAME,"w",newline="",encoding="utf-8") as f: csv.DictWriter(f,fieldnames=HEADER).writeheader(); csv.DictWriter(f,fieldnames=HEADER).writerows(history)
    except: pass
    return change

# --- Core Functions ---
def fetch_and_process_sources(session:requests.Session)->Dict[str,Set[str]]:
    source_sets={}
    with ThreadPoolExecutor(max_workers=len(BLOCKLIST_SOURCES)) as executor:
        future_to_name={executor.submit(fetch_list,url,session):name for name,url in BLOCKLIST_SOURCES.items()}
        for f in future_to_name:
            name=future_to_name[f]; lines=f.result(); domains=set(filter(None,[process_domain(l) for l in lines])); source_sets[name]=domains
            logging.info(f"Fetched {len(domains):,} domains from {name}")
    return source_sets

def aggregate_and_score_domains(source_sets:Dict[str,Set[str]]):
    combined_counter=Counter(); overlap_counter=Counter(); domain_sources=defaultdict(set)
    for name,domains in source_sets.items(): w=SOURCE_WEIGHTS.get(name,1); 
        for d in domains: combined_counter[d]+=w; overlap_counter[d]+=1; domain_sources[d].add(name)
    return combined_counter, overlap_counter, domain_sources

def filter_and_prioritize(combined_counter:Counter, session:requests.Session):
    tld_lines=fetch_list(HAGEZI_ABUSED_TLDS, session)
    abused_tlds=set(l.strip() for l in tld_lines if l and not l.startswith("#"))
    logging.info(f"Excluding {len(abused_tlds)} Hagezi abused TLDs")
    filtered_weighted=[]; excluded_count=0
    for d,w in combined_counter.items():
        filtered_weighted.append((d,w)) if extract_tld(d) not in abused_tlds else excluded_count+=1
    filtered_weighted.sort(key=lambda x:x[1],reverse=True)
    final_priority={d for d,_ in filtered_weighted[:PRIORITY_CAP]}
    full_filtered=[d for d,_ in filtered_weighted]
    logging.info(f"Excluded {excluded_count:,} domains; Priority list: {len(final_priority):,}")
    return final_priority, abused_tlds, excluded_count, full_filtered

# --- Heatmap ---
def generate_interactive_heatmap(filtered_domains, overlap_counter, domain_sources):
    logging.info(f"Generating interactive heatmap at {HEATMAP_IMAGE}")
    overlap_levels=sorted(set(overlap_counter[d] for d in filtered_domains),reverse=True)
    sources=list(BLOCKLIST_SOURCES.keys())
    heatmap_data={src:[] for src in sources}
    for lvl in overlap_levels:
        doms=[d for d in filtered_domains if overlap_counter[d]==lvl]
        for src in sources: heatmap_data[src].append(sum(1 for d in doms if src in domain_sources[d]))
    fig=go.Figure(); bottom=[0]*len(overlap_levels)
    for src in sources:
        fig.add_trace(go.Bar(x=[str(l) for l in overlap_levels],y=heatmap_data[src],name=src,marker_color=SOURCE_COLORS[src],text=[f"{c} domains from {src}" for c in heatmap_data[src]],hoverinfo="text"))
    fig.update_layout(barmode='stack',title="Singularity DNS Domain Overlap Heatmap",xaxis_title="Number of Sources Domain Appears In",yaxis_title="Domain Count (Filtered List)",template="plotly_dark")
    pio.write_html(fig,str(DASHBOARD_HTML).replace(".html","_heatmap.html"),auto_open=False)
    fig.write_image(str(HEATMAP_IMAGE))

# --- Markdown Report ---
def generate_markdown_report(priority_count,change,total_unfiltered,excluded_count,full_filtered_list,overlap_counter,domain_sources):
    logging.info(f"Generating Markdown report at {REPORT_FILENAME}")
    report=[]
    report.append(f"# 🛡️ Singularity DNS Blocklist Dashboard")
    report.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    total_unique_one=sum(1 for d in full_filtered_list if overlap_counter[d]==1)
    report.append("\n## 📊 Summary Metrics")
    report.append("| Metric | Count | Change |"); report.append("| :--- | :--- | :--- |")
    report.append(f"| Priority List Count | {priority_count:,} | {change:+} |")
    report.append(f"| Total Unique Domains (Pre-filter) | {total_unfiltered:,} | |")
    report.append(f"| Domains Excluded by Hagezi TLDs | {excluded_count:,} | |")
    report.append(f"| Total Filtered Domains (Post-filter) | {len(full_filtered_list):,} | |")
    report.append(f"| Domains Unique to 1 Source | {total_unique_one:,} | |")
    report.append("\n## 🔥 Interactive Stacked Domain Overlap Heatmap")
    report.append(f"<iframe src='{DASHBOARD_HTML.stem}_heatmap.html' width='100%' height='600'></iframe>")
    with open(REPORT_FILENAME,"w",encoding="utf-8") as f: f.write("\n".join(report))

# --- File Writing ---
def write_output_files(priority_set, abused_tlds, full_list):
    logging.info("Writing output files...")
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(PRIORITY_FILENAME,"w",encoding="utf-8") as f:
        f.write(f"# Priority {PRIORITY_CAP} Blocklist\n# Generated: {datetime.now()}\n# Total: {len(priority_set)}\n"); f.writelines(d+"\n" for d in sorted(priority_set))
    with open(REGEX_TLD_FILENAME,"w",encoding="utf-8") as f:
        f.write(f"# Hagezi Abused TLDs\n# Generated: {datetime.now()}\n# Total: {len(abused_tlds)}\n"); f.writelines(rf"\.{t}$\n" for t in sorted(abused_tlds))
    with open(UNFILTERED_FILENAME,"w",encoding="utf-8") as f:
        f.write(f"# Full Aggregated List\n# Generated: {datetime.now()}\n# Total: {len(full_list)}\n"); f.writelines(d+"\n" for d in sorted(full_list))
    logging.info(f"✅ Priority: {PRIORITY_FILENAME} | Regex: {REGEX_TLD_FILENAME} | Full: {UNFILTERED_FILENAME} | Report: {REPORT_FILENAME} | Heatmap: {HEATMAP_IMAGE}")

# --- Main ---
def main():
    start=datetime.now(); logging.info("--- 🛡️ Starting Singularity DNS Aggregation ---")
    OUTPUT_DIR.mkdir(exist_ok=True)
    with requests.Session() as session:
        sources=fetch_and_process_sources(session)
        combined,overlap,domain_sources=aggregate_and_score_domains(sources)
        priority_set, abused_tlds, excluded_count, full_filtered=filter_and_prioritize(combined,session)
    change=track_history(len(priority_set))
    generate_interactive_heatmap(full_filtered,overlap,domain_sources)
    generate_markdown_report(len(priority_set),change,len(combined),excluded_count,full_filtered,overlap,domain_sources)
    write_output_files(priority_set,abused_tlds,list(combined.keys()))
    logging.info(f"--- ✅ Aggregation Complete in {(datetime.now()-start).total_seconds():.2f}s ---")

if __name__=="__main__": main()
