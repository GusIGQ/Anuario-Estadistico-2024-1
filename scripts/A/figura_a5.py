"""
Figura A.5 — Inversión Extranjera Directa (IED) en telecomunicaciones

Gráfica de barras horizontales:
  - Barra larga (azul claro): IED total de México (millones de dólares)
  - Barra corta (púrpura oscuro): IED en Telecomunicaciones (sector 517 SCIAN)

Datos actualizados al 3er trimestre de 2025.
Período: 2013-2024 (2024 acumulado a junio).

Fuente: Secretaría de Economía – Registro Nacional de Inversiones Extranjeras.
"""

import os
import numpy as np
import openpyxl
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
import matplotlib.ticker as mticker

# 1. Leer datos
base = os.path.join(os.path.dirname(__file__), "..", "..", 'datos', 'A.5')

# --- IED total de México (datos actualizados) ---
wb1 = openpyxl.load_workbook(
    os.path.join(base, 'Datos_originales_y_actualizacion__1_.xlsx'),
    data_only=True)
ws1 = wb1['Preliminares y actualización']

total_ied = {}
for r in range(3, ws1.max_row + 1):
    yr = ws1.cell(r, 1).value
    period = ws1.cell(r, 2).value
    val = ws1.cell(r, 4).value  # Columna D = datos actualizados
    if yr and period and val:
        yr = int(yr)
        if 2013 <= yr <= 2024:
            if yr < 2024 and 'diciembre' in str(period):
                total_ied[yr] = float(val)
            elif yr == 2024 and 'junio' in str(period):
                total_ied[yr] = float(val)
wb1.close()

# --- IED en telecomunicaciones (sector 517, datos actualizados) ---
wb2 = openpyxl.load_workbook(
    os.path.join(base, '2025_3T_Flujosportipodeinversion_actu__3_.xlsx'),
    data_only=True, read_only=True)
ws2 = wb2['Por sector']

YEAR_START = 2006
telecom_ied = {}
for row in ws2.iter_rows(min_row=5, max_col=80, values_only=False):
    cell_a = str(row[0].value) if row[0].value else ''
    if cell_a.startswith('517 '):
        for yr in range(2013, 2025):
            if yr < 2024:
                idx = (yr - YEAR_START) * 4 + 3   # Q4 = anual
            else:
                idx = (yr - YEAR_START) * 4 + 1   # Q2 = enero-junio 2024
            v = row[idx + 1].value  # +1 porque row[0] es el label
            if v is not None and str(v) != 'C':
                telecom_ied[yr] = float(v)
            else:
                telecom_ied[yr] = 0.0
        break
wb2.close()

# 2. Preparar arrays
years = list(range(2013, 2025))
ied_mexico = np.array([total_ied[y] for y in years])
ied_telecom = np.array([telecom_ied[y] for y in years])

# Imprimir tabla de verificación
print(f"{'Año':<6} {'IED México':>14} {'IED Telecom':>14}")
print("-" * 36)
for i, yr in enumerate(years):
    print(f"{yr:<6} {ied_mexico[i]:>14,.2f} {ied_telecom[i]:>14,.2f}")

# 3. Gráfica
fig, ax = plt.subplots(figsize=(14, 8.5))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

n = len(years)
y_pos = np.arange(n)
bar_height = 0.38

# Colores estilo IFT
COLOR_MEXICO = '#A8C8E8'     # Azul claro
COLOR_TELECOM = '#2B1055'    # Púrpura oscuro

# Barras: IED México (barra larga, azul claro)
bars_mx = ax.barh(y_pos + bar_height / 2, ied_mexico, height=bar_height,
                  color=COLOR_MEXICO, edgecolor='none', zorder=2,
                  label='Inversión Extranjera Directa de México')

# Barras: IED Telecom (barra corta, púrpura oscuro)
bars_tc = ax.barh(y_pos - bar_height / 2, ied_telecom, height=bar_height,
                  color=COLOR_TELECOM, edgecolor='none', zorder=2,
                  label='Inversión Extranjera Directa en Telecomunicaciones')

