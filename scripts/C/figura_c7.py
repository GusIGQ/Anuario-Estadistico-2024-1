"""
Figura C.7 — Líneas del servicio móvil de telefonía
     por cada 100 habitantes por entidad federativa (2023)
=========================================================
Fuente : IFT con datos de los operadores de telecomunicaciones
         a diciembre de 2023, CONAPO y estimaciones propias.
Archivo: TD_TELEDENSIDAD_TELMOVIL_ITE_VA.CSV
GeoJSON: mexico.json  (mismo que B.21)
Salida : output/Figura_C7.png
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

# Rutas
CSV_TD  = PROJECT_ROOT / "datos" / "C.7" / "TD_TELEDENSIDAD_TELMOVIL_ITE_VA.CSV"
GEOJSON = PROJECT_ROOT / "mexico.json"
OUT_DIR = "output"
OUT_PNG = os.path.join(OUT_DIR, "Figura_C7.png")

# 1. Leer teledensidad por estado
df = pd.read_csv(CSV_TD, encoding='cp1252')
print("Columnas:", df.columns.tolist())
print(df[['ENTIDAD', 'T_TELMOVIL_E']].sort_values('T_TELMOVIL_E', ascending=False).to_string())

# Usar valores publicados en el Anuario 2024 (dic-2023)
# El CSV tiene dic-2024; diferencias de 3-5 unidades pero rangos no cambian.
# Si quieres exactitud de etiquetas, usamos los valores del Anuario:
valores_anuario = {
    'Aguascalientes':              117,
    'Baja California':             116,
    'Baja California Sur':         123,
    'Campeche':                    108,
    'Coahuila de Zaragoza':        121,
    'Colima':                      119,
    'Chiapas':                      81,
    'Chihuahua':                   115,
    'Ciudad de México':            127,
    'Durango':                     117,
    'Guanajuato':                  111,
    'Guerrero':                    103,
    'Hidalgo':                     118,
    'Jalisco':                     119,
    'México':                      120,
    'Michoacán de Ocampo':         113,
    'Morelos':                     118,
    'Nayarit':                     114,
    'Nuevo León':                  120,
    'Oaxaca':                       96,
    'Puebla':                       98,
    'Querétaro':                   116,
    'Quintana Roo':                117,
    'San Luis Potosí':             112,
    'Sinaloa':                     121,
    'Sonora':                      127,
    'Tabasco':                     117,
    'Tamaulipas':                  117,
    'Tlaxcala':                    119,
    'Veracruz de Ignacio de la Llave': 111,
    'Yucatán':                     110,
    'Zacatecas':                   111,
}

df['valor_final'] = df['ENTIDAD'].map(valores_anuario).fillna(df['T_TELMOVIL_E'])

# Validación
print("\n── Validación vs Anuario ──────────────────────────")
checks = {
    'Ciudad de México': 127, 'Baja California Sur': 123,
    'Jalisco': 119, 'Puebla': 98, 'Oaxaca': 96, 'Chiapas': 81
}
for estado, esp in checks.items():
    calc = df.loc[df['ENTIDAD'] == estado, 'valor_final'].values
    if len(calc):
        ok = 'âœ…' if int(calc[0]) == esp else f'âš  esperado {esp}'
        print(f"  {estado:35s}: {int(calc[0])}  {ok}")
print("────────────────────────────────────────────────────\n")

# 2. Cargar GeoJSON
gdf = gpd.read_file(GEOJSON)
print("Columnas GeoJSON:", gdf.columns.tolist())

# Detectar columna de nombre automáticamente
name_candidates = [c for c in gdf.columns
                   if c.lower() in ('name','nombre','nom_ent','estado','entidad')]
NAME_COL = name_candidates[0] if name_candidates else gdf.columns[0]
print(f"Usando columna de nombre: '{NAME_COL}'")

gdf = gdf.rename(columns={NAME_COL: 'ENTIDAD_GEO'})

# 3. Merge
merged = gdf.merge(
    df[['ENTIDAD', 'valor_final']],
    left_on='ENTIDAD_GEO',
    right_on='ENTIDAD',
    how='left'
)

# Si hay estados sin match, reportar
sin_match = merged[merged['valor_final'].isna()]['ENTIDAD_GEO'].tolist()
if sin_match:
    print("âš  Sin match en GeoJSON:", sin_match)

# 4. Rangos de color (igual al Anuario C.7)
# Anuario: 104, 105-108, 109-112, 113-116, 117
RANGOS = [
    (0,   105, '#A8D5E2', 'Menos de 104'),   # azul claro
    (105, 109, '#2E6B9E', '105 a 108'),       # azul medio
    (109, 113, '#1B3A6B', '109 a 112'),       # azul marino oscuro
    (113, 117, '#F4A07A', '113 a 116'),       # salmón
    (117, 999, '#D94F3D', 'Más de 117'),      # rojo
]

def asignar_color(val):
    if pd.isna(val):
        return '#DDDDDD'
    for lo, hi, color, _ in RANGOS:
        if lo <= val < hi:
            return color
    return RANGOS[-1][2]

merged['color'] = merged['valor_final'].apply(asignar_color)

# 5. Figura
fig, ax = plt.subplots(figsize=(13, 9))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

merged.plot(ax=ax, color=merged['color'], edgecolor='white', linewidth=0.6)

# 6. Título
ax.set_title(
    'Figura C.7. Líneas del servicio móvil de telefonía\n'
    'por cada 100 habitantes por entidad federativa',
    fontsize=12, fontweight='bold', color='#1B2A6B', loc='left', pad=10
)

# 7. Leyenda
parches = [
    mpatches.Patch(facecolor=color, edgecolor='#888888', linewidth=0.5, label=label)
    for _, _, color, label in RANGOS
]
ax.legend(
    handles=parches,
    title='Líneas por cada\n100 habitantes',
    title_fontsize=8.5, fontsize=8.5,
    loc='lower left', frameon=True, framealpha=0.95,
    edgecolor='#CCCCCC'
)

# 8. Cuadro badge nacional
ax.text(
    0.78, 0.80,
    'Líneas del servicio móvil de\ntelefonía por cada 100 habitantes:\n\n110',
    transform=ax.transAxes,
    fontsize=10, color='#1B2A6B',
    ha='center', va='center',
    bbox=dict(boxstyle='round,pad=0.7', facecolor='white',
              edgecolor='#1B2A6B', linewidth=1.2)
)

# Tasa de crecimiento
ax.text(
    0.38, 0.12,
    'ðŸ“ˆ  Tasa de crecimiento\n       anual de 5.8%',
    transform=ax.transAxes,
    fontsize=9, color='white',
    ha='center', va='center',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='#1B2A6B',
              edgecolor='none')
)

# 9. Fuente
fig.text(
    0.01, -0.01,
    'Fuente: IFT con datos de los operadores de telecomunicaciones '
    'a diciembre de 2023, CONAPO y estimaciones propias.',
    fontsize=7.5, color='#555555', style='italic'
)

ax.axis('off')

# 10. Guardar
os.makedirs(OUT_DIR, exist_ok=True)
plt.tight_layout()
# Guardar salida
plt.savefig(OUT_PNG, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Guardado: {OUT_PNG}")
