"""
Figura B.23 — Tecnologías de conexión del Servicio de Televisión Restringida por segmento
Fuente: IFT con datos de los operadores de telecomunicaciones a diciembre de 2023.
Archivo: TD_ACC_TVRES_ITE_VA.CSV
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

# Rutas
INPUT  = PROJECT_ROOT / "datos" / "B.23" / "TD_ACC_TVRES_ITE_VA.CSV"
OUTPUT = "output/Figura_B23.png"
os.makedirs("output", exist_ok=True)

# Lectura y filtro
df = pd.read_csv(INPUT, encoding="latin-1", low_memory=False)

# Normalizar nombre duplicado por mayúsculas/minúsculas (igual que B.16)
df["TECNO_ACCESO_TV"] = df["TECNO_ACCESO_TV"].str.strip()

# Filtrar diciembre 2023
df = df[(df["ANIO"] == 2023) & (df["MES"] == 12)]

# Columnas numéricas
for col in ["A_RESIDENCIAL_E", "A_NO_RESIDENCIAL_E", "A_TOTAL_E"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# Tecnologías de interés (igual que en el Anuario)
TECNOS_INTERES = ["Cable", "Direct-to-home (DTH)", "IPTV Terrestre"]

# Agrupar por tecnología
grp = df.groupby("TECNO_ACCESO_TV")[["A_RESIDENCIAL_E", "A_NO_RESIDENCIAL_E"]].sum()
print("\n--- Todas las tecnologías en dic 2023 ---")
print(grp)

# Totales por segmento
total_res   = grp["A_RESIDENCIAL_E"].sum()
total_nores = grp["A_NO_RESIDENCIAL_E"].sum()
print(f"\nTotal residencial   : {total_res:,.0f}  (Anuario: 22,506,526)")
print(f"Total no residencial: {total_nores:,.0f}  (Anuario: 455,305)")

# Filtrar solo las tecnologías que aparecen en la figura
# (ajusta los nombres si el CSV usa variantes distintas)
mask_res   = grp.index.isin(TECNOS_INTERES)
otros_res  = grp.loc[~mask_res, "A_RESIDENCIAL_E"].sum()
otros_nores = grp.loc[~mask_res, "A_NO_RESIDENCIAL_E"].sum()

# Porcentajes residencial
pct_res = {}
for t in TECNOS_INTERES:
    val = grp.loc[t, "A_RESIDENCIAL_E"] if t in grp.index else 0
    pct_res[t] = val / total_res * 100

# Porcentajes no residencial
pct_nores = {}
for t in TECNOS_INTERES:
    val = grp.loc[t, "A_NO_RESIDENCIAL_E"] if t in grp.index else 0
    pct_nores[t] = val / total_nores * 100

print("\n--- Porcentajes residencial ---")
for k, v in pct_res.items():
    print(f"  {k}: {v:.1f}%")

print("\n--- Porcentajes no residencial ---")
for k, v in pct_nores.items():
    print(f"  {k}: {v:.1f}%")

# Paleta (igual al Anuario)
# Residencial: azul oscuro Cable, azul medio DTH, azul claro IPTV
# No residencial: salmón/rojo Cable, azul oscuro DTH, azul medio IPTV
COLORS_RES   = {"Cable": "#1a3a5c", "Direct-to-home (DTH)": "#4a7fa5", "IPTV Terrestre": "#a8d0e6"}
COLORS_NORES = {"Cable": "#c0392b", "Direct-to-home (DTH)": "#1a3a5c",  "IPTV Terrestre": "#4a7fa5"}

def make_pie(ax, pct_dict, colors, total_label, total_val, seg_label):
    labels = list(pct_dict.keys())
    sizes  = [pct_dict[l] for l in labels]
    clrs   = [colors[l] for l in labels]

    wedges, texts = ax.pie(
        sizes, colors=clrs,
        startangle=90,
        wedgeprops=dict(width=0.85, edgecolor="white", linewidth=1.5)
    )
    ax.set_title(seg_label, fontsize=13, fontweight="bold", pad=14)

    # Etiquetas dentro/fuera
    for i, (wedge, label, pct) in enumerate(zip(wedges, labels, sizes)):
        ang   = (wedge.theta2 + wedge.theta1) / 2
        x     = 0.65 * plt.matplotlib.patches.Wedge(
                    (0,0), 1, wedge.theta1, wedge.theta2).center[0]
        # usar annotate para posicionar bien
        ax.annotate(
            f"{label}\n{pct:.1f}%",
            xy=(plt.np.cos(plt.np.radians(ang)) * 0.55,
                plt.np.sin(plt.np.radians(ang)) * 0.55),
            ha="center", va="center",
            fontsize=9, fontweight="bold", color="white"
        )

    # Badge de total
    ax.text(0, -1.45,
            f"Accesos {'residenciales' if 'Res' in seg_label else 'no residenciales'}\na nivel nacional:\n{total_val:,}",
            ha="center", va="center", fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#cccccc", lw=1))

# Figura
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
fig.patch.set_facecolor("#f5f5f5")

make_pie(ax1, pct_res,   COLORS_RES,   "Residencial",    int(total_res),   "Residencial")
make_pie(ax2, pct_nores, COLORS_NORES, "No Residencial", int(total_nores), "No Residencial")

fig.suptitle("Figura B.23. Tecnologías de conexión del Servicio de Televisión\nRestringida por segmento",
             fontsize=13, fontweight="bold", y=1.01)

note = ("Fuente: IFT con datos de los operadores de telecomunicaciones a diciembre de 2023.\n"
        "Nota: La suma de los porcentajes no suma 100% por cuestiones de redondeo.")
fig.text(0.5, -0.04, note, ha="center", fontsize=7.5, color="#555555")

plt.tight_layout()
# Guardar salida
plt.savefig(OUTPUT, dpi=150, bbox_inches="tight")
print(f"\nGuardado en {OUTPUT}")
plt.show()
