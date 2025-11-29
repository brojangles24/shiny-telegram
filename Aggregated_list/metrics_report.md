# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)
*Generated: 2025-11-29 04:30:40*

## 📜 Aggregation Summary
| Metric | Count | Insight |
| :--- | :---: | :--- |
| **Total Scored Domains** | **1,351,698** | Size of the list including TLD rejected entries. |
| Change vs. Last Run | `+820196` ⬆️ | Trend in the total unique domain pool. |
| Priority List Size | 1,231,017 | Domains with Score >= **Min Score: 1** (Max: 33). |
| High Consensus (Score 11+) | 156,153 | Domains backed by strong weighted evidence. |
| TLD Filter Exclusions | 120,681 | Domains rejected by the abusive TLD list. |

---

## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)
These are the highest-scoring domains that failed to make the final list:
| Domain | Weighted Score | Exclusion Reason |
| :--- | :---: | :--- |
| `zlp6s.pw` | <span style='color:red;'>**30**</span> | TLD Rejected: **.pw is marked as abusive.** |
| `stats.ozwebsites.biz` | <span style='color:red;'>**30**</span> | TLD Rejected: **.biz is marked as abusive.** |
| `adop.cc` | <span style='color:red;'>**29**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `adserve.work` | <span style='color:red;'>**29**</span> | TLD Rejected: **.work is marked as abusive.** |
| `optimix.asia` | <span style='color:red;'>**29**</span> | TLD Rejected: **.asia is marked as abusive.** |

*The complete list of 120,681 excluded domains is in `excluded_domains_report.csv`.*

---

## 🚫 Top 10 Abusive TLD Trends
Domains with these TLDs were excluded from the priority list.
| Rank | Abusive TLD | Excluded Domain Count |
| :---: | :--- | :---: |
| 1 | **.top** | 16,233 |
| 2 | **.shop** | 8,880 |
| 3 | **.online** | 7,364 |
| 4 | **.icu** | 6,668 |
| 5 | **.site** | 6,260 |
| 6 | **.cc** | 6,100 |
| 7 | **.click** | 5,601 |
| 8 | **.cfd** | 4,877 |
| 9 | **.space** | 4,657 |
| 10 | **.biz** | 4,290 |

---

## 🔄 Priority List Change & Novelty Index
| Change Type | Domain Count | Novelty Breakdown |
| :--- | :---: | :--- |
| **Domains Added** | 1,001,493 | **1,001,493 Fresh** ✨ |
| **Domains Removed** | 4,931 | |
| **Domains Remained** | 229,524 | |

## 🌐 Source Performance & Health Check
| Source | Category | Weight | Total Fetched | In Priority List | % List In Priority | Volatility ($\pm \%$) | Color |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **HAGEZI_ULTIMATE** | Aggregated/Wildcard | 7 | 234,133 | 187,206 | **79.96%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#d62728;'>███</span> |
| **1HOSTS_XTRA** | Aggregated/Wildcard | 6 | 941,084 | 872,332 | **92.69%** | <span style='color:cyan;'>`New`</span> | <span style='color:#e377c2;'>███</span> |
| **OISD_BIG** | Aggregated/Wildcard | 5 | 216,323 | 188,803 | **87.28%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#1f77b4;'>███</span> |
| **ADGUARD_BASE** | ABP Rule List | 5 | 119,980 | 98,991 | **82.51%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#17becf;'>███</span> |
| **ANUDEEP_ADSERVERS** | Specialized (Ads) | 4 | 42,347 | 41,973 | **99.12%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#9467bd;'>███</span> |
| **STEVENBLACK_HOSTS** | Hosts File (Legacy) | 3 | 88,075 | 73,443 | **83.39%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#ff7f0e;'>███</span> |
| **ADAWAY_HOSTS** | Specialized (Ads) | 3 | 6,540 | 6,498 | **99.36%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#8c564b;'>███</span> |

---

## 🖇️ List Similarity Matrix (Jaccard Index)
Measures the overlap between lists (Intersection / Union). A high value (e.g., 0.85) means the lists are very redundant.



| Source |**1HOSTS...** | **ADAWAY...** | **ADGUAR...** | **ANUDEE...** | **HAGEZI...** | **OISD_B...** | **STEVEN...** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1HOSTS_XTRA** | `1.00` | 0.00 | 0.05 | 0.00 | 0.08 | 0.04 | 0.01 |
| **ADAWAY_HOSTS** | 0.00 | `1.00` | 0.01 | 0.04 | 0.01 | 0.00 | 0.07 |
| **ADGUARD_BASE** | 0.05 | 0.01 | `1.00` | 0.01 | 0.23 | 0.16 | 0.02 |
| **ANUDEEP_ADSERVERS** | 0.00 | 0.04 | 0.01 | `1.00` | 0.01 | 0.01 | 0.03 |
| **HAGEZI_ULTIMATE** | 0.08 | 0.01 | 0.23 | 0.01 | `1.00` | 0.23 | 0.05 |
| **OISD_BIG** | 0.04 | 0.00 | 0.16 | 0.01 | 0.23 | `1.00` | 0.09 |
| **STEVENBLACK_HOSTS** | 0.01 | 0.07 | 0.02 | 0.03 | 0.05 | 0.09 | `1.00` |

