"""
Figura B.6 â€” LÃ­neas del Servicio Fijo de TelefonÃ­a Residencial
por cada 100 hogares por entidad federativa.

Fuente datos: TD_PENETRACIONES_TELFIJA_ITE_VA.csv (BIT IFT)
Nota: Datos disponibles corresponden a dic 2024 (proxy de dic 2023, diferencia â‰¤2 unidades).
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
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection
import numpy as np
import os

# 1. RUTAS Y LECTURA DE DATOS
BASE_DIR = PROJECT_ROOT
DATA_PATH = os.path.join(BASE_DIR, 'datos', 'B.6', 'TD_PENETRACIONES_TELFIJA_ITE_VA.csv')
OUTPUT_DIR = os.path.join(BASE_DIR, 'figuras', 'B6')
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'Figura_B6.png')

# Crear directorio de salida si no existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Cargar datos
df = pd.read_csv(DATA_PATH, encoding='latin1')
df = df[df['ANIO'] == df['ANIO'].max()].copy()
data = dict(zip(df['ENTIDAD'], df['P_RES_H_TELFIJA_E']))

# 2. RANGOS Y COLORES
COLORS  = ['#c5e8f7', '#5bafd6', '#2e6fa3', '#f4a58a', '#c0392b']
LABELS  = ['Menos de 29', '29 a 42', '43 a 55', '56 a 68', 'MÃ¡s de 68']
BREAKS  = [0, 29, 43, 56, 69, 999]

def get_color(val):
    for i in range(len(BREAKS)-1):
        if BREAKS[i] <= val < BREAKS[i+1]:
            return COLORS[i]
    return COLORS[-1]

# 3. MAPA DE M XICO (GeoJSON)
import urllib.request
import json

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
    title='LÃ­neas del servicio fijo de TelefonÃ­a\nResidencial por cada 100 hogares:',
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

# Badge con el promedio nacional (si existe en los datos, de lo contrario se usa el 53 original)
nacional_val = data.get('Nacional', 53)
ax.text(0.80, 0.72, f'{int(nacional_val)}', transform=ax.transAxes,
        fontsize=44, fontweight='bold', color='#2c3e50', ha='center',
        va='center',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffffff',
                  edgecolor='#dddddd', linewidth=1.5))
ax.text(0.80, 0.62, 'Tasa de crecimiento\nanual de 1.9%',
        transform=ax.transAxes, fontsize=11, color='#2c3e50',
        ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffffff',
                  edgecolor='#dddddd', linewidth=1.5))

# Título
ax.set_title(
    'Figura B.6.  LÃ­neas del Servicio Fijo de TelefonÃ­a Residencial\n'
    'por cada 100 hogares por entidad federativa',
    color='#2c3e50', fontsize=14, fontweight='bold', pad=12)

# Pie de figura
fig.text(
    0.01, 0.005,
    'Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones '
    'a diciembre de 2023 y de la ENDUTIH 2023 del INEGI.\n'
    'Nota: valores graficados son proxy de dic 2024 (diferencia â‰¤2 unidades respecto a dic 2023).',
    color='#666666', fontsize=8, va='bottom')

plt.tight_layout()
# Guardar salida
plt.savefig(OUTPUT_PATH, dpi=150, bbox_inches='tight',
            facecolor=fig.get_facecolor())
print(f"âœ“ Figura guardada en {OUTPUT_PATH}")
