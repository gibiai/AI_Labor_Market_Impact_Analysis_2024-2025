# analysis/sql_analysis.py
# Task 3 — SQL Analysis using SQLite in-memory database
#
# SQLite is a lightweight database that runs entirely in memory —
# no server needed. We load the cleaned DataFrame as a SQL table,
# then run real SQL queries and get results back as DataFrames.

import pandas as pd
import sqlite3
import os
os.makedirs("output", exist_ok=True)

# load cleaned dataset
df = pd.read_csv("data/processed/ai_jobs_clean.csv")
print("Dataset loaded:", df.shape)

# crete in-memory SQLite database
# ":memory:" creates the database in RAM — no file is saved to disk
# when the script ends, the database is gone
conn = sqlite3.connect(":memory:")

# load DataFrame into the database as a table named "ai_jobs"
# index=False -> don't include the pandas row index as a column
df.to_sql("ai_jobs", conn, index=False, if_exists="replace")
print("Table 'ai_jobs' created in SQLite\n")

print("-" * 40)
print("SQL Analysis - 6 Queries")
print("-" * 40)

# Q1: vaerage salary by experience level
# GROUP BY groups all rows with the same experience_level
# AVG calculates the average salary for each group
# ORDER BY sorts from highest to lowest
q1 = pd.read_sql("""
    SELECT
        experience_level,
        ROUND(AVG(salary_usd), 0)  AS avg_salary,
        ROUND(MIN(salary_usd), 0)  AS min_salary,
        ROUND(MAX(salary_usd), 0)  AS max_salary,
        COUNT(*)                   AS job_count
    FROM ai_jobs
    GROUP BY experience_level
    ORDER BY avg_salary DESC
""", conn)
 
print("\nQ1 — Average salary by experience level:")
print(q1.to_string(index=False))

# Q2: Top 10 countries by average salary
# same pattern — GROUP BY country, order by average salary
q2 = pd.read_sql("""
    SELECT
        company_location            AS country,
        ROUND(AVG(salary_usd), 0)  AS avg_salary,
        COUNT(*)                   AS job_count
    FROM ai_jobs
    GROUP BY company_location
    ORDER BY avg_salary DESC
    LIMIT 10
""", conn)
 
print("\nQ2 — Top 10 countries by average salary:")
print(q2.to_string(index=False))

# Q3: remote work distribution and salary impact
# shows how many jobs are remote/hybrid/on-site and if salary differs
 
q3 = pd.read_sql("""
    SELECT
        remote_label,
        COUNT(*)                   AS job_count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM ai_jobs), 1) AS pct,
        ROUND(AVG(salary_usd), 0)  AS avg_salary
    FROM ai_jobs
    GROUP BY remote_label
    ORDER BY job_count DESC
""", conn)
 
print("\nQ3 — Remote work distribution and salary impact:")
print(q3.to_string(index=False))

# Q4: Top 10 job titles by average salary
# HAVING filters groups AFTER GROUP BY — same concept as in Pandas
# here we use it to exclude job titles with fewer than 50 postings
# to avoid averages based on very few data points
q4 = pd.read_sql("""
    SELECT
        job_title,
        ROUND(AVG(salary_usd), 0)  AS avg_salary,
        COUNT(*)                   AS job_count
    FROM ai_jobs
    GROUP BY job_title
    HAVING COUNT(*) >= 50
    ORDER BY avg_salary DESC
    LIMIT 10
""", conn)
 
print("\nQ4 — Top 10 job titles by average salary (min 50 postings):")
print(q4.to_string(index=False))
# ── Q5: salary by experience level AND company size ──────────────────────────
# two GROUP BY columns — creates one row for each combination
# this is like a pivot table but in SQL
 
q5 = pd.read_sql("""
    SELECT
        experience_level,
        company_size,
        ROUND(AVG(salary_usd), 0)  AS avg_salary,
        COUNT(*)                   AS job_count
    FROM ai_jobs
    GROUP BY experience_level, company_size
    ORDER BY experience_level, avg_salary DESC
""", conn)
 
print("\nQ5 — Salary by experience level and company size:")
print(q5.to_string(index=False))
 
# Q6: Senior and Executive roles paying above market average 
# subquery: the inner SELECT calculates the overall average salary
# the outer WHERE uses that result to filter rows
# this is a common pattern in real SQL analysis
q6 = pd.read_sql("""
    SELECT
        job_title,
        experience_level,
        company_location,
        salary_usd,
        employment_type
    FROM ai_jobs
    WHERE experience_level IN ('Senior', 'Executive')
      AND salary_usd > (SELECT AVG(salary_usd) FROM ai_jobs)
    ORDER BY salary_usd DESC
    LIMIT 15
""", conn)
 
print("\nQ6 — Senior/Executive roles above market average salary (top 15):")
print(q6.to_string(index=False))
 
 
# save results to CSV 
q1.to_csv("output/sql_q1_salary_by_experience.csv", index=False)
q2.to_csv("output/sql_q2_top_countries.csv",        index=False)
q4.to_csv("output/sql_q4_top_job_titles.csv",       index=False)
print("\nSQL results saved to output/")
 
# close connection
conn.close()
print("SQLite connection closed.")