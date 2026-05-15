"""
Week 5 Analytics Project – Data Profiling & Cleansing
Dataset: Diabetes 130-US Hospitals for Years 1999-2008 (UCI ML Repository)
Author: Shruti Malik
Course: ITEC 5040
"""

import os
import urllib.request
import zipfile
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = r"C:\Users\Owner\Documents\Analytics-Project-Draft"
DATA_URL = "https://archive.ics.uci.edu/static/public/296/diabetes+130-us+hospitals+for+years+1999-2008.zip"
ZIP_PATH  = os.path.join(BASE_DIR, "diabetes_raw.zip")
CSV_PATH  = os.path.join(BASE_DIR, "diabetic_data.csv")

# ── 1. Download dataset if needed ────────────────────────────────────────────
if not os.path.exists(CSV_PATH):
    print("Downloading dataset …")
    urllib.request.urlretrieve(DATA_URL, ZIP_PATH)
    with zipfile.ZipFile(ZIP_PATH, 'r') as z:
        z.extractall(BASE_DIR)
    # the zip may nest the csv; find it
    for root, dirs, files in os.walk(BASE_DIR):
        for f in files:
            if f == "diabetic_data.csv":
                src = os.path.join(root, f)
                if src != CSV_PATH:
                    import shutil
                    shutil.copy(src, CSV_PATH)
                break
    print("Download complete.")
else:
    print("Dataset already present. Skipping download.")

