import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from pathlib import Path


df = pd.read_csv("data\source_tables\calibration_summary_v3.csv")

labels_brier=df[df['model']=='Baseline']['task'].tolist()
baseline_brier=df[df['model']=='Baseline']['brier'].tolist()
sheaf_brier=df[df['model']=='Sheaf']['brier'].tolist()
index=list(range(len(labels_brier)))
bar_width=0.25

labels_ece=df[df['model']=='Baseline']['task'].tolist()
baseline_ece=df[df['model']=='Baseline']['ece'].tolist()
sheaf_ece=df[df['model']=='Sheaf']['ece'].tolist()

fig, (ax1, ax2) = plt.subplots(1, 2, layout='constrained')
fig.set_size_inches(10, 6)

ax1.set_ylabel("Brier score")
ax1.bar([ind-bar_width for ind in index],baseline_brier,width=bar_width,label='Baseline')
ax1.bar(index,sheaf_brier,width=bar_width,label='Sheaf')
ax1.legend(loc="best")
ax1.set_xticks([ind-bar_width/2 for ind in index],labels_brier)
ax1.set_title("Brier Score")
ax1.grid(linestyle="--")

ax2.set_ylabel("Expected Calibration Error")
ax2.bar([ind-bar_width for ind in index],baseline_ece,width=bar_width,label='Baseline')
ax2.bar(index,sheaf_ece,width=bar_width,label='Sheaf')
ax2.legend(loc="best")
ax2.set_xticks([ind-bar_width/2 for ind in index],labels_ece)
ax2.set_title("Expected Calibration Error")
ax2.grid(linestyle="--")

plt.savefig('fig6.png', dpi=300, bbox_inches='tight')
plt.show()
