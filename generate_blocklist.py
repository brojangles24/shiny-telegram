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
OUTPUT_FILENAME = os.path.join(OUTPUT_DIR, "combined_blocklist.txt")
HISTORY_FILENAME = os.path.join(OUTPUT_DIR, "history.csv")
METRICS_FILENAME = os.path.join(OUTPUT_DIR, "metrics.json") # For detailed counts

# --- Utility Functions ---

def fetch_list(url):
    """Fetches content from a URL, returns a list of lines."""
    print(f"Fetching: {url}")
    try:
        response = requests.get(url, timeout=30)
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
    # Use split to get the last component, which is treated as the TLD for this filter
    return domain.split('.')[-1]

def track_history(final_count):
    """Reads, updates, and writes the list size history."""
    header = ['Date', 'Final_Count', 'Change']
    history = []
    
    if os.path.exists(HISTORY_FILENAME):
        with open(HISTORY_FILENAME, 'r') as f:
            reader = csv.reader(f)
            history = list(reader)
            # Remove header if it exists
            if history and history[0] == header:
                history.pop(0)

    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Calculate change from last entry
    last_count = int(history[-1][1]) if history else 0
    change = final_count - last_count
    
    new_entry = [current_date, str(final_count), str(change)]
    history.append(new_entry)

    with open(HISTORY_FILENAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(history)
        
    return change

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

    # 2. Fetch and Process All Blocklists Separately
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
                combined_domains.add(domain) # Build master list for counting
                
        source_sets[name] = current_set
        print(f" -> {name}: {len(current_set)} entries.")
    
    # 3. Analyze Uniqueness
    for domain in combined_domains:
        for name, domain_set in source_sets.items():
            if domain in domain_set:
                domain_appearance_counter[domain] += 1
                
    # Identify domains unique to only one list
    unique_domains_only = {domain for domain, count in domain_appearance_counter.items() if count == 1}
    
    # 4. Filter Combined List (TLD Exclusion)
    initial_count = len(combined_domains)
    final_list_set = set()
    excluded_count = 0
    
    for domain in combined_domains:
        domain_tld = extract_tld(domain)
        
        if domain_tld in exclude_tlds:
            excluded_count += 1
        else:
            final_list_set.add(domain)

    final_count = len(final_list_set)
    
    # 5. Track History
    change_in_size = track_history(final_count)
    
    # 6. Write Final List
    sorted_list = sorted(list(final_list_set))
    
    with open(OUTPUT_FILENAME, "w") as f:
        f.write("# Combined, Filtered, and Deduplicated Wildcard Blocklist\n")
        f.write(f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# ------------------------------------------------------------------\n")
        f.write(f"# INITIAL SOURCES COUNT:\n")
        for name, domain_set in source_sets.items():
             f.write(f"#   - {name}: {len(domain_set):,}\n")
        f.write(f"# ------------------------------------------------------------------\n")
        f.write(f"# AGGREGATION METRICS:\n")
        f.write(f"#   - Total unique domains before filtering: {initial_count:,}\n")
        f.write(f"#   - Domains excluded by Spam TLD filter: {excluded_count:,}\n")
        f.write(f"#   - Domains unique to ONLY one source list: {len(unique_domains_only):,}\n")
        f.write(f"#   - FINAL COUNT: {final_count:,}\n")
        f.write(f"#   - Size change since last run: {change_in_size:+}\n\n")
        
        for entry in sorted_list:
            f.write(entry + "\n")

    print(f"\n✅ Successfully created {OUTPUT_FILENAME} with {final_count:,} entries.")
    print(f"📊 Metrics and history saved in {OUTPUT_DIR}/.")

if __name__ == "__main__":
    # Ensure requests is installed before running
    # pip install requests
    generate_blocklist()
