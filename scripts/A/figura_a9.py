"""
Figura A.9 â€” Porcentaje de hogares con Servicios de Telecomunicaciones MÃ³viles
por decil de ingreso

Barras horizontales pareadas:
  - Rosa/salmÃ³n: % Hogares que disponen y gastan en telecomunicaciones mÃ³viles
  - Azul oscuro: % Hogares con telecomunicaciones mÃ³viles

Fuente: IFT con datos de la ENIGH 2022, del INEGI.
Datos disponibles en: https://www.inegi.org.mx/programas/enigh/nc/2022/.

MetodologÃ­a:
  - Deciles construidos sobre ingreso corriente total (ing_cor) de concentradohogar,
    ponderados por factor de expansiÃ³n.
  - "Con telecomunicaciones mÃ³viles": hogares con celular=1 (hogares.csv).
  - "Disponen y gastan": lo anterior AND comunica > 0 en concentradohogar.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
import matplotlib.ticker as mticker

# 1. Carga de microdatos ENIGH 2022
BASE = os.path.join(os.path.dirname(__file__), "..", "..", 'datos', 'A.7', 'microdatos')

# Cargar datos
concentrado = pd.read_csv(
    os.path.join(BASE, 'concentradohogar.csv'), low_memory=False,
    usecols=['folioviv', 'foliohog', 'ing_cor', 'factor', 'comunica'])
concentrado['ing_cor'] = pd.to_numeric(concentrado['ing_cor'], errors='coerce').fillna(0)
concentrado['comunica'] = pd.to_numeric(concentrado['comunica'], errors='coerce').fillna(0)

hogares = pd.read_csv(
    os.path.join(BASE, 'hogares.csv'), low_memory=False,
    usecols=['folioviv', 'foliohog', 'telefono', 'celular', 'tv_paga', 'conex_inte'])

df = concentrado.merge(hogares, on=['folioviv', 'foliohog'], how='left')

# 1b. Deciles de ingreso corriente
df = df.sort_values('ing_cor').reset_index(drop=True)
df['cum_factor'] = df['factor'].cumsum()
total_factor = df['factor'].sum()
df['pct_cum'] = df['cum_factor'] / total_factor
df['decil'] = pd.cut(
    df['pct_cum'], bins=np.linspace(0, 1, 11),
    labels=range(1, 11), include_lowest=True
).astype(int)

# 1c. Indicadores
df['tiene_moviles'] = (df['celular'] == 1).astype(int)
df['dg_moviles'] = ((df['tiene_moviles'] == 1) & (df['comunica'] > 0)).astype(int)

# 1d. Cálculo por decil
deciles = list(range(1, 11))
pct_con_telecom = []
pct_disponen_gastan = []

for d in deciles:
    sub = df[df['decil'] == d]
    w = sub['factor']
    pct_con_telecom.append(round((sub['tiene_moviles'] * w).sum() / w.sum() * 100, 1))
    pct_disponen_gastan.append(round((sub['dg_moviles'] * w).sum() / w.sum() * 100, 1))

# 2. Gráfica
fig, ax = plt.subplots(figsize=(14, 8.5))
fig.patch.set_facecolor('white')
ax.set_facecolor('#F8F8FA')

y_pos = np.arange(len(deciles))
bar_height = 0.38

# Colores estilo IFT
COLOR_DISPONEN = '#E8A8A0'    # Rosa/salmÃ³n
COLOR_CON_TELECOM = '#4A6FA5' # Azul

# Barras: % Hogares con telecomunicaciones móviles (barra inferior)
bars_con = ax.barh(y_pos - bar_height / 2, pct_con_telecom, height=bar_height,
                   color=COLOR_CON_TELECOM, edgecolor='none', zorder=2,
                   label='%Hogares con telecomunicaciones mÃ³viles')

# Barras: % Hogares que disponen y gastan (barra superior)
bars_dg = ax.barh(y_pos + bar_height / 2, pct_disponen_gastan, height=bar_height,
                  color=COLOR_DISPONEN, edgecolor='none', zorder=2,
                  label='%Hogares que disponen y gastan en telecomunicaciones mÃ³viles')

# 3. Anotaciones de valor
for i in range(len(deciles)):
    # Valor disponen y gastan
    ax.text(pct_disponen_gastan[i] + 0.5, y_pos[i] + bar_height / 2,
            f'{pct_disponen_gastan[i]:.1f}%',
            va='center', ha='left', fontsize=8.5, color='#555555',
            fontweight='bold')
    # Valor con telecomunicaciones
    ax.text(pct_con_telecom[i] + 0.5, y_pos[i] - bar_height / 2,
            f'{pct_con_telecom[i]:.1f}%',
            va='center', ha='left', fontsize=8.5, color='#555555',
            fontweight='bold')

# 4. Ejes
ax.set_yticks(y_pos)
ax.set_yticklabels(deciles, fontsize=11, fontweight='bold', color='#333333')
ax.set_ylabel('Decil de ingreso', fontsize=11, fontweight='bold',
              color='#333333', labelpad=10)

ax.set_xlim(0, 108)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{v:.0f}%'))
ax.tick_params(axis='x', labelsize=9, colors='#555555')

# Grid vertical suave
ax.grid(axis='x', alpha=0.2, color='#999999', zorder=0)

# Bordes
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#CCCCCC')
ax.spines['left'].set_color('#CCCCCC')

# 5. Título
fig.text(0.02, 0.96, 'â–  ', fontsize=12, color='#7B2D8E', fontweight='bold',
         transform=fig.transFigure, va='top')
fig.text(0.04, 0.965, 'Figura A.9.  ', fontsize=12, color='#333333',
         fontweight='bold', transform=fig.transFigure, va='top')
fig.text(0.115, 0.965,
         'Porcentaje de hogares con Servicios de Telecomunicaciones MÃ³viles '
         'por decil de ingreso',
         fontsize=12, color='#333333', transform=fig.transFigure, va='top')

# 6. Leyenda
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.12), ncol=2,
          fontsize=10, frameon=False, handlelength=2.5)

# 7. Notas al pie
note = ('Fuente: IFT con datos de la ENIGH 2022, del INEGI. '
        'Datos disponibles en: https://www.inegi.org.mx/programas/enigh/nc/2022/.')
fig.text(0.02, 0.01, note, fontsize=7.5, color='#555555',
         fontweight='bold', transform=fig.transFigure, va='bottom')

# 8. Guardar
fig.subplots_adjust(left=0.07, right=0.92, top=0.92, bottom=0.12)
output_path = os.path.join(os.path.dirname(__file__), "..", "..", 'output', 'Figura_A9.png')
# Guardar salida
fig.savefig(output_path, dpi=200, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print(f"GrÃ¡fica guardada en: {output_path}")
plt.close(fig)
