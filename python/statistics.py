
from pathlib import Path
import pandas as pd
from scipy import stats

print("=" * 60)
print("RUNNING FILE 2: STATISTICAL HYPOTHESIS TESTING")
print("=" * 60)

# 1. Setup path to look inside the data folder using the ROOT path variable
ROOT = Path(__file__).resolve().parent.parent  
DATA_IN = ROOT / "data" / "Clean_data.csv"

# 2. Load the freshly cleaned data file into memory
df = pd.read_csv(DATA_IN)



# TEST 1: Income vs Attrition (Independent Samples T-Test)
# We filter the salary column into two separate groups using Pandas
income_left = df[df["Attrition"] == "Yes"]["MonthlyIncome"]
income_stayed = df[df["Attrition"] == "No"]["MonthlyIncome"]

# Run the t-test calculator to check if the salary gap is mathematically real
t_statistic, p_value_income = stats.ttest_ind(income_left, income_stayed, equal_var=False)

print("\n Statistical Check 1 (Income vs Attrition):")
print(f" -> Average Income of employees who Left:   ${income_left.mean():.2f}")
print(f" -> Average Income of employees who Stayed: ${income_stayed.mean():.2f}")
print(f" -> Math p-value result: {p_value_income:.6f}")

if p_value_income < 0.05:
    print(" -> CONCLUSION: The income difference is real and statistically significant!")
else:
    print(" -> CONCLUSION: No meaningful statistical income gap found.")



# TEST 2: OverTime vs Attrition (Chi-Square Test)
# Create a basic cross-tabulation table using standard Pandas crosstab
comparison_table = pd.crosstab(df["OverTime"], df["Attrition"])

# Run the chi-square calculator to check if overtime is linked to leaving
chi2_value, p_value_overtime, _, _ = stats.chi2_contingency(comparison_table)

print("\n Statistical Check 2 (OverTime vs Attrition):")
print(comparison_table)
print(f" -> Math p-value result: {p_value_overtime:.6f}")

if p_value_overtime < 0.05:
    print(" -> CONCLUSION: Overtime is strongly and directly tied to employee attrition!")
else:
    print(" -> CONCLUSION: No meaningful mathematical link between overtime and attrition.")


print("\n" + "=" * 60)
print("✅ Success: Statistics calculated using dynamic ROOT pathways!")
print("=" * 60)
