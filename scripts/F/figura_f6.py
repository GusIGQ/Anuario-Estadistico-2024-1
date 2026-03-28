import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import numpy as np
import re
import textwrap

# 1. RUTA AL ARCHIVO EXCEL (Ajusta la carpeta si es necesario)
ruta_archivo = PROJECT_ROOT / "datos" / "F.6" / "mociba2023_tabulados.xlsx" 

# 2. LEER LA TABLA
df = pd.read_excel(ruta_archivo, sheet_name='1.25')

# Buscar automáticamente las filas donde dicen Hombres y Mujeres
col0_limpia = df.iloc[:, 0].fillna('').astype(str).str.strip()
idx_hombres = col0_limpia[col0_limpia == 'Hombres'].index[0]
idx_mujeres = col0_limpia[col0_limpia == 'Mujeres'].index[0]

# Extraer el total de población víctima por sexo (Columna 1)
total_hombres = float(df.iloc[idx_hombres, 1])
total_mujeres = float(df.iloc[idx_mujeres, 1])

# Extraer los 13 valores absolutos (Columna 1)
absolutos_hombres = df.iloc[idx_hombres+1 : idx_hombres+14, 1].astype(float)
absolutos_mujeres = df.iloc[idx_mujeres+1 : idx_mujeres+14, 1].astype(float)

# Extraer y limpiar las etiquetas (quitar los numeritos finales y ajustar el texto largo)
etiquetas_raw = df.iloc[idx_hombres+1 : idx_hombres+14, 0].astype(str)
etiquetas_limpias = [re.sub(r'\d+$', '', lbl).strip() for lbl in etiquetas_raw]
etiquetas_limpias = [textwrap.fill(lbl, width=38) for lbl in etiquetas_limpias] # Para que no queden muy largas en la grÃ¡fica

# 3. CÁLCULO DE PORCENTAJES
pct_hombres = (absolutos_hombres.values / total_hombres) * 100
pct_mujeres = (absolutos_mujeres.values / total_mujeres) * 100

# Armar tabla interna y ordenar de mayor a menor basándonos en Mujeres (como la infografía)
df_res = pd.DataFrame({
    'Situacion': etiquetas_limpias,
    'Hombres': pct_hombres,
    'Mujeres': pct_mujeres
})
df_res = df_res.sort_values(by='Mujeres', ascending=True)

# 4. CREAR LA GRÁFICA ESTILO ANUARIO (Barras Horizontales)
fig, ax = plt.subplots(figsize=(12, 9))
fig.patch.set_facecolor('#ffffff')

# Colores similares a la infografía
color_hombres = '#F39180' # Coral/Naranja
color_mujeres = '#8AD2D1' # Aqua/Cyan

y = np.arange(len(df_res))
height = 0.35 # Grosor de la barra

# Dibujar las barras
bars_h = ax.barh(y - height/2, df_res['Hombres'], height, color=color_hombres, label='Hombres', edgecolor='none')
bars_m = ax.barh(y + height/2, df_res['Mujeres'], height, color=color_mujeres, label='Mujeres', edgecolor='none')

# Formatear ejes y textos
ax.set_yticks(y)
ax.set_yticklabels(df_res['Situacion'], fontsize=10, color='#666666')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False) # Ocultamos la lÃ­nea izquierda para que sea mÃ¡s limpio
ax.spines['bottom'].set_color('#cccccc')

# Etiquetas con los porcentajes exactos en la punta de cada barra
ax.bar_label(bars_h, fmt='%.1f%%', padding=5, color='#404040', fontsize=9, fontweight='bold')
ax.bar_label(bars_m, fmt='%.1f%%', padding=5, color='#404040', fontsize=9, fontweight='bold')

# Título y Leyenda
plt.title('DistribuciÃ³n porcentual de las situaciones de ciberacoso experimentadas\nen los Ãºltimos 12 meses, por sexo', 
          fontsize=14, fontweight='bold', color='#404040', pad=20)
ax.legend(loc='lower right', frameon=False, fontsize=11)

# Ajustar márgenes, guardar y mostrar
plt.tight_layout()
# Guardar salida
plt.savefig(PROJECT_ROOT / "output" / "figura_f6.png", dpi=300, bbox_inches='tight')

print("\n--- DATOS CALCULADOS CON 100% DE PRECISIÃ“N ---")
print(df_res.sort_values(by='Mujeres', ascending=False).to_string(index=False))
print("\nÂ¡GrÃ¡fica generada con Ã©xito como 'figura_f6.png'!")

plt.show()
