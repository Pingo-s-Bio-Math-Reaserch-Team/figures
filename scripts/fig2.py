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

for bserr in baseErrorList:
    baseStrError.append('±' + str(bserr))

for sserr in errorList:
    sheafStrError.append('±' + str(sserr))
    
iter = 0
for attribute, measurement in data.items():
    offset = width * multiplier
    if(iter == 0):
        rects = ax1.bar(x + offset, measurement, width, label=attribute, yerr = baseErrorList, capsize = 5)
        ax1.bar_label(container=rects, padding=3, labels=baseStrError)
    else:
        rects = ax1.bar(x + offset, measurement, width, label=attribute, yerr = errorList, capsize = 5)
        ax1.bar_label(container=rects, padding=3, labels=sheafStrError)
    multiplier += 1
    iter+=1
    


    

ax1.set_ylabel('Balanced accuracy')
ax1.set_title('Balanced accuracy')
ax1.set_xticks(x + width, tasks)
ax1.legend(loc='upper left', ncols=3)
ax1.set_ylim(0, 1)


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
sheafStrError = list()

for bserr in baseErrorList:
    baseStrError.append('±' + str(bserr))

for sserr in errorList:
    sheafStrError.append('±' + str(sserr))

iter = 0
for attribute, measurement in data.items():
    offset = width * multiplier
    if(iter == 0):
        rects = ax2.bar(x + offset, measurement, width, label=attribute, yerr = baseErrorList, capsize = 5)
        ax2.bar_label(container=rects, padding=3, labels=baseStrError)
    else:
        rects = ax2.bar(x + offset, measurement, width, label=attribute, yerr = errorList, capsize = 5)
        ax2.bar_label(container=rects, padding=3, labels=sheafStrError)
        
    
    multiplier += 1
    iter+=1
    


    
ax2.set_ylabel('AUROC')
ax2.set_title('AUROC')
ax2.set_xticks(x + width, tasks)

ax2.set_ylim(0, 1)

plt.show()
  