# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)
*Generated: 2025-11-29 06:32:45*

## 📜 Aggregation Summary
| Metric | Count | Insight |
| :--- | :---: | :--- |
| **Total Scored Domains** | **531,558** | Size of the list including TLD rejected entries. |
| Change vs. Last Run | `+41` ⬆️ | Trend in the total unique domain pool. |
| Priority List Size | 300,000 | Domains with **Min Score: 1 (Filtered-Full) | Cap: 300,000** (Max: 33). |
| High Consensus (Score 11+) | 133,279 | Domains backed by strong weighted evidence. |
| **Avg. Priority Score** | **9.74** | Average confidence score of the final list. |
| TLD Filter Exclusions | 66,710 | Domains rejected by the abusive TLD list. |

---

## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)
These are the highest-scoring domains that failed to make the final list:
| Domain | Weighted Score | Exclusion Reason |
| :--- | :---: | :--- |
| `stats.ozwebsites.biz` | <span style='color:red;'>**30**</span> | TLD Rejected: **.biz is marked as abusive.** |
| `zlp6s.pw` | <span style='color:red;'>**30**</span> | TLD Rejected: **.pw is marked as abusive.** |
| `crosspromotion.weplayer.cc` | <span style='color:red;'>**29**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `adop.cc` | <span style='color:red;'>**29**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `ad.weplayer.cc` | <span style='color:red;'>**29**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `renouvellement-abo.fr` | <span style='color:orange;'>**5**</span> | Cap Cutoff: **300,000 list. list** |
| `mean-disease.gl.at.ply.gg` | <span style='color:orange;'>**5**</span> | Cap Cutoff: **300,000 list. list** |
| `aquamarinesalamander.pro` | <span style='color:orange;'>**5**</span> | Cap Cutoff: **300,000 list. list** |
| `accu-trader-edge.com` | <span style='color:orange;'>**5**</span> | Cap Cutoff: **300,000 list. list** |
| `gorillahikeafrica.com` | <span style='color:orange;'>**5**</span> | Cap Cutoff: **300,000 list. list** |

*The complete list of 231,558 excluded domains is in `excluded_domains_report.csv`.*

---

## 🚫 Top 10 Abusive TLD Trends
Domains with these TLDs were excluded from the priority list.
| Rank | Abusive TLD | Excluded Domain Count |
| :---: | :--- | :---: |
| 1 | **.top** | 7,727 |
| 2 | **.shop** | 6,089 |
| 3 | **.online** | 4,611 |
| 4 | **.cfd** | 4,073 |
| 5 | **.click** | 3,867 |
| 6 | **.icu** | 3,800 |
| 7 | **.site** | 3,732 |
| 8 | **.space** | 3,004 |
| 9 | **.sbs** | 2,607 |
| 10 | **.store** | 2,484 |

---

## 🔄 Priority List Change & Novelty Index
| Change Type | Domain Count | Novelty Breakdown |
| :--- | :---: | :--- |
| **Domains Added** | 277,886 | **277,886 Fresh** ✨ |
| **Domains Removed** | 9,120 | |
| **Domains Remained** | 22,114 | |

## 🌐 Source Performance & Health Check
| Source | Category | Weight | FP Risk | Coverage | Total Fetched | % In Priority | Volatility ($\pm \%$) | Color |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **HAGEZI_ULTIMATE** | Aggregated/Wildcard | 7 | **High 🟥** | **Broad 🟩** | 234,133 | **79.96%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#d62728;'>███</span> |
| **1HOSTS_LITE** | Aggregated/Wildcard | 6 | **Medium 🟨** | **Broad 🟩** | 92,444 | **85.30%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#2ca02c;'>███</span> |
| **OISD_BIG** | Aggregated/Wildcard | 5 | **High 🟥** | **Broad 🟩** | 216,360 | **64.88%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#1f77b4;'>███</span> |
| **ADGUARD_BASE** | ABP Rule List | 5 | **Medium 🟨** | **Medium 🟨** | 119,995 | **47.75%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#17becf;'>███</span> |
| **ANUDEEP_ADSERVERS** | Specialized (Ads) | 4 | **High 🟥** | **Specialized 🟦** | 42,347 | **16.64%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#9467bd;'>███</span> |
| **STEVENBLACK_HOSTS** | Hosts File (Legacy) | 3 | **High 🟥** | **Medium 🟨** | 88,075 | **38.26%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#ff7f0e;'>███</span> |
| **ADAWAY_HOSTS** | Specialized (Ads) | 3 | **Low 🟩** | **Specialized 🟦** | 6,540 | **99.20%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#8c564b;'>███</span> |

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
| **2** | 89,341 | **16.81%** |
| **1** | 371,866 | **69.96%** |

