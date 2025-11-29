# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)
*Generated: 2025-11-29 02:33:19*

## 📜 Aggregation Summary
| Metric | Count | Insight |
| :--- | :---: | :--- |
| **Total Scored Domains** | **531,369** | Size of the list including TLD rejected entries. |
| Change vs. Last Run | `+0` ➡️ | Trend in the total unique domain pool. |
| Priority List Size | 99,870 | Domains with Score >= **6** (Max: 17). |
| High Consensus (Score 6+) | 132,358 | Domains backed by strong weighted evidence. |
| TLD Filter Exclusions | 32,488 | Domains rejected by the abusive TLD list. |

---

## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)
These are the highest-scoring domains that failed to make the final list:
| Domain | Weighted Score | Exclusion Reason |
| :--- | :---: | :--- |
| `optimix.asia` | <span style='color:red;'>**15**</span> | TLD Rejected: **.asia is marked as abusive.** |
| `crosspromotion.weplayer.cc` | <span style='color:red;'>**15**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `stats.ozwebsites.biz` | <span style='color:red;'>**15**</span> | TLD Rejected: **.biz is marked as abusive.** |
| `ad.weplayer.cc` | <span style='color:red;'>**15**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `adop.cc` | <span style='color:red;'>**15**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `ads.miarroba.com` | <span style='color:orange;'>**5**</span> | Score Cutoff: **5 is below minimum confidence 6.** |
| `twkvetgiilegjwzxfo.store` | <span style='color:orange;'>**5**</span> | Score Cutoff: **5 is below minimum confidence 6.** |
| `kn2pab.icu` | <span style='color:orange;'>**5**</span> | Score Cutoff: **5 is below minimum confidence 6.** |
| `lrukvnjpgdyfpv.store` | <span style='color:orange;'>**5**</span> | Score Cutoff: **5 is below minimum confidence 6.** |
| `adv.donejty.pl` | <span style='color:orange;'>**5**</span> | Score Cutoff: **5 is below minimum confidence 6.** |

*The complete list of 431,499 excluded domains is in `excluded_domains_report.csv`.*

---

## 🚫 Top 10 Abusive TLD Trends
Domains with these TLDs were excluded from the priority list.
| Rank | Abusive TLD | Excluded Domain Count |
| :---: | :--- | :---: |
| 1 | **.shop** | 3,637 |
| 2 | **.top** | 3,443 |
| 3 | **.click** | 2,424 |
| 4 | **.online** | 2,230 |
| 5 | **.site** | 2,140 |
| 6 | **.space** | 1,548 |
| 7 | **.website** | 1,353 |
| 8 | **.cfd** | 1,338 |
| 9 | **.store** | 1,292 |
| 10 | **.icu** | 1,158 |

---

## 🔄 Priority List Change & Novelty Index
| Change Type | Domain Count | Novelty Breakdown |
| :--- | :---: | :--- |
| **Domains Added** | 69,104 | **69,104 Fresh** ✨ |
| **Domains Removed** | 0 | |
| **Domains Remained** | 30,766 | |

## 🌐 Source Performance & Health Check
| Source | Category | Weight | Total Fetched | In Priority List | % List In Priority | Volatility ($\pm \%$) | Color |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **HAGEZI_ULTIMATE** | Aggregated/Wildcard | 4 | 234,133 | 96,706 | **41.30%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#d62728;'>███</span> |
| **1HOSTS_LITE** | Aggregated/Wildcard | 3 | 92,444 | 55,877 | **60.44%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#2ca02c;'>███</span> |
| **ADGUARD_BASE** | ABP Rule List | 3 | 119,931 | 54,631 | **45.55%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#17becf;'>███</span> |
| **OISD_BIG** | Aggregated/Wildcard | 2 | 216,246 | 58,392 | **27.00%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#1f77b4;'>███</span> |
| **ANUDEEP_ADSERVERS** | Specialized (Ads) | 2 | 42,347 | 2,298 | **5.43%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#9467bd;'>███</span> |
| **ADAWAY_HOSTS** | Specialized (Ads) | 2 | 6,540 | 2,498 | **38.20%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#8c564b;'>███</span> |
| **STEVENBLACK_HOSTS** | Hosts File (Legacy) | 1 | 88,075 | 12,858 | **14.60%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#ff7f0e;'>███</span> |

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
| 1 | **.com** | 64,229 | 64.31% |
| 2 | **.net** | 7,616 | 7.63% |
| 3 | **.de** | 2,897 | 2.90% |
| 4 | **.org** | 1,852 | 1.85% |
| 5 | **.ru** | 1,829 | 1.83% |
| 6 | **.xyz** | 1,427 | 1.43% |
| 7 | **.io** | 1,392 | 1.39% |
| 8 | **.pro** | 1,369 | 1.37% |
| 9 | **.fr** | 1,166 | 1.17% |
| 10 | **.cn** | 1,154 | 1.16% |
| 11 | **.jp** | 933 | 0.93% |
| 12 | **.info** | 833 | 0.83% |
| 13 | **.pl** | 602 | 0.60% |
| 14 | **.uk** | 588 | 0.59% |
| 15 | **.co** | 587 | 0.59% |

**Domain Properties:**
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. Domain Entropy** | `2.747` | 'Randomness' score. (Higher = more 'random', e.g., DGA) |
| **Top 5 Trigrams** | `ing`, `ion`, `ent`, `lou`, `ont` | Common 3-letter strings in domain names. |

**Domain Depth (Subdomains):**
| Depth | Domain Count | % of Priority List | Example |
| :---: | :---: | :---: | :--- |
| 1 (e.g., d.d) | 58,567 | 58.64% | `google.com` |
| 2 (e.g., d.d.d) | 34,651 | 34.70% | `ads.google.com` |
| 3 (e.g., d.d.d.d) | 5,350 | 5.36% | `sub.ads.google.com` |
| 4 (e.g., d.d.d.d.d) | 1,004 | 1.01% | `sub.ads.google.com` |
| 5 (e.g., d.d.d.d.d.d) | 220 | 0.22% | `sub.ads.google.com` |
| 6 (e.g., d.d.d.d.d.d.d) | 57 | 0.06% | `sub.ads.google.com` |
| 7 (e.g., d.d.d.d.d.d.d.d) | 4 | 0.00% | `sub.ads.google.com` |
| 8 (e.g., d.d.d.d.d.d.d.d.d) | 15 | 0.02% | `sub.ads.google.com` |
| 9 (e.g., d.d.d.d.d.d.d.d.d.d) | 2 | 0.00% | `sub.ads.google.com` |

### 2. New Domain Threat Analysis
Analysis of the **69,104** domains *added* to the list this run.
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. *New* Domain Entropy** | `2.711` | 'Randomness' of *new* threats. A spike here is bad. |
| **Top 5 *New* Trigrams** | `ing`, `ion`, `tra`, `com`, `ent` | Shows the 'shape' of new attack campaigns. |

---

## 📈 Interactive Visualization





See `historical_trend_chart.png` and `score_distribution_chart.png`.