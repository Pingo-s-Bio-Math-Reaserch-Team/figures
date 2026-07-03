"""Reproduce all manuscript figures from bundled source tables.

This script does not generate or invent any result values. All plotted numerical
results are read from CSV files under data/source_tables or data/final_competitive_results.
Figure 1 is a deterministic schematic of the method and contains no empirical results.
"""
from pathlib import Path
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / 'data' / 'source_tables'
F = ROOT / 'data' / 'final_competitive_results'
FIG = ROOT / 'figures'
FIG.mkdir(exist_ok=True)

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['DejaVu Serif', 'Times New Roman', 'Liberation Serif'],
    'font.size': 8,
    'axes.titlesize': 9,
    'axes.labelsize': 8,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'legend.fontsize': 7,
    'figure.dpi': 300,
    'savefig.dpi': 600,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

def savefig(name):
    plt.tight_layout()
    plt.savefig(FIG / f'{name}.pdf', bbox_inches='tight')
    plt.savefig(FIG / f'{name}.png', bbox_inches='tight', dpi=600)
    plt.close()

def parse_pm(s):
    nums = re.findall(r'[0-9]+\.?[0-9]*', str(s))
    if len(nums) >= 2:
        return float(nums[0]), float(nums[1])
    if len(nums) == 1:
        return float(nums[0]), np.nan
    return np.nan, np.nan

def bh_stars(q):
    if q < 0.001: return '***'
    if q < 0.01: return '**'
    if q < 0.05: return '*'
    return 'ns'

# ---------------- Figure 1: architecture schematic ----------------
def fig1_architecture():
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    ax.axis('off')
    nodes = {
        'CNV': (0.08, 0.72),
        'Methylation': (0.08, 0.50),
        'miRNA/WES': (0.08, 0.28),
        'RNA': (0.34, 0.50),
        'Pathway': (0.58, 0.50),
        'Phenotype / survival': (0.84, 0.50),
        'Treatment-aware baseline B': (0.58, 0.17),
        'Orthogonal residuals S_perp': (0.84, 0.17),
    }
    def box(text, xy, w=0.16, h=0.10):
        x,y=xy
        rect = plt.Rectangle((x-w/2,y-h/2), w,h, fill=False, linewidth=1.2)
        ax.add_patch(rect)
        ax.text(x,y,text, ha='center', va='center', fontsize=8)
    for k,v in nodes.items():
        box(k,v, w=0.20 if 'Treatment' in k or 'Orthogonal' in k or 'Phenotype' in k else 0.16)
    def arrow(a,b,label=''):
        ax.annotate('', xy=nodes[b], xytext=nodes[a], arrowprops=dict(arrowstyle='->', lw=1.0))
        if label:
            xa,ya=nodes[a]; xb,yb=nodes[b]
            ax.text((xa+xb)/2, (ya+yb)/2+0.035, label, ha='center', fontsize=6)
    arrow('CNV','RNA','CNV->RNA')
    arrow('Methylation','RNA','Meth->RNA')
    arrow('miRNA/WES','RNA','miRNA/WES->RNA')
    arrow('RNA','Pathway','RNA->pathway')
    arrow('Pathway','Phenotype / survival','PLIS/SRIS')
    arrow('Pathway','Orthogonal residuals S_perp','S')
    arrow('Treatment-aware baseline B','Orthogonal residuals S_perp','S - QQ^T S')
    ax.text(0.5,0.92,'Multi-omics cellular sheaf architecture',ha='center',fontsize=10)
    ax.text(0.5,0.84,r'$r_e^\theta(p)=\rho_{u,e}^\theta(x_u(p))-x_v(p)$,  $\rho^\theta(x)=Ax+U\sigma(Vx+b)$',ha='center',fontsize=8)
    ax.text(0.5,0.06,r'Treatment-aware QR residualization: $S_\perp=S-QQ^\top S$, with $\operatorname{span}(Q)=\operatorname{col}(B)$',ha='center',fontsize=8)
    savefig('figure1_architecture_recreated')

