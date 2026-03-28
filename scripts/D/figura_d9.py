"""
Figura D.9 â€” Porcentaje de la poblaciÃ³n usuaria de Internet segÃºn nivel de seguridad
que consideran tiene realizar diferentes actividades en Internet (por grupo de edad)
SubtÃ­tulo mostrado: PercepciÃ³n de seguridad al realizar compras en Internet

Fuente: IFT, con informaciÃ³n de la Encuesta de Confianza en el Servicio de Internet (ECSI) 2024.
Archivo de entrada: baseconfianzadigital__3_.csv

Variable principal : seg_comp  (pregunta 18.5c)
Factor de expansiÃ³n: fac_per
Filtro             : rescate_internet == 1  (usuarios de internet)
Desglose           : edad_gpos (1=18-24, 2=25-34, 3=35-44, 4=45-54, 5=55+)

Mapeo de categorÃ­as:
  1 â†’ Muy seguro
  2 â†’ Seguro
  3 â†’ Ni seguro / Ni inseguro
  4 â†’ Inseguro
  5 + 9 + NaN â†’ NS/NR

FÃ³rmula:
  pct(cat, edad) = SUM(fac_per | cat & edad) / SUM(fac_per | rescate_internet==1 & edad) * 100

Nota: NS/NR puede diferir ~0.3-1 pp del Anuario (misma discrepancia documentada en README).
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import matplotlib.patches as mpatches

# 1. DATOS
CSV_PATH = PROJECT_ROOT / "datos" / "D.9" / "baseconfianzadigital.csv"

# Cargar datos
df = pd.read_csv(CSV_PATH, low_memory=False)

# Filtrar usuarios de internet
users = df[df["rescate_internet"] == 1].copy()

# Categorizar seg_comp: 5 NS/NR, NaN NS/NR
users["cat"] = users["seg_comp"].map({1.0: 1, 2.0: 2, 3.0: 3, 4.0: 4, 5.0: 9, 9.0: 9})
users["cat"] = users["cat"].fillna(9).astype(int)

AGE_CODES  = [1, 2, 3, 4, 5]
AGE_LABELS = ["18 a 24 aÃ±os", "25 a 34 aÃ±os", "35 a 44 aÃ±os", "45 a 54 aÃ±os", "55 a mÃ¡s aÃ±os"]
CAT_CODES  = [1, 2, 3, 4, 9]
CAT_LABELS = ["Muy seguro", "Seguro", "Ni seguro/ Ni inseguro", "Inseguro", "NS/NR"]

# 2. CÁLCULO PONDERADO
results = {}
for age_code, age_lbl in zip(AGE_CODES, AGE_LABELS):
    sub      = users[users["edad_gpos"] == age_code]
    total_w  = sub["fac_per"].sum()
    row = {}
    for c, c_lbl in zip(CAT_CODES, CAT_LABELS):
        w = sub[sub["cat"] == c]["fac_per"].sum()
        row[c_lbl] = round(w / total_w * 100, 1)
    results[age_lbl] = row

print("Valores calculados:")
for age, row in results.items():
    print(f"\n  {age}")
    for cat, val in row.items():
        print(f"    {cat:26s}: {val}%")

# 3. PREPARAR DATOS PARA LA GRÁFICA
# Colores del Anuario IFT
COLORS = {
    "Muy seguro":               "#A8D5E2",   # azul muy claro
    "Seguro":                   "#E8856A",   # salmÃ³n / naranja
    "Ni seguro/ Ni inseguro":   "#2C3E7A",   # azul marino oscuro
    "Inseguro":                 "#C0392B",   # rojo
    "NS/NR":                    "#1A2557",   # azul muy oscuro
}

n_ages = len(AGE_LABELS)
n_cats = len(CAT_LABELS)
x      = np.arange(n_ages)
# ancho total del cluster / número de categorías
width  = 0.14
offsets = np.linspace(-(n_cats - 1) / 2 * width, (n_cats - 1) / 2 * width, n_cats)

# 4. GRÁFICA
fig, ax = plt.subplots(figsize=(13, 7))
fig.patch.set_facecolor("white")

for i, (cat_lbl, offset) in enumerate(zip(CAT_LABELS, offsets)):
    vals = [results[age][cat_lbl] for age in AGE_LABELS]
    bars = ax.bar(x + offset, vals, width=width * 0.92,
                  color=COLORS[cat_lbl], zorder=3, label=cat_lbl)

    # Etiquetas encima de cada barra
    for bar, val in zip(bars, vals):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"{val}%",
            ha="center", va="bottom",
            fontsize=7.5, fontweight="bold", color="#222222",
        )

# Ejes
ax.set_xticks(x)
ax.set_xticklabels(AGE_LABELS, fontsize=11, color="#333333")
ax.set_ylim(0, 66)
ax.set_yticks(range(0, 70, 10))
ax.set_yticklabels([f"{v}%" for v in range(0, 70, 10)], fontsize=10, color="#555555")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#CCCCCC")
ax.spines["bottom"].set_color("#CCCCCC")
ax.yaxis.grid(True, color="#EEEEEE", linewidth=0.8, zorder=0)
ax.set_axisbelow(True)

# Leyenda
legend_handles = [mpatches.Patch(color=COLORS[c], label=c) for c in CAT_LABELS]
ax.legend(
    handles=legend_handles,
    ncol=5,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.10),
    frameon=False,
    fontsize=9.5,
    handlelength=1.3,
)

# Título y notas
ax.set_title(
    "Figura D.9. Porcentaje de la poblaciÃ³n usuaria de Internet segÃºn nivel de seguridad\n"
    "que consideran tiene realizar diferentes actividades en Internet (por grupo de edad)",
    fontsize=12, fontweight="bold", color="#1A1A2E", pad=32, loc="left",
)

# Badge / callout Percepción de seguridad al realizar compras en Internet
ax.annotate(
    "PercepciÃ³n de seguridad al\nrealizar compras en Internet",
    xy=(0.58, 0.90), xycoords="axes fraction",
    fontsize=9, ha="center", va="center",
    bbox=dict(boxstyle="round,pad=0.5", facecolor="#EAF4FB", edgecolor="#7EC8C8", linewidth=1.2),
)

fig.text(
    0.01, -0.03,
    "Fuente: IFT, con informaciÃ³n de la Encuesta de Confianza en el Servicio de Internet (ECSI) 2024.\n"
    "Nota: Respuesta mÃºltiple, por lo que la suma no da 100%. "
    "Los resultados pueden presentar variaciones explicadas por el error teÃ³rico de cada encuesta.",
    fontsize=8, color="#666666",
)

plt.tight_layout()

# 5. GUARDAR
OUTPUT = PROJECT_ROOT / "output" / "Figura_D9.png"
# Guardar salida
plt.savefig(OUTPUT, dpi=150, bbox_inches="tight", facecolor="white")
print(f"\nGuardada â†’ {OUTPUT}")
plt.close()
