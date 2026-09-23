
from pathlib import Path
import pandas as pd
from scipy import stats
import numpy as np

print("=" * 60)
print("RUNNING FILE 4: A/B TESTING SAMPLE SIZING DESIGN")
print("=" * 60)

# 1. Setup paths to pull your clean data using your dynamic root
ROOT = Path(__file__).resolve().parent.parent  
DATA_IN = ROOT / "data" / "Clean_data.csv"
df = pd.read_csv(DATA_IN)

# EXPERIMENT DESIGN PARAMETERS
# Based on SQL segment, high-risk baseline attrition rate is ~57.8% (0.578)
p1 = 0.578  

# If HR's new flexible policy works, we target dropping attrition to 45.0% (0.450)
p2 = 0.450  

# Standard industry guardrails: 95% Confidence (alpha=0.05) and 80% Power (beta=0.20)
alpha = 0.05
power = 0.80

# Get the standard statistical Z-scores for our confidence levels
z_alpha = stats.norm.ppf(1 - alpha / 2) # Z-score for 95% confidence (~1.96)
z_beta = stats.norm.ppf(power)          # Z-score for 80% power (~0.84)

print(" Experiment Inputs:")
print(f" -> Current High-Risk Attrition Baseline (Control Group): {p1*100:.1f}%")
print(f" -> Desired Target Attrition Level (Treatment Group):    {p2*100:.1f}%")

# =====================================================================
# MATH FORMULA: TWO-PROPORTION SAMPLE SIZE CALCULATION
# =====================================================================
# Pooled variance calculation
p_pooled = (p1 + p2) / 2
variance = 2 * p_pooled * (1 - p_pooled)
effect_size_sq = (p1 - p2) ** 2

# Calculate the required sample size per group
sample_size_per_group = (variance * (z_alpha + z_beta) ** 2) / effect_size_sq
sample_size_per_group = int(np.ceil(sample_size_per_group)) # Round up to whole person

print("\n🎯 Final Experiment Requirements:")
print(f" -> Required Sample Size PER GROUP: ~{sample_size_per_group} employees")
print(f" -> Total Sample Size for the test:   ~{sample_size_per_group * 2} employees")

print("\n" + "=" * 60)
print("✅ Success: A/B Test metrics calculated using dynamic ROOT pathways!")
print("=" * 60)
