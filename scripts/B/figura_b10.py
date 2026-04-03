"""
Figura B.10 (BAF) — Índice Herfindahl-Hirschman. Concentración de mercado
del Servicio Fijo de Acceso a Internet (2013-2023)
Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones a diciembre de cada año.
Nota: IHH estimado con respecto al número de accesos del servicio fijo de internet.
CSV: TD_IHH_BAF_ITE_VA.csv
Columna: IHH_BAF_E | Filtro: MES==12 | años: 2013-2023
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

# 1. Carga y cálculo
df = pd.read_csv(PROJECT_ROOT / "datos" / "b.10" / "TD_IHH_BAF_ITE_VA.csv", encoding="latin1")
df["IHH_BAF_E"] = (
    df["IHH_BAF_E"].astype(str)
    .str.replace(",", "").str.strip()
    .astype(float)
)
df["MES"]  = pd.to_numeric(df["MES"],  errors="coerce")
df["ANIO"] = pd.to_numeric(df["ANIO"], errors="coerce")

data = (
    df[df["MES"] == 12]
    .sort_values("ANIO")
    [["ANIO","IHH_BAF_E"]]
    .rename(columns={"ANIO":"anio","IHH_BAF_E":"ihh"})
)
data = data[(data["anio"] >= 2013) & (data["anio"] <= 2023)].reset_index(drop=True)

print("Valores calculados IHH BAF:")
print(data.to_string(index=False))

# 2. Figura
COLOR_BAR   = "#2A8FA0"   # teal similar al Anuario
COLOR_LABEL = "#1A3A5C"

# Crear grafica
fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

años    = data["anio"].values
valores = data["ihh"].values

# Barras horizontales
bars = ax.barh(
    [str(a) for a in años],
    valores,
    color=COLOR_BAR,
    height=0.65,
    zorder=3,
)

# Etiquetas al final de cada barra
for bar, val in zip(bars, valores):
    ax.text(
        val + 30, bar.get_y() + bar.get_height() / 2,
        f"{int(val):,}",
        va="center", ha="left",
        fontsize=9.5, color=COLOR_LABEL, fontweight="bold"
    )

# Ejes
ax.set_xlim(0, max(valores) * 1.15)
ax.invert_yaxis()
ax.set_xlabel("")
ax.set_xticks([])
ax.tick_params(axis="y", which="both", length=0, labelsize=10, labelcolor="#333")
ax.spines[["top","right","bottom","left"]].set_visible(False)

# Etiquetas de año extremo
ax.text(
    -50, 0, "2013", ha="right", va="center",
    fontsize=9, color="#555"
)

# Título y fuente
ax.set_title(
    "Índice Herfindahl-Hirschman (IHH).\nConcentración de mercado del Servicio Fijo de Internet (2013-2023)",
    fontsize=11, fontweight="bold", color=COLOR_LABEL,
    loc="left", pad=12
)
fig.text(
    0.01, -0.02,
    "Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones a diciembre de cada año.\n"
    "Nota: IHH estimado con respecto al número de accesos del servicio fijo de internet.",
    fontsize=7.5, color="#666", style="italic"
)

plt.tight_layout()
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "figura_b10.png")
# Guardar salida
plt.savefig(output_path, dpi=150, bbox_inches="tight")
print(f"\nGuardado: {output_path}")