# 4. Anotaciones de valor
for i, yr in enumerate(years):
    # Valor IED México
    mx_val = ied_mexico[i]
    ax.text(mx_val + 300, y_pos[i] + bar_height / 2,
            f'{mx_val:,.0f}'.replace(',', ','),
            va='center', ha='left', fontsize=8, color='#555555',
            fontweight='bold')

    # Valor IED Telecom
    tc_val = ied_telecom[i]
    if tc_val >= 0:
        ax.text(tc_val + 300, y_pos[i] - bar_height / 2,
                f'{tc_val:,.2f}'.replace(',', ','),
                va='center', ha='left', fontsize=8, color='#555555',
                fontweight='bold')
    else:
        ax.text(tc_val - 300, y_pos[i] - bar_height / 2,
                f'{tc_val:,.2f}'.replace(',', ','),
                va='center', ha='right', fontsize=8, color='#555555',
                fontweight='bold')

# 5. Ejes
ax.set_yticks(y_pos)
ax.set_yticklabels(years, fontsize=10, fontweight='bold', color='#333333')
ax.invert_yaxis()  # 2024 arriba, 2013 abajo

ax.set_xlabel('Millones de dólares', fontsize=11, fontweight='bold',
              color='#333333', labelpad=10)
ax.set_ylabel('AÑO', fontsize=11, fontweight='bold',
              color='#333333', labelpad=10)

# Rango del eje X
x_min = min(ied_telecom.min(), 0) - 2000
x_max = ied_mexico.max() + 5000
ax.set_xlim(x_min, x_max)
ax.xaxis.set_major_locator(mticker.MultipleLocator(10000))
ax.xaxis.set_major_formatter(mticker.FuncFormatter(
    lambda v, _: f'{int(v):,}'.replace(',', ',')))
ax.tick_params(axis='x', labelsize=9, colors='#555555')

# Grid vertical suave
ax.grid(axis='x', alpha=0.25, color='#999999', zorder=0)
ax.axvline(x=0, color='#999999', linewidth=0.8, zorder=1)

# Bordes
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#CCCCCC')
ax.spines['left'].set_color('#CCCCCC')

# 6. Título
fig.text(0.02, 0.96, '■ ', fontsize=12, color='#7B2D8E', fontweight='bold',
         transform=fig.transFigure, va='top')
fig.text(0.04, 0.965, 'Figura A.5. ', fontsize=12, color='#333333',
         fontweight='bold', transform=fig.transFigure, va='top')
fig.text(0.115, 0.965,
         'Inversión Extranjera Directa (IED) en telecomunicaciones',
         fontsize=12, color='#333333', transform=fig.transFigure, va='top')

# 7. Leyenda
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.14), ncol=2,
          fontsize=10, frameon=False, handlelength=2.5)

# 8. Notas al pie
note_fuente = (
    'Fuente: IFT con datos de la Secretaría de Economía (datos actualizados '
    'al 3er trimestre de 2025). Datos disponibles en:\n'
    'https://www.gob.mx/se/acciones-y-programas/'
    'competitividad-y-normatividad-inversion-extranjera-directa?state=published.')
note_notas = (
    'Notas: Cifras en millones de dólares de Estados Unidos de América '
    '(dólares corrientes de cada año). La información mostrada se refiere a '
    'la Rama 5151 Transmisión de programas de radio y televisión,\n'
    'Subsector 517 Telecomunicaciones del Sistema de Clasificación Industrial '
    'de América del Norte (SCIAN). Los datos de 2024 corresponden a la '
    'inversión acumulada al mes de junio. Para los demás años\n'
    'se presenta la inversión acumulada al mes de diciembre.')

fig.text(0.02, 0.02, note_fuente, fontsize=7.5, color='#555555',
         fontweight='bold', transform=fig.transFigure, va='bottom',
         linespacing=1.4)
fig.text(0.02, -0.03, note_notas, fontsize=7.5, color='#555555',
         transform=fig.transFigure, va='bottom', linespacing=1.4)

# 9. Guardar
fig.subplots_adjust(left=0.07, right=0.92, top=0.92, bottom=0.15)
output_path = os.path.join(os.path.dirname(__file__), "..", "..", 'output', 'Figura_A5.png')
# Guardar salida
fig.savefig(output_path, dpi=200, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print(f"\nGráfica guardada en: {output_path}")
plt.close(fig)
