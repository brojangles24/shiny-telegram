import requests, sys, os, csv
from datetime import datetime
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

# --- Config ---
BLOCKLIST_SOURCES = {
    "OISD_BIG": "https://raw.githubusercontent.com/oisd/oisd/main/blocks/hosts/oisd_blocklist.txt",
    "HAGEZI_ULTIMATE": "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/wildcard/ultimate-onlydomains.txt",
    "1HOSTS_LITE": "https://raw.githubusercontent.com/badmojr/1Hosts/refs/heads/master/Lite/domains.wildcards",
    "STEVENBLACK_HOSTS": "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"
}

HAGEZI_ABUSED_TLDS = "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/wildcard/most-abused-tlds.txt"

OUTPUT_DIR = "Aggregated_list"
PRIORITY_FILENAME = os.path.join(OUTPUT_DIR, "priority_300k.txt")
REGEX_TLD_FILENAME = os.path.join(OUTPUT_DIR, "regex_hagezi_tlds.txt")
UNFILTERED_FILENAME = os.path.join(OUTPUT_DIR, "aggregated_full.txt")
HISTORY_FILENAME = os.path.join(OUTPUT_DIR, "history.csv")
REPORT_FILENAME = os.path.join(OUTPUT_DIR, "metrics_report.md")
HEATMAP_IMAGE = os.path.join(OUTPUT_DIR, "overlap_heatmap_sources.png")

PRIORITY_CAP = 300000
SOURCE_WEIGHTS = {"HAGEZI_ULTIMATE": 3, "OISD_BIG": 2, "1HOSTS_LITE": 1, "STEVENBLACK_HOSTS": 1}
SOURCE_COLORS = {"HAGEZI_ULTIMATE":"#d62728","OISD_BIG":"#1f77b4","1HOSTS_LITE":"#2ca02c","STEVENBLACK_HOSTS":"#ff7f0e"}

# --- Utility ---
def fetch_list(url):
    try:
        resp = requests.get(url, timeout=45)
        resp.raise_for_status()
        return [line.strip().lower() for line in resp.text.splitlines() if line.strip()]
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return []

def process_domain(line):
    if line.startswith(('#','!')): return None
    parts = line.split()
    if len(parts)>1 and parts[0] in ("0.0.0.0","127.0.0.1"): domain = parts[1]
    elif len(parts)==1: domain = parts[0]
    else: return None
    if domain in ("localhost","::1","255.255.255.255"): return None
    return domain.strip()

def extract_tld(domain):
    domain = domain.lstrip("*").lstrip(".")
    return domain.split(".")[-1] if domain else None

def track_history(count):
    header = ["Date","Priority_Count","Change"]
    history=[]
    if os.path.exists(HISTORY_FILENAME):
        with open(HISTORY_FILENAME,"r") as f:
            reader=list(csv.reader(f))
            if reader and reader[0]==header: reader.pop(0)
            history=reader
    last=int(history[-1][1]) if history else 0
    change=count-last
    history.append([datetime.now().strftime("%Y-%m-%d"),str(count),str(change)])
    with open(HISTORY_FILENAME,"w",newline="") as f:
        writer=csv.writer(f)
        writer.writerow(header)
        writer.writerows(history)
    return change

