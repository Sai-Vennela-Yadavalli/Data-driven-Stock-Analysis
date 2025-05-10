# Data-driven-Stock-Analysis
Mini project for stock performance analytics using Python, Streamlit, and Power BI
# 📈 Data-Driven Stock Analysis

A complete stock analytics project using Python, Streamlit, and Power BI. Built as a mini-project for Guvi's Data Science program, this project analyses Nifty 50 stocks and presents the insights through interactive visualisations.

---

## 📁 Project Structure

```
Data-Driven-Stock-Analysis/
├── app.py                        # Streamlit dashboard app
├── prepare_data.py              # Script to process and save data
├── Sector_data - Sheet1.csv     # Sector mapping file
├── stock_csvs/                  # Raw daily YAML-converted stock CSVs
├── data/                        # Auto-generated data for visualisation
└── README.md                    # This file
```

---

## 🚀 Features

* ✅ Extracts and transforms YAML stock data into clean CSVs
* 📈 Calculates yearly return, volatility, and cumulative return
* 🏢 Performs sector-wise analysis
* 📊 Interactive dashboards in **Streamlit**
* 📉 Data visualizations in **Power BI**
* 🔗 Correlation heatmaps between stock prices
* 📅 Monthly top gainers and losers

---

## 🛠️ Tech Stack

* **Python** 🐍 (Pandas, Matplotlib, Seaborn)
* **Streamlit** 🌐 (dashboard UI)
* **Power BI** 📊 (interactive reporting)
* **Git & GitHub** 💻 (version control)

---

## ▶️ How to Run

### 1️⃣ Clone the Repo

```bash
git clone (https://github.com/Sai-Vennela-Yadavalli/Data-driven-Stock-Analysis.git)
cd Data-driven-Stock-Analysis
```


### 2️⃣ Install Requirements

```bash
pip install -r requirements.txt  # Or manually install: pandas, numpy, matplotlib, seaborn, streamlit
```

### 3️⃣ Prepare the Data

```bash
python prepare_data.py
```

### 4️⃣ Launch the Dashboard

```bash
streamlit run app.py
```

🧠 Visit: `http://localhost:8501`

---

## 📊 Power BI Report

All data in `/data/` can be used to build Power BI dashboards:

* Bar charts for top gainers/losers
* Sector-wise comparisons
* Monthly return slicers

---

## 📝 Credits

* 💻 Developed by Sai Vennela Yadavalli
* 🎓 Guvi Mini Project (Data Science Program)
* 📦 Stock data based on YAML sources provided

---

## 🔗 Connect

* 💬 For questions, contact me on (https://www.linkedin.com/in/sai-vennela-yadavalli-8b854432a/)

---

### ⭐ If you like this project, don’t forget to star it!
