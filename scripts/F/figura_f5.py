import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import numpy as np

# 1. EXTRAER LOS DATOS EXACTOS
ruta_archivo = PROJECT_ROOT / "datos" / "F.5" / "mociba2023_tabulados.xlsx"

# Leemos las hojas sin saltar filas para mantener los índices correctos
df_mujeres = pd.read_excel(ruta_archivo, sheet_name='1.18')
df_hombres = pd.read_excel(ruta_archivo, sheet_name='1.17')

# La fila 17 tiene el Total. La columna 3 tiene los Absolutos de Sí vivió ciberacoso
total_mujeres = float(df_mujeres.iloc[17, 3])
total_hombres = float(df_hombres.iloc[17, 3])

# Las filas 18 a la 23 tienen los 6 rangos de edad
absolutos_mujeres = df_mujeres.iloc[18:24, 3].astype(float)
absolutos_hombres = df_hombres.iloc[18:24, 3].astype(float)

# Calculamos los porcentajes exactos
pct_mujeres = (absolutos_mujeres / total_mujeres) * 100
pct_hombres = (absolutos_hombres / total_hombres) * 100

# Etiquetas para la gráfica (con salto de línea para que se vean bien)
edades = ['De 12 a\n19 años', 'De 20 a\n29 años', 'De 30 a\n39 años', 'De 40 a\n49 años', 'De 50 a\n59 años', 'De 60 años\ny más']

# 2. CREAR LA GRÁFICA ESTILO ANUARIO IFT
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6), sharey=True)
fig.patch.set_facecolor('#ffffff')

# Colores similares a la infografía
color_mujeres = '#8AD2D1' # Aqua/Cyan
color_hombres = '#F39180' # Coral/Naranja

x = np.arange(len(edades))
width = 0.4 # Grosor de las barras

# --- Gráfica Mujeres ---
bars1 = ax1.bar(x, pct_mujeres, width, color=color_mujeres, edgecolor='none', capstyle='round')
ax1.set_title('Mujeres', fontsize=16, fontweight='bold', color='#404040', pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(edades, fontsize=10, color='#666666')
ax1.set_ylim(0, 35) # Limite Y para que haya espacio arriba
# Ocultar bordes y ejes y para que sea limpio como el PDF
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.spines['bottom'].set_color('#cccccc')
ax1.set_yticks([]) 
ax1.bar_label(bars1, fmt='%.1f%%', padding=5, color='#404040', fontweight='bold', fontsize=10)

# --- Gráfica Hombres ---
bars2 = ax2.bar(x, pct_hombres, width, color=color_hombres, edgecolor='none')
ax2.set_title('Hombres', fontsize=16, fontweight='bold', color='#404040', pad=20)
ax2.set_xticks(x)
ax2.set_xticklabels(edades, fontsize=10, color='#666666')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['bottom'].set_color('#cccccc')
ax2.set_yticks([])
ax2.bar_label(bars2, fmt='%.1f%%', padding=5, color='#404040', fontweight='bold', fontsize=10)

# Ajustar diseño y guardar
fig.suptitle('Figura F.5. Distribución porcentual de personas que vivieron ciberacoso por grupo de edad y sexo', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
# Guardar salida
plt.savefig(PROJECT_ROOT / "output" / "figura_f5.png", dpi=300, bbox_inches='tight')
print("¡Cálculos completados al 100% de precisión y Gráfica generada con éxito!")
plt.show()
