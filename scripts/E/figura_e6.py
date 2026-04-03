import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 1. CÁLCULO DE DATOS EXACTOS

# Cargar la base de datos (ajusta el nombre del archivo si es necesario)
file_path = PROJECT_ROOT / "datos" / "E.6" / "Base de datos_Cuarta Encuesta 2023_MiPymes.xlsx"
# Cargar datos
df = pd.read_excel(file_path)

# Definir las columnas a utilizar
vender_internet_col = '¿Cuál de las siguientes actividades realiza a través de Internet? Vender servicios o productos'
beneficio_col = '¿Cuál es el principal beneficio de que la empresa venda a través de Internet?'
size_col = 'Clasificación de la empresa por su tamaño'
factor_col = 'Factor de Expansión Final'

# Filtrar solo las empresas que SÍ venden por internet
df_vende = df[df[vender_internet_col] == 'Sí']

# Función para calcular los porcentajes ponderados
def obtener_porcentajes(df_subset):
    peso_total = df_subset[factor_col].sum()
    resultados = {}
    for cat in df_subset[beneficio_col].unique():
        if pd.isna(cat): continue
        peso_cat = df_subset[df_subset[beneficio_col] == cat][factor_col].sum()
        resultados[cat] = (peso_cat / peso_total) * 100
    return resultados

# Calcular para cada segmento
datos_general = obtener_porcentajes(df_vende)
datos_micro = obtener_porcentajes(df_vende[df_vende[size_col] == 'Micro'])
datos_pequena = obtener_porcentajes(df_vende[df_vende[size_col] == 'Pequeña'])
datos_mediana = obtener_porcentajes(df_vende[df_vende[size_col] == 'Mediana'])

# Categorías que queremos graficar (en el orden de la imagen)
categorias = [
    'Incremento de ventas', 
    'Ampliar canales de venta', 
    'Inclusión de marketing digital', 
    'La rapidez en la que se realizan las ventas o compras', 
    'Otro'
]

# Etiquetas más cortas para el eje X
etiquetas_x = [
    'Incremento de ventas', 
    'Ampliar canales\nde venta', 
    'Inclusión de\nmarketing digital', 
    'La rapidez en la que se\nrealizan las ventas...', 
    'Otros'
]

# Extraer los valores en el orden correcto, si no existe el valor se pone 0
valores_general = [datos_general.get(cat, 0) for cat in categorias]
valores_micro = [datos_micro.get(cat, 0) for cat in categorias]
valores_pequena = [datos_pequena.get(cat, 0) for cat in categorias]
valores_mediana = [datos_mediana.get(cat, 0) for cat in categorias]

# 2. GENERACI N DE LA GRÁFICA

# Configuración de colores basados en la infografía
colores = {
    'General': '#a2d2d9', # Azul claro
    'Micro': '#f19a9b',   # Salmón
    'Pequeña': '#297b93', # Azul oscuro
    'Mediana': '#ea5b60'  # Rojo
}

# Preparar las posiciones de las barras
x = np.arange(len(categorias))  # Localización de las etiquetas
ancho_barra = 0.15              # Ancho de cada barra

# Crear grafica
fig, ax = plt.subplots(figsize=(12, 6))

# Dibujar las barras para cada segmento
barras_general = ax.bar(x - ancho_barra*1.5, valores_general, ancho_barra, label='General', color=colores['General'])
barras_micro = ax.bar(x - ancho_barra*0.5, valores_micro, ancho_barra, label='Micro', color=colores['Micro'])
barras_pequena = ax.bar(x + ancho_barra*0.5, valores_pequena, ancho_barra, label='Pequeña', color=colores['Pequeña'])
barras_mediana = ax.bar(x + ancho_barra*1.5, valores_mediana, ancho_barra, label='Mediana', color=colores['Mediana'])

# Función para añadir las etiquetas de porcentaje encima de cada barra
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        if height > 0: # Solo mostrar si es mayor a 0
            ax.annotate(f'{height:.1f}%',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 puntos de desplazamiento vertical
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)

autolabel(barras_general)
autolabel(barras_micro)
autolabel(barras_pequena)
autolabel(barras_mediana)

# Formatear el gráfico
ax.set_ylabel('Porcentaje (%)')
ax.set_title('Beneficios de vender a través de Internet fijo')
ax.set_xticks(x)
ax.set_xticklabels(etiquetas_x)
ax.set_ylim(0, 65) # Limite en Y para dar espacio a las etiquetas y coincidir con el 60% de la imagen

# Añadir leyenda abajo
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4, frameon=False)

# Ocultar los bordes superior y derecho para un diseño más limpio
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Añadir una cuadrícula sutil en el eje Y
ax.yaxis.grid(True, linestyle='--', alpha=0.7)
ax.set_axisbelow(True)

# Ajustar el diseño para que no se corte nada
fig.suptitle('Figura E.6. Beneficios de vender a través de Internet para las MiPymes', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()

# Guardar la gráfica como imagen en lugar de mostrarla
plt.savefig(PROJECT_ROOT / "output" / "Figura_E6.png", dpi=300, bbox_inches='tight')
print("¡Cálculo finalizado y Gráfica guardada exitosamente como 'grafica_beneficios_calculada.png'!")
