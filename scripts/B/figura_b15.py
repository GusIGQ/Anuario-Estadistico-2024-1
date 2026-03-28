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
from pathlib import Path

# Rutas
INPUT  = PROJECT_ROOT / "datos" / "b.15" / "TD_ACC_BAFXV_ITE_VA.csv"
OUTPUT = PROJECT_ROOT / "output" / "Figura_B15.png"
Path(OUTPUT).parent.mkdir(parents=True, exist_ok=True)

# Lectura y filtro
df = pd.read_csv(INPUT, encoding="cp1252")
dic = df[df["MES"] == 12].copy()
dic = dic[(dic["ANIO"] >= 2013) & (dic["ANIO"] <= 2023)]

# Agregación por año
agg = dic.groupby("ANIO")[
    ["A_V1_E", "A_V2_E", "A_V3_E", "A_V4_E", "A_NO_ESPECIFICADO_E", "A_TOTAL_E"]
].sum()

# Porcentajes
tot = agg["A_TOTAL_E"]
pct = pd.DataFrame({
    "v1": agg["A_V1_E"]               / tot * 100,
    "v2": agg["A_V2_E"]               / tot * 100,
    "v3": agg["A_V3_E"]               / tot * 100,
    "v4": agg["A_V4_E"]               / tot * 100,
    "ns": agg["A_NO_ESPECIFICADO_E"]  / tot * 100,
}, index=agg.index)

years  = pct.index.tolist()
n      = len(years)
x      = np.arange(n)
w      = 0.55

# Colores (mismo orden visual de la gráfica original)
C_V1 = "#7EC8C8"   # azul claro  â€” 256 Kbpsâ€“1.99 Mbps
C_V2 = "#B0D8E8"   # azul pÃ¡lido â€” 2â€“9.99 Mbps
C_V3 = "#1B3A6B"   # azul oscuro â€” 10â€“100 Mbps
C_V4 = "#F4956A"   # salmÃ³n      â€” >100 Mbps
C_NS = "#E84040"   # rojo        â€” Sin informaciÃ³n

# Figura
fig, ax = plt.subplots(figsize=(16, 8))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# Barras apiladas (orden de abajo a arriba: v3, v2, v1, v4, ns)
bar_v3 = ax.bar(x, pct["v3"], w, color=C_V3, zorder=3)
bar_v2 = ax.bar(x, pct["v2"], w, bottom=pct["v3"], color=C_V2, zorder=3)
bar_v1 = ax.bar(x, pct["v1"], w, bottom=pct["v3"]+pct["v2"], color=C_V1, zorder=3)
bar_v4 = ax.bar(x, pct["v4"], w,
                bottom=pct["v3"]+pct["v2"]+pct["v1"], color=C_V4, zorder=3)
bar_ns = ax.bar(x, pct["ns"], w,
                bottom=pct["v3"]+pct["v2"]+pct["v1"]+pct["v4"], color=C_NS, zorder=3)

# Etiquetas dentro de las barras
def label(bars, bottoms, vals, color="white", threshold=2.0):
    for i, (b, bot, v) in enumerate(zip(bars, bottoms, vals)):
        if v >= threshold:
            ax.text(b.get_x() + b.get_width()/2,
                    bot + v/2,
                    f"{v:.0f}%" if v >= 1 else f"{v:.2f}%",
                    ha="center", va="center",
                    fontsize=7.5, fontweight="bold", color=color, zorder=5)

zeros = pd.Series([0]*n, index=years)
label(bar_v3, zeros,                                   pct["v3"])
label(bar_v2, pct["v3"],                               pct["v2"], color="#333333")
label(bar_v1, pct["v3"]+pct["v2"],                    pct["v1"], color="#333333")
label(bar_v4, pct["v3"]+pct["v2"]+pct["v1"],          pct["v4"], color="white")
label(bar_ns, pct["v3"]+pct["v2"]+pct["v1"]+pct["v4"],pct["ns"], color="white", threshold=0.5)

# Etiquetas pequeñas encima de la barra (valores threshold que igual se muestran arriba)
for i, yr in enumerate(years):
    top = pct.loc[yr, ["v1","v2","v3","v4","ns"]].sum()
    for col, offset in [("ns", 0), ("v4", -0.5)]:
        v = pct.loc[yr, col]
        if v < 2.0 and v > 0.005:
            ax.text(x[i], top + 1.2 - (0 if col=="ns" else 2.5),
                    f"{v:.1f}%" if v < 1 else f"{v:.0f}%",
                    ha="center", va="bottom", fontsize=6.5,
                    color=C_NS if col=="ns" else C_V4, zorder=5)

# Decoración
ax.set_xticks(x)
ax.set_xticklabels([str(y) for y in years], fontsize=10)
ax.set_ylim(0, 115)
ax.set_yticks([])
ax.spines[["top","right","left"]].set_visible(False)
ax.spines["bottom"].set_color("#cccccc")
ax.tick_params(axis="x", length=0)
ax.grid(False)

# Total nacional 2023
total_2023 = int(agg.loc[2023, "A_TOTAL_E"])
fig.text(0.50, 0.93,
         "Total de accesos del Servicio Fijo de Internet a nivel nacional:",
         ha="center", fontsize=9.5, color="#444444")
fig.text(0.50, 0.87,
         f"{total_2023:,}",
         ha="center", fontsize=22, fontweight="bold", color="#1B3A6B")

# Título
fig.text(0.02, 0.97,
         "â— Figura B.15. DistribuciÃ³n de los accesos del Servicio Fijo de Internet "
         "por rangos de velocidad (2013-2023)",
         fontsize=10, fontweight="bold", color="#1B3A6B", va="top")

# Leyenda
patches = [
    mpatches.Patch(color=C_V1, label="256 Kbps y 1.99 Mbps"),
    mpatches.Patch(color=C_V2, label="2 Mbps y 9.99 Mbps"),
    mpatches.Patch(color=C_V3, label="10 Mbps y 100 Mbps"),
    mpatches.Patch(color=C_V4, label="Mayores a 100 Mbps"),
    mpatches.Patch(color=C_NS, label="Sin informaciÃ³n de velocidad"),
]
ax.legend(handles=patches, loc="upper center",
          bbox_to_anchor=(0.5, -0.08), ncol=5,
          fontsize=8.5, frameon=False)

# Fuente
fig.text(0.02, 0.01,
         "Fuente: IFT con datos de los operadores de telecomunicaciones a diciembre de cada aÃ±o.",
         fontsize=8, color="#666666")

plt.tight_layout(rect=[0, 0.04, 1, 0.85])
# Guardar salida
plt.savefig(OUTPUT, dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print(f"Figura guardada en: {OUTPUT}")
print(f"\nVerificaciÃ³n 2023:")
for col, label_str, anuario in [
    ("v1","256K-2M","5%"), ("v2","2M-10M","0.01%"),
    ("v3","10M-100M","65%"), ("v4",">100M","25%"), ("ns","Sin info","4.5%")
]:
    print(f"  {label_str:12s}: {pct.loc[2023, col]:.2f}%  â†’ Anuario: {anuario}")
