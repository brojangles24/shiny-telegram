# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)
*Generated: 2025-11-27 17:09:15*

## 📜 Aggregation Summary
| Metric | Count | Insight |
| :--- | :---: | :--- |
| **Total Scored Domains** | **535,102** | Size of the list including TLD rejected entries. |
| Change vs. Last Run | `+0` ➡️ | Trend in the total unique domain pool. |
| Priority List Size | 300,000 | Capped domains selected (Cap: **300,000**). |
| High Consensus (Score 6+) | 131,741 | Domains backed by strong weighted evidence. |
| TLD Filter Exclusions | 66,555 | Domains rejected by the abusive TLD list. |

---

## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)
These are the highest-scoring domains that failed to make the final list:
| Domain | Weighted Score | Exclusion Reason |
| :--- | :---: | :--- |
| `adop.cc` | <span style='color:red;'>**15**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `crosspromotion.weplayer.cc` | <span style='color:red;'>**15**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `zlp6s.pw` | <span style='color:red;'>**15**</span> | TLD Rejected: **.pw is marked as abusive.** |
| `ad.weplayer.cc` | <span style='color:red;'>**15**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `adserve.work` | <span style='color:red;'>**15**</span> | TLD Rejected: **.work is marked as abusive.** |
| `pylanthorequivmos.com` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `link.1905.com` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `jobasistent.ro` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `aurynithpartners.com` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `holzbrenaaa.xyz` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |

*The complete list of 235,102 excluded domains is available in `excluded_domains_report.csv` for deeper analysis.*

---

## 🚫 Top 10 Abusive TLD Trends
Domains with these TLDs were excluded from the priority list.
| Rank | Abusive TLD | Excluded Domain Count |
| :---: | :--- | :---: |
| 1 | **.top** | 7,713 |
| 2 | **.shop** | 6,126 |
| 3 | **.online** | 4,868 |
| 4 | **.cfd** | 4,031 |
| 5 | **.icu** | 3,836 |
| 6 | **.site** | 3,822 |
| 7 | **.click** | 3,814 |
| 8 | **.space** | 2,873 |
| 9 | **.sbs** | 2,568 |
| 10 | **.store** | 2,444 |

---

## 🔄 Priority List Change & Novelty Index
| Change Type | Domain Count | Novelty Breakdown |
| :--- | :---: | :--- |
| **Domains Added** | 16,916 | **16,916 Fresh** ✨ |
| **Domains Removed** | 16,916 | |
| **Domains Remained** | 283,084 | |

## 🌐 Source Performance & Health Check
| Source | Category | Weight | Total Fetched | In Priority List | % List In Priority | Volatility ($\pm \%$) | Color |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **HAGEZI_ULTIMATE** | Aggregated/Wildcard | 4 | 232,940 | 186,411 | **80.03%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#d62728;'>███</span> |
| **1HOSTS_LITE** | Aggregated/Wildcard | 3 | 92,384 | 78,914 | **85.42%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#2ca02c;'>███</span> |
| **ADGUARD_BASE** | ABP Rule List | 3 | 119,555 | 98,785 | **82.63%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#17becf;'>███</span> |
| **OISD_BIG** | Aggregated/Wildcard | 2 | 214,727 | 98,927 | **46.07%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#1f77b4;'>███</span> |
| **ANUDEEP_ADSERVERS** | Specialized (Ads) | 2 | 42,347 | 7,045 | **16.64%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#9467bd;'>███</span> |
| **ADAWAY_HOSTS** | Specialized (Ads) | 2 | 6,540 | 6,488 | **99.20%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#8c564b;'>███</span> |
| **STEVENBLACK_HOSTS** | Hosts File (Legacy) | 1 | 97,120 | 37,550 | **38.66%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#ff7f0e;'>███</span> |

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
| **OISD_BIG** | 0.14 | 0.00 | 0.17 | 0.01 | 0.23 | `1.00` | 0.10 |
| **STEVENBLACK_HOSTS** | 0.04 | 0.07 | 0.02 | 0.03 | 0.05 | 0.10 | `1.00` |

---

## 🤝 Domain Overlap Breakdown
Distribution of domains across multiple sources (as a percentage of the Total Scored Domains).
| Overlap Level (Sources) | Domains (Count) | % of Total Scored List |
| :---: | :---: | :---: |
| **7** | 110 | **0.02%** |
| **6** | 693 | **0.13%** |
| **5** | 2,545 | **0.48%** |
| **4** | 30,578 | **5.71%** |
| **3** | 36,015 | **6.73%** |
| **2** | 92,442 | **17.28%** |
| **1** | 372,719 | **69.65%** |

---

## 📊 Priority List Composition (Top 15 TLDs)
The most common TLDs in the final `priority_300k.txt` list.


[Image of a vertical bar chart]

| Rank | TLD | Domain Count | % of Priority List |
| :---: | :--- | :---: | :---: |
| 1 | **.com** | 181,367 | 60.46% |
| 2 | **.net** | 24,070 | 8.02% |
| 3 | **.de** | 7,393 | 2.46% |
| 4 | **.org** | 6,504 | 2.17% |
| 5 | **.xyz** | 6,177 | 2.06% |
| 6 | **.ru** | 5,521 | 1.84% |
| 7 | **.pro** | 4,882 | 1.63% |
| 8 | **.fr** | 3,922 | 1.31% |
| 9 | **.cn** | 3,716 | 1.24% |
| 10 | **.br** | 3,615 | 1.21% |
| 11 | **.io** | 3,548 | 1.18% |
| 12 | **.info** | 3,029 | 1.01% |
| 13 | **.jp** | 3,017 | 1.01% |
| 14 | **.app** | 2,418 | 0.81% |
| 15 | **.pl** | 2,313 | 0.77% |

---

## 📈 Interactive Visualization


[Image of a time series line graph]

See `historical_trend_chart.png` and `score_distribution_chart.png`.