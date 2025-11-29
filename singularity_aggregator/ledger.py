"""
Phase 3: Domain Ledger Management

This module handles the persistent "ledger" of every domain ever seen by
the aggregator. It tracks a domain's first-seen date, last-seen date,
seen count, last-known score, and current status (active, inactive, lapsed).

This provides the foundation for domain lifecycle analysis (Phase 3b).
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Set
from collections import Counter

# Import settings from our config module
from . import config
from .utils import ConsoleLogger

# Define the ledger file path from config
LEDGER_FILE_PATH = config.DOMAIN_LEDGER_FILE

# --- Type Hint for Ledger Entry ---
class LedgerEntry(dict):
    first_seen: str
    last_seen: str
    seen_count: int
    last_score: int
    status: str # 'active', 'inactive', 'lapsed'

def load_ledger(logger: ConsoleLogger) -> Dict[str, LedgerEntry]:
    """
    Loads the persistent domain ledger from disk.
    Returns an empty dict if it doesn't exist or is corrupt.
    """
    if not LEDGER_FILE_PATH.exists():
        logger.info("No domain_ledger.json found. Will create a new one.")
        return {}
    
    logger.info(f"Loading persistent domain ledger from {LEDGER_FILE_PATH.name}...")
    try:
        with open(LEDGER_FILE_PATH, 'r', encoding='utf-8') as f:
            # Use streaming load for potentially large file
            ledger_data = json.load(f)
        logger.info(f"Loaded {len(ledger_data):,} domains from ledger.")
        return ledger_data
    except json.JSONDecodeError:
        logger.error("Failed to decode domain_ledger.json. Starting fresh.")
        return {}
    except Exception as e:
        logger.error(f"Failed to load domain_ledger.json: {e}. Starting fresh.")
        return {}

def save_ledger(ledger_data: Dict[str, LedgerEntry], logger: ConsoleLogger):
    """
    Saves the persistent domain ledger to disk.
    """
    logger.info(f"Saving persistent domain ledger ({len(ledger_data):,} total entries)...")
    try:
        with open(LEDGER_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(ledger_data, f) # No indent for performance
        logger.info("✅ Domain ledger saved.")
    except Exception as e:
        logger.error(f"FATAL: Failed to save domain_ledger.json: {e}")

def update_ledger(
    combined_counter: Counter,
    priority_set: Set[str],
    logger: ConsoleLogger
):
    """
    The core function for Phase 3a.
    Loads the old ledger, cross-references it with the current run's data,
    and saves the updated version.
    """
    logger.info("🧠 Updating persistent domain ledger...")
    ledger = load_ledger(logger)
    today = datetime.now().strftime('%Y-%m-%d')
    
    domains_in_this_run = set(combined_counter.keys())
    domains_ever_seen = set(ledger.keys())
    
    new_domains = domains_in_this_run - domains_ever_seen
    seen_domains = domains_in_this_run & domains_ever_seen
    lapsed_domains = domains_ever_seen - domains_in_this_run
    
    new_domain_count = 0
    updated_domain_count = 0
    lapsed_domain_count = 0
    
    # 1. Process NEW domains
    for domain in new_domains:
        new_domain_count += 1
        ledger[domain] = {
            "first_seen": today,
            "last_seen": today,
            "seen_count": 1,
            "last_score": combined_counter[domain],
            "status": "active" if domain in priority_set else "inactive"
        }
        
    # 2. Process SEEN domains
    for domain in seen_domains:
        updated_domain_count += 1
        entry = ledger[domain]
        entry["last_seen"] = today
        entry["seen_count"] = entry.get("seen_count", 0) + 1
        entry["last_score"] = combined_counter[domain]
        entry["status"] = "active" if domain in priority_set else "inactive"
        
    # 3. Process LAPSED domains (were in ledger, but not in this run)
    for domain in lapsed_domains:
        lapsed_domain_count += 1
        ledger[domain]["status"] = "lapsed"

    # Save the updated ledger back to disk
    save_ledger(ledger, logger)
    
    logger.info(f"🧠 Ledger update complete: {new_domain_count:,} new, {updated_domain_count:,} updated, {lapsed_domain_count:,} lapsed.")
