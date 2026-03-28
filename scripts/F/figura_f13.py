import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import numpy as np

print("Cargando base de datos de TelefonÃ­a MÃ³vil...")
# 1. Cargar la base de Telefonía Móvil
df_movil = pd.read_excel(PROJECT_ROOT / "datos" / "F.13" / "Tercera Encuesta 2023_Tel M\u00f3vil.xlsx")

# 2. Definir factor de expansión y filtro de usuario
w_col = 'Calibrador (post-estratificaciÃ³n) final que considera distribuciÃ³n de lÃ­neas telefÃ³nicas mÃ³viles por entidad federativa y poblaciÃ³n por grupos de edad 5 (redondeos corregidos)'
df_movil[w_col] = pd.to_numeric(df_movil[w_col], errors='coerce')

user_col = 'Â¿Es usted\xa0el usuario habitual de esta lÃ­nea de telÃ©fono mÃ³vil o celular?'
df_filtered = df_movil[df_movil[user_col].astype(str).str.strip().str.lower() == 'sÃ­'].copy()

# 3. Pesos totales divididos por género (Hombre/Mujer)
w_hombres = df_filtered[df_filtered['GÃ©nero'] == 'Hombre'][w_col].sum()
w_mujeres = df_filtered[df_filtered['GÃ©nero'] == 'Mujer'][w_col].sum()

# 4. Mapeo de categorías con los nombres del PDF y su orden de aparición
label_mapping = {
    'Menores de edad': 'NiÃ±os, niÃ±as y\nadolescentes',
    'Adultos mayores / Personas de la tercera edad': 'Personas adultas\nmayores',
    'Mujeres': 'Mujeres',
    'Parientes (familiares)': 'Parientes\n(familiares)',
    'Hombres': 'Hombres',
    'Personas con discapacidad': 'Personas con\ndiscapacidad',
    'Todas las personas son vulnerables': 'Todas las personas\nson vulnerables'
}

pdf_order = [
    'NiÃ±os, niÃ±as y\nadolescentes',
    'Personas adultas\nmayores',
    'Mujeres',
    'Parientes\n(familiares)',
    'Hombres',
    'Personas con\ndiscapacidad',
    'Todas las personas\nson vulnerables'
]

# 5. Cálculo dinámico cruzando Violencia vs Género
violencia_cols = [c for c in df_movil.columns if 'mayor riesgo' in c.lower()]
results_h = {}
results_m = {}

for col in violencia_cols:
    if '? ' in col:
        categoria = col.split('? ')[1]
        if categoria in label_mapping:
            label = label_mapping[categoria]

            # Filtramos los que respondieron Sí a esta categoría
            mask_si = df_filtered[col].apply(lambda x: str(x).strip().lower() == 'sÃ­')
            df_si = df_filtered[mask_si]

            # Sumamos los pesos segmentando por género
            w_si_h = df_si[df_si['GÃ©nero'] == 'Hombre'][w_col].sum()
            w_si_m = df_si[df_si['GÃ©nero'] == 'Mujer'][w_col].sum()

            # Calculamos los porcentajes (Suma parcial / Suma total del género)
            results_h[label] = (w_si_h / w_hombres) * 100
            results_m[label] = (w_si_m / w_mujeres) * 100

# Ordenamos e invertimos las listas para la gráfica (Matplotlib dibuja de abajo arriba)
categorias_rev = pdf_order[::-1]
valores_h = [results_h[cat] for cat in categorias_rev]
valores_m = [results_m[cat] for cat in categorias_rev]

# 6. Graficar barras agrupadas
fig, ax = plt.subplots(figsize=(10, 8))

y = np.arange(len(categorias_rev))
height = 0.35

# Barras de Hombres (Rosa fuerte) y Mujeres (Rosa claro)
rects_muj = ax.barh(y - height/2, valores_m, height, label='Mujeres', color='#f48fb1')
rects_hom = ax.barh(y + height/2, valores_h, height, label='Hombres', color='#c2185b')

# 7. Formato de las etiquetas y leyendas
ax.set_yticks(y)
ax.set_yticklabels(categorias_rev, fontsize=11)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False, fontsize=11)

# Función para poner el % exacto junto a cada barra
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

# 8. Limpiar visualmente la gráfica
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.get_xaxis().set_ticks([])
ax.tick_params(axis='y', length=0)

plt.title('Personas usuarias con mayor riesgo de ser vÃ­ctimas de violencia\ndigital a travÃ©s del telÃ©fono mÃ³vil. Por sexo', 
          fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()

# 9. Guardar la figura
plt.savefig(PROJECT_ROOT / "output" / "figura_f13.png", dpi=300)
print("Â¡GrÃ¡fica F.13 generada exitosamente!")
