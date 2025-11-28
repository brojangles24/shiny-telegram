# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)
*Generated: 2025-11-28 04:22:45*

## 📜 Aggregation Summary
| Metric | Count | Insight |
| :--- | :---: | :--- |
| **Total Scored Domains** | **529,613** | Size of the list including TLD rejected entries. |
| Change vs. Last Run | `+0` ➡️ | Trend in the total unique domain pool. |
| Priority List Size | 300,000 | Capped domains selected (Cap: **300,000**). |
| High Consensus (Score 6+) | 131,811 | Domains backed by strong weighted evidence. |
| TLD Filter Exclusions | 109,973 | Domains rejected by the abusive TLD list. |

---

## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)
These are the highest-scoring domains that failed to make the final list:
| Domain | Weighted Score | Exclusion Reason |
| :--- | :---: | :--- |
| `applog.uc.cn` | <span style='color:red;'>**17**</span> | TLD Rejected: **.cn is marked as abusive.** |
| `gjapplog.uc.cn` | <span style='color:red;'>**17**</span> | TLD Rejected: **.cn is marked as abusive.** |
| `pubnative.info` | <span style='color:red;'>**17**</span> | TLD Rejected: **.info is marked as abusive.** |
| `track.uc.cn` | <span style='color:red;'>**17**</span> | TLD Rejected: **.cn is marked as abusive.** |
| `advmob.cn` | <span style='color:red;'>**15**</span> | TLD Rejected: **.cn is marked as abusive.** |
| `service-transfert-argent.fr` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `sso-ledgr-livelog-tool.pages.dev` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `paypal.com.security.amaaonaws.com` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `is292-express.firebaseapp.com` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `yahoo.affex.org` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |

*The complete list of 229,613 excluded domains is available in `excluded_domains_report.csv` for deeper analysis.*

---

## 🚫 Top 10 Abusive TLD Trends
Domains with these TLDs were excluded from the priority list.
| Rank | Abusive TLD | Excluded Domain Count |
| :---: | :--- | :---: |
| 1 | **.pro** | 11,303 |
| 2 | **.ru** | 9,218 |
| 3 | **.top** | 7,759 |
| 4 | **.xyz** | 7,515 |
| 5 | **.info** | 6,481 |
| 6 | **.shop** | 6,079 |
| 7 | **.cn** | 5,043 |
| 8 | **.online** | 4,592 |
| 9 | **.br** | 4,198 |
| 10 | **.cfd** | 3,988 |

---

## 🔄 Priority List Change & Novelty Index
| Change Type | Domain Count | Novelty Breakdown |
| :--- | :---: | :--- |
| **Domains Added** | 37,552 | **37,552 Fresh** ✨ |
| **Domains Removed** | 37,552 | |
| **Domains Remained** | 262,448 | |

## 🌐 Source Performance & Health Check
| Source | Category | Weight | Total Fetched | In Priority List | % List In Priority | Volatility ($\pm \%$) | Color |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **HAGEZI_ULTIMATE** | Aggregated/Wildcard | 4 | 233,465 | 170,267 | **72.93%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#d62728;'>███</span> |
| **1HOSTS_LITE** | Aggregated/Wildcard | 3 | 92,384 | 74,728 | **80.89%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#2ca02c;'>███</span> |
| **ADGUARD_BASE** | ABP Rule List | 3 | 119,718 | 90,456 | **75.56%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#17becf;'>███</span> |
| **OISD_BIG** | Aggregated/Wildcard | 2 | 214,672 | 116,599 | **54.31%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#1f77b4;'>███</span> |
| **ANUDEEP_ADSERVERS** | Specialized (Ads) | 2 | 42,347 | 6,972 | **16.46%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#9467bd;'>███</span> |
| **ADAWAY_HOSTS** | Specialized (Ads) | 2 | 6,540 | 6,355 | **97.17%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#8c564b;'>███</span> |
| **STEVENBLACK_HOSTS** | Hosts File (Legacy) | 1 | 88,075 | 31,709 | **36.00%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#ff7f0e;'>███</span> |

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
| **5** | 2,544 | **0.48%** |
| **4** | 30,538 | **5.77%** |
| **3** | 36,345 | **6.86%** |
| **2** | 88,983 | **16.80%** |
| **1** | 370,400 | **69.94%** |

---

## 📊 Priority List Composition (Top 15 TLDs)
The most common TLDs in the final `priority_300k.txt` list.




[Image of a vertical bar chart]


| Rank | TLD | Domain Count | % of Priority List |
| :---: | :--- | :---: | :---: |
| 1 | **.com** | 197,361 | 65.79% |
| 2 | **.net** | 25,689 | 8.56% |
| 3 | **.de** | 8,005 | 2.67% |
| 4 | **.org** | 7,205 | 2.40% |
| 5 | **.fr** | 5,679 | 1.89% |
| 6 | **.io** | 3,825 | 1.27% |
| 7 | **.app** | 3,382 | 1.13% |
| 8 | **.jp** | 3,055 | 1.02% |
| 9 | **.pl** | 2,486 | 0.83% |
| 10 | **.uk** | 2,398 | 0.80% |
| 11 | **.dev** | 1,992 | 0.66% |
| 12 | **.co** | 1,953 | 0.65% |
| 13 | **.it** | 1,518 | 0.51% |
| 14 | **.nl** | 1,482 | 0.49% |
| 15 | **.digital** | 1,301 | 0.43% |

---

## 📈 Interactive Visualization




[Image of a time series line graph]


See `historical_trend_chart.png` and `score_distribution_chart.png`.