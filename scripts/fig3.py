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

g3 = pat[pat['grade_label'] == '3']
median = g3['transition_sheaf_risk_index'].median()

low = g3[g3['transition_sheaf_risk_index'] <= median]
high = g3[g3['transition_sheaf_risk_index'] > median]

# create data
x = [1,2,3,4,5]
y = [3,4,6,7,8]

# plot lines
ax2.plot(x, y, label = "line 1", linestyle="-")
ax2.plot(y, x, label = "line 2", linestyle="--")

ax2.legend()


plt.tight_layout()
plt.savefig('fig3.png', dpi=300, bbox_inches='tight')
plt.show()