# ---------------- Figure 2: performance ----------------
def fig2_performance():
    perf = pd.read_csv(T/'performance_mean_sd_for_latex.csv')
    rows=[]
    for _,r in perf.iterrows():
        ba_m,ba_sd = parse_pm(r['Balanced accuracy'])
        au_m,au_sd = parse_pm(r['AUROC'])
        rows.append({**r.to_dict(), 'BA_mean':ba_m, 'BA_sd':ba_sd, 'AUROC_mean':au_m, 'AUROC_sd':au_sd})
    d=pd.DataFrame(rows)
    tasks = d['Task'].unique().tolist()
    x=np.arange(len(tasks)); width=0.33
    fig, axes = plt.subplots(1,2,figsize=(7.2,2.8))
    for ax, metric, sd, title, ylabel in [
        (axes[0],'BA_mean','BA_sd','Balanced accuracy','Balanced accuracy'),
        (axes[1],'AUROC_mean','AUROC_sd','AUROC','AUROC')]:
        base=[]; base_sd=[]; sheaf=[]; sheaf_sd=[]
        for t in tasks:
            b=d[(d.Task==t)&(d.Model=='Baseline')].iloc[0]
            s=d[(d.Task==t)&(d.Model=='Sheaf')].iloc[0]
            base.append(b[metric]); base_sd.append(b[sd]); sheaf.append(s[metric]); sheaf_sd.append(s[sd])
        ax.bar(x-width/2,base,width,yerr=base_sd,capsize=2,label='Baseline')
        ax.bar(x+width/2,sheaf,width,yerr=sheaf_sd,capsize=2,label='Sheaf')
        ax.set_xticks(x); ax.set_xticklabels(tasks,rotation=20,ha='right')
        ax.set_ylabel(ylabel); ax.set_title(title); ax.set_ylim(0,1.05)
        for i,(b,s) in enumerate(zip(base,sheaf)):
            ax.text(i,max(b,s)+0.035,f'+{s-b:.3f}',ha='center',fontsize=7)
    axes[0].legend(frameon=False, loc='lower right')
    savefig('figure2_performance_ablation_recreated')

# ---------------- Figure 3: residual geometry + KM ----------------
def fig3_geometry_km():
    pt = pd.read_csv(F/'iteration2_patient_transition_risk_scores.csv')
    pathway_cols=[c for c in pt.columns if c.startswith('pathway_')]
    X=pt[pathway_cols].replace([np.inf,-np.inf],np.nan).fillna(pt[pathway_cols].median())
    Z=PCA(n_components=2,random_state=17).fit_transform(StandardScaler().fit_transform(X))
    pt['PC1']=Z[:,0]; pt['PC2']=Z[:,1]
    g3=pt[pt.grade==3].copy()
    cut=g3.transition_sheaf_risk_index.median()
    pt['group']='Other'
    pt.loc[(pt.grade==3)&(pt.transition_sheaf_risk_index<=cut),'group']='Grade 3 low'
    pt.loc[(pt.grade==3)&(pt.transition_sheaf_risk_index>cut),'group']='Grade 3 high'
    pt.loc[pt.grade==4,'group']='Grade 4'
    fig, axes=plt.subplots(1,2,figsize=(7.2,3.1))
    ax=axes[0]
    order=['Other','Grade 3 low','Grade 3 high','Grade 4']
    markers={'Other':'o','Grade 3 low':'o','Grade 3 high':'o','Grade 4':'^'}
    for group in order:
        sub=pt[pt.group==group]
        ax.scatter(sub.PC1,sub.PC2,s=10 if group=='Other' else 22,alpha=0.22 if group=='Other' else 0.75,label=group,marker=markers[group])
    g4=pt[pt.group=='Grade 4']
    ax.scatter(g4.PC1.mean(),g4.PC2.mean(),s=90,marker='*',label='Grade 4 centroid')
    ax.set_xlabel('PC1 of pathway residual space')
    ax.set_ylabel('PC2')
    ax.set_title('Residual geometry')
    ax.legend(frameon=False,fontsize=6)
    ax=axes[1]
    kmf=KaplanMeierFitter()
    g3_high=g3[g3.transition_sheaf_risk_index>cut]
    g3_low=g3[g3.transition_sheaf_risk_index<=cut]
    for label,sub in [('Low transition risk',g3_low),('High transition risk',g3_high)]:
        kmf.fit(sub.os_months,event_observed=sub.deceased,label=label)
        kmf.plot_survival_function(ax=ax,ci_show=False)
    lr=logrank_test(g3_high.os_months,g3_low.os_months,event_observed_A=g3_high.deceased,event_observed_B=g3_low.deceased)
    ax.set_title('Grade 3 survival')
    ax.set_xlabel('Overall survival (months)')
    ax.set_ylabel('Survival probability')
    ax.text(0.03,0.08,f'log-rank p={lr.p_value:.2e}',transform=ax.transAxes,fontsize=7)
    ax.legend(frameon=False,fontsize=7)
    # Simple risk table at selected times
    ticks=[0,24,48,72,96]
    ypos=-0.28
    ax.text(0.0,ypos,'At risk:',transform=ax.transAxes,fontsize=6)
    # use axis transform: map x tick data to axes fraction by xlim
    xmin,xmax=ax.get_xlim()
    for i,t in enumerate(ticks):
        frac=(t-xmin)/(xmax-xmin)
        ax.text(frac,ypos+0.06,str(t),transform=ax.transAxes,ha='center',fontsize=6)
        ax.text(frac,ypos-0.00,str((g3_low.os_months>=t).sum()),transform=ax.transAxes,ha='center',fontsize=6)
        ax.text(frac,ypos-0.06,str((g3_high.os_months>=t).sum()),transform=ax.transAxes,ha='center',fontsize=6)
    ax.text(-0.02,ypos-0.00,'Low',transform=ax.transAxes,ha='right',fontsize=6)
    ax.text(-0.02,ypos-0.06,'High',transform=ax.transAxes,ha='right',fontsize=6)
    savefig('figure3_transition_geometry_km_recreated')