---

## 🔬 Domain Property Analysis (DPA)
A 'nerd-out' deep-dive into the *properties* of the domains being blocked.

### 1. Final Priority List Composition
Analysis of all domains in the final `filtered-full_priority_list.txt` list.

**Top 15 TLDs in `filtered-full_priority_list.txt`:**
| Rank | TLD | Domain Count | % of Priority List |
| :---: | :--- | :---: | :---: |
| 1 | **.com** | 182,905 | 60.97% |
| 2 | **.net** | 23,866 | 7.96% |
| 3 | **.pro** | 7,329 | 2.44% |
| 4 | **.org** | 6,857 | 2.29% |
| 5 | **.ru** | 6,579 | 2.19% |
| 6 | **.de** | 6,557 | 2.19% |
| 7 | **.xyz** | 5,582 | 1.86% |
| 8 | **.fr** | 5,137 | 1.71% |
| 9 | **.cn** | 3,977 | 1.33% |
| 10 | **.info** | 3,903 | 1.30% |
| 11 | **.io** | 3,741 | 1.25% |
| 12 | **.app** | 3,570 | 1.19% |
| 13 | **.pl** | 2,235 | 0.74% |
| 14 | **.dev** | 2,105 | 0.70% |
| 15 | **.uk** | 1,898 | 0.63% |

**Domain Properties:**
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. Domain Entropy** | `2.753` | 'Randomness' score. (Higher = more 'random', e.g., DGA) |
| **Top 5 Trigrams** | `ing`, `app`, `ion`, `ent`, `tra` | Common 3-letter strings in domain names. |

**Domain Depth (Subdomains):**
| Depth | Domain Count | % of Priority List | Example |
| :---: | :---: | :---: | :--- |
| 1 (e.g., d.d) | 181,182 | 60.39% | `google.com` |
| 2 (e.g., d.d.d) | 95,399 | 31.80% | `ads.google.com` |
| 3 (e.g., d.d.d.d) | 18,065 | 6.02% | `sub.ads.google.com` |
| 4 (e.g., d.d.d.d.d) | 3,973 | 1.32% | `sub.ads.google.com` |
| 5 (e.g., d.d.d.d.d.d) | 791 | 0.26% | `sub.ads.google.com` |
| 6 (e.g., d.d.d.d.d.d.d) | 282 | 0.09% | `sub.ads.google.com` |
| 7 (e.g., d.d.d.d.d.d.d.d) | 39 | 0.01% | `sub.ads.google.com` |
| 8 (e.g., d.d.d.d.d.d.d.d.d) | 49 | 0.02% | `sub.ads.google.com` |
| 9 (e.g., d.d.d.d.d.d.d.d.d.d) | 134 | 0.04% | `sub.ads.google.com` |
| 10 (e.g., d.d.d.d.d.d.d.d.d.d.d) | 63 | 0.02% | `sub.ads.google.com` |
| 11 (e.g., d.d.d.d.d.d.d.d.d.d.d.d) | 14 | 0.00% | `sub.ads.google.com` |
| 12 (e.g., d.d.d.d.d.d.d.d.d.d.d.d.d) | 1 | 0.00% | `sub.ads.google.com` |
| 19 (e.g., d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d) | 7 | 0.00% | `sub.ads.google.com` |
| 21 (e.g., d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d) | 1 | 0.00% | `sub.ads.google.com` |

### 2. New Domain Threat Analysis
Analysis of the **277,886** domains *added* to the list this run.
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. *New* Domain Entropy** | `2.742` | 'Randomness' of *new* threats. A spike here is bad. |
| **Top 5 *New* Trigrams** | `ing`, `app`, `ion`, `tra`, `ent` | Shows the 'shape' of new attack campaigns. |

---

## 📈 Interactive Visualization





See `historical_trends_chart.png`, `score_distribution_chart.png`, and `jaccard_heatmap.png`.
The old `historical_trend_chart.png` only shows total domains. The new **`historical_trends_chart.png`** is a full dashboard.