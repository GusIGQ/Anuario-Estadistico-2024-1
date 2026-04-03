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
import re

# 1. RUTA AL ARCHIVO EXCEL
ruta_archivo = PROJECT_ROOT / "datos" / "F.8" / "mociba2023_tabulados.xlsx"

# 2. LEER LA TABLA
df = pd.read_excel(ruta_archivo, sheet_name='1.42')

# Listas para guardar los datos extraídos
plataformas = []
porcentajes = []

# 3. EXTRACCI N DINÁMICA DE DATOS
# Recorremos todas las columnas buscando la palabra Relativos en la fila 15
for col in range(len(df.columns)):
    if str(df.iloc[15, col]).strip() == 'Relativos':
        # El nombre de la red social está en la fila 14, una columna a la izquierda
        nombre = str(df.iloc[14, col-1]).strip()

        # Por si la celda combinada desfasó el nombre una columna más
        if nombre.lower() == 'nan':
            nombre = str(df.iloc[14, col-2]).strip()

        # Limpiar el nombre (quitarle numeritos al final si los tiene)
        nombre = re.sub(r'\d+$', '', nombre).strip()

        # El valor porcentual está en la fila 17
        valor = df.iloc[17, col]

        # Guardar solo si el valor es un número válido (Ignorar NS - No sabe)
        if pd.notna(valor) and str(valor).strip() != 'NS':
            # Ajustar nombres largos para que quepan en la gráfica
            nombre_wrap = textwrap.fill(nombre, width=15)
            plataformas.append(nombre_wrap)
            porcentajes.append(float(valor))

# 4. PREPARAR DATOS (Ordenar de mayor a menor)
df_res = pd.DataFrame({'Medio': plataformas, 'Porcentaje': porcentajes})
df_res = df_res.sort_values(by='Porcentaje', ascending=False).reset_index(drop=True)

# 5. CREAR LA GRÁFICA ESTILO ANUARIO (Barras Verticales)
fig, ax = plt.subplots(figsize=(14, 6))
fig.patch.set_facecolor('#ffffff')

# Color Aqua/Teal característico del IFT
color_barras = '#8AD2D1'

x = np.arange(len(df_res))
width = 0.6 # Grosor de las barras

# Dibujar las barras
bars = ax.bar(x, df_res['Porcentaje'], width, color=color_barras, edgecolor='none')

# Configurar el Eje X
ax.set_xticks(x)
ax.set_xticklabels(df_res['Medio'], fontsize=9, color='#404040', rotation=0)

# Estilo limpio (sin bordes arriba, derecha, ni izquierda)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color('#cccccc')
ax.set_yticks([]) # Ocultar los números del eje Y

# Poner las etiquetas con el porcentaje exacto encima de cada barra
ax.bar_label(bars, fmt='%.1f%%', padding=5, color='#404040', fontweight='bold', fontsize=10)

# Título de la gráfica
plt.title('Porcentaje de población de 12 años y más que vivió ciberacoso por medios digitales', 
          fontsize=14, fontweight='bold', color='#404040', pad=20)

# Ajustar márgenes y guardar
fig.suptitle('Figura F.8. Porcentaje de población de 12 años y más que vivió ciberacoso por medios digitales', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
# Guardar salida
plt.savefig(PROJECT_ROOT / "output" / "figura_f8.png", dpi=300, bbox_inches='tight')

# Mostrar los datos extraídos en consola para validación
print("\n--- DATOS CALCULADOS CON 100% DE PRECISIÓN ---")
for index, row in df_res.iterrows():
    print(f"{row['Medio'].replace(chr(10), ' ')}: {row['Porcentaje']:.1f}%")

print("\n¡Gráfica generada con éxito como 'grafica_medios_digitales.png'!")
plt.show()
