import requests
import sys
import os
import csv
from datetime import datetime
from collections import Counter

# --- Configuration ---

BLOCKLIST_SOURCES = {
    "OISD_WILD": "https://raw.githubusercontent.com/sjhgvr/oisd/refs/heads/main/domainswild2_big.txt",
    "HAGEZI_ULTIMATE": "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/wildcard/ultimate-onlydomains.txt",
    "1HOSTS_LITE": "https://raw.githubusercontent.com/badmojr/1Hosts/refs/heads/master/Lite/domains.wildcards",
    "STEVENBLACK_HOSTS": "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"
}

EXCLUSION_URL = "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/wildcard/spam-tlds-onlydomains.txt"

OUTPUT_DIR = "Aggregated_list"
OUTPUT_FILENAME_FILTERED = os.path.join(OUTPUT_DIR, "aggregated_noTLD.txt")
OUTPUT_FILENAME_UNFILTERED = os.path.join(OUTPUT_DIR, "aggregated_withTLD.txt")

HISTORY_FILENAME = os.path.join(OUTPUT_DIR, "history.csv")
REPORT_FILENAME = os.path.join(OUTPUT_DIR, "metrics_report.md") 

# --- Utility Functions (Only the critical file writing functions are shown) ---

def fetch_list(url):
    """Fetches content from a URL, returns a list of lines."""
    print(f"Fetching: {url}")
    try:
        response = requests.get(url, timeout=45) 
        response.raise_for_status()
        return response.text.splitlines()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return []

def process_line(line):
    """Cleans a single line: removes comments, extracts domain from hosts format."""
    line = line.strip().lower()
    
    if not line or line.startswith(('#', '!')):
        return None
        
    parts = line.split()
    if len(parts) > 1 and parts[0] in ('0.0.0.0', '127.0.0.1'):
        domain = parts[1]
    elif len(parts) == 1:
        domain = parts[0]
    else:
        return None
        
    if domain in ('localhost', '::1', '255.255.255.255'):
        return None
        
    return domain.strip()

def extract_tld(domain):
    """Extracts the 'TLD' component (the last segment after the final dot) for filtering."""
    domain = domain.lstrip('*').lstrip('.').strip()
    if not domain:
        return None
    return domain.split('.')[-1]

