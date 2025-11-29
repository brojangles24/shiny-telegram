# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)
*Generated: 2025-11-29 02:41:36*

## 📜 Aggregation Summary
| Metric | Count | Insight |
| :--- | :---: | :--- |
| **Total Scored Domains** | **531,369** | Size of the list including TLD rejected entries. |
| Change vs. Last Run | `+0` ➡️ | Trend in the total unique domain pool. |
| Priority List Size | 212,901 | Domains with Score >= **Min Score: 6** (Max: 29). |
| High Consensus (Score 11+) | 102,328 | Domains backed by strong weighted evidence. |
| TLD Filter Exclusions | 48,199 | Domains rejected by the abusive TLD list. |

---

## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)
These are the highest-scoring domains that failed to make the final list:
| Domain | Weighted Score | Exclusion Reason |
| :--- | :---: | :--- |
| `stats.ozwebsites.biz` | <span style='color:red;'>**26**</span> | TLD Rejected: **.biz is marked as abusive.** |
| `zlp6s.pw` | <span style='color:red;'>**26**</span> | TLD Rejected: **.pw is marked as abusive.** |
| `adserve.work` | <span style='color:red;'>**25**</span> | TLD Rejected: **.work is marked as abusive.** |
| `ad.weplayer.cc` | <span style='color:red;'>**25**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `crosspromotion.weplayer.cc` | <span style='color:red;'>**25**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `tvevents-production.tvinteractive.tv` | <span style='color:orange;'>**5**</span> | Score Cutoff: **5 is below minimum confidence 6.** |
| `innovativemetrics.com` | <span style='color:orange;'>**5**</span> | Score Cutoff: **5 is below minimum confidence 6.** |
| `node9.nimiq-network.com` | <span style='color:orange;'>**5**</span> | Score Cutoff: **5 is below minimum confidence 6.** |
| `brax-cdn.com` | <span style='color:orange;'>**5**</span> | Score Cutoff: **5 is below minimum confidence 6.** |
| `tvcontrol-azkaban.tvinteractive.tv` | <span style='color:orange;'>**5**</span> | Score Cutoff: **5 is below minimum confidence 6.** |

*The complete list of 318,468 excluded domains is in `excluded_domains_report.csv`.*

---

## 🚫 Top 10 Abusive TLD Trends
Domains with these TLDs were excluded from the priority list.
| Rank | Abusive TLD | Excluded Domain Count |
| :---: | :--- | :---: |
| 1 | **.top** | 5,728 |
| 2 | **.shop** | 5,304 |
| 3 | **.click** | 3,406 |
| 4 | **.online** | 2,930 |
| 5 | **.site** | 2,642 |
| 6 | **.cfd** | 2,357 |
| 7 | **.icu** | 2,276 |
| 8 | **.space** | 2,015 |
| 9 | **.store** | 1,778 |
| 10 | **.cc** | 1,573 |

---

## 🔄 Priority List Change & Novelty Index
| Change Type | Domain Count | Novelty Breakdown |
| :--- | :---: | :--- |
| **Domains Added** | 113,031 | **113,031 Fresh** ✨ |
| **Domains Removed** | 0 | |
| **Domains Remained** | 99,870 | |

## 🌐 Source Performance & Health Check
| Source | Category | Weight | Total Fetched | In Priority List | % List In Priority | Volatility ($\pm \%$) | Color |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **HAGEZI_ULTIMATE** | Aggregated/Wildcard | 6 | 234,133 | 187,206 | **79.96%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#d62728;'>███</span> |
| **1HOSTS_LITE** | Aggregated/Wildcard | 5 | 92,444 | 60,004 | **64.91%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#2ca02c;'>███</span> |
| **ADGUARD_BASE** | ABP Rule List | 5 | 119,931 | 57,275 | **47.76%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#17becf;'>███</span> |
| **OISD_BIG** | Aggregated/Wildcard | 4 | 216,246 | 74,831 | **34.60%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#1f77b4;'>███</span> |
| **ANUDEEP_ADSERVERS** | Specialized (Ads) | 4 | 42,347 | 7,046 | **16.64%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#9467bd;'>███</span> |
| **ADAWAY_HOSTS** | Specialized (Ads) | 3 | 6,540 | 3,793 | **58.00%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#8c564b;'>███</span> |
| **STEVENBLACK_HOSTS** | Hosts File (Legacy) | 2 | 88,075 | 31,001 | **35.20%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#ff7f0e;'>███</span> |

