"""
General utilities:
- ConsoleLogger: Sets up logging.
- Cache Functions: Load/save metrics cache.
- History Tracking: track_history for the CSV.
- Helpers: generate_sparkline, extract_tld.
"""
import sys
import csv
import logging
import json
import re
import math  # <-- ADDED
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple, Any
import idna

# Import settings from our config module
from . import config

# --- Logging Setup ---
class ConsoleLogger:
    """Sets up a simple console logger."""
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
    def warning(self, msg): self.logger.warning(msg)

# --- Lightweight Metrics Cache Functions ---
def load_metrics_cache() -> Dict[str, Any]:
    """Loads only the source metrics cache from disk."""
    if config.METRICS_CACHE_FILE.exists():
        try:
            with open(config.METRICS_CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {}

def save_metrics_cache(metrics_data: Dict[str, Any]):
    """Saves only the source metrics cache to disk."""
    try:
        config.METRICS_CACHE_FILE.parent.mkdir(exist_ok=True)
        with open(config.METRICS_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(metrics_data, f, indent=2)
    except Exception as e:
        logging.error(f"Failed to save metrics cache file: {e}")

# --- General Utility Functions ---
def generate_sparkline(values: List[int], logger: ConsoleLogger) -> str:
    """Generates an ASCII sparkline from a list of integer values."""
    if not values: return ""
    min_val, max_val = min(values), max(values)
    range_val = max_val - min_val
    num_chars = len(config.ASCII_SPARKLINE_CHARS) - 1
    
    if range_val == 0: return config.ASCII_SPARKLINE_CHARS[-1] * len(values)

    try:
        sparkline = ""
        for val in values:
            index = int((val - min_val) / range_val * num_chars)
            sparkline += config.ASCII_SPARKLINE_CHARS[index]
        return sparkline
    except Exception as e:
        logger.error(f"Sparkline generation failed: {e}")
        return "N/A"

def extract_tld(domain: str) -> Optional[str]:
    """Extracts the simple TLD."""
    parts = domain.split(".")
    return parts[-1] if len(parts) >= 2 else None

def track_history(
    count: int, logger: ConsoleLogger
) -> Tuple[int, List[Dict[str, str]]]:
    """Reads, updates, and writes the aggregation history, returning all history."""
    history_path = config.OUTPUT_DIR / config.HISTORY_FILENAME
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
    if config.IPV4_REGEX.match(domain_candidate): return None

    try:
        ascii_domain = idna.encode(domain_candidate).decode('ascii')
    except idna.IDNAError:
        return None

    if not config.DOMAIN_REGEX.match(ascii_domain): return None

    return ascii_domain

# --- NEW: Phase 1 DPA Functions ---

def calculate_entropy(domain: str) -> float:
    """Calculates the Shannon entropy of the main domain part."""
    # We only care about the entropy of the "SLD" (second-level domain)
    # e.g., in 'ads.google.com', we only analyze 'google'
    parts = domain.split('.')
    if len(parts) > 1:
        # Use the part before the TLD (e.g., 'google' from 'google.com')
        # or ('ads' from 'ads.co.uk')
        domain_part = parts[-2]
    else:
        # Failsafe for a domain like 'localhost'
        domain_part = domain

    if not domain_part:
        return 0.0
        
    p, l = Counter(domain_part), float(len(domain_part))
    return -sum(count/l * math.log2(count/l) for count in p.values())

def get_ngrams(domain: str, n: int) -> list:
    """Extracts n-grams from the main domain part."""
    parts = domain.split('.')
    if len(parts) > 1:
        domain_part = parts[-2]
    else:
        domain_part = domain
    
    return [domain_part[i:i+n] for i in range(len(domain_part)-n+1)]

def get_domain_depth(domain: str) -> int:
    """Calculates the subdomain depth. 'google.com' is 1. 'ads.google.com' is 2."""
    # We count the dots. 'google.com' (1 dot) is depth 1.
    return domain.count('.')
