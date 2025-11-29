"""
Handles saving and loading of historical time-series metrics.
This allows for tracking trends beyond just the total domain count.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from collections import Counter

# Import settings from our config module
from . import config
from .utils import ConsoleLogger

HISTORICAL_METRICS_FILE = config.OUTPUT_DIR / config.PATHS.get("historical_metrics_file", "historical_metrics.json")

def load_historical_metrics(logger: ConsoleLogger) -> List[Dict[str, Any]]:
    """Loads the list of historical metric snapshots."""
    if not HISTORICAL_METRICS_FILE.exists():
        logger.info("No historical_metrics.json found. Will create a new one.")
        return []
    try:
        with open(HISTORICAL_METRICS_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
        if isinstance(history, list):
            return history
        else:
            logger.warning("historical_metrics.json is corrupt. Starting fresh.")
            return []
    except json.JSONDecodeError:
        logger.error("Failed to decode historical_metrics.json. Starting fresh.")
        return []
    except Exception as e:
        logger.error(f"Failed to load historical_metrics.json: {e}. Starting fresh.")
        return []

def save_historical_metrics(history: List[Dict[str, Any]], logger: ConsoleLogger):
    """Saves the updated list of historical metric snapshots."""
    try:
        with open(HISTORICAL_METRICS_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2)
        logger.info("💾 Saved historical metrics snapshot.")
    except Exception as e:
        logger.error(f"Failed to save historical_metrics.json: {e}")

def create_and_save_snapshot(
    logger: ConsoleLogger,
    priority_count: int,
    priority_list_avg_score: float, # <-- NEW
    priority_set_metrics: Dict[str, Any],
    new_domain_metrics: Dict[str, Any],
    jaccard_matrix: Dict[str, Dict[str, float]],
    change_report: Dict[str, List[Dict[str, Any]]],
    tld_exclusion_counter: Counter
):
    """
    Creates a new snapshot of key metrics and appends it to the history file.
    """
    logger.info("📈 Creating historical metrics snapshot...")
    
    top_tld = None
    if tld_exclusion_counter:
        top_tld = tld_exclusion_counter.most_common(1)[0][0]

    jac_hagezi_oisd = jaccard_matrix.get("HAGEZI_ULTIMATE", {}).get("OISD_BIG", 0.0)
    jac_hagezi_1hosts_key = "1HOSTS_LITE" if "1HOSTS_LITE" in jaccard_matrix else "1HOSTS_XTRA"
    jac_hagezi_1hosts = jaccard_matrix.get("HAGEZI_ULTIMATE", {}).get(jac_hagezi_1hosts_key, 0.0)

    snapshot = {
        "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "priority_list_size": priority_count,
        "priority_list_avg_score": priority_list_avg_score, # <-- NEW
        "avg_entropy": priority_set_metrics.get('avg_entropy', 0.0),
        "avg_new_domain_entropy": new_domain_metrics.get('avg_entropy', 0.0),
        "domains_added": len(change_report.get('added', [])),
        "domains_removed": len(change_report.get('removed', [])),
        "top_excluded_tld": top_tld,
        "jaccard_hagezi_oisd": jac_hagezi_oisd,
        "jaccard_hagezi_1hosts": jac_hagezi_1hosts
    }
    
    history = load_historical_metrics(logger)
    history.append(snapshot)
    save_historical_metrics(history, logger)
    
    if len(history) > 1000:
        logger.info("Pruning old historical metrics...")
        save_historical_metrics(history[-1000:], logger)