# ── 2. Load ──────────────────────────────────────────────────────────────────
df = pd.read_csv(CSV_PATH, na_values=["?"])
print(f"\n{'='*60}")
print(f"RAW DATASET  – {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"{'='*60}")

# ── 3. Initial Profiling Summary ─────────────────────────────────────────────
print("\n--- Column Types ---")
print(df.dtypes.to_string())

print("\n--- Missing Values (% of rows) ---")
miss = df.isnull().sum()
miss_pct = (miss / len(df) * 100).round(2)
miss_df  = pd.DataFrame({"Missing N": miss, "Missing %": miss_pct})
miss_df  = miss_df[miss_df["Missing N"] > 0].sort_values("Missing N", ascending=False)
print(miss_df.to_string())

print("\n--- Descriptive Statistics (numeric columns) ---")
print(df.describe().to_string())

print("\n--- Target Variable Distribution: readmitted ---")
print(df["readmitted"].value_counts())
print(df["readmitted"].value_counts(normalize=True).round(3).to_string())

# ── 4. FIGURE 1 – Missing Values Bar Chart ───────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4))
miss_df["Missing %"].plot(kind='barh', ax=ax, color='#d62728')
ax.set_xlabel("% Missing", fontsize=11)
ax.set_title("Figure 1: Missing Values by Feature (%)", fontsize=13, fontweight='bold')
ax.axvline(50, color='navy', linestyle='--', linewidth=1, label='50 % threshold')
ax.legend(fontsize=9)
plt.tight_layout()
fig.savefig(os.path.join(BASE_DIR, "fig1_missing_values.png"), dpi=150)
plt.close()
print("\nSaved fig1_missing_values.png")

# ── 5. FIGURE 2 – Target Variable Distribution ───────────────────────────────
readmit_counts = df["readmitted"].value_counts()
colors = ['#2ca02c', '#1f77b4', '#ff7f0e']
fig, ax = plt.subplots(figsize=(5, 4))
ax.bar(readmit_counts.index, readmit_counts.values, color=colors)
ax.set_title("Figure 2: Readmission Outcome Distribution", fontsize=13, fontweight='bold')
ax.set_xlabel("Readmission Status", fontsize=11)
ax.set_ylabel("Number of Encounters", fontsize=11)
for i, v in enumerate(readmit_counts.values):
    ax.text(i, v + 200, f"{v:,}", ha='center', fontsize=9)
plt.tight_layout()
fig.savefig(os.path.join(BASE_DIR, "fig2_readmission_dist.png"), dpi=150)
plt.close()
print("Saved fig2_readmission_dist.png")

# ── 6. FIGURE 3 – Age Distribution ───────────────────────────────────────────
age_order = ['[0-10)', '[10-20)', '[20-30)', '[30-40)', '[40-50)',
             '[50-60)', '[60-70)', '[70-80)', '[80-90)', '[90-100)']
age_counts = df['age'].value_counts().reindex(age_order)
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(age_counts.index, age_counts.values, color='#1f77b4', edgecolor='white')
ax.set_title("Figure 3: Age Distribution of Patient Encounters", fontsize=13, fontweight='bold')
ax.set_xlabel("Age Group", fontsize=11)
ax.set_ylabel("Encounters", fontsize=11)
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
fig.savefig(os.path.join(BASE_DIR, "fig3_age_distribution.png"), dpi=150)
plt.close()
print("Saved fig3_age_distribution.png")

# ── 7. FIGURE 4 – Top 10 Medical Specialties (with high missingness) ──────────
spec_counts = df['medical_specialty'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(spec_counts.index[::-1], spec_counts.values[::-1], color='#9467bd')
ax.set_title("Figure 4: Top 10 Medical Specialties (with NA shown)", fontsize=13, fontweight='bold')
ax.set_xlabel("Encounter Count", fontsize=11)
plt.tight_layout()
fig.savefig(os.path.join(BASE_DIR, "fig4_medical_specialty.png"), dpi=150)
plt.close()
print("Saved fig4_medical_specialty.png")

# ── 8. FIGURE 5 – Num Medications Distribution ───────────────────────────────
fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(df['num_medications'].dropna(), bins=30, color='#17becf', edgecolor='white')
ax.set_title("Figure 5: Distribution of Number of Medications", fontsize=13, fontweight='bold')
ax.set_xlabel("Number of Medications", fontsize=11)
ax.set_ylabel("Frequency", fontsize=11)
ax.axvline(df['num_medications'].median(), color='red', linestyle='--',
           label=f"Median = {df['num_medications'].median():.0f}")
ax.legend()
plt.tight_layout()
fig.savefig(os.path.join(BASE_DIR, "fig5_num_medications.png"), dpi=150)
plt.close()
print("Saved fig5_num_medications.png")

# ── 9. FIGURE 6 – Readmission Rate by Age Group ──────────────────────────────
df['early_readmit'] = (df['readmitted'] == '<30').astype(int)
readmit_by_age = df.groupby('age')['early_readmit'].mean().reindex(age_order) * 100
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(readmit_by_age.index, readmit_by_age.values, marker='o', linewidth=2, color='#d62728')
ax.set_title("Figure 6: 30-Day Readmission Rate (%) by Age Group", fontsize=13, fontweight='bold')
ax.set_xlabel("Age Group", fontsize=11)
ax.set_ylabel("Readmission Rate (%)", fontsize=11)
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
fig.savefig(os.path.join(BASE_DIR, "fig6_readmit_by_age.png"), dpi=150)
plt.close()
print("Saved fig6_readmit_by_age.png")

# ═══════════════════════════════════════════════════════════════════════════════
# 10. DATA CLEANSING
# ═══════════════════════════════════════════════════════════════════════════════
print(f"\n{'='*60}")
print("DATA CLEANSING STEPS")
print(f"{'='*60}")
df_clean = df.copy()

# Step A – Remove duplicate encounter IDs
before = len(df_clean)
df_clean.drop_duplicates(subset='encounter_id', inplace=True)
print(f"A) Dropped {before - len(df_clean):,} duplicate encounter rows. Remaining: {len(df_clean):,}")

# Step B – Remove rows where gender is 'Unknown/Invalid'
before = len(df_clean)
df_clean = df_clean[df_clean['gender'] != 'Unknown/Invalid']
print(f"B) Dropped {before - len(df_clean):,} rows with Unknown/Invalid gender. Remaining: {len(df_clean):,}")

# Step C – Drop columns with >40% missing
high_miss = miss_df[miss_df["Missing %"] > 40].index.tolist()
print(f"C) Columns >40% missing to drop: {high_miss}")
df_clean.drop(columns=high_miss, errors='ignore', inplace=True)

# Step D – Impute medical_specialty with 'Unknown' (categorical)
if 'medical_specialty' in df_clean.columns:
    df_clean['medical_specialty'].fillna('Unknown', inplace=True)
    print(f"D) Filled medical_specialty NA with 'Unknown'.")

# Step E – Impute payer_code with mode (if still present after C)
if 'payer_code' in df_clean.columns:
    mode_val = df_clean['payer_code'].mode()[0]
    df_clean['payer_code'].fillna(mode_val, inplace=True)
    print(f"E) Filled payer_code NA with mode='{mode_val}'.")

# Step F – Map readmitted to binary target (1 = readmitted <30 days, 0 = otherwise)
df_clean['readmit_30'] = (df_clean['readmitted'] == '<30').astype(int)
print(f"F) Created binary target 'readmit_30'. Class balance:\n"
      f"   {df_clean['readmit_30'].value_counts().to_dict()}")

# Step G – Convert age bracket to ordinal integer midpoint
age_map = {
    '[0-10)': 5, '[10-20)': 15, '[20-30)': 25, '[30-40)': 35,
    '[40-50)': 45, '[50-60)': 55, '[60-70)': 65, '[70-80)': 75,
    '[80-90)': 85, '[90-100)': 95
}
df_clean['age_midpoint'] = df_clean['age'].map(age_map)
print(f"G) Mapped age brackets to numeric midpoints.")

# Step H – Remove encounters with discharge_disposition_id = 11, 13, 14, 19, 20, 21
#           (patient deceased or transferred to hospice – not relevant to readmission)
excl_dispositions = [11, 13, 14, 19, 20, 21]
before = len(df_clean)
df_clean = df_clean[~df_clean['discharge_disposition_id'].isin(excl_dispositions)]
print(f"H) Removed {before - len(df_clean):,} hospice/deceased encounters. Remaining: {len(df_clean):,}")

# Step I – Keep only first encounter per patient (avoid data leakage)
before = len(df_clean)
df_clean.sort_values('encounter_id', inplace=True)
df_clean.drop_duplicates(subset='patient_nbr', keep='first', inplace=True)
print(f"I) Kept first encounter per patient: removed {before - len(df_clean):,}. Remaining: {len(df_clean):,}")

# Step J – Save cleaned dataset
clean_path = os.path.join(BASE_DIR, "diabetic_data_clean.csv")
df_clean.to_csv(clean_path, index=False)
print(f"\nCleaned dataset saved -> {clean_path}")
print(f"Final shape: {df_clean.shape[0]:,} rows × {df_clean.shape[1]} columns")

print(f"\n{'='*60}")
print("All profiling figures and cleaned dataset are ready.")
print(f"{'='*60}")
