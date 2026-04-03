"""
Figura B.21 — Accesos del Servicio de Televisión Restringida Residencial
         por cada 100 hogares por entidad federativa (2023)
=========================================================================
Fuentes:
  - IFT con datos de operadores de telecomunicaciones a diciembre de 2023
    Archivo: TD_ACC_TVRES_ITE_VA.csv  (BIT: Servicio de TV Restringida)
  - ENDUTIH 2023, INEGI
    Archivo: tic_2023_hogares.DBF     (microdatos ENDUTIH 2023)

Geometría de estados requerida (descargar una sola vez):
  URL: https://raw.githubusercontent.com/angelmtz4/mexico-geojson/master/states.geojson
  Guardar como: datos/B.21/mexico_states.geojson

Salida: output/Figura_B21.png

Metodología
-----------
1. Filtrar TD_ACC_TVRES_ITE_VA.csv â†’ ANIO==2023, MES==12
2. Agrupar por ENTIDAD â†’ sumar A_RESIDENCIAL_E
3. Desde ENDUTIH: agrupar por ENT â†’ sumar FAC_HOG â†’ mapear a nombre de estado
4. Merge por nombre de estado â†’ penetración = accesos / hogares * 100
5. Unir con GeoJSON â†’ mapa coroplético con 5 rangos de color

Validación (valores exactos del Anuario IFT 2024)
--------------------------------------------------
Querétaro : 94   Sonora : 80   Sinaloa : 76
Yucatán   : 42   Oaxaca : 38   Chiapas : 35
Nacional  : 58
"""

import os
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
from dbfread import DBF

# Rutas
CSV_ACC   = PROJECT_ROOT / "datos" / "b.21" / "TD_ACC_TVRES_ITE_VA.csv"
DBF_HOG   = PROJECT_ROOT / "datos" / "b.21" / "tic_2023_hogares.DBF"
GEOJSON   = PROJECT_ROOT / "mexico.json"
OUT_DIR   = "output"
OUT_FILE  = os.path.join(OUT_DIR, "Figura_B21.png")

# Mapeo clave INEGI (ENT) - nombre de estado
ENT_MAP = {
    1: 'Aguascalientes',           2: 'Baja California',
    3: 'Baja California Sur',      4: 'Campeche',
    5: 'Coahuila de Zaragoza',     6: 'Colima',
    7: 'Chiapas',                  8: 'Chihuahua',
    9: 'Ciudad de México',        10: 'Durango',
    11: 'Guanajuato',             12: 'Guerrero',
    13: 'Hidalgo',                14: 'Jalisco',
    15: 'México',                 16: 'Michoacán de Ocampo',
    17: 'Morelos',                18: 'Nayarit',
    19: 'Nuevo León',             20: 'Oaxaca',
    21: 'Puebla',                 22: 'Querétaro',
    23: 'Quintana Roo',           24: 'San Luis Potosí',
    25: 'Sinaloa',                26: 'Sonora',
    27: 'Tabasco',                28: 'Tamaulipas',
    29: 'Tlaxcala',               30: 'Veracruz de Ignacio de la Llave',
    31: 'Yucatán',                32: 'Zacatecas'
}

# 1. Accesos residenciales por entidad (BIT)
print("Leyendo accesos BIT...")
# Cargar datos
df_acc = pd.read_csv(CSV_ACC, encoding='latin1')
df_dic = df_acc[(df_acc['ANIO'] == 2023) & (df_acc['MES'] == 12)]
por_entidad = (df_dic.groupby('ENTIDAD')['A_RESIDENCIAL_E']
               .sum().reset_index())
por_entidad.columns = ['ENTIDAD', 'accesos']
por_entidad = por_entidad[por_entidad['ENTIDAD'] != 'Sin información de Entidad']

# 2. Hogares por entidad (ENDUTIH 2023)
print("Leyendo ENDUTIH...")
tabla = DBF(DBF_HOG, encoding='latin1')
df_hog = pd.DataFrame(iter(tabla))
df_hog['ENT'] = df_hog['ENT'].astype(int)
df_hog['ENTIDAD'] = df_hog['ENT'].map(ENT_MAP)
df_hog['FAC_HOG'] = pd.to_numeric(df_hog['FAC_HOG'], errors='coerce')
hogares = df_hog.groupby('ENTIDAD')['FAC_HOG'].sum().reset_index()
hogares.columns = ['ENTIDAD', 'hogares']

