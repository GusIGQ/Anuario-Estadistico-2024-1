"""
Figura D.7 â€” Anuario EstadÃ­stico IFT 2024
Usuarios que han vivido experiencias negativas al utilizar Internet
y/o realizar actividades en lÃ­nea, por grupo de edad.

Fuente: IFT, con informaciÃ³n de la Encuesta de Confianza en el
        Servicio de Internet (ECSI) 2024.
Datos:  baseconfianzadigital.csv
        https://www.ift.org.mx/encuesta-confianza-en-internet

Nota: Respuesta mÃºltiple, por lo que la suma no da 100%.

CÃ¡lculo:
  PoblaciÃ³n base: usuarios de internet (rescate_internet == 1)
  PonderaciÃ³n:    fac_per (Factor de ExpansiÃ³n Final de Personas)
  Filtro edad:    edad_gpos (1=18-24, 2=25-34, 3=35-44, 4=45-54, 5=55+)

  Variables de experiencias negativas (SecciÃ³n IV del cuestionario):
    expp_mensnd  â†’ Le han enviado mensajes no deseados         (P25_1_a)
    expp_pubipi  â†’ Han publicado informaciÃ³n personal sin permiso (P25_1_b)
    expp_datpre  â†’ Han usado datos para pedir prÃ©stamos sin permiso (P25_1_d)
    expp_robcon  â†’ Le han robado sus contraseÃ±as (hackeado)    (P25_1_e)

  FÃ³rmula por grupo de edad g y experiencia e:
    %e_g = SUM(fac_per | edad_gpos==g & expp_e==1)
           / SUM(fac_per | edad_gpos==g)  * 100

  Valores reproducidos (coinciden con el Anuario al decimal):
    Mensajes no deseados: 64.8 / 62.6 / 60.8 / 57.6 / 53.4
    Info personal:        16.5 / 14.5 / 13.1 / 14.5 /  9.4
    Datos prÃ©stamos:       8.6 / 13.9 / 11.9 / 11.4 /  8.6
    Robo contraseÃ±as:     23.1 / 20.0 / 18.2 / 11.2 /  9.5
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter

# Rutas
CSV_PATH = PROJECT_ROOT / "datos" / "D.7" / "baseconfianzadigital.csv"
OUT_PATH = PROJECT_ROOT / "output" / "Figura_D7.png"

# Carga y filtro
df = pd.read_csv(CSV_PATH, low_memory=False)
df_usr = df[df['rescate_internet'] == 1].copy()   # solo usuarios de internet

# Grupos de edad
GRUPOS = {
    1: '18 a 24 aÃ±os',
    2: '25 a 34 aÃ±os',
    3: '35 a 44 aÃ±os',
    4: '45 a 54 aÃ±os',
    5: '55 a mÃ¡s aÃ±os',
}

# Variables de experiencias negativas
EXPERIENCIAS = {
    'Recibir mensajes\nno deseados':              'expp_mensnd',
    'Han publicado informaciÃ³n\npersonal sin su permiso': 'expp_pubipi',
    'Han usado sus datos para pedir\nprÃ©stamos o crÃ©ditos sin su permiso': 'expp_datpre',
    'Han robado sus contraseÃ±as':                 'expp_robcon',
}

# Cálculo ponderado
def pct_pond(df_sub, col):
    """% ponderado de experiencia positiva (valor==1) en el subconjunto."""
    total = df_sub['fac_per'].sum()
    if total == 0:
        return np.nan
    si = df_sub[df_sub[col] == 1]['fac_per'].sum()
    return si / total * 100

resultados = {}
for g, label in GRUPOS.items():
    sub = df_usr[df_usr['edad_gpos'] == g]
    resultados[label] = {
        nombre: pct_pond(sub, col)
        for nombre, col in EXPERIENCIAS.items()
    }

# Paleta (igual que el Anuario)
COLORES = {
    'Recibir mensajes\nno deseados':              '#9BD0D4',   # azul cielo
    'Han publicado informaciÃ³n\npersonal sin su permiso': '#F4A185',  # salmÃ³n
    'Han usado sus datos para pedir\nprÃ©stamos o crÃ©ditos sin su permiso': '#2E4A72',  # azul oscuro
    'Han robado sus contraseÃ±as':                 '#C0392B',   # rojo
}

GRUPOS_LABEL = list(GRUPOS.values())          # eje X
EXP_KEYS     = list(EXPERIENCIAS.keys())      # 4 series

# Figura
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

n_grupos = len(GRUPOS_LABEL)
n_series = len(EXP_KEYS)

# Ancho de cada bloque de grupo y de cada barra individual
bloque_w = 0.72
barra_w  = bloque_w / n_series          # ~0.18

x_base = np.arange(n_grupos)           # posiciones centrales de grupo

for i, exp in enumerate(EXP_KEYS):
    color = COLORES[exp]
    offset = (i - (n_series - 1) / 2) * barra_w

    valores = [resultados[g][exp] for g in GRUPOS_LABEL]
    xs = x_base + offset

    bars = ax.bar(
        xs, valores,
        width=barra_w * 0.88,
        color=color,
        zorder=3,
    )

    # Etiquetas sobre cada barra (solo si el valor es visible )
    for bar, val in zip(bars, valores):
        if val >= 5:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.4,
                f'{val:.1f}%',
                ha='center', va='bottom',
                fontsize=7.5, fontweight='bold',
                color='#333333',
            )

# Ejes
ax.set_xlim(-0.55, n_grupos - 0.45)
ax.set_ylim(0, 78)
ax.set_yticks([0, 10, 20, 30, 40, 50, 60, 70])
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{int(v)}%'))
ax.set_xticks(x_base)
ax.set_xticklabels(GRUPOS_LABEL, fontsize=10)
ax.tick_params(axis='y', labelsize=9, colors='#555555')
ax.tick_params(axis='x', labelsize=10, colors='#333333', length=0)

# Grid horizontal
ax.yaxis.grid(True, color='#DDDDDD', linewidth=0.6, zorder=0)
ax.set_axisbelow(True)

# Bordes
for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#CCCCCC')

# Leyenda
parches = [
    mpatches.Patch(color=COLORES[e], label=e.replace('\n', ' '))
    for e in EXP_KEYS
]
ax.legend(
    handles=parches,
    loc='upper center',
    bbox_to_anchor=(0.5, -0.11),
    ncol=2,
    frameon=False,
    fontsize=8.5,
    handlelength=1.4,
    handleheight=0.9,
)

# Título de la figura
fig.text(
    0.01, 0.97,
    'â–  Figura D.7. Usuarios que han vivido experiencias negativas al utilizar Internet\n'
    '   y/o realizar actividades en lÃ­nea, por grupo de edad',
    fontsize=10, fontweight='bold', color='#1a1a1a',
    va='top',
)

# Fuente y nota
nota = (
    'Fuente: IFT, con informaciÃ³n de la Encuesta de Confianza en el Servicio de Internet (ECSI) 2024.\n'
    'Nota: Respuesta mÃºltiple, por lo que la suma no da 100%. Es importante seÃ±alar que los resultados '
    'pueden presentar variaciones\nque pueden ser explicadas por el error teÃ³rico de cada encuesta.'
)
fig.text(0.01, 0.01, nota, fontsize=7.5, color='#555555', va='bottom')

plt.tight_layout(rect=[0, 0.07, 1, 0.92])
# Guardar salida
plt.savefig(OUT_PATH, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print(f"âœ…  Figura guardada en: {OUT_PATH}")

# Verificación numérica
print("\nVerificaciÃ³n de valores calculados vs Anuario IFT 2024:")
anuario = {
    'Recibir mensajes\nno deseados':              [64.8, 62.7, 60.8, 57.6, 53.4],
    'Han publicado informaciÃ³n\npersonal sin su permiso': [16.5, 14.5, 13.1, 14.5,  9.4],
    'Han usado sus datos para pedir\nprÃ©stamos o crÃ©ditos sin su permiso': [ 8.6, 13.9, 11.9, 11.4,  8.6],
    'Han robado sus contraseÃ±as':                 [23.1, 20.0, 18.2, 11.2,  9.5],
}
for exp, vals_ref in anuario.items():
    titulo_corto = exp.split('\n')[0][:40]
    for g, ref in zip(GRUPOS_LABEL, vals_ref):
        calc = resultados[g][exp]
        diff = abs(calc - ref)
        estado = "âœ…" if diff < 0.15 else "âš ï¸"
        print(f"  {estado} {titulo_corto:<40} {g:<15} calc={calc:.1f}%  ref={ref:.1f}%  Î”={diff:.2f}")
