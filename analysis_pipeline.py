import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.size'] = 10

data_path = r'C:\Users\Owner\Documents\week10 ANLT 5010\cf_ANLT5010_W10_Penalties_ClarionCourt.csv'
df = pd.read_csv(data_path)

output_dir = r'C:\Users\Owner\.gemini\antigravity\brain\7756d66f-ad62-4dd1-aa6c-3248550ebf73'
img_dir = os.path.join(output_dir, 'figures')
os.makedirs(img_dir, exist_ok=True)

print("Total Records:", len(df))

# 1. Target Recoding
# In NNHS coding: 1 = Yes, 2 = No, 8 = Unknown/Not Ascertained
df['Fall_Binary'] = df['ANYFALLS'].apply(lambda x: 1 if x == 1 else (0 if x == 2 else np.nan))
df['PressureUlcer_Binary'] = df['ULCERHI'].apply(lambda x: 1 if x in [1, 2, 3, 4] else (0 if x == 0 else np.nan))

# Clean predictors
features = [
    'AGEATINT', 'SEX', 'TOTALADL', 'BEDMOBIL', 'TRANSFER', 'WALKING', 
    'DECISION', 'MOOD', 'BOWLCONT', 'BLADCONT', 'WGTLOSS', 'RXTOTAL', 
    'LOS', 'SIDERAIL', 'BEDRAIL'
]

clean_df = df.copy()

# Recode values
clean_df['AGEATINT'] = clean_df['AGEATINT'].replace({999: np.nan})
clean_df['BEDMOBIL'] = clean_df['BEDMOBIL'].replace({88: np.nan, 8: np.nan})
clean_df['TRANSFER'] = clean_df['TRANSFER'].replace({88: np.nan, 8: np.nan})
clean_df['WALKING'] = clean_df['WALKING'].replace({8: np.nan})
clean_df['DECISION'] = clean_df['DECISION'].replace({8: np.nan})
clean_df['MOOD'] = clean_df['MOOD'].replace({8: np.nan})
clean_df['BOWLCONT'] = clean_df['BOWLCONT'].replace({8: np.nan})
clean_df['BLADCONT'] = clean_df['BLADCONT'].replace({8: np.nan})
clean_df['WGTLOSS'] = clean_df['WGTLOSS'].apply(lambda x: 1 if x == 1 else (0 if x == 2 else np.nan))
clean_df['SIDERAIL'] = clean_df['SIDERAIL'].apply(lambda x: 1 if x in [1, 2] else (0 if x == 0 else np.nan))
clean_df['BEDRAIL'] = clean_df['BEDRAIL'].apply(lambda x: 1 if x in [1, 2] else (0 if x == 0 else np.nan))

# Impute medians
for col in features:
    clean_df[col] = clean_df[col].fillna(clean_df[col].median())

# ==========================================
# Figure 1: Financial & Operational Impact (Penalties by Deficiency)
# ==========================================
fig, ax = plt.subplots(figsize=(10, 6))
def_summary = df.groupby('deficiency_desc')['fine_amt'].agg(['count', 'sum', 'mean']).reset_index()
def_summary = def_summary.sort_values(by='sum', ascending=False).head(8)