# ---------------- Figure 4: PLIS drivers ----------------
def fig4_plis_drivers():
    d=pd.read_csv(T/'plis_drivers_fdr_bootstrap.csv').sort_values('delta_plis',ascending=True)
    fig, ax=plt.subplots(figsize=(3.6,3.2))
    xerr=np.vstack([d.delta_plis-d.ci_low,d.ci_high-d.delta_plis])
    ax.barh(d.pathway,d.delta_plis,xerr=xerr,capsize=2)
    ax.set_xlabel('Mean PLIS difference\nHigh-risk Grade 3 - Low-risk Grade 3')
    ax.set_title('Pathway-local drivers')
    for i,(_,r) in enumerate(d.iterrows()):
        ax.text(r.ci_high+0.15,i,bh_stars(r.q_value),va='center',fontsize=8)
    savefig('figure4_plis_drivers_fdr_ci_recreated')

# ---------------- Figure 5: alpha sensitivity ----------------
def fig5_alpha():
    d=pd.read_csv(T/'alpha_sensitivity.csv')
    fig, ax=plt.subplots(figsize=(3.6,2.5))
    ax.plot(d.alpha,d.grade3_c_index,marker='o',label='C-index')
    ax.set_xlabel('Alpha in transition index')
    ax.set_ylabel('Grade 3 C-index')
    ax2=ax.twinx()
    ax2.plot(d.alpha,-np.log10(d.logrank_p),marker='s',linestyle='--',label='-log10 p')
    ax2.set_ylabel('-log10(log-rank p)')
    ax.set_title('Alpha sensitivity')
    savefig('figure5_alpha_sensitivity_recreated')

# ---------------- Figure 6: calibration ----------------
def fig6_calibration():
    d=pd.read_csv(T/'calibration_summary_v3.csv')
    tasks=d.task.unique().tolist(); x=np.arange(len(tasks)); width=0.33
    fig, axes=plt.subplots(1,2,figsize=(7.2,2.6))
    for ax, metric, title in [(axes[0],'brier','Brier score'),(axes[1],'ece','Expected calibration error')]:
        base=[]; sheaf=[]
        for t in tasks:
            base.append(d[(d.task==t)&(d.model=='Baseline')][metric].iloc[0])
            sheaf.append(d[(d.task==t)&(d.model=='Sheaf')][metric].iloc[0])
        ax.bar(x-width/2,base,width,label='Baseline')
        ax.bar(x+width/2,sheaf,width,label='Sheaf')
        ax.set_xticks(x); ax.set_xticklabels(tasks,rotation=20,ha='right')
        ax.set_title(title)
        ax.set_ylabel(metric.upper())
    axes[0].legend(frameon=False)
    savefig('figure6_calibration_metrics_recreated')

# ---------------- Figure 7: CPLIS distribution ----------------
def fig7_cplis():
    pt=pd.read_csv(T/'cplis_patient_table.csv')
    grades=[2,3,4]
    data=[pt[pt.grade==g].CPLIS.dropna() for g in grades]
    fig, ax=plt.subplots(figsize=(3.4,2.5))
    ax.boxplot(data,labels=[f'Grade {g}' for g in grades],showfliers=False)
    means=[v.mean() for v in data]
    ax.plot(np.arange(1,4),means,marker='o',linestyle='--',label='Mean')
    ax.set_ylabel('CPLIS')
    ax.set_title('Concentrated PLIS by grade')
    ax.legend(frameon=False)
    savefig('figure7_cplis_distribution_recreated')

if __name__ == '__main__':
    fig1_architecture()
    fig2_performance()
    fig3_geometry_km()
    fig4_plis_drivers()
    fig5_alpha()
    fig6_calibration()
    fig7_cplis()
    print(f'Recreated figures saved in {FIG}')
