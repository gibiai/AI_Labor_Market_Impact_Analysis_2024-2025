# analysis/cleaning_eda.py
# Task 1 - Data Loading, cleaning adn explanatory analysis
# Dataset: Global AI Job Market & Salary Trends 2025 (15,000 rows)

import pandas as pd
import numpy as np
import os

np.random.seed(42)
os.makedirs("output", exist_ok=True)

print("-" * 40)
print("AI Labor Market - Loading and Cleaning")
print("-" * 40)

# load dataset
df = pd.read_csv("data/ai_job_dataset1.csv")

print(f"\nDataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
print("\n Info BEFORE cleaning:")
df.info()
print("\nFirst 5 rows:")
print(df.head())

# check missing values
print("\nMissing values:")
print(df.isnull().sum())

# standard categorical columns 
# experience_level: abbreviations -> readable labels
# EN = Entry/Junior, MI = Mid, SE = Senior, EX = Executive
experience_map = {
    "EN": "Junior",
    "MI": "Mid",
    "SE": "Senior",
    "EX": "Executive"
}
# map() replaces each value using the dictionary
df["experience_level"] = df["experience_level"].map(experience_map)

# employement_type: abbreviations -> readable labels
# FT = Full-Time, PT = Part-Time, CT = Contract, FL = Freelance
employment_map = {
    "FT": "Full-Time",
    "PT": "Part-Time",
    "CT": "Contract",
    "FL": "Freelance"
}
df["employment_type"] = df["employment_type"].map(employment_map)
 
# company_size: S/M/L → Small/Medium/Large
size_map = {"S": "Small", "M": "Medium", "L": "Large"}
df["company_size"] = df["company_size"].map(size_map)
 
# remote_ratio: 0/50/100 → On-Site/Hybrid/Remote
# creates a readable label column alongside the numeric one
remote_map = {0: "On-Site", 50: "Hybrid", 100: "Remote"}
df["remote_label"] = df["remote_ratio"].map(remote_map)

# Data conversion
# pd.to_datetime converts string "2024-01-15" into a datetime object
# without this, pandas treats dates as plain text
df["posting_date"] = pd.to_datetime(df["posting_date"])
df["application_deadline"] = pd.to_datetime(df["application_deadline"])

# derived column: how many days the job posting was open
# .dt is the accessor for datetime operations on a Series
df["days_open"] = (df["application_deadline"] - df["posting_date"]).dt.days

# salary bracket - derived column
# pd.cut splits a continuous numeric column into labeled intervals (bins)
# useful for grouping salaries in Power BI and charts
bins   = [0, 60000, 100000, 150000, 999999]
labels = ["< 60K", "60K-100K", "100K-150K", "> 150K"]
# pd.cut splits salary into labeled ranges — like if/elif but for ranges
# bins = the boundaries of each interval
# labels = the name assigned to each interval
# result: "< 60K", "60K-100K", "100K-150K", "> 150K"
df["salary_bracket"] = pd.cut(df["salary_usd"], bins=bins, labels=labels)
 
print("\n--- After standardization ---")
print(f"experience_level: {df['experience_level'].value_counts().to_dict()}")
print(f"employment_type:  {df['employment_type'].value_counts().to_dict()}")
print(f"company_size:     {df['company_size'].value_counts().to_dict()}")
print(f"remote_label:     {df['remote_label'].value_counts().to_dict()}")

# ----- EXPLORATORY DATA ANALYSIS (EDA) -----
print("-" * 40)
print("EDA - Exploratory Data Analysis")
print("-" * 40)

# general salary statistics
print("\n--- salary $ statistics ---")
print(df["salary_usd"].describe().round(2))

# salary by experience level
print("\n--- Average salary by experience level ---")
salary_exp = df.groupby("experience_level")["salary_usd"].agg(
    mean = "mean",
    median = "median",
    count = "count"
).round(0)

# reindex to show in career progression order
order = ["Junior", "Mid", "Senior", "Executive"]
salary_exp = salary_exp.reindex(order)
print(salary_exp)

# top 10 countries by average salary
print("\n--- Top 10 countries by average salary ---")
top_countries = (
    df.groupby("company_location")["salary_usd"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .round(0)
)
print(top_countries)

# salary by remote work mode
print("\n--- Average salary by work mode ---")
salary_remote = df.groupby("remote_label")["salary_usd"].agg(
    mean = "mean",
    median = "median"
).round(0)
print(salary_remote)

# salary by industry
print("\n--- Top 10 industries by average salary ---")
top_industry = (
    df.groupby("industry")["salary_usd"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .round(0)
)
print(top_industry)

# salary by company size
print("\n--- Average salary by company size ---")
salary_size = df.groupby("company_size")["salary_usd"].agg(
    mean = "mean",
    median = "median"
).round(0)
print(salary_size)

# numerical correlation with salary
# check which numeri columns correlate with salary_usd
print("\n--- Correlation with salary $ ---")
numeric_cols = ["salary_usd", "years_experience", "remote_ratio",
                "job_description_length", "benefits_score", "days_open"]
corr = df[numeric_cols].corr()["salary_usd"].drop("salary_usd").round(4)
print(corr.sort_values(ascending=False))

# save cleaned dataset
os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/ai_jobs_clean.csv", index=False, encoding="utf-8")
print("\nCleaned dataset saved to data/processed/")
print(f"Final shape: {df.shape}")
