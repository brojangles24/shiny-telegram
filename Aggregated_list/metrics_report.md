# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)
*Generated: 2025-11-29 02:28:06*

## 📜 Aggregation Summary
| Metric | Count | Insight |
| :--- | :---: | :--- |
| **Total Scored Domains** | **531,369** | Size of the list including TLD rejected entries. |
| Change vs. Last Run | `+531369` ⬆️ | Trend in the total unique domain pool. |
| Priority List Size | 30,766 | Domains with Score >= **10** (Max: 17). |
| High Consensus (Score 6+) | 132,358 | Domains backed by strong weighted evidence. |
| TLD Filter Exclusions | 10,057 | Domains rejected by the abusive TLD list. |

---

## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)
These are the highest-scoring domains that failed to make the final list:
| Domain | Weighted Score | Exclusion Reason |
| :--- | :---: | :--- |
| `ad.weplayer.cc` | <span style='color:red;'>**15**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `adserve.work` | <span style='color:red;'>**15**</span> | TLD Rejected: **.work is marked as abusive.** |
| `adop.cc` | <span style='color:red;'>**15**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `stats.ozwebsites.biz` | <span style='color:red;'>**15**</span> | TLD Rejected: **.biz is marked as abusive.** |
| `zlp6s.pw` | <span style='color:red;'>**15**</span> | TLD Rejected: **.pw is marked as abusive.** |
| `appletrelentlessfreeway.com` | <span style='color:orange;'>**9**</span> | Score Cutoff: **9 is below minimum confidence 10.** |
| `savoryink.com` | <span style='color:orange;'>**9**</span> | Score Cutoff: **9 is below minimum confidence 10.** |
| `geoip.nekudo.com` | <span style='color:orange;'>**9**</span> | Score Cutoff: **9 is below minimum confidence 10.** |
| `tghrfv.icu` | <span style='color:orange;'>**9**</span> | Score Cutoff: **9 is below minimum confidence 10.** |
| `staggereddam.com` | <span style='color:orange;'>**9**</span> | Score Cutoff: **9 is below minimum confidence 10.** |

*The complete list of 500,603 excluded domains is in `excluded_domains_report.csv`.*

---

## 🚫 Top 10 Abusive TLD Trends
Domains with these TLDs were excluded from the priority list.
| Rank | Abusive TLD | Excluded Domain Count |
| :---: | :--- | :---: |
| 1 | **.site** | 1,250 |
| 2 | **.space** | 1,215 |
| 3 | **.online** | 1,181 |
| 4 | **.website** | 1,048 |
| 5 | **.store** | 939 |
| 6 | **.cfd** | 526 |
| 7 | **.shop** | 483 |
| 8 | **.click** | 460 |
| 9 | **.cyou** | 456 |
| 10 | **.help** | 399 |

---

## 🔄 Priority List Change & Novelty Index
| Change Type | Domain Count | Novelty Breakdown |
| :--- | :---: | :--- |
| **Domains Added** | 30,766 | **30,766 Fresh** ✨ |
| **Domains Removed** | 0 | |
| **Domains Remained** | 0 | |

## 🌐 Source Performance & Health Check
| Source | Category | Weight | Total Fetched | In Priority List | % List In Priority | Volatility ($\pm \%$) | Color |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **HAGEZI_ULTIMATE** | Aggregated/Wildcard | 4 | 234,133 | 30,624 | **13.08%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#d62728;'>███</span> |
| **1HOSTS_LITE** | Aggregated/Wildcard | 3 | 92,444 | 29,883 | **32.33%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#2ca02c;'>███</span> |
| **ADGUARD_BASE** | ABP Rule List | 3 | 119,931 | 29,305 | **24.43%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#17becf;'>███</span> |
| **OISD_BIG** | Aggregated/Wildcard | 2 | 216,246 | 23,444 | **10.84%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#1f77b4;'>███</span> |
| **ANUDEEP_ADSERVERS** | Specialized (Ads) | 2 | 42,347 | 1,002 | **2.37%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#9467bd;'>███</span> |
| **ADAWAY_HOSTS** | Specialized (Ads) | 2 | 6,540 | 1,349 | **20.63%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#8c564b;'>███</span> |
| **STEVENBLACK_HOSTS** | Hosts File (Legacy) | 1 | 88,075 | 5,160 | **5.86%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#ff7f0e;'>███</span> |

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
| 1 | **.com** | 21,470 | 69.78% |
| 2 | **.net** | 2,410 | 7.83% |
| 3 | **.pro** | 815 | 2.65% |
| 4 | **.de** | 797 | 2.59% |
| 5 | **.org** | 659 | 2.14% |
| 6 | **.vn** | 465 | 1.51% |
| 7 | **.ru** | 396 | 1.29% |
| 8 | **.xyz** | 369 | 1.20% |
| 9 | **.io** | 350 | 1.14% |
| 10 | **.jp** | 237 | 0.77% |
| 11 | **.uk** | 174 | 0.57% |
| 12 | **.co** | 146 | 0.47% |
| 13 | **.digital** | 117 | 0.38% |
| 14 | **.me** | 106 | 0.34% |
| 15 | **.cn** | 105 | 0.34% |

**Domain Properties:**
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. Domain Entropy** | `2.829` | 'Randomness' score. (Higher = more 'random', e.g., DGA) |
| **Top 5 Trigrams** | `ing`, `ont`, `lou`, `clo`, `ron` | Common 3-letter strings in domain names. |

**Domain Depth (Subdomains):**
| Depth | Domain Count | % of Priority List | Example |
| :---: | :---: | :---: | :--- |
| 1 (e.g., d.d) | 20,248 | 65.81% | `google.com` |
| 2 (e.g., d.d.d) | 9,261 | 30.10% | `ads.google.com` |
| 3 (e.g., d.d.d.d) | 1,133 | 3.68% | `sub.ads.google.com` |
| 4 (e.g., d.d.d.d.d) | 106 | 0.34% | `sub.ads.google.com` |
| 5 (e.g., d.d.d.d.d.d) | 16 | 0.05% | `sub.ads.google.com` |
| 6 (e.g., d.d.d.d.d.d.d) | 2 | 0.01% | `sub.ads.google.com` |

### 2. New Domain Threat Analysis
Analysis of the **30,766** domains *added* to the list this run.
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. *New* Domain Entropy** | `2.829` | 'Randomness' of *new* threats. A spike here is bad. |
| **Top 5 *New* Trigrams** | `ing`, `ont`, `lou`, `clo`, `ron` | Shows the 'shape' of new attack campaigns. |

---

## 📈 Interactive Visualization





See `historical_trend_chart.png` and `score_distribution_chart.png`.