# - - coding: utf-8 - -
"""
Figura A.7 — Porcentaje de hogares con servicios de telecomunicaciones
fijas por decil de ingreso

Gráfica de barras horizontales agrupadas con dos métricas:
  1. % Hogares con telecomunicaciones fijas
  2. % Hogares que disponen y gastan en telecomunicaciones fijas

Fuente: IFT con datos de la ENIGH 2022, del INEGI.
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

# 1. CARGA DE MICRODATOS ENIGH 2022

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", 'datos', 'A.7-A.8-A.9-A.10', 'microdatos')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Cargando concentradohogar...")
# Cargar datos
concentrado = pd.read_csv(
    os.path.join(BASE, 'concentradohogar.csv'), low_memory=False,
    usecols=['folioviv', 'foliohog', 'ing_cor', 'factor'])
concentrado['ing_cor'] = pd.to_numeric(concentrado['ing_cor'], errors='coerce').fillna(0)

print("Cargando hogares...")
hogares = pd.read_csv(
    os.path.join(BASE, 'hogares.csv'), low_memory=False,
    usecols=['folioviv', 'foliohog', 'telefono', 'tv_paga', 'conex_inte'])

print("Cargando gastoshogar...")
gh = pd.read_csv(os.path.join(BASE, 'gastoshogar.csv'), low_memory=False,
                 usecols=['folioviv', 'foliohog', 'clave', 'gasto_tri', 'gas_nm_tri'])

print("Cargando gastospersona...")
gp = pd.read_csv(os.path.join(BASE, 'gastospersona.csv'), low_memory=False,
                 usecols=['folioviv', 'foliohog', 'clave', 'gasto_tri'])

# 2. GASTO EN TELECOMUNICACIONES FIJAS

FIJAS_CLAVES = ['R005', 'R006', 'R008', 'R009', 'R010', 'R011']

gh['gasto'] = (pd.to_numeric(gh['gasto_tri'], errors='coerce').fillna(0)
               + pd.to_numeric(gh['gas_nm_tri'], errors='coerce').fillna(0))
gp['gasto'] = pd.to_numeric(gp['gasto_tri'], errors='coerce').fillna(0)

all_gastos = pd.concat([
    gh[['folioviv', 'foliohog', 'clave', 'gasto']],
    gp[['folioviv', 'foliohog', 'clave', 'gasto']]
])

gf = (all_gastos[all_gastos['clave'].isin(FIJAS_CLAVES)]
      .groupby(['folioviv', 'foliohog'])['gasto']
      .sum()
      .reset_index())
gf.columns = ['folioviv', 'foliohog', 'gasto_fijas']

# 3. MERGE DE TABLAS Y DECILES

print("Calculando indicadores y deciles...")
df = concentrado.merge(hogares, on=['folioviv', 'foliohog'], how='left')
df = df.merge(gf, on=['folioviv', 'foliohog'], how='left')
df['gasto_fijas'] = df['gasto_fijas'].fillna(0)

# Deciles usando pct_cum ponderado
df = df.sort_values('ing_cor').reset_index(drop=True)
df['pct_cum'] = df['factor'].cumsum() / df['factor'].sum()
df['decil'] = pd.cut(df['pct_cum'], bins=np.linspace(0, 1, 11), labels=range(1, 11), include_lowest=True).astype(int)

# 4. INDICADORES

# Hogares que reportan equipos OR reportan gasto (Métrica oficial del IFT 35.4% D1)
df['tiene_fijas'] = ((df['telefono'] == 1) | (df['conex_inte'] == 1) | (df['tv_paga'] == 1) | (df['gasto_fijas'] > 0)).astype(int)

# Hogares que disponen y además tienen gasto documentado (Métrica Coral IFT 29% D1)
# Usando la definicion estricta eq + gasto para acercarnos al target conservador del IFT.
df['tiene_eq'] = ((df['telefono'] == 1) | (df['conex_inte'] == 1) | (df['tv_paga'] == 1)).astype(int)
df['dg_fijas'] = ((df['tiene_eq'] == 1) & (df['gasto_fijas'] > 0)).astype(int)

deciles = list(range(1, 11))
pct_tienen = []
pct_disponen_gastan = []

for d in deciles:
    sub = df[df['decil'] == d]
    tot = sub['factor'].sum()

    t = sub[sub['tiene_fijas'] == 1]['factor'].sum() / tot * 100
    dg = sub[sub['dg_fijas'] == 1]['factor'].sum() / tot * 100

    pct_tienen.append(t)
    pct_disponen_gastan.append(dg)

# 5. GRÁFICA A.7 EXACTA

print("\nGenerando figura A.7...")
# Crear grafica
fig, ax = plt.subplots(figsize=(14, 8))
fig.patch.set_facecolor('white')
ax.set_facecolor('#F8F8FA')

# Configuración de barras
y = np.arange(len(deciles))
bar_width = 0.35

# Colores fieles a la gráfica
color_tienen = '#4A6FA5'
color_gastan = '#F2998A'

# Barras horizontales (Decil 10 arriba - invertimos el eje Y luego)
bars1 = ax.barh(y - bar_width/2, pct_tienen, bar_width, label='%Hogares con telecomunicaciones fijas', color=color_tienen)
bars2 = ax.barh(y + bar_width/2, pct_disponen_gastan, bar_width, label='%Hogares que disponen y gastan en telecomunicaciones fijas', color=color_gastan)

# Formatear el eje X para que no se muestre y usar Data Labels
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.set_xticks([])

# Eje Y: Deciles
ax.set_yticks(y)
ax.set_yticklabels(deciles, fontsize=10, color='#555555')
ax.set_ylabel('Decil de ingreso', fontsize=11, color='#555555')
ax.invert_yaxis()  # Decil 1 abajo, Decil 10 arriba
ax.spines['left'].set_color('#CCCCCC')

# Agregar los % al final de las barras
for bar in bars1:
    width = bar.get_width()
    ax.text(width + 0.5, bar.get_y() + bar.get_height()/2, f'{width:.1f}%',
            ha='left', va='center', fontsize=9, color='#555555', fontweight='bold')

for bar in bars2:
    width = bar.get_width()
    ax.text(width + 0.5, bar.get_y() + bar.get_height()/2, f'{width:.1f}%',
            ha='left', va='center', fontsize=9, color='#555555', fontweight='bold')

# Título de la Gráfica
fig.text(0.04, 0.94, '■ ', fontsize=12, color='#F2998A', fontweight='bold', transform=fig.transFigure)
fig.text(0.06, 0.94, 'Figura A.7. ', fontsize=12, color='#333333', fontweight='bold', transform=fig.transFigure)
fig.text(0.14, 0.94, 'Porcentaje de hogares con servicios de telecomunicaciones fijas por decil de ingreso',
         fontsize=12, color='#555555', transform=fig.transFigure)

# Panel Izquierdo: Texto Descriptivo
fig.text(0.02, 0.65, 'INGRESO Y GASTO\nDE LOS HOGARES EN\nTELECOMUNICACIONES FIJAS',
         fontsize=14, color='#2B1055', fontweight='bold', ha='left')

texto_lateral = (
    "Los resultados de la Encuesta Nacional de\n"
    "Ingresos y Gastos de los Hogares (ENIGH)\n"
    "2022 indican que, en el segmento de las\n"
    "telecomunicaciones fijas, a mayor nivel de\n"
    "ingresos, mayor es el porcentaje de hogares\n"
    "que gastan y disponen de servicios fijos de\n"
    "telecomunicacionesÂ¹."
)
fig.text(0.02, 0.40, texto_lateral, fontsize=11, color='#000000', ha='left',
         bbox=dict(boxstyle='round,pad=1.5', facecolor='white', edgecolor='#E0E0E0'))

# Leyenda manual abajo al centro
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False, fontsize=10)

# Notas al pie
nota_fuente = 'Fuente: IFT con datos de la ENIGH 2022, del INEGI. Datos disponibles en: https://www.inegi.org.mx/programas/enigh/nc/2022/.'
nota_decil = 'Â¹ El valor de los deciles de ingreso se encuentra disponible en: https://www.inegi.org.mx/temas/ingresoshog/default.html#Informacion_general.'
fig.text(0.3, 0.05, nota_fuente, fontsize=8, color='#555555', transform=fig.transFigure)
fig.text(0.02, -0.01, nota_decil, fontsize=8, color='#0066CC', transform=fig.transFigure)

# Ajustes de layout para espacio del panel izquierdo (30%)
plt.subplots_adjust(left=0.3, right=0.95, top=0.88, bottom=0.15)

# Guardar
output_path = os.path.join(OUTPUT_DIR, 'figura_a7.png')
# Guardar salida
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Figura guardada en: {output_path}")
plt.close()
