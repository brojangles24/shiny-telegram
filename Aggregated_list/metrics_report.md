# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)
*Generated: 2025-11-29 05:33:27*

## 📜 Aggregation Summary
| Metric | Count | Insight |
| :--- | :---: | :--- |
| **Total Scored Domains** | **531,517** | Size of the list including TLD rejected entries. |
| Change vs. Last Run | `+0` ➡️ | Trend in the total unique domain pool. |
| Priority List Size | 58,713 | Domains with **Min Confidence: 50% (Score >= 17)** (Max: 33). |
| High Consensus (Score 11+) | 133,278 | Domains backed by strong weighted evidence. |
| **Avg. Priority Score** | **20.71** | Average confidence score of the final list. |
| TLD Filter Exclusions | 0 | Domains rejected by the abusive TLD list. |

---

## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)
These are the highest-scoring domains that failed to make the final list:
| Domain | Weighted Score | Exclusion Reason |
| :--- | :---: | :--- |
| `razor.arnes.si` | <span style='color:orange;'>**16**</span> | Score Cutoff: **16 is below minimum confidence 17.** |
| `weblink.settrade.com` | <span style='color:orange;'>**16**</span> | Score Cutoff: **16 is below minimum confidence 17.** |
| `trafficg.com` | <span style='color:orange;'>**16**</span> | Score Cutoff: **16 is below minimum confidence 17.** |
| `fireads.org` | <span style='color:orange;'>**16**</span> | Score Cutoff: **16 is below minimum confidence 17.** |
| `ads.virtuopolitan.com` | <span style='color:orange;'>**16**</span> | Score Cutoff: **16 is below minimum confidence 17.** |

*The complete list of 472,804 excluded domains is in `excluded_domains_report.csv`.*

---

## 🔄 Priority List Change & Novelty Index
| Change Type | Domain Count | Novelty Breakdown |
| :--- | :---: | :--- |
| **Domains Added** | 27,479 | **27,479 Fresh** ✨ |
| **Domains Removed** | 0 | |
| **Domains Remained** | 31,234 | |

## 🌐 Source Performance & Health Check
| Source | Category | Weight | FP Risk | Coverage | Total Fetched | % In Priority | Volatility ($\pm \%$) | Color |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **HAGEZI_ULTIMATE** | Aggregated/Wildcard | 7 | **High 🟥** | **Broad 🟩** | 234,133 | **24.98%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#d62728;'>███</span> |
| **1HOSTS_LITE** | Aggregated/Wildcard | 6 | **Medium 🟨** | **Broad 🟩** | 92,444 | **48.14%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#2ca02c;'>███</span> |
| **OISD_BIG** | Aggregated/Wildcard | 5 | **High 🟥** | **Broad 🟩** | 216,323 | **23.11%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#1f77b4;'>███</span> |
| **ADGUARD_BASE** | ABP Rule List | 5 | **Medium 🟨** | **Medium 🟨** | 119,995 | **43.87%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#17becf;'>███</span> |
| **ANUDEEP_ADSERVERS** | Specialized (Ads) | 4 | **High 🟥** | **Specialized 🟦** | 42,347 | **3.60%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#9467bd;'>███</span> |
| **STEVENBLACK_HOSTS** | Hosts File (Legacy) | 3 | **High 🟥** | **Medium 🟨** | 88,075 | **6.14%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#ff7f0e;'>███</span> |
| **ADAWAY_HOSTS** | Specialized (Ads) | 3 | **Low 🟩** | **Specialized 🟦** | 6,540 | **22.17%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#8c564b;'>███</span> |

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
Analysis of all domains in the final `minimal_priority_list.txt` list.

**Top 15 TLDs in `minimal_priority_list.txt`:**
| Rank | TLD | Domain Count | % of Priority List |
| :---: | :--- | :---: | :---: |
| 1 | **.com** | 32,290 | 55.00% |
| 2 | **.net** | 3,452 | 5.88% |
| 3 | **.site** | 1,386 | 2.36% |
| 4 | **.online** | 1,341 | 2.28% |
| 5 | **.space** | 1,255 | 2.14% |
| 6 | **.website** | 1,067 | 1.82% |
| 7 | **.de** | 956 | 1.63% |
| 8 | **.store** | 956 | 1.63% |
| 9 | **.org** | 933 | 1.59% |
| 10 | **.pro** | 905 | 1.54% |
| 11 | **.xyz** | 678 | 1.15% |
| 12 | **.ru** | 646 | 1.10% |
| 13 | **.top** | 627 | 1.07% |
| 14 | **.shop** | 564 | 0.96% |
| 15 | **.io** | 554 | 0.94% |

**Domain Properties:**
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. Domain Entropy** | `2.849` | 'Randomness' score. (Higher = more 'random', e.g., DGA) |
| **Top 5 Trigrams** | `ing`, `ont`, `lou`, `clo`, `ron` | Common 3-letter strings in domain names. |

**Domain Depth (Subdomains):**
| Depth | Domain Count | % of Priority List | Example |
| :---: | :---: | :---: | :--- |
| 1 (e.g., d.d) | 40,222 | 68.51% | `google.com` |
| 2 (e.g., d.d.d) | 16,282 | 27.73% | `ads.google.com` |
| 3 (e.g., d.d.d.d) | 1,981 | 3.37% | `sub.ads.google.com` |
| 4 (e.g., d.d.d.d.d) | 201 | 0.34% | `sub.ads.google.com` |
| 5 (e.g., d.d.d.d.d.d) | 24 | 0.04% | `sub.ads.google.com` |
| 6 (e.g., d.d.d.d.d.d.d) | 3 | 0.01% | `sub.ads.google.com` |

### 2. New Domain Threat Analysis
Analysis of the **27,479** domains *added* to the list this run.
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. *New* Domain Entropy** | `2.704` | 'Randomness' of *new* threats. A spike here is bad. |
| **Top 5 *New* Trigrams** | `ing`, `ont`, `com`, `ron`, `ter` | Shows the 'shape' of new attack campaigns. |

---

## 📈 Interactive Visualization





See `historical_trends_chart.png`, `score_distribution_chart.png`, and `jaccard_heatmap.png`.
The old `historical_trend_chart.png` only shows total domains. The new **`historical_trends_chart.png`** is a full dashboard.