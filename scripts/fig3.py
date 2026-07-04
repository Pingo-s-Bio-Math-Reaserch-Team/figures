import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os 
from pathlib import Path
from sklearn.decomposition import PCA
from lifelines import KaplanMeierFitter 
from lifelines.statistics import logrank_test

pat = pd.read_csv("data/final_competitive_results/iteration2_patient_transition_risk_scores.csv")
adj = pd.read_csv("data/final_competitive_results/iteration2_transition_adjusted_cox.csv")
km = pd.read_csv("data/final_competitive_results/iteration2_transition_km_logrank.csv")

fig, (ax1, ax2) = plt.subplots(1, 2, layout='constrained')
fig.set_size_inches(10, 4)

#--------------ax1 begins here----------------

select_columns = [column for column in pat.columns if column.startswith('pathway_')]
pca = PCA(n_components=2)
coords = pca.fit_transform(pat[select_columns])

pat['PC1'] = coords[:, 0]
pat['PC2'] = coords[:, 1]

g3med = pat.loc[pat['grade'] == 3, 'transition_sheaf_risk_index'].median()
other = pat[pat['grade'] != 3]
g3_low = pat[(pat['grade'] == 3) & (pat['transition_sheaf_risk_index'] < g3med)]
g3_high = pat[(pat['grade'] == 3) & (pat['transition_sheaf_risk_index'] >= g3med)]
g4 = pat[pat['grade'] == 4]

ax1.scatter(other['PC1'], other['PC2'], c='lightblue', alpha=0.5, label='Other', s= 50)
ax1.scatter(g3_low['PC1'], g3_low['PC2'], c='orange', alpha=0.5, label='Grade 3 low', s= 50)
ax1.scatter(g3_high['PC1'], g3_high['PC2'], c='green', alpha=0.5, label='Grade 3 high', s= 50)
ax1.scatter(g4['PC1'], g4['PC2'], c='red', marker='^' , alpha=0.5, label='Grade 4', s= 50) #DELETE THIS LINE IF YOU DONT WANT GRADE 4 POINTS
ax1.scatter(g4['PC1'].mean(), g4['PC2'].mean(), c='darkorchid', marker='*', label='Grade 4 centroid', s= 200)

leg = ax1.legend(fontsize = 8, loc='upper left')

ax1.set_xlabel('PC1 of pathway residual space')
ax1.set_ylabel('PC2')
ax1.set_title('Residual geometry')

print(pca.explained_variance_ratio_)

#-------------ax2 divide line------------------

ind = 'os_months'
dep = 'deceased'
sort = 'transition_sheaf_risk_index'

g3 = pat.loc[pat['grade_label'] == 3]
g3 = g3.sort_values(by=[ind], ascending=False)

median = g3[sort].median()

low = g3[g3[sort] <= median]
high = g3[g3[sort] > median]

kmfl = KaplanMeierFitter(label="Low Transition Risk")
kmfl = kmfl.fit(low[ind], low[dep])
kmfl.plot()


kmfh = KaplanMeierFitter(label="High Transition Risk")
kmfh = kmfh.fit(high[ind], high[dep])
kmfh.plot()

ax2.set_title("Grade 3 Kaplan-Meier separation")
pval = str(logrank_test(high[ind], low[ind], high[dep], low[dep]).p_value)
num = pval[0:5]
num = float(num)
num *= 100
num = round(num)
num /= 100
indexOfE = pval.find("e")

pval = pval[indexOfE:]

pval = str(num) + "-" + pval
ax2.text(1, 0, "og-rank p=" + pval)

ax2.legend()
ax2.set_ylabel("Survival probability")

plt.tight_layout()
#plt.savefig('fig3.png', dpi=300, bbox_inches='tight')
plt.show()