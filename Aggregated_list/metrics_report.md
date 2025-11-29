# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)
*Generated: 2025-11-29 04:47:09*

## 📜 Aggregation Summary
| Metric | Count | Insight |
| :--- | :---: | :--- |
| **Total Scored Domains** | **531,502** | Size of the list including TLD rejected entries. |
| Change vs. Last Run | `+0` ➡️ | Trend in the total unique domain pool. |
| Priority List Size | 53,637 | Domains with Score >= **Min Score: 14** (Max: 33). |
| High Consensus (Score 11+) | 133,278 | Domains backed by strong weighted evidence. |
| TLD Filter Exclusions | 14,419 | Domains rejected by the abusive TLD list. |

---

## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)
These are the highest-scoring domains that failed to make the final list:
| Domain | Weighted Score | Exclusion Reason |
| :--- | :---: | :--- |
| `stats.ozwebsites.biz` | <span style='color:red;'>**30**</span> | TLD Rejected: **.biz is marked as abusive.** |
| `zlp6s.pw` | <span style='color:red;'>**30**</span> | TLD Rejected: **.pw is marked as abusive.** |
| `crosspromotion.weplayer.cc` | <span style='color:red;'>**29**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `ad.weplayer.cc` | <span style='color:red;'>**29**</span> | TLD Rejected: **.cc is marked as abusive.** |
| `adserve.work` | <span style='color:red;'>**29**</span> | TLD Rejected: **.work is marked as abusive.** |
| `api-push.com` | <span style='color:orange;'>**13**</span> | Score Cutoff: **13 is below minimum confidence 14.** |
| `imirkii05.com` | <span style='color:orange;'>**13**</span> | Score Cutoff: **13 is below minimum confidence 14.** |
| `insights.gatedcontent.com` | <span style='color:orange;'>**13**</span> | Score Cutoff: **13 is below minimum confidence 14.** |
| `pixel.nanotera.eu` | <span style='color:orange;'>**13**</span> | Score Cutoff: **13 is below minimum confidence 14.** |
| `eng45.com` | <span style='color:orange;'>**13**</span> | Score Cutoff: **13 is below minimum confidence 14.** |

*The complete list of 477,865 excluded domains is in `excluded_domains_report.csv`.*

---

## 🚫 Top 10 Abusive TLD Trends
Domains with these TLDs were excluded from the priority list.
| Rank | Abusive TLD | Excluded Domain Count |
| :---: | :--- | :---: |
| 1 | **.online** | 1,472 |
| 2 | **.site** | 1,446 |
| 3 | **.space** | 1,281 |
| 4 | **.top** | 1,161 |
| 5 | **.website** | 1,083 |
| 6 | **.shop** | 1,024 |
| 7 | **.store** | 1,012 |
| 8 | **.click** | 768 |
| 9 | **.icu** | 644 |
| 10 | **.cfd** | 589 |

---

## 🔄 Priority List Change & Novelty Index
| Change Type | Domain Count | Novelty Breakdown |
| :--- | :---: | :--- |
| **Domains Added** | 53,637 | **53,637 Fresh** ✨ |
| **Domains Removed** | 234,455 | |
| **Domains Remained** | 0 | |

## 🌐 Source Performance & Health Check
| Source | Category | Weight | FP Risk | Coverage | Total Fetched | % In Priority | Volatility ($\pm \%$) | Color |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **HAGEZI_ULTIMATE** | Aggregated/Wildcard | 7 | **High 🟥** | **Broad 🟩** | 234,133 | **22.44%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#d62728;'>███</span> |
| **1HOSTS_LITE** | Aggregated/Wildcard | 6 | **Medium 🟨** | **Broad 🟩** | 92,444 | **38.36%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#2ca02c;'>███</span> |
| **OISD_BIG** | Aggregated/Wildcard | 5 | **High 🟥** | **Broad 🟩** | 216,323 | **20.61%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#1f77b4;'>███</span> |
| **ADGUARD_BASE** | ABP Rule List | 5 | **Medium 🟨** | **Medium 🟨** | 119,980 | **34.51%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#17becf;'>███</span> |
| **ANUDEEP_ADSERVERS** | Specialized (Ads) | 4 | **High 🟥** | **Specialized 🟦** | 42,347 | **4.88%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#9467bd;'>███</span> |
| **STEVENBLACK_HOSTS** | Hosts File (Legacy) | 3 | **High 🟥** | **Medium 🟨** | 88,075 | **13.69%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#ff7f0e;'>███</span> |
| **ADAWAY_HOSTS** | Specialized (Ads) | 3 | **Low 🟩** | **Specialized 🟦** | 6,540 | **28.82%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#8c564b;'>███</span> |

---

## 🖇️ List Similarity Matrix (Jaccard Index)
Measures the overlap between lists (Intersection / Union).
Dark blue = highly unique. Bright yellow = highly redundant.






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
Analysis of all domains in the final `tiny_priority_list.txt` list.

**Top 15 TLDs in `tiny_priority_list.txt`:**
| Rank | TLD | Domain Count | % of Priority List |
| :---: | :--- | :---: | :---: |
| 1 | **.com** | 36,540 | 68.12% |
| 2 | **.net** | 4,347 | 8.10% |
| 3 | **.pro** | 1,072 | 2.00% |
| 4 | **.org** | 1,038 | 1.94% |
| 5 | **.de** | 1,031 | 1.92% |
| 6 | **.xyz** | 873 | 1.63% |
| 7 | **.ru** | 688 | 1.28% |
| 8 | **.io** | 623 | 1.16% |
| 9 | **.vn** | 503 | 0.94% |
| 10 | **.info** | 489 | 0.91% |
| 11 | **.cn** | 428 | 0.80% |
| 12 | **.jp** | 387 | 0.72% |
| 13 | **.pl** | 369 | 0.69% |
| 14 | **.digital** | 291 | 0.54% |
| 15 | **.se** | 288 | 0.54% |

**Domain Properties:**
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. Domain Entropy** | `2.802` | 'Randomness' score. (Higher = more 'random', e.g., DGA) |
| **Top 5 Trigrams** | `ing`, `ont`, `lou`, `ron`, `ion` | Common 3-letter strings in domain names. |

**Domain Depth (Subdomains):**
| Depth | Domain Count | % of Priority List | Example |
| :---: | :---: | :---: | :--- |
| 1 (e.g., d.d) | 33,750 | 62.92% | `google.com` |
| 2 (e.g., d.d.d) | 17,452 | 32.54% | `ads.google.com` |
| 3 (e.g., d.d.d.d) | 2,180 | 4.06% | `sub.ads.google.com` |
| 4 (e.g., d.d.d.d.d) | 226 | 0.42% | `sub.ads.google.com` |
| 5 (e.g., d.d.d.d.d.d) | 26 | 0.05% | `sub.ads.google.com` |
| 6 (e.g., d.d.d.d.d.d.d) | 3 | 0.01% | `sub.ads.google.com` |

### 2. New Domain Threat Analysis
Analysis of the **53,637** domains *added* to the list this run.
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. *New* Domain Entropy** | `2.802` | 'Randomness' of *new* threats. A spike here is bad. |
| **Top 5 *New* Trigrams** | `ing`, `ont`, `lou`, `ron`, `ion` | Shows the 'shape' of new attack campaigns. |

---

## 📈 Interactive Visualization





See `historical_trend_chart.png`, `score_distribution_chart.png`, and `jaccard_heatmap.png`.