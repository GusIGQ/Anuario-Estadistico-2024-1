"""
Figura D.1 â€” Disponibilidad de las TIC en los hogares (2010-2023)
Fuente:
  - 2001-2014: INEGI MODUTIH  â†’ 27_2023_hnal110.xlsx  (Computadora, Radio, TelefonÃ­a)
                               â†’ 30_2023_hnal130.xlsx  (TV digital / analÃ³gico)
  - 2015-2023: INEGI ENDUTIH  â†’ mismos archivos
"""

import openpyxl
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import matplotlib.ticker as mticker
import numpy as np
import os

# Rutas de entrada
BASE = PROJECT_ROOT / "datos" / "D.1"
FILE27 = os.path.join(BASE, "27_2023_hnal110.xlsx")
FILE30 = os.path.join(BASE, "30_2023_hnal130.xlsx")

# Lectura archivo 27: Computadora, Radio, Telefonía
def leer_archivo27(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.active
    data = {}
    for row in ws.iter_rows(min_row=6, values_only=True):
        raw = str(row[0]).strip()
        anio_str = ''.join(c for c in raw if c.isdigit())
        if len(anio_str) == 4:
            anio = int(anio_str)
            data[anio] = {
                'computadora': row[2],   # % Computadora
                'radio':       row[12],  # % Radio
                'telefonia':   row[10],  # % TelefonÃ­a (cel + fija combinada)
            }
    return data

# Lectura archivo 30: TV digital y analógico
def leer_archivo30(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.active
    data = {}
    for row in ws.iter_rows(min_row=6, values_only=True):
        raw = str(row[0]).strip()
        anio_str = ''.join(c for c in raw if c.isdigit())
        if len(anio_str) == 4:
            anio = int(anio_str)
            solo_dig = row[4] or 0   # Solo digital %
            solo_ana = row[6] or 0   # Solo analÃ³gico %
            ambos    = row[8] or 0   # Ambos tipos %
            data[anio] = {
                'tv_digital':   solo_dig + ambos,   # hogares con al menos 1 digital
                'tv_analogico': solo_ana + ambos,   # hogares con al menos 1 analÃ³gico
            }
    return data

data27 = leer_archivo27(FILE27)
data30 = leer_archivo30(FILE30)

# Construir series 2010-2023
years = list(range(2010, 2024))

comp  = [round(data27[y]['computadora'] or 0) for y in years]
radio = [round(data27[y]['radio']       or 0) for y in years]
cel   = [round(data27[y]['telefonia']   or 0) for y in years]
tvdig = [round(data30[y]['tv_digital']  or 0) for y in years]
tvana = [round(data30[y]['tv_analogico']or 0) for y in years]

# Colores exactos del Anuario
COLOR_COMP  = '#E05C3A'   # naranja-rojo
COLOR_RADIO = '#F5A623'   # naranja
COLOR_TVANA = '#3B5B8C'   # azul marino oscuro
COLOR_TVDIG = '#3EAFC4'   # azul celeste
COLOR_CEL   = '#A8D8EA'   # azul claro

# Figura
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor('#F7F7F7')
ax.set_facecolor('#F7F7F7')

lw = 2.2
ms = 5

l1, = ax.plot(years, cel,   color=COLOR_CEL,   lw=lw, marker='o', ms=ms, label='TelÃ©fono celular')
l2, = ax.plot(years, tvdig, color=COLOR_TVDIG,  lw=lw, marker='o', ms=ms, label='Televisor digital')
l3, = ax.plot(years, comp,  color=COLOR_COMP,   lw=lw, marker='o', ms=ms, label='Equipo de cÃ³mputo')
l4, = ax.plot(years, radio, color=COLOR_RADIO,  lw=lw, marker='o', ms=ms, label='Aparatos de radio')
l5, = ax.plot(years, tvana, color=COLOR_TVANA,  lw=lw, marker='o', ms=ms, label='Televisor analÃ³gico')

# Etiquetas en cada punto
def etiquetar(series, color, offsets=None):
    """Agrega etiqueta % en cada punto con offset opcional."""
    for i, (x, y) in enumerate(zip(years, series)):
        dy = offsets[i] if offsets else 2
        ax.annotate(f'{y}%', xy=(x, y), xytext=(0, dy),
                    textcoords='offset points', ha='center', va='bottom',
                    fontsize=6.5, color=color, fontweight='bold')

etiquetar(cel,   COLOR_CEL,   offsets=[ 5]*14)
etiquetar(tvdig, COLOR_TVDIG, offsets=[ 5]*14)
etiquetar(comp,  COLOR_COMP,  offsets=[-12]*14)
etiquetar(radio, COLOR_RADIO, offsets=[ 5]*14)
etiquetar(tvana, COLOR_TVANA, offsets=[-12]*14)

# Ejes
ax.set_xlim(2009.5, 2023.5)
ax.set_ylim(0, 105)
ax.set_xticks(years)
ax.set_xticklabels([str(y) for y in years], fontsize=9)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{int(v)}%'))
ax.set_yticks(range(0, 110, 10))
ax.tick_params(axis='both', labelsize=9)
ax.spines[['top','right']].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.4)

# Leyenda
ax.legend(handles=[l3, l4, l5, l2, l1],
          loc='upper center', bbox_to_anchor=(0.5, -0.10),
          ncol=5, fontsize=9, frameon=False,
          handlelength=2)

# Título y fuente
ax.set_title('Figura D.1. Disponibilidad de las TIC en los hogares (2010-2023)',
             fontsize=11, fontweight='bold', pad=12, loc='left')

fig.text(0.01, -0.04,
         'Fuente: IFT con datos del MODUTIH para el periodo 2010-2014 y la ENDUTIH para el periodo 2015-2023, del INEGI.',
         fontsize=8, color='#555555', transform=ax.transAxes)

plt.tight_layout()
out = 'output/Figura_D1.png'
os.makedirs(os.path.dirname(out), exist_ok=True)
# Guardar salida
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
print(f"Guardado: {out}")