# --- Main ---
def generate_cyberpunk_blocklist():
    os.makedirs(OUTPUT_DIR,exist_ok=True)

    # Parallel fetch
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_name={executor.submit(fetch_list,url):name for name,url in BLOCKLIST_SOURCES.items()}
        source_sets={}
        for future in future_to_name:
            name=future_to_name[future]
            lines=future.result()
            domains=set(filter(None,[process_domain(l) for l in lines]))
            source_sets[name]=domains
            print(f"Fetched {len(domains):,} domains from {name}")

    # Weighted counters and overlap trackers
    combined_counter=Counter()
    overlap_counter=Counter()
    domain_sources=defaultdict(set)

    for name,domains in source_sets.items():
        weight=SOURCE_WEIGHTS.get(name,1)
        for d in domains:
            combined_counter[d]+=weight
            overlap_counter[d]+=1
            domain_sources[d].add(name)

    # Exclude Hagezi abused TLDs and generate regex for auto-block
    abused_tlds=set(filter(None,[line.strip().lower() for line in fetch_list(HAGEZI_ABUSED_TLDS) if not line.startswith("#")]))
    print(f"Excluding {len(abused_tlds)} Hagezi abused TLDs")

    filtered_domains=[d for d in combined_counter if extract_tld(d) not in abused_tlds]
    excluded_count=len(combined_counter)-len(filtered_domains)
    filtered_domains.sort(key=lambda d: combined_counter[d],reverse=True)
    final_priority=set(filtered_domains[:PRIORITY_CAP])

    # Metrics
    total_unique=len([d for d,c in overlap_counter.items() if c==1])
    metrics={"Total_Unfiltered":len(combined_counter),"Excluded_Count":excluded_count,"Unique_Count":total_unique}
    change=track_history(len(final_priority))

    # --- Stacked Heatmap Graph ---
    overlap_levels = sorted(set(overlap_counter[d] for d in filtered_domains), reverse=True)
    stacked_data = {src:[0]*len(overlap_levels) for src in BLOCKLIST_SOURCES.keys()}

    for i,level in enumerate(overlap_levels):
        for d in filtered_domains:
            if overlap_counter[d]==level:
                for src in domain_sources[d]:
                    stacked_data[src][i]+=1

    bottom = [0]*len(overlap_levels)
    plt.figure(figsize=(12,6))
    for src,color in SOURCE_COLORS.items():
        plt.bar([str(l) for l in overlap_levels], stacked_data[src], bottom=bottom, color=color, label=src)
        bottom=[sum(x) for x in zip(bottom,stacked_data[src])]

    plt.xlabel("Number of Sources Domain Appears In")
    plt.ylabel("Domain Count")
    plt.title("Cyberpunk Stacked Domain Overlap Heatmap")
    plt.legend()
    plt.tight_layout()
    plt.savefig(HEATMAP_IMAGE)
    plt.close()

    # --- Markdown report ---
    report=[]
    report.append(f"# 🛡️ Cyberpunk Blocklist Hacker Dashboard")
    report.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

    report.append(f"\n## 📊 Summary Metrics")
    report.append(f"| Metric | Count | Change |")
    report.append(f"| :--- | :--- | :--- |")
    report.append(f"| Priority List Count | {len(final_priority):,} | {change:+} |")
    report.append(f"| Total Unique Domains | {metrics['Total_Unfiltered']:,} | |")
    report.append(f"| Domains Excluded by Hagezi TLDs | {metrics['Excluded_Count']:,} | |")
    report.append(f"| Domains Unique to 1 Source | {metrics['Unique_Count']:,} | |")

    report.append(f"\n## 🔥 Stacked Domain Overlap Heatmap")
    report.append(f"![Stacked Heatmap]({os.path.basename(HEATMAP_IMAGE)})")

    # --- Top domains per overlap level ---
    report.append(f"\n## 💥 Top 50 Domains Per Overlap Level (Sources color-coded)")
    for level in sorted(overlap_levels, reverse=True):
        domains_in_level = [d for d in filtered_domains if overlap_counter[d]==level]
        report.append(f"\n### Domains appearing in {level} sources ({len(domains_in_level):,})")
        report.append("| Domain | Sources |")
        report.append("| :--- | :--- |")
        for d in domains_in_level[:50]:
            sources=domain_sources[d]
            badges=" ".join([f"<span style='color:{SOURCE_COLORS[src]};font-weight:bold'>{src}</span>" for src in sources])
            report.append(f"| {d} | {badges} |")
        if len(domains_in_level)>50:
            report.append(f"| ... and {len(domains_in_level)-50} more | |")

    with open(REPORT_FILENAME,"w",encoding="utf-8") as f:
        f.write("\n".join(report))

    # --- Output files ---
    with open(PRIORITY_FILENAME,"w",encoding="utf-8") as f:
        f.write(f"# Priority {PRIORITY_CAP} Blocklist\n")
        for d in sorted(final_priority): f.write(d+"\n")

    # Auto-generate regex TLD blocklist from Hagezi abused TLDs
    with open(REGEX_TLD_FILENAME,"w",encoding="utf-8") as f:
        for tld in sorted(abused_tlds):
            f.write(rf"\.{tld}$"+"\n")  # ready to drop into Pi-hole / Cloudflare regex

    with open(UNFILTERED_FILENAME,"w",encoding="utf-8") as f:
        for d in sorted(combined_counter): f.write(d+"\n")

    print(f"✅ Priority blocklist: {PRIORITY_FILENAME}")
    print(f"✅ Regex TLD list: {REGEX_TLD_FILENAME}")
    print(f"✅ Full unfiltered list: {UNFILTERED_FILENAME}")
    print(f"📄 Report: {REPORT_FILENAME}")
    print(f"🖼 Stacked heatmap graph: {HEATMAP_IMAGE}")
    print(f"📊 Metrics logged to {HISTORY_FILENAME}")

if __name__=="__main__":
    generate_cyberpunk_blocklist()