def track_history(final_metrics):
    """Reads, updates, and writes the list size history, including all counts."""
    
    source_names = list(BLOCKLIST_SOURCES.keys())
    
    header = ['Date', 'Final_Count', 'Change', 'Total_Unfiltered', 'Excluded_Count', 'Unique_Count'] + [f'Source_{name}' for name in source_names]
    
    history = []
    
    if os.path.exists(HISTORY_FILENAME):
        with open(HISTORY_FILENAME, 'r') as f:
            reader = csv.reader(f)
            history = list(reader)
            if history and history[0] == header:
                history.pop(0)

    current_date = datetime.now().strftime('%Y-%m-%d')
    current_final_count = final_metrics['Final_Count']
    
    last_count = int(history[-1][1]) if history else 0
    change = current_final_count - last_count
    
    new_entry = [current_date, str(current_final_count), str(change), str(final_metrics['Total_Unfiltered']), str(final_metrics['Excluded_Count']), str(final_metrics['Unique_Count'])]
    
    for name in source_names:
        new_entry.append(str(final_metrics['Source_Counts'][name]))
    
    history.append(new_entry)

    with open(HISTORY_FILENAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(history)
        
    return change

def generate_markdown_report(metrics, domain_appearance_counter, final_list_set, source_sets, change_in_size):
    """Generates a readable Markdown report with metrics and analysis."""
    
    report_content = []
    report_content.append(f"# 🛡️ Blocklist Aggregation Report\n")
    report_content.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    report_content.append(f"\n---\n")

    # --- Section 1: Summary Metrics (Table) ---
    report_content.append(f"## 📊 Run Summary Metrics\n")
    report_content.append(f"\n| Metric | Count | Change Since Last Run |")
    report_content.append(f"| :--- | :--- | :--- |")
    report_content.append(f"| **Final Filtered Count** | {metrics['Final_Count']:,} | **{change_in_size:+}** |")
    report_content.append(f"| Total Unique Domains (Unfiltered) | {metrics['Total_Unfiltered']:,} | |")
    report_content.append(f"| Domains Excluded by Spam TLD Filter | {metrics['Excluded_Count']:,} | |")
    report_content.append(f"| Domains Unique to ONLY One Source | {metrics['Unique_Count']:,} | |\n")
    
    # --- Section 2: Source Contribution ---
    report_content.append(f"\n## 📚 Source List Contribution\n")
    report_content.append(f"\n| Source List | Initial Count |")
    report_content.append(f"| :--- | :--- |")
    for name, count in metrics['Source_Counts'].items():
        report_content.append(f"| {name.replace('_', ' ')} | {count:,} |")
    report_content.append(f"\n---\n")

    # --- Section 3: Overlap and Analysis ---
    
    # Identify unique and top domains
    unique_domains_only = {domain for domain, count in domain_appearance_counter.items() if count == 1}
    unique_in_final = {d for d in unique_domains_only if d in final_list_set}
    
    report_content.append(f"## ✨ Overlap Analysis (Top & Unique Domains)\n")
    report_content.append(f"### Most Common Domains (Appearing in Multiple Source Lists)\n")
    report_content.append(f"*(Showing up to 50 examples that made it into the final list)*\n")
    
    for count in range(len(source_sets), 1, -1):
        domain_set = {domain for domain, c in domain_appearance_counter.items() 
                      if c == count and domain in final_list_set}
        report_content.append(f"\n#### Found in ALL {count} Lists ({len(domain_set):,} domains total)\n")
        report_content.append("```\n")
        for i, domain in enumerate(sorted(list(domain_set))):
            if i >= 50:
                report_content.append(f"... and {len(domain_set) - 50} more.\n")
                break
            report_content.append(f"{domain}\n")
        report_content.append("```\n")

    report_content.append(f"\n### Exclusive Contributions (Domains Unique to ONE List)\n")
    report_content.append(f"Total Unique Domains (in final filtered list): {len(unique_in_final):,}\n")

    # Group unique domains by the list they belong to
    unique_by_source = {}
    for name, domain_set in source_sets.items():
        unique_by_source[name] = [d for d in domain_set if domain_appearance_counter[d] == 1 and d in final_list_set]

    for name, unique_list in unique_by_source.items():
        report_content.append(f"\n#### Unique to {name.replace('_', ' ')} ({len(unique_list):,} domains)\n")
        report_content.append("```\n")
        for i, domain in enumerate(sorted(unique_list)):
            if i >= 50:
                report_content.append(f"... and {len(unique_list) - 50} more.\n")
                break
            f'{domain}\n'
        report_content.append("```\n")

    # *** FIX: Using explicit UTF-8 encoding for reliable writing ***
    try:
        with open(REPORT_FILENAME, "w", encoding='utf-8') as f:
            f.write("\n".join(report_content))
    except Exception as e:
        print(f"FATAL ERROR writing Markdown report: {e}", file=sys.stderr)
        # We allow the script to continue to write the other critical files

    return len(unique_domains_only)


def write_blocklist_file(filename, list_set, source_sets, initial_count, excluded_count, total_unique_count=None, change_in_size=None, is_filtered=True):
    """Writes the blocklist file with an appropriate header."""
    sorted_list = sorted(list(list_set))
    final_count = len(sorted_list)
    
    # Use explicit UTF-8 encoding for blocklists as well
    with open(filename, "w", encoding='utf-8') as f:
        f.write("# Blocklist Aggregation Report\n")
        f.write(f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# ------------------------------------------------------------------\n")
        
        if is_filtered:
            f.write(f"# TYPE: Filtered List (Spam TLDs REMOVED) - {os.path.basename(filename)}\n")
        else:
            f.write(f"# TYPE: Unfiltered List (Contains ALL unique domains) - {os.path.basename(filename)}\n")
            
        f.write("# ------------------------------------------------------------------\n")
        
        f.write(f"# INITIAL SOURCES COUNT:\n")
        for name, domain_set in source_sets.items():
             f.write(f"#   - {name}: {len(domain_set):,}\n")
        f.write("# ------------------------------------------------------------------\n")
        
        if is_filtered:
            f.write(f"# FILTERED METRICS:\n")
            f.write(f"#   - Total unique domains before filtering: {initial_count:,}\n")
            f.write(f"#   - Domains excluded by Spam TLD filter: {excluded_count:,}\n")
            f.write(f"#   - Domains unique to ONLY one source list (unfiltered): {total_unique_count:,}\n")
            f.write(f"#   - FINAL FILTERED COUNT: {final_count:,}\n")
            f.write(f"#   - Size change since last run: {change_in_size:+}\n\n")
        else:
            f.write(f"# UNFILTERED METRICS:\n")
            f.write(f"#   - FINAL UNFILTERED COUNT: {final_count:,}\n\n")

        for entry in sorted_list:
            f.write(entry + "\n")


# --- Main Logic ---

def generate_blocklist():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. Fetch and Process Exclusion List
    raw_exclusion_lines = fetch_list(EXCLUSION_URL)
    exclude_tlds = set()
    for line in raw_exclusion_lines:
        domain = process_line(line)
        if domain:
            tld_segment = extract_tld(domain)
            if tld_segment:
                exclude_tlds.add(tld_segment)
    
    print(f"\nIdentified {len(exclude_tlds)} TLDs for exclusion.")

    # 2. Fetch and Process All Blocklists Separately and Count Overlap
    source_sets = {}
    combined_domains = set()
    domain_appearance_counter = Counter()

    for name, url in BLOCKLIST_SOURCES.items():
        raw_lines = fetch_list(url)
        current_set = set()
        for line in raw_lines:
            domain = process_line(line)
            if domain:
                current_set.add(domain)
                
        for domain in current_set:
            combined_domains.add(domain) 
            domain_appearance_counter[domain] += 1
                
        source_sets[name] = current_set
        print(f" -> {name}: {len(current_set):,} entries.")
    
    initial_count = len(combined_domains)
    
    # 3. Filter Combined List (TLD Exclusion)
    final_list_set_filtered = set()
    excluded_count = 0
    
    for domain in combined_domains:
        domain_tld = extract_tld(domain)
        
        if domain_tld in exclude_tlds:
            excluded_count += 1
        else:
            final_list_set_filtered.add(domain)

    final_count_filtered = len(final_list_set_filtered)

    # 4. Prepare Metrics Dictionary for History and Report Generation
    total_unique_unfiltered_count = len({domain for domain, count in domain_appearance_counter.items() if count == 1})
    
    metrics = {
        'Final_Count': final_count_filtered,
        'Total_Unfiltered': initial_count,
        'Excluded_Count': excluded_count,
        'Unique_Count': total_unique_unfiltered_count,
        'Source_Counts': {name: len(s) for name, s in source_sets.items()}
    }
    
    # 5. Track History (This calculates change_in_size and updates history.csv)
    change_in_size = track_history(metrics)
    
    # 6. Generate Markdown Report
    generate_markdown_report(metrics, domain_appearance_counter, final_list_set_filtered, source_sets, change_in_size)
    
    # 7. Write Final Blocklists
    
    # A) Write the UNFILTERED list (Aggregated_list/aggregated_withTLD.txt)
    write_blocklist_file(
        OUTPUT_FILENAME_UNFILTERED, combined_domains, source_sets, 
        initial_count, excluded_count, is_filtered=False
    )
    
    # B) Write the FILTERED list (Aggregated_list/aggregated_noTLD.txt)
    write_blocklist_file(
        OUTPUT_FILENAME_FILTERED, final_list_set_filtered, source_sets, 
        initial_count, excluded_count, total_unique_unfiltered_count, change_in_size, is_filtered=True
    )
    
    print(f"\n✅ Successfully created blocklists.")
    print(f"📊 Central metrics logged to history.csv.")
    print(f"📄 Detailed report generated: {REPORT_FILENAME}.")

if __name__ == "__main__":
    generate_blocklist()
