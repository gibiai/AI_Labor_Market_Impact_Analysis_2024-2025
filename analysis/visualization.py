# analysis/visualization.py
# Task 2 - Data Visualization
# Create 6 charts + 1 animated GIF from the cleaned AI jobs dataset

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import os
 
# global settings for all charts
plt.rcParams["figure.dpi"] = 100
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["font.size"] = 11
sns.set_theme(style="whitegrid")
 
os.makedirs("output", exist_ok=True)

# load cleaned dataset
df = pd.read_csv("data/processed/ai_jobs_clean.csv")
print("Dataset loaded:", df.shape)

# career order used in multiple charts
experience_order = ["Junior", "Mid", "Senior", "Executive"]
exp_colors = {
    "Junior":    "#2A9D8F",
    "Mid":       "#457B9D",
    "Senior":    "#E9C46A",
    "Executive": "#E63946",
}

# ---- CHART 1 - Salary distribution by experience level ----
# Business question: how much does salary grow with experience?

fig, graph = plt.subplots(figsize=(10, 5))
sns.boxplot(
    data = df,
    x = "experience_level",
    y = "salary_usd",
    hue = "experience_level",
    order = experience_order,
    palette = list(exp_colors.values()),
    legend = False,
    ax = graph,
)

graph.set_title("Salary Distribution by Experience Level", fontsize=13, fontweight="bold")
graph.set_xlabel("Experience Level")
graph.set_ylabel("Salary (USD)")
# Format Y-axis as USD currency with thousands separator (e.g., $1,000,000)
graph.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.savefig("output/01_salary_by_experience.png", bbox_inches="tight")
plt.close()
print("Chart 1 saved")

# ---- CHART 2 - Top 10 countries by average salary ----
# Business question: wich locations pay the most?

