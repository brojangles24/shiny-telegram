# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)
*Generated: 2025-11-26 22:10:06*

## 📜 Aggregation Summary
| Metric | Count | Insight |
| :--- | :---: | :--- |
| **Total Scored Domains** | **535,105** | Size of the list including TLD rejected entries. |
| Change vs. Last Run | `+78` ⬆️ | Trend in the total unique domain pool. |
| Priority List Size | 300,000 | Capped domains selected (Cap: **300,000**). |
| High Consensus (Score 6+) | 131,813 | Domains backed by strong weighted evidence. |
| TLD Filter Exclusions | 66,444 | Domains rejected by the abusive TLD list. |

---

## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)
These are the highest-scoring domains that failed to make the final list:
| Domain | Weighted Score | Exclusion Reason |
| :--- | :---: | :--- |
| `adserve.work` | <span style='color:red;'>**15**</span> | TLD Rejected: **.work is marked as abusive.** |
| `stats.ozwebsites.biz` | <span style='color:red;'>**15**</span> | TLD Rejected: **.biz is marked as abusive.** |
| `adop.cc` | <span style='color:red;'>**15**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `ad.weplayer.cc` | <span style='color:red;'>**15**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `crosspromotion.weplayer.cc` | <span style='color:red;'>**15**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `every.njyi99.cn` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `fswposlete.web.app` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `hairnbow.com` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `securedatas.info` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |
| `antirwharf.com` | <span style='color:orange;'>**2**</span> | Score Cutoff: **Did not make Top 300,000** |

*The complete list of 235,105 excluded domains is available in `excluded_domains_report.csv` for deeper analysis.*

---

## 🚫 Top 10 Abusive TLD Trends
Domains with these TLDs were excluded from the priority list.
| Rank | Abusive TLD | Excluded Domain Count |
| :---: | :--- | :---: |
| 1 | **.top** | 7,875 |
| 2 | **.shop** | 6,111 |
| 3 | **.online** | 4,875 |
| 4 | **.cfd** | 3,959 |
| 5 | **.site** | 3,816 |
| 6 | **.icu** | 3,806 |
| 7 | **.click** | 3,757 |
| 8 | **.space** | 2,858 |
| 9 | **.sbs** | 2,568 |
| 10 | **.store** | 2,445 |

---

## 🔄 Priority List Change & Novelty Index
| Change Type | Domain Count | Novelty Breakdown |
| :--- | :---: | :--- |
| **Domains Added** | 16,975 | **16,975 Fresh** ✨ |
| **Domains Removed** | 16,975 | |
| **Domains Remained** | 283,025 | |

## 🌐 Source Performance & Health Check
| Source | Category | Weight | Total Fetched | In Priority List | % List In Priority | Volatility ($\pm \%$) | Color |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **HAGEZI_ULTIMATE** | Aggregated/Wildcard | 4 | 232,644 | 186,270 | **80.07%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#d62728;'>███</span> |
| **1HOSTS_LITE** | Aggregated/Wildcard | 3 | 92,543 | 79,126 | **85.50%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#2ca02c;'>███</span> |
| **ADGUARD_BASE** | ABP Rule List | 3 | 119,335 | 98,704 | **82.71%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#17becf;'>███</span> |
| **OISD_BIG** | Aggregated/Wildcard | 2 | 215,312 | 99,113 | **46.03%** | <span style='color:green;'>`-0.0%`</span> | <span style='color:#1f77b4;'>███</span> |
| **ANUDEEP_ADSERVERS** | Specialized (Ads) | 2 | 42,347 | 7,045 | **16.64%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#9467bd;'>███</span> |
| **ADAWAY_HOSTS** | Specialized (Ads) | 2 | 6,540 | 6,488 | **99.20%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#8c564b;'>███</span> |
| **STEVENBLACK_HOSTS** | Hosts File (Legacy) | 1 | 97,120 | 37,634 | **38.75%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#ff7f0e;'>███</span> |

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
| **6** | 694 | **0.13%** |
| **5** | 2,544 | **0.48%** |
| **4** | 30,499 | **5.70%** |
| **3** | 36,396 | **6.80%** |
| **2** | 92,141 | **17.22%** |
| **1** | 372,721 | **69.65%** |

---

## 📊 Priority List Composition (Top 15 TLDs)
The most common TLDs in the final `priority_300k.txt` list.


[Image of a vertical bar chart]

| Rank | TLD | Domain Count | % of Priority List |
| :---: | :--- | :---: | :---: |
| 1 | **.com** | 181,237 | 60.41% |
| 2 | **.net** | 24,113 | 8.04% |
| 3 | **.de** | 7,414 | 2.47% |
| 4 | **.org** | 6,567 | 2.19% |
| 5 | **.xyz** | 6,021 | 2.01% |
| 6 | **.ru** | 5,514 | 1.84% |
| 7 | **.pro** | 5,001 | 1.67% |
| 8 | **.fr** | 3,893 | 1.30% |
| 9 | **.cn** | 3,703 | 1.23% |
| 10 | **.br** | 3,641 | 1.21% |
| 11 | **.io** | 3,523 | 1.17% |
| 12 | **.info** | 3,053 | 1.02% |
| 13 | **.jp** | 3,011 | 1.00% |
| 14 | **.app** | 2,423 | 0.81% |
| 15 | **.pl** | 2,262 | 0.75% |

---

## 📈 Interactive Visualization


[Image of a time series line graph]

See `historical_trend_chart.png` and `score_distribution_chart.png`.