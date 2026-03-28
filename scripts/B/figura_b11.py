"""
Figura B.11 â€” Accesos del Servicio Fijo de Internet (2000-2023)
Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones a diciembre de cada aÃ±o.
CSV: TD_ACC_INTER_HIS_ITE_VA.csv
Columna: A_TOTAL_E | Filtro: MES==12 | OperaciÃ³n: SUM por aÃ±o
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
import os

# 1. Carga y cálculo
df = pd.read_csv(PROJECT_ROOT / "datos" / "b.11" / "TD_ACC_INTER_HIS_ITE_VA.csv", encoding="latin1")
df["MES"] = pd.to_numeric(df["MES"], errors="coerce")
df["ANIO"] = pd.to_numeric(df["ANIO"], errors="coerce")
df["A_TOTAL_E"] = pd.to_numeric(df["A_TOTAL_E"], errors="coerce")

data = (
    df[df["MES"] == 12]
    .groupby("ANIO")["A_TOTAL_E"]
    .sum()
    .reset_index()
    .rename(columns={"ANIO": "anio", "A_TOTAL_E": "accesos"})
)
data = data[(data["anio"] >= 2000) & (data["anio"] <= 2023)].reset_index(drop=True)

# Verificación
print("Valores calculados:")
print(data.to_string(index=False))
print(f"\n2000: {data.loc[data.anio==2000,'accesos'].values[0]:,.0f}  (Anuario: 110,133)")
print(f"2023: {data.loc[data.anio==2023,'accesos'].values[0]:,.0f}  (Anuario: 26,749,342)")

# 2. Figura
COLOR_FILL  = "#2A6EBB"
COLOR_LINE  = "#1A4F8A"
COLOR_LABEL = "#1A3A5C"

# Crear grafica
fig, ax = plt.subplots(figsize=(14, 6))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

aÃ±os   = data["anio"].values
valores = data["accesos"].values

ax.fill_between(aÃ±os, valores, alpha=0.18, color=COLOR_FILL)
ax.plot(aÃ±os, valores, color=COLOR_LINE, linewidth=2.2, zorder=3)
ax.scatter(aÃ±os, valores, color=COLOR_LINE, s=28, zorder=4)

# Etiquetas solo en extremos
for anio, val in [(2000, valores[0]), (2023, valores[-1])]:
    idx = list(aÃ±os).index(anio)
    offset = -1_200_000 if anio == 2000 else 800_000
    ax.annotate(
        f"{val:,.0f}",
        xy=(anio, val),
        xytext=(anio, val + offset),
        fontsize=9.5, fontweight="bold", color=COLOR_LABEL,
        ha="center",
    )

# Ejes
ax.set_xlim(1999.3, 2023.7)
ax.set_ylim(-500_000, 31_000_000)
ax.set_xticks(aÃ±os)
ax.set_xticklabels([str(a) for a in aÃ±os], rotation=0, fontsize=8.5)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.yaxis.set_major_locator(mticker.MultipleLocator(5_000_000))
ax.tick_params(axis="both", which="both", length=0, labelcolor="#444")
ax.spines[["top","right","left"]].set_visible(False)
ax.spines["bottom"].set_color("#ccc")
ax.grid(axis="y", color="#e8e8e8", linewidth=0.7)

# Línea vertical divisoria 2000 2023
ax.axvline(x=1999.5, color="#aaa", linewidth=0.8, linestyle="--")
ax.axvline(x=2023.5, color="#aaa", linewidth=0.8, linestyle="--")

# Título y fuente
ax.set_title(
    "Figura B.11. Accesos del Servicio Fijo de Internet (2000-2023)",
    fontsize=12, fontweight="bold", color=COLOR_LABEL,
    loc="left", pad=12
)
fig.text(
    0.01, -0.04,
    "Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones a diciembre de cada aÃ±o.",
    fontsize=7.5, color="#666", style="italic"
)

plt.tight_layout()
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "figura_b11.png")
# Guardar salida
plt.savefig(output_path, dpi=150, bbox_inches="tight")
print(f"\nGuardado: {output_path}")
