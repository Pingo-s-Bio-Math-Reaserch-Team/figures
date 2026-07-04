# hi so this is currently imcomplete but im too lazy to finish it rn but anywho currentyly it just has all 3 dotplots for the grades ok just like dress it up thx

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib.patches import Polygon

df = pd.read_csv("data/source_tables/cplis_patient_table.csv")
print(df.head())
print(df.columns)

grade_col = "grade"
cplis_col = "CPLIS"

data = []

grades = sorted(df[grade_col].dropna().unique())
for grade in grades:
    grade_df = df[df[grade_col] == grade]
    data.append(grade_df[cplis_col].dropna().values)
    

plt.boxplot(data)
plt.title('basic plot')
plt.show()