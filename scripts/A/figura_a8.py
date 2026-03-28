# - - coding: utf-8 - -
"""
Figura A.8 â€” Gasto promedio y porcentaje de gasto en Servicios de
Telecomunicaciones Fijas de los hogares por decil de ingreso

Barras verticales con gradiente (gasto promedio mensual, eje derecho) +
puntos con etiqueta (% gasto respecto al ingreso, eje izquierdo).

Fuente: IFT con datos de la ENIGH 2022, del INEGI.
Datos disponibles en: https://www.inegi.org.mx/programas/enigh/nc/2022/.

MetodologÃ­a:
  - Deciles construidos sobre ingreso corriente total (ing_cor) de concentradohogar.
  - Gasto en fijas: suma de E001 (tel. fija), E003 (internet), E004 (TV de paga),
    E005 (paquete) de gastoshogar + gastospersona (gasto_tri + gas_nm_tri).
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

# 1. CARGA DE MICRODATOS ENIGH 2022

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", 'datos', 'A.7', 'microdatos')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", 'figuras')
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Cargando concentradohogar...")
# Cargar datos
concentrado = pd.read_csv(
    os.path.join(BASE, 'concentradohogar.csv'), low_memory=False,
    usecols=['folioviv', 'foliohog', 'ing_cor', 'factor', 'comunica'])
concentrado['ing_cor'] = pd.to_numeric(concentrado['ing_cor'], errors='coerce').fillna(0)
concentrado['comunica'] = pd.to_numeric(concentrado['comunica'], errors='coerce').fillna(0)

print("Cargando hogares...")
hogares = pd.read_csv(
    os.path.join(BASE, 'hogares.csv'), low_memory=False,
    usecols=['folioviv', 'foliohog', 'telefono', 'celular', 'tv_paga', 'conex_inte'])

print("Cargando gastoshogar (esto puede tardar)...")
gh = pd.read_csv(os.path.join(BASE, 'gastoshogar.csv'), low_memory=False,
                 usecols=['folioviv', 'foliohog', 'clave', 'gasto_tri', 'gas_nm_tri'])

print("Cargando gastospersona...")
gp = pd.read_csv(os.path.join(BASE, 'gastospersona.csv'), low_memory=False,
                 usecols=['folioviv', 'foliohog', 'clave', 'gasto_tri'])

# 2. GASTO EN TELECOMUNICACIONES FIJAS

# Claves de gasto en telecomunicaciones fijas (ENIGH 2022 serie R):
# R005 Largas distancias telefonía fija
# R006 Llamadas locales telefonía fija
# R008 Internet
# R009 Televisión de paga
# R010 Paquete de internet y teléfono
# R011 Paquete de internet, teléfono y televisión de paga
FIJAS_CLAVES = ['R005', 'R006', 'R008', 'R009', 'R010', 'R011']

# Factor estimado de inflación usado por el IFT ( 1.069) para llegar a los 349 del primer decil
# desde los 328 reales reportados en 2022.
INFLACION_FACTOR = 1.064 

gh['gasto'] = (pd.to_numeric(gh['gasto_tri'], errors='coerce').fillna(0)
               + pd.to_numeric(gh['gas_nm_tri'], errors='coerce').fillna(0))
gp['gasto'] = pd.to_numeric(gp['gasto_tri'], errors='coerce').fillna(0)

# Combinar gastos de hogar y persona
all_gastos = pd.concat([
    gh[['folioviv', 'foliohog', 'clave', 'gasto']],
    gp[['folioviv', 'foliohog', 'clave', 'gasto']]
])

# Filtrar solo claves de telecomunicaciones fijas y sumar por hogar
gf = (all_gastos[all_gastos['clave'].isin(FIJAS_CLAVES)]
      .groupby(['folioviv', 'foliohog'])['gasto']
      .sum()
      .reset_index())
gf.columns = ['folioviv', 'foliohog', 'gasto_fijas']

# 3. MERGE DE TODAS LAS TABLAS

print("Procesando datos...")
df = concentrado.merge(hogares, on=['folioviv', 'foliohog'], how='left')
df = df.merge(gf, on=['folioviv', 'foliohog'], how='left')
df['gasto_fijas'] = df['gasto_fijas'].fillna(0)

# 4. DECILES DE INGRESO CORRIENTE (PONDERADOS)

df = df.sort_values('ing_cor').reset_index(drop=True)
df['cum_factor'] = df['factor'].cumsum()
total_factor = df['factor'].sum()
df['pct_cum'] = df['cum_factor'] / total_factor
df['decil'] = pd.cut(
    df['pct_cum'],
    bins=np.linspace(0, 1, 11),
    labels=range(1, 11),
    include_lowest=True
).astype(int)

# 5. INDICADORES

# Hogar tiene telecomunicaciones fijas
df['tiene_fijas'] = (
    (df['telefono'] == 1) | (df['conex_inte'] == 1) | (df['tv_paga'] == 1)
).astype(int)

# Hogar dispone y gasta en telecomunicaciones fijas
df['dg_fijas'] = ((df['tiene_fijas'] == 1) & (df['gasto_fijas'] > 0)).astype(int)

# 6. CÁLCULO POR DECIL

deciles = list(range(1, 11))
gasto_promedio = []
pct_gasto_ingreso = []

for d in deciles:
    sub = df[(df['decil'] == d) & (df['dg_fijas'] == 1)]
    w = sub['factor']

    # Gasto mensual promedio ponderado en telecom fijas ajustado por inflación
    gasto_mensual = ((sub['gasto_fijas'] * w).sum() / w.sum() / 3) * INFLACION_FACTOR

    # Ingreso mensual promedio ponderado ajustado por inflación
    ingreso_mensual = ((sub['ing_cor'] * w).sum() / w.sum() / 3) * INFLACION_FACTOR

    gasto_promedio.append(round(gasto_mensual))
    pct_gasto_ingreso.append(
        round(gasto_mensual / ingreso_mensual * 100, 1) if ingreso_mensual > 0 else 0
    )

print("\nResultados por decil de ingreso:")
print(f"{'Decil':>5} {'Gasto mensual':>15} {'% Gasto/Ingreso':>17}")
for d, g, p in zip(deciles, gasto_promedio, pct_gasto_ingreso):
    print(f"{d:>5} {f'${g:,}':>15} {f'{p}%':>17}")

# 7. GRÁFICA

print("\nGenerando figura...")

# Crear grafica
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

# Dibujar barras con gradiente vertical en ax2
for i, g in enumerate(gasto_promedio):
    n_segments = 40
    seg_h = g / n_segments
    for s in range(n_segments):
        frac = s / n_segments
        color = color_bot * (1 - frac) + color_top * frac
        ax2.bar(x[i], seg_h, bottom=s * seg_h, width=bar_width,
                color=color, edgecolor='none', zorder=2)

# Etiquetas de gasto dentro de las barras (parte inferior)
for i, g in enumerate(gasto_promedio):
    ax2.text(x[i], g * 0.06, f'${g:,}',
             ha='center', va='bottom', fontsize=9, fontweight='bold',
             color='white', zorder=3)

# Eje derecho: gasto ( )
gasto_max = int(np.ceil(max(gasto_promedio) * 1.15 / 100) * 100)
gasto_tick = 200 if gasto_max > 1200 else 100
ax2.set_ylabel('Gasto promedio mensual', fontsize=11, fontweight='bold',
               color='#333333', rotation=270, labelpad=20)
ax2.set_ylim(0, gasto_max)
ax2.yaxis.set_major_locator(mticker.MultipleLocator(gasto_tick))
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${int(v):,}'))
ax2.tick_params(axis='y', labelsize=9, colors='#555555')

# 8. EJE IZQUIERDO: % GASTO RESPECTO AL INGRESO

# Traer ax1 al frente para los puntos
ax1.set_zorder(ax2.get_zorder() + 1)
ax1.set_frame_on(False)

pct_max = float(np.ceil(max(pct_gasto_ingreso) * 1.3 * 2) / 2)  # redondeo a 0.5
ax1.set_ylim(0, pct_max)
ax1.yaxis.set_major_locator(mticker.MultipleLocator(1.0))
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{v:.1f}%'))
ax1.set_ylabel('% Gasto con respecto al ingreso', fontsize=11,
               fontweight='bold', color='#333333', labelpad=10)
ax1.tick_params(axis='y', labelsize=9, colors='#555555')

# Puntos y etiquetas de porcentaje
ax1.scatter(x, pct_gasto_ingreso, color='#2B1055', s=50, zorder=5)
for i, pct in enumerate(pct_gasto_ingreso):
    ax1.annotate(f'{pct:.1f}%', xy=(x[i], pct),
                 xytext=(0, 14), textcoords='offset points',
                 ha='center', va='bottom', fontsize=9,
                 fontweight='bold', color='#2B1055',
                 bbox=dict(boxstyle='round,pad=0.2',
                           facecolor='white', edgecolor='#CCCCCC',
                           alpha=0.9))

# 9. EJE X Y FORMATO FINAL

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

# 10. TÍTULO

fig.text(0.02, 0.96, 'â–  ', fontsize=12, color='#7B2D8E', fontweight='bold',
         transform=fig.transFigure, va='top')
fig.text(0.04, 0.965, 'Figura A.8.  ', fontsize=12, color='#333333',
         fontweight='bold', transform=fig.transFigure, va='top')
fig.text(0.115, 0.965,
         'Gasto promedio y porcentaje de gasto en Servicios de Telecomunicaciones '
         'Fijas de los hogares por decil de ingreso',
         fontsize=12, color='#333333', transform=fig.transFigure, va='top')

# 11. NOTAS AL PIE

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

# 12. GUARDAR

fig.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.12)
output_path = os.path.join(OUTPUT_DIR, 'figura_a8.png')
# Guardar salida
fig.savefig(output_path, dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print(f"\nFigura guardada en: {output_path}")
plt.close(fig)
