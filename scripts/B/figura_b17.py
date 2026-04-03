import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import numpy as np

# --- Cargar y limpiar ---
df = pd.read_csv(PROJECT_ROOT / "datos" / "b.17" / "TD_MARKET_SHARE_BAF_ITE_VA.csv", encoding='cp1252')
df['MS'] = pd.to_numeric(
    df['MARKET_SHARE'].astype(str).str.replace('%', '').str.strip(),
    errors='coerce'
)

df_dic = df[(df['MES'] == 12) & (df['ANIO'] >= 2013) & (df['ANIO'] <= 2023)].copy()

# --- Mapeo corregido ---
def asignar_grupo(nombre):
    n = str(nombre).upper()
    if 'AMÉRICA MÓVIL' in n or 'AMERICA MOVIL' in n or 'TELMEX' in n or 'CABLEMAS' in n or 'TELNOR' in n:
        return 'América Móvil'
    if 'GRUPO TELEVISA' in n or 'CABLEVISION' in n:
        return 'Grupo Televisa'
    if 'MEGACABLE' in n:
        return 'Megacable-MCM'
    if 'GRUPO SALINAS' in n or 'TOTALPLAY' in n:
        return 'Grupo Salinas'
    if 'AXTEL' in n:
        return 'Axtel'
    if 'MAXCOM' in n:
        return 'Maxcom'
    if 'CABLECOM' in n:
        return 'Cablecom'
    if n == 'IST':
        return 'IST'
    return 'Otros'

df_dic['GRUPO_AGR'] = df_dic['GRUPO'].apply(asignar_grupo)

pivot = df_dic.groupby(['ANIO', 'GRUPO_AGR'])['MS'].sum().unstack(fill_value=0)
pivot.index = pivot.index.astype(int)

print(pivot[['América Móvil', 'Grupo Televisa', 'Megacable-MCM',
             'Grupo Salinas', 'Axtel', 'Maxcom', 'Cablecom', 'IST', 'Otros']])

# --- Colores del Anuario ---
GRUPOS = ['América Móvil', 'Grupo Televisa', 'Megacable-MCM',
          'Grupo Salinas', 'Axtel', 'Maxcom', 'Cablecom', 'IST', 'Otros']
COLORES = ['#E8907A', '#2C3E6B', '#4A7FB5', '#A8D4E6',
           '#4B3F72', '#8E8EA0', '#2E7D6B', '#C0392B', '#5BB8C1']

# --- Graficar ---
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor('white')

years = pivot.index.tolist()
x = np.arange(len(years))
width = 0.6

bottoms = np.zeros(len(years))
bars_dict = {}

for grupo, color in zip(GRUPOS, COLORES):
    if grupo not in pivot.columns:
        vals = np.zeros(len(years))
    else:
        vals = pivot[grupo].values
    bars = ax.bar(x, vals, width, bottom=bottoms, color=color, label=grupo)
    bars_dict[grupo] = (bars, vals, bottoms.copy())
    bottoms += vals

# Etiquetas dentro de barras (solo si 1.5%)
for grupo, color in zip(GRUPOS, COLORES):
    if grupo not in pivot.columns:
        continue
    bars, vals, bots = bars_dict[grupo]
    for i, (v, b) in enumerate(zip(vals, bots)):
        if v >= 1.5:
            ax.text(x[i], b + v / 2, f'{v:.2f}%',
                    ha='center', va='center', fontsize=6.5,
                    color='white', fontweight='bold')

# Ejes
ax.set_xticks(x)
ax.set_xticklabels([str(y) for y in years], fontsize=10)
ax.set_ylim(0, 110)
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

# Leyenda
ax.legend(GRUPOS, loc='upper center', bbox_to_anchor=(0.5, -0.08),
          ncol=5, fontsize=8, frameon=False)

# Título y fuente
ax.set_title(
    'Figura B.17. Participación de mercado del servicio fijo de Internet (2013-2023)',
    fontsize=11, fontweight='bold', loc='left', pad=12, color='#2C3E50'
)
fig.text(0.08, 0.01,
         'Fuente: Participación de mercado calculada con respecto al número de accesos '
         'del servicio fijo de Internet.\n'
         'Nota: IFT con datos proporcionados por los operadores de telecomunicaciones '
         'a diciembre de cada año.',
         fontsize=7.5, color='gray')

plt.tight_layout(rect=[0, 0.06, 1, 1])
# Guardar salida
plt.savefig('output/Figura_B17.png', dpi=150, bbox_inches='tight')
plt.show()
print("Guardada: output/Figura_B17.png")
