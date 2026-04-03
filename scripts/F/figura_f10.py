import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]

print("Cargando y procesando la base de datos...")
# 1. Cargar datos
df = pd.read_excel(PROJECT_ROOT / "datos" / "F.10" / "Tercera Encuesta 2023_Int&TV.xlsx")

# 2. Definir columnas clave
# Columna del ponderador (peso de la encuesta para representar a nivel nacional)
w_col = 'Factor de Expansión Final Normalizado que considera calibración (post-estratificación) por sexo y grupos de edad 5 (redondeos corregidos) (a cifras del Censo INEGI, 2020)'
df[w_col] = pd.to_numeric(df[w_col], errors='coerce')

# Columna para filtrar únicamente a quienes tienen Internet Fijo
col_internet = 'De la siguiente lista de servicios, ¿podría decirme cuáles tiene contratados o cuenta con ellos en su hogar? Conexión a Internet fijo en su hogar (incluye conexión Wi-Fi)'

# 3. Filtrar a los usuarios de Internet Fijo y calcular el peso total
df_internet = df[df[col_internet] == 'Sí'].copy()
total_weight = df_internet[w_col].sum()

# 4. Diccionario para mapear el final del nombre de la columna con el texto exacto que pide la gráfica
label_mapping = {
    'Menores de edad': 'Niños, niñas y\nadolescentes',
    'Mujeres': 'Mujeres',
    'Todas las personas son vulnerables': 'Todas las personas\nson vulnerables',
    'Adultos mayores / Personas de la tercera edad': 'Personas adultas\nmayores',
    'Personas con discapacidad': 'Personas con\ndiscapacidad',
    'Integrantes de la comunidad LGBTIQ+': 'Personas de la\ncomunidad LGBTIQ+',
    'Personas indígenas': 'Personas indígenas',
    'Hombres': 'Hombres',
    'Personas negras o afrodescendientes': 'Personas\nafrodescendientes'
}

# 5. Calcular porcentajes dinámicamente
resultados_dinamicos = {}
violencia_cols = [col for col in df.columns if 'mayor riesgo' in col.lower()]

for col in violencia_cols:
    if '? ' in col:
        # Extraer a qué categoría pertenece esta columna en específico
        category = col.split('? ')[1] 

        # Si es una de las categorías a graficar, calculamos su porcentaje
        if category in label_mapping:
            label = label_mapping[category]

            # Sumar ponderador solo donde contestaron Sí
            mask = df_internet[col].apply(lambda x: str(x).strip().lower() == 'sí')
            weighted_sum = df_internet.loc[mask, w_col].sum()

            # Obtener el porcentaje matemático
            pct = (weighted_sum / total_weight) * 100
            resultados_dinamicos[label] = pct

# 6. Ordenar resultados de mayor a menor como en el anuario
resultados_ordenados = sorted(resultados_dinamicos.items(), key=lambda item: item[1], reverse=True)

# Separar en dos listas para graficar
categorias = [item[0] for item in resultados_ordenados]
valores = [item[1] for item in resultados_ordenados]

# Invertir orden porque el formato barh de Matplotlib dibuja de abajo hacia arriba
categorias_rev = categorias[::-1]
valores_rev = valores[::-1]

# 7. Graficar con diseño idéntico al reporte
fig, ax = plt.subplots(figsize=(10, 6))

# Determinar colores dinámicos:
# Si la categoría está entre los primeros dos lugares (índice 0 o 1 de la lista original), es rosa fuerte
colores = ['#c2185b' if cat in categorias[:2] else '#f48fb1' for cat in categorias_rev]

barras = ax.barh(categorias_rev, valores_rev, color=colores, height=0.6)

# Etiquetas de texto en la punta de cada barra
for barra in barras:
    ancho = barra.get_width()
    ax.annotate(f'{ancho:.1f}%',
                xy=(ancho, barra.get_y() + barra.get_height() / 2),
                xytext=(5, 0),
                textcoords="offset points",
                ha='left', va='center', fontsize=11, fontweight='bold', color='black')

# Formato limpio de gráfica
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.get_xaxis().set_ticks([])
ax.tick_params(axis='y', length=0, labelsize=11)

plt.title('Personas usuarias con mayor riesgo de ser víctimas\nde Violencia Digital a través de Internet', 
          fontsize=14, fontweight='bold', pad=20)
fig.suptitle('Figura F.10. Principales razones de los usuarios de Internet para no utilizar servicios de gobierno', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()

# 8. Exportar
plt.savefig(PROJECT_ROOT / "output" / "figura_f10.png", dpi=300)
print("¡Listo! Gráfica generada y calculada directo del CSV.")
