import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os 
from pathlib import Path


df = pd.read_csv("data\source_tables\performance_mean_sd_for_latex.csv")

t = list(df['Task'])
tmp = set()

for str in t:
    if not(str in tmp):
        tmp.add(str)
        
tasks = tuple(tmp)
    


penguin_means = {
    'Bill Depth': (18.35, 18.43, 14.98),
    'Bill Length': (38.79, 48.83, 47.50),
    'Flipper Length': (189.95, 195.82, 217.19),
}

x = np.arange(len(tasks))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, (ax1, ax2) = plt.subplots(1, 2, layout='constrained')
fig.set_size_inches(10, 6)
for attribute, measurement in penguin_means.items():
    offset = width * multiplier
    rects = ax1.bar(x + offset, measurement, width, label=attribute)
    ax1.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax1.set_ylabel('Length (mm)')
ax1.set_title('Penguin attributes by species')
ax1.set_xticks(x + width, tasks)
ax1.legend(loc='upper left', ncols=3)
ax1.set_ylim(0, 250)

plt.show()