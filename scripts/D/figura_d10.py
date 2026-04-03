"""
Figura D.10 — Percepción de seguridad al realizar transacciones bancarias en Internet
por grupo de edad.

Fuente: IFT, Encuesta de Confianza en el Servicio de Internet (ECSI) 2024.

Metodología:
  - Universo  : rescate_internet == 1  (usuarios de Internet)
  - Variable  : seg_banca  (P18_5d)
      1 = Muy seguro | 2 = Seguro | 3 = Ni seguro / Ni inseguro
      4 = Inseguro   | 9 = NS/NR
  - Ponderador: fac_per
  - Denominador: total ponderado del grupo de edad (incluyendo NaN),
                 por eso las barras NO suman 100 %.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

# ── 1. Carga ──────────────────────────────────────────────────────────────────
DATA_PATH = Path(r"C:\Users\ivan-\Documents\GitHub\anuario\datos\D.10\baseconfianzadigital.csv")          # <-- ajusta la ruta si es necesario

df = pd.read_csv(DATA_PATH, low_memory=False)

# ── 2. Filtro universo ────────────────────────────────────────────────────────
usuarios = df[df["rescate_internet"] == 1].copy()

# ── 3. Cálculo ponderado ──────────────────────────────────────────────────────
GRUPOS = {
    1: "18 a 24 años",
    2: "25 a 34 años",
    3: "35 a 44 años",
    4: "45 a 54 años",
    5: "55 a más años",
}

SEG_CODIGOS = {
    "Muy seguro":              1,
    "Seguro":                  2,
    "Ni seguro / Ni inseguro": 3,
    "Inseguro":                4,
    "NS/NR":                   9,
}

resultados = {}

for edad_cod, edad_label in GRUPOS.items():
    grp       = usuarios[usuarios["edad_gpos"] == edad_cod]
    total_w   = grp["fac_per"].sum()                         # denominador del grupo
    row = {}
    for cat_label, seg_cod in SEG_CODIGOS.items():
        peso_cat   = grp.loc[grp["seg_banca"] == seg_cod, "fac_per"].sum()
        row[cat_label] = round(peso_cat / total_w * 100, 1)
    resultados[edad_label] = row

# Convertir a DataFrame  (filas = categorías de seguridad, columnas = grupos de edad)
df_plot = pd.DataFrame(resultados).T          # filas = grupos de edad
df_plot.index.name = "Grupo de edad"

print("\n── Tabla de resultados (% sobre total del grupo de edad) ──")
print(df_plot.to_string())

# ── 4. Gráfica ────────────────────────────────────────────────────────────────
CATEGORIAS   = list(SEG_CODIGOS.keys())
COLORES      = {
    "Muy seguro":              "#3B5EA6",
    "Seguro":                  "#1A3366",
    "Ni seguro / Ni inseguro": "#7EB8D4",
    "Inseguro":                "#C94040",
    "NS/NR":                   "#E8845A",
}

age_labels  = list(GRUPOS.values())
x           = np.arange(len(age_labels))
n_cats      = len(CATEGORIAS)
bar_width   = 0.13
offsets     = np.linspace(-(n_cats - 1) / 2, (n_cats - 1) / 2, n_cats) * bar_width

fig, ax = plt.subplots(figsize=(12, 6.5))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

for i, cat in enumerate(CATEGORIAS):
    valores = [df_plot.loc[g, cat] for g in age_labels]
    bars = ax.bar(
        x + offsets[i],
        valores,
        width=bar_width * 0.92,
        color=COLORES[cat],
        label=cat,
        zorder=3,
    )
    # Etiquetas dentro de la barra (solo si hay espacio suficiente)
    for bar, val in zip(bars, valores):
        if val >= 3.5:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() / 2,
                f"{val:.1f}%",
                ha="center", va="center",
                fontsize=7.5, color="white", fontweight="bold",
                zorder=4,
            )

# Ejes
ax.set_xticks(x)
ax.set_xticklabels(age_labels, fontsize=10.5)
ax.set_ylim(0, 72)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v)}%"))
ax.set_yticks(range(0, 71, 10))
ax.tick_params(axis="y", labelsize=9, colors="#555")
ax.tick_params(axis="x", bottom=False)

# Cuadrícula
ax.yaxis.grid(True, linestyle="--", linewidth=0.5, color="#d8d8d8", zorder=0)
ax.set_axisbelow(True)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.spines["bottom"].set_color("#ccc")

# Leyenda
parches = [
    mpatches.Patch(color=COLORES[c], label=c) for c in CATEGORIAS
]
ax.legend(
    handles=parches,
    loc="upper right",
    fontsize=8.5,
    frameon=False,
    ncol=1,
    handlelength=1.2,
    handleheight=1.0,
)

# Títulos y fuente
ax.set_title(
    "Figura D.10. Porcentaje de la población usuaria de Internet según nivel de seguridad\n"
    "que consideran tiene realizar transacciones bancarias en Internet (por grupo de edad)",
    fontsize=11, fontweight="normal", loc="left", pad=12, color="#222",
)
fig.text(
    0.01, -0.03,
    "Fuente: IFT, con información de la Encuesta de Confianza en el Servicio de Internet (ECSI) 2024.\n"
    "Nota: Respuesta múltiple, por lo que la suma no da 100 %. "
    "Universo: rescate_internet = 1. Ponderador: fac_per.",
    fontsize=7.5, color="#777", va="top",
)

plt.tight_layout()

OUTPUT = Path(r"C:\Users\ivan-\Documents\GitHub\anuario\output\figura_D10.png")
plt.savefig(OUTPUT, dpi=180, bbox_inches="tight", facecolor="white")
print(f"\nGráfica guardada en: {OUTPUT.resolve()}")
plt.show()