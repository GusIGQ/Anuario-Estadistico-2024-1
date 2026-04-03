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

# 1. RUTA AL ARCHIVO EXCEL (Ajusta la carpeta F.9 si es necesario)
ruta_archivo = PROJECT_ROOT / "datos" / "F.9" / "mociba2023_tabulados.xlsx"

# 2. LEER LA TABLA
df = pd.read_excel(ruta_archivo, sheet_name='1.50')

medidas = []
porcentajes = []

# 3. EXTRACCI N DINÁMICA DE DATOS
# En esta hoja, la palabra Relativos está en la fila 15 (índice 15 de pandas)
for col in range(len(df.columns)):
    if str(df.iloc[15, col]).strip() == 'Relativos':
        # El nombre de la medida está en la fila 14, una o dos columnas a la izquierda
        nombre = str(df.iloc[14, col-1]).strip()

        if nombre.lower() == 'nan':
            nombre = str(df.iloc[14, col-2]).strip()

        # Limpiar nombre de numeritos de referencias del INEGI (ej. Ninguna12 )
        nombre = re.sub(r'\d+$', '', nombre).strip()

        # El valor porcentual nacional está en la fila 17
        valor = df.iloc[17, col]

        if pd.notna(valor) and str(valor).strip() != 'NS':
            # Ajustar textos largos para la gráfica (max 35 caracteres por línea)
            nombre_wrap = textwrap.fill(nombre, width=35) 
            medidas.append(nombre_wrap)
            porcentajes.append(float(valor))

# 4. PREPARAR DATOS (Ordenar de MENOR a MAYOR para la gráfica horizontal)
df_res = pd.DataFrame({'Medida': medidas, 'Porcentaje': porcentajes})
df_res = df_res.sort_values(by='Porcentaje', ascending=True).reset_index(drop=True)

# 5. CREAR LA GRÁFICA ESTILO ANUARIO (Barras Horizontales)
fig, ax = plt.subplots(figsize=(10, 8))
fig.patch.set_facecolor('#ffffff')

color_barras = '#8AD2D1' # Aqua/Teal del IFT

y = np.arange(len(df_res))
height = 0.6 # Grosor de las barras

# Dibujar barras
bars = ax.barh(y, df_res['Porcentaje'], height, color=color_barras, edgecolor='none')

# Configurar el Eje Y
ax.set_yticks(y)
ax.set_yticklabels(df_res['Medida'], fontsize=10, color='#404040')

# Estilo ultra limpio (sin bordes arriba, derecha, abajo)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.set_xticks([]) # Ocultar los números del eje X

# Etiquetas con el porcentaje exacto al final de cada barra
ax.bar_label(bars, fmt='%.1f%%', padding=5, color='#404040', fontweight='bold', fontsize=10)

# Título de la gráfica
plt.title('Medidas tomadas contra el ciberacoso experimentado', 
          fontsize=16, fontweight='bold', color='#404040', pad=20)

# Ajustar márgenes y guardar
fig.suptitle('Figura F.9. Acciones de los usuarios de Internet que vivieron ciberacoso', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
# Guardar salida
plt.savefig(PROJECT_ROOT / "output" / "figura_f9.png", dpi=300, bbox_inches='tight')

# Mostrar los datos extraídos en consola (Ordenados de mayor a menor para leerlos fácil)
print("\n--- DATOS CALCULADOS CON 100% DE PRECISIÓN ---")
for index, row in df_res.sort_values(by='Porcentaje', ascending=False).iterrows():
    print(f"{row['Medida'].replace(chr(10), ' ')}: {row['Porcentaje']:.1f}%")

print("\n¡Gráfica generada con éxito como 'figura_f9.png'!")
plt.show()
