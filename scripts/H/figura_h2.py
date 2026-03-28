import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import numpy as np
import matplotlib.ticker as ticker

# 1. Cargar y procesar los datos
df = pd.read_csv(PROJECT_ROOT / "datos" / "H.2" / "TD_CONSUMO_GENERO_VA.csv", encoding='latin1')

# Corregir problemas de codificación de texto y estandarizar nombres como en el PDF
df['GENERO'] = df['GENERO'].replace({
    'PelÃƒ\xadculas': 'PelÃ­culas',
    'ReligiÃƒÂ³n': 'ReligiÃ³n',
    'Comicos': 'CÃ³micos',
    'Dramatizado unitario': 'Dramatizado\nunitario',
    'Reality Show': 'Reality\nShow',
    'Talk Show': 'Talk\nShow'
})

# Ordenar alfabéticamente para que coincida con el eje X del diseño original
df = df.sort_values(by='GENERO').reset_index(drop=True)

# Calcular Rating a Porcentaje
df['RATING_PCT'] = df['PORC_RATING'] * 100

# 2. Configuración de la figura y diseño base
fig, ax1 = plt.subplots(figsize=(16, 5), facecolor='white')

# Posiciones y variables visuales
x = np.arange(len(df['GENERO']))
width = 0.35
color_rating = '#3E3466'  # Morado oscuro original (Rating Total)
color_horas = '#FFA08A'   # Durazno/SalmÃ³n original (Puntos de horas)

# 3. Eje Principal Izquierdo: Gráfica de Barras para Rating (%)
bars = ax1.bar(x, df['RATING_PCT'], width, color=color_rating, zorder=3)
ax1.set_ylabel('Rating (%)', fontsize=9, fontstyle='italic', color='#555555')
ax1.set_ylim(0, 3.5)
ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
ax1.set_yticks(np.arange(0, 3.51, 0.5))
ax1.tick_params(axis='y', labelsize=8, colors='#555555')

# 4. Eje Secundario Derecho: Gráfica de Puntos para Horas de programación
ax2 = ax1.twinx()
dots = ax2.scatter(x, df['HORAS_PROGRAMACION'], color=color_horas, s=150, zorder=4, alpha=0.9)
ax2.set_ylabel('Horas de programaciÃ³n (#)', fontsize=9, fontstyle='italic', color='#555555', rotation=-90, labelpad=15)
ax2.set_ylim(0, 21600)
ax2.set_yticks(np.arange(0, 21601, 2400))
ax2.tick_params(axis='y', labelsize=8, colors='#555555')

# 5. Estilos: Cuadrículas y Bordes
ax1.grid(axis='y', linestyle='-', color='#E5E5E5', zorder=0)
ax1.grid(axis='x', linestyle='-', color='#E5E5E5', zorder=0)

for spine in ax1.spines.values(): spine.set_visible(False)
for spine in ax2.spines.values(): spine.set_visible(False)

# Etiquetas del eje X
ax1.set_xticks(x)
ax1.set_xticklabels(df['GENERO'], fontsize=7.5, color='#444444')
ax1.tick_params(axis='x', length=0)

# 6. Leyenda y Títulos a la medida
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

legend_elements = [
    mpatches.Rectangle((0,0), 1, 1, color=color_rating, label='Rating Total personas'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=color_horas, markersize=10, label='Horas de programaciÃ³n')
]

fig.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False, fontsize=9)

plt.text(0.12, -0.05, "Horas dedicadas y rating\npromedio por gÃ©nero en\ncanales nacionales", 
         transform=fig.transFigure, fontsize=10, ha='center', va='center',
         bbox=dict(boxstyle="round,pad=1.2", facecolor='#F9F9F9', edgecolor='#E0E0E0', alpha=0.8))

plt.subplots_adjust(bottom=0.15)
# Guardar salida
plt.savefig(PROJECT_ROOT / "output" / "figura_h2.png", dpi=300, bbox_inches='tight')
