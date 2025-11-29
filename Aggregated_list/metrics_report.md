# 🛡️ Singularity DNS Blocklist Dashboard (v5.8.4)
*Generated: 2025-11-29 05:29:10*

## 📜 Aggregation Summary
| Metric | Count | Insight |
| :--- | :---: | :--- |
| **Total Scored Domains** | **531,517** | Size of the list including TLD rejected entries. |
| Change vs. Last Run | `+0` ➡️ | Trend in the total unique domain pool. |
| Priority List Size | 129,923 | Domains with **Min Confidence: 35% (Score >= 12)** (Max: 33). |
| High Consensus (Score 11+) | 133,278 | Domains backed by strong weighted evidence. |
| **Avg. Priority Score** | **16.32** | Average confidence score of the final list. |
| TLD Filter Exclusions | 0 | Domains rejected by the abusive TLD list. |

---

## 🗑️ Top Excluded Domains for Audit (High Score / TLD Rejection)
These are the highest-scoring domains that failed to make the final list:
| Domain | Weighted Score | Exclusion Reason |
| :--- | :---: | :--- |
| `aax-us-pdx-rtb.amazon-adsystem.com` | <span style='color:orange;'>**11**</span> | Score Cutoff: **11 is below minimum confidence 12.** |
| `aax-us-west-rtb.amazon-adsystem.com` | <span style='color:orange;'>**11**</span> | Score Cutoff: **11 is below minimum confidence 12.** |
| `analytics.ccs.mcafee.com` | <span style='color:orange;'>**11**</span> | Score Cutoff: **11 is below minimum confidence 12.** |
| `pad.mymovies.it` | <span style='color:orange;'>**11**</span> | Score Cutoff: **11 is below minimum confidence 12.** |
| `d3ujids68p6xmq.cloudfront.net` | <span style='color:orange;'>**11**</span> | Score Cutoff: **11 is below minimum confidence 12.** |

*The complete list of 401,594 excluded domains is in `excluded_domains_report.csv`.*

---

## 🔄 Priority List Change & Novelty Index
| Change Type | Domain Count | Novelty Breakdown |
| :--- | :---: | :--- |
| **Domains Added** | 98,689 | **98,689 Fresh** ✨ |
| **Domains Removed** | 0 | |
| **Domains Remained** | 31,234 | |

## 🌐 Source Performance & Health Check
| Source | Category | Weight | FP Risk | Coverage | Total Fetched | % In Priority | Volatility ($\pm \%$) | Color |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **HAGEZI_ULTIMATE** | Aggregated/Wildcard | 7 | **High 🟥** | **Broad 🟩** | 234,133 | **54.68%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#d62728;'>███</span> |
| **1HOSTS_LITE** | Aggregated/Wildcard | 6 | **Medium 🟨** | **Broad 🟩** | 92,444 | **71.69%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#2ca02c;'>███</span> |
| **OISD_BIG** | Aggregated/Wildcard | 5 | **High 🟥** | **Broad 🟩** | 216,323 | **39.43%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#1f77b4;'>███</span> |
| **ADGUARD_BASE** | ABP Rule List | 5 | **Medium 🟨** | **Medium 🟨** | 119,995 | **56.13%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#17becf;'>███</span> |
| **ANUDEEP_ADSERVERS** | Specialized (Ads) | 4 | **High 🟥** | **Specialized 🟦** | 42,347 | **5.62%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#9467bd;'>███</span> |
| **STEVENBLACK_HOSTS** | Hosts File (Legacy) | 3 | **High 🟥** | **Medium 🟨** | 88,075 | **17.43%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#ff7f0e;'>███</span> |
| **ADAWAY_HOSTS** | Specialized (Ads) | 3 | **Low 🟩** | **Specialized 🟦** | 6,540 | **37.13%** | <span style='color:green;'>`+0.0%`</span> | <span style='color:#8c564b;'>███</span> |

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
| **1** | 371,821 | **69.95%** |

---

## 🔬 Domain Property Analysis (DPA)
A 'nerd-out' deep-dive into the *properties* of the domains being blocked.

### 1. Final Priority List Composition
Analysis of all domains in the final `priority_list.txt` list.

**Top 15 TLDs in `priority_list.txt`:**
| Rank | TLD | Domain Count | % of Priority List |
| :---: | :--- | :---: | :---: |
| 1 | **.com** | 63,348 | 48.76% |
| 2 | **.net** | 7,384 | 5.68% |
| 3 | **.shop** | 3,628 | 2.79% |
| 4 | **.top** | 3,417 | 2.63% |
| 5 | **.de** | 2,881 | 2.22% |
| 6 | **.click** | 2,416 | 1.86% |
| 7 | **.online** | 2,099 | 1.62% |
| 8 | **.site** | 2,033 | 1.56% |
| 9 | **.org** | 1,839 | 1.42% |
| 10 | **.ru** | 1,821 | 1.40% |
| 11 | **.space** | 1,441 | 1.11% |
| 12 | **.xyz** | 1,401 | 1.08% |
| 13 | **.io** | 1,386 | 1.07% |
| 14 | **.pro** | 1,337 | 1.03% |
| 15 | **.store** | 1,258 | 0.97% |

**Domain Properties:**
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. Domain Entropy** | `2.795` | 'Randomness' score. (Higher = more 'random', e.g., DGA) |
| **Top 5 Trigrams** | `ing`, `ion`, `ent`, `ter`, `ont` | Common 3-letter strings in domain names. |

**Domain Depth (Subdomains):**
| Depth | Domain Count | % of Priority List | Example |
| :---: | :---: | :---: | :--- |
| 1 (e.g., d.d) | 85,586 | 65.87% | `google.com` |
| 2 (e.g., d.d.d) | 37,573 | 28.92% | `ads.google.com` |
| 3 (e.g., d.d.d.d) | 5,463 | 4.20% | `sub.ads.google.com` |
| 4 (e.g., d.d.d.d.d) | 1,003 | 0.77% | `sub.ads.google.com` |
| 5 (e.g., d.d.d.d.d.d) | 220 | 0.17% | `sub.ads.google.com` |
| 6 (e.g., d.d.d.d.d.d.d) | 57 | 0.04% | `sub.ads.google.com` |
| 7 (e.g., d.d.d.d.d.d.d.d) | 4 | 0.00% | `sub.ads.google.com` |
| 8 (e.g., d.d.d.d.d.d.d.d.d) | 15 | 0.01% | `sub.ads.google.com` |
| 9 (e.g., d.d.d.d.d.d.d.d.d.d) | 2 | 0.00% | `sub.ads.google.com` |

### 2. New Domain Threat Analysis
Analysis of the **98,689** domains *added* to the list this run.
| Property | Value | Insight |
| :--- | :---: | :--- |
| **Avg. *New* Domain Entropy** | `2.737` | 'Randomness' of *new* threats. A spike here is bad. |
| **Top 5 *New* Trigrams** | `ing`, `ion`, `tra`, `ent`, `tel` | Shows the 'shape' of new attack campaigns. |

---

## 📈 Interactive Visualization





See `historical_trends_chart.png`, `score_distribution_chart.png`, and `jaccard_heatmap.png`.
The old `historical_trend_chart.png` only shows total domains. The new **`historical_trends_chart.png`** is a full dashboard.