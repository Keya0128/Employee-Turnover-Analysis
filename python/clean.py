from pathlib import Path
import pandas as pd
import numpy as np

print("=" * 60)
print("RUNNING FILE 1: DATA CLEANING & PREPARATION")
print("=" * 60)

# Setup paths and load provided raw dataset dynamically
ROOT = Path(__file__).resolve().parent.parent  
DATA_IN = ROOT / "data" / "Raw_Data.csv"
DATA_OUT = ROOT / "data" / "Clean_data.csv"


# We must actually use the pandas read_csv tool to load the DATA_IN path variable
df = pd.read_csv(DATA_IN)

print(" Running Data Quality Integrity Checks...")

# Condition A: Check and remove duplicate Employee IDs
if not df["EmployeeID"].is_unique:
    duplicate_count = df.duplicated(subset="EmployeeID").sum()
    print(f" ->  WARNING: Found {duplicate_count} duplicate rows! Removing copies...")
    df = df.drop_duplicates(subset="EmployeeID", keep="first")
else:
    print(" -> PASS: All Employee ID records are uniquely verified.")

# Condition B: Check and remove negative income bugs
if not (df["MonthlyIncome"] >= 0).all():
    negative_count = (df["MonthlyIncome"] < 0).sum()
    print(f" ->  WARNING: Found {negative_count} rows with negative income! Removing errors...")
    df = df[df["MonthlyIncome"] >= 0]
else:
    print(" -> PASS: Income fields contain zero negative calculation anomalies.")

# Condition C: Check and remove empty blank spaces in your target column
if not df["Attrition"].notna().all():
    blank_count = df["Attrition"].isna().sum()
    print(f" ->  WARNING: Found {blank_count} rows with blank Attrition fields! Removing rows...")
    df = df.dropna(subset=["Attrition"])
else:
    print(" -> PASS: Target Attrition field data is 100% complete.")

# Condition D: Check and remove broken Infinite numbers (inf) from bad calculations
if not np.isfinite(df["MonthlyIncome"]).all():
    inf_count = np.isinf(df["MonthlyIncome"]).sum()
    print(f" ->  WARNING: Found {inf_count} rows with Infinite numbers! Cleaning columns...")
    df["MonthlyIncome"] = df["MonthlyIncome"].replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=["MonthlyIncome"])
else:
    print(" -> PASS: Monthly Income contains 100% stable, finite numbers.")


# . Convert 'Yes' and 'No' into simple numbers (1 and 0)
df["Attrition_Numeric"] = df["Attrition"].map({"Yes": 1, "No": 0})

# Create 'Tenure Bands' (0-1 yrs, 2-3 yrs, etc.) using Pandas cut
bins = [-1, 1, 3, 6, 100]
labels = ["0-1 yrs", "2-3 yrs", "4-6 yrs", "7+ yrs"]
df["Tenure_Band"] = pd.cut(df["YearsAtCompany"], bins=bins, labels=labels)

# We use the DATA_OUT path variable so it saves right next to raw data
df.to_csv(DATA_OUT, index=False)

print("✅ Success: 'Clean_data.csv' is created and ready!")
print("=" * 60)
