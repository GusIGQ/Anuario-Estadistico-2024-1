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
import matplotlib.ticker as mticker

# 1. Leer y limpiar
df = pd.read_csv(PROJECT_ROOT / "datos" / "C.8" / "TD_TRAF_HIST_TELMOVIL_ITE_VA.csv", encoding='latin1')

df['TRAF_SALIDA'] = (df['TRAF_SALIDA']
                     .astype(str)
                     .str.replace(',', '')
                     .str.strip())
df['TRAF_SALIDA'] = pd.to_numeric(df['TRAF_SALIDA'], errors='coerce')

# 2. Agregar por año y convertir a millones de minutos
trafico = df.groupby('ANIO')['TRAF_SALIDA'].sum() / 1_000_000
trafico = trafico.loc[1997:2023]

years  = trafico.index.astype(int).tolist()
values = trafico.values.tolist()

# 3. Figura
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# Área sombreada + línea
ax.fill_between(years, values, alpha=0.18, color='#5b9bd5', zorder=2)
ax.plot(years, values, color='#1f4e79', linewidth=1.8, zorder=3)

# Puntos en cada año
ax.scatter(years, values, color='#1f4e79', s=28, zorder=4)

# Etiquetas solo en extremos
ax.annotate(f'{round(values[0]):,}',
            xy=(years[0], values[0]),
            xytext=(years[0] + 0.3, values[0] + 8_000),
            fontsize=9, color='#1f4e79', fontweight='bold')

ax.annotate(f'{round(values[-1]):,}',
            xy=(years[-1], values[-1]),
            xytext=(years[-1] - 2.5, values[-1] + 8_000),
            fontsize=9, color='#1f4e79', fontweight='bold')

# 4. Ejes
ax.set_xlim(years[0] - 0.5, years[-1] + 0.5)
ax.set_ylim(0, max(values) * 1.18)

ax.set_xticks(years)
ax.set_xticklabels([str(y) for y in years], rotation=90, fontsize=8)

ax.yaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, _: f'{int(x):,}'))
ax.set_ylabel('Millones de minutos', fontsize=9, color='#555')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#ccc')
ax.spines['bottom'].set_color('#ccc')
ax.tick_params(colors='#555')
ax.yaxis.label.set_color('#555')

# 5. Título y fuente
fig.text(0.08, 0.96,
         'â–  Figura C.8.  TrÃ¡fico de salida del servicio mÃ³vil de telefonÃ­a (1997-2023)',
         fontsize=11, fontweight='bold', color='#1f4e79', va='top')

fig.text(0.08, 0.02,
         'Fuente: IFT con datos de los operadores de telecomunicaciones. '
         'Para cada aÃ±o los datos se presentan acumulados al mes de diciembre.',
         fontsize=7.5, color='#555')

plt.tight_layout(rect=[0, 0.05, 1, 0.94])
# Guardar salida
plt.savefig('output/Figura_C8.png', dpi=150, bbox_inches='tight')
plt.savefig('output/Figura_C8.pdf', bbox_inches='tight')
plt.show()
print("âœ… Figura C.8 guardada en output/")
