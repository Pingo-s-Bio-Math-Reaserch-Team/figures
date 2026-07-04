import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib.patches import Polygon

df = pd.read_csv("data/source_tables/cplis_patient_table.csv")

grade_col = "grade"
cplis_col = "CPLIS"

data = []

grades = sorted(df[grade_col].dropna().unique())
for grade in grades:
    grade_df = df[df[grade_col] == grade]
    data.append(grade_df[cplis_col].dropna().values)
    
plt.ylabel("CPLIS", fontsize=14)
plt.boxplot(data, sym='', labels=["Grade 2", "Grade 3", "Grade 4"], showmeans=True, meanprops={"marker": "o", "markerfacecolor": "C0", "markersize": 10})
plt.tick_params(axis='both', labelsize=14) 

box = plt.boxplot(data, sym='', labels=["Grade 2", "Grade 3", "Grade 4"], showmeans=True, meanprops={"marker": "o", "markerfacecolor": "C0", "markersize": 10, "markeredgecolor": "C0"})

means_x = []
means_y = []

for mean in box['means']:
    x, y = mean.get_xdata(), mean.get_ydata()
    means_x.append(x[0])
    means_y.append(y[0])

plt.plot(means_x, means_y, color='C0', linestyle='--', linewidth=2)

plt.legend([box['means'][0]], ['Mean'])
plt.title('Concentrated PLIS by grade', fontsize=16)
plt.savefig('fig7.png', dpi=300, bbox_inches='tight')
plt.show()