import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os 
from pathlib import Path
from sklearn.decomposition import PCA

pat = pd.read_csv("data/final_competitive_results/iteration2_patient_transition_risk_scores.csv")
adj = pd.read_csv("data/final_competitive_results/iteration2_transition_adjusted_cox.csv")
km = pd.read_csv("data/final_competitive_results/iteration2_transition_km_logrank.csv")

fig, (ax1, ax2) = plt.subplots(1, 2, layout='constrained')
fig.set_size_inches(10, 4)





#---- ax 2 divide line ;---;

ind = 'os_months'
dep = 'transition_sheaf_risk_index'

g3 = pat.loc[pat['grade_label'] == 3]
g3 = g3.sort_values(by=[ind], ascending=False)

median = g3[dep].median()


low = g3[g3[dep] <= median]
high = g3[g3[dep] > median]



x = list(low[ind])
y = list(low[dep])
ax2.plot(x, y, label = "Low risk (" + str(round(low[dep].median()*10000)/10000) + ")", linestyle="-")

x = list(high[ind])
y = list(high[dep])
ax2.plot(x, y, label = "High risk (" + str(round(high[dep].median()*10000)/10000) + ")", linestyle="-", color = "red")

ax2.legend()


plt.tight_layout()
plt.savefig('fig3.png', dpi=300, bbox_inches='tight')
plt.show()