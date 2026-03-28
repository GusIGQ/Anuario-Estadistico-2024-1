"""
Figura C.2 â€” DistribuciÃ³n del espectro radioelÃ©ctrico por operador y por banda de frecuencia
Fuente: IFT con datos a agosto de 2024.
Archivo de entrada: datos/C.2/TD_ESPECTRO_BANDA_VA.csv
Salida: output/Figura_C2.png
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
import numpy as np
import os

# Rutas
INPUT  = PROJECT_ROOT / "datos" / "C.2" / "TD_ESPECTRO_BANDA_VA.csv"
OUTPUT = PROJECT_ROOT / "output" / "Figura_C2.png"
os.makedirs("output", exist_ok=True)

# Leer CSV
df = pd.read_csv(INPUT)
df = df.set_index("OPERADOR")

# Mapeo columnas CSV etiquetas del eje X (igual que el Anuario)
BANDAS = {
    "B_700_MHZ": "700 MHZ",
    "B_800_MHZ": "800 MHZ",
    "B_850_MHZ": "850 MHZ",
    "B_PCS":     "1900 MHZ",   # B_PCS corresponde a 1900 MHz en la figura
    "B_AWS":     "B_PCS",      # AWS aparece como "B_PCS" en el eje del Anuario
    "B_2_5_GHZ": "AWS",        # 2.5 GHz aparece como "AWS" en el eje
    "B_3_5_GHZ": "3500 MHZ",
}
# Nota: B_3_3_GHZ y la columna 2500 MHZ del Anuario:
# En el PDF el eje muestra: 700 / 800 / 850 / 1900 / B_PCS / AWS / 2500 / 3500
# Revisando los datos: Telcel tiene 1.0 en B_3_3_GHZ esa es la banda 2500 MHZ
BANDAS_FINAL = {
    "B_700_MHZ": "700 MHZ",
    "B_800_MHZ": "800 MHZ",
    "B_850_MHZ": "850 MHZ",
    "B_PCS":     "1900 MHZ",
    "B_AWS":     "B_PCS",
    "B_2_5_GHZ": "AWS",
    "B_3_3_GHZ": "2500 MHZ",
    "B_3_5_GHZ": "3500 MHZ",
}

OPERADORES = ["TELCEL", "AT&T", "ALTAN"]

# Construir tabla de porcentajes por banda
# Los valores en el CSV ya son fracciones (0.65 65%). NaN 0% en esa banda.
cols = list(BANDAS_FINAL.keys())
etiquetas = list(BANDAS_FINAL.values())

data = df.reindex(OPERADORES)[cols].fillna(0)

# Verificación: suma por columna debe ser 1.0 (o 0 si nadie tiene esa banda)
# print(data.sum()) descomentar para debug

# Colores (igual al Anuario: azul claro Telcel, azul oscuro AT&T, marino Altán)
COLORES = {
    "TELCEL": "#8ECAE6",   # azul claro
    "AT&T":   "#1D3557",   # azul oscuro / marino
    "ALTAN":  "#264653",   # azul muy oscuro / casi negro
}

# Figura
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

x = np.arange(len(etiquetas))
bar_w = 0.55

bottoms = np.zeros(len(etiquetas))
bar_containers = {}

for op in OPERADORES:
    vals = data.loc[op].values.astype(float)
    bars = ax.bar(x, vals, bar_w, bottom=bottoms, color=COLORES[op], label=op)
    bar_containers[op] = (bars, vals, bottoms.copy())
    bottoms += vals

# Etiquetas de porcentaje dentro de cada segmento
for op in OPERADORES:
    bars, vals, bots = bar_containers[op]
    for i, (v, b) in enumerate(zip(vals, bots)):
        if v > 0.02:   # solo etiquetar si el segmento es visible
            pct = int(round(v * 100))
            y_pos = b + v / 2
            color_txt = "white" if op in ("AT&T", "ALTAN") else "#1a1a2e"
            ax.text(x[i], y_pos, f"{pct}%", ha="center", va="center",
                    fontsize=10, fontweight="bold", color=color_txt)

# Ejes y estilo
ax.set_xticks(x)
ax.set_xticklabels(etiquetas, fontsize=11)
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=10)
ax.set_ylim(0, 1.15)
ax.yaxis.grid(True, linestyle="--", alpha=0.4)
ax.set_axisbelow(True)
for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color("#cccccc")

# Leyenda
patches = [mpatches.Patch(color=COLORES[op], label=op.title()) for op in OPERADORES]
ax.legend(handles=patches, loc="upper right", frameon=False,
          fontsize=10, ncol=3,
          bbox_to_anchor=(1.0, 1.12))

# Título y fuente
fig.text(0.01, 0.97,
         "Figura C.2. DistribuciÃ³n del espectro radioelÃ©ctrico por operador y por banda de frecuencia",
         fontsize=12, fontweight="bold", va="top")

fig.text(0.01, 0.02,
         "Fuente: IFT con datos a agosto de 2024.\n"
         "Nota: La banda AWS corresponde a las bandas de 1.7/2.1 GHz; la banda PCS corresponde a la banda de 1900 MHz.",
         fontsize=8, color="#555555", va="bottom")

plt.tight_layout(rect=[0, 0.06, 1, 0.95])
# Guardar salida
plt.savefig(OUTPUT, dpi=150, bbox_inches="tight")
plt.close()
print(f"Guardado: {OUTPUT}")
