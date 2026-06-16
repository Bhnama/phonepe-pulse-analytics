<div align="center">

<img src="https://img.shields.io/badge/PhonePe-Pulse%20Analytics-5f4bb6?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyem0tMSAxNHYtNEg3bDUtOXY0aDRsLTUgOXoiLz48L3N2Zz4=" alt="PhonePe"/>

# 💜 PhonePe Pulse — India Digital Payments Analytics

**A full-stack data analytics project: EDA · Interactive Dashboard · ML Forecast · SQL Explorer**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-5.20-3F4F75?style=flat-square&logo=plotly&logoColor=white)](https://plotly.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Streamlit_Cloud-FF4B4B?style=flat-square)](https://your-app-name.streamlit.app)

<br/>

> **Analyzing 3 years of PhonePe transaction data across 28+ Indian states, 700+ districts,  
> and 14 quarters — from Q1 2018 to Q2 2021.**

</div>

---

## 🎯 Project Highlights

| Feature | Description |
|---|---|
| 🗺️ **India Choropleth Map** | State-wise transaction volume visualized on an animated India map |
| 📊 **Interactive EDA** | Filter by state, year, quarter — all charts update live |
| 🎬 **Animated Bar Race** | Watch state rankings evolve quarter by quarter |
| 🤖 **ML Forecast** | Polynomial regression predicts future transaction volumes |
| 🗄️ **SQL Explorer** | Write and run live SQL queries on the dataset in the browser |
| 💜 **Dark UI** | Professional dark-themed dashboard built for portfolio presentation |

---

## 📸 Dashboard Preview

> *(Screenshots will be added after deployment)*

| Overview | India Map | ML Forecast |
|---|---|---|
| KPI cards + growth trend | Choropleth + animated bar race | Regression + forecast table |

---

## 📂 Project Structure

```
phonepe-pulse-analytics/
│
├── 📊 app.py                    # Streamlit dashboard (6 pages)
├── 📓 notebooks/
│   └── PhonePe_Analysis.ipynb   # Full Jupyter notebook (Tasks 1–6)
├── 📁 data/
│   └── phonepe_data.xlsx        # Raw dataset (Q1 2018 – Q2 2021)
├── 📋 requirements.txt          # Python dependencies
└── 📖 README.md
```

---

## 🔍 Dataset Overview

The dataset contains **5 tables** spanning Q1 2018 to Q2 2021:

| Table | Description | Rows |
|---|---|---|
| `State_Txn and Users` | Transactions, amount, ATV, users by state/quarter | 504 |
| `State_TxnSplit` | Breakdown by transaction type (P2P, merchant, etc.) | 2,514 |
| `State_DeviceData` | Device brands used by registered users | 5,544 |
| `District_Txn and Users` | District-level transaction data | 10,248 |
| `District Demographics` | Population, density, area per district | 742 |

**Source:** [PhonePe Pulse](https://www.phonepe.com/pulse/) — India's largest digital payments platform

---

## 📊 Key Findings

### 📈 Explosive Growth
- Transactions grew by **~1,200%** from Q1 2018 to Q2 2021
- COVID-19 (2020) acted as a **major accelerator** — app opens surged 3× in a single year
- Total transactions crossed **2 billion** by Q2 2021

### 🏆 Top States
- **Maharashtra, Telangana, Karnataka** consistently lead in transaction volumes
- **Goa and Telangana** have the highest registered-user-to-population ratios
- North-East states show the lowest volumes but consistent upward trends

### 💳 Transaction Types
- **Peer-to-peer** payments dominate (>60% in most states)
- **Merchant payments** growing fastest year-over-year
- **Recharge & bill payments** highly consistent across all regions

### 📱 Device Landscape
- **Xiaomi** and **Samsung** have the highest PhonePe user bases
- Strong correlation between budget Android device penetration and PhonePe adoption
- Xiaomi dominant in Tier-2/3 cities; Samsung stronger in metros

### 🏙️ Demographics & Transactions
- Moderate positive correlation (r ≈ 0.35) between **population density** and transaction volume
- High-density districts (Mumbai, Bengaluru) are not always proportionally highest — **rural adoption** is significant
- Districts with HQs in major cities have 4× higher ATV than rural districts

---

## 🚀 Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/Bhnama/phonepe-pulse-analytics.git
cd phonepe-pulse-analytics
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the dashboard
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ☁️ Deploy to Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your repo → set **Main file: `app.py`**
4. Click **Deploy** — your live link is ready in ~2 minutes!

---

## 🧪 Notebook Walkthrough

The Jupyter notebook covers all 6 tasks:

| Task | Topic |
|---|---|
| Task 1 | Data loading, structure, missing values, summary stats |
| Task 2 | EDA — state trends, transaction types, device brands, ATV |
| Task 3 | Data quality — cross-validating state vs district totals |
| Task 4 | Advanced merging — user/population ratio, density correlation |
| Task 5 | Visualizations — line plots, pie charts, choropleth maps |
| Task 6 | Insights, correlation heatmap, actionable recommendations |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Data Processing** | `pandas`, `numpy` |
| **Visualization** | `plotly` (interactive), `matplotlib`, `seaborn` |
| **Machine Learning** | `scikit-learn` (Polynomial Regression) |
| **Database** | `SQLite` (in-memory via `sqlite3`) |
| **Dashboard** | `Streamlit` |
| **Deployment** | Streamlit Cloud (free tier) |

---

## 💡 Skills Demonstrated

```
✅ Data loading & cleaning          ✅ Exploratory data analysis
✅ Multi-table merging & joins       ✅ Statistical correlation analysis
✅ Interactive Plotly visualizations  ✅ Choropleth mapping
✅ Animated bar race charts          ✅ Machine learning (regression)
✅ SQL queries on real data          ✅ Streamlit web app development
✅ GitHub portfolio presentation     ✅ Business insight extraction
```

---

## 📬 Connect

**Made with 💜 for the Coding Ninjas Python Module Case Study**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat-square&logo=linkedin)](https://linkedin.com/in/YOUR_PROFILE)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github)](https://github.com/YOUR_USERNAME)

---

<div align="center">
<sub>⭐ If this project helped you, please star the repo — it helps others find it!</sub>
</div>