---

## 🤝 Domain Overlap Breakdown
Distribution of domains across multiple sources (as a percentage of the Total Scored Domains).
| Overlap Level (Sources) | Domains (Count) | % of Total Scored List |
| :---: | :---: | :---: |
| **7** | 100 | **0.01%** |
| **6** | 649 | **0.05%** |
| **5** | 2,533 | **0.19%** |
| **4** | 32,096 | **2.37%** |
| **3** | 39,700 | **2.94%** |
| **2** | 107,119 | **7.92%** |
| **1** | 1,169,501 | **86.52%** |

---

## 🔬 Domain Property Analysis (DPA)
A 'nerd-out' deep-dive into the *properties* of the domains being blocked.

### 1. Final Priority List Composition
Analysis of all domains in the final `nuclear_priority_list.txt` list.

**Top 15 TLDs in `nuclear_priority_list.txt`:**
| Rank | TLD | Domain Count | % of Priority List |
| :---: | :--- | :---: | :---: |
| 1 | **.com** | 731,865 | 59.45% |
| 2 | **.net** | 88,678 | 7.20% |
| 3 | **.org** | 54,775 | 4.45% |
| 4 | **.de** | 32,833 | 2.67% |
| 5 | **.ru** | 24,211 | 1.97% |
| 6 | **.fr** | 16,647 | 1.35% |
| 7 | **.cn** | 15,506 | 1.26% |
| 8 | **.io** | 15,391 | 1.25% |
| 9 | **.xyz** | 14,237 | 1.16% |
| 10 | **.pro** | 13,399 | 1.09% |
| 11 | **.info** | 12,618 | 1.03% |
| 12 | **.nl** | 11,313 | 0.92% |
| 13 | **.pl** | 9,023 | 0.73% |
| 14 | **.app** | 8,491 | 0.69% |
| 15 | **.co** | 7,678 | 0.62% |

**Domain Properties:**
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. Domain Entropy** | `2.800` | 'Randomness' score. (Higher = more 'random', e.g., DGA) |
| **Top 5 Trigrams** | `ing`, `ion`, `ent`, `ter`, `tra` | Common 3-letter strings in domain names. |

**Domain Depth (Subdomains):**
| Depth | Domain Count | % of Priority List | Example |
| :---: | :---: | :---: | :--- |
| 1 (e.g., d.d) | 953,070 | 77.42% | `google.com` |
| 2 (e.g., d.d.d) | 219,642 | 17.84% | `ads.google.com` |
| 3 (e.g., d.d.d.d) | 46,192 | 3.75% | `sub.ads.google.com` |
| 4 (e.g., d.d.d.d.d) | 8,699 | 0.71% | `sub.ads.google.com` |
| 5 (e.g., d.d.d.d.d.d) | 1,814 | 0.15% | `sub.ads.google.com` |
| 6 (e.g., d.d.d.d.d.d.d) | 1,152 | 0.09% | `sub.ads.google.com` |
| 7 (e.g., d.d.d.d.d.d.d.d) | 151 | 0.01% | `sub.ads.google.com` |
| 8 (e.g., d.d.d.d.d.d.d.d.d) | 73 | 0.01% | `sub.ads.google.com` |
| 9 (e.g., d.d.d.d.d.d.d.d.d.d) | 136 | 0.01% | `sub.ads.google.com` |
| 10 (e.g., d.d.d.d.d.d.d.d.d.d.d) | 67 | 0.01% | `sub.ads.google.com` |
| 11 (e.g., d.d.d.d.d.d.d.d.d.d.d.d) | 13 | 0.00% | `sub.ads.google.com` |
| 12 (e.g., d.d.d.d.d.d.d.d.d.d.d.d.d) | 1 | 0.00% | `sub.ads.google.com` |
| 19 (e.g., d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d) | 7 | 0.00% | `sub.ads.google.com` |

### 2. New Domain Threat Analysis
Analysis of the **1,001,493** domains *added* to the list this run.
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. *New* Domain Entropy** | `2.812` | 'Randomness' of *new* threats. A spike here is bad. |
| **Top 5 *New* Trigrams** | `ing`, `ent`, `ion`, `ter`, `tra` | Shows the 'shape' of new attack campaigns. |

---

## 📈 Interactive Visualization





See `historical_trend_chart.png` and `score_distribution_chart.png`.