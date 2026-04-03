"""
Figura C.12 — Líneas del servicio móvil de acceso a Internet
            por cada 100 habitantes (2010-2023)
Fuente: IFT con datos de operadores, CONAPO, INEGI y estimaciones propias.
Archivo: TD_TELEDENSIDAD_H_IMOVIL_ITE_VA.csv
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import matplotlib.ticker as mticker
import numpy as np
import sys

CSV_PATH = PROJECT_ROOT / "datos" / "C.12" / "TD_TELEDENSIDAD_H_IMOVIL_ITE_VA.csv"
OUTPUT   = "output/Figura_C12.png"

# 1. Lectura y filtro
df  = pd.read_csv(CSV_PATH, encoding="latin1")
dic = df[(df["MES"] == 12) & (df["ANIO"] >= 2010) & (df["ANIO"] <= 2023)].copy()
dic = dic.sort_values("ANIO").reset_index(drop=True)

anios  = dic["ANIO"].tolist()
valores = dic["T_H_INTMOVIL_E"].tolist()

# 2. Figura
fig, ax = plt.subplots(figsize=(13, 6.5))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

C_FILL = "#D6EAF8"   # azul muy claro — área rellena
C_LINE = "#2471A3"   # azul medio     — línea y marcadores
C_DOT  = "#154360"   # azul oscuro    — puntos

x = np.arange(len(anios))

# Área rellena
ax.fill_between(x, 0, valores, color=C_FILL, alpha=0.7)

# Línea con marcadores
ax.plot(x, valores, color=C_LINE, linewidth=2.2, zorder=4)
ax.scatter(x, valores, color=C_DOT, s=40, zorder=5)

# Líneas verticales desde el eje X hasta cada punto (estilo del Anuario)
for xi, v in enumerate(valores):
    ax.plot([xi, xi], [0, v], color=C_LINE, linewidth=0.8,
            linestyle="--", alpha=0.5, zorder=3)

# Etiquetas sobre cada punto
for xi, (v, a) in enumerate(zip(valores, anios)):
    ax.annotate(str(v), xy=(xi, v), xytext=(0, 6),
                textcoords="offset points",
                ha="center", va="bottom",
                fontsize=9, fontweight="bold", color=C_DOT)

# Ejes y estilo
ax.set_xlim(-0.5, len(anios) - 0.5)
ax.set_ylim(0, 115)
ax.set_xticks(x)
ax.set_xticklabels([str(a) for a in anios], fontsize=10)
ax.yaxis.set_visible(False)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_linewidth(0.8)

# Título
ax.set_title(
    "Figura C.12. Líneas del servicio móvil de acceso a Internet\n"
    "por cada 100 habitantes (2010-2023)",
    fontsize=11, fontweight="bold", loc="left", pad=12
)

# Nota al pie
fig.text(
    0.05, -0.03,
    "Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones "
    "a diciembre de cada año, del CONAPO, el INEGI y estimaciones propias.",
    fontsize=7.5, color="#555555"
)

plt.tight_layout()
# Guardar salida
plt.savefig(OUTPUT, dpi=180, bbox_inches="tight")
print(f"Figura guardada: {OUTPUT}")
