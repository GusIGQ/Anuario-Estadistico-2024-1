"""
Figura D.2 — Uso de Smartphone e Internet por grupos de edad (2023)
Fuente: INEGI, ENDUTIH 2023

Archivo de entrada:
  tr_endutih_usuarios_anual_2023.csv

Flujo del cuestionario (sección P6 — Internet):
  P6_1 = '1' â†’ usa computadora â†’ salta a P6_4 (dispositivo principal de internet)
  P6_1 = '2' â†’ no usa comp   â†’ P6_3: ¿usa internet? (1=sí, 2=no)
  Por tanto:
    usa_internet = (P6_3 == '1')  OR  (P6_4 no es NaN)
  Equivalente: NO tiene P6_3 == '2'

Flujo del cuestionario (sección P7 — Celular):
  P7_1 = '1' â†’ tiene celular â†’ P7_3: ¿es smartphone? (1=sí, 2=no)
  P7_1 = '2' â†’ no tiene celular â†’ P7_3 queda NaN
  Por tanto:
    usa_smartphone = (P7_3 == '1')

Variables:
  EDAD    — edad de la persona
  P6_3    — ¿usa internet? solo para quienes no usan comp (1=sí, 2=no, NaN=saltó)
  P6_4    — dispositivo principal de internet (NaN=no usa internet)
  P7_3    — tipo de celular (1=smartphone, 2=básico, NaN=sin celular)
  FAC_PER — factor de expansión (~119.5 millones total)
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import matplotlib.patches as mpatches
import os

# Rutas
CSV_PATH = PROJECT_ROOT / "datos" / "D.2" / "tr_endutih_usuarios_anual_2023.csv"
OUTPUT   = PROJECT_ROOT / "output" / "Figura_D2.png"

# 1. Lectura
print("Leyendo CSV...")
# Cargar datos
df = pd.read_csv(
    CSV_PATH,
    usecols=['EDAD', 'P6_3', 'P6_4', 'P7_3', 'FAC_PER'],
    dtype=str
)
df['EDAD']    = pd.to_numeric(df['EDAD'],    errors='coerce')
df['FAC_PER'] = pd.to_numeric(df['FAC_PER'], errors='coerce')
print(f"  Registros leídos : {len(df):,}")
print(f"  Suma FAC_PER     : {df['FAC_PER'].sum():,.0f}")

# 2. Filtro: personas de 6 años o más
df = df[df['EDAD'] >= 6].copy()

# 3. Indicadores binarios
# Internet: usa comp (P6_4 no NaN) O usa internet sin comp (P6_3 1 )
# Equivalente: quien NO tiene P6_3 2 (no usa internet)
df['internet']   = (df['P6_3'].str.strip() != '2').astype(int)
# Pero P6_3 NaN para usuarios de comp no significa no usa ya está cubierto
# La condición (P6_3 2 ) es correcta:
# P6_3 2 no usa internet 0
# P6_3 1 usa internet sin comp 1
# P6_3 NaN usa comp (implica usa internet) 1

# Smartphone: P7_3 1
df['smartphone'] = (df['P7_3'].str.strip() == '1').astype(int)

# 4. Grupos de edad
bins   = [5, 11, 17, 24, 34, 44, 54, 200]
labels = ['6 a 11\naños', '12 a 17\naños', '18 a 24\naños',
          '25 a 34\naños', '35 a 44\naños', '45 a 54\naños', '55 o\nmás']
df['grupo'] = pd.cut(df['EDAD'], bins=bins, labels=labels)

# 5. Cálculo ponderado por FAC_PER
def calcular_pct(g):
    total_fac = g['FAC_PER'].sum()
    return pd.Series({
        'pct_internet':   g['internet'].mul(g['FAC_PER']).sum()   / total_fac * 100,
        'pct_smartphone': g['smartphone'].mul(g['FAC_PER']).sum() / total_fac * 100,
    })

resultado = (
    df.groupby('grupo', observed=True)
    .apply(calcular_pct)
    .reset_index()
)

print("\nValores calculados:")
print(resultado.round(1).to_string(index=False))

grupos  = resultado['grupo'].tolist()
pct_smt = resultado['pct_smartphone'].tolist()
pct_int = resultado['pct_internet'].tolist()

# 6. Figura
COLOR_SMT = '#3B4F8C'
COLOR_INT = '#E05C6A'

n   = len(grupos)
x   = range(n)
w   = 0.38
gap = 0.04

# Crear grafica
fig, ax = plt.subplots(figsize=(13, 7))
fig.patch.set_facecolor('#F7F7F7')
ax.set_facecolor('#F7F7F7')

pos_smt = [i - w/2 - gap/2 for i in x]
pos_int = [i + w/2 + gap/2 for i in x]

bars_smt = ax.bar(pos_smt, pct_smt, width=w, color=COLOR_SMT)
bars_int = ax.bar(pos_int, pct_int, width=w, color=COLOR_INT)

for bar, val in zip(bars_smt, pct_smt):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
            f'{val:.1f}%', ha='center', va='bottom',
            fontsize=9, fontweight='bold', color=COLOR_SMT)

for bar, val in zip(bars_int, pct_int):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
            f'{val:.1f}%', ha='center', va='bottom',
            fontsize=9, fontweight='bold', color=COLOR_INT)

ax.set_xticks(list(x))
ax.set_xticklabels(grupos, fontsize=10)
ax.set_ylim(0, 110)
ax.set_yticks([])
ax.spines[['top', 'right', 'left']].set_visible(False)
ax.spines['bottom'].set_color('#CCCCCC')
ax.tick_params(axis='x', length=0)

patch_smt = mpatches.Patch(color=COLOR_SMT, label='% de usuarios de Smartphone')
patch_int = mpatches.Patch(color=COLOR_INT, label='% de usuarios de Internet')
ax.legend(handles=[patch_smt, patch_int],
          loc='upper center', bbox_to_anchor=(0.5, -0.10),
          ncol=2, fontsize=10, frameon=False)

ax.set_title('Figura D.2. Uso de Smartphone e internet por grupos de edad',
             fontsize=11, fontweight='bold', pad=14, loc='left')
fig.text(0.0, -0.04,
         'Fuente: IFT con datos de la ENDUTIH 2023, del INEGI.',
         fontsize=8, color='#555555', transform=ax.transAxes)

plt.tight_layout()
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
# Guardar salida
plt.savefig(OUTPUT, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
print(f"\nGuardado: {OUTPUT}")
