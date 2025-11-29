"""
Loads all settings from config.toml and makes them available
as Python constants for other modules.
"""
import tomli
import re
from pathlib import Path
from typing import Dict, List

try:
    # Get the path to config.toml (which is in the parent directory of this file's parent)
    CONFIG_PATH = Path(__file__).parent.parent / "config.toml"
    
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"config.toml not found at {CONFIG_PATH}")

    with open(CONFIG_PATH, "rb") as f:
        _config = tomli.load(f)

    # --- [main] ---
    MAIN = _config.get("main", {})
    OUTPUT_FORMAT_DEFAULT = MAIN.get("output_format", "raw")

    # --- [policy] ---
    POLICY = _config.get("policy", {})
    AGGRESSIVENESS_DEFAULT = POLICY.get("aggressiveness", 5)
    USE_TLD_EXCLUSION_DEFAULT = POLICY.get("use_tld_exclusion", True)

    # --- [policy_score_map] ---
    # Convert string keys from TOML to int keys
    POLICY_SCORE_MAP: Dict[int, int] = {
        int(k): v for k, v in _config.get("policy_score_map", {}).items()
    }

    # --- [paths] ---
    PATHS = _config.get("paths", {})
    OUTPUT_DIR = Path(PATHS.get("output_dir", "Aggregated_list"))
    ARCHIVE_DIR_NAME = PATHS.get("archive_dir_name", "archive")
    ARCHIVE_DIR = OUTPUT_DIR / ARCHIVE_DIR_NAME
    
    PRIORITY_FILENAME = PATHS.get("priority_filename", "priority_list.txt")
    REGEX_TLD_FILENAME = PATHS.get("regex_tld_filename", "regex_hagezi_tlds.txt")
    UNFILTERED_FILENAME = PATHS.get("unfiltered_filename", "aggregated_full.txt")
    HISTORY_FILENAME = PATHS.get("history_filename", "history.csv")
    REPORT_FILENAME = PATHS.get("report_filename", "metrics_report.md")
    DASHBOARD_HTML = PATHS.get("dashboard_html", "dashboard_html_removed.html")
    VERBOSE_EXCLUSION_FILE = PATHS.get("verbose_exclusion_file", "excluded_domains_report.csv")
    METRICS_CACHE_FILE = OUTPUT_DIR / PATHS.get("metrics_cache_file", "metrics_cache.json")

    # --- [network] ---
    NETWORK = _config.get("network", {})
    MAX_WORKERS_DEFAULT = NETWORK.get("max_workers", 8)
    MAX_FETCH_RETRIES = NETWORK.get("max_fetch_retries", 3)

    # --- [robustness] ---
    ROBUSTNESS = _config.get("robustness", {})
    CACHE_CLEANUP_DAYS = ROBUSTNESS.get("cache_cleanup_days", 30)
    ARCHIVE_LIMIT_MB_DEFAULT = ROBUSTNESS.get("archive_limit_mb", 50)

    # --- [tlds] ---
    TLDS = _config.get("tlds", {})
    HAGEZI_ABUSED_TLDS_URL = TLDS.get("hagezi_abused_tlds_url", "")
    NO_HAGEZI_TLDS_DEFAULT = TLDS.get("no_hagezi_tlds", False)
    
    _custom_tld_file_raw = TLDS.get("custom_tld_file")  # This will get "" or None
    CUSTOM_TLD_FILE_DEFAULT = _custom_tld_file_raw if _custom_tld_file_raw else None # This converts "" to None
    
    CUSTOM_BLOCK_TLDS = TLDS.get("custom_block_tlds", [])

    # --- [scoring] ---
    SCORING = _config.get("scoring", {})
    CONSENSUS_THRESHOLD = SCORING.get("consensus_threshold", 6)
    # This is now mutable, will be modified by processor.py
    SOURCE_WEIGHTS: Dict[str, int] = _config.get("scoring", {}).get("weights", {})
    
    # MAX_SCORE will be calculated dynamically in processor.py after source list modification
    MAX_SCORE = 0

    # --- [sources] ---
    # This is now mutable, will be modified by processor.py
    BLOCKLIST_SOURCES: Dict[str, str] = _config.get("sources", {})

    # --- [metadata] ---
    METADATA = _config.get("metadata", {})
    SOURCE_CATEGORIES: Dict[str, str] = METADATA.get("categories", {})
    SOURCE_COLORS: Dict[str, str] = METADATA.get("colors", {})
    ASCII_SPARKLINE_CHARS: str = METADATA.get("sparkline_chars", " ▂▃▄▅▆▇█")

    # --- Pre-compiled Regex (from original script) ---
    DOMAIN_REGEX = re.compile(
        r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$"
    )
    IPV4_REGEX = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

except Exception as e:
    print(f"FATAL ERROR: Could not load config.toml: {e}")
    print("Please ensure config.toml exists in the root directory and is valid.")
    import sys
    sys.exit(1)
