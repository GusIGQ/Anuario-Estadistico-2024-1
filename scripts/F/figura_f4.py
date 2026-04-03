import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import matplotlib.ticker as mtick
import numpy as np

print("Iniciando el procesamiento de datos...")

# FASE 1: EXTRACCI N Y LIMPIEZA DE DATOS

archivo_excel = PROJECT_ROOT / "datos" / "F.4" / "mociba2023_tabulados.xlsx"

# 1. Cargar las hojas correspondientes (1.17 Hombres, 1.18 Mujeres)
# Saltamos las primeras 14 filas porque son los títulos y metadatos del INEGI
df_1_17 = pd.read_excel(archivo_excel, sheet_name='1.17', skiprows=14)
df_1_18 = pd.read_excel(archivo_excel, sheet_name='1.18', skiprows=14)

# 2. Extraer columnas clave: Entidad (índice 0) y Absolutos de Sí vivió ciberacoso (índice 3)
hombres = df_1_17.iloc[:1000, [0, 3]].dropna().copy()
mujeres = df_1_18.iloc[:1000, [0, 3]].dropna().copy()

hombres.columns = ['Entidad', 'Hombres_Ciberacoso']
mujeres.columns = ['Entidad', 'Mujeres_Ciberacoso']

# 3. Limpieza de texto y conversión a números
hombres['Entidad'] = hombres['Entidad'].astype(str).str.strip()
mujeres['Entidad'] = mujeres['Entidad'].astype(str).str.strip()

# Si los números vienen con comas (como texto), las quitamos y pasamos a numérico
hombres['Hombres_Ciberacoso'] = pd.to_numeric(hombres['Hombres_Ciberacoso'].astype(str).str.replace(',', ''), errors='coerce')
mujeres['Mujeres_Ciberacoso'] = pd.to_numeric(mujeres['Mujeres_Ciberacoso'].astype(str).str.replace(',', ''), errors='coerce')

# 4. Extraer el Total Nacional (necesario para la fórmula)
total_hombres = hombres[hombres['Entidad'] == 'Estados Unidos Mexicanos']['Hombres_Ciberacoso'].values[0]
total_mujeres = mujeres[mujeres['Entidad'] == 'Estados Unidos Mexicanos']['Mujeres_Ciberacoso'].values[0]

# 5. Filtrar la basura (Grupos de edad, notas al pie, etc.) para dejar solo los 32 estados
patron_filtro = '^(De |Estados Unidos Mexicanos|Entidad|Absolutos|Estimaciones)'
hombres_estados = hombres[~hombres['Entidad'].str.match(patron_filtro, case=False)].drop_duplicates(subset=['Entidad'])
mujeres_estados = mujeres[~mujeres['Entidad'].str.match(patron_filtro, case=False)].drop_duplicates(subset=['Entidad'])

# 6. Unir datos y calcular porcentajes exactos
df_final = pd.merge(hombres_estados, mujeres_estados, on='Entidad', how='inner').head(32)
df_final['Hombres (%)'] = (df_final['Hombres_Ciberacoso'] / total_hombres * 100).round(1)
df_final['Mujeres (%)'] = (df_final['Mujeres_Ciberacoso'] / total_mujeres * 100).round(1)

# Ordenar alfabéticamente para igualar el PDF original
df_final = df_final.sort_values('Entidad').reset_index(drop=True)

print("Datos calculados con éxito. Generando Gráfica...")

# FASE 2: DIBUJO Y DISE O DE LA GRÁFICA

# 1. Configuración de colores (Extraídos de la gráfica del IFT)
color_hombres = '#2C7B95'
color_mujeres = '#F19A8A'

# 2. Lienzo y dimensiones
fig, ax = plt.subplots(figsize=(18, 7), facecolor='white')
x = np.arange(len(df_final['Entidad']))
width = 0.35  

# 3. Dibujar las barras
rects1 = ax.bar(x - width/2, df_final['Hombres (%)'], width, label='Hombres', color=color_hombres)
rects2 = ax.bar(x + width/2, df_final['Mujeres (%)'], width, label='Mujeres', color=color_mujeres)

# 4. Función para poner el % chiquito sobre cada barra
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=6)

autolabel(rects1)
autolabel(rects2)

# 5. Formato del Eje Y (0 a 16%, en pasos de 2%)
ax.set_ylim(0, 16.5)
ax.set_yticks(np.arange(0, 17, 2))
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))

# 6. Formato del Eje X (Nombres de estados rotados)
ax.set_xticks(x)
ax.set_xticklabels(df_final['Entidad'], rotation=90, fontsize=9)

# 7. Estilo minimalista (Quitar bordes innecesarios y poner líneas guía)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#DDDDDD')
ax.spines['bottom'].set_color('#DDDDDD')
ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=0.15)
ax.set_axisbelow(True) 

# 8. Leyenda superior
ax.legend(loc='upper left', bbox_to_anchor=(0.15, 0.95), frameon=False, ncol=2, fontsize=10)

# 9. Guardar y mostrar
fig.suptitle('Figura F.4. Ingreso promedio de trabajadores en telecomunicaciones y radiodifusión', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
nombre_salida = PROJECT_ROOT / "output" / "Figura_F4.png"
# Guardar salida
plt.savefig(nombre_salida, dpi=300, bbox_inches='tight')

print(f"¡Terminado! Gráfica guardada exitosamente como '{nombre_salida}' en tu carpeta actual.")
