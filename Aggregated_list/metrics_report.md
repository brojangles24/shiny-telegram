# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)
*Generated: 2025-11-28 17:09:20*

## 📜 Aggregation Summary
| Metric | Count | Insight |
| :--- | :---: | :--- |
| **Total Scored Domains** | **531,019** | Size of the list including TLD rejected entries. |
| Change vs. Last Run | `+11` ⬆️ | Trend in the total unique domain pool. |
| Priority List Size | 300,000 | Capped domains selected (Cap: **300,000**). |
| High Consensus (Score 6+) | 131,447 | Domains backed by strong weighted evidence. |
| TLD Filter Exclusions | 66,499 | Domains rejected by the abusive TLD list. |

---

## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)
These are the highest-scoring domains that failed to make the final list:
| Domain | Weighted Score | Exclusion Reason |
| :--- | :---: | :--- |
| `zlp6s.pw` | <span style='color:red;'>**15**</span> | TLD Rejected: **.pw is marked as abusive.** |
| `ad.weplayer.cc` | <span style='color:red;'>**15**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `adop.cc` | <span style='color:red;'>**15**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `optimix.asia` | <span style='color:red;'>**15**</span> | TLD Rejected: **.asia is marked as abusive.** |
| `stats.ozwebsites.biz` | <span style='color:red;'>**15**</span> | TLD Rejected: **.biz is marked as abusive.** |
| `assurance-maladie-enligne.fr` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `141-24.dedicado.com.uy` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `altoprimbu.pro` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `lendvero.digital` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `soy.myddns.rocks` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |

*The complete list of 231,019 excluded domains is available in `excluded_domains_report.csv` for deeper analysis.*

---

## 🚫 Top 10 Abusive TLD Trends
Domains with these TLDs were excluded from the priority list.
| Rank | Abusive TLD | Excluded Domain Count |
| :---: | :--- | :---: |
| 1 | **.top** | 7,712 |
| 2 | **.shop** | 6,078 |
| 3 | **.online** | 4,608 |
| 4 | **.cfd** | 4,012 |
| 5 | **.click** | 3,857 |
| 6 | **.icu** | 3,773 |
| 7 | **.site** | 3,733 |
| 8 | **.space** | 3,004 |
| 9 | **.sbs** | 2,570 |
| 10 | **.store** | 2,481 |

---

## 🔄 Priority List Change & Novelty Index
| Change Type | Domain Count | Novelty Breakdown |
| :--- | :---: | :--- |
| **Domains Added** | 19,099 | **19,099 Fresh** ✨ |
| **Domains Removed** | 19,099 | |
| **Domains Remained** | 280,901 | |

## 🌐 Source Performance & Health Check
| Source | Category | Weight | Total Fetched | In Priority List | % List In Priority | Volatility ($\pm \%$) | Color |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **HAGEZI_ULTIMATE** | Aggregated/Wildcard | 4 | 233,408 | 186,776 | **80.02%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#d62728;'>███</span> |
| **1HOSTS_LITE** | Aggregated/Wildcard | 3 | 92,444 | 78,851 | **85.30%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#2ca02c;'>███</span> |
| **ADGUARD_BASE** | ABP Rule List | 3 | 119,878 | 98,938 | **82.53%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#17becf;'>███</span> |
| **OISD_BIG** | Aggregated/Wildcard | 2 | 215,707 | 98,629 | **45.72%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#1f77b4;'>███</span> |
| **ANUDEEP_ADSERVERS** | Specialized (Ads) | 2 | 42,347 | 7,046 | **16.64%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#9467bd;'>███</span> |
| **ADAWAY_HOSTS** | Specialized (Ads) | 2 | 6,540 | 6,488 | **99.20%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#8c564b;'>███</span> |
| **STEVENBLACK_HOSTS** | Hosts File (Legacy) | 1 | 88,075 | 33,699 | **38.26%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#ff7f0e;'>███</span> |

---

## 🖇️ List Similarity Matrix (Jaccard Index)
Measures the overlap between lists (Intersection / Union). A high value (e.g., 0.85) means the lists are very redundant.




| Source |**1HOSTS...** | **ADAWAY...** | **ADGUAR...** | **ANUDEE...** | **HAGEZI...** | **OISD_B...** | **STEVEN...** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1HOSTS_LITE** | `1.00` | 0.02 | 0.24 | 0.03 | 0.25 | 0.14 | 0.04 |
| **ADAWAY_HOSTS** | 0.02 | `1.00` | 0.01 | 0.04 | 0.01 | 0.00 | 0.07 |
| **ADGUARD_BASE** | 0.24 | 0.01 | `1.00` | 0.01 | 0.23 | 0.16 | 0.02 |
| **ANUDEEP_ADSERVERS** | 0.03 | 0.04 | 0.01 | `1.00` | 0.01 | 0.01 | 0.03 |
| **HAGEZI_ULTIMATE** | 0.25 | 0.01 | 0.23 | 0.01 | `1.00` | 0.23 | 0.05 |
| **OISD_BIG** | 0.14 | 0.00 | 0.16 | 0.01 | 0.23 | `1.00` | 0.09 |
| **STEVENBLACK_HOSTS** | 0.04 | 0.07 | 0.02 | 0.03 | 0.05 | 0.09 | `1.00` |

---

## 🤝 Domain Overlap Breakdown
Distribution of domains across multiple sources (as a percentage of the Total Scored Domains).
| Overlap Level (Sources) | Domains (Count) | % of Total Scored List |
| :---: | :---: | :---: |
| **7** | 110 | **0.02%** |
| **6** | 693 | **0.13%** |
| **5** | 2,547 | **0.48%** |
| **4** | 30,670 | **5.78%** |
| **3** | 36,194 | **6.82%** |
| **2** | 88,669 | **16.70%** |
| **1** | 372,136 | **70.08%** |

---

## 📊 Priority List Composition (Top 15 TLDs)
The most common TLDs in the final `priority_300k.txt` list.




[Image of a vertical bar chart]


| Rank | TLD | Domain Count | % of Priority List |
| :---: | :--- | :---: | :---: |
| 1 | **.com** | 181,434 | 60.48% |
| 2 | **.net** | 23,201 | 7.73% |
| 3 | **.de** | 7,474 | 2.49% |
| 4 | **.org** | 6,461 | 2.15% |
| 5 | **.xyz** | 6,103 | 2.03% |
| 6 | **.ru** | 5,638 | 1.88% |
| 7 | **.pro** | 4,813 | 1.60% |
| 8 | **.fr** | 4,112 | 1.37% |
| 9 | **.cn** | 3,822 | 1.27% |
| 10 | **.br** | 3,644 | 1.21% |
| 11 | **.io** | 3,531 | 1.18% |
| 12 | **.info** | 3,236 | 1.08% |
| 13 | **.jp** | 3,020 | 1.01% |
| 14 | **.app** | 2,372 | 0.79% |
| 15 | **.pl** | 2,331 | 0.78% |

---

## 📈 Interactive Visualization




[Image of a time series line graph]


See `historical_trend_chart.png` and `score_distribution_chart.png`.