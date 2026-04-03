"""
Figura C.15 — Participación de mercado del servicio móvil de acceso a Internet (2013-2023)
Fuente: IFT con datos de los operadores de telecomunicaciones a diciembre de cada año.
Nota: Participación de mercado calculada con respecto al número de líneas del servicio móvil de Internet.

Archivo de entrada: TD_MARKET_SHARE_INTMOVIL_ITE_VA.csv
  - Columnas usadas: ANIO, MES, K_GRUPO, GRUPO, MARKET_SHARE
  - Filtro: MES == 12, ANIO 2013-2023
  - Agrupación: 5 grupos ( América Móvil, AT&T, Grupo Walmart, Telefónica, Otros)
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
import os, sys

# 1. LECTURA
CSV_PATH = PROJECT_ROOT / "datos" / "C.15" / "TD_MARKET_SHARE_INTMOVIL_ITE_VA.csv"
if not os.path.exists(CSV_PATH):
    print(f"ERROR: No se encontró {CSV_PATH}")
    sys.exit(1)

# Cargar datos
df = pd.read_csv(CSV_PATH, encoding="latin-1")

# 2. LIMPIEZA
df["MS"] = df["MARKET_SHARE"].str.replace("%", "").astype(float)

# 3. FILTRO: diciembre, 2013-2023
df_dic = df[(df["MES"] == 12) & (df["ANIO"] >= 2013) & (df["ANIO"] <= 2023)].copy()

# 4. MAPEO DE OPERADORES A GRUPOS DE LA FIGURA
# Basado en K_GRUPO (código único del IFT):
# G006 AM RICA M VIL América Móvil
# G007 AT&T AT&T
# C804 GRUPO WALMART Grupo Walmart
# G003 TELEF NICA Telefónica
# todo lo demás Otros
def mapear_grupo(k_grupo, nombre):
    if k_grupo == "G006":
        return " América Móvil"
    if k_grupo == "G007":
        return "AT&T"
    if k_grupo == "C804":
        return "Grupo Walmart"
    if k_grupo == "G003":
        return "Telefónica"
    return "Otros"

df_dic["GRUPO_FIG"] = df_dic.apply(
    lambda r: mapear_grupo(r["K_GRUPO"], r["GRUPO"]), axis=1
)

# 5. CÁLCULO DE MARKET SHARE POR GRUPO Y A O
ORDEN = [" América Móvil", "AT&T", "Grupo Walmart", "Telefónica", "Otros"]

pivot = (
    df_dic.groupby(["ANIO", "GRUPO_FIG"])["MS"]
    .sum()
    .unstack(fill_value=0)
    .reindex(columns=ORDEN, fill_value=0)
)

print("── Valores calculados ──────────────────────────────────────────────────")
print(f"{'año':>4}  {' América Móvil':>13}  {'AT&T':>6}  {'G.Walmart':>9}  {'Telefónica':>10}  {'Otros':>5}")
for anio, row in pivot.iterrows():
    print(f"{anio:>4}  {row[' América Móvil']:>13.2f}  {row['AT&T']:>6.2f}  "
          f"{row['Grupo Walmart']:>9.2f}  {row['Telefónica']:>10.2f}  {row['Otros']:>5.2f}")

anios = pivot.index.tolist()

# 6. COLORES (igual que el Anuario)
COLORES = {
    " América Móvil": "#F4A07A",   # salmón/naranja claro
    "AT&T":          "#2D3270",   # azul marino oscuro
    "Grupo Walmart": "#4A5299",   # azul marino medio
    "Telefónica":    "#A8D8EA",   # azul claro/celeste
    "Otros":         "#E8614A",   # rojo-coral
}

# 7. GRÁFICA
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

x = range(len(anios))
bar_w = 0.6
bottoms = [0.0] * len(anios)

bar_refs = {}
for grupo in ORDEN:
    vals = pivot[grupo].tolist()
    bars = ax.bar(x, vals, bar_w, bottom=bottoms, color=COLORES[grupo], label=grupo)
    bar_refs[grupo] = (bars, vals, bottoms[:])

    # Etiqueta dentro de la barra si es visible ( 1.5 pp)
    for bar, val, bot in zip(bars, vals, bottoms):
        if val >= 1.5:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bot + val / 2,
                f"{val:.2f}%",
                ha="center", va="center",
                fontsize=7.2, color="white", fontweight="bold"
            )

    bottoms = [b + v for b, v in zip(bottoms, vals)]

# 8. EJES Y FORMATO
ax.set_xlim(-0.5, len(anios) - 0.5)
ax.set_ylim(0, 107)
ax.set_xticks(list(x))
ax.set_xticklabels(anios, fontsize=10)
ax.set_yticks([])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.tick_params(axis="x", bottom=False)

# 9. LEYENDA
parches = [mpatches.Patch(color=COLORES[g], label=g) for g in ORDEN]
ax.legend(
    handles=parches,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.12),
    ncol=5,
    frameon=False,
    fontsize=9.5,
)

# 10. TÍTULO Y FUENTE
fig.text(
    0.07, 0.96,
    "Figura C.15. Participación de mercado del servicio móvil de acceso a Internet (2013-2023)",
    fontsize=11, fontweight="bold", color="#2D3270", va="top"
)
fig.text(
    0.07, 0.025,
    "Fuente: IFT con datos de los operadores de telecomunicaciones a diciembre de cada año.\n"
    "Nota: Participación de mercado calculada con respecto al número de líneas del servicio móvil de Internet.",
    fontsize=7.5, color="#555555"
)

plt.tight_layout(rect=[0, 0.07, 1, 0.94])

os.makedirs("output", exist_ok=True)
OUTPUT = "output/Figura_C15.png"
# Guardar salida
plt.savefig(OUTPUT, dpi=150, bbox_inches="tight", facecolor="white")
plt.savefig("output/Figura_C15.pdf", bbox_inches="tight", facecolor="white")
print(f"\nGuardado en {OUTPUT}")
plt.close()
