"""
Figura C.16 â€” Herfindahl-Hirschman (IHH). ConcentraciÃ³n de mercado
              del servicio mÃ³vil de acceso a Internet (2013-2023)
Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones
        a diciembre de cada aÃ±o.
Nota: IHH estimado con respecto al nÃºmero de lÃ­neas del servicio mÃ³vil de
      acceso a Internet.

Archivo de entrada: TD_IHH_INTMOVIL_ITE_VA.csv
  - Columna usada: IHH_TELFIJA_E
  - Filtro: MES == 12, ANIO 2013-2023
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
import os, sys

# 1. LECTURA
CSV_PATH = PROJECT_ROOT / "datos" / "C.16" / "TD_IHH_INTMOVIL_ITE_VA.csv"
if not os.path.exists(CSV_PATH):
    print(f"ERROR: No se encontrÃ³ {CSV_PATH}")
    sys.exit(1)

# Cargar datos
df = pd.read_csv(CSV_PATH, encoding="latin-1")

# 2. LIMPIEZA
# La columna viene con comas como separador de miles limpiar antes de convertir
df["IHH"] = df["IHH_TELFIJA_E"].astype(str).str.replace(",", "").str.strip()
df["IHH"] = pd.to_numeric(df["IHH"], errors="coerce")

# 3. FILTRO: diciembre, 2013-2023
df_dic = df[(df["MES"] == 12) & (df["ANIO"] >= 2013) & (df["ANIO"] <= 2023)].copy()
df_dic = df_dic.sort_values("ANIO").reset_index(drop=True)

anios = df_dic["ANIO"].tolist()
ihh   = df_dic["IHH"].tolist()

print("â”€â”€ Valores calculados â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€")
print(f"{'AÃ±o':>4}  {'IHH':>6}")
for a, v in zip(anios, ihh):
    print(f"{a:>4}  {v:>6,.0f}")

# 4. GRÁFICA: barras horizontales
COLOR_BARRA = "#1A6B8A"   # azul petrÃ³leo (igual al Anuario)
COLOR_TEXTO = "#333333"

# Crear grafica
fig, ax = plt.subplots(figsize=(11, 7))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# Las barras van de abajo (2023) a arriba (2013) invertir orden para que
# 2013 quede en la parte superior del eje Y
anios_inv = anios[::-1]
ihh_inv   = ihh[::-1]

y = range(len(anios_inv))
bar_h = 0.55

bars = ax.barh(list(y), ihh_inv, bar_h, color=COLOR_BARRA)

# 5. ETIQUETAS AL FINAL DE CADA BARRA
x_max = max(ihh_inv)
for bar, val in zip(bars, ihh_inv):
    ax.text(
        val + x_max * 0.008,
        bar.get_y() + bar.get_height() / 2,
        f"{val:,.0f}",
        ha="left", va="center",
        fontsize=10, color=COLOR_TEXTO, fontweight="bold"
    )

# 6. EJES Y FORMATO
ax.set_yticks(list(y))
ax.set_yticklabels(anios_inv, fontsize=10)
ax.set_xlim(0, x_max * 1.12)
ax.set_xticks([])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.tick_params(axis="y", left=False)

# 7. TÍTULO Y FUENTE
fig.text(
    0.07, 0.97,
    "â–   Figura C.16.  Herfindahl-Hirschman (IHH). ConcentraciÃ³n de mercado\n"
    "    del servicio mÃ³vil de acceso a Internet (2013-2023)",
    fontsize=11, fontweight="bold", color="#2D3270", va="top"
)
fig.text(
    0.07, 0.025,
    "Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones a diciembre de cada aÃ±o.\n"
    "Nota: Herfindahl-Hirschman (IHH) estimado con respecto al nÃºmero de lÃ­neas del servicio mÃ³vil de acceso a Internet.",
    fontsize=7.8, color="#555555"
)

plt.tight_layout(rect=[0, 0.07, 1, 0.93])

os.makedirs("output", exist_ok=True)
OUTPUT = "output/Figura_C16.png"
# Guardar salida
plt.savefig(OUTPUT, dpi=150, bbox_inches="tight", facecolor="white")
plt.savefig("output/Figura_C16.pdf", bbox_inches="tight", facecolor="white")
print(f"\nGuardado en {OUTPUT}")
plt.close()
