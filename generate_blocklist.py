#!/usr/bin/env python3
"""
Improved Blocklist Aggregator
Features:
- concurrent fetches with retries
- argparse for runtime options (workers, max output, verbose, skip-history)
- stricter hosts/hosts-like parsing and wildcard handling
- robust history CSV handling
- UTF-8 safe outputs and markdown report
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import argparse
import sys
import os
import csv
from datetime import datetime
from collections import Counter, defaultdict
import re

# --- Default Configuration (can be overridden via CLI) ---
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

HOSTS_LINE_RE = re.compile(r'^(?:0\.0\.0\.0|127\.0\.0\.1|::1)\s+(.+)$')
DOMAIN_CLEAN_RE = re.compile(r'^[\*\.\w\-]+\.[\w\-]+$')  # simple sanity check (has at least one dot)

# --- Utilities ---
def make_session(total_retries=3, backoff_factor=0.3, status_forcelist=(429, 500, 502, 503, 504)):
    s = requests.Session()
    retries = Retry(total=total_retries, backoff_factor=backoff_factor,
                    status_forcelist=status_forcelist, allowed_methods=frozenset(['GET','HEAD']))
    adapter = HTTPAdapter(max_retries=retries)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    s.headers.update({"User-Agent": "Blocklist-Aggregator/1.0"})
    return s

def fetch_text(session, url, timeout=30):
    try:
        r = session.get(url, timeout=timeout)
        r.raise_for_status()
        return r.text.splitlines()
    except Exception as e:
        return []

def parse_domain_from_line(line):
    """Return cleaned domain or None."""
    if not line:
        return None
    line = line.strip()
    if not line:
        return None
    # drop inline comments
    if '#' in line:
        line = line.split('#',1)[0].strip()
    parts = line.split()
    # hosts format
    m = HOSTS_LINE_RE.match(line)
    if m:
        domain = m.group(1).strip()
    elif len(parts) == 1:
        domain = parts[0].strip()
    elif len(parts) > 1 and parts[0] in ('0.0.0.0', '127.0.0.1', '::1'):
        domain = parts[1].strip()
    else:
        return None

    # normalize
    domain = domain.lower().lstrip('*.').lstrip('.')
    if domain in ('localhost', '', '::1', '255.255.255.255'):
        return None
    # skip entries that are single-label (no dot)
    if '.' not in domain:
        return None
    # sanity: remove stray characters
    domain = re.sub(r'[^a-z0-9\.\-]', '', domain)
    if not DOMAIN_CLEAN_RE.match(domain):
        return None
    return domain

def extract_tld(domain):
    d = domain.lstrip('*.').lstrip('.').strip()
    if not d or '.' not in d:
        return None
    return d.rsplit('.',1)[-1]

def safe_read_history(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            return rows
    except Exception:
        return []

def safe_write_history(path, header, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

# --- Core functions ---
def fetch_all_sources(sources, session, workers=6, verbose=False):
    results = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(fetch_text, session, url): name for name,url in sources.items()}
        for fut in as_completed(futures):
            name = futures[fut]
            lines = fut.result()
            parsed = set()
            for line in lines:
                d = parse_domain_from_line(line)
                if d:
                    parsed.add(d)
            results[name] = parsed
            if verbose:
                print(f"Fetched {name}: {len(parsed):,}")
    return results

def fetch_exclude_tlds(excl_url, session, verbose=False):
    lines = fetch_text(session, excl_url)
    tlds = set()
    for line in lines:
        d = parse_domain_from_line(line)
        if d:
            t = extract_tld(d)
            if t:
                tlds.add(t)
    if verbose:
        print(f"Excluded TLDs: {len(tlds)}")
    return tlds

def write_blocklist_file(filename, domains, source_sets, metrics_header_lines=None, is_filtered=True):
    sorted_list = sorted(domains)
    os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# Blocklist Aggregation Report\n")
        f.write(f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# ------------------------------------------------------------------\n")
        if is_filtered:
            f.write(f"# TYPE: Filtered List (Spam TLDs REMOVED) - {os.path.basename(filename)}\n")
        else:
            f.write(f"# TYPE: Unfiltered List (Contains ALL unique domains) - {os.path.basename(filename)}\n")
        f.write("# ------------------------------------------------------------------\n")
        if metrics_header_lines:
            for ln in metrics_header_lines:
                f.write(f"# {ln}\n")
            f.write("# ------------------------------------------------------------------\n")
        for entry in sorted_list:
            f.write(entry + "\n")

def generate_markdown_report(path, metrics, top_excluded_tlds, unique_by_source, appearance_counter, final_list_set, source_count):
    lines = []
    lines.append(f"# Blocklist Aggregation Report")
    lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    lines.append("## Summary\n")
    lines.append(f"- Final Filtered Count: {metrics['Final_Count']:,}")
    lines.append(f"- Total Unfiltered Unique: {metrics['Total_Unfiltered']:,}")
    lines.append(f"- Excluded Count: {metrics['Excluded_Count']:,}")
    lines.append(f"- Unique to one source (unfiltered): {metrics['Unique_Count']:,}\n")
    lines.append("## Source Contributions\n")
    for k,v in metrics['Source_Counts'].items():
        lines.append(f"- {k}: {v:,}")
    lines.append("\n## Top Excluded TLDs\n")
    lines.append("| Rank | TLD | Count |")
    lines.append("| --- | --- | --- |")
    for i,(t,c) in enumerate(top_excluded_tlds):
        if i>=50: break
        lines.append(f"| {i+1} | .{t} | {c:,} |")

    lines.append("\n## Example Overlap (domains appearing in multiple lists)\n")
    # show handful from highest overlap down to 2
    for overlap in range(source_count, 1, -1):
        bucket = [d for d,cnt in appearance_counter.items() if cnt==overlap and d in final_list_set]
        if not bucket: continue
        lines.append(f"### Present in {overlap} lists ({len(bucket):,})")
        for d in sorted(bucket)[:50]:
            lines.append(f"- {d}")
        if len(bucket)>50:
            lines.append(f"- ... and {len(bucket)-50:,} more\n")

    lines.append("\n## Unique domains per source (examples)\n")
    for src, lst in unique_by_source.items():
        lines.append(f"### {src} ({len(lst):,})")
        for d in sorted(lst)[:50]:
            lines.append(f"- {d}")
        if len(lst)>50:
            lines.append(f"- ... and {len(lst)-50:,} more\n")

    with open(path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

# --- CLI entrypoint ---
def main(argv=None):
    p = argparse.ArgumentParser(description="Aggregate and filter domain blocklists.")
    p.add_argument("--workers", type=int, default=6)
    p.add_argument("--max-output", type=int, default=0, help="Cap final output to N domains (0 = no cap).")
    p.add_argument("--skip-history", action="store_true")
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--no-exclusion", action="store_true", help="Skip TLD exclusion fetch and filtering.")
    args = p.parse_args(argv)

    session = make_session()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # fetch exclusion list
    exclude_tlds = set()
    if not args.no_exclusion:
        exclude_tlds = fetch_exclude_tlds(EXCLUSION_URL, session, verbose=args.verbose)

    # fetch sources concurrently
    source_sets = fetch_all_sources(BLOCKLIST_SOURCES, session, workers=args.workers, verbose=args.verbose)

    # combine and count appearances
    combined = set()
    appearance = Counter()
    for name, s in source_sets.items():
        for d in s:
            combined.add(d)
            appearance[d] += 1

    initial_count = len(combined)

    # filter by exclude_tlds
    excluded_counter = Counter()
    final_filtered = set()
    for d in combined:
        t = extract_tld(d)
        if t and t in exclude_tlds:
            excluded_counter[t] += 1
        else:
            final_filtered.add(d)

    # optional cap
    if args.max_output and args.max_output > 0 and len(final_filtered) > args.max_output:
        # deterministic truncation: sort by frequency (higher first), then lexicographically
        ranked = sorted(final_filtered, key=lambda x: (-appearance[x], x))
        final_filtered = set(ranked[:args.max_output])
        if args.verbose:
            print(f"Applied cap: final list truncated to {len(final_filtered):,} entries")

    # metrics
    total_unique_unfiltered = sum(1 for d,c in appearance.items() if c==1)
    metrics = {
        'Final_Count': len(final_filtered),
        'Total_Unfiltered': initial_count,
        'Excluded_Count': sum(excluded_counter.values()),
        'Unique_Count': total_unique_unfiltered,
        'Source_Counts': {k: len(v) for k,v in source_sets.items()}
    }

    # history tracking (safe)
    change = 0
    header = ['Date', 'Final_Count', 'Change', 'Total_Unfiltered', 'Excluded_Count', 'Unique_Count'] + list(metrics['Source_Counts'].keys())
    if not args.skip_history:
        rows = safe_read_history(HISTORY_FILENAME)
        prev_count = 0
        if rows and len(rows) > 0:
            # assume header present; try to read last numeric Final_Count from last row
            try:
                prev_count = int(rows[-1][1])
            except Exception:
                prev_count = 0
        change = metrics['Final_Count'] - prev_count
        new_row = [datetime.now().strftime('%Y-%m-%d'), str(metrics['Final_Count']), str(change), str(metrics['Total_Unfiltered']),
                   str(metrics['Excluded_Count']), str(metrics['Unique_Count'])]
        for k in metrics['Source_Counts'].keys():
            new_row.append(str(metrics['Source_Counts'][k]))
        # rebuild history rows: keep previous rows that are data (not header)
        data_rows = [r for r in rows if r and r[0] != header[0]]
        data_rows.append(new_row)
        safe_write_history(HISTORY_FILENAME, header, data_rows)

    # prepare report and files
    top_excluded = excluded_counter.most_common(50)
    # build unique_by_source for final filtered set
    unique_by_source = {}
    for name, s in source_sets.items():
        unique_by_source[name] = [d for d in s if appearance[d] == 1 and d in final_filtered]

    # write files
    metrics_header_lines = [
        f"Final Filtered Count: {metrics['Final_Count']:,}",
        f"Total Unfiltered Unique: {metrics['Total_Unfiltered']:,}",
        f"Excluded Count: {metrics['Excluded_Count']:,}",
        f"Unique to one source (unfiltered): {metrics['Unique_Count']:,}",
        f"Size change since last run: {change:+}"
    ]
    write_blocklist_file(OUTPUT_FILENAME_UNFILTERED, combined, source_sets, metrics_header_lines=None, is_filtered=False)
    write_blocklist_file(OUTPUT_FILENAME_FILTERED, final_filtered, source_sets, metrics_header_lines=metrics_header_lines, is_filtered=True)
    generate_markdown_report(REPORT_FILENAME, metrics, top_excluded, unique_by_source, appearance, final_filtered, len(source_sets))

    if args.verbose:
        print(f"Final filtered: {metrics['Final_Count']:,}  excluded: {metrics['Excluded_Count']:,}  combined: {initial_count:,}")
        print(f"Report: {REPORT_FILENAME}  Files: {OUTPUT_FILENAME_FILTERED}, {OUTPUT_FILENAME_UNFILTERED}")
    else:
        print(f"✅ Done. Final: {metrics['Final_Count']:,}  Excluded: {metrics['Excluded_Count']:,}")

if __name__ == "__main__":
    main()
