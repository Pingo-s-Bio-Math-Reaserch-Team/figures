import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os 
from pathlib import Path
import math

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
errorList = list()

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
    errorList.append(esfl)

  
data = {
    'Baseline': baseValList,
    'Sheaf': sheafValList,
}


x = np.arange(len(tasks)) 
width = 0.4 
multiplier = 0

fig, (ax1, ax2) = plt.subplots(1, 2, layout='constrained')
fig.set_size_inches(10, 4)

baseStrError = list()
sheafStrError = list()


    
iter = 0


for i in range(len(baseValList)):
    num = sheafValList[i] - baseValList[i]
    num *= 10000
    num = round(num)
    num /= 10000
    if(num > 0):
        strer = str(num)
        baseStrError.append("+" + strer[0:5] )

    
    else:
        strer = str(num)
        baseStrError.append(strer[0:6])
        
        
for attribute, measurement in data.items():
    offset = width * multiplier
    if(iter == 0):
        rects = ax1.bar(x + offset, measurement, width, label=attribute, yerr = baseErrorList, capsize = 5)

    else:
        rects = ax1.bar(x + offset, measurement, width, label=attribute, yerr = errorList, capsize = 5)
       
    multiplier += 1
    iter+=1
    
for i in range(len(errorList)):
    ax1.text((width*.5)-.1 + (width + offset*1.5) * i, 1, baseStrError[i])

    

ax1.set_ylabel('Balanced accuracy')
ax1.set_title('Balanced accuracy')
ax1.set_xticks(x + width, tasks)
ax1.legend(loc='upper left', ncols=3)
ax1.set_ylim(0, 1.2)


baseline = df.loc[df['Model'] == "Baseline"]
sheaf = df.loc[df['Model'] == "Sheaf"]

baseValList = list()
baseErrorList = list()
sheafValList = list()
errorList = list()
er = list()
for st in tasks:
    bs = baseline.loc[df['Task'] == str(st)]
    bstr = bs.iloc[0]['AUROC']
    
    bfl = float(bstr[0:bstr.find("$")])
    baseValList.append(bfl)
    
    ebfl = float(bstr[bstr.find("$")+6:])
    baseErrorList.append(ebfl)
    er.append(ebfl)
    
    ss = sheaf.loc[df['Task'] == str(st)]
    sstr = ss.iloc[0]['AUROC']
    
    sfl = float(sstr[0:sstr.find("$")])
    sheafValList.append(sfl)
    
    esfl = float(sstr[sstr.find("$")+6:])
    errorList.append(esfl)
    er.append(esfl)
  
data = {
    'Baseline': baseValList,
    'Sheaf': sheafValList,
}


x = np.arange(len(tasks))  
width = 0.4  
multiplier = 0


baseStrError = list()


for i in range(len(baseValList)):
    num = sheafValList[i] - baseValList[i]
    num *= 10000
    num = round(num)
    num /= 10000
    num = sheafValList[i] - baseValList[i]
    if(num > 0):
        strer = str(num)
        baseStrError.append("+" + strer[0:5] )
    else:
        strer = str(num)
        baseStrError.append(strer[0:6])



for attribute, measurement in data.items():
    offset = width * multiplier
    if(iter == 0):
        rects = ax2.bar(x + offset, measurement, width, label=attribute, yerr = baseErrorList, capsize = 5)
    else:
        rects = ax2.bar(x + offset, measurement, width, label=attribute, yerr = errorList, capsize = 5)
    
    multiplier += 1
    

for i in range(len(errorList)):
    ax2.text((width*.5)-.1 + (width + offset*1.5) * i, 1, baseStrError[i])
    
    
ax2.set_ylabel('AUROC')
ax2.set_title('AUROC')
ax2.set_xticks(x + width, tasks)

ax2.set_ylim(0, 1.2)

plt.tight_layout()
plt.savefig('fig2.png', dpi=300, bbox_inches='tight')
plt.show()
  