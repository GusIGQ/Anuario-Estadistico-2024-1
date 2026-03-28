import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import numpy as np

print("Cargando y procesando la base de datos...")
# 1. Cargar datos
df = pd.read_excel(PROJECT_ROOT / "datos" / "F.11" / "Tercera Encuesta 2023_Int&TV.xlsx")

# 2. Definir columnas clave
w_col = 'Factor de ExpansiÃ³n Final Normalizado que considera calibraciÃ³n (post-estratificaciÃ³n) por sexo y grupos de edad 5 (redondeos corregidos) (a cifras del Censo INEGI, 2020)'
df[w_col] = pd.to_numeric(df[w_col], errors='coerce')

col_internet = 'De la siguiente lista de servicios, Â¿podrÃ­a decirme cuÃ¡les tiene contratados o cuenta con ellos en su hogar? ConexiÃ³n a Internet fijo en su hogar (incluye conexiÃ³n Wi-Fi)'

# 3. Filtrar usuarios de Internet Fijo
df_internet = df[df[col_internet] == 'SÃ­'].copy()

# 4. Calcular pesos totales de la muestra poblacional por género
w_hombres = df_internet[df_internet['GÃ©nero'] == 'Hombre'][w_col].sum()
w_mujeres = df_internet[df_internet['GÃ©nero'] == 'Mujer'][w_col].sum()

# 5. Diccionario y orden de categorías según la Figura F.11
label_mapping = {
    'Menores de edad': 'NiÃ±os, niÃ±as y\nadolescentes',
    'Mujeres': 'Mujeres',
    'Adultos mayores / Personas de la tercera edad': 'Personas adultas\nmayores',
    'Personas con discapacidad': 'Personas con\ndiscapacidad',
    'Integrantes de la comunidad LGBTIQ+': 'Personas de la\ncomunidad LGBTIQ+',
    'Personas indÃ­genas': 'Personas indÃ­genas',
    'Hombres': 'Hombres',
    'Personas negras o afrodescendientes': 'Personas\nafrodescendientes',
    'Todas las personas son vulnerables': 'Todas las personas\nson vulnerables'
}

pdf_order = [
    'NiÃ±os, niÃ±as y\nadolescentes',
    'Mujeres',
    'Personas adultas\nmayores',
    'Personas con\ndiscapacidad',
    'Personas de la\ncomunidad LGBTIQ+',
    'Personas indÃ­genas',
    'Hombres',
    'Personas\nafrodescendientes',
    'Todas las personas\nson vulnerables'
]

# 6. Cálculo dinámico iterando sobre las columnas de violencia
violencia_cols = [col for col in df.columns if 'mayor riesgo' in col.lower()]
results_hombres = {}
results_mujeres = {}

for col in violencia_cols:
    if '? ' in col:
        category = col.split('? ')[1]
        if category in label_mapping:
            label = label_mapping[category]

            # Filtramos los que respondieron que Sí
            mask_si = df_internet[col].apply(lambda x: str(x).strip().lower() == 'sÃ­')
            df_si = df_internet[mask_si]

            # Sumamos los ponderadores de los Sí separados por género
            w_si_hombres = df_si[df_si['GÃ©nero'] == 'Hombre'][w_col].sum()
            w_si_mujeres = df_si[df_si['GÃ©nero'] == 'Mujer'][w_col].sum()

            # Calculamos porcentaje matemático final
            results_hombres[label] = (w_si_hombres / w_hombres) * 100
            results_mujeres[label] = (w_si_mujeres / w_mujeres) * 100

# Preparar listas para la gráfica (se invierten para que el primero quede hasta arriba)
categorias_rev = pdf_order[::-1]
valores_hombres = [results_hombres[cat] for cat in categorias_rev]
valores_mujeres = [results_mujeres[cat] for cat in categorias_rev]

# 7. Graficar (Gráfico de barras agrupadas horizontales)
fig, ax = plt.subplots(figsize=(10, 8))

y = np.arange(len(categorias_rev))
height = 0.35 # Grosor de las barras

# Crear las dos barras paralelas por categoría
rects_muj = ax.barh(y - height/2, valores_mujeres, height, label='Mujeres', color='#f48fb1')
rects_hom = ax.barh(y + height/2, valores_hombres, height, label='Hombres', color='#c2185b')

# 8. Etiquetas y Leyenda
ax.set_yticks(y)
ax.set_yticklabels(categorias_rev, fontsize=11)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False, fontsize=11)

# Poner el % en texto junto a cada barra
def autolabel(rects):
    for rect in rects:
        width = rect.get_width()
        ax.annotate(f'{width:.1f}%',
                    xy=(width, rect.get_y() + rect.get_height() / 2),
                    xytext=(4, 0),
                    textcoords="offset points",
                    ha='left', va='center', fontsize=10, color='black')

autolabel(rects_muj)
autolabel(rects_hom)

# 9. Limpieza visual (quitar bordes que no se necesitan)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.get_xaxis().set_ticks([])
ax.tick_params(axis='y', length=0)

plt.title('Personas usuarias con mayor riesgo de ser vÃ­ctimas de\nviolencia digital a travÃ©s de la Internet, desagregada por sexo', 
          fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()

# 10. Guardar la imagen final
plt.savefig(PROJECT_ROOT / "output" / "figura_f11.png", dpi=300)
print("Â¡Listo! Figura F.11 generada dinÃ¡micamente.")
