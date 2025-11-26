# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)
*Generated: 2025-11-26 15:18:51*

## 📜 Aggregation Summary
| Metric | Count | Insight |
| :--- | :---: | :--- |
| **Total Scored Domains** | **534,850** | Size of the list including TLD rejected entries. |
| Change vs. Last Run | `-100` ⬇️ | Trend in the total unique domain pool. |
| Priority List Size | 300,000 | Capped domains selected (Cap: **300,000**). |
| High Consensus (Score 6+) | 131,927 | Domains backed by strong weighted evidence. |
| TLD Filter Exclusions | 66,265 | Domains rejected by the abusive TLD list. |

---

## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)
These are the highest-scoring domains that failed to make the final list:
| Domain | Weighted Score | Exclusion Reason |
| :--- | :---: | :--- |
| `stats.ozwebsites.biz` | <span style='color:red;'>**15**</span> | TLD Rejected: **.biz is marked as abusive.** |
| `ad.weplayer.cc` | <span style='color:red;'>**15**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `adserve.work` | <span style='color:red;'>**15**</span> | TLD Rejected: **.work is marked as abusive.** |
| `crosspromotion.weplayer.cc` | <span style='color:red;'>**15**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `zlp6s.pw` | <span style='color:red;'>**15**</span> | TLD Rejected: **.pw is marked as abusive.** |
| `token330zixer.net` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `okazjeskleps.com` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `ports68ma-verification13.start.page` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `pcwizz.com` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `good.jessami.com` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |

*The complete list of 234,850 excluded domains is available in `excluded_domains_report.csv` for deeper analysis.*

---

## 🚫 Top 10 Abusive TLD Trends
Domains with these TLDs were excluded from the priority list.
| Rank | Abusive TLD | Excluded Domain Count |
| :---: | :--- | :---: |
| 1 | **.top** | 7,845 |
| 2 | **.shop** | 6,103 |
| 3 | **.online** | 4,852 |
| 4 | **.cfd** | 3,936 |
| 5 | **.site** | 3,809 |
| 6 | **.icu** | 3,792 |
| 7 | **.click** | 3,745 |
| 8 | **.space** | 2,854 |
| 9 | **.sbs** | 2,555 |
| 10 | **.store** | 2,445 |

---

## 🔄 Priority List Change & Novelty Index
| Change Type | Domain Count | Novelty Breakdown |
| :--- | :---: | :--- |
| **Domains Added** | 16,950 | **16,950 Fresh** ✨ |
| **Domains Removed** | 16,950 | |
| **Domains Remained** | 283,050 | |

## 🌐 Source Performance & Health Check
| Source | Category | Weight | Total Fetched | In Priority List | % List In Priority | Volatility ($\pm \%$) | Color |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **HAGEZI_ULTIMATE** | Aggregated/Wildcard | 4 | 232,644 | 186,270 | **80.07%** | <span style='color:cyan;'>`New`</span> | <span style='color:#d62728;'>███</span> |
| **1HOSTS_LITE** | Aggregated/Wildcard | 3 | 92,543 | 79,126 | **85.50%** | <span style='color:cyan;'>`New`</span> | <span style='color:#2ca02c;'>███</span> |
| **ADGUARD_BASE** | ABP Rule List | 3 | 119,255 | 98,675 | **82.74%** | <span style='color:cyan;'>`New`</span> | <span style='color:#17becf;'>███</span> |
| **OISD_BIG** | Aggregated/Wildcard | 2 | 215,206 | 99,130 | **46.06%** | <span style='color:cyan;'>`New`</span> | <span style='color:#1f77b4;'>███</span> |
| **ANUDEEP_ADSERVERS** | Specialized (Ads) | 2 | 42,347 | 7,045 | **16.64%** | <span style='color:cyan;'>`New`</span> | <span style='color:#9467bd;'>███</span> |
| **ADAWAY_HOSTS** | Specialized (Ads) | 2 | 6,540 | 6,488 | **99.20%** | <span style='color:cyan;'>`New`</span> | <span style='color:#8c564b;'>███</span> |
| **STEVENBLACK_HOSTS** | Hosts File (Legacy) | 1 | 97,120 | 37,646 | **38.76%** | <span style='color:cyan;'>`New`</span> | <span style='color:#ff7f0e;'>███</span> |

---

## 🖇️ List Similarity Matrix (Jaccard Index)
Measures the overlap between lists (Intersection / Union). A high value (e.g., 0.85) means the lists are very redundant.


[Image of a data heatmap for correlation]

| Source |**1HOSTS...** | **ADAWAY...** | **ADGUAR...** | **ANUDEE...** | **HAGEZI...** | **OISD_B...** | **STEVEN...** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1HOSTS_LITE** | `1.00` | 0.02 | 0.24 | 0.03 | 0.25 | 0.14 | 0.04 |
| **ADAWAY_HOSTS** | 0.02 | `1.00` | 0.01 | 0.04 | 0.01 | 0.00 | 0.07 |
| **ADGUARD_BASE** | 0.24 | 0.01 | `1.00` | 0.01 | 0.23 | 0.16 | 0.02 |
| **ANUDEEP_ADSERVERS** | 0.03 | 0.04 | 0.01 | `1.00` | 0.01 | 0.01 | 0.03 |
| **HAGEZI_ULTIMATE** | 0.25 | 0.01 | 0.23 | 0.01 | `1.00` | 0.23 | 0.05 |
| **OISD_BIG** | 0.14 | 0.00 | 0.16 | 0.01 | 0.23 | `1.00` | 0.10 |
| **STEVENBLACK_HOSTS** | 0.04 | 0.07 | 0.02 | 0.03 | 0.05 | 0.10 | `1.00` |

---

## 🤝 Domain Overlap Breakdown
Distribution of domains across multiple sources (as a percentage of the Total Scored Domains).
| Overlap Level (Sources) | Domains (Count) | % of Total Scored List |
| :---: | :---: | :---: |
| **7** | 110 | **0.02%** |
| **6** | 694 | **0.13%** |
| **5** | 2,544 | **0.48%** |
| **4** | 30,522 | **5.71%** |
| **3** | 36,400 | **6.81%** |
| **2** | 92,133 | **17.23%** |
| **1** | 372,447 | **69.64%** |

---

## 📊 Priority List Composition (Top 15 TLDs)
The most common TLDs in the final `priority_300k.txt` list.


[Image of a vertical bar chart]

| Rank | TLD | Domain Count | % of Priority List |
| :---: | :--- | :---: | :---: |
| 1 | **.com** | 181,302 | 60.43% |
| 2 | **.net** | 24,090 | 8.03% |
| 3 | **.de** | 7,388 | 2.46% |
| 4 | **.org** | 6,518 | 2.17% |
| 5 | **.xyz** | 6,025 | 2.01% |
| 6 | **.ru** | 5,562 | 1.85% |
| 7 | **.pro** | 4,977 | 1.66% |
| 8 | **.fr** | 3,916 | 1.31% |
| 9 | **.cn** | 3,745 | 1.25% |
| 10 | **.br** | 3,620 | 1.21% |
| 11 | **.io** | 3,562 | 1.19% |
| 12 | **.info** | 3,020 | 1.01% |
| 13 | **.jp** | 3,015 | 1.00% |
| 14 | **.app** | 2,432 | 0.81% |
| 15 | **.pl** | 2,262 | 0.75% |

---

## 📈 Interactive Visualization


[Image of a time series line graph]

See `historical_trend_chart.png` and `score_distribution_chart.png`.