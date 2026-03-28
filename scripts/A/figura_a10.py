"""
Figura A.10 â€” Gasto promedio y porcentaje de gasto en Servicios de
Telecomunicaciones MÃ³viles de los hogares por decil de ingreso

Barras verticales con gradiente (gasto promedio mensual, eje derecho) +
puntos con etiqueta (% gasto respecto al ingreso, eje izquierdo).

Fuente: IFT con datos de la ENIGH 2022, del INEGI.
Datos disponibles en: https://www.inegi.org.mx/programas/enigh/nc/2022/.

MetodologÃ­a:
  - Deciles construidos sobre ingreso corriente total (ing_cor) de concentradohogar.
  - Gasto en mÃ³viles: clave E002 (celular) de gastoshogar + gastospersona
    (gasto_tri + gas_nm_tri).
  - Promedios para hogares que disponen y gastan (tienen el servicio Y comunica > 0).
  - Gasto mensual = gasto_tri / 3.
  - % gasto = gasto_mensual / (ing_cor / 3) Ã— 100.
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
import matplotlib.colors as mcolors

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

# Gastos en telecomunicaciones móviles desde gastoshogar + gastospersona
gh = pd.read_csv(os.path.join(BASE, 'gastoshogar.csv'), low_memory=False,
                 usecols=['folioviv', 'foliohog', 'clave', 'gasto_tri', 'gas_nm_tri'])
gp = pd.read_csv(os.path.join(BASE, 'gastospersona.csv'), low_memory=False,
                 usecols=['folioviv', 'foliohog', 'clave', 'gasto_tri'])

gh['gasto'] = (pd.to_numeric(gh['gasto_tri'], errors='coerce').fillna(0)
               + pd.to_numeric(gh['gas_nm_tri'], errors='coerce').fillna(0))
gp['gasto'] = pd.to_numeric(gp['gasto_tri'], errors='coerce').fillna(0)

MOVILES_CLAVES = ['E002']
all_gastos = pd.concat([gh[['folioviv', 'foliohog', 'clave', 'gasto']],
                        gp[['folioviv', 'foliohog', 'clave', 'gasto']]])
gm = (all_gastos[all_gastos['clave'].isin(MOVILES_CLAVES)]
      .groupby(['folioviv', 'foliohog'])['gasto'].sum().reset_index())
gm.columns = ['folioviv', 'foliohog', 'gasto_moviles']

df = concentrado.merge(hogares, on=['folioviv', 'foliohog'], how='left')
df = df.merge(gm, on=['folioviv', 'foliohog'], how='left')
df['gasto_moviles'] = df['gasto_moviles'].fillna(0)

# 1b. Deciles de ingreso corriente
df = df.sort_values('ing_cor').reset_index(drop=True)
df['cum_factor'] = df['factor'].cumsum()
df['pct_cum'] = df['cum_factor'] / df['factor'].sum()
df['decil'] = pd.cut(
    df['pct_cum'], bins=np.linspace(0, 1, 11),
    labels=range(1, 11), include_lowest=True
).astype(int)

# 1c. Indicadores
df['tiene_moviles'] = (df['celular'] == 1).astype(int)
df['dg_moviles'] = ((df['tiene_moviles'] == 1) & (df['comunica'] > 0)).astype(int)

# 1d. Cálculo por decil
deciles = list(range(1, 11))
gasto = []
pct_gasto = []

for d in deciles:
    sub = df[(df['decil'] == d) & (df['dg_moviles'] == 1)]
    w = sub['factor']
    gasto_mensual = (sub['gasto_moviles'] * w).sum() / w.sum() / 3
    ingreso_mensual = (sub['ing_cor'] * w).sum() / w.sum() / 3
    gasto.append(round(gasto_mensual))
    pct_gasto.append(round(gasto_mensual / ingreso_mensual * 100, 1) if ingreso_mensual > 0 else 0)

# 2. Gráfica
fig, ax1 = plt.subplots(figsize=(14, 8.5))
fig.patch.set_facecolor('white')
ax1.set_facecolor('#F8F8FA')

x = np.arange(len(deciles))
bar_width = 0.6

# Gradiente vertical para barras (púrpura oscuro arriba azul claro abajo)
color_top = np.array(mcolors.to_rgb('#2B1055'))
color_bot = np.array(mcolors.to_rgb('#7597C9'))

# Crear eje derecho para gasto
ax2 = ax1.twinx()

# Dibujar barras con gradiente en ax2 (escala de gasto)
for i, g in enumerate(gasto):
    n_segments = 40
    seg_h = g / n_segments
    for s in range(n_segments):
        frac = s / n_segments
        color = color_bot * (1 - frac) + color_top * frac
        ax2.bar(x[i], seg_h, bottom=s * seg_h, width=bar_width,
                color=color, edgecolor='none', zorder=2)

# Etiquetas de gasto dentro de las barras
for i, g in enumerate(gasto):
    ax2.text(x[i], g * 0.06, f'${g:,}',
             ha='center', va='bottom', fontsize=9, fontweight='bold',
             color='white', zorder=3)

# eje derecho: gasto ( ) límite dinámico
gasto_max = int(np.ceil(max(gasto) * 1.15 / 100) * 100)
gasto_tick = 200 if gasto_max > 1200 else 100
ax2.set_ylabel('Gasto promedio mensual', fontsize=11, fontweight='bold',
               color='#333333', rotation=270, labelpad=20)
ax2.set_ylim(0, gasto_max)
ax2.yaxis.set_major_locator(mticker.MultipleLocator(gasto_tick))
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${int(v):,}'))
ax2.tick_params(axis='y', labelsize=9, colors='#555555')

# 3. Eje izquierdo: % gasto
# Traer ax1 al frente para los puntos
ax1.set_zorder(ax2.get_zorder() + 1)
ax1.set_frame_on(False)

pct_max = float(np.ceil(max(pct_gasto) * 1.3 * 2) / 2)  # redondeo a 0.5
ax1.set_ylim(0, pct_max)
ax1.yaxis.set_major_locator(mticker.MultipleLocator(0.5))
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{v:.1f}%'))
ax1.set_ylabel('% Gasto con respecto al ingreso', fontsize=11,
               fontweight='bold', color='#333333', labelpad=10)
ax1.tick_params(axis='y', labelsize=9, colors='#555555')

# Puntos y etiquetas de porcentaje
ax1.scatter(x, pct_gasto, color='#2B1055', s=50, zorder=5)
for i, pct in enumerate(pct_gasto):
    ax1.annotate(f'{pct:.1f}%', xy=(x[i], pct),
                 xytext=(0, 14), textcoords='offset points',
                 ha='center', va='bottom', fontsize=9,
                 fontweight='bold', color='#2B1055',
                 bbox=dict(boxstyle='round,pad=0.2',
                           facecolor='white', edgecolor='#CCCCCC',
                           alpha=0.9))

# 4. Eje X
ax1.set_xticks(x)
ax1.set_xticklabels(deciles, fontsize=11, fontweight='bold', color='#333333')
ax1.set_xlabel('Decil de ingreso', fontsize=11, fontweight='bold',
               color='#333333', labelpad=10)
ax1.set_xlim(-0.6, len(deciles) - 0.4)

# Grid
ax1.grid(axis='y', alpha=0.2, color='#999999', zorder=0)

# Bordes
ax2.spines['top'].set_visible(False)
ax2.spines['bottom'].set_color('#CCCCCC')
ax2.spines['right'].set_color('#CCCCCC')

# 5. Título
fig.text(0.02, 0.96, 'â–  ', fontsize=12, color='#7B2D8E', fontweight='bold',
         transform=fig.transFigure, va='top')
fig.text(0.04, 0.965, 'Figura A.10.  ', fontsize=12, color='#333333',
         fontweight='bold', transform=fig.transFigure, va='top')
fig.text(0.12, 0.965,
         'Gasto promedio y porcentaje de gasto en Servicios de Telecomunicaciones '
         'MÃ³viles de los hogares por decil de ingreso',
         fontsize=12, color='#333333', transform=fig.transFigure, va='top')

# 6. Notas al pie
note = ('Fuente: IFT con datos de la ENIGH 2022, del INEGI. '
        'Datos disponibles en: https://www.inegi.org.mx/programas/enigh/nc/2022/.')
note2 = ('Notas: El gasto e ingreso utilizados para los porcentajes son el '
         'promedio para los hogares de cada decil de ingreso que disponen del '
         'servicio y gastan en Ã©l. Las cifras de ingresos y gastos fueron\n'
         'ajustadas con base a la inflaciÃ³n para reflejar su valor real en '
         'tÃ©rminos comparativos.')
fig.text(0.02, 0.015, note, fontsize=7.5, color='#555555',
         fontweight='bold', transform=fig.transFigure, va='bottom')
fig.text(0.02, -0.02, note2, fontsize=7.5, color='#555555',
         transform=fig.transFigure, va='bottom', linespacing=1.4)

# 7. Guardar
fig.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.12)
output_path = os.path.join(os.path.dirname(__file__), "..", "..", 'output', 'Figura_A10.png')
# Guardar salida
fig.savefig(output_path, dpi=200, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print(f"GrÃ¡fica guardada en: {output_path}")
plt.close(fig)
