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
# List 1: The final, filtered list (NO spam TLDs)
OUTPUT_FILENAME_FILTERED = os.path.join(OUTPUT_DIR, "aggregated_noTLD.txt")
# List 2: The full, unfiltered combined list (WITH spam TLDs)
OUTPUT_FILENAME_UNFILTERED = os.path.join(OUTPUT_DIR, "aggregated_withTLD.txt")

HISTORY_FILENAME = os.path.join(OUTPUT_DIR, "history.csv")
ANALYSIS_FILENAME = os.path.join(OUTPUT_DIR, "overlap_analysis.txt")

# --- Utility Functions ---

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
    
    # Remove comments (lines starting with # or !) and ignore empty lines
    if not line or line.startswith(('#', '!')):
        return None
        
    # Handle hosts file format (e.g., '0.0.0.0 example.com')
    parts = line.split()
    if len(parts) > 1 and parts[0] in ('0.0.0.0', '127.0.0.1'):
        domain = parts[1]
    elif len(parts) == 1:
        domain = parts[0]
    else:
        return None
        
    # Basic validation/cleanup for common non-domain entries
    if domain in ('localhost', '::1', '255.255.255.255'):
        return None
        
    return domain.strip()

def extract_tld(domain):
    """Extracts the 'TLD' component (the last segment after the final dot) for filtering."""
    domain = domain.lstrip('*').lstrip('.').strip()
    if not domain:
        return None
    return domain.split('.')[-1]

def track_history(final_count):
    """Reads, updates, and writes the list size history."""
    header = ['Date', 'Final_Count', 'Change']
    history = []
    
    if os.path.exists(HISTORY_FILENAME):
        with open(HISTORY_FILENAME, 'r') as f:
            reader = csv.reader(f)
            history = list(reader)
            if history and history[0] == header:
                history.pop(0)

    current_date = datetime.now().strftime('%Y-%m-%d')
    
    last_count = int(history[-1][1]) if history else 0
    change = final_count - last_count
    
    new_entry = [current_date, str(final_count), str(change)]
    history.append(new_entry)

    with open(HISTORY_FILENAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(history)
        
    return change

def perform_overlap_analysis(source_sets, domain_appearance_counter, final_list_set, total_unique_unfiltered_count):
    """Identifies unique domains and top domains appearing across lists."""
    
    unique_domains_only = {domain for domain, count in domain_appearance_counter.items() if count == 1}
    
    # Identify top domains by appearance count, but only include those that are NOT filtered out
    top_domains = {}
    
    for i in range(len(source_sets), 1, -1):
        top_domains[f'{i}_lists'] = {domain for domain, count in domain_appearance_counter.items() 
                                     if count == i and domain in final_list_set}
    
    # Domains unique to one list and made it into the final list
    unique_in_final = {d for d in unique_domains_only if d in final_list_set}
    
    # Write analysis to a new file
    with open(ANALYSIS_FILENAME, "w") as f:
        f.write(f"Overlap Analysis Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("------------------------------------------------------------------\n")
        f.write(f"Total Unique Domains (All Sources, Before Filter): {total_unique_unfiltered_count:,}\n")
        
        # Top Domains (Most Common)
        f.write(f"\n## Top Domains (Appearing in Multiple Source Lists)\n")
        f.write(f"NOTE: Only lists domains that made it into the final '{os.path.basename(OUTPUT_FILENAME_FILTERED)}' blocklist.\n\n")
        
        for count in range(len(source_sets), 1, -1):
            key = f'{count}_lists'
            domain_set = top_domains[key]
            f.write(f"### Domains in ALL {count} Lists ({len(domain_set):,} domains)\n")
            # Limit the output to the top 50 examples for readability
            for i, domain in enumerate(sorted(list(domain_set))):
                if i >= 50:
                    f.write(f"... and {len(domain_set) - 50} more.\n")
                    break
                f.write(f"{domain}\n")
            f.write("\n")
            
        # Unique Domains
        f.write(f"\n## Unique Domains (Appearing in ONLY One Source List)\n")
        f.write(f"Total Unique Domains (in final filtered list): {len(unique_in_final):,}\n")
        
        unique_by_source = {}
        for name, domain_set in source_sets.items():
            unique_by_source[name] = [d for d in domain_set if domain_appearance_counter[d] == 1 and d in final_list_set]

        for name, unique_list in unique_by_source.items():
            f.write(f"### Unique to {name} ({len(unique_list):,} domains)\n")
            # Limit the output to the top 50 examples for readability
            for i, domain in enumerate(sorted(unique_list)):
                if i >= 50:
                    f.write(f"... and {len(unique_list) - 50} more.\n")
                    break
                f.write(f"{domain}\n")
            f.write("\n")
            
    return len(unique_domains_only)

def write_blocklist_file(filename, list_set, source_sets, initial_count, excluded_count, total_unique_count=None, change_in_size=None, is_filtered=True):
    """Writes the blocklist file with an appropriate header."""
    sorted_list = sorted(list(list_set))
    final_count = len(sorted_list)
    
    with open(filename, "w") as f:
        f.write("# Blocklist Aggregation Report\n")
        f.write(f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# ------------------------------------------------------------------\n")
        
        if is_filtered:
            f.write(f"# TYPE: Filtered List (Spam TLDs REMOVED)\n")
        else:
            f.write(f"# TYPE: Unfiltered List (Contains ALL unique domains)\n")
            
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
    combined_domains = set() # This is the full, unfiltered list
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
    
    # The full list count before TLD filtering
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
    
    # 4. Perform Overlap Analysis
    total_unique_count = perform_overlap_analysis(source_sets, domain_appearance_counter, final_list_set_filtered, initial_count)
    
    # 5. Track History (only tracks the filtered list size)
    change_in_size = track_history(final_count_filtered)
    
    # 6. Write Final Lists
    
    # A) Write the UNFILTERED list (Aggregated_list/aggregated_withTLD.txt)
    write_blocklist_file(
        OUTPUT_FILENAME_UNFILTERED, combined_domains, source_sets, 
        initial_count, excluded_count, is_filtered=False
    )
    
    # B) Write the FILTERED list (Aggregated_list/aggregated_noTLD.txt)
    write_blocklist_file(
        OUTPUT_FILENAME_FILTERED, final_list_set_filtered, source_sets, 
        initial_count, excluded_count, total_unique_count, change_in_size, is_filtered=True
    )
    
    print(f"\n✅ Successfully created {os.path.basename(OUTPUT_FILENAME_UNFILTERED)} ({initial_count:,} entries).")
    print(f"✅ Successfully created {os.path.basename(OUTPUT_FILENAME_FILTERED)} ({final_count_filtered:,} entries).")
    print(f"📊 Metrics, history, and detailed overlap analysis saved in {OUTPUT_DIR}/.")

if __name__ == "__main__":
    generate_blocklist()
