import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os 
from pathlib import Path


df = pd.read_csv("data/source_tables/plis_drivers_fdr_bootstrap.csv")
df = df.sort_values("delta_plis", ascending=True)

pathways = df["pathway"]
delta_plis = df["delta_plis"]
q_values = df["q_value"]

def asterisk(q):
    if q<0.001:
        return '***'
    if q<0.01:
        return '**'
    if q<0.05:
        return '*'
    return 'ns'

xerr = np.vstack([df["delta_plis"] - df["ci_low"], df["ci_high"] - df["delta_plis"]])

fig, ax = plt.subplots(figsize=(7, 5))

ax.barh(pathways, delta_plis, xerr=xerr, align="center", capsize=4)
ax.set_xlim(left=0)

for i in range(len(pathways)):
    ax.text(df["ci_high"].iloc[i]+0.1, pathways.iloc[i], asterisk(q_values.iloc[i]), va='center', fontsize=12)

ax.set_xlabel("Mean PLIS difference (high risk G3 - low-risk G3)")
ax.set_title("Pathway-local drivers")
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.savefig('figures/fig4.png', dpi=600, bbox_inches='tight')
plt.show()