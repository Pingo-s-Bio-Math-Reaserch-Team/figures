import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os 
from pathlib import Path


df = pd.read_csv("data\source_tables\performance_mean_sd_for_latex.csv")

t = list(df['Task'])
tmp = set()

for st in t:
    if not(st in tmp):
        tmp.add(st)
        
tasks = tuple(tmp)
baseline = df.loc[df['Model'] == "Baseline"]
sheaf = df.loc[df['Model'] == "Sheaf"]

baseValList = list()
baseErrorList = list()
sheafValList = list()
sheafErrorList = list()

for st in tasks:
    bs = baseline.loc[df['Task'] == str(st)]
    bstr = bs.iloc[0]['Balanced accuracy']
    
    bfl = float(bstr[0:bstr.find("$")])
    baseValList.append(bfl)
    
    ebfl = float(bstr[bstr.find("$")+6:])
    baseErrorList.append(ebfl)
    
    ss = sheaf.loc[df['Task'] == str(st)]
    sstr = ss.iloc[0]['Balanced accuracy']
    
    sfl = float(sstr[0:sstr.find("$")])
    sheafValList.append(sfl)
    
    esfl = float(sstr[sstr.find("$")+6:])
    sheafErrorList.append(esfl)

  
data = {
    'Baseline': baseValList,
    'Sheaf': sheafValList,
}

x = np.arange(len(tasks))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, (ax1, ax2) = plt.subplots(1, 2, layout='constrained')
fig.set_size_inches(10, 6)
for attribute, measurement in data.items():
    offset = width * multiplier
    rects = ax1.bar(x + offset, measurement, width, label=attribute)
    ax1.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax1.set_ylabel('Length (mm)')
ax1.set_title('Penguin attributes by species')
ax1.set_xticks(x + width, tasks)
ax1.legend(loc='upper left', ncols=3)
ax1.set_ylim(0, 1)

plt.show()
  