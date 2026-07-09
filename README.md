# Marketing Funnel & Conversion Performance Analysis

**Future Interns – Data Science & Analytics, Task 3**

An analysis of a bank's telemarketing campaign, tracking how contacted customers move through a 3-stage funnel — **Contacted → Engaged → Converted** — to identify where leads drop off and which segments convert best.

🔗 **Live Dashboard:** https://futureds03-dncyzv6liykte3qbeepxkv.streamlit.app/
📊 **Dataset:** [Bank Marketing Dataset (UCI)](https://archive.ics.uci.edu/dataset/222/bank+marketing)

---

## 📌 Objective

Analyze a marketing/lead funnel to answer:
- Where are users dropping off?
- Which channels and segments bring high-quality leads?
- What actions would improve conversion rates?

## 🧹 Methodology

**Data cleaning:**
- Started with 41,188 records across 21 features
- Removed rows containing `"unknown"` values in `job`, `marital`, `education`, `default`, `housing`, or `loan` — 30,488 rows (74%) retained for analysis
- Converted the `pdays` placeholder value (999 = "never previously contacted") into a clean boolean flag

**Funnel definition:**
Since this is a phone campaign rather than a website, the funnel was defined as:

| Stage | Definition |
|---|---|
| 1. Contacted | Every customer called during the campaign |
| 2. Engaged | Call duration at or above the median (181 seconds) — a proxy for a genuine conversation vs. an immediate hang-up |
| 3. Converted | Subscribed to the product, **and** was already counted as Engaged (each stage is a true subset of the one before it) |

## 📊 Key Findings

**Overall funnel:**

| Stage | Count | % of Previous | % of Total |
|---|---|---|---|
| Contacted | 30,488 | — | 100% |
| Engaged | 15,245 | 50.0% | 50.0% |
| Converted | 3,361 | 22.0% | 11.0% |

**By channel** — cellular substantially outperforms telephone, and the gap is concentrated in the engaged→converted step, not the initial contact:

| Channel | Engage Rate | Convert Rate (of Engaged) | Overall Rate |
|---|---|---|---|
| Cellular | 50.7% | 27.3% | **13.8%** |
| Telephone | 48.5% | 10.9% | **5.3%** |

**By month** — a clear volume-vs-quality tradeoff. High-volume months convert far worse than low-volume months:

| Volume tier | Months | Overall Conversion |
|---|---|---|
| High volume | May, Jun, Jul, Aug, Nov | 6.9% – 10.7% |
| Low volume | Mar, Sep, Oct, Dec | 34.1% – 42.0% |

May alone accounts for ~32% of all contacts but converts at just 6.9% — the campaign's lowest rate.

**By job** — students and retirees convert best; blue-collar workers convert worst:

| Job | Overall Conversion |
|---|---|
| Student | 26.9% |
| Retired | 23.1% |
| Unemployed | 15.2% |
| Admin | 11.9% |
| *(mid-tier roles)* | 8.4% – 11.2% |
| Blue-collar | 7.4% |

**By education** — a flatter spread than job, with university degree holders converting best among statistically meaningful groups:

| Education | Overall Conversion |
|---|---|
| University degree | 12.6% |
| Basic (4y) | 11.6% |
| Professional course | 10.9% |
| High school | 10.8% |
| Basic (6y) | 9.0% |
| Basic (9y) | 8.2% |

*(Illiterate shows 18.2% but only reflects 11 people — too small a sample to act on.)*

## ✅ Recommendations

1. **Shift call volume toward cellular contacts.** The overall conversion rate is 2.6x higher than telephone, driven by conversation quality once someone answers — not by answer rate. Reallocating telephone-channel effort to cellular is the single highest-leverage change available.

2. **Investigate May's lead quality.** May drives a third of all campaign volume but converts at the campaign's lowest rate (6.9%). Either the leads called in May are lower-quality, or high-volume months are diluting call quality (e.g. less time per call, less-targeted lists). Worth a focused review before the next campaign cycle.

3. **Prioritize students and retirees as target segments.** These two groups convert 2–2.5x above the overall average. A smaller, more targeted campaign toward these segments would likely be more efficient than broad outreach.

4. **Re-time the campaign toward low-volume months' conditions.** Mar, Sep, Oct, and Dec convert 3–4x higher than the high-volume months. If the operational goal allows it, testing whether spreading contact volume more evenly across the year (rather than concentrating in May–Aug) improves overall performance would be a valuable follow-up experiment.

5. **De-prioritize blue-collar outreach relative to other segments**, or test a different pitch/offer for this group specifically, since the current approach converts here at roughly half the rate of the top segments.

## 🛠️ Tools Used

- **Python** (pandas) — data cleaning and funnel calculations
- **Plotly** — funnel diagram
- **Matplotlib** — static charts
- **Streamlit** — interactive dashboard with live filtering

## 📁 Repository Structure

```
├── dashboard.py          # Streamlit interactive dashboard
├── analysis.ipynb        # Full exploratory analysis & cleaning steps
├── requirements.txt      # Python dependencies
├── data/
│   └── bank_clean.csv    # Cleaned dataset with funnel stage flags
├── charts/                # Static exported charts (PNG)
└── README.md
```

## ▶️ Running Locally

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```
