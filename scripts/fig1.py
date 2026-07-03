import matplotlib.pyplot as plt
import textwrap

fig, ax = plt.subplots(figsize=(15, 6))
from matplotlib.patches import Rectangle

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_axis_off()

def addbox(ax, x, y, width, height, text, fontsize=13, wrap_chars=None):
    box = Rectangle((x, y), width, height, fill=False, linewidth = 1, clip_on=False)
    ax.add_patch(box)
    if wrap_chars is not None:
        text = '\n'.join(textwrap.wrap(text, width=wrap_chars))
    ax.text(x + width/2, y + height/2, text, ha='center', va='center', fontsize=fontsize, transform=ax.transAxes)

def addarrow(ax, start, end, label=None, fontsize = 12, offset = 0.035, xoffset=0):
    ax.annotate("", xy=end, xytext=start, arrowprops=dict(arrowstyle="->", linewidth=1))
    x1, y1 = start
    x2, y2 = end

    ax.text((x1 + x2)/2 + xoffset, (y1 + y2)/2 + offset, label, ha='center', va='center', fontsize=fontsize, transform=ax.transAxes)


addbox(ax, 0.025, 0.65, 0.2, 0.1, 'CNV')
addbox(ax, 0.025, 0.35, 0.2, 0.1, 'Methylation')
addbox(ax, 0.025, 0.05, 0.2, 0.1, 'miRNA/WES')

addbox(ax, 0.275, 0.35, 0.2, 0.1, 'RNA')
addbox(ax, 0.525, 0.35, 0.2, 0.1, 'Pathway')
addbox(ax, 0.775, 0.35, 0.2, 0.1, 'Phenotype Survival')
addbox(ax, 0.525, 0.05, 0.2, 0.15, 'Baseline covariates (age, IDH, MGMT, grade; treatment if available)', wrap_chars=34)
addbox(ax, 0.775, 0.05, 0.2, 0.1, r'$S_{\perp} = S - QQ^{\top}S$')

addarrow(ax, (0.225, 0.65), (0.275, 0.45), r'$\rho_e^\theta$')
addarrow(ax, (0.225, 0.4), (0.275, 0.4), r'$\rho_e^\theta$')
addarrow(ax, (0.225, 0.15), (0.275, 0.35), r'$\rho_e^\theta$')

addarrow(ax, (0.475, 0.4), (0.525, 0.4), 'PLIS')

addarrow(ax, (0.725, 0.4), (0.775, 0.4), 'T(p)')

addarrow(ax, (0.725, 0.35), (0.775, 0.15), 'Residual matrix S', 12, 0.035, 0.045)

addarrow(ax, (0.725, 0.1), (0.775, 0.1), 'QR')

ax.text(0.5, 0.95, 'Multi-Omics Cellular-Sheaf Architecture', ha='center', va='center', fontsize=20, transform=ax.transAxes)
ax.text(0.5, 0.9, r'Low-rank neural restriction map: $\rho_e^\theta$(x) = $A_e$x + $U_e\sigma$($V_e$x+$b_e$)', ha='center', va='center', fontsize=16, transform=ax.transAxes)


plt.tight_layout()
plt.savefig('fig1.png', dpi=300, bbox_inches='tight')

plt.show()