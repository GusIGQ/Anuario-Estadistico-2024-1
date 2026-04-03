"""
Figura A.3 – Índices de precios (INPC e IPCOM)

Reproduce la Gráfica del Anuario Estadístico 2024 del IFT (p. 13).
- Dos líneas: INPC (ascendente) e IPCOM (descendente).
- Datos a diciembre de cada año (2010-2023) y julio de 2024.
- Base: julio 2018 = 100.
- Columna 1 del CSV = INPC total, columna 9 = "08 Comunicaciones" (IPCOM).

Fuente: IFT con datos del INEGI a julio de 2024.
"""

import csv
import os
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
import matplotlib.ticker as mticker
import numpy as np

# 1. Leer datos
base = os.path.join(os.path.dirname(__file__), "..", "..", 'datos', 'A.3')
csv_path = os.path.join(base, 'INP_INP20260310133506.CSV')

# Leer con csv.reader para manejar el encabezado multi-línea
rows_data = []
with open(csv_path, 'r', encoding='latin-1') as f:
    reader = csv.reader(f)
    months = ('Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
              'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic')
    for row in reader:
        if len(row) == 14 and row[0].strip()[:3] in months:
            rows_data.append(row)

# 2. Filtrar: diciembre 2010-2023 + julio 2024
selected = []
for row in rows_data:
    fecha = row[0].strip()
    if fecha.startswith('Dic'):
        year = int(fecha.split()[1])
        if 2010 <= year <= 2023:
            selected.append((str(year), float(row[1]), float(row[9])))
    elif fecha == 'Jul 2024':
        selected.append(('2024*', float(row[1]), float(row[9])))

# Ordenar por año
selected.sort(key=lambda t: int(t[0].replace('*', '')))

years = [s[0] for s in selected]
inpc = [s[1] for s in selected]
ipcom = [s[2] for s in selected]

# 3. Imprimir tabla
print(f"{'año':<8} {'INPC':>10} {'IPCOM':>10}")
print("-" * 30)
for y, i, c in selected:
    print(f"{y:<8} {i:>10.2f} {c:>10.2f}")

# 4. Generar gráfica estilo IFT
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor('white')
ax.set_facecolor('#F8F8FA')

x = np.arange(len(years))

# Colores IFT
color_inpc = '#2B1055'   # Púrpura oscuro
color_ipcom = '#7B2D8E'  # Morado IFT

# Líneas
ax.plot(x, inpc, color=color_inpc, linewidth=2.5, zorder=4,
        marker='o', markersize=7, markerfacecolor=color_inpc,
        markeredgecolor='white', markeredgewidth=1.5,
        label='Índice Nacional de Precios al Consumidor (INPC)')

ax.plot(x, ipcom, color=color_ipcom, linewidth=2.5, zorder=4,
        marker='s', markersize=7, markerfacecolor=color_ipcom,
        markeredgecolor='white', markeredgewidth=1.5,
        label='Índice de Precios de Comunicaciones (IPCOM)')

# Etiquetas de datos (valores redondeados)
for i_idx in range(len(years)):
    # INPC etiqueta debajo de la línea
    ax.annotate(f'{round(inpc[i_idx])}', xy=(x[i_idx], inpc[i_idx]),
                xytext=(0, -16), textcoords='offset points',
                ha='center', va='top', fontsize=7.5, fontweight='bold',
                color=color_inpc,
                bbox=dict(boxstyle='round,pad=0.12', facecolor='white',
                          edgecolor='none', alpha=0.8))
    # IPCOM etiqueta arriba de la línea
    ax.annotate(f'{round(ipcom[i_idx])}', xy=(x[i_idx], ipcom[i_idx]),
                xytext=(0, 12), textcoords='offset points',
                ha='center', va='bottom', fontsize=7.5, fontweight='bold',
                color=color_ipcom,
                bbox=dict(boxstyle='round,pad=0.12', facecolor='white',
                          edgecolor='none', alpha=0.8))

# Ejes
ax.set_ylim(60, 170)
ax.yaxis.set_major_locator(mticker.MultipleLocator(10))
ax.tick_params(axis='y', labelsize=9, colors='#555555')
ax.set_xticks(x)
ax.set_xticklabels(years, fontsize=9, color='#333333', fontweight='bold')
ax.tick_params(axis='x', length=3, color='#CCCCCC')

# Cuadrícula
ax.grid(axis='y', alpha=0.25, color='#999999', zorder=0)

# Bordes
for spine in ax.spines.values():
    spine.set_color('#CCCCCC')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 5. Título
fig.text(0.02, 0.96, '■ ', fontsize=12, color='#7B2D8E', fontweight='bold',
         transform=fig.transFigure, va='top')
fig.text(0.04, 0.965, 'Figura A.3. ', fontsize=12, color='#333333',
         fontweight='bold', transform=fig.transFigure, va='top')
fig.text(0.115, 0.965, 'Índices de precios (INPC e IPCOM)',
         fontsize=12, color='#333333', transform=fig.transFigure, va='top')

# 6. Leyenda
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=2,
          fontsize=9.5, frameon=False, handlelength=2.5)

# 7. Notas al pie
note1 = ('Fuente: IFT con datos del INEGI a julio de 2024. Datos disponibles en: '
         'https://www.inegi.org.mx/app/indicesdeprecios/')
note2 = ('Notas: Base julio 2018 = 100. Los índices de 2010 a 2023 corresponden '
         'a diciembre de cada año, mientras que para el año 2024 a julio.')
fig.text(0.02, 0.01, note1, fontsize=7.5, color='#555555',
         transform=fig.transFigure, va='bottom')
fig.text(0.02, -0.02, note2, fontsize=7.5, color='#555555',
         transform=fig.transFigure, va='bottom')

# 8. Guardar
fig.subplots_adjust(left=0.06, right=0.97, top=0.92, bottom=0.14)

output_dir = os.path.join(os.path.dirname(__file__), "..", "..", 'output')
os.makedirs(output_dir, exist_ok=True)
output_png = os.path.join(output_dir, 'Figura_A3.png')
output_svg = os.path.join(output_dir, 'Figura_A3.svg')

plt.rcParams['svg.fonttype'] = 'none'

# Guardar salida PNG (alta resolución)
fig.savefig(output_png, dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print(f"\nGráfica guardada en versión PNG de alta resolución: {output_png}")

# Guardar salida SVG (vectorial escalable)
fig.savefig(output_svg, format='svg', bbox_inches='tight',
            facecolor='white', edgecolor='none')
print(f"Gráfica guardada en versión vectorial SVG editable: {output_svg}")

plt.close(fig)
