import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import numpy as np

print("Cargando la base de datos de Internet Fijo...")
# 1. Cargar datos
df = pd.read_excel(PROJECT_ROOT / "datos" / "F.15" / "Tercera Encuesta 2023_Int&TV.xlsx")

# 2. Factor de expansión
w_col = 'Factor de ExpansiÃ³n Final Normalizado que considera calibraciÃ³n (post-estratificaciÃ³n) por sexo y grupos de edad 5 (redondeos corregidos) (a cifras del Censo INEGI, 2020)'
df[w_col] = pd.to_numeric(df[w_col], errors='coerce')

# 3. Filtrar Usuarios de Internet Fijo
col_internet = 'De la siguiente lista de servicios, Â¿podrÃ­a decirme cuÃ¡les tiene contratados o cuenta con ellos en su hogar? ConexiÃ³n a Internet fijo en su hogar (incluye conexiÃ³n Wi-Fi)'
df_internet = df[df[col_internet] == 'SÃ­'].copy()

# 4. Suma de Pesos Poblacionales Totales y por Sexo
total_w = df_internet[w_col].sum()
w_hombres = df_internet[df_internet['GÃ©nero'] == 'Hombre'][w_col].sum()
w_mujeres = df_internet[df_internet['GÃ©nero'] == 'Mujer'][w_col].sum()

# 5. Mapeo de columnas con el texto exacto a mostrar en la gráfica
label_mapping = {
    'Evitar compartir informaciÃ³n personal': 'Evitar compartir\ninformaciÃ³n\npersonal',
    'Evitar compartir contraseÃ±as de sus dispositivos y/o aplicaciones': 'Evitar compartir\ncontraseÃ±as de sus\ndispositivos y\naplicaciones',
    'Revisar un perfil antes de aceptarlo': 'Revisar un perfil\nantes de aceptarlo',
    'Ser mÃ¡s precavido al abrir links o archivos recibidos': 'Ser mÃ¡s precavido (a)\nal abrir links\no archivos recibidos',
    'Evitar subir informaciÃ³n donde sea fÃ¡cil ubicarle a usted o a su familia (ubicaciÃ³n, fotos y/o videos)': 'Evitar subir informaciÃ³n\ndonde sea fÃ¡cil ubicarte\na usted o a su familia\n(ubicaciÃ³n, fotos y/o\nvideos)',
    'Redes sociales privadas solo para familiares y/o amistades': 'Redes sociales\nprivadas solo para\nfamiliares y/o\namistades',
    'Publicar fotos y/o videos con restricciones para no recibir acoso y evitar comentarios': 'Publicar fotos y/o\nvideos con restricciones\npara no recibir\nacoso y evitar\ncomentarios',
    'Cuestionarse sobre el contenido que publicarÃ¡': 'Cuestionarse sobre\nel contenido que\npublicarÃ¡',
    'Evitar ser muy activo en redes sociales (Limitar publicaciones y/o no interactuar en redes sociales)': 'Evitar ser muy activo (a)\nen redes sociales\n(limitar publicaciones y\nno interactuar en\nredes sociales)',
    'Comentar con otras personas sobre lo que sucede y ve en redes sociales': 'Comentar con\notras personas\nsobre lo que\nsucede y ves en\nredes sociales'
}

# Solo seleccionamos las columnas de esta batería de preguntas
cols_acciones = [col for col in df.columns if 'Â¿CuÃ¡les de las siguientes acciones realiza para protegerse o prevenir' in col]

# Limpiamos respuestas de Ninguna , Otro y Ns/Nc que no aparecen en la gráfica
cols_acciones = [c for c in cols_acciones if 'Ninguna' not in c and 'Otro' not in c and 'Ns/Nc' not in c]

# 6. Cálculo dinámico iterando sobre las acciones
results_gen, results_muj, results_hom, labels = [], [], [], []

for col in cols_acciones:
    name_raw = col.split('? ')[-1]

    if name_raw in label_mapping:
        labels.append(label_mapping[name_raw])

        # Filtramos quiénes contestaron Sí a esta acción específica
        mask_si = df_internet[col].apply(lambda x: str(x).strip().lower() == 'sÃ­')
        df_si = df_internet[mask_si]

        # Ponderadores
        w_si_total = df_si[w_col].sum()
        w_si_hom = df_si[df_si['GÃ©nero'] == 'Hombre'][w_col].sum()
        w_si_muj = df_si[df_si['GÃ©nero'] == 'Mujer'][w_col].sum()

        # Porcentajes matemáticos exactos
        results_gen.append((w_si_total / total_w) * 100)
        results_muj.append((w_si_muj / w_mujeres) * 100)
        results_hom.append((w_si_hom / w_hombres) * 100)

# 7. Graficación de Barras Agrupadas Verticales
fig, ax = plt.subplots(figsize=(16, 7))

x = np.arange(len(labels))
width = 0.25 # Grosor de cada barra

# Dibujar las 3 barras por categoría
rects1 = ax.bar(x - width, results_gen, width, label='General', color='#E0E0E0') # Gris
rects2 = ax.bar(x, results_muj, width, label='Mujeres', color='#f48fb1') # Rosa claro
rects3 = ax.bar(x + width, results_hom, width, label='Hombres', color='#c2185b') # Rosa fuerte

# 8. Diseño y Tipografía
ax.set_ylabel('Porcentaje', fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=90, ha='center', fontsize=9) # Rotamos a 90Â° para que quepan
ax.set_ylim(0, 110) # Damos margen hasta 110 para que quepan los textos sobre las barras

# Eje Y en formato de Porcentaje
ax.set_yticks(np.arange(0, 101, 10))
ax.set_yticklabels([f'{int(tick)}%' for tick in ax.get_yticks()], fontsize=10)

ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.6), ncol=3, frameon=False, fontsize=11)

# Función para poner el porcentaje encima de la barra girado a 90 grados
def autolabel(rects, fontsize=8):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=fontsize, rotation=90)

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

# 9. Limpieza de bordes
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(axis='y', length=0)

plt.title('Acciones realizadas por las personas usuarias para protegerse o prevenir la\nviolencia digital a travÃ©s de Internet (por sexo)', 
          fontsize=14, fontweight='bold', pad=20)

# Ajustar espacio inferior debido a las etiquetas largas
plt.subplots_adjust(bottom=0.45) 
# Guardar salida
plt.savefig(PROJECT_ROOT / "output" / "figura_f15.png", dpi=300, bbox_inches='tight')
print("Â¡GrÃ¡fica F.15 lista!")
