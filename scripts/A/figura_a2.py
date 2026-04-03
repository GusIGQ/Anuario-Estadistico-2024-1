import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
import matplotlib.patches as patches
import os
import matplotlib.colors as mcolors

# Create directory
output_dir = os.path.join(os.path.dirname(__file__), "..", "..", 'output')
os.makedirs(output_dir, exist_ok=True)

# Load data
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "..", "..", 'datos', 'A.2', 'datos_a2_extracted.csv'))
# Calculate totals
df['total'] = df['telecom'] + df['radio']
df['pct_telecom'] = (df['telecom'] / df['total']) * 100
df['pct_radio'] = (df['radio'] / df['total']) * 100

# Colors
color_tel = '#29618C' # Telecomunicaciones (dark blue)
color_tel_bot = '#1D4E72' # Darker at bottom
color_rad = '#ADE5E7' # Radiodifusión (light green/blue)
color_rad_bot = '#8BC6CA' # Darker at bottom

# Crear grafica
fig, ax = plt.subplots(figsize=(15, 8.5))
fig.patch.set_facecolor('#FDFDFD')
ax.set_facecolor('#FDFDFD')

x = np.arange(len(df))
width = 0.5

# We will draw gradient stacked bars using small segments
for i, row in df.iterrows():
    p_tel = row['pct_telecom']
    p_rad = row['pct_radio']

    # Draw telecom gradient (bottom to top)
    n_seg = 30
    h_seg = p_tel / n_seg
    for s in range(n_seg):
        frac = s / n_seg
        c = np.array(mcolors.to_rgb(color_tel_bot)) * (1 - frac) + np.array(mcolors.to_rgb(color_tel)) * frac
        # To make rounded bottom, we can draw a FancyBboxPatch instead, but simpler with a small shift or just let it be flat
        ax.bar(x[i], h_seg, bottom=s*h_seg, width=width, color=c, edgecolor='none', zorder=2)

    # Draw radio gradient
    h_seg2 = p_rad / n_seg
    for s in range(n_seg):
        frac = s / n_seg
        c2 = np.array(mcolors.to_rgb(color_rad_bot)) * (1 - frac) + np.array(mcolors.to_rgb(color_rad)) * frac
        ax.bar(x[i], h_seg2, bottom=p_tel + s*h_seg2, width=width, color=c2, edgecolor='none', zorder=2)

    # Rounded bottom effect (a semicircle patch at bottom)
    circ = patches.Ellipse((x[i], 0), width, 4, color=color_tel_bot, zorder=1)
    ax.add_patch(circ)

    # Callouts
    val_tel_pct = f"{p_tel:.1f}%"
    val_rad_pct = f"{p_rad:.1f}%"

    # Left callout for telecom
    ax.annotate(val_tel_pct, 
                xy=(x[i] - width/2, p_tel / 2),
                xytext=(-15, 0), textcoords="offset points",
                ha='right', va='center',
                fontsize=9, fontweight='heavy', color='#47476F',
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=1.0, zorder=5), zorder=6)

    # Right callout for radio
    ax.annotate(val_rad_pct, 
                xy=(x[i] + width/2, p_tel + p_rad / 2),
                xytext=(15, 0), textcoords="offset points",
                ha='left', va='center',
                fontsize=9, fontweight='heavy', color='#47476F',
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=1.0, zorder=5), zorder=6)

    # Total over the bar
    total_val = row['total']
    ax.text(x[i], 103, f"{total_val:,.0f}",
            ha='center', va='bottom', fontsize=8, color='#AAAAAA', fontweight='bold', zorder=4)

# Custom X axis
quarter_labels = []
for idx, q in enumerate(df['quarter']):
    if q == 1: quarter_labels.append("I")
    elif q == 2: quarter_labels.append("II")
    elif q == 3: quarter_labels.append("III")
    elif q == 4: quarter_labels.append("IV")

ax.set_xticks(x)
ax.set_xticklabels(quarter_labels, fontsize=10, fontweight='bold', color='#888888')

# Draw vertical lines between years
years = df['year'].values
for i in range(1, len(years)):
    if years[i] != years[i-1]:
        ax.axvline(x=i-0.5, ymin=0, ymax=0.03, color='#888888', lw=1.5, clip_on=False)

# Draw Years
unique_years = df['year'].unique()
for y in unique_years:
    idx = df.index[df['year'] == y].tolist()
    if len(idx) > 1:
        mid_x = (idx[0] + idx[-1]) / 2
    else:
        mid_x = idx[0]
    ax.text(mid_x, -10, str(y), ha='center', va='top', fontsize=10, fontweight='bold', color='#555555')

ax.set_ylim(0, 115)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_yticks([])

# Title
fig.text(0.04, 0.94, '■ ', fontsize=12, color='#EDA396', fontweight='bold', va='top')
fig.text(0.06, 0.94, 'Figura A.2. ', fontsize=13, color='#555577', fontweight='bold', va='top')
fig.text(0.12, 0.94, 'Empleo en los sectores de telecomunicaciones y radiodifusión', 
         fontsize=13, color='#777799', va='top')

# Legend
fig.text(0.40, 0.15, '■ ', fontsize=14, color=color_tel, fontweight='bold', va='center')
fig.text(0.42, 0.15, 'Telecomunicaciones', fontsize=11, color='#444455', fontweight='bold', va='center')
fig.text(0.55, 0.15, '■ ', fontsize=14, color=color_rad, fontweight='bold', va='center')
fig.text(0.57, 0.15, 'Radiodifusión', fontsize=11, color='#444455', fontweight='bold', va='center')

# Note
note1 = "Fuente: IFT con datos de la Encuesta Nacional de Ocupación y Empleo (ENOE) del INEGI, con cifras a junio 2024.\nDatos disponibles en https://www.inegi.org.mx/programas/enoe/15ymas/default.html#Microdatos\nNotas: Para el año 2020 se considera la información al primer y cuarto trimestre."
fig.text(0.04, 0.03, note1, fontsize=9, color='#777777', va='bottom', linespacing=1.5)

# Y-axis label
fig.text(0.03, 0.5, "POBLACIÓN OCUPADA EN TYR Y DISTRIBUCIÓN POR SECTOR", 
         rotation=90, va='center', ha='center', fontsize=9, color='#888888', fontweight='bold')

plt.subplots_adjust(bottom=0.25, left=0.08, right=0.95, top=0.88)
# Guardar salida
plt.savefig(os.path.join(output_dir, "Figura_A2.png"), dpi=300, facecolor='#FDFDFD')
print("Figura A.2 generada en output/Figura_A2.png")