top_countries = (
    df.groupby("company_location")["salary_usd"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
top_countries.columns = ["country", "avg_salary"]
 
fig, graph2 = plt.subplots(figsize=(10, 5))
graph2.barh(top_countries["country"], top_countries["avg_salary"], color="#457B9D")
 
for i, val in enumerate(top_countries["avg_salary"]):
    graph2.text(val + 500, i, f"${val:,.0f}", va="center", fontsize=9)
 
graph2.set_title("Top 10 Countries by Average Salary", fontsize=13, fontweight="bold")
graph2.set_xlabel("Average Salary (USD)")
graph2.set_ylabel("")
# invert_yaxis puts highest value at top instead of bottom
graph2.invert_yaxis()
# Format x-axis as USD currency with thousands separator (e.g., $1,000,000)
graph2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.tight_layout()
plt.savefig("output/02_top_countries_salary.png", bbox_inches="tight")
plt.close()
print("Chart 2 saved")

# ---- CHART 3 - Salary by remote work type ----
# Business question: does remote work affect salary?

fig, graph3 = plt.subplots(figsize=(8, 5))
# violinplot shows the full distribution shape, not just quartiles like boxplot
sns.violinplot(
    data    = df,
    x       = "remote_label",
    y       = "salary_usd",
    hue     = "remote_label",
    order   = ["On-Site", "Hybrid", "Remote"],
    palette = ["#E63946", "#E9C46A", "#2A9D8F"],
    legend  = False,
    ax      = graph3,
)
 
graph3.set_title("Salary Distribution by Work Mode", fontsize=13, fontweight="bold")
graph3.set_xlabel("Work Mode")
graph3.set_ylabel("Salary (USD)")
graph3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.tight_layout()
plt.savefig("output/03_salary_by_remote.png", bbox_inches="tight")
plt.close()
print("Chart 3 saved")

# ---- CHART 4 - Top 10 job titles by average salary ----
# Business question: which roles pay the most?
 
top_titles = (
    df.groupby("job_title")["salary_usd"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
top_titles.columns = ["job_title", "avg_salary"]
 
fig, graph4 = plt.subplots(figsize=(10, 6))
 
graph4.barh(top_titles["job_title"], top_titles["avg_salary"], color="#2A9D8F")
# Add salary value labels at the end of each horizontal bar (e.g., $85,000) 
for i, val in enumerate(top_titles["avg_salary"]):
    graph4.text(val + 500, i, f"${val:,.0f}", va="center", fontsize=9)
 
graph4.set_title("Top 10 Job Titles by Average Salary", fontsize=13, fontweight="bold")
graph4.set_xlabel("Average Salary (USD)")
graph4.set_ylabel("")
# invert_yaxis puts highest value at top instead of bottom
graph4.invert_yaxis()
graph4.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.tight_layout()
plt.savefig("output/04_top_job_titles.png", bbox_inches="tight")
plt.close()
print("Chart 4 saved")

# ---- CHART 5 - Years of experience vs salary (scatter + trend line)
# Business question: how strong is the experience-salary relationship?

fig, graph5 = plt.subplots(figsize=(10, 5))
 
for level in experience_order:
    subset = df[df["experience_level"] == level]
    graph5.scatter(
        subset["years_experience"],
        subset["salary_usd"],
        label  = level,
        color  = exp_colors[level],
        alpha  = 0.3,
        s      = 15,
    )
 
# trend line — linear regression using np.polyfit
x = df["years_experience"].values
y = df["salary_usd"].values
m, q   = np.polyfit(x, y, 1)
x_line = np.linspace(x.min(), x.max(), 100)
y_line = m * x_line + q

# Plot dashed trend line showing yearly salary growth rate (Trend ($5,000/year)) 
graph5.plot(x_line, y_line, color="black", linewidth=2,
        linestyle="--", label=f"Trend (~${m:,.0f}/year)")
 
graph5.set_title("Years of Experience vs Salary", fontsize=13, fontweight="bold")
graph5.set_xlabel("Years of Experience")
graph5.set_ylabel("Salary (USD)")
graph5.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
graph5.legend(loc="upper left")
plt.tight_layout()
plt.savefig("output/05_experience_vs_salary.png", bbox_inches="tight")
plt.close()
print("Chart 5 (PNG) saved")

# ---- CHART 5 - animated gif - experience levels appear one by one ───────────────────────
# FuncAnimation calls update() once per frame
# each frame adds one experience level to the scatter plot

fig, gif = plt.subplots(figsize=(10, 5))
 
def update(frame):
    gif.clear()
    # show levels up to current frame
    levels_visible = experience_order[:frame + 1]
    for level in levels_visible:
        subset = df[df["experience_level"] == level]
        gif.scatter(
            subset["years_experience"],
            subset["salary_usd"],
            label  = level,
            color  = exp_colors[level],
            alpha  = 0.3,
            s      = 15,
        )
    gif.set_title("Years of Experience vs Salary", fontsize=13, fontweight="bold")
    gif.set_xlabel("Years of Experience")
    gif.set_ylabel("Salary (USD)")
    gif.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    gif.set_xlim(0, df["years_experience"].max() + 1)
    gif.set_ylim(0, df["salary_usd"].max() * 1.05)
    gif.legend(loc="upper left")
    plt.tight_layout()
 
ani = animation.FuncAnimation(
    fig,
    update,
    frames   = len(experience_order),
    interval = 1000,
    repeat   = False,
)
 
ani.save("output/05_experience_vs_salary.gif", writer="pillow", fps=1)
plt.close()
ani._fig = None
print("Chart 5 (GIF) saved")
 
# ---- CHART 6 - Dashboard: 2x2 summary
# Business question: overall market snapshot

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("AI Job Market — Executive Dashboard", fontsize=16, fontweight="bold")
 
# top-left: average salary by experience
salary_exp = (
    df.groupby("experience_level")["salary_usd"]
    .mean()
    .reindex(experience_order)
)
axes[0, 0].bar(
    salary_exp.index,
    salary_exp.values,
    color=list(exp_colors.values()),
)
axes[0, 0].set_title("Avg Salary by Experience")
axes[0, 0].set_ylabel("USD")
axes[0, 0].yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, _: f"${x/1000:.0f}K")
)
 
# top-right: job count by company size
size_counts = df["company_size"].value_counts()
axes[0, 1].pie(
    size_counts.values,
    labels     = size_counts.index,
    autopct    = "%1.1f%%",
    colors     = ["#E63946", "#457B9D", "#2A9D8F"],
    startangle = 90,
)
axes[0, 1].set_title("Jobs by Company Size")
 
# bottom-left: average salary by work mode
remote_avg = df.groupby("remote_label")["salary_usd"].mean()
axes[1, 0].bar(
    remote_avg.index,
    remote_avg.values,
    color=["#E9C46A", "#457B9D", "#2A9D8F"],
)
axes[1, 0].set_title("Avg Salary by Work Mode")
axes[1, 0].set_ylabel("USD")
axes[1, 0].yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, _: f"${x/1000:.0f}K")
)
 
# bottom-right: overall salary distribution
sns.histplot(data=df, x="salary_usd", bins=40, color="#457B9D", ax=axes[1, 1])
axes[1, 1].set_title("Overall Salary Distribution")
axes[1, 1].set_xlabel("Salary (USD)")
axes[1, 1].xaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, _: f"${x/1000:.0f}K")
)
 
plt.tight_layout()
plt.savefig("output/06_dashboard.png", bbox_inches="tight")
plt.close()
print("Chart 6 saved")
 
print("\nAll charts saved to output/")