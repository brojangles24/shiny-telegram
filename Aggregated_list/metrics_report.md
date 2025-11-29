# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)
*Generated: 2025-11-29 04:27:44*

## 📜 Aggregation Summary
| Metric | Count | Insight |
| :--- | :---: | :--- |
| **Total Scored Domains** | **531,502** | Size of the list including TLD rejected entries. |
| Change vs. Last Run | `+133` ⬆️ | Trend in the total unique domain pool. |
| Priority List Size | 234,455 | Domains with Score >= **Min Score: 6** (Max: 33). |
| High Consensus (Score 11+) | 133,278 | Domains backed by strong weighted evidence. |
| TLD Filter Exclusions | 49,011 | Domains rejected by the abusive TLD list. |

---

## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)
These are the highest-scoring domains that failed to make the final list:
| Domain | Weighted Score | Exclusion Reason |
| :--- | :---: | :--- |
| `stats.ozwebsites.biz` | <span style='color:red;'>**30**</span> | TLD Rejected: **.biz is marked as abusive.** |
| `zlp6s.pw` | <span style='color:red;'>**30**</span> | TLD Rejected: **.pw is marked as abusive.** |
| `crosspromotion.weplayer.cc` | <span style='color:red;'>**29**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `adop.cc` | <span style='color:red;'>**29**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `adserve.work` | <span style='color:red;'>**29**</span> | TLD Rejected: **.work is marked as abusive.** |
| `bafkreibgd2wtcznb45mcvspfhagfwzzxxgieudttk3iqhs5osvkbeehtqi.ipfs.dweb.link` | <span style='color:orange;'>**5**</span> | Score Cutoff: **5 is below minimum confidence 6.** |
| `65786545.weebly.com` | <span style='color:orange;'>**5**</span> | Score Cutoff: **5 is below minimum confidence 6.** |
| `ship-be.gl.at.ply.gg` | <span style='color:orange;'>**5**</span> | Score Cutoff: **5 is below minimum confidence 6.** |
| `storpnaive.pro` | <span style='color:orange;'>**5**</span> | Score Cutoff: **5 is below minimum confidence 6.** |
| `cus.infolife.mobi` | <span style='color:orange;'>**5**</span> | Score Cutoff: **5 is below minimum confidence 6.** |

*The complete list of 297,047 excluded domains is in `excluded_domains_report.csv`.*

---

## 🚫 Top 10 Abusive TLD Trends
Domains with these TLDs were excluded from the priority list.
| Rank | Abusive TLD | Excluded Domain Count |
| :---: | :--- | :---: |
| 1 | **.top** | 6,151 |
| 2 | **.shop** | 5,328 |
| 3 | **.click** | 3,418 |
| 4 | **.online** | 2,963 |
| 5 | **.site** | 2,671 |
| 6 | **.cfd** | 2,364 |
| 7 | **.icu** | 2,277 |
| 8 | **.space** | 2,026 |
| 9 | **.store** | 1,789 |
| 10 | **.cc** | 1,611 |

---

## 🔄 Priority List Change & Novelty Index
| Change Type | Domain Count | Novelty Breakdown |
| :--- | :---: | :--- |
| **Domains Added** | 12 | **12 Fresh** ✨ |
| **Domains Removed** | 0 | |
| **Domains Remained** | 234,443 | |

## 🌐 Source Performance & Health Check
| Source | Category | Weight | Total Fetched | In Priority List | % List In Priority | Volatility ($\pm \%$) | Color |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **HAGEZI_ULTIMATE** | Aggregated/Wildcard | 7 | 234,133 | 187,206 | **79.96%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#d62728;'>███</span> |
| **1HOSTS_LITE** | Aggregated/Wildcard | 6 | 92,444 | 78,851 | **85.30%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#2ca02c;'>███</span> |
| **OISD_BIG** | Aggregated/Wildcard | 5 | 216,323 | 74,838 | **34.60%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#1f77b4;'>███</span> |
| **ADGUARD_BASE** | ABP Rule List | 5 | 119,980 | 57,291 | **47.75%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#17becf;'>███</span> |
| **ANUDEEP_ADSERVERS** | Specialized (Ads) | 4 | 42,347 | 7,046 | **16.64%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#9467bd;'>███</span> |
| **STEVENBLACK_HOSTS** | Hosts File (Legacy) | 3 | 88,075 | 33,696 | **38.26%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#ff7f0e;'>███</span> |
| **ADAWAY_HOSTS** | Specialized (Ads) | 3 | 6,540 | 6,488 | **99.20%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#8c564b;'>███</span> |

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
| **4** | 30,680 | **5.77%** |
| **3** | 36,321 | **6.83%** |
| **2** | 89,345 | **16.81%** |
| **1** | 371,806 | **69.95%** |

