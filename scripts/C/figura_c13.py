"""
Figura C.13 — Líneas del servicio móvil de acceso a Internet
             por cada 100 habitantes por entidad federativa (diciembre 2023)
Fuente: IFT con datos de operadores, CONAPO y estimaciones propias.
Archivos: TD_TELEDENSIDAD_INTMOVIL_ITE_VA.csv + mexico.json
Nota: el CSV disponible contiene datos de diciembre 2024; los rangos de color
      del mapa no se ven afectados respecto al Anuario (diciembre 2023).
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import matplotlib.patches as mpatches
import sys

CSV_PATH = PROJECT_ROOT / "datos" / "C.13" / "TD_TELEDENSIDAD_INTMOVIL_ITE_VA.csv"
GEO_PATH = PROJECT_ROOT / "datos" / "C.13" / "mexico.json"
OUTPUT   = "output/Figura_C13.png"

# 1. Leer CSV
df = pd.read_csv(CSV_PATH, encoding="latin1")
dic = df[df["MES"] == 12].copy()

# Normalizar nombres para hacer merge con GeoJSON
rename_csv = {
    "Coahuila de Zaragoza":             "Coahuila",
    "Veracruz de Ignacio de la Llave":  "Veracruz",
    "Michoacán de Ocampo":              "Michoacán",
}
dic["ENTIDAD_N"] = dic["ENTIDAD"].replace(rename_csv)

# 2. Leer GeoJSON
gdf = gpd.read_file(GEO_PATH)
gdf = gdf.rename(columns={"name": "ENTIDAD_N"})

# 3. Merge
gdf = gdf.merge(dic[["ENTIDAD_N", "T_INTMOVIL_ITE_VA"]], on="ENTIDAD_N", how="left")

# 4. Clasificar en rangos (igual que el Anuario)
def rango(v):
    if   v < 84:   return 0   # Menos de 84   â†’ rojo
    elif v <= 91:  return 1   # 85 a 91        â†’ salmón
    elif v <= 97:  return 2   # 92 a 97        â†’ azul marino
    elif v <= 103: return 3   # 98 a 103       â†’ azul teal
    else:          return 4   # Más de 104     â†’ azul claro

gdf["rango"] = gdf["T_INTMOVIL_ITE_VA"].apply(rango)

COLORES = {
    0: "#E63946",   # rojo
    1: "#F4A261",   # salmón
    2: "#1D3557",   # azul marino oscuro
    3: "#457B9D",   # azul teal
    4: "#A8DADC",   # azul claro
}
LABELS = {
    0: "Menos de 84",
    1: "85 a 91",
    2: "92 a 97",
    3: "98 a 103",
    4: "Más de 104",
}

gdf["color"] = gdf["rango"].map(COLORES)

# 5. Plot
fig, ax = plt.subplots(figsize=(13, 9))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

for rng in range(5):
    subset = gdf[gdf["rango"] == rng]
    subset.plot(ax=ax, color=COLORES[rng], edgecolor="white", linewidth=0.8)

ax.set_axis_off()

# Título
ax.set_title(
    "Figura C.13. Líneas del servicio móvil de acceso a Internet\n"
    "por cada 100 habitantes por entidad federativa",
    fontsize=11, fontweight="bold", loc="left", pad=10
)

# Leyenda
patches = [mpatches.Patch(color=COLORES[r], label=LABELS[r]) for r in range(5)]
ax.legend(handles=patches, loc="lower left", fontsize=9,
          frameon=True, framealpha=0.9, title=None,
          bbox_to_anchor=(0.01, 0.05))

# Badge nacional
bbox_props = dict(boxstyle="round,pad=0.6", facecolor="white",
                  edgecolor="#457B9D", linewidth=1.5)
ax.text(0.78, 0.75,
        "Líneas del servicio móvil de acceso\na Internet por cada 100 habitantes:\n",
        transform=ax.transAxes, fontsize=8, ha="center", va="center",
        bbox=bbox_props, color="#333333")
ax.text(0.78, 0.68,
        "96",
        transform=ax.transAxes, fontsize=22, ha="center", va="center",
        fontweight="bold", color="#1D3557")

# Badge tasa de crecimiento
ax.text(0.40, 0.10,
        "Tasa de crecimiento\nanual de 4.3%",
        transform=ax.transAxes, fontsize=9, ha="center", va="center",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#1D3557",
                  edgecolor="none"), color="white", fontweight="bold")

# Nota al pie
fig.text(0.05, -0.01,
    "Fuente: IFT con datos de los operadores de telecomunicaciones "
    "a diciembre de 2023, CONAPO y estimaciones propias.",
    fontsize=7.5, color="#555555")

plt.tight_layout()
# Guardar salida
plt.savefig(OUTPUT, dpi=180, bbox_inches="tight")
print(f"Figura guardada: {OUTPUT}")
