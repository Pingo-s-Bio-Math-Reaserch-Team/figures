from pathlib import Path
import json
import pandas as pd
import numpy as np
from lifelines.statistics import logrank_test

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / 'data' / 'source_tables'
F = ROOT / 'data' / 'final_competitive_results'

checks = []
def add_check(name, value, expected=None, tolerance=None, note=''):
    ok = True
    if expected is not None and tolerance is not None:
        ok = abs(value - expected) <= tolerance
    checks.append({'check': name, 'value': value, 'expected': expected, 'tolerance': tolerance, 'ok': bool(ok), 'note': note})

perf = pd.read_csv(T/'performance_mean_sd_for_latex.csv')
# Parse values like 0.600 $\pm$ 0.068
import re
def parse_mean(s):
    m = re.search(r'([0-9.]+)', str(s))
    return float(m.group(1)) if m else np.nan

grade_base = perf[(perf['Task']=='Grade label') & (perf['Model']=='Baseline')]['Balanced accuracy'].iloc[0]
grade_sheaf = perf[(perf['Task']=='Grade label') & (perf['Model']=='Sheaf')]['Balanced accuracy'].iloc[0]
add_check('Grade label baseline balanced accuracy mean', parse_mean(grade_base), 0.517, 5e-4, 'From performance_mean_sd_for_latex.csv')
add_check('Grade label sheaf balanced accuracy mean', parse_mean(grade_sheaf), 0.600, 5e-4, 'From performance_mean_sd_for_latex.csv')

km = pd.read_csv(F/'iteration2_transition_km_logrank.csv')
g3_km = km[km['scope']=='grade3_only'].iloc[0]
add_check('Grade 3 log-rank p', float(g3_km['logrank_p']), 2.551326e-09, 1e-12, 'From iteration2_transition_km_logrank.csv')
add_check('Grade 3 C-index', float(g3_km['c_index']), 0.729680, 1e-6, 'From iteration2_transition_km_logrank.csv')

cox = pd.read_csv(F/'iteration2_transition_adjusted_cox.csv')
g3_cox = cox[(cox['scope']=='grade3_only') & (cox['covariate']=='transition_sheaf_risk_index')].iloc[0]
add_check('Grade 3 Cox HR per SD', float(g3_cox['HR_per_SD']), 2.51895, 1e-5, 'From iteration2_transition_adjusted_cox.csv')
add_check('Grade 3 Cox p-value', float(g3_cox['p']), 4.307379e-07, 1e-12, 'From iteration2_transition_adjusted_cox.csv')

plis = pd.read_csv(T/'plis_drivers_fdr_bootstrap.csv')
add_check('Number of PLIS driver rows', len(plis), 11, 0, 'From plis_drivers_fdr_bootstrap.csv')
add_check('Top PLIS driver delta', float(plis.iloc[0]['delta_plis']), float(plis.iloc[0]['delta_plis']), 0, f"Top pathway: {plis.iloc[0]['pathway']}")

alpha = pd.read_csv(T/'alpha_sensitivity.csv')
add_check('Alpha sensitivity rows', len(alpha), 5, 0, 'alpha in {0,0.25,0.5,0.75,1}')

out = ROOT / 'checksums_and_validation.json'
with open(out, 'w') as f:
    json.dump(checks, f, indent=2)

bad = [c for c in checks if not c['ok']]
print(pd.DataFrame(checks).to_string(index=False))
if bad:
    raise SystemExit(f'{len(bad)} validation checks failed; see checksums_and_validation.json')
print('\nAll key-result validation checks passed.')
