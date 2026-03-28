"""
Figura C.14 â€” TrÃ¡fico del servicio mÃ³vil de acceso a Internet (2015-2023)
Fuente: IFT con datos de los operadores de telecomunicaciones.
CSV: TD_TRAF_INTMOVIL_ITE_VA.csv

METODOLOGÃA:
- Se suman TODOS los meses de cada aÃ±o (el trÃ¡fico es acumulado anual, no snapshot)
- El denominador de los porcentajes es TOTAL_TB_E (incluye trÃ¡fico no especificado)
- El orden de apilado es: 2G (abajo), 3G (medio), 4G (arriba)
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import matplotlib.patches as mpatches
import numpy as np
import os

# 1. LECTURA
CSV = PROJECT_ROOT / "datos" / "C.14" / "TD_TRAF_INTMOVIL_ITE_VA.csv"
# Cargar datos
df = pd.read_csv(CSV, encoding='latin-1')

for col in ['TRAF_TB_2G_E', 'TRAF_TB_3G_E', 'TRAF_TB_4G_E', 'TOTAL_TB_E']:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# 2. CÁLCULO
# Sumar TODOS los meses del año (flujo acumulado anual)
df_f = df[(df['ANIO'] >= 2015) & (df['ANIO'] <= 2023)]

g = df_f.groupby('ANIO')[
    ['TRAF_TB_2G_E', 'TRAF_TB_3G_E', 'TRAF_TB_4G_E', 'TOTAL_TB_E']
].sum()

# Porcentajes sobre TOTAL_TB_E (denominador incluye tráfico no especificado)
g['PCT_2G'] = (g['TRAF_TB_2G_E'] / g['TOTAL_TB_E'] * 100).round(1)
g['PCT_3G'] = (g['TRAF_TB_3G_E'] / g['TOTAL_TB_E'] * 100).round(1)
g['PCT_4G'] = (g['TRAF_TB_4G_E'] / g['TOTAL_TB_E'] * 100).round(1)

anios  = g.index.tolist()
h_2g   = g['TRAF_TB_2G_E'].tolist()
h_3g   = g['TRAF_TB_3G_E'].tolist()
h_4g   = g['TRAF_TB_4G_E'].tolist()
total  = g['TOTAL_TB_E'].tolist()
pct_2g = g['PCT_2G'].tolist()
pct_3g = g['PCT_3G'].tolist()
pct_4g = g['PCT_4G'].tolist()

# 3. COLORES (fieles al Anuario IFT)
COLOR_2G   = '#D94F3D'   # rojo-salmÃ³n oscuro (franja pequeÃ±a, base)
COLOR_3G   = '#F0A896'   # salmÃ³n claro (franja media)
COLOR_4G   = '#2E3B7A'   # azul marino (franja dominante)
COLOR_TEXT = '#1E2A5E'

# 4. FIGURA
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

x     = np.arange(len(anios))
width = 0.52

# Barras apiladas: 2G (abajo) 3G (medio) 4G (arriba)
ax.bar(x, h_2g, width, color=COLOR_2G, zorder=3)
ax.bar(x, h_3g, width, bottom=h_2g,   color=COLOR_3G, zorder=3)
ax.bar(x, h_4g, width,
       bottom=[a + b for a, b in zip(h_2g, h_3g)],
       color=COLOR_4G, zorder=3)

# 5. ETIQUETAS DE PORCENTAJE DENTRO DE CADA SEGMENTO
for i in range(len(anios)):
    mid_2g = h_2g[i] / 2
    mid_3g = h_2g[i] + h_3g[i] / 2
    mid_4g = h_2g[i] + h_3g[i] + h_4g[i] / 2

    # 2G solo si el segmento es visible
    if pct_2g[i] >= 0.1:
        ax.text(x[i], mid_2g, f'{pct_2g[i]}%',
                ha='center', va='center',
                color='white', fontsize=8, fontweight='bold')

    # 3G posición izquierda del segmento (igual que el Anuario)
    ax.text(x[i] - width/2 - 0.04, mid_3g, f'{pct_3g[i]}%',
            ha='right', va='center',
            color=COLOR_TEXT, fontsize=8, fontweight='bold')

    # 4G posición izquierda del segmento
    ax.text(x[i] - width/2 - 0.04, mid_4g, f'{pct_4g[i]}%',
            ha='right', va='center',
            color=COLOR_TEXT, fontsize=8, fontweight='bold')

# 6. ETIQUETA TOTAL ENCIMA DE CADA BARRA
for i in range(len(anios)):
    ax.text(x[i], total[i] * 1.015,
            f'{total[i]:,.0f}',
            ha='center', va='bottom',
            fontsize=7.8, color=COLOR_TEXT, fontweight='bold')

# 7. ESTILO EJES
ax.set_xticks(x)
ax.set_xticklabels([str(a) for a in anios], fontsize=10, color='#444')
ax.set_xlim(-0.6, len(anios) - 0.4)
ax.set_ylim(0, max(total) * 1.16)
ax.yaxis.set_visible(False)
for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#cccccc')
ax.tick_params(axis='x', length=0)
ax.grid(False)

# 8. LEYENDA
patches = [
    mpatches.Patch(color=COLOR_2G, label='TrÃ¡fico 2G'),
    mpatches.Patch(color=COLOR_3G, label='TrÃ¡fico 3G'),
    mpatches.Patch(color=COLOR_4G, label='TrÃ¡fico 4G'),
]
ax.legend(handles=patches, loc='lower center', frameon=False,
          fontsize=9.5, ncol=3, bbox_to_anchor=(0.5, -0.1))

# 9. TÍTULO Y FUENTE
fig.text(0.04, 0.97,
         'Figura C.14. TrÃ¡fico del servicio mÃ³vil de acceso a Internet (2015-2023)',
         ha='left', va='top', fontsize=11, fontweight='bold', color=COLOR_TEXT)
fig.text(0.04, -0.03,
         'Fuente: IFT con datos de los operadores de telecomunicaciones. '
         'Para cada aÃ±o los datos se presentan acumulados al mes de diciembre.',
         ha='left', va='bottom', fontsize=7.5, color='gray')

plt.tight_layout(rect=[0, 0.04, 1, 0.96])

os.makedirs('output', exist_ok=True)
# Guardar salida
plt.savefig('output/Figura_C14.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("âœ…  Guardada: output/Figura_C14.png")

# 10. VERIFICACI N EN CONSOLA
print("\nâ”€â”€ Valores calculados vs Anuario â”€â”€")
anuario_total = {2015:270026, 2016:623944, 2017:1212063, 2018:2092039,
                 2019:3965441, 2020:5282622, 2021:6314845, 2022:7712771, 2023:8750075}
anuario_pct   = {
    2015:(3.5,29.2,67.3), 2016:(1.9,37.6,60.5), 2017:(0.7,46.0,53.3),
    2018:(0.3,32.8,66.9), 2019:(0.2,23.3,76.5), 2020:(0.1,18.8,81.0),
    2021:(0.1,14.6,84.6), 2022:(0.1,11.3,85.5), 2023:(0.1,9.3,83.5),
}
print(f"{'AÃ±o':>4} | {'Total CSV':>12} | {'Total ANU':>12} | {'2G csv/anu':>12} | {'3G csv/anu':>12} | {'4G csv/anu':>12}")
print("-" * 75)
for i, a in enumerate(anios):
    a2, a3, a4 = anuario_pct[a]
    print(f"{a} | {total[i]:>12,.0f} | {anuario_total[a]:>12,} | "
          f"{pct_2g[i]:>5}/{a2:<5} | {pct_3g[i]:>5}/{a3:<5} | {pct_4g[i]:>5}/{a4:<5}")
