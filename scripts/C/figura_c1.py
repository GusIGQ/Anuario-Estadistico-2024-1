"""
Figura C.1 â€” Espectro radioelÃ©ctrico (MHz) asignado por banda de frecuencia
Fuente: IFT con datos a agosto de 2024.
Archivo de entrada: datos/C.1/TD_DIST_ESPECTRO_VA.csv
Salida: output/Figura_C1.png
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
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

# Rutas
INPUT  = PROJECT_ROOT / "datos" / "C.1" / "TD_DIST_ESPECTRO_VA.csv"
OUTPUT = PROJECT_ROOT / "output" / "Figura_C1.png"
os.makedirs(PROJECT_ROOT / "output", exist_ok=True)

# Leer CSV y filtrar ago-24
df = pd.read_csv(INPUT)
row = df[df["ESTADO"] == "ago-24"].iloc[0]

bandas = {
    "Banda de\n2500 MHz": ("B_2_5_GHZ", "#E07A5F"),   # rojo/salmÃ³n
    "Banda AWS":           ("B_AWS",     "#E07A5F"),   # rojo/salmÃ³n (mÃ¡s claro)
    "Banda de\n700 MHz":  ("B_700_MHZ", "#3D405B"),   # azul marino oscuro
    "Banda de\n3500 MHz": ("B_3_5_GHZ", "#3D405B"),   # azul marino oscuro
    "Banda PCS":           ("B_PCS",     "#2196a0"),   # teal
    "Banda de\n3300 MHz": ("B_3_3_GHZ", "#2196a0"),   # teal
    "Banda de\n850 MHz":  ("B_850_MHZ", "#5b9fc9"),   # azul medio
    "Banda de\n800 MHz":  ("B_800_MHZ", "#5b9fc9"),   # azul medio
}

valores = {}
colores = {}
for k, (col, c) in bandas.items():
    valores[k] = int(row[col]) if not pd.isna(row[col]) else 0
    colores[k] = c

total = int(row["B_700_MHZ"] + row["B_800_MHZ"] + row["B_850_MHZ"] +
            row["B_PCS"] + row["B_AWS"] + row["B_2_5_GHZ"] +
            row["B_3_3_GHZ"] + row["B_3_5_GHZ"])

# Layout manual del treemap (posiciones relativas al PDF)
# Cada cuadro: (x, y, ancho, alto) en unidades normalizadas 0,1
# El tamaño es proporcional a los MHz
# Layout visual del Anuario (2 columnas grandes + 2 columnas derecha)

# 2500 MHz AWS 3500 MHz PCS 3300
# 2500 MHz AWS 700 MHz 850 800

fig, ax = plt.subplots(figsize=(13, 7))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# Definir celdas manualmente (x0, y0, w, h) proporcionales a MHz
# Columna 1: 2500 MHz (140) ocupa toda la altura
# Columna 2: AWS (130) ocupa toda la altura
# Columna 3: 3500 (100) arriba + 700 (90) abajo
# Columna 4: PCS (68) arriba + 850 (47) abajo
# Columna 5: 3300 (50) arriba + 800 (20) abajo

PAD = 0.008

celdas = [
    # (nombre, x0, y0, w, h, color)
    ("Banda de\n2500 MHz\n140",  0.00,  0.00, 0.210, 1.00, "#E8735A"),
    ("Banda AWS\n130",           0.215, 0.00, 0.195, 1.00, "#F0956A"),
    ("Banda de\n3500 MHz\n100",  0.415, 0.53, 0.245, 0.47, "#2F4A6D"),
    ("Banda de\n700 MHz\n90",    0.415, 0.00, 0.245, 0.52, "#3D5A80"),
    ("Banda PCS\n68",            0.665, 0.40, 0.195, 0.60, "#2196A0"),
    ("Banda de\n850 MHz\n47",    0.665, 0.00, 0.195, 0.39, "#4AABB5"),
    ("Banda de\n3300 MHz\n50",   0.865, 0.40, 0.135, 0.60, "#17768A"),
    ("Banda de\n800 MHz\n20",    0.865, 0.00, 0.135, 0.39, "#5BBDD6"),
]

for (label, x0, y0, w, h, color) in celdas:
    # Rectángulo con padding
    rect = FancyBboxPatch(
        (x0 + PAD, y0 + PAD),
        w - 2*PAD, h - 2*PAD,
        boxstyle="round,pad=0.005",
        linewidth=0,
        facecolor=color,
        zorder=2
    )
    ax.add_patch(rect)

    # Texto centrado en la celda
    cx = x0 + w / 2
    cy = y0 + h / 2

    lines = label.strip().split("\n")
    # sltima línea número MHz (negrita grande), resto nombre banda
    nombre = "\n".join(lines[:-1])
    mhz    = lines[-1]

    # Tamaño de fuente proporcional al área de la celda
    area = w * h
    fs_nombre = max(7, min(13, area * 120))
    fs_mhz    = max(10, min(22, area * 200))

    ax.text(cx, cy + h * 0.10, nombre,
            ha="center", va="center", fontsize=fs_nombre,
            color="white", fontweight="normal",
            multialignment="center", zorder=3)
    ax.text(cx, cy - h * 0.14, mhz,
            ha="center", va="center", fontsize=fs_mhz,
            color="white", fontweight="bold", zorder=3)

# Título y fuente
fig.text(0.01, 0.97,
         "Figura C.1. Espectro radioelÃ©ctrico (MHz) asignado por banda de frecuencia",
         fontsize=12, fontweight="bold", va="top")

fig.text(0.01, 0.01,
         f"Fuente: IFT con datos a agosto de 2024.  |  Total asignado: {total} MHz\n"
         "Nota: El tamaÃ±o de los cuadros corresponde a los MHz asignados por banda de frecuencia.\n"
         "La banda AWS corresponde a las bandas de 1.7/2.1 GHz; la banda PCS corresponde a la banda de 1900 MHz.",
         fontsize=7.5, color="#555555", va="bottom")

plt.tight_layout(rect=[0, 0.07, 1, 0.94])
# Guardar salida
plt.savefig(OUTPUT, dpi=150, bbox_inches="tight")
plt.close()
print(f"Guardado: {OUTPUT}")
print(f"Total MHz (ago-24): {total}")
