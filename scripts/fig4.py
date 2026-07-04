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

xerr = np.vstack([df["delta_plis"] - df["ci_low"], df["ci_high"] - df["delta_plis"]])

fig, ax = plt.subplots(figsize=(7, 5))

ax.barh(pathways, delta_plis, xerr=xerr, align="center", capsize=4)
ax.set_xlim(left=0)

ax.set_xlabel("Mean PLIS difference (high risk G3 - low-risk G3)")
ax.set_title("Pathway-local drivers")

plt.savefig('fig4.png', dpi=300, bbox_inches='tight')
plt.tight_layout()
plt.show()