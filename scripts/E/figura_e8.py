import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import os

# 1. RUTA Y CARGA DE DATOS

# Ruta de tu archivo 2023
ruta_2023 = PROJECT_ROOT / "datos" / "E.8" / "Base de datos_Cuarta Encuesta 2023_MiPymes.xlsx"

try:
    # Cargar datos
    df = pd.read_excel(ruta_2023, engine='openpyxl')
    print("¡Base de datos 2023 cargada exitosamente!")
except Exception as e:
    print(f"Error al cargar el archivo Excel: {e}")
    exit()

# 2. B sSQUEDA DE COLUMNAS Y CÁLCULOS

# Identificar dinámicamente el Tamaño de empresa y Factor de expansión
col_tam = [c for c in df.columns if 'tama' in c.lower() or 'tam' in c.lower()][0]
col_fac = [c for c in df.columns if 'factor' in c.lower() or 'expans' in c.lower()][0]

# Función para calcular porcentaje ponderado
def calcular_pct_ponderado(df_filtro, col_val, col_peso):
    df_valido = df_filtro[df_filtro[col_val].notna()]
    if df_valido.empty: return 0.0
    peso_si = df_valido.loc[df_valido[col_val].astype(str).str.startswith('S', na=False), col_peso].sum()
    peso_total = df_valido[col_peso].sum()
    return (peso_si / peso_total) * 100 if peso_total > 0 else 0

categorias = ['General', 'Micro', 'Pequeña', 'Mediana']

# Los 4 beneficios a evaluar con sus palabras clave para encontrar la columna en el Excel
beneficios_config = [
    {"titulo": "El contacto con los clientes\nes más rápido", "clave": "contacto con los clientes"},
    {"titulo": "La solicitud de pedidos\nes más ágil", "clave": "solicitud de pedidos"},
    {"titulo": "Mayor competitividad\nen el mercado", "clave": "competitividad"},
    {"titulo": "Facilita el control\nde ventas", "clave": "control de ventas"}
]

print("\nCalculando datos al vuelo...")
resultados = {}

for ben in beneficios_config:
    titulo = ben['titulo']

    # Buscar la columna que contiene la pregunta sobre los beneficios de la app
    cols_encontradas = [c for c in df.columns if 'beneficios de contar con una aplicaci' in c.lower() and ben['clave'].lower() in c.lower()]

    if not cols_encontradas:
        print(f"ERROR: No se encontró la columna para: {titulo}")
        continue

    col_exacta = cols_encontradas[0]
    lista_pcts = []

    # 1. General
    lista_pcts.append(calcular_pct_ponderado(df, col_exacta, col_fac))

    # 2. Por tamaño
    for cat in categorias[1:]:
        # Adaptar al texto real en el Excel (ignora tildes rotas)
        nombre_real = [t for t in df[col_tam].dropna().unique() if cat[:4].lower() in t.lower()][0]
        df_tam = df[df[col_tam] == nombre_real]
        lista_pcts.append(calcular_pct_ponderado(df_tam, col_exacta, col_fac))

    resultados[titulo] = lista_pcts

print("Cálculos listos. Dibujando Gráfica...")

# 3. GENERACI N DE LA GRÁFICA (2x2)

# Configurar lienzo para 4 paneles
fig, axes = plt.subplots(2, 2, figsize=(12, 10), dpi=150)
fig.patch.set_facecolor('#F8FBFA')

# Usaremos un color institucional del IFT para el 2023
color_barras = '#2B7B94'

x = np.arange(len(categorias))
width = 0.5 # Barras un poco más anchas al ser un solo año

axes_planos = axes.flatten()

for i, ax in enumerate(axes_planos):
    config = beneficios_config[i]
    titulo = config['titulo']
    datos = resultados[titulo]

    # Dibujar barras (solo 1 por categoría)
    rects = ax.bar(x, datos, width, color=color_barras)

    # Estilo del panel
    ax.set_title(titulo, loc='center', fontsize=13, fontweight='bold', color='#333333', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(categorias, fontsize=11, color='#555555')

    # Limpiar bordes
    ax.get_yaxis().set_visible(False)
    for spine in ax.spines.values(): spine.set_visible(False)

    # Etiquetas de % arriba de cada barra
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold', color='#222222')

    max_h = max(datos)
    ax.set_ylim(0, max_h + (max_h * 0.25))

# 4. EXPORTACI N

# Texto descriptivo inferior calcado del PDF
footer_text = 'Fuente: IFT con información de la Cuarta Encuesta 2023, Usuarios de Servicios de Telecomunicaciones (micro, pequeñas y medianas empresas).' \
              '\nNota: Respuesta espontánea y múltiple no suma 100%.'
fig.text(0.05, 0.02, footer_text, fontsize=10, color='#555555', ha='left')

fig.suptitle('Figura E.8. Actividades de las MiPymes en Internet', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout(rect=[0.02, 0.05, 0.98, 0.95])

# Definir la ruta de salida
ruta_salida_dir = PROJECT_ROOT / "output"
nombre_imagen = "Figura_E8.png"
ruta_completa = os.path.join(ruta_salida_dir, nombre_imagen)

os.makedirs(ruta_salida_dir, exist_ok=True)
# Guardar salida
plt.savefig(ruta_completa, facecolor=fig.get_facecolor(), bbox_inches='tight')

print(f"¡Gráfica exportada exitosamente en: {ruta_completa}!")
