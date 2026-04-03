import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import numpy as np

# 1. Cargar las dos bases de datos históricas (2022 y 2023)
df_2022 = pd.read_excel(PROJECT_ROOT / "datos" / "E.2" / "Base de datos_Cuarta Encuesta 2022_MiPymes.xlsx")
df_2023 = pd.read_excel(PROJECT_ROOT / "datos" / "E.2" / "Base de datos_Cuarta Encuesta 2023_MiPymes.xlsx")

# 2. Identificar columnas (son iguales en ambos años)
col_clasif = 'Clasificación de la empresa por su tamaño'
col_int = 'En términos generales ¿qué tan satisfechos se encuentran con el servicio de Internet recibido en la empresa o negocio en los últimos 12 meses? Recodificada'
col_fija = 'En términos generales ¿qué tan satisfechos se encuentran con el servicio de telefonía fija recibido en la empresa o negocio en los últimos 12 meses? Recodificada'

# 3. Calcular promedios para 2022 y 2023
means_int_2022 = df_2022.groupby(col_clasif)[col_int].mean()
means_fija_2022 = df_2022.groupby(col_clasif)[col_fija].mean()

means_int_2023 = df_2023.groupby(col_clasif)[col_int].mean()
means_fija_2023 = df_2023.groupby(col_clasif)[col_fija].mean()

# 4. Ordenar los datos (Micro, Pequeña, Mediana)
order = ['Micro', 'Pequeña', 'Mediana']

val_int_2022 = [means_int_2022.get(x, 0) for x in order]
val_fija_2022 = [means_fija_2022.get(x, 0) for x in order]

val_int_2023 = [means_int_2023.get(x, 0) for x in order]
val_fija_2023 = [means_fija_2023.get(x, 0) for x in order]

# 5. Configurar el lienzo (1 fila, 2 columnas)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
x = np.arange(len(order))
width = 0.35

# Colores (Gris para 2022, Naranja/Azul para 2023)
color_2022 = '#D3D3D3'
color_int_2023 = '#F79A8D' 
color_fija_2023 = '#2874A6'

# --- Gráfica 1: Internet Fijo ---
rects1_2022 = ax1.bar(x - width/2, val_int_2022, width, label='2022', color=color_2022)
rects1_2023 = ax1.bar(x + width/2, val_int_2023, width, label='2023', color=color_int_2023)

def autolabel(ax, rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  
                    textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold', color='black', fontsize=11)

autolabel(ax1, rects1_2022)
autolabel(ax1, rects1_2023)

# Limpieza visual Ax1
ax1.set_xticks(x)
ax1.set_xticklabels(order, fontweight='bold', fontsize=12)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.yaxis.set_visible(False)
ax1.set_title('Internet Fijo', fontweight='bold', fontsize=14, pad=15)
ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False, fontsize=11)

# --- Gráfica 2: Telefonía Fija ---
rects2_2022 = ax2.bar(x - width/2, val_fija_2022, width, label='2022', color=color_2022)
rects2_2023 = ax2.bar(x + width/2, val_fija_2023, width, label='2023', color=color_fija_2023)

autolabel(ax2, rects2_2022)
autolabel(ax2, rects2_2023)

# Limpieza visual Ax2
ax2.set_xticks(x)
ax2.set_xticklabels(order, fontweight='bold', fontsize=12)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.yaxis.set_visible(False)
ax2.set_title('Telefonía Fija', fontweight='bold', fontsize=14, pad=15)
ax2.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False, fontsize=11)

# Guardar la gráfica sin valores hardcodeados
fig.suptitle('Figura E.3. Servicios de telecomunicaciones contratados por las MiPymes', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
# Guardar salida
plt.savefig(PROJECT_ROOT / "output" / "Figura_E3.png", dpi=300, bbox_inches='tight')
