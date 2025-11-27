# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)
*Generated: 2025-11-27 23:09:37*

## 📜 Aggregation Summary
| Metric | Count | Insight |
| :--- | :---: | :--- |
| **Total Scored Domains** | **529,292** | Size of the list including TLD rejected entries. |
| Change vs. Last Run | `+27` ⬆️ | Trend in the total unique domain pool. |
| Priority List Size | 300,000 | Capped domains selected (Cap: **300,000**). |
| High Consensus (Score 6+) | 131,705 | Domains backed by strong weighted evidence. |
| TLD Filter Exclusions | 66,103 | Domains rejected by the abusive TLD list. |

---

## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)
These are the highest-scoring domains that failed to make the final list:
| Domain | Weighted Score | Exclusion Reason |
| :--- | :---: | :--- |
| `crosspromotion.weplayer.cc` | <span style='color:red;'>**15**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `ad.weplayer.cc` | <span style='color:red;'>**15**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `zlp6s.pw` | <span style='color:red;'>**15**</span> | TLD Rejected: **.pw is marked as abusive.** |
| `optimix.asia` | <span style='color:red;'>**15**</span> | TLD Rejected: **.asia is marked as abusive.** |
| `stats.ozwebsites.biz` | <span style='color:red;'>**15**</span> | TLD Rejected: **.biz is marked as abusive.** |
| `ykglqsbgjbxsja.com` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `vircom.cz` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `northale.com` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `hydramidehda.info` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `2d6twx.close.futureisready.com` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |

*The complete list of 229,292 excluded domains is available in `excluded_domains_report.csv` for deeper analysis.*

---

## 🚫 Top 10 Abusive TLD Trends
Domains with these TLDs were excluded from the priority list.
| Rank | Abusive TLD | Excluded Domain Count |
| :---: | :--- | :---: |
| 1 | **.top** | 7,737 |
| 2 | **.shop** | 6,076 |
| 3 | **.online** | 4,590 |
| 4 | **.cfd** | 3,985 |
| 5 | **.click** | 3,831 |
| 6 | **.icu** | 3,730 |
| 7 | **.site** | 3,711 |
| 8 | **.space** | 2,972 |
| 9 | **.sbs** | 2,536 |
| 10 | **.store** | 2,480 |

---

## 🔄 Priority List Change & Novelty Index
| Change Type | Domain Count | Novelty Breakdown |
| :--- | :---: | :--- |
| **Domains Added** | 19,147 | **19,147 Fresh** ✨ |
| **Domains Removed** | 19,147 | |
| **Domains Remained** | 280,853 | |

## 🌐 Source Performance & Health Check
| Source | Category | Weight | Total Fetched | In Priority List | % List In Priority | Volatility ($\pm \%$) | Color |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **HAGEZI_ULTIMATE** | Aggregated/Wildcard | 4 | 232,940 | 186,411 | **80.03%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#d62728;'>███</span> |
| **1HOSTS_LITE** | Aggregated/Wildcard | 3 | 92,384 | 78,914 | **85.42%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#2ca02c;'>███</span> |
| **ADGUARD_BASE** | ABP Rule List | 3 | 119,661 | 98,837 | **82.60%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#17becf;'>███</span> |
| **OISD_BIG** | Aggregated/Wildcard | 2 | 215,020 | 98,950 | **46.02%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#1f77b4;'>███</span> |
| **ANUDEEP_ADSERVERS** | Specialized (Ads) | 2 | 42,347 | 7,045 | **16.64%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#9467bd;'>███</span> |
| **ADAWAY_HOSTS** | Specialized (Ads) | 2 | 6,540 | 6,488 | **99.20%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#8c564b;'>███</span> |
| **STEVENBLACK_HOSTS** | Hosts File (Legacy) | 1 | 88,075 | 33,812 | **38.39%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#ff7f0e;'>███</span> |

---

## 🖇️ List Similarity Matrix (Jaccard Index)
Measures the overlap between lists (Intersection / Union). A high value (e.g., 0.85) means the lists are very redundant.


[Image of a data heatmap for correlation]

| Source |**1HOSTS...** | **ADAWAY...** | **ADGUAR...** | **ANUDEE...** | **HAGEZI...** | **OISD_B...** | **STEVEN...** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1HOSTS_LITE** | `1.00` | 0.02 | 0.24 | 0.03 | 0.25 | 0.14 | 0.04 |
| **ADAWAY_HOSTS** | 0.02 | `1.00` | 0.01 | 0.04 | 0.01 | 0.00 | 0.07 |
| **ADGUARD_BASE** | 0.24 | 0.01 | `1.00` | 0.01 | 0.23 | 0.17 | 0.02 |
| **ANUDEEP_ADSERVERS** | 0.03 | 0.04 | 0.01 | `1.00` | 0.01 | 0.01 | 0.03 |
| **HAGEZI_ULTIMATE** | 0.25 | 0.01 | 0.23 | 0.01 | `1.00` | 0.23 | 0.05 |
| **OISD_BIG** | 0.14 | 0.00 | 0.17 | 0.01 | 0.23 | `1.00` | 0.09 |
| **STEVENBLACK_HOSTS** | 0.04 | 0.07 | 0.02 | 0.03 | 0.05 | 0.09 | `1.00` |

---

## 🤝 Domain Overlap Breakdown
Distribution of domains across multiple sources (as a percentage of the Total Scored Domains).
| Overlap Level (Sources) | Domains (Count) | % of Total Scored List |
| :---: | :---: | :---: |
| **7** | 110 | **0.02%** |
| **6** | 693 | **0.13%** |
| **5** | 2,545 | **0.48%** |
| **4** | 30,579 | **5.78%** |
| **3** | 36,295 | **6.86%** |
| **2** | 89,043 | **16.82%** |
| **1** | 370,027 | **69.91%** |

---

## 📊 Priority List Composition (Top 15 TLDs)
The most common TLDs in the final `priority_300k.txt` list.


[Image of a vertical bar chart]

| Rank | TLD | Domain Count | % of Priority List |
| :---: | :--- | :---: | :---: |
| 1 | **.com** | 181,356 | 60.45% |
| 2 | **.net** | 23,333 | 7.78% |
| 3 | **.de** | 7,460 | 2.49% |
| 4 | **.org** | 6,486 | 2.16% |
| 5 | **.xyz** | 6,194 | 2.06% |
| 6 | **.ru** | 5,537 | 1.85% |
| 7 | **.pro** | 4,864 | 1.62% |
| 8 | **.fr** | 4,057 | 1.35% |
| 9 | **.cn** | 3,780 | 1.26% |
| 10 | **.br** | 3,630 | 1.21% |
| 11 | **.io** | 3,556 | 1.19% |
| 12 | **.info** | 3,074 | 1.02% |
| 13 | **.jp** | 3,016 | 1.01% |
| 14 | **.app** | 2,444 | 0.81% |
| 15 | **.pl** | 2,322 | 0.77% |

---

## 📈 Interactive Visualization


[Image of a time series line graph]

See `historical_trend_chart.png` and `score_distribution_chart.png`.