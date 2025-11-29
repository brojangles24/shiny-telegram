# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)
*Generated: 2025-11-29 16:26:44*

## 📜 Aggregation Summary
| Metric | Count | Insight |
| :--- | :---: | :--- |
| **Total Scored Domains** | **532,035** | Size of the list including TLD rejected entries. |
| Change vs. Last Run | `+0` ➡️ | Trend in the total unique domain pool. |
| Priority List Size | 300,000 | Domains with **Min Score: 1 (Filtered-Full) | Cap: 300,000** (Max: 33). |
| High Consensus (Score 11+) | 133,275 | Domains backed by strong weighted evidence. |
| **Avg. Priority Score** | **9.73** | Average confidence score of the final list. |
| TLD Filter Exclusions | 67,129 | Domains rejected by the abusive TLD list. |

---

## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)
These are the highest-scoring domains that failed to make the final list:
| Domain | Weighted Score | Exclusion Reason |
| :--- | :---: | :--- |
| `stats.ozwebsites.biz` | <span style='color:red;'>**30**</span> | TLD Rejected: **.biz is marked as abusive.** |
| `zlp6s.pw` | <span style='color:red;'>**30**</span> | TLD Rejected: **.pw is marked as abusive.** |
| `crosspromotion.weplayer.cc` | <span style='color:red;'>**29**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `adserve.work` | <span style='color:red;'>**29**</span> | TLD Rejected: **.work is marked as abusive.** |
| `optimix.asia` | <span style='color:red;'>**29**</span> | TLD Rejected: **.asia is marked as abusive.** |
| `houstontacolover.com` | <span style='color:orange;'>**5**</span> | Cap Cutoff: **300,000 list. list** |
| `soureriagg.com` | <span style='color:orange;'>**5**</span> | Cap Cutoff: **300,000 list. list** |
| `protaskera.digital` | <span style='color:orange;'>**5**</span> | Cap Cutoff: **300,000 list. list** |
| `formob-cf1e8.firebaseapp.com` | <span style='color:orange;'>**5**</span> | Cap Cutoff: **300,000 list. list** |
| `preparereport.net` | <span style='color:orange;'>**5**</span> | Cap Cutoff: **300,000 list. list** |

*The complete list of 232,035 excluded domains is in `excluded_domains_report.csv`.*

---

## 🚫 Top 10 Abusive TLD Trends
Domains with these TLDs were excluded from the priority list.
| Rank | Abusive TLD | Excluded Domain Count |
| :---: | :--- | :---: |
| 1 | **.top** | 7,884 |
| 2 | **.shop** | 6,080 |
| 3 | **.online** | 4,623 |
| 4 | **.cfd** | 4,303 |
| 5 | **.click** | 3,865 |
| 6 | **.icu** | 3,830 |
| 7 | **.site** | 3,755 |
| 8 | **.space** | 3,021 |
| 9 | **.sbs** | 2,598 |
| 10 | **.store** | 2,501 |

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
| **HAGEZI_ULTIMATE** | Aggregated/Wildcard | 7 | **High 🟥** | **Broad 🟩** | 234,120 | **79.84%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#d62728;'>███</span> |
| **1HOSTS_LITE** | Aggregated/Wildcard | 6 | **Medium 🟨** | **Broad 🟩** | 92,589 | **85.22%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#2ca02c;'>███</span> |
| **OISD_BIG** | Aggregated/Wildcard | 5 | **High 🟥** | **Broad 🟩** | 216,725 | **64.86%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#1f77b4;'>███</span> |
| **ADGUARD_BASE** | ABP Rule List | 5 | **Medium 🟨** | **Medium 🟨** | 120,103 | **47.75%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#17becf;'>███</span> |
| **ANUDEEP_ADSERVERS** | Specialized (Ads) | 4 | **High 🟥** | **Specialized 🟦** | 42,347 | **16.64%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#9467bd;'>███</span> |
| **STEVENBLACK_HOSTS** | Hosts File (Legacy) | 3 | **High 🟥** | **Medium 🟨** | 88,075 | **38.25%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#ff7f0e;'>███</span> |
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
| **5** | 2,550 | **0.48%** |
| **4** | 30,770 | **5.78%** |
| **3** | 36,280 | **6.82%** |
| **2** | 89,274 | **16.78%** |
| **1** | 372,359 | **69.99%** |

---

## 🔬 Domain Property Analysis (DPA)
A 'nerd-out' deep-dive into the *properties* of the domains being blocked.

### 1. Final Priority List Composition
Analysis of all domains in the final `filtered-full_priority_list.txt` list.

**Top 15 TLDs in `filtered-full_priority_list.txt`:**
| Rank | TLD | Domain Count | % of Priority List |
| :---: | :--- | :---: | :---: |
| 1 | **.com** | 182,896 | 60.97% |
| 2 | **.net** | 23,841 | 7.95% |
| 3 | **.pro** | 7,340 | 2.45% |
| 4 | **.org** | 6,858 | 2.29% |
| 5 | **.ru** | 6,737 | 2.25% |
| 6 | **.de** | 6,559 | 2.19% |
| 7 | **.xyz** | 5,517 | 1.84% |
| 8 | **.fr** | 5,061 | 1.69% |
| 9 | **.cn** | 3,949 | 1.32% |
| 10 | **.info** | 3,883 | 1.29% |
| 11 | **.io** | 3,740 | 1.25% |
| 12 | **.app** | 3,612 | 1.20% |
| 13 | **.pl** | 2,235 | 0.74% |
| 14 | **.dev** | 2,107 | 0.70% |
| 15 | **.uk** | 1,947 | 0.65% |

**Domain Properties:**
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. Domain Entropy** | `2.753` | 'Randomness' score. (Higher = more 'random', e.g., DGA) |
| **Top 5 Trigrams** | `ing`, `app`, `ion`, `ent`, `tra` | Common 3-letter strings in domain names. |

**Domain Depth (Subdomains):**
| Depth | Domain Count | % of Priority List | Example |
| :---: | :---: | :---: | :--- |
| 1 (e.g., d.d) | 180,984 | 60.33% | `google.com` |
| 2 (e.g., d.d.d) | 95,593 | 31.86% | `ads.google.com` |
| 3 (e.g., d.d.d.d) | 18,020 | 6.01% | `sub.ads.google.com` |
| 4 (e.g., d.d.d.d.d) | 4,025 | 1.34% | `sub.ads.google.com` |
| 5 (e.g., d.d.d.d.d.d) | 795 | 0.27% | `sub.ads.google.com` |
| 6 (e.g., d.d.d.d.d.d.d) | 275 | 0.09% | `sub.ads.google.com` |
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
| **Avg. *New* Domain Entropy** | `2.741` | 'Randomness' of *new* threats. A spike here is bad. |
| **Top 5 *New* Trigrams** | `app`, `ing`, `ion`, `ent`, `tra` | Shows the 'shape' of new attack campaigns. |

---

## 📈 Interactive Visualization





See `historical_trends_chart.png`, `score_distribution_chart.png`, and `jaccard_heatmap.png`.
The old `historical_trend_chart.png` only shows total domains. The new **`historical_trends_chart.png`** is a full dashboard.