# 3. Penetración por estado
merged = por_entidad.merge(hogares, on='ENTIDAD', how='inner')
merged['penetracion'] = (merged['accesos'] / merged['hogares'] * 100).round(0).astype(int)

# Validación en consola
print("\n── Validación ──────────────────────────────────")
for estado, esperado in [('Querétaro', 94), ('Sonora', 80), ('Sinaloa', 76),
                          ('Yucatán', 42), ('Oaxaca', 38), ('Chiapas', 35)]:
    calc = merged.loc[merged['ENTIDAD'] == estado, 'penetracion'].values[0]
    ok = 'âœ…' if calc == esperado else f'âš  esperado {esperado}'
    print(f"  {estado:30s}: {calc:3d}  {ok}")
nac = round(merged['accesos'].sum() / merged['hogares'].sum() * 100, 1)
print(f"  {'Nacional':30s}: {nac}  (Anuario: 58)")
print("────────────────────────────────────────────────\n")

# 4. Cargar GeoJSON y hacer merge
print("Cargando geometría...")
gdf = gpd.read_file(GEOJSON)

# Inspeccionar columna de nombre en el GeoJSON
# (puede ser name , NAME , estado , NOM_ENT , etc.)
print("Columnas GeoJSON:", gdf.columns.tolist())
# Ajusta name si la columna tiene otro nombre en tu GeoJSON
NAME_COL = 'name'  # â† cambiar si es necesario

# Normalizar nombres para el merge (quitar acentos problemáticos si los hay)
gdf = gdf.rename(columns={NAME_COL: 'ENTIDAD_GEO'})
merged_geo = gdf.merge(merged, left_on='ENTIDAD_GEO', right_on='ENTIDAD', how='left')

# 5. Clasificar en rangos de color
# Rangos del Anuario: 55, 56-65, 66-75, 76-85, 85
RANGOS = [
    (0,  55, '#A8D5E2', 'Menos de 55'),   # azul claro
    (55, 65, '#2E6B9E', '56-65'),          # azul medio
    (65, 75, '#1B3A6B', '66-75'),          # azul marino oscuro
    (75, 85, '#F4A07A', '76-85'),          # salmón
    (85, 200,'#D94F3D', 'Más de 85'),      # rojo
]

def asignar_color(val):
    if pd.isna(val):
        return '#DDDDDD'
    for lo, hi, color, _ in RANGOS:
        if lo <= val < hi:
            return color
    return RANGOS[-1][2]

merged_geo['color'] = merged_geo['penetracion'].apply(asignar_color)

# 6. Graficar
fig, ax = plt.subplots(figsize=(14, 9))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

merged_geo.plot(ax=ax, color=merged_geo['color'], edgecolor='white',
                linewidth=0.6)

# Título
ax.set_title(
    'Figura B.21. Accesos del Servicio de Televisión Restringida\n'
    'Residencial por cada 100 hogares por entidad federativa',
    fontsize=12, fontweight='bold', color='#1B2A6B', loc='left', pad=10
)

# Leyenda
parches = [mpatches.Patch(facecolor=color, edgecolor='white', label=label)
           for _, _, color, label in RANGOS]
ax.legend(handles=parches, title='Accesos por cada\n100 hogares',
          title_fontsize=8.5, fontsize=8.5,
          loc='lower left', frameon=True, framealpha=0.9,
          edgecolor='#CCCCCC')

# Cuadro nacional
ax.text(0.78, 0.82,
        'Accesos del servicio de televisión\nrestringida residencial\npor cada 100 hogares:\n\n58',
        transform=ax.transAxes,
        fontsize=10, color='#1B2A6B',
        ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='white',
                  edgecolor='#1B2A6B', linewidth=1.2))

# Nota al pie
fig.text(0.01, -0.01,
         'Fuente: IFT con datos de los operadores de telecomunicaciones '
         'a diciembre de 2023 y de la ENDUTIH 2023 del INEGI.',
         fontsize=7.5, color='#555555', style='italic')

ax.axis('off')

# Guardar
os.makedirs(OUT_DIR, exist_ok=True)
plt.tight_layout()
# Guardar salida
plt.savefig(OUT_FILE, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Figura guardada en: {OUT_FILE}")