---

## 🖇️ List Similarity Matrix (Jaccard Index)
Measures the overlap between lists (Intersection / Union). A high value (e.g., 0.85) means the lists are very redundant.



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
| **5** | 2,547 | **0.48%** |
| **4** | 30,680 | **5.77%** |
| **3** | 36,349 | **6.84%** |
| **2** | 89,296 | **16.80%** |
| **1** | 371,694 | **69.95%** |

---

## 🔬 Domain Property Analysis (DPA)
A 'nerd-out' deep-dive into the *properties* of the domains being blocked.

### 1. Final Priority List Composition
Analysis of all domains in the final `priority_list.txt` list.

**Top 15 TLDs in `priority_list.txt`:**
| Rank | TLD | Domain Count | % of Priority List |
| :---: | :--- | :---: | :---: |
| 1 | **.com** | 135,282 | 63.54% |
| 2 | **.net** | 16,394 | 7.70% |
| 3 | **.de** | 5,141 | 2.41% |
| 4 | **.xyz** | 4,880 | 2.29% |
| 5 | **.org** | 4,834 | 2.27% |
| 6 | **.ru** | 4,390 | 2.06% |
| 7 | **.cn** | 2,906 | 1.36% |
| 8 | **.pro** | 2,846 | 1.34% |
| 9 | **.info** | 2,708 | 1.27% |
| 10 | **.io** | 2,633 | 1.24% |
| 11 | **.pl** | 1,877 | 0.88% |
| 12 | **.fr** | 1,813 | 0.85% |
| 13 | **.app** | 1,541 | 0.72% |
| 14 | **.uk** | 1,478 | 0.69% |
| 15 | **.jp** | 1,364 | 0.64% |

**Domain Properties:**
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. Domain Entropy** | `2.762` | 'Randomness' score. (Higher = more 'random', e.g., DGA) |
| **Top 5 Trigrams** | `ing`, `ion`, `ent`, `ter`, `ate` | Common 3-letter strings in domain names. |

**Domain Depth (Subdomains):**
| Depth | Domain Count | % of Priority List | Example |
| :---: | :---: | :---: | :--- |
| 1 (e.g., d.d) | 132,144 | 62.07% | `google.com` |
| 2 (e.g., d.d.d) | 65,975 | 30.99% | `ads.google.com` |
| 3 (e.g., d.d.d.d) | 12,207 | 5.73% | `sub.ads.google.com` |
| 4 (e.g., d.d.d.d.d) | 1,912 | 0.90% | `sub.ads.google.com` |
| 5 (e.g., d.d.d.d.d.d) | 480 | 0.23% | `sub.ads.google.com` |
| 6 (e.g., d.d.d.d.d.d.d) | 145 | 0.07% | `sub.ads.google.com` |
| 7 (e.g., d.d.d.d.d.d.d.d) | 19 | 0.01% | `sub.ads.google.com` |
| 8 (e.g., d.d.d.d.d.d.d.d.d) | 16 | 0.01% | `sub.ads.google.com` |
| 9 (e.g., d.d.d.d.d.d.d.d.d.d) | 2 | 0.00% | `sub.ads.google.com` |
| 10 (e.g., d.d.d.d.d.d.d.d.d.d.d) | 1 | 0.00% | `sub.ads.google.com` |

### 2. New Domain Threat Analysis
Analysis of the **113,031** domains *added* to the list this run.
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. *New* Domain Entropy** | `2.775` | 'Randomness' of *new* threats. A spike here is bad. |
| **Top 5 *New* Trigrams** | `ing`, `ion`, `ate`, `ent`, `ter` | Shows the 'shape' of new attack campaigns. |

---

## 📈 Interactive Visualization





See `historical_trend_chart.png` and `score_distribution_chart.png`.