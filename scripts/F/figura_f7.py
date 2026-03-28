import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import numpy as np
import textwrap

# 1. RUTA AL ARCHIVO EXCEL
ruta_archivo = PROJECT_ROOT / "datos" / "F.7" / "mociba2023_tabulados.xlsx"

# 2. LEER LAS TABLAS (Hombres 1.11, Mujeres 1.12)
df_hombres = pd.read_excel(ruta_archivo, sheet_name='1.11')
df_mujeres = pd.read_excel(ruta_archivo, sheet_name='1.12')

# 3. EXTRAER DATOS (De la fila 18 a la 25, y la columna 4 que tiene los relativos)
# Aseguramos que los nombres de las medidas los tomamos de una de las tablas
etiquetas_raw = df_mujeres.iloc[18:26, 0].astype(str)

# Limpiar las etiquetas para la gráfica
etiquetas_limpias = []
for lbl in etiquetas_raw:
    lbl_clean = lbl.strip()
    # Romper el texto para que quepa bien en el eje Y
    lbl_wrapped = textwrap.fill(lbl_clean, width=25) 
    etiquetas_limpias.append(lbl_wrapped)

# Extraer los porcentajes de la columna 4 (índice 4)
pct_hombres = df_hombres.iloc[18:26, 4].astype(float).values
pct_mujeres = df_mujeres.iloc[18:26, 4].astype(float).values

# Invertir el orden para que la medida del 96% quede hasta arriba en la gráfica
etiquetas_limpias = etiquetas_limpias[::-1]
pct_hombres = pct_hombres[::-1]
pct_mujeres = pct_mujeres[::-1]

# 4. CREAR LA GRÁFICA ESTILO ANUARIO (Dos paneles)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8), sharey=True)
fig.patch.set_facecolor('#ffffff')

# Colores institucionales
color_hombres = '#F39180' # Coral
color_mujeres = '#8AD2D1' # Aqua

y = np.arange(len(etiquetas_limpias))
height = 0.6 # Grosor de las barras

# --- Gráfica Hombres (Izquierda) ---
bars1 = ax1.barh(y, pct_hombres, height, color=color_hombres, edgecolor='none')
ax1.set_title('Hombres', fontsize=16, fontweight='bold', color='#404040', pad=20)
ax1.set_yticks(y)
ax1.set_yticklabels(etiquetas_limpias, fontsize=10, color='#404040')
ax1.set_xlim(0, 105) # LÃ­mite hasta 100%

# Estilo limpio
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_color('#cccccc')
ax1.spines['left'].set_visible(False)

# Etiquetas de datos
ax1.bar_label(bars1, fmt='%.1f%%', padding=5, color='#404040', fontweight='bold', fontsize=10)

# --- Gráfica Mujeres (Derecha) ---
bars2 = ax2.barh(y, pct_mujeres, height, color=color_mujeres, edgecolor='none')
ax2.set_title('Mujeres', fontsize=16, fontweight='bold', color='#404040', pad=20)
ax2.set_xlim(0, 105)

# Estilo limpio
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_color('#cccccc')
ax2.spines['left'].set_visible(False)

# Etiquetas de datos
ax2.bar_label(bars2, fmt='%.1f%%', padding=5, color='#404040', fontweight='bold', fontsize=10)

# Ajustes finales y guardado
plt.tight_layout()
plt.subplots_adjust(wspace=0.1) # Reducir espacio entre las dos grÃ¡ficas
# Guardar salida
plt.savefig(PROJECT_ROOT / "output" / "figura_f7.png", dpi=300, bbox_inches='tight')

print("\nÂ¡GrÃ¡fica generada con Ã©xito como 'grafica_medidas_seguridad.png'!")
plt.show()
