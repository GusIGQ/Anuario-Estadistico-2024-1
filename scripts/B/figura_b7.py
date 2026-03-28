"""
Figura B.7 â€” LÃ­neas del Servicio Fijo de TelefonÃ­a No Residencial
por cada 100 unidades econÃ³micas por entidad federativa.

Fuente datos: TD_PENETRACIONES_TELFIJA_ITE_VA.csv (BIT IFT)
Nota: Datos disponibles corresponden a dic 2024 (proxy de dic 2023).
      Para CDMX y Nuevo LeÃ³n la diferencia es mayor (~174 y ~181 unidades),
      pero los rangos de color no se ven afectados.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
import matplotlib.patches as mpatches
import os

# 1. DATOS
df = pd.read_csv('datos/B.6/TD_PENETRACIONES_TELFIJA_ITE_VA.csv', encoding='latin1')
data = dict(zip(df['ENTIDAD'], df['P_NRES_H_TELFIJA_E']))

# 2. RANGOS Y COLORES (Anuario B.7)
COLORS = ['#c5e8f7', '#5bafd6', '#2e6fa3', '#f4a58a', '#c0392b']
LABELS = ['Menos de 38', '39 a 60', '61 a 97', '98 a 114', 'MÃ¡s de 114']
BREAKS = [0, 38, 61, 98, 115, 9999]

def get_color(val):
    for i in range(len(BREAKS)-1):
        if BREAKS[i] <= val < BREAKS[i+1]:
            return COLORS[i]
    return COLORS[-1]

# 3. MAPA DE M XICO (GeoJSON)
import urllib.request
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
GEOJSON_PATH = os.path.join(BASE_DIR, 'datos', 'mexico.json')
if not os.path.exists(GEOJSON_PATH):
    print("Descargando mapa de MÃ©xico...")
    urllib.request.urlretrieve('https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json', GEOJSON_PATH)

with open(GEOJSON_PATH, 'r', encoding='utf-8') as f:
    mexico_geojson = json.load(f)

# Mapeo de nombres del GeoJSON a los datos
NAME_MAPPING = {
    'Veracruz': 'Veracruz de Ignacio de la Llave',
    'MichoacÃ¡n': 'MichoacÃ¡n de Ocampo',
    'Coahuila': 'Coahuila de Zaragoza',
}

# 4. GRAFICAR
fig, ax = plt.subplots(figsize=(14, 9))
ax.set_facecolor('#f8f9fa')
fig.patch.set_facecolor('#f8f9fa')

for feature in mexico_geojson['features']:
    geo_name = feature['properties']['name']
    data_name = NAME_MAPPING.get(geo_name, geo_name)
    color = get_color(data.get(data_name, 0))

    geom_type = feature['geometry']['type']
    coords = feature['geometry']['coordinates']

    # Polygon puede tener varios anillos, pero tomaremos el borde exterior (índice 0)
    def draw_polygon(polygon_coords):
        poly_points = polygon_coords[0]
        poly = plt.Polygon(poly_points, closed=True,
                           facecolor=color, edgecolor='white',
                           linewidth=0.6, alpha=0.93)
        ax.add_patch(poly)

    if geom_type == 'Polygon':
        draw_polygon(coords)
    elif geom_type == 'MultiPolygon':
        for poly_coords in coords:
            draw_polygon(poly_coords)

ax.set_xlim(-118.5, -86.0)
ax.set_ylim(14.0, 33.5)
ax.set_aspect(1.1)  # Ajuste de proyecciÃ³n Mercator aproximada
ax.axis('off')

# 5. LEYENDA
patches = [mpatches.Patch(facecolor=COLORS[i], edgecolor='none',
                           label=LABELS[i]) for i in range(5)]
legend = ax.legend(
    handles=patches,
    title='LÃ­neas del servicio fijo de TelefonÃ­a\nNo Residencial por cada 100\nunidades econÃ³micas:',
    loc='lower left',
    bbox_to_anchor=(0.01, 0.03),
    fontsize=10,
    title_fontsize=11,
    facecolor='#ffffff',
    labelcolor='#2c3e50',
    edgecolor='none',
    framealpha=0.9,
)
legend.get_title().set_color('#2c3e50')

# 6. BADGE NACIONAL
ax.text(0.80, 0.72, '128', transform=ax.transAxes,
        fontsize=42, fontweight='bold', color='#2c3e50', ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffffff',
                  edgecolor='#dddddd', linewidth=1.5))
ax.text(0.80, 0.62, 'Tasa de crecimiento\nanual de 13.3%',
        transform=ax.transAxes, fontsize=11, color='#2c3e50',
        ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffffff',
                  edgecolor='#dddddd', linewidth=1.5))

# 7. TÍTULO Y PIE
ax.set_title(
    'Figura B.7.  LÃ­neas del Servicio Fijo de TelefonÃ­a No Residencial\n'
    'por cada 100 unidades econÃ³micas por entidad federativa',
    color='#2c3e50', fontsize=14, fontweight='bold', pad=12)

fig.text(
    0.01, 0.005,
    'Fuente: IFT con datos de los operadores de telecomunicaciones a diciembre de 2023 '
    'y del DENUE del INEGI, a noviembre de 2023.\n'
    'Nota: valores graficados son proxy de dic 2024 (diferencia variable por estado respecto a dic 2023).',
    color='#666666', fontsize=8, va='bottom')

plt.tight_layout()
os.makedirs('output', exist_ok=True)
# Guardar salida
plt.savefig('output/Figura_B7.png', dpi=150, bbox_inches='tight',
            facecolor=fig.get_facecolor())
print("âœ“ Figura guardada en output/Figura_B7.png")
