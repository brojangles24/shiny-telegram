# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)
*Generated: 2025-11-29 10:22:44*

## 📜 Aggregation Summary
| Metric | Count | Insight |
| :--- | :---: | :--- |
| **Total Scored Domains** | **532,255** | Size of the list including TLD rejected entries. |
| Change vs. Last Run | `+0` ➡️ | Trend in the total unique domain pool. |
| Priority List Size | 300,000 | Domains with **Min Score: 1 (Filtered-Full) | Cap: 300,000** (Max: 33). |
| High Consensus (Score 11+) | 133,634 | Domains backed by strong weighted evidence. |
| **Avg. Priority Score** | **9.74** | Average confidence score of the final list. |
| TLD Filter Exclusions | 67,233 | Domains rejected by the abusive TLD list. |

---

## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)
These are the highest-scoring domains that failed to make the final list:
| Domain | Weighted Score | Exclusion Reason |
| :--- | :---: | :--- |
| `zlp6s.pw` | <span style='color:red;'>**30**</span> | TLD Rejected: **.pw is marked as abusive.** |
| `stats.ozwebsites.biz` | <span style='color:red;'>**30**</span> | TLD Rejected: **.biz is marked as abusive.** |
| `adserve.work` | <span style='color:red;'>**29**</span> | TLD Rejected: **.work is marked as abusive.** |
| `optimix.asia` | <span style='color:red;'>**29**</span> | TLD Rejected: **.asia is marked as abusive.** |
| `adop.cc` | <span style='color:red;'>**29**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `dc-historic.gl.at.ply.gg` | <span style='color:orange;'>**5**</span> | Cap Cutoff: **300,000 list. list** |
| `aefohouaencouea.ws` | <span style='color:orange;'>**5**</span> | Cap Cutoff: **300,000 list. list** |
| `upaep-mx.weebly.com` | <span style='color:orange;'>**5**</span> | Cap Cutoff: **300,000 list. list** |
| `dubaiescortsgirl.com` | <span style='color:orange;'>**5**</span> | Cap Cutoff: **300,000 list. list** |
| `fralimbo.net` | <span style='color:orange;'>**5**</span> | Cap Cutoff: **300,000 list. list** |

*The complete list of 232,255 excluded domains is in `excluded_domains_report.csv`.*

---

## 🚫 Top 10 Abusive TLD Trends
Domains with these TLDs were excluded from the priority list.
| Rank | Abusive TLD | Excluded Domain Count |
| :---: | :--- | :---: |
| 1 | **.top** | 7,851 |
| 2 | **.shop** | 6,125 |
| 3 | **.online** | 4,647 |
| 4 | **.cfd** | 4,277 |
| 5 | **.click** | 3,875 |
| 6 | **.icu** | 3,827 |
| 7 | **.site** | 3,762 |
| 8 | **.space** | 3,011 |
| 9 | **.sbs** | 2,610 |
| 10 | **.store** | 2,497 |

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
| **HAGEZI_ULTIMATE** | Aggregated/Wildcard | 7 | **High 🟥** | **Broad 🟩** | 235,074 | **79.75%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#d62728;'>███</span> |
| **1HOSTS_LITE** | Aggregated/Wildcard | 6 | **Medium 🟨** | **Broad 🟩** | 92,589 | **85.22%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#2ca02c;'>███</span> |
| **OISD_BIG** | Aggregated/Wildcard | 5 | **High 🟥** | **Broad 🟩** | 216,387 | **64.79%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#1f77b4;'>███</span> |
| **ADGUARD_BASE** | ABP Rule List | 5 | **Medium 🟨** | **Medium 🟨** | 120,031 | **47.76%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#17becf;'>███</span> |
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
| **6** | 692 | **0.13%** |
| **5** | 2,549 | **0.48%** |
| **4** | 30,725 | **5.77%** |
| **3** | 36,345 | **6.83%** |
| **2** | 89,607 | **16.84%** |
| **1** | 372,227 | **69.93%** |

---

## 🔬 Domain Property Analysis (DPA)
A 'nerd-out' deep-dive into the *properties* of the domains being blocked.

### 1. Final Priority List Composition
Analysis of all domains in the final `filtered-full_priority_list.txt` list.

**Top 15 TLDs in `filtered-full_priority_list.txt`:**
| Rank | TLD | Domain Count | % of Priority List |
| :---: | :--- | :---: | :---: |
| 1 | **.com** | 182,891 | 60.96% |
| 2 | **.net** | 23,887 | 7.96% |
| 3 | **.pro** | 7,332 | 2.44% |
| 4 | **.org** | 6,858 | 2.29% |
| 5 | **.ru** | 6,591 | 2.20% |
| 6 | **.de** | 6,547 | 2.18% |
| 7 | **.xyz** | 5,627 | 1.88% |
| 8 | **.fr** | 5,013 | 1.67% |
| 9 | **.cn** | 3,990 | 1.33% |
| 10 | **.info** | 3,911 | 1.30% |
| 11 | **.io** | 3,725 | 1.24% |
| 12 | **.app** | 3,643 | 1.21% |
| 13 | **.pl** | 2,261 | 0.75% |
| 14 | **.dev** | 2,093 | 0.70% |
| 15 | **.uk** | 1,912 | 0.64% |

**Domain Properties:**
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. Domain Entropy** | `2.753` | 'Randomness' score. (Higher = more 'random', e.g., DGA) |
| **Top 5 Trigrams** | `ing`, `app`, `ion`, `ent`, `tra` | Common 3-letter strings in domain names. |

**Domain Depth (Subdomains):**
| Depth | Domain Count | % of Priority List | Example |
| :---: | :---: | :---: | :--- |
| 1 (e.g., d.d) | 181,143 | 60.38% | `google.com` |
| 2 (e.g., d.d.d) | 95,504 | 31.83% | `ads.google.com` |
| 3 (e.g., d.d.d.d) | 18,020 | 6.01% | `sub.ads.google.com` |
| 4 (e.g., d.d.d.d.d) | 3,954 | 1.32% | `sub.ads.google.com` |
| 5 (e.g., d.d.d.d.d.d) | 794 | 0.26% | `sub.ads.google.com` |
| 6 (e.g., d.d.d.d.d.d.d) | 277 | 0.09% | `sub.ads.google.com` |
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