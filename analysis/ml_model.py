# analysis/ml_model.py
# Task 4 — Machine Learning Model
# Predicts salary_usd using Random Forest
# Also shows which features impact salary the most (feature importance)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import os

np.random.seed(42)
os.makedirs("output", exist_ok=True)
 
plt.rcParams["figure.dpi"] = 100
plt.rcParams["figure.facecolor"] = "white"
sns.set_theme(style="whitegrid")

# load cleaned dataset
df = pd.read_csv("data/processed/ai_jobs_clean.csv")
print("Dataset loaded:", df.shape)

# FEATURE SELECTION
# choose which columns to use as input (features) for the model
# we exclude: job_id (unique ID, no predictive value), salary_local
# (too correlated with salary_usd), salary_bracket (derived from target),
# posting_date / application_deadline (use days_open instead)

features = [
    "experience_level",      # Junior / Mid / Senior / Executive
    "employment_type",       # Full-Time / Part-Time / Contract / Freelance
    "company_size",          # Small / Medium / Large
    "remote_ratio",          # 0 / 50 / 100
    "years_experience",      # numeric — how many years of experience
    "education_required",    # Bachelor / Master / PhD
    "benefits_score",        # numeric score for benefits package
    "days_open",             # how many days the posting was open
]
 
target = "salary_usd"   # what we want to predict
 
df_model = df[features + [target]].copy()

# LABEL ENCODING
# Machine learning models only understand numbers — not strings like "Junior"
# LabelEncoder converts each unique string value to an integer
# "Executive"→0, "Junior"→1, "Mid"→2, "Senior"→3 (alphabetical order)
# we save the encoder for each column so we can decode later if needed

# identify which columns contain strings (object dtype)
categorical_cols = df_model.select_dtypes(include=["object"]).columns.tolist()
print(f"\nCategorical columns to encode: {categorical_cols}")
 
encoders = {}   # store one encoder per column
 
for col in categorical_cols:
    le = LabelEncoder()                    # create a new encoder for this column
    df_model[col] = le.fit_transform(df_model[col])   # fit and transform in one step
    encoders[col] = le                     # save encoder in case we need it later
    print(f"  {col}: {dict(zip(le.classes_, le.transform(le.classes_)))}")

# TRAIN / TEST SPLIT
# we split the dataset into two parts:
# - training set (80%): the model learns from this data
# - test set (20%): we evaluate the model on data it has never seen
# test_size=0.2 means 20% goes to test, 80% to train
# random_state=42 ensures the split is always the same

X = df_model[features]   # input features — everything except salary
y = df_model[target]     # target — salary_usd
 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
 
print(f"\nTraining set: {X_train.shape[0]} rows")
print(f"Test set:     {X_test.shape[0]} rows")

# RANDOM FOREST MODEL
# Random Forest builds many decision trees and averages their predictions
# n_estimators=100 means 100 trees — more trees = more stable but slower
# random_state=42 makes results reproducible

print("\nTraining Random Forest...")
model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
# n_jobs=-1 uses all available CPU cores — speeds up training
model.fit(X_train, y_train)   # train the model on the training data
print("Training complete.")

# MODEL EVALUATION
# we predict salaries on the test set and compare with actual values
# R²: how much variance the model explains (1.0 = perfect, 0 = useless)
# MAE: average absolute error in USD — easy to interpret
# RMSE: like MAE but penalizes large errors more

y_pred = model.predict(X_test)   # predict salaries on test set
 
r2   = r2_score(y_test, y_pred)
mae  = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
 
print("\n--- Model Evaluation ---")
print(f"R²   (explained variance): {r2:.4f}")
print(f"MAE  (avg error in USD):   ${mae:,.0f}")
print(f"RMSE (penalizes outliers): ${rmse:,.0f}")

# FEATURE IMPORTANCE
# after training, Random Forest can tell us which features
# were most useful for predicting salary
# higher importance = stronger influence on the prediction
  
importance_df = pd.DataFrame({
    "feature":    features,
    "importance": model.feature_importances_,
}).sort_values("importance", ascending=False)
 
print("\n--- Feature Importance ---")
print(importance_df.to_string(index=False))

# CHART 7 — Feature importance bar chart

fig, graph7 = plt.subplots(figsize=(10, 5))
 
graph7.barh(
    importance_df["feature"],
    importance_df["importance"],
    color="#457B9D",
)
graph7.set_title("Feature Importance — What Drives Salary?",
             fontsize=13, fontweight="bold")
graph7.set_xlabel("Importance Score")
graph7.set_ylabel("")
graph7.invert_yaxis()   # most important feature at top
 
for i, val in enumerate(importance_df["importance"]):
    graph7.text(val + 0.001, i, f"{val:.3f}", va="center", fontsize=9)
 
plt.tight_layout()
plt.savefig("output/07_feature_importance.png", bbox_inches="tight")
plt.close()
print("\nChart 7 (feature importance) saved")

# CHART 8 — Actual vs Predicted salary scatter
# if the model is good, points should be close to the diagonal line

fig, graph8 = plt.subplots(figsize=(8, 6))
 
graph8.scatter(y_test, y_pred, alpha=0.2, color="#457B9D", s=10)
 
# perfect prediction line — y = x
min_val = min(y_test.min(), y_pred.min())
max_val = max(y_test.max(), y_pred.max())
graph8.plot([min_val, max_val], [min_val, max_val],
        color="red", linewidth=1.5, linestyle="--", label="Perfect prediction")
 
graph8.set_title(f"Actual vs Predicted Salary  (R² = {r2:.3f})",
             fontsize=13, fontweight="bold")
graph8.set_xlabel("Actual Salary (USD)")
graph8.set_ylabel("Predicted Salary (USD)")
graph8.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))
graph8.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))
graph8.legend()
plt.tight_layout()
plt.savefig("output/08_actual_vs_predicted.png", bbox_inches="tight")
plt.close()
print("Chart 8 (actual vs predicted) saved")

# save results
importance_df.to_csv("output/feature_importance.csv", index=False)
 
results_summary = pd.DataFrame({
    "metric": ["R²", "MAE (USD)", "RMSE (USD)"],
    "value":  [round(r2, 4), round(mae, 0), round(rmse, 0)]
})
results_summary.to_csv("output/model_results.csv", index=False)
print("Results saved to output/")