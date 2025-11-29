# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)
*Generated: 2025-11-29 05:30:44*

## 📜 Aggregation Summary
| Metric | Count | Insight |
| :--- | :---: | :--- |
| **Total Scored Domains** | **531,517** | Size of the list including TLD rejected entries. |
| Change vs. Last Run | `+0` ➡️ | Trend in the total unique domain pool. |
| Priority List Size | 3,126 | Domains with **Min Confidence: 70% (Score >= 24)** (Max: 33). |
| High Consensus (Score 11+) | 133,278 | Domains backed by strong weighted evidence. |
| **Avg. Priority Score** | **26.82** | Average confidence score of the final list. |
| TLD Filter Exclusions | 0 | Domains rejected by the abusive TLD list. |

---

## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)
These are the highest-scoring domains that failed to make the final list:
| Domain | Weighted Score | Exclusion Reason |
| :--- | :---: | :--- |
| `chessbranch.com` | <span style='color:orange;'>**23**</span> | Score Cutoff: **23 is below minimum confidence 24.** |
| `unwittingmark.pro` | <span style='color:orange;'>**23**</span> | Score Cutoff: **23 is below minimum confidence 24.** |
| `arawakarmies.shop` | <span style='color:orange;'>**23**</span> | Score Cutoff: **23 is below minimum confidence 24.** |
| `ecomm.events` | <span style='color:orange;'>**23**</span> | Score Cutoff: **23 is below minimum confidence 24.** |
| `cosshencoital.com` | <span style='color:orange;'>**23**</span> | Score Cutoff: **23 is below minimum confidence 24.** |

*The complete list of 528,391 excluded domains is in `excluded_domains_report.csv`.*

---

## 🔄 Priority List Change & Novelty Index
| Change Type | Domain Count | Novelty Breakdown |
| :--- | :---: | :--- |
| **Domains Added** | 0 | **0 Fresh** ✨ |
| **Domains Removed** | 28,108 | |
| **Domains Remained** | 3,126 | |

## 🌐 Source Performance & Health Check
| Source | Category | Weight | FP Risk | Coverage | Total Fetched | % In Priority | Volatility ($\pm \%$) | Color |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **HAGEZI_ULTIMATE** | Aggregated/Wildcard | 7 | **High 🟥** | **Broad 🟩** | 234,133 | **1.33%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#d62728;'>███</span> |
| **1HOSTS_LITE** | Aggregated/Wildcard | 6 | **Medium 🟨** | **Broad 🟩** | 92,444 | **3.35%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#2ca02c;'>███</span> |
| **OISD_BIG** | Aggregated/Wildcard | 5 | **High 🟥** | **Broad 🟩** | 216,323 | **1.39%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#1f77b4;'>███</span> |
| **ADGUARD_BASE** | ABP Rule List | 5 | **Medium 🟨** | **Medium 🟨** | 119,995 | **2.42%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#17becf;'>███</span> |
| **ANUDEEP_ADSERVERS** | Specialized (Ads) | 4 | **High 🟥** | **Specialized 🟦** | 42,347 | **1.51%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#9467bd;'>███</span> |
| **STEVENBLACK_HOSTS** | Hosts File (Legacy) | 3 | **High 🟥** | **Medium 🟨** | 88,075 | **3.37%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#ff7f0e;'>███</span> |
| **ADAWAY_HOSTS** | Specialized (Ads) | 3 | **Low 🟩** | **Specialized 🟦** | 6,540 | **12.51%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#8c564b;'>███</span> |

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
| 1 | **.com** | 2,030 | 64.94% |
| 2 | **.vn** | 311 | 9.95% |
| 3 | **.net** | 225 | 7.20% |
| 4 | **.jp** | 66 | 2.11% |
| 5 | **.io** | 51 | 1.63% |
| 6 | **.me** | 39 | 1.25% |
| 7 | **.org** | 33 | 1.06% |
| 8 | **.cn** | 31 | 0.99% |
| 9 | **.ru** | 31 | 0.99% |
| 10 | **.de** | 28 | 0.90% |
| 11 | **.uk** | 17 | 0.54% |
| 12 | **.pw** | 17 | 0.54% |
| 13 | **.tv** | 16 | 0.51% |
| 14 | **.asia** | 12 | 0.38% |
| 15 | **.pl** | 12 | 0.38% |

**Domain Properties:**
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. Domain Entropy** | `2.580` | 'Randomness' score. (Higher = more 'random', e.g., DGA) |
| **Top 5 Trigrams** | `ads`, `ing`, `sta`, `edi`, `tra` | Common 3-letter strings in domain names. |

**Domain Depth (Subdomains):**
| Depth | Domain Count | % of Priority List | Example |
| :---: | :---: | :---: | :--- |
| 1 (e.g., d.d) | 1,643 | 52.56% | `google.com` |
| 2 (e.g., d.d.d) | 1,250 | 39.99% | `ads.google.com` |
| 3 (e.g., d.d.d.d) | 213 | 6.81% | `sub.ads.google.com` |
| 4 (e.g., d.d.d.d.d) | 17 | 0.54% | `sub.ads.google.com` |
| 5 (e.g., d.d.d.d.d.d) | 3 | 0.10% | `sub.ads.google.com` |

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