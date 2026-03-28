"""

Figura A.1 - Producto Interno Bruto (PIB) y contribuciÃ³n del PIB
de los subsectores de telecomunicaciones y radiodifusiÃ³n.

Reproduce la grÃ¡fica exacta del Anuario EstadÃ­stico 2024 del IFT.
- Datos TRIMESTRALES de 2013-I a 2024-II
- Barras: PIB nacional en miles de millones de pesos (precios de 2018)
- LÃ­nea: ParticipaciÃ³n TyR = (517 Telecomunicaciones + 515 Radio y TV) / PIB

Fuente: INEGI / IFT con datos a junio de 2024.

"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
import matplotlib.ticker as mticker
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import os
import numpy as np

# 1. Leer datos
base = os.path.join(os.path.dirname(__file__), "..", "..", 'datos', 'A.1', 'tabulados_PIBT')
path = os.path.join(base, 'PIBT_2.xlsx')
# Cargar datos
df = pd.read_excel(path, sheet_name='Tabulado', header=None)

# Filas clave (bloque 1: Millones de pesos a precios de 2018 )
ROW_PIB = 7          # Producto interno bruto
ROW_TELECOM = 155    # 517 - Telecomunicaciones
ROW_RADIO_TV = 154   # 515 - Radio y televisiÃ³n

# 2. Extraer datos trimestrales 2013-2024
# Cada año ocupa 7 columnas: T1, T2, T3, T4, 6 Meses, 9 Meses, Anual
# col_start para un año 1 + (año - 1993) 7
# T1 +0, T2 +1, T3 +2, T4 +3

quarters_data = []  # lista de (etiqueta, pib, telecom, radio_tv)

for year in range(2013, 2025):
    col_start = 1 + (year - 1993) * 7
    # Determinar cuántos trimestres para este año
    max_q = 4 if year < 2024 else 2  # Solo Q1-Q2 para 2024
    for q in range(max_q):
        col = col_start + q
        if col >= df.shape[1]:
            break
        pib_val = df.iloc[ROW_PIB, col]
        tel_val = df.iloc[ROW_TELECOM, col]
        rtv_val = df.iloc[ROW_RADIO_TV, col]
        if pd.notna(pib_val):
            label = f"{year}-T{q+1}"
            quarters_data.append({
                'label': label,
                'year': year,
                'quarter': q + 1,
                'pib': float(pib_val),
                'telecom': float(tel_val) if pd.notna(tel_val) else 0,
                'radio_tv': float(rtv_val) if pd.notna(rtv_val) else 0,
            })

qdf = pd.DataFrame(quarters_data)
# PIB en miles de millones de pesos
qdf['pib_mmdp'] = qdf['pib'] / 1_000
# Participación TyR (%) (telecom + radio_tv) / pib 100
qdf['tyr'] = qdf['telecom'] + qdf['radio_tv']
qdf['pct_tyr'] = qdf['tyr'] / qdf['pib'] * 100

# 3. Imprimir tabla
print(f"{'Trim':<12} {'PIB (MDP)':>14} {'Telecom':>12} {'Radio/TV':>12} "
      f"{'TyR':>12} {'% TyR':>8}")
print("-" * 75)
for _, r in qdf.iterrows():
    print(f"{r['label']:<12} {r['pib']:>14,.0f} {r['telecom']:>12,.0f} "
          f"{r['radio_tv']:>12,.0f} {r['tyr']:>12,.0f} {r['pct_tyr']:>8.2f}%")

# 4. Generar gráfica estilo IFT
fig, ax1 = plt.subplots(figsize=(18, 8.5))
fig.patch.set_facecolor('white')
ax1.set_facecolor('#F8F8FA')

n = len(qdf)
x = np.arange(n)

# --- Barras con gradiente vertical (oscuro arriba, claro abajo) ---
# Colores del gradiente IFT (púrpura oscuro azul claro)
color_top = np.array(mcolors.to_rgb('#2B1055'))     # PÃºrpura oscuro
color_bot = np.array(mcolors.to_rgb('#7597C9'))     # Azul claro
bar_width = 0.72

for i, (_, row) in enumerate(qdf.iterrows()):
    h = row['pib_mmdp']
    n_segments = 40
    seg_h = h / n_segments
    for s in range(n_segments):
        frac = s / n_segments  # 0=bottom, 1=top
        color = color_bot * (1 - frac) + color_top * frac
        ax1.bar(x[i], seg_h, bottom=s * seg_h, width=bar_width,
                color=color, edgecolor='none', zorder=2)

# --- Eje Y izquierdo: PIB ---
ax1.set_ylabel('PIB Nacional en miles de millones de pesos',
               fontsize=11, fontweight='bold', color='#333333', labelpad=10)
ax1.set_ylim(0, 30000)
ax1.yaxis.set_major_locator(mticker.MultipleLocator(5000))
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(
    lambda v, _: f'{int(v):,}'.replace(',', ',')))
ax1.tick_params(axis='y', labelsize=9, colors='#555555')

# --- Eje X: etiquetas trimestre II y IV debajo, años centrados ---
# Marcas menores en cada trimestre, etiquetas solo en II y IV
ax1.set_xticks(x)
xlabels = []
for _, row in qdf.iterrows():
    q = int(row['quarter'])
    if q == 2:
        xlabels.append('II')
    elif q == 4:
        xlabels.append('IV')
    else:
        xlabels.append('')
ax1.set_xticklabels(xlabels, fontsize=8, color='#555555')
ax1.tick_params(axis='x', length=3, color='#CCCCCC')

# Etiquetas de año centradas debajo
prev_year = None
year_positions = []
for i, (_, row) in enumerate(qdf.iterrows()):
    yr = int(row['year'])
    if yr != prev_year:
        year_start = i
        prev_year = yr
    # Cuando cambia año o es el último, marcar centro
    next_yr = int(qdf.iloc[i + 1]['year']) if i + 1 < n else -1
    if next_yr != yr:
        center = (year_start + i) / 2
        year_positions.append((center, yr))

for cx, yr in year_positions:
    ax1.text(cx, -1700, str(yr), ha='center', va='top',
             fontsize=9, fontweight='bold', color='#333333')

# --- Eje Y derecho: Participación TyR ---
ax2 = ax1.twinx()
pct_vals = qdf['pct_tyr'].values

ax2.plot(x, pct_vals, color='#6B6B6B', linewidth=2, zorder=4,
         marker='o', markersize=5, markerfacecolor='#8B78A8',
         markeredgecolor='white', markeredgewidth=1.2)

ax2.set_ylabel('Porcentaje de participaciÃ³n de los subsectores de las TyR',
               fontsize=10, fontweight='bold', color='#333333',
               rotation=270, labelpad=22)
ax2.set_ylim(0, 1.8)
ax2.yaxis.set_major_locator(mticker.MultipleLocator(0.2))
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(
    lambda v, _: f'{v:.1f}%'))
ax2.tick_params(axis='y', labelsize=9, colors='#555555')

# --- Anotaciones de porcentaje (en Q2 y Q4 de cada año) ---
for i, (_, row) in enumerate(qdf.iterrows()):
    q = int(row['quarter'])
    if q == 2 or q == 4:
        pct = row['pct_tyr']
        ax2.annotate(f'{pct:.1f}%', xy=(x[i], pct),
                     xytext=(0, 14), textcoords='offset points',
                     ha='center', va='bottom', fontsize=7.5,
                     fontweight='bold', color='#1A1A2E',
                     bbox=dict(boxstyle='round,pad=0.15',
                               facecolor='white', edgecolor='none',
                               alpha=0.75))

# --- Título ---
fig.text(0.02, 0.96,
         'â–  ', fontsize=12, color='#7B2D8E', fontweight='bold',
         transform=fig.transFigure, va='top')
fig.text(0.04, 0.965,
         'Figura A.1.  ', fontsize=12, color='#333333', fontweight='bold',
         transform=fig.transFigure, va='top')
fig.text(0.115, 0.965,
         'Producto Interno Bruto (PIB) y contribuciÃ³n del PIB de los subsectores '
         'de telecomunicaciones y radiodifusiÃ³n',
         fontsize=12, color='#333333',
         transform=fig.transFigure, va='top')

# --- Leyenda ---
bar_patch = mpatches.Patch(facecolor='#3D2070', edgecolor='none',
                           label='PIB nacional')
line_patch = plt.Line2D([0], [0], color='#6B6B6B', marker='o',
                        markersize=6, markerfacecolor='#8B78A8',
                        markeredgecolor='white', linewidth=2,
                        label='ParticipaciÃ³n TyR')
ax1.legend(handles=[bar_patch, line_patch], loc='lower center',
           bbox_to_anchor=(0.5, -0.16), ncol=2, fontsize=10,
           frameon=False, handlelength=2.5)

# --- Notas al pie ---
note1 = ('Fuente: IFT con datos del INEGI a junio de 2024. '
         'Datos disponibles en: https://www.inegi.org.mx/temas/pib/.')
note2 = ('Notas: PIB a precios constantes de 2018. La participaciÃ³n de los '
         'subsectores de TyR corresponde a la contribuciÃ³n del sector 51 '
         '(InformaciÃ³n en medios masivos) de acuerdo con el Sistema de\n'
         'ClasificaciÃ³n Industrial de AmÃ©rica del Norte, MÃ©xico SCIAN 2023.')
fig.text(0.02, 0.01, note1, fontsize=7.5, color='#555555',
         transform=fig.transFigure, va='bottom')
fig.text(0.02, -0.025, note2, fontsize=7.5, color='#555555',
         transform=fig.transFigure, va='bottom')

# --- Ajustes finales ---
ax1.set_xlim(-0.8, n - 0.2)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.spines['bottom'].set_color('#CCCCCC')
ax1.spines['left'].set_color('#CCCCCC')
ax1.spines['right'].set_color('#CCCCCC')
ax2.spines['bottom'].set_color('#CCCCCC')
ax2.spines['left'].set_color('#CCCCCC')
ax2.spines['right'].set_color('#CCCCCC')
ax1.grid(axis='y', alpha=0.25, color='#999999', zorder=0)

fig.subplots_adjust(left=0.07, right=0.93, top=0.92, bottom=0.15)

# Guardar
output_path = os.path.join(os.path.dirname(__file__), "..", "..", 'output', 'Figura_A1.png')
# Guardar salida
fig.savefig(output_path, dpi=200, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print(f"\nGrÃ¡fica guardada en: {output_path}")
plt.close(fig)
