# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)
*Generated: 2025-11-29 05:39:14*

## 📜 Aggregation Summary
| Metric | Count | Insight |
| :--- | :---: | :--- |
| **Total Scored Domains** | **531,517** | Size of the list including TLD rejected entries. |
| Change vs. Last Run | `+0` ➡️ | Trend in the total unique domain pool. |
| Priority List Size | 31,234 | Domains with **Min Confidence: 65% (Score >= 22)** (Max: 33). |
| High Consensus (Score 11+) | 133,278 | Domains backed by strong weighted evidence. |
| **Avg. Priority Score** | **23.38** | Average confidence score of the final list. |
| TLD Filter Exclusions | 0 | Domains rejected by the abusive TLD list. |

---

## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)
These are the highest-scoring domains that failed to make the final list:
| Domain | Weighted Score | Exclusion Reason |
| :--- | :---: | :--- |
| `hananokai.tv` | <span style='color:orange;'>**21**</span> | Score Cutoff: **21 is below minimum confidence 22.** |
| `mbs.megaroticlive.com` | <span style='color:orange;'>**21**</span> | Score Cutoff: **21 is below minimum confidence 22.** |
| `trackedweb.net` | <span style='color:orange;'>**21**</span> | Score Cutoff: **21 is below minimum confidence 22.** |
| `istartsurf.com` | <span style='color:orange;'>**21**</span> | Score Cutoff: **21 is below minimum confidence 22.** |
| `ads.golfweek.com` | <span style='color:orange;'>**21**</span> | Score Cutoff: **21 is below minimum confidence 22.** |

*The complete list of 500,283 excluded domains is in `excluded_domains_report.csv`.*

---

## 🔄 Priority List Change & Novelty Index
| Change Type | Domain Count | Novelty Breakdown |
| :--- | :---: | :--- |
| **Domains Added** | 0 | **0 Fresh** ✨ |
| **Domains Removed** | 1,858 | |
| **Domains Remained** | 31,234 | |

## 🌐 Source Performance & Health Check
| Source | Category | Weight | FP Risk | Coverage | Total Fetched | % In Priority | Volatility ($\pm \%$) | Color |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **HAGEZI_ULTIMATE** | Aggregated/Wildcard | 7 | **High 🟥** | **Broad 🟩** | 234,133 | **13.32%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#d62728;'>███</span> |
| **1HOSTS_LITE** | Aggregated/Wildcard | 6 | **Medium 🟨** | **Broad 🟩** | 92,444 | **33.71%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#2ca02c;'>███</span> |
| **OISD_BIG** | Aggregated/Wildcard | 5 | **High 🟥** | **Broad 🟩** | 216,323 | **14.34%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#1f77b4;'>███</span> |
| **ADGUARD_BASE** | ABP Rule List | 5 | **Medium 🟨** | **Medium 🟨** | 119,995 | **25.73%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#17becf;'>███</span> |
| **ANUDEEP_ADSERVERS** | Specialized (Ads) | 4 | **High 🟥** | **Specialized 🟦** | 42,347 | **1.92%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#9467bd;'>███</span> |
| **STEVENBLACK_HOSTS** | Hosts File (Legacy) | 3 | **High 🟥** | **Medium 🟨** | 88,075 | **3.52%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#ff7f0e;'>███</span> |
| **ADAWAY_HOSTS** | Specialized (Ads) | 3 | **Low 🟩** | **Specialized 🟦** | 6,540 | **14.48%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#8c564b;'>███</span> |

---

## 🖇️ List Similarity Matrix (Jaccard Index)
Measures the overlap between lists (Intersection / Union).
Dark blue = highly unique. Bright yellow = highly redundant.






---

## 🤝 Domain Overlap Breakdown
Distribution of domains across multiple sources (as a percentage of the Total Scored Domains).
| Overlap Level (Sources) | Domains (Count) | % of Total Scored List |
| :---: | :---: | :---: |
| **7** | 110 | **0.02%** |
| **6** | 693 | **0.13%** |
| **5** | 2,547 | **0.48%** |
| **4** | 30,680 | **5.77%** |
| **3** | 36,321 | **6.83%** |
| **2** | 89,345 | **16.81%** |
| **1** | 371,821 | **69.95%** |

---

## 🔬 Domain Property Analysis (DPA)
A 'nerd-out' deep-dive into the *properties* of the domains being blocked.

### 1. Final Priority List Composition
Analysis of all domains in the final `tiny_priority_list.txt` list.

**Top 15 TLDs in `tiny_priority_list.txt`:**
| Rank | TLD | Domain Count | % of Priority List |
| :---: | :--- | :---: | :---: |
| 1 | **.com** | 15,743 | 50.40% |
| 2 | **.net** | 1,965 | 6.29% |
| 3 | **.site** | 1,219 | 3.90% |
| 4 | **.space** | 1,182 | 3.78% |
| 5 | **.online** | 1,145 | 3.67% |
| 6 | **.website** | 1,029 | 3.29% |
| 7 | **.store** | 918 | 2.94% |
| 8 | **.pro** | 676 | 2.16% |
| 9 | **.org** | 518 | 1.66% |
| 10 | **.shop** | 436 | 1.40% |
| 11 | **.click** | 410 | 1.31% |
| 12 | **.de** | 335 | 1.07% |
| 13 | **.cyou** | 335 | 1.07% |
| 14 | **.cfd** | 333 | 1.07% |
| 15 | **.xyz** | 323 | 1.03% |

**Domain Properties:**
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. Domain Entropy** | `2.976` | 'Randomness' score. (Higher = more 'random', e.g., DGA) |
| **Top 5 Trigrams** | `ing`, `ont`, `lou`, `clo`, `ron` | Common 3-letter strings in domain names. |

**Domain Depth (Subdomains):**
| Depth | Domain Count | % of Priority List | Example |
| :---: | :---: | :---: | :--- |
| 1 (e.g., d.d) | 25,250 | 80.84% | `google.com` |
| 2 (e.g., d.d.d) | 5,271 | 16.88% | `ads.google.com` |
| 3 (e.g., d.d.d.d) | 638 | 2.04% | `sub.ads.google.com` |
| 4 (e.g., d.d.d.d.d) | 61 | 0.20% | `sub.ads.google.com` |
| 5 (e.g., d.d.d.d.d.d) | 13 | 0.04% | `sub.ads.google.com` |
| 6 (e.g., d.d.d.d.d.d.d) | 1 | 0.00% | `sub.ads.google.com` |

### 2. New Domain Threat Analysis
Analysis of the **0** domains *added* to the list this run.
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. *New* Domain Entropy** | `0.000` | 'Randomness' of *new* threats. A spike here is bad. |
| **Top 5 *New* Trigrams** |  | Shows the 'shape' of new attack campaigns. |

---

## 📈 Interactive Visualization





See `historical_trends_chart.png`, `score_distribution_chart.png`, and `jaccard_heatmap.png`.
The old `historical_trend_chart.png` only shows total domains. The new **`historical_trends_chart.png`** is a full dashboard.