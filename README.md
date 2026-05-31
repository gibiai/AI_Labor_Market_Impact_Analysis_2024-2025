<div align="center">
  <img src="assets/logo.png" alt="AI Jobs Market Analysis" width="60%"/>
</div>

# 💼 AI Jobs Market Analysis & Salary Prediction
### Data-Driven Insights into the AI Revolution in the Job Market

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-red.svg)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow.svg)
![Status](https://img.shields.io/badge/Status-Complete-success.svg)

AI Labor Market Impact Analysis 🤖

> End-to-end data analysis of the global AI job market — salary trends, remote work patterns, and a machine learning model to predict compensation.

---

## Description

This project analyzes 15,000 AI job postings from 2024-2025 across 50+ countries to understand what drives salaries in the artificial intelligence sector. The pipeline covers data cleaning and EDA, SQL analysis with SQLite, data visualization with Matplotlib and Seaborn, and a Random Forest model that predicts salary with R² = 0.62. Key finding: years of experience and seniority level together account for 65% of salary variance, while remote work has virtually no impact on compensation.

---

## Project Structure

```
AI_Labor_Market_Impact_Analysis/
│
├── dati/
│   ├── ai_job_dataset1.csv          # raw dataset (15,000 rows)
│   └── processed/
│       └── ai_jobs_clean.csv        # cleaned dataset (23 columns)
│
├── analisi/
│   ├── cleaning_eda.py              # Task 1 — data cleaning & EDA
│   ├── sql_analysis.py              # Task 2 — SQL analysis via SQLite
│   ├── visualization.py             # Task 3 — charts & animated GIF
│   └── ml_model.py                  # Task 4 — Random Forest model
│
├── output/                          # all charts, GIFs and CSV results
├── main.py                          # entry point — runs everything in order
├── requirements.txt
└── .gitignore
```

---

## Installation & Usage

**1. Clone the repository**
```bash
git clone https://github.com/gibiai/AI_Labor_Market_Impact_Analysis_2020-2024.git
cd AI_Labor_Market_Impact_Analysis_2020-2024
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the full pipeline**
```bash
python3 main.py
```

**Or run each module individually in order:**
```bash
python3 analisi/cleaning_eda.py
python3 analisi/sql_analysis.py
python3 analisi/visualization.py
python3 analisi/ml_model.py
```

---

## Dependencies

```
numpy>=1.24
pandas>=2.0
matplotlib>=3.7
seaborn>=0.12
scikit-learn>=1.3
pillow>=10.0
```

---

## Output

### Charts

**Chart 1 — Salary Distribution by Experience Level**
> *How much does compensation grow with seniority?*

![Salary by experience](output/01_salary_by_experience.png)

---

**Chart 2 — Top 10 Countries by Average Salary**
> *Which locations offer the highest AI salaries?*

![Top countries](output/02_top_countries_salary.png)

---

**Chart 3 — Salary by Work Mode**
> *Does remote work actually pay more?*

![Remote salary](output/03_salary_by_remote.png)

---

**Chart 4 — Top 10 Job Titles by Average Salary**
> *Which AI roles command the highest compensation?*

![Top job titles](output/04_top_job_titles.png)

---

**Chart 5 — Years of Experience vs Salary**
> *How strong is the experience-salary relationship?*

![Experience vs salary](output/05_experience_vs_salary.png)

**Animated version:**

![Experience vs salary GIF](output/05_experience_vs_salary.gif)

---

**Chart 6 — Executive Dashboard**
> *Overall market snapshot across key dimensions.*

![Dashboard](output/06_dashboard.png)

---

**Chart 7 — Feature Importance**
> *What actually drives salary predictions?*

![Feature importance](output/07_feature_importance.png)

---

**Chart 8 — Actual vs Predicted Salary**
> *How accurate is the Random Forest model?*

![Actual vs predicted](output/08_actual_vs_predicted.png)

---

### CSV Results

| File | Description |
|------|-------------|
| `output/sql_q1_salary_by_experience.csv` | Average salary by experience level |
| `output/sql_q2_top_countries.csv` | Top countries by salary |
| `output/sql_q4_top_job_titles.csv` | Top job titles by salary |
| `output/feature_importance.csv` | Random Forest feature importance scores |
| `output/model_results.csv` | R², MAE, RMSE summary |

---

## Key Findings

| Finding | Value |
|---------|-------|
| **Top paying country** | Switzerland ($173K avg) |
| **Executive vs Junior gap** | $198K vs $67K — 3x difference |
| **Remote work salary impact** | Virtually none ($122K Remote vs $121K On-Site) |
| **Most predictive feature** | Years of experience (35.6% importance) |
| **Model R²** | 0.62 — explains 62% of salary variance |
| **Model MAE** | $27,066 average prediction error |

---

## Techniques Used

| Area | Techniques |
|------|-----------|
| **Python** | Pandas, NumPy, type hints, list comprehension |
| **SQL** | SQLite in-memory, GROUP BY, HAVING, subqueries |
| **Visualization** | Matplotlib, Seaborn, FuncAnimation, violinplot |
| **Machine Learning** | Label Encoding, train/test split, Random Forest, feature importance, R²/MAE/RMSE |

---

## 📊 Power BI Dashboard
The interactive dashboard allows you to explore these results dynamically:

**Interactive Dashboard:**
[![Power BI](https://img.shields.io/badge/Power%20BI-View%20Dashboard-yellow?logo=powerbi)](https://app.powerbi.com/view?r=eyJrIjoiZTRlODg4OGQtMWY1ZC00OTUzLThjODgtZjQ2ZTBlZDQzMTI3IiwidCI6IjFmNTRhMThlLTg0MjUtNDdiYi1hMDk3LTczODg2ZTM1MTE4YSIsImMiOjh9)
<sup>↗️ *Ctrl+click to open in a new tab*</sup>

---

## Author

**Gabriele De Carlo** — Data Analyst Portfolio Project, 2025
Dataset: [Global AI Job Market & Salary Trends 2025](https://www.kaggle.com/datasets/bismasajjad/global-ai-job-market-and-salary-trends-2025) — Kaggle

[!note that this is a synthetically generated dataset designed to reflect realistic AI job market patterns!]
