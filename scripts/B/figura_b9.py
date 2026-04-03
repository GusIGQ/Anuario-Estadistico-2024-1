"""
Figura B.9 — Participación de mercado del Servicio Fijo de Telefonía (2013-2023)
Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones
        a diciembre de cada año.
Archivo: TD_MARKET_SHARE_TELFIJA_ITE_VA.csv
Portal:  https://bit.ift.org.mx/BitWebApp/descargaDatos.xhtml
         Sección: Servicio Fijo de Telefonía

Metodología:
- Filtrar MES == 12 (diciembre) y ANIO 2013-2023
- Mapear operadores individuales a 7 grupos (como en la figura)
- Los valores de MARKET_SHARE ya están precalculados en el CSV
- Para 2021: MAXCOM (0.37%) aparece bajo DISH-MVS en el CSV actual
  â†’ se mantiene en "Otros" (diferencia de redondeo vs Anuario)
- Para 2023: pequeñas diferencias (~0.3-1%) por revisiones posteriores
  de operadores (comportamiento documentado en el Anuario)
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
import matplotlib.patches as mpatches
import numpy as np

# 1. LECTURA Y LIMPIEZA
df = pd.read_csv(
    "datos/b.9/TD_MARKET_SHARE_TELFIJA_ITE_VA.csv",
    encoding="latin1"
)
df["MARKET_SHARE"] = (
    df["MARKET_SHARE"].str.replace("%", "").str.strip().astype(float)
)

# 2. FILTRO: diciembre, 2013-2023
df_dic = df[(df["MES"] == 12) & (df["ANIO"].between(2013, 2023))].copy()

# 3. MAPEO DE OPERADORES A GRUPOS
# Operadores con nombre explícito en la figura mapeo directo
# El resto Otros
mapeo = {
    "América Móvil":  " América Móvil",
    "GRUPO TELEVISA": "Grupo Televisa",
    "MEGACABLE-MCM":  "Megacable-MCM",
    "GRUPO SALINAS":  "Grupo Salinas",
    "AXTEL":          "Axtel",
    "TELEFÓNICA":     "Telefónica",
}
df_dic["GRUPO_FIGURA"] = df_dic["GRUPO"].map(mapeo).fillna("Otros")

# 4. PIVOTE: años - grupos
pivot = (
    df_dic
    .groupby(["ANIO", "GRUPO_FIGURA"])["MARKET_SHARE"]
    .sum()
    .unstack(fill_value=0)
)

# Orden de columnas igual que en la figura (de abajo a arriba en la barra)
orden = [
    " América Móvil",
    "Grupo Televisa",
    "Megacable-MCM",
    "Grupo Salinas",
    "Axtel",
    "Telefónica",
    "Otros",
]
pivot = pivot.reindex(columns=orden, fill_value=0)

years = pivot.index.tolist()

# 5. COLORES (paleta del Anuario IFT)
colores = {
    " América Móvil":  "#1a3a5c",   # azul marino oscuro
    "Grupo Televisa": "#4a9fd4",   # azul claro
    "Megacable-MCM":  "#1b2a4a",   # azul muy oscuro
    "Grupo Salinas":  "#e8956a",   # naranja
    "Axtel":          "#d64c3e",   # rojo
    "Telefónica":     "#5bbfb5",   # turquesa
    "Otros":          "#7fc8e0",   # azul pálido
}

# 6. FIGURA
fig, ax = plt.subplots(figsize=(16, 8))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

x = np.arange(len(years))
bar_w = 0.55

bottoms = np.zeros(len(years))
bars_dict = {}

for grupo in orden:
    vals = pivot[grupo].values
    bars = ax.bar(x, vals, bar_w, bottom=bottoms,
                  color=colores[grupo], label=grupo,
                  zorder=2)
    bars_dict[grupo] = (bars, bottoms.copy(), vals)
    bottoms += vals

# 7. ETIQUETAS DENTRO DE CADA SEGMENTO
# Solo etiquetas visibles ( 0.5%)
for grupo in orden:
    bars, bot, vals = bars_dict[grupo]
    for i, (bar, b, v) in enumerate(zip(bars, bot, vals)):
        if v >= 0.5:
            cy = b + v / 2
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                cy,
                f"{v:.2f}%",
                ha="center", va="center",
                fontsize=6.5, color="white", fontweight="bold",
                zorder=3
            )

# 8. EJES Y ESTILO
ax.set_xticks(x)
ax.set_xticklabels(years, fontsize=10)
ax.set_ylim(0, 105)
ax.set_yticks([])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.yaxis.set_visible(False)
ax.tick_params(axis="x", length=0)

# 9. LEYENDA
handles = [
    mpatches.Patch(color=colores[g], label=g) for g in orden
]
ax.legend(
    handles=handles,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.12),
    ncol=7,
    fontsize=8.5,
    frameon=False,
    handlelength=1.2,
    handleheight=0.8,
)

# 10. TÍTULO Y FUENTE
ax.set_title(
    "Figura B.9. Participación de mercado del Servicio Fijo de Telefonía (2013-2023)",
    fontsize=12, fontweight="bold", loc="left", pad=14,
    color="#c0392b"
)
fig.text(
    0.01, -0.04,
    "Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones a diciembre de cada año.\n"
    "Nota: Participación de mercado estimada con respecto al número de líneas del servicio fijo de telefonía.",
    fontsize=7.5, color="#555555"
)

plt.tight_layout(rect=[0, 0.04, 1, 1])
# Guardar salida
plt.savefig("figura_B9.png", dpi=180, bbox_inches="tight",
            facecolor="white")
plt.close()
print("figura_B9.png generada")

# 11. VERIFICACI N DE VALORES CLAVE
print("\n=== Verificación vs Anuario (valores clave) ===")
checks = {
    2013: (" América Móvil", 70.11),
    2015: ("Grupo Televisa", 14.76),
    2019: ("Megacable-MCM", 11.17),
    2020: ("Grupo Salinas", 11.32),
}
for anio, (grp, esperado) in checks.items():
    calc = pivot.loc[anio, grp]
    ok = "âœ…" if abs(calc - esperado) < 0.05 else "âš ï¸"
    print(f"  {anio} {grp}: calculado={calc:.2f}%  esperado={esperado:.2f}%  {ok}")
