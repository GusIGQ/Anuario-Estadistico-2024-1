import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import matplotlib.patches as mpatches
import os

# 1. RUTAS Y CARGA DE DATOS (DINÁMICO)

# Importante Asegúrate de que estas rutas coincidan con la ubicación en tu PC
ruta_2022 = PROJECT_ROOT / "datos" / "E.7" / "Base de datos_Cuarta Encuesta 2022_MiPymes.xlsx"
ruta_2023 = PROJECT_ROOT / "datos" / "E.7" / "Base de datos_Cuarta Encuesta 2023_MiPymes.xlsx"

try:
    # Usar openpyxl como motor para leer xlsx
    df_2022 = pd.read_excel(ruta_2022, engine='openpyxl')
    df_2023 = pd.read_excel(ruta_2023, engine='openpyxl')
    print("¡Bases de datos cargadas exitosamente!")
except Exception as e:
    print(f"Error fatal al cargar archivos Excel: {e}")
    exit()

# 2. CONFIGURACI N Y FUNCIONES DE CÁLCULO

# Categorías estándar para el eje X
categorias = ['General', 'Micro', 'Pequeña', 'Mediana']

# Configuración de los 6 dispositivos (Título en PDF y Palabra clave en Excel)
configuracion_dispositivos = [
    {"titulo": "Teléfonos móviles inteligentes\n(Smartphones)", "clave": "Smartphone"},
    {"titulo": "Computadoras de escritorio", "clave": "escritorio"},
    {"titulo": "Terminal punto de venta fija,\npara celular (clip) o tableta", "clave": "Terminal"},
    {"titulo": "Laptop", "clave": "Laptop"},
    {"titulo": "Teléfonos móviles análogos", "clave": "sin acceso"},
    {"titulo": "Servidores de almacenamiento\nde información", "clave": "Servidores"}
]

# Función para calcular porcentaje ponderado
def calcular_pct_ponderado(df, col_val, col_peso):
    # Asegurarnos de que no hay valores vacíos antes de calcular
    df_valido = df[df[col_val].notna()]
    if df_valido.empty: return 0.0
    # Sumamos los pesos de los que contestaron que Sí (empiezan con la S)
    peso_si = df_valido.loc[df_valido[col_val].astype(str).str.startswith('S', na=False), col_peso].sum()
    peso_total = df_valido[col_peso].sum()
    return (peso_si / peso_total) * 100 if peso_total > 0 else 0

# --- PROCESO DE CÁLCULO DINÁMICO ---
print("\nIniciando cálculo de datos al vuelo...")

# Estructura para guardar resultados: resultados Smartphone 2023 Gral, Micro, Peq, Med
resultados = {} 

for df, anio in [(df_2022, 2022), (df_2023, 2023)]:
    # Identificar columnas clave dinámicamente en esta base
    col_tam = [c for c in df.columns if 'tama' in c.lower() or 'tam' in c.lower()][0]
    col_fac = [c for c in df.columns if 'factor' in c.lower() or 'expans' in c.lower()][0]

    for dev in configuracion_dispositivos:
        titulo = dev['titulo']
        if titulo not in resultados: resultados[titulo] = {}

        # Encontrar la columna exacta para este dispositivo en esta base
        col_dev = [c for c in df.columns if dev['clave'].lower() in c.lower()][0]

        # Calcular los 4 valores
        lista_pcts = []
        # 1. General
        lista_pcts.append(calcular_pct_ponderado(df, col_dev, col_fac))
        # 2-4. Por tamaño
        for cat in categorias[1:]:
            # Buscar el nombre real en la columna (ej. Pequeña, Peque f a)
            nombre_real = [t for t in df[col_tam].dropna().unique() if cat[:4].lower() in t.lower()][0]
            df_tam = df[df[col_tam] == nombre_real]
            lista_pcts.append(calcular_pct_ponderado(df_tam, col_dev, col_fac))

        resultados[titulo][anio] = lista_pcts

print("¡Cálculos completados! Generando Gráfica...")

# 3. GENERACI N DE LA GRÁFICA MULTIPANEL

# Configurar el lienzo (2 filas x 3 columnas 6 gráficas)
fig, axes = plt.subplots(2, 3, figsize=(18, 11), dpi=150)
fig.patch.set_facecolor('#F8FBFA') # Fondo sutil azulado del PDF

# Colores fila superior (índices 0, 1, 2)
color_2022_top = '#AEE0D8' # Verde agua claro
color_2023_top = '#297285' # Azul/Teal oscuro

# Colores fila inferior (índices 3, 4, 5)
color_2022_bot = '#F5A18B' # Naranja claro
color_2023_bot = '#EA5D4E' # Rojo oscuro

x = np.arange(len(categorias))
width = 0.3  # Ancho de las barras

