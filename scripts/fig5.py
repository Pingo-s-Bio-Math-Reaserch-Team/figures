import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("data/source_tables/alpha_sensitivity.csv")

plt.rcParams["figure.figsize"] = (5, 5)

x = df["alpha"]
y = df['grade3_c_index']
z = -np.log10(df['logrank_p'])

fig, ax1 = plt.subplots(figsize=(7, 6))

ax1.plot(x, y, marker="o", markersize=8, label="C-index", color = 'C0')
ax1.set_xlabel(r"$\alpha$ in transition index", fontsize=11)
ax1.set_ylabel("Grade 3 C-index", fontsize=11)
ax1.set_ylim(0.58, 0.73)
ax1.set_xticks(x)

ax2 = ax1.twinx()
ax2.set_ylabel("-log10(log-rank p)", fontsize=11)
ax2.plot(x, z, ls="--", lw=3, marker="s", markersize=7,label="-log10(p)", color = 'C0')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

ax1.legend(lines1 + lines2, labels1 + labels2, loc=0)
ax1.set_title(r"Transition-risk robustness across $\alpha$", fontsize=14)


plt.savefig('fig5.png', dpi=300, bbox_inches='tight')
plt.show()