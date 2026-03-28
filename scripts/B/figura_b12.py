"""
Figura B.12 â€” Accesos del Servicio Fijo de Internet por cada 100 hogares (2000-2023)
Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones a diciembre de cada aÃ±o,
        del CONAPO y el INEGI.
CSV: TD_PENETRACION_H_BAF_ITE_VA.csv
Columna: P_BAF_E (precalculada por IFT) | Filtro: MES==12
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
import os

# 1. Carga y cálculo
df = pd.read_csv(PROJECT_ROOT / "datos" / "b.12" / "TD_PENETRACION_H_BAF_ITE_VA.csv", encoding="latin1")
df["MES"]  = pd.to_numeric(df["MES"],  errors="coerce")
df["ANIO"] = pd.to_numeric(df["ANIO"], errors="coerce")

data = (
    df[df["MES"] == 12]
    .sort_values("ANIO")
    [["ANIO","P_BAF_E"]]
    .rename(columns={"ANIO":"anio","P_BAF_E":"pen"})
)
data = data[(data["anio"] >= 2000) & (data["anio"] <= 2023)].reset_index(drop=True)

print("Valores calculados:")
print(data.to_string(index=False))

# 2. Figura
COLOR_LINE  = "#2A6EBB"
COLOR_DOT   = "#1A4F8A"
COLOR_LABEL = "#1A3A5C"

# Crear grafica
fig, ax = plt.subplots(figsize=(14, 6))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

aÃ±os    = data["anio"].values
valores = data["pen"].values

ax.plot(aÃ±os, valores, color=COLOR_LINE, linewidth=2.0, zorder=3)
ax.scatter(aÃ±os, valores, color=COLOR_DOT, s=30, zorder=4)

# Etiquetas sobre cada punto
for anio, val in zip(aÃ±os, valores):
    offset = 1.8
    ha = "center"
    ax.annotate(
        str(int(val)),
        xy=(anio, val),
        xytext=(anio, val + offset),
        fontsize=7.8, color=COLOR_LABEL,
        ha=ha, va="bottom",
    )

# Ejes
ax.set_xlim(1999.3, 2023.7)
ax.set_ylim(-5, 85)
ax.set_xticks(aÃ±os)
ax.set_xticklabels([str(a) for a in aÃ±os], rotation=0, fontsize=8.5)
ax.set_yticks([])
ax.tick_params(axis="both", which="both", length=0, labelcolor="#444")
ax.spines[["top","right","left","bottom"]].set_visible(False)
ax.grid(axis="y", color="#e8e8e8", linewidth=0.7)

# Anotaciones 2000 y 2023
ax.annotate("2000", xy=(2000, -4), fontsize=9, fontweight="bold",
            color=COLOR_LABEL, ha="center")
ax.annotate("2023", xy=(2023, -4), fontsize=9, fontweight="bold",
            color=COLOR_LABEL, ha="center")

# Título y fuente
ax.set_title(
    "Figura B.12. Accesos del Servicio Fijo de Internet por cada 100 hogares (2000-2023)",
    fontsize=12, fontweight="bold", color=COLOR_LABEL,
    loc="left", pad=12
)
fig.text(
    0.01, -0.04,
    "Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones a diciembre de cada aÃ±o, del CONAPO y el INEGI.",
    fontsize=7.5, color="#666", style="italic"
)

plt.tight_layout()
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "figura_b12.png")
# Guardar salida
plt.savefig(output_path, dpi=150, bbox_inches="tight")
print(f"\nGuardado: {output_path}")
