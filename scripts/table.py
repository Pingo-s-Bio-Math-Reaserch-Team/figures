import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os 
from pathlib import Path


df = pd.read_csv(r"data\final_competitive_results\iteration2_patient_transition_risk_scores.csv")
g3 = df.query("grade == 3.0").copy()
timeset = [0, 24, 48, 72, 96, 120]
indexdf = g3.transition_sheaf_risk_index
med = indexdf.median()
high = g3.transition_sheaf_risk_index > med
low = g3.transition_sheaf_risk_index <= med
high_df = g3[high]
low_df = g3[low]
high_counts = []
low_counts = []

for t in timeset:
    low_counts.append((low_df["os_months"] > t).sum())
    high_counts.append((high_df["os_months"] > t).sum())

table = pd.DataFrame (
    [low_counts, high_counts],
    index=["Low","High"],
    columns=timeset
)

print(table)

fig, ax = plt.subplots(figsize=(8,2))
ax.axis('off')
figtable = ax.table(
    cellText=table.values,
    rowLabels=table.index,
    colLabels=table.columns,
    cellLoc="center",
    loc="center"
)
plt.savefig('figures/tableForFig3.png', dpi=600, bbox_inches='tight')

plt.show()