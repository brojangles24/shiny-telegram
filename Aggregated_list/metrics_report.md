# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)
*Generated: 2025-11-29 05:01:49*

## 📜 Aggregation Summary
| Metric | Count | Insight |
| :--- | :---: | :--- |
| **Total Scored Domains** | **531,517** | Size of the list including TLD rejected entries. |
| Change vs. Last Run | `+15` ⬆️ | Trend in the total unique domain pool. |
| Priority List Size | 3,068 | Domains with **Min Confidence: 70% (Score >= 24)** (Max: 33). |
| High Consensus (Score 11+) | 133,278 | Domains backed by strong weighted evidence. |
| TLD Filter Exclusions | 58 | Domains rejected by the abusive TLD list. |

---

## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)
These are the highest-scoring domains that failed to make the final list:
| Domain | Weighted Score | Exclusion Reason |
| :--- | :---: | :--- |
| `stats.ozwebsites.biz` | <span style='color:red;'>**30**</span> | TLD Rejected: **.biz is marked as abusive.** |
| `zlp6s.pw` | <span style='color:red;'>**30**</span> | TLD Rejected: **.pw is marked as abusive.** |
| `adop.cc` | <span style='color:red;'>**29**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `optimix.asia` | <span style='color:red;'>**29**</span> | TLD Rejected: **.asia is marked as abusive.** |
| `ad.weplayer.cc` | <span style='color:red;'>**29**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `souseuncurst.shop` | <span style='color:orange;'>**23**</span> | Score Cutoff: **23 is below minimum confidence 24.** |
| `linkworth.com` | <span style='color:orange;'>**23**</span> | Score Cutoff: **23 is below minimum confidence 24.** |
| `szgoetmggljs.com` | <span style='color:orange;'>**23**</span> | Score Cutoff: **23 is below minimum confidence 24.** |
| `regal-high.com` | <span style='color:orange;'>**23**</span> | Score Cutoff: **23 is below minimum confidence 24.** |
| `largelydisplace.com` | <span style='color:orange;'>**23**</span> | Score Cutoff: **23 is below minimum confidence 24.** |

*The complete list of 528,449 excluded domains is in `excluded_domains_report.csv`.*

---

## 🚫 Top 10 Abusive TLD Trends
Domains with these TLDs were excluded from the priority list.
| Rank | Abusive TLD | Excluded Domain Count |
| :---: | :--- | :---: |
| 1 | **.pw** | 17 |
| 2 | **.asia** | 12 |
| 3 | **.cc** | 6 |
| 4 | **.biz** | 4 |
| 5 | **.top** | 3 |
| 6 | **.online** | 3 |
| 7 | **.work** | 1 |
| 8 | **.support** | 1 |
| 9 | **.delivery** | 1 |
| 10 | **.vip** | 1 |

---

## 🔄 Priority List Change & Novelty Index
| Change Type | Domain Count | Novelty Breakdown |
| :--- | :---: | :--- |
| **Domains Added** | 0 | **0 Fresh** ✨ |
| **Domains Removed** | 50,569 | |
| **Domains Remained** | 3,068 | |

## 🌐 Source Performance & Health Check
| Source | Category | Weight | FP Risk | Coverage | Total Fetched | % In Priority | Volatility ($\pm \%$) | Color |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **HAGEZI_ULTIMATE** | Aggregated/Wildcard | 7 | **High 🟥** | **Broad 🟩** | 234,133 | **1.31%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#d62728;'>███</span> |
| **1HOSTS_LITE** | Aggregated/Wildcard | 6 | **Medium 🟨** | **Broad 🟩** | 92,444 | **3.29%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#2ca02c;'>███</span> |
| **OISD_BIG** | Aggregated/Wildcard | 5 | **High 🟥** | **Broad 🟩** | 216,323 | **1.36%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#1f77b4;'>███</span> |
| **ADGUARD_BASE** | ABP Rule List | 5 | **Medium 🟨** | **Medium 🟨** | 119,995 | **2.37%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#17becf;'>███</span> |
| **ANUDEEP_ADSERVERS** | Specialized (Ads) | 4 | **High 🟥** | **Specialized 🟦** | 42,347 | **1.49%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#9467bd;'>███</span> |
| **STEVENBLACK_HOSTS** | Hosts File (Legacy) | 3 | **High 🟥** | **Medium 🟨** | 88,075 | **3.31%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#ff7f0e;'>███</span> |
| **ADAWAY_HOSTS** | Specialized (Ads) | 3 | **Low 🟩** | **Specialized 🟦** | 6,540 | **12.40%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#8c564b;'>███</span> |

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
| 1 | **.com** | 2,030 | 66.17% |
| 2 | **.vn** | 311 | 10.14% |
| 3 | **.net** | 225 | 7.33% |
| 4 | **.jp** | 66 | 2.15% |
| 5 | **.io** | 51 | 1.66% |
| 6 | **.me** | 39 | 1.27% |
| 7 | **.org** | 33 | 1.08% |
| 8 | **.ru** | 31 | 1.01% |
| 9 | **.cn** | 31 | 1.01% |
| 10 | **.de** | 28 | 0.91% |
| 11 | **.uk** | 17 | 0.55% |
| 12 | **.tv** | 16 | 0.52% |
| 13 | **.pl** | 12 | 0.39% |
| 14 | **.ca** | 9 | 0.29% |
| 15 | **.xyz** | 9 | 0.29% |

**Domain Properties:**
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. Domain Entropy** | `2.582` | 'Randomness' score. (Higher = more 'random', e.g., DGA) |
| **Top 5 Trigrams** | `ads`, `ing`, `sta`, `tra`, `edi` | Common 3-letter strings in domain names. |

**Domain Depth (Subdomains):**
| Depth | Domain Count | % of Priority List | Example |
| :---: | :---: | :---: | :--- |
| 1 (e.g., d.d) | 1,611 | 52.51% | `google.com` |
| 2 (e.g., d.d.d) | 1,224 | 39.90% | `ads.google.com` |
| 3 (e.g., d.d.d.d) | 213 | 6.94% | `sub.ads.google.com` |
| 4 (e.g., d.d.d.d.d) | 17 | 0.55% | `sub.ads.google.com` |
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