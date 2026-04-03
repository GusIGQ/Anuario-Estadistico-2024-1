import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import numpy as np

# 1. Carga de datos
file_path = PROJECT_ROOT / "datos" / "E.9" / "Base de datos_MiPymes_imp_exp_2022.xlsx"
# Cargar datos
df = pd.read_excel(file_path)

# Definimos los nombres de las columnas basados en tu archivo
col_pregunta = "¿Y cuál de estos servicios considera el MÁS importante para llevar a cabo estas actividades?"
col_factor = "Factor de Expansión Final"

# 2. Procesamiento y Cálculo de Porcentajes Exactos
# El IFT calcula el porcentaje sobre el TOTAL de respuestas, incluyendo Ns/Nc
# en el denominador para obtener las cifras del reporte (63.4%, 20.8%, etc.)
df_valid = df.dropna(subset=[col_pregunta])
total_expandido = df_valid[col_factor].sum()

# Agrupamos y sumamos el factor de expansión por cada servicio
conteos_ponderados = df_valid.groupby(col_pregunta)[col_factor].sum()
porcentajes = (conteos_ponderados / total_expandido) * 100

# 3. Preparación de datos para la gráfica (Excluyendo Ns/Nc para la visualización)
servicios_map = {
    "Conexión a Internet fijo (incluye conexión Wi-Fi)": "Conexión a\nInternet fijo",
    "Telefonía fija": "Telefonía fija",
    "Telefonía móvil": "Telefonía móvil",
    "Conexión a Internet por datos móviles (por red de telefonía móvil)": "Conexión a Internet\npor datos móviles",
    "Televisión de paga": "Televisión de paga"
}

# Extraemos los valores específicos en el orden deseado
labels = list(servicios_map.values())
valores = [porcentajes.get(k, 0) for k in servicios_map.keys()]
colores = ['#A8DADC', '#2A6F97', '#463F59', '#F4A29B', '#EF476F']

# Invertimos el orden para que el más alto aparezca arriba en la gráfica de barras horizontales
labels.reverse()
valores.reverse()
colores.reverse()

# 4. Generación de la Gráfica
fig, ax = plt.subplots(figsize=(10, 6))
y_pos = np.arange(len(labels))

bars = ax.barh(y_pos, valores, color=colores, height=0.6)

# Estética de la gráfica (Quitar bordes y ejes)
for spine in ['top', 'right', 'bottom', 'left']:
    ax.spines[spine].set_visible(False)
ax.xaxis.set_ticks([])
ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=11, color='#333333')
ax.tick_params(axis='y', length=0)

# Añadir etiquetas de porcentaje al final de cada barra
for bar in bars:
    width = bar.get_width()
    ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
            f'{width:.1f}%', va='center', fontsize=11, fontweight='bold', color='#333333')

plt.title("Figura E.9. Servicios de Telecomunicaciones más importantes para MiPymes (Imp/Exp)", 
          fontsize=12, loc='left', pad=20)

plt.tight_layout()
# Guardar salida
plt.savefig(PROJECT_ROOT / "output" / "Figura_E9.png", dpi=300)
plt.show()
