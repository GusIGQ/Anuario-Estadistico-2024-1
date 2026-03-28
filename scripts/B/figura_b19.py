"""
Figura B.19 â€” Accesos del Servicio de TelevisiÃ³n Restringida (1998â€“2023)
=========================================================================
Fuente : IFT con datos proporcionados por los operadores de
         telecomunicaciones a diciembre de cada aÃ±o.
Archivo: TD_ACC_TVRES_HIS_ITE_VA.csv
         Descargable desde la secciÃ³n "Servicio de TelevisiÃ³n Restringida" en
         https://bit.ift.org.mx/BitWebApp/descargaDatos.xhtml
Salida : output/Figura_B19.png

MetodologÃ­a
-----------
1. Leer el CSV histÃ³rico de accesos de TV restringida.
2. Filtrar solo el mes de diciembre (MES == 12) de cada aÃ±o.
3. Agrupar por aÃ±o y sumar accesos de todos los operadores (A_TOTAL_E).
4. Filtrar el rango 1998â€“2023.
5. Graficar lÃ­nea con Ã¡rea sombreada y etiquetas en los extremos (1998 y 2023).

FÃ³rmula
-------
accesos_anio = SUM(A_TOTAL_E)  para MES == 12, agrupado por ANIO

Nota de discrepancia
--------------------
El valor de 2023 calculado desde el CSV es 23,485,338, mientras que el
Anuario publica 23,418,226 (diferencia de ~67,000 accesos, ~0.3%).
Esta diferencia es atribuible a revisiones posteriores de los operadores,
comportamiento documentado en el propio Anuario y esperado en todos los
archivos del BIT.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import matplotlib.ticker as mticker

# Rutas
CSV_PATH = PROJECT_ROOT / "datos" / "b.19" / "TD_ACC_TVRES_HIS_ITE_VA.csv"
OUT_DIR  = PROJECT_ROOT / "output"
OUT_FILE = os.path.join(OUT_DIR, "Figura_B19.png")

# Colores IFT (paleta del Anuario)
COLOR_LINEA  = "#1B2A6B"   # azul marino IFT
COLOR_AREA   = "#C8D4F0"   # azul claro para relleno
COLOR_PUNTO  = "#1B2A6B"
COLOR_TEXTO  = "#1B2A6B"
COLOR_ETIQ   = "#FFFFFF"   # texto sobre marcador de valor

# 1. Lectura y procesamiento
df = pd.read_csv(CSV_PATH, encoding="latin1")

df_dic   = df[df["MES"] == 12]
serie    = df_dic.groupby("ANIO")["A_TOTAL_E"].sum()
serie    = serie[(serie.index >= 1998) & (serie.index <= 2023)].copy()
serie    = serie.sort_index()

anios    = serie.index.tolist()
valores  = serie.values.tolist()

# 2. Figura
fig, ax = plt.subplots(figsize=(14, 6))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# Área sombreada
ax.fill_between(anios, valores, alpha=0.18, color=COLOR_AREA)

# Línea principal
ax.plot(anios, valores, color=COLOR_LINEA, linewidth=2.2, zorder=3)

# Puntos en todos los años
ax.scatter(anios, valores, color=COLOR_PUNTO, s=38, zorder=4)

# Etiquetas en extremos (1998 y 2023)
for anio, valor, ha, offset_x in [
    (anios[0],  valores[0],  "right", -0.3),
    (anios[-1], valores[-1], "left",  +0.3),
]:
    ax.annotate(
        f"{valor:,.0f}",
        xy=(anio, valor),
        xytext=(anio + offset_x, valor + 600_000),
        fontsize=9.5,
        fontweight="bold",
        color=COLOR_TEXTO,
        ha=ha,
        va="bottom",
    )

# Ejes
ax.set_xlim(anios[0] - 0.8, anios[-1] + 0.8)
ax.set_ylim(0, 28_000_000)

ax.set_xticks(anios)
ax.set_xticklabels(
    [str(a) for a in anios],
    rotation=45, ha="right", fontsize=8.5, color="#333333"
)

ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"{x:,.0f}")
)
ax.tick_params(axis="y", labelsize=8.5, colors="#333333")

# Grilla horizontal ligera
ax.yaxis.grid(True, linestyle="--", linewidth=0.5, color="#CCCCCC", alpha=0.7)
ax.set_axisbelow(True)

# Quitar bordes innecesarios
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
ax.spines["left"].set_color("#CCCCCC")
ax.spines["bottom"].set_color("#CCCCCC")

# Títulos y nota al pie
ax.set_title(
    "Figura B.19. Accesos del Servicio de TelevisiÃ³n Restringida (1998-2023)",
    fontsize=11, fontweight="bold", color=COLOR_TEXTO,
    loc="left", pad=12
)

fig.text(
    0.01, -0.04,
    "Fuente: IFT con datos proporcionados por los operadores de "
    "telecomunicaciones a diciembre de cada aÃ±o.",
    fontsize=7.5, color="#555555", style="italic"
)

# Guardar
os.makedirs(OUT_DIR, exist_ok=True)
plt.tight_layout()
# Guardar salida
plt.savefig(OUT_FILE, dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print(f"Figura guardada en: {OUT_FILE}")
print(f"Valor 1998 : {valores[0]:>15,.0f}")
print(f"Valor 2023 : {valores[-1]:>15,.0f}  (Anuario: 23,418,226)")