# Título Principal
fig.text(0.02, 0.94, '■', fontsize=12, color='#E8604B', fontweight='bold', ha='left')
fig.text(0.03, 0.94, 'Figura E.7. Dispositivos que usan las MiPymes para realizar sus actividades (2022-2023)', 
         fontsize=14, fontweight='bold', color='#5D6778', ha='left')

axes_planos = axes.flatten()

for i, ax in enumerate(axes_planos):
    config = configuracion_dispositivos[i]
    titulo = config['titulo']

    data_2022 = resultados[titulo][2022]
    data_2023 = resultados[titulo][2023]

    c_2022 = color_2022_top if i < 3 else color_2022_bot
    c_2023 = color_2023_top if i < 3 else color_2023_bot

    # Fondo redondeado de cada panel
    bbox = mpatches.FancyBboxPatch(
        (0, 0), 1, 1,
        boxstyle="round,pad=0.08,rounding_size=0.04",
        transform=ax.transAxes,
        facecolor='#F0F6F5',
        edgecolor='none',
        zorder=0
    )
    ax.add_patch(bbox)
    ax.set_facecolor('none')

    # Pintar las barras
    rects1 = ax.bar(x - width/2 - 0.02, data_2022, width, label='2022', color=c_2022, zorder=3)
    rects2 = ax.bar(x + width/2 + 0.02, data_2023, width, label='2023', color=c_2023, zorder=3)

    # Titulo del panel (evitando set_title para posicionar dentro de la tarjeta)
    ax.text(0.05, 0.92, titulo, transform=ax.transAxes, fontsize=12, fontweight='bold', color='#3B4252',
            va='top', ha='left')

    ax.set_xticks(x)
    ax.set_xticklabels(categorias, fontsize=10, fontweight='bold', color='#7A8593')

    # Limpieza visual
    ax.get_yaxis().set_visible(False)
    for spine in ax.spines.values(): 
        spine.set_visible(False)
    ax.tick_params(axis='x', length=0, pad=8)

    # Etiquetas de datos
    def autolabel(rects, ax):
        for rect in rects:
            height = rect.get_height()
            if height > 0:
                ax.annotate(f'{height:.1f}%',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 5), 
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=9, fontweight='bold', color='#4C566A')

    autolabel(rects1, ax)
    autolabel(rects2, ax)

    max_h = max(data_2022 + data_2023)
    ax.set_ylim(0, max_h + 30) # Espacio para el título y leyendas

    # Mini leyenda por panel
    patch_2022 = mpatches.Patch(color=c_2022, label='2022')
    patch_2023 = mpatches.Patch(color=c_2023, label='2023')
    ax.legend(handles=[patch_2022, patch_2023], loc='lower center', bbox_to_anchor=(0.5, -0.25),
               ncol=2, frameon=False, fontsize=10, handlelength=1.5, handleheight=0.6)

# Ajuste global
plt.subplots_adjust(wspace=0.15, hspace=0.45, top=0.85, bottom=0.2, left=0.03, right=0.97)

# Textos inferiores (Footer)
footer_y = 0.08
fig.text(0.02, footer_y, 'Fuente: ', fontsize=10, fontweight='bold', color='#3B4252', ha='left')
fig.text(0.06, footer_y, 'IFT con información de la Cuarta Encuesta 2023, Usuarios de Servicios de Telecomunicaciones (micro, pequeñas y medianas empresas).', 
         fontsize=10, color='#3B4252', ha='left')

fig.text(0.02, footer_y - 0.025, 'Para más información consultar: ', fontsize=10, color='#3B4252', ha='left')
fig.text(0.165, footer_y - 0.025, 'https://www.ift.org.mx/usuarios-y-audiencias/encuestas-trimestrales.', 
         fontsize=10, color='#3B4252', ha='left', style='italic')

fig.text(0.02, footer_y - 0.05, 'Nota: ', fontsize=10, fontweight='bold', color='#3B4252', ha='left')
fig.text(0.05, footer_y - 0.05, 'Respuesta múltiple, por lo que la suma no da 100%. Es importante señalar que los resultados pueden presentar variaciones que pueden ser explicadas por el error teórico de cada encuesta.', 
         fontsize=10, color='#3B4252', ha='left')

ruta_salida_dir = PROJECT_ROOT / "output"
nombre_imagen = "figura_E7.png"
ruta_completa = os.path.join(ruta_salida_dir, nombre_imagen)
os.makedirs(ruta_salida_dir, exist_ok=True)
# Guardar salida
plt.savefig(ruta_completa, facecolor=fig.get_facecolor(), bbox_inches='tight', dpi=150)
print(f"¡Gráfica completa y réplica exportada exitosamente en: {ruta_completa}!")
