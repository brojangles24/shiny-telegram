"""
Handles all user-facing reporting:
- generate_static_score_histogram: Creates the score distribution PNG.
- generate_history_plot: Creates the historical trend PNG.
- generate_markdown_report: Creates the main metrics_report.md.
"""
import logging
from datetime import datetime
from collections import Counter, defaultdict
from pathlib import Path
from typing import List, Dict, Set, Any, Union

# --- Dependency Check ---
try:
    import plotly.graph_objects as go
    import plotly.io as pio
except ImportError:
    logging.error("FATAL ERROR: Missing 'plotly' library.")
    logging.error("Please run: pip install plotly")
    raise
# --- End Dependency Check ---

# Import settings from our config module
from . import config
from .utils import ConsoleLogger, extract_tld, Counter # Import logger for type hinting

# --- Visualization ---

def generate_static_score_histogram(
    combined_counter: Counter, full_list: List[str], logger: ConsoleLogger
):
    """Generates a static PNG histogram showing the distribution of weighted scores."""
    image_path = config.OUTPUT_DIR / "score_distribution_chart.png"
    logger.info(f"📊 Generating static score distribution histogram at {image_path.name}")
    
    scores = [combined_counter[d] for d in full_list if combined_counter.get(d) is not None]
    
    # Use dynamic MAX_SCORE from config
    max_score = config.MAX_SCORE
    score_levels = sorted(list(set(scores)), reverse=True)

    fig = go.Figure(data=[go.Histogram(
        x=scores, xbins=dict(start=0, end=max_score + 1, size=1), marker_color="#1f77b4"
    )])

    fig.update_layout(
        title='Weighted Score Distribution (All Scored Domains)',
        xaxis=dict(
            title='Weighted Score', 
            tickvals=[s for s in score_levels if s % 2 == 0 or s == max_score], 
            range=[-0.5, max_score + 0.5]
        ),
        yaxis_title='Domain Count', bargap=0.05, template="plotly_dark"
    )
    
    try:
        pio.write_image(fig, str(image_path), scale=1.5, width=900, height=600)
    except Exception as e:
        logger.error(f"Failed to write histogram image: {e}")
        logger.error("Plotly static image export may require 'kaleido'. Try: pip install kaleido")

def generate_history_plot(history: List[Dict[str, str]], logger: ConsoleLogger):
    """Generates a static PNG of the total domain count over time."""
    if len(history) < 2:
        logger.info("Skipping history plot: not enough data points.")
        return

    try:
        dates = [datetime.strptime(row["Date"], "%Y-%m-%d") for row in history]
        totals = [int(row["Total_Unique_Domains"]) for row in history]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=totals, name='Total Scored Domains',
            mode='lines+markers', line=dict(color='#1f77b4', width=2)
        ))
        
        fig.update_layout(
            title='Historical Trend: Total Scored Domains',
            xaxis_title='Date', yaxis_title='Domain Count',
            template="plotly_dark", height=500, width=900
        )
        
        history_image_path = config.OUTPUT_DIR / "historical_trend_chart.png"
        pio.write_image(fig, str(history_image_path), scale=1.5)
        logger.info(f"📉 Generated historical trend plot: {history_image_path.name}")
        
    except Exception as e:
        logger.error(f"Failed to generate history plot: {e}")
        logger.error("Plotly static image export may require 'kaleido'. Try: pip install kaleido")

# --- Markdown Reporting ---

def generate_markdown_report(
    priority_count: int, change: int, total_unfiltered: int, excluded_count_tld: int, 
    full_list: List[str], combined_counter: Counter, overlap_counter: Counter, 
    source_metrics: Dict[str, Dict[str, Union[int, str]]],
    history: List[Dict[str, str]], logger: ConsoleLogger, domain_sources: Dict[str, Set[str]],
    change_report: Dict[str, List[Dict[str, Any]]], tld_exclusion_counter: Counter, 
    min_confidence_score: Union[int, str],  # <-- MODIFIED (can be int or str)
    excluded_domains_verbose: List[Dict[str, Any]],
    jaccard_matrix: Dict[str, Dict[str, float]],
    priority_set: Set[str],
    priority_set_metrics: Dict[str, Any],
    new_domain_metrics: Dict[str, Any]
):
    """
    Creates a detailed, aesthetic Markdown report with enhanced metrics.
    """
    report_path = config.OUTPUT_DIR / config.REPORT_FILENAME
    logger.info(f"📝 Generating Markdown report at {report_path.name}")
    report: List[str] = []
    
    report.append(f"# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)")
    report.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    trend_icon = "⬆️" if change > 0 else "⬇️" if change < 0 else "➡️"
    high_consensus_count = sum(1 for d in full_list if combined_counter.get(d) >= config.CONSENSUS_THRESHOLD)
    
    report.append(f"\n## 📜 Aggregation Summary")
    report.append("| Metric | Count | Insight |")
    report.append("| :--- | :---: | :--- |")
    report.append(f"| **Total Scored Domains** | **{len(full_list):,}** | Size of the list including TLD rejected entries. |") 
    report.append(f"| Change vs. Last Run | `{change:+}` {trend_icon} | Trend in the total unique domain pool. |")
    report.append(f"| Priority List Size | {priority_count:,} | Domains with Score >= **{min_confidence_score}** (Max: {config.MAX_SCORE}). |")
    report.append(f"| High Consensus (Score {config.CONSENSUS_THRESHOLD}+) | {high_consensus_count:,} | Domains backed by strong weighted evidence. |")
    report.append(f"| TLD Filter Exclusions | {excluded_count_tld:,} | Domains rejected by the abusive TLD list. |")
    report.append("\n---")
    
    if excluded_domains_verbose:
        report.append("\n## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)")
        tld_excluded = [d for d in excluded_domains_verbose if d['status'] == 'TLD EXCLUDED']
        score_excluded = [d for d in excluded_domains_verbose if d['status'] == 'SCORE CUTOFF']
        samples_to_show = []
        
        tld_excluded.sort(key=lambda x: x['score'], reverse=True)
        for d in tld_excluded[:5]:
            samples_to_show.append({
                'domain': d['domain'], 'score': d['score'],
                'reason': f"TLD Rejected: **{d['reason'].split('TLD ')[1]}**"
            })
            
        score_excluded.sort(key=lambda x: x['score'], reverse=True)
        for d in score_excluded[:5]:
                samples_to_show.append({
                'domain': d['domain'], 'score': d['score'],
                'reason': f"Score Cutoff: **{d['reason'].split('Score ')[1]}**"
            })
        
        samples_to_show.sort(key=lambda x: x['score'], reverse=True)

        if samples_to_show:
            report.append("These are the highest-scoring domains that failed to make the final list:")
            report.append("| Domain | Weighted Score | Exclusion Reason |")
            report.append("| :--- | :---: | :--- |")
            for item in samples_to_show[:10]:
                reason_color = "red" if "TLD Rejected" in item['reason'] else "orange"
                report.append(f"| `{item['domain']}` | <span style='color:{reason_color};'>**{item['score']}**</span> | {item['reason']} |")
        
        report.append(f"\n*The complete list of {len(excluded_domains_verbose):,} excluded domains is in `{config.VERBOSE_EXCLUSION_FILE}`.*")
        report.append("\n---")
    
    if tld_exclusion_counter:
        report.append("\n## 🚫 Top 10 Abusive TLD Trends")
        report.append("Domains with these TLDs were excluded from the priority list.")
        report.append("| Rank | Abusive TLD | Excluded Domain Count |")
        report.append("| :---: | :--- | :---: |")
        for rank, (tld, count) in enumerate(tld_exclusion_counter.most_common(10)):
            report.append(f"| {rank + 1} | **.{tld}** | {count:,} |")
        report.append("\n---")
    
    report.append("\n## 🔄 Priority List Change & Novelty Index")
    added_count = len(change_report.get('added', []))
    removed_count = len(change_report.get('removed', []))
    remained_count = len(change_report.get('remained', []))
    fresh_count = sum(1 for entry in change_report.get('added', []) if entry.get('novelty') == 'Fresh')
    
    if added_count > 0 or removed_count > 0 or remained_count > 0:
        report.append(f"| Change Type | Domain Count | Novelty Breakdown |")
        report.append("| :--- | :---: | :--- |")
        report.append(f"| **Domains Added** | {added_count:,} | **{fresh_count:,} Fresh** ✨ |")
        report.append(f"| **Domains Removed** | {removed_count:,} | |")
        report.append(f"| **Domains Remained** | {remained_count:,} | |")
    else:
        report.append("> *No previous archive file found. Change tracking will begin on the next run.*")
    
    report.append("\n## 🌐 Source Performance & Health Check")
    report.append(r"| Source | Category | Weight | Total Fetched | In Priority List | % List In Priority | Volatility ($\pm \%$) | Color |")
    report.append("| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |")
    
    # Use the (potentially modified) list of sources from config
    sorted_sources = sorted(config.BLOCKLIST_SOURCES.keys(), key=lambda n: config.SOURCE_WEIGHTS.get(n, 0), reverse=True)
    
    for name in sorted_sources:
        weight = config.SOURCE_WEIGHTS.get(name, 1)
        category = config.SOURCE_CATEGORIES.get(name, "Other")
        fetched_count = source_metrics.get(name, {}).get("Total_Fetched", 0)
        in_priority = source_metrics.get(name, {}).get("In_Priority_List", 0)
        volatility_raw = source_metrics.get(name, {}).get("Volatility", "N/A")
        
        percent_in_priority = f"{((in_priority / fetched_count) * 100):.2f}%" if fetched_count > 0 else "0.00%"
        
        color_style = ""
        volatility_display = str(volatility_raw)
        
        if volatility_display not in ("N/A", "New"):
            try:
                change_pct = float(volatility_display.replace('%', ''))
                if abs(change_pct) <= 5.0: color_style = "color:green;"
                elif change_pct >= 25.0: color_style = "color:orange;"
                elif change_pct <= -25.0: color_style = "color:red;"
            except ValueError: pass
        elif volatility_display == "New":
            color_style = "color:cyan;"

        source_color = config.SOURCE_COLORS.get(name, "black")
        
        report.append(
            f"| **{name}** | {category} | {weight} | {fetched_count:,} | {in_priority:,} | **{percent_in_priority}** | "
            f"<span style='{color_style}'>`{volatility_display}`</span> | <span style='color:{source_color};'>███</span> |"
        )
    report.append("\n---")
    
    report.append("\n## 🖇️ List Similarity Matrix (Jaccard Index)")
    report.append("Measures the overlap between lists (Intersection / Union). A high value (e.g., 0.85) means the lists are very redundant.")
    report.append("\n\n")
    
    matrix_sources = sorted(jaccard_matrix.keys())
    header = "| Source |" + " | ".join([f"**{name[:6]}...**" for name in matrix_sources]) + " |"
    divider = "| :--- |" + " :---: |" * len(matrix_sources)
    report.append(header)
    report.append(divider)
    
    for name_a in matrix_sources:
        row = f"| **{name_a}** |"
        for name_b in matrix_sources:
            value = jaccard_matrix.get(name_a, {}).get(name_b, 0.0)
            if value == 1.0: row += " `1.00` |"
            elif value > 0.75: row += f" <span style='color:red;'>**{value:.2f}**</span> |"
            elif value > 0.5: row += f" <span style='color:orange;'>{value:.2f}</span> |"
            else: row += f" {value:.2f} |"
        report.append(row)
    report.append("\n---")
    
    report.append("\n## 🤝 Domain Overlap Breakdown")
    report.append("Distribution of domains across multiple sources (as a percentage of the Total Scored Domains).")
    
    overlap_counts = Counter(overlap_counter[d] for d in full_list)
    total_scored_count = len(full_list)
    
    report.append("| Overlap Level (Sources) | Domains (Count) | % of Total Scored List |")
    report.append("| :---: | :---: | :---: |")
    
    for level in sorted(overlap_counts.keys(), reverse=True):
        count = overlap_counts[level]
        percent = f"{(count / total_scored_count * 100):.2f}%" if total_scored_count > 0 else "0.00%"
        report.append(f"| **{level}** | {count:,} | **{percent}** |")
    report.append("\n---")

    # --- Phase 1 DPA Section ---
    report.append("\n## 🔬 Domain Property Analysis (DPA)")
    report.append("A 'nerd-out' deep-dive into the *properties* of the domains being blocked.")

    # --- DPA Sub-Section 1: Priority List Composition ---
    report.append("\n### 1. Final Priority List Composition")
    report.append(f"Analysis of all domains in the final `{config.PRIORITY_FILENAME}` list.")
    
    # DPA: TLDs
    report.append("\n**Top 15 TLDs in Priority List:**")
    priority_tld_counter = Counter(extract_tld(d) for d in priority_set if extract_tld(d))
    report.append("| Rank | TLD | Domain Count | % of Priority List |")
    report.append("| :---: | :--- | :---: | :---: |")
    for rank, (tld, count) in enumerate(priority_tld_counter.most_common(15)):
        percent = (count / priority_count * 100) if priority_count > 0 else 0
        report.append(f"| {rank + 1} | **.{tld}** | {count:,} | {percent:.2f}% |")

    # DPA: Entropy & N-grams
    report.append("\n**Domain Properties:**")
    report.append("| Property | Value | Insight |")
    report.append("| :--- | :---: | :--- |")
    report.append(f"| **Avg. Domain Entropy** | `{priority_set_metrics['avg_entropy']:.3f}` | 'Randomness' score. (Higher = more 'random', e.g., DGA) |")
    
    top_trigrams_str = ", ".join([f"`{tg}`" for tg, count in priority_set_metrics['top_trigrams'][:5]])
    report.append(f"| **Top 5 Trigrams** | {top_trigrams_str} | Common 3-letter strings in domain names. |")

    # DPA: Domain Depth
    report.append("\n**Domain Depth (Subdomains):**")
    report.append("| Depth | Domain Count | % of Priority List | Example |")
    report.append("| :---: | :---: | :---: | :--- |")
    depth_counts = priority_set_metrics['depth_counts']
    for depth in sorted(depth_counts.keys()):
        count = depth_counts[depth]
        percent = (count / priority_count * 100) if priority_count > 0 else 0
        example = "`google.com`" if depth == 1 else "`ads.google.com`" if depth == 2 else "`sub.ads.google.com`"
        report.append(f"| {depth} (e.g., {'.'.join(['d']*(depth+1))}) | {count:,} | {percent:.2f}% | {example} |")

    # --- DPA Sub-Section 2: New Domain Analysis ---
    report.append("\n### 2. New Domain Threat Analysis")
    new_domain_count = sum(new_domain_metrics.get("depth_counts", {}).values())
    report.append(f"Analysis of the **{new_domain_count:,}** domains *added* to the list this run.")
    
    report.append("| Property | Value | Insight |")
    report.append("| :--- | :---: | :--- |")
    report.append(f"| **Avg. *New* Domain Entropy** | `{new_domain_metrics['avg_entropy']:.3f}` | 'Randomness' of *new* threats. A spike here is bad. |")
    
    new_trigrams_str = ", ".join([f"`{tg}`" for tg, count in new_domain_metrics['top_trigrams'][:5]])
    report.append(f"| **Top 5 *New* Trigrams** | {new_trigrams_str} | Shows the 'shape' of new attack campaigns. |")
    report.append("\n---")
    
    report.append("\n## 📈 Interactive Visualization")
    report.append("\n\n\n\n")
    report.append(f"See `historical_trend_chart.png` and `score_distribution_chart.png`.")
    
    # Write the report
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report))
    except Exception as e:
        logger.error(f"Failed to write Markdown report: {e}")
