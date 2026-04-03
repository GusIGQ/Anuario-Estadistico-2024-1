import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import numpy as np
import os

# 1. CARGA Y PREPARACI N DE DATOS

ruta_csv = r'datos/F.1.3/tr_endutih_usuarios_anual_2023.csv'
print("Cargando la base de datos...")
# Cargar datos
df = pd.read_csv(ruta_csv, low_memory=False)

# Diccionario de habilidades mapeando la descripción con su columna en la ENDUTIH
mapa_habilidades = {
    'Enviar y recibir correo electrónico': 'P6_8_1',
    'Descargar contenidos de Internet': 'P6_8_2',
    'Crear archivos de texto': 'P6_8_4',
    'Copiar archivos entre directorios (carpetas)': 'P6_8_3',
    'Crear presentaciones': 'P6_8_6',
    'Crear hojas de cálculo': 'P6_8_5',
    'Instalar dispositivos periféricos': 'P6_8_7',
    'Crear o usar bases de datos': 'P6_8_8',
    'Programar en lenguaje especializado': 'P6_8_9'
}

# Filtros base: 6 años o más Y que sí usan computadora (P6_1 1)
filtro_base = (df['EDAD'] >= 6) & (df['P6_1'] == 1)
filtro_mujeres = filtro_base & (df['SEXO'] == 2)
filtro_hombres = filtro_base & (df['SEXO'] == 1)

# Totales poblacionales
total_mujeres_compu = df.loc[filtro_mujeres, 'FAC_PER'].sum()
total_hombres_compu = df.loc[filtro_hombres, 'FAC_PER'].sum()

# Listas dinámicas para guardar los resultados
nombres_habilidades = list(mapa_habilidades.keys())
pct_mujeres = []
pct_hombres = []

print("\nCalculando porcentajes...")
for nombre, columna in mapa_habilidades.items():
    # Suma de factores de expansión para quienes respondieron Sí (1) a la habilidad
    suma_mujeres = df.loc[filtro_mujeres & (df[columna] == 1), 'FAC_PER'].sum()
    suma_hombres = df.loc[filtro_hombres & (df[columna] == 1), 'FAC_PER'].sum()

    # Cálculo de porcentajes (redondeados a 0 decimales como en el Anuario)
    pct_m = round((suma_mujeres / total_mujeres_compu) * 100)
    pct_h = round((suma_hombres / total_hombres_compu) * 100)

    pct_mujeres.append(pct_m)
    pct_hombres.append(pct_h)

# 2. CREACI N DE LA GRÁFICA

# Invertir listas para que la primera habilidad (Correo) aparezca hasta arriba en la gráfica
nombres_habilidades.reverse()
pct_mujeres.reverse()
pct_hombres.reverse()

# Configuración del lienzo
fig, ax = plt.subplots(figsize=(12, 8))
x = np.arange(len(nombres_habilidades))
width = 0.35  # Grosor de las barras

# Dibujar las barras horizontales
rects1 = ax.barh(x + width/2, pct_mujeres, width, label='Mujeres', color='#8B3A62') # Color guinda IFT
rects2 = ax.barh(x - width/2, pct_hombres, width, label='Hombres', color='#B4B4B4') # Color gris

# Personalización del diseño
ax.set_xlabel('Porcentaje (%)', fontsize=11)
ax.set_title('Figura F.1.3. Habilidades en la computadora\n(Porcentaje con respecto del total de usuarios de computadora)', 
             pad=20, fontsize=14, fontweight='bold')
ax.set_yticks(x)
ax.set_yticklabels(nombres_habilidades, fontsize=11)
ax.legend(loc='lower right', frameon=False, fontsize=11)

# Estética: Quitar bordes para un diseño más limpio
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')
ax.set_xlim(0, 100)

# Función para poner los números en las barras
def autolabel(rects):
    for rect in rects:
        width_val = rect.get_width()
        # Colocamos la etiqueta a la derecha de la barra
        ax.annotate(f'{int(width_val)}%',
                    xy=(width_val, rect.get_y() + rect.get_height() / 2),
                    xytext=(15, 0),  # 15 puntos de separación
                    textcoords="offset points",
                    ha='center', va='center',
                    fontsize=10, fontweight='bold', color='#333333')

autolabel(rects1)
autolabel(rects2)

# Ajustar márgenes para que los textos no se corten
fig.suptitle('Figura F.1.3. Habilidades en la computadora', fontsize=14, fontweight='bold', y=1.02)
fig.tight_layout()

print("Generando Gráfica...")

# Guardar la gráfica en la carpeta de salida
output_dir = PROJECT_ROOT / "output"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "figura_f1.3.png")
# Guardar salida
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Gráfica guardada en: {output_path}")

plt.show()
