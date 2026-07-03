import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os 
from pathlib import Path


df = pd.read_csv("data\source_tables\performance_mean_sd_for_latex.csv")



x = np.linspace(0, 2, 322)
y = np.sin(x * 2)



fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Horizontally stacked subplots')
ax1.plot(x, y)
ax2.plot(x, -y)