---

## 🔬 Domain Property Analysis (DPA)
A 'nerd-out' deep-dive into the *properties* of the domains being blocked.

### 1. Final Priority List Composition
Analysis of all domains in the final `priority_list.txt` list.

**Top 15 TLDs in `priority_list.txt`:**
| Rank | TLD | Domain Count | % of Priority List |
| :---: | :--- | :---: | :---: |
| 1 | **.com** | 149,393 | 63.72% |
| 2 | **.net** | 18,839 | 8.04% |
| 3 | **.de** | 5,443 | 2.32% |
| 4 | **.org** | 5,270 | 2.25% |
| 5 | **.xyz** | 5,126 | 2.19% |
| 6 | **.ru** | 4,633 | 1.98% |
| 7 | **.io** | 3,164 | 1.35% |
| 8 | **.cn** | 3,082 | 1.31% |
| 9 | **.pro** | 2,880 | 1.23% |
| 10 | **.info** | 2,788 | 1.19% |
| 11 | **.pl** | 1,926 | 0.82% |
| 12 | **.fr** | 1,865 | 0.80% |
| 13 | **.uk** | 1,631 | 0.70% |
| 14 | **.app** | 1,620 | 0.69% |
| 15 | **.jp** | 1,495 | 0.64% |

**Domain Properties:**
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. Domain Entropy** | `2.748` | 'Randomness' score. (Higher = more 'random', e.g., DGA) |
| **Top 5 Trigrams** | `ing`, `ion`, `ent`, `ter`, `ate` | Common 3-letter strings in domain names. |

**Domain Depth (Subdomains):**
| Depth | Domain Count | % of Priority List | Example |
| :---: | :---: | :---: | :--- |
| 1 (e.g., d.d) | 137,022 | 58.44% | `google.com` |
| 2 (e.g., d.d.d) | 77,784 | 33.18% | `ads.google.com` |
| 3 (e.g., d.d.d.d) | 15,615 | 6.66% | `sub.ads.google.com` |
| 4 (e.g., d.d.d.d.d) | 2,724 | 1.16% | `sub.ads.google.com` |
| 5 (e.g., d.d.d.d.d.d) | 741 | 0.32% | `sub.ads.google.com` |
| 6 (e.g., d.d.d.d.d.d.d) | 261 | 0.11% | `sub.ads.google.com` |
| 7 (e.g., d.d.d.d.d.d.d.d) | 39 | 0.02% | `sub.ads.google.com` |
| 8 (e.g., d.d.d.d.d.d.d.d.d) | 49 | 0.02% | `sub.ads.google.com` |
| 9 (e.g., d.d.d.d.d.d.d.d.d.d) | 134 | 0.06% | `sub.ads.google.com` |
| 10 (e.g., d.d.d.d.d.d.d.d.d.d.d) | 63 | 0.03% | `sub.ads.google.com` |
| 11 (e.g., d.d.d.d.d.d.d.d.d.d.d.d) | 14 | 0.01% | `sub.ads.google.com` |
| 12 (e.g., d.d.d.d.d.d.d.d.d.d.d.d.d) | 1 | 0.00% | `sub.ads.google.com` |
| 19 (e.g., d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d) | 7 | 0.00% | `sub.ads.google.com` |
| 21 (e.g., d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d.d) | 1 | 0.00% | `sub.ads.google.com` |

### 2. New Domain Threat Analysis
Analysis of the **12** domains *added* to the list this run.
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. *New* Domain Entropy** | `3.098` | 'Randomness' of *new* threats. A spike here is bad. |
| **Top 5 *New* Trigrams** | `nmr`, `mru`, `rue`, `uee`, `ees` | Shows the 'shape' of new attack campaigns. |

---

## 📈 Interactive Visualization





See `historical_trend_chart.png` and `score_distribution_chart.png`.