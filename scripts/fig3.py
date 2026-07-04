import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os 
from pathlib import Path


df = pd.read_csv("iteration2_patient_transition_risk_scores.csv")

plt.tight_layout()
plt.savefig('fig4.png', dpi=300, bbox_inches='tight')
plt.show()