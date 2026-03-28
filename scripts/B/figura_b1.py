"""
Figura B.1 â€” DistribuciÃ³n de los Servicios Fijos con respecto del total de hogares a nivel nacional
Fuente: IFT con datos de la ENDUTIH 2023, del INEGI.
Datos: https://www.inegi.org.mx/programas/endutih/2023/#microdatos

Archivos requeridos:
  - tic_2023_hogares.DBF  (microdatos, 9.4 MB)
  - FD_ENDUTIH2023.xlsx   (descriptor de archivos, referencia de variables)

Variables usadas:
  P4_4    : Â¿Disponen de conexiÃ³n a internet en el hogar?    (1=SÃ­, 2=No)
  P4_5    : Â¿La conexiÃ³n es fija, mÃ³vil o ambas?             (1=Solo fija, 2=Solo mÃ³vil, 3=Ambas, 9=No sabe)
  P5_1    : Â¿Disponen de servicio de televisiÃ³n de paga?     (1=SÃ­, 2=No)
  P5_5    : Â¿Disponen de lÃ­nea telefÃ³nica fija?              (1=SÃ­, 2=No)
  FAC_HOG : Factor de expansiÃ³n del hogar

Nota metodolÃ³gica:
  Los microdatos pÃºblicos producen diferencias de 1-4 pp respecto al Anuario IFT 2024
  (ej. Tres servicios: 19.4% calculado vs 21% publicado). Se usan los valores del
  Anuario para la grÃ¡fica final. La discrepancia se atribuye a revisiones de FAC_HOG
  posteriores a la publicaciÃ³n.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import pandas as pd
from dbfread import DBF
import os

# Ruta al archivo DBF
DBF_PATH = PROJECT_ROOT / "datos" / "B.1-B.2-B.3-D.2-D.3-D.4" / "microdatos" / "endutih2023_bd_dbf" / "tic_2023_hogares.DBF"
OUTPUT_PATH = PROJECT_ROOT / "output" / "Figura_B1.png"

# Carga de microdatos
print("Cargando microdatos...")
# Cargar datos
table = DBF(DBF_PATH, load=True)
df = pd.DataFrame(iter(table))

# Definición de servicios fijos
df['internet_fijo'] = (df['P4_4'] == '1') & (df['P4_5'].isin(['1', '3']))
df['tv_paga']       = (df['P5_1'] == '1')
df['tel_fija']      = (df['P5_5'] == '1')
df['num_servicios'] = (
    df['internet_fijo'].astype(int) +
    df['tv_paga'].astype(int) +
    df['tel_fija'].astype(int)
)

# Diagnóstico
w = df['FAC_HOG']
total = w.sum()
print(f"Total hogares calculado: {total:>12,.0f}")
print(f"(Anuario IFT reporta:    38,627,319)\n")
for label, mask in [
    ('Tres servicios', df['num_servicios'] == 3),
    ('Dos servicios',  df['num_servicios'] == 2),
    ('Un servicio',    df['num_servicios'] == 1),
    ('Ninguno',        df['num_servicios'] == 0),
]:
    v = w[mask].sum()
    print(f"  {label}: {v:>12,.0f}  ({v/total*100:.1f}%)")

# Valores publicados en el Anuario IFT 2024
TOTAL_HOG = 38_627_319

# Pastel principal
pct_tres    = 21
pct_dos     = 34
pct_uno     = 25
pct_ninguno = 20

# Desglose Un servicio
un_srv = {'Solo\nInternet': 18, 'Solo\nTV Rest.': 6, 'Solo\nTelefonÃ­a': 1}

# Desglose Dos servicios
dos_srv = {'Internet +\nTelefonÃ­a': 20, 'TV +\nInternet': 13, 'TV +\nTelefonÃ­a': 1}

# Paleta
C_TRES    = '#1a3a5c'
C_DOS     = '#e05a4e'
C_UNO     = '#a8d4e0'
C_NINGUNO = '#c8d8e0'

# Figura
fig = plt.figure(figsize=(16, 9), facecolor='white')

# Títulos
fig.text(0.04, 0.96, 'B. SERVICIOS FIJOS DE TELECOMUNICACIONES',
         fontsize=13, fontweight='bold', color='#1a3a5c', va='top')
fig.text(0.04, 0.91,
         'Figura B.1.  DistribuciÃ³n de los Servicios Fijos con respecto del total de hogares a nivel nacional',
         fontsize=9.5, color='#1a3a5c', va='top', style='italic')

# Pastel principal
ax_pie = fig.add_axes([0.01, 0.10, 0.46, 0.76])

sizes  = [pct_tres, pct_dos, pct_uno, pct_ninguno]
colors = [C_TRES, C_DOS, C_UNO, C_NINGUNO]
explode = (0.04, 0.04, 0.04, 0.04)

wedges, _ = ax_pie.pie(
    sizes, colors=colors, explode=explode,
    startangle=90, counterclock=False,
    wedgeprops=dict(linewidth=2, edgecolor='white'),
)

# Etiquetas dentro del pastel
etiquetas = [
    ('Tres\nservicios',  f'{pct_tres}%',    ( 0.38,  0.58), ( 0.20,  0.30)),
    ('Dos\nservicios',   f'{pct_dos}%',     ( 0.18, -0.52), ( 0.08, -0.26)),
    ('Un\nservicio',     f'{pct_uno}%',     (-0.60,  0.22), (-0.30,  0.11)),
    ('Ninguno',          f'{pct_ninguno}%', (-0.28, -0.68), (-0.14, -0.36)),
]
for lbl, pct, (lx, ly), (px, py) in etiquetas:
    ax_pie.text(lx, ly, lbl, ha='center', va='center',
                fontsize=8.5, color='white', fontweight='bold')
    ax_pie.text(px, py, pct, ha='center', va='center',
                fontsize=15, color='white', fontweight='bold')

# Total en el centro
ax_pie.text(0,  0.07, 'Total de hogares en MÃ©xico:', ha='center',
            fontsize=7.5, color='#1a3a5c')
ax_pie.text(0, -0.07, f'{TOTAL_HOG:,}', ha='center',
            fontsize=11, color='#1a3a5c', fontweight='bold')

# Anotación Tres servicios
ax_pie.annotate(
    '(TelefonÃ­a Fija +\nTV Restringida\n+ Internet)',
    xy=(0.60, 0.80), xycoords='axes fraction',
    fontsize=7.5, color='#1a3a5c', ha='center',
    bbox=dict(boxstyle='round,pad=0.35', fc='white', ec='#1a3a5c', lw=0.8),
)
ax_pie.set_aspect('equal')

# Panel Un servicio
ax_uno = fig.add_axes([0.52, 0.52, 0.44, 0.34])
ax_uno.set_facecolor('#f2f8fb')
for sp in ax_uno.spines.values():
    sp.set_edgecolor('#1a3a5c'); sp.set_linewidth(0.8)

ax_uno.set_title('Un servicio', fontsize=10, color='#1a3a5c',
                 fontweight='bold', pad=5)

cats_u = list(un_srv.keys())
vals_u = list(un_srv.values())
cols_u = ['#a8d4e0', '#c8e8f4', '#ddf0f8']

b1 = ax_uno.bar(cats_u, vals_u, color=cols_u, width=0.45,
                edgecolor='white', linewidth=1.2)
for bar, v in zip(b1, vals_u):
    ax_uno.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.5, f'{v}%',
                ha='center', va='bottom',
                fontsize=13, fontweight='bold', color='#1a3a5c')

ax_uno.set_ylim(0, 27)
ax_uno.tick_params(left=False, bottom=False, labelleft=False)
for sp in ax_uno.spines.values():
    sp.set_visible(False)
ax_uno.set_xticks(range(len(cats_u)))
ax_uno.set_xticklabels(cats_u, fontsize=8.5, color='#1a3a5c')

# Panel Dos servicios
ax_dos = fig.add_axes([0.52, 0.11, 0.44, 0.34])
ax_dos.set_facecolor('#fff5f4')
for sp in ax_dos.spines.values():
    sp.set_edgecolor('#e05a4e'); sp.set_linewidth(0.8)

ax_dos.set_title('Dos servicios', fontsize=10, color='#e05a4e',
                 fontweight='bold', pad=5)

cats_d = list(dos_srv.keys())
vals_d = list(dos_srv.values())
cols_d = ['#e05a4e', '#c04040', '#f08878']

b2 = ax_dos.bar(cats_d, vals_d, color=cols_d, width=0.45,
                edgecolor='white', linewidth=1.2)
for bar, v in zip(b2, vals_d):
    ax_dos.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.5, f'{v}%',
                ha='center', va='bottom',
                fontsize=13, fontweight='bold', color='#e05a4e')

ax_dos.set_ylim(0, 27)
ax_dos.tick_params(left=False, bottom=False, labelleft=False)
for sp in ax_dos.spines.values():
    sp.set_visible(False)
ax_dos.set_xticks(range(len(cats_d)))
ax_dos.set_xticklabels(cats_d, fontsize=8.5, color='#1a3a5c')

# Nota al pie
fig.text(
    0.04, 0.065,
    'Fuente: IFT con datos de la ENDUTIH 2023, del INEGI. '
    'Datos disponibles en https://www.inegi.org.mx/programas/endutih/2023/\n'
    'Nota: Los porcentajes pueden no sumar 100% debido al redondeo.',
    fontsize=7, color='#666666', va='top'
)

# Logo IFT
fig.text(0.965, 0.975, 'ift', fontsize=17, color='#1a3a5c',
         fontweight='bold', ha='right', va='top')
fig.text(0.965, 0.940,
         'INSTITUTO FEDERAL DE\nTELECOMUNICACIONES',
         fontsize=5.5, color='#1a3a5c', ha='right', va='top')

# Número de página
fig.text(0.04, 0.035, '21', fontsize=11, color='white',
         ha='center', va='center',
         bbox=dict(boxstyle='circle,pad=0.3', fc='#1a3a5c'))

# Guardar
os.makedirs(os.path.dirname(os.path.abspath(OUTPUT_PATH)), exist_ok=True)
# Guardar salida
plt.savefig(OUTPUT_PATH, dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print(f"\nFigura guardada en: {OUTPUT_PATH}")
plt.close()
