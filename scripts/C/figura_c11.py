"""
Figura C.11 — Líneas del servicio móvil de acceso a Internet (2010-2023)
Fuente: IFT con datos de los operadores de telecomunicaciones a diciembre de cada año.
Archivo: TD_LINEAS_HIST_INTMOVIL_ITE_VA.csv
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
import sys

# Ruta al CSV
CSV_PATH = PROJECT_ROOT / "datos" / "C.11" / "TD_LINEAS_HIST_INTMOVIL_ITE_VA.csv"
OUTPUT   = "output/Figura_C11.png"

# 1. Lectura y limpieza
df = pd.read_csv(CSV_PATH, encoding="latin1")

cols_num = ["L_PREPAGO_E", "L_POSPAGO_E", "L_POSPAGOC_E",
            "L_POSPAGOL_E", "L_NO_ESPECIFICADO_E", "L_TOTAL_E"]
for col in cols_num:
    df[col] = (pd.to_numeric(df[col].astype(str)
               .str.replace(",", "").str.strip(), errors="coerce")
               .fillna(0))

# 2. Filtrar diciembre 2010-2023 y agregar por año
dic = df[(df["MES"] == 12) & (df["ANIO"] >= 2010) & (df["ANIO"] <= 2023)]
g   = dic.groupby("ANIO")[cols_num].sum() / 1_000_000   # millones de líneas

# 3. Construir segmentos apilados
# Antes de 2017 solo existe L_POSPAGO_E; desde 2017 se desagrega en C y L
# El stacking del Anuario es (de abajo a arriba):
# Sin segmento Prepago Pospago (pre-2017) Pospago controlado Pospago libre

anios    = g.index.tolist()
sin_seg  = g["L_NO_ESPECIFICADO_E"].values
prepago  = g["L_PREPAGO_E"].values
pospago  = g["L_POSPAGO_E"].values        # solo hasta 2016
pospagoc = g["L_POSPAGOC_E"].values       # desde 2017
pospagol = g["L_POSPAGOL_E"].values       # desde 2017
total    = g["L_TOTAL_E"].values

# 4. Figura
fig, ax = plt.subplots(figsize=(13, 7))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# Colores (aproximados al Anuario)
C_SIN_SEG  = "#F4A261"   # salmón / naranja claro  — sin segmento
C_PREPAGO  = "#90E0EF"   # azul cielo             — prepago
C_POSPAGO  = "#CAF0F8"   # azul muy claro          — pospago (pre-2017)
C_POSP_C   = "#023E8A"   # azul marino oscuro      — pospago controlado
C_POSP_L   = "#0077B6"   # azul medio              — pospago libre
C_TOTAL    = "#E63946"   # rojo/rosa               — línea total

x = np.arange(len(anios))

# Área apilada rellena (fill_between por segmento)
bottom_sin  = np.zeros(len(anios))
bottom_pre  = sin_seg
bottom_pos  = bottom_pre  + prepago
bottom_posC = bottom_pos  + pospago
bottom_posL = bottom_posC + pospagoc

ax.fill_between(x, bottom_sin, bottom_sin + sin_seg,
                color=C_SIN_SEG, alpha=0.85, label="Líneas sin segmento especificado")
ax.fill_between(x, bottom_pre, bottom_pre + prepago,
                color=C_PREPAGO, alpha=0.85, label="Líneas Prepago")
ax.fill_between(x, bottom_pos, bottom_pos + pospago,
                color=C_POSPAGO, alpha=0.85, label="Líneas Pospago")
ax.fill_between(x, bottom_posC, bottom_posC + pospagoc,
                color=C_POSP_C, alpha=0.85, label="Líneas Pospago controlado")
ax.fill_between(x, bottom_posL, bottom_posL + pospagol,
                color=C_POSP_L, alpha=0.85, label="Líneas Pospago libre")

# Línea total
ax.plot(x, total, color=C_TOTAL, linewidth=2.2, marker="o",
        markersize=4, zorder=5, label="Líneas totales")

# Etiquetas sobre la línea total (redondeadas a entero, como en el Anuario)
for xi, (t, a) in enumerate(zip(total, anios)):
    label = str(int(round(t)))
    offset = 3.5
    ax.annotate(label, xy=(xi, t), xytext=(0, offset),
                textcoords="offset points",
                ha="center", va="bottom", fontsize=8.5,
                color=C_TOTAL, fontweight="bold")

# Ejes y estilo
ax.set_xlim(-0.5, len(anios) - 0.5)
ax.set_ylim(0, 145)
ax.set_xticks(x)
ax.set_xticklabels([str(a) for a in anios], rotation=90, fontsize=9)
ax.set_ylabel("Millones de líneas", fontsize=10)
ax.yaxis.set_tick_params(labelsize=9)

# Quitar bordes superior y derecho
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.5)

# Título
ax.set_title(
    "Figura C.11. Líneas del servicio móvil de acceso a Internet (2010-2023)",
    fontsize=11, fontweight="bold", loc="left", pad=12
)

# Leyenda horizontal abajo
handles = [
    mpatches.Patch(color=C_SIN_SEG, label="Líneas sin segmento especificado"),
    mpatches.Patch(color=C_PREPAGO,  label="Líneas Prepago"),
    mpatches.Patch(color=C_POSPAGO,  label="Líneas Pospago"),
    mpatches.Patch(color=C_POSP_C,   label="Líneas Pospago controlado"),
    mpatches.Patch(color=C_POSP_L,   label="Líneas Pospago libre"),
    plt.Line2D([0],[0], color=C_TOTAL, linewidth=2, marker="o",
               markersize=5, label="Líneas totales"),
]
ax.legend(handles=handles, loc="upper left", fontsize=8,
          frameon=False, ncol=3, bbox_to_anchor=(0, -0.18))

# Nota al pie
fig.text(0.05, -0.06,
    "Fuente: IFT con datos de los operadores de telecomunicaciones a diciembre de cada año.\n"
    "Nota: A partir de 2017, se comenzó a solicitar la desagregación por pospago libre y pospago controlado.",
    fontsize=7.5, color="#555555")

plt.tight_layout()
# Guardar salida
plt.savefig(OUTPUT, dpi=180, bbox_inches="tight")
print(f"Figura guardada: {OUTPUT}")