sns.barplot(data=def_summary, y='deficiency_desc', x='sum', palette='Blues_r', ax=ax)
ax.set_title('Figure 1: Top Health Deficiency Penalties by Total Fines ($)', fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Total Fine Amount (USD)', fontsize=11, fontweight='bold')
ax.set_ylabel('Deficiency Category', fontsize=11, fontweight='bold')
ax.xaxis.set_major_formatter('${x:,.0f}')
plt.tight_layout()
plt.savefig(os.path.join(img_dir, 'figure1_fines_by_deficiency.png'), dpi=300)
plt.close()

# ==========================================
# Figure 2: Fall and Pressure Ulcer Distribution across ADL Impairment
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# Fall rate by ADL
adl_fall = clean_df.groupby('TOTALADL')['Fall_Binary'].mean().reset_index()
sns.barplot(data=adl_fall, x='TOTALADL', y='Fall_Binary', color='#2b5c8f', ax=ax1)
ax1.set_title('A: Fall Incidence Rate by ADL Score (0-5)', fontsize=11, fontweight='bold')
ax1.set_xlabel('Total ADL Impairment Score (0=Independent, 5=Dependent)', fontsize=10)
ax1.set_ylabel('Proportion of Residents Experiencing Falls', fontsize=10)
ax1.yaxis.set_major_formatter('{x:.1%}')

# Pressure ulcer rate by Bed Mobility
bed_pu = clean_df.groupby('BEDMOBIL')['PressureUlcer_Binary'].mean().reset_index()
sns.barplot(data=bed_pu, x='BEDMOBIL', y='PressureUlcer_Binary', color='#d95f02', ax=ax2)
ax2.set_title('B: Pressure Ulcer Rate by Bed Mobility Level', fontsize=11, fontweight='bold')
ax2.set_xlabel('Bed Mobility (0=Indep, 1=Supervis, 2=Limited, 3=Extens, 4=Total)', fontsize=10)
ax2.set_ylabel('Proportion with Pressure Ulcers', fontsize=10)
ax2.yaxis.set_major_formatter('{x:.1%}')

plt.suptitle('Figure 2: Clinical Risk Correlations with Physical Functional Impairment', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(img_dir, 'figure2_risk_vs_impairment.png'), dpi=300)
plt.close()

# ==========================================
# Predictive Modeling: Fall Risk
# ==========================================
fall_df = clean_df.dropna(subset=['Fall_Binary'])
X_f = fall_df[features]
y_f = fall_df['Fall_Binary']

X_tr_f, X_te_f, y_tr_f, y_te_f = train_test_split(X_f, y_f, test_size=0.25, random_state=42, stratify=y_f)

lr_fall = LogisticRegression(max_iter=1000, random_state=42)
lr_fall.fit(X_tr_f, y_tr_f)
y_pred_f = lr_fall.predict(X_te_f)
y_prob_f = lr_fall.predict_proba(X_te_f)[:, 1]

rf_fall = RandomForestClassifier(n_estimators=150, max_depth=5, random_state=42)
rf_fall.fit(X_tr_f, y_tr_f)
y_pred_rf_f = rf_fall.predict(X_te_f)
y_prob_rf_f = rf_fall.predict_proba(X_te_f)[:, 1]

auc_lr_f = roc_auc_score(y_te_f, y_prob_f)
auc_rf_f = roc_auc_score(y_te_f, y_prob_rf_f)

print(f"Fall Model - Logistic Regression AUC: {auc_lr_f:.3f}, RF AUC: {auc_rf_f:.3f}")

# ==========================================
# Predictive Modeling: Pressure Ulcer Risk
# ==========================================
pu_df = clean_df.dropna(subset=['PressureUlcer_Binary'])
X_p = pu_df[features]
y_p = pu_df['PressureUlcer_Binary']

X_tr_p, X_te_p, y_tr_p, y_te_p = train_test_split(X_p, y_p, test_size=0.25, random_state=42, stratify=y_p)

lr_pu = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
lr_pu.fit(X_tr_p, y_tr_p)
y_pred_p = lr_pu.predict(X_te_p)
y_prob_p = lr_pu.predict_proba(X_te_p)[:, 1]

rf_pu = RandomForestClassifier(n_estimators=150, max_depth=5, class_weight='balanced', random_state=42)
rf_pu.fit(X_tr_p, y_tr_p)
y_pred_rf_p = rf_pu.predict(X_te_p)
y_prob_rf_p = rf_pu.predict_proba(X_te_p)[:, 1]

auc_lr_p = roc_auc_score(y_te_p, y_prob_p)
auc_rf_p = roc_auc_score(y_te_p, y_prob_rf_p)

print(f"Pressure Ulcer Model - Logistic Regression AUC: {auc_lr_p:.3f}, RF AUC: {auc_rf_p:.3f}")

# ==========================================
# Figure 3: ROC Curves for Fall and Pressure Ulcer Models
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# Fall ROC
fpr_f_lr, tpr_f_lr, _ = roc_curve(y_te_f, y_prob_f)
fpr_f_rf, tpr_f_rf, _ = roc_curve(y_te_f, y_prob_rf_f)
ax1.plot(fpr_f_lr, tpr_f_lr, label=f'Logistic Regression (AUC = {auc_lr_f:.2f})', color='#1f77b4', lw=2)
ax1.plot(fpr_f_rf, tpr_f_rf, label=f'Random Forest (AUC = {auc_rf_f:.2f})', color='#2ca02c', lw=2, linestyle='--')
ax1.plot([0, 1], [0, 1], 'k:', lw=1.5)
ax1.set_title('A: Fall Risk ROC Performance', fontsize=11, fontweight='bold')
ax1.set_xlabel('False Positive Rate (1 - Specificity)', fontsize=10)
ax1.set_ylabel('True Positive Rate (Sensitivity)', fontsize=10)
ax1.legend(loc='lower right', frameon=True)

# Pressure Ulcer ROC
fpr_p_lr, tpr_p_lr, _ = roc_curve(y_te_p, y_prob_p)
fpr_p_rf, tpr_p_rf, _ = roc_curve(y_te_p, y_prob_rf_p)
ax2.plot(fpr_p_lr, tpr_p_lr, label=f'Logistic Regression (AUC = {auc_lr_p:.2f})', color='#d62728', lw=2)
ax2.plot(fpr_p_rf, tpr_p_rf, label=f'Random Forest (AUC = {auc_rf_p:.2f})', color='#9467bd', lw=2, linestyle='--')
ax2.plot([0, 1], [0, 1], 'k:', lw=1.5)
ax2.set_title('B: Pressure Ulcer Risk ROC Performance', fontsize=11, fontweight='bold')
ax2.set_xlabel('False Positive Rate (1 - Specificity)', fontsize=10)
ax2.set_ylabel('True Positive Rate (Sensitivity)', fontsize=10)
ax2.legend(loc='lower right', frameon=True)

plt.suptitle('Figure 3: Receiver Operating Characteristic (ROC) Validation Curves', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(img_dir, 'figure3_roc_curves.png'), dpi=300)
plt.close()

# ==========================================
# Figure 4: Feature Importance / Odds Ratios
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

fall_odds = pd.DataFrame({'Feature': features, 'Odds_Ratio': np.exp(lr_fall.coef_[0])}).sort_values('Odds_Ratio')
ax1.barh(fall_odds['Feature'], fall_odds['Odds_Ratio'], color='#3182bd')
ax1.axvline(1.0, color='red', linestyle='--', linewidth=1.5)
ax1.set_title('A: Fall Risk Odds Ratios (Logistic Regression)', fontsize=11, fontweight='bold')
ax1.set_xlabel('Adjusted Odds Ratio (OR > 1.0 indicates higher risk)', fontsize=10)

pu_odds = pd.DataFrame({'Feature': features, 'Odds_Ratio': np.exp(lr_pu.coef_[0])}).sort_values('Odds_Ratio')
ax2.barh(pu_odds['Feature'], pu_odds['Odds_Ratio'], color='#e6550d')
ax2.axvline(1.0, color='red', linestyle='--', linewidth=1.5)
ax2.set_title('B: Pressure Ulcer Risk Odds Ratios (Logistic Regression)', fontsize=11, fontweight='bold')
ax2.set_xlabel('Adjusted Odds Ratio (OR > 1.0 indicates higher risk)', fontsize=10)

plt.suptitle('Figure 4: Diagnostic Predictor Coefficients & Impact Ratios', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(img_dir, 'figure4_odds_ratios.png'), dpi=300)
plt.close()

print("All figures and model outputs generated successfully!")
