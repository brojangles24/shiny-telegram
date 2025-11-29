"""
Handles all network fetching operations.
- fetch_list: Async function to fetch a single blocklist.
- fetch_all_lists_async: Manages concurrent fetching of all sources.
"""
import asyncio
import aiohttp
from typing import List, Dict, Set, Tuple
from collections import defaultdict

# Import settings from our config module
from . import config
from .utils import ConsoleLogger # Import logger for type hinting
from .processor import process_domain # Import domain processor

async def fetch_list(
    session: aiohttp.ClientSession, url: str, name: str, logger: ConsoleLogger
) -> List[str]:
    """Fetches list using aiohttp and retries, without file caching."""
    headers = {'User-Agent': 'SingularityDNSBlocklistAggregator/5.8.4'}
    
    for attempt in range(config.MAX_FETCH_RETRIES):
        try:
            async with session.get(url, timeout=30 + attempt * 10, headers=headers) as resp:
                resp.raise_for_status()
                content = await resp.text()
                content_lines = [l.strip().lower() for l in content.splitlines() if l.strip()]
                return content_lines
                
        except aiohttp.client_exceptions.ClientError as e:
            logger.error(f"Error fetching {name} (Attempt {attempt+1}/{config.MAX_FETCH_RETRIES}): {e.__class__.__name__}: {e}")
            if attempt < config.MAX_FETCH_RETRIES - 1:
                await asyncio.sleep(2 * (attempt + 1))
        except Exception as e:
            logger.error(f"Unexpected error for {name}: {e}")
            break

    logger.error(f"❌ All attempts failed for {name}. Returning empty list.")
    return []

async def fetch_and_process_sources_async(
    max_workers: int, logger: ConsoleLogger
) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    """Manages concurrent fetching and processing of all blocklists."""
    source_sets: Dict[str, Set[str]] = {}
    all_domains_from_sources: Dict[str, Set[str]] = defaultdict(set)
    
    conn = aiohttp.TCPConnector(limit=max_workers)
    
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = [
            fetch_list(session, url, name, logger) 
            for name, url in config.BLOCKLIST_SOURCES.items()
        ]
        results = await asyncio.gather(*tasks)

        for i, lines in enumerate(results):
            name = list(config.BLOCKLIST_SOURCES.keys())[i]
            # Process domains as they are fetched
            domains = {d for d in (process_domain(l) for l in lines) if d}
            source_sets[name] = domains
            all_domains_from_sources[name] = domains
            logger.info(f"🌐 Processed {len(domains):,} unique domains from **{name}**")
            
    return source_sets, all_domains_from_sources
