"""
Figura D.8 — Percepción o grado de confianza que las personas tienen al hacer uso del Internet
Fuente: IFT, con información de la Encuesta de Confianza en el Servicio de Internet (ECSI) 2024
Archivo de entrada: baseconfianzadigital__3_.csv
Variable: conf_int (pregunta 27.5)
Factor de expansión: fac_per

Códigos válidos:
  1 = Nada
  2 = Poco
  3 = Le es indiferente
  4 = Algo
  5 = Mucho
  9 = NS/NR

Fórmula:
  pct_categoria = SUM(fac_per | conf_int == categoria) / SUM(fac_per | conf_int in [1,2,3,4,5,9]) * 100
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
import matplotlib.ticker as mticker
import numpy as np

# 1. DATOS
CSV_PATH = PROJECT_ROOT / "datos" / "D.8" / "baseconfianzadigital.csv"

# Cargar datos
df = pd.read_csv(CSV_PATH, low_memory=False)

CODES   = [1, 2, 3, 4, 5, 9]
LABELS  = ["Nada", "Poco", "Le es indiferente", "Algo", "Mucho", "NS/NR"]

valid    = df[df["conf_int"].isin(CODES)].copy()
weighted = valid.groupby("conf_int")["fac_per"].sum()
total    = weighted.sum()
pct      = (weighted / total * 100).round(1)

# Ordenar según CODES
values = [pct[c] for c in CODES]

print("Valores calculados (deben coincidir con el Anuario):")
for lbl, val in zip(LABELS, values):
    print(f"  {lbl:20s}: {val:.1f}%")

# 2. COLORES (paleta del Anuario IFT)
COLORS = [
    "#C0392B",   # Nada           — rojo
    "#E8856A",   # Poco           — salmón
    "#3B4A7A",   # Le es indiferente — azul oscuro
    "#3B4A7A",   # Algo           — azul oscuro (más claro abajo)
    "#7EC8C8",   # Mucho          — azul claro
    "#5B6FA6",   # NS/NR          — azul medio
]

# Algo usa tono más claro que Nada/indiferente
COLORS[3] = "#5B6FA6"

# 3. GRÁFICA
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("white")

x      = np.arange(len(LABELS))
width  = 0.55

bars = ax.bar(x, values, width=width, color=COLORS, zorder=3)

# Etiquetas sobre cada barra
for bar, val in zip(bars, values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        f"{val}%",
        ha="center", va="bottom",
        fontsize=11, fontweight="bold",
        color="#222222",
    )

# Ejes
ax.set_xticks(x)
ax.set_xticklabels(LABELS, fontsize=11, color="#333333")
ax.set_ylim(0, 46)
ax.yaxis.set_major_locator(mticker.MultipleLocator(5))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
ax.tick_params(axis="y", labelsize=10, colors="#555555")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#CCCCCC")
ax.spines["bottom"].set_color("#CCCCCC")
ax.yaxis.grid(True, color="#EEEEEE", linewidth=0.8, zorder=0)
ax.set_axisbelow(True)

# Leyenda de colores (igual que la figura original)
legend_items = [
    mpatches.Patch(color=COLORS[0], label="Nada"),
    mpatches.Patch(color=COLORS[1], label="Poco"),
    mpatches.Patch(color=COLORS[2], label="Le es indiferente"),
    mpatches.Patch(color=COLORS[3], label="Algo"),
    mpatches.Patch(color=COLORS[4], label="Mucho"),
    mpatches.Patch(color=COLORS[5], label="NS/NR"),
]
ax.legend(
    handles=legend_items,
    ncol=6,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.08),
    frameon=False,
    fontsize=9,
    handlelength=1.2,
    handleheight=0.9,
)

# Título y nota al pie
ax.set_title(
    "Figura D.8. Percepción o grado de confianza que las personas\ntienen al hacer uso del Internet",
    fontsize=13, fontweight="bold", color="#1A1A2E", pad=28, loc="left",
)

fig.text(
    0.01, -0.04,
    "Fuente: IFT, con información de la Encuesta de Confianza en el Servicio de Internet (ECSI) 2024.",
    fontsize=8.5, color="#666666",
)

plt.tight_layout()

# 4. GUARDAR
OUTPUT = PROJECT_ROOT / "output" / "Figura_D8.png"
# Guardar salida
plt.savefig(OUTPUT, dpi=150, bbox_inches="tight", facecolor="white")
print(f"\nGuardada â†’ {OUTPUT}")
plt.close()
