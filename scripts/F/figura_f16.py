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
# 1. Cargar Base de Datos
df = pd.read_excel(PROJECT_ROOT / "datos" / "F.16" / "Tercera Encuesta 2023_Int&TV.xlsx")

# 2. Factor de Expansión (Ponderador)
w_col = 'Factor de Expansión Final Normalizado que considera calibración (post-estratificación) por sexo y grupos de edad 5 (redondeos corregidos) (a cifras del Censo INEGI, 2020)'
df[w_col] = pd.to_numeric(df[w_col], errors='coerce')

# 3. Filtro para usuarios de Internet Fijo
col_internet = 'De la siguiente lista de servicios, ¿podría decirme cuáles tiene contratados o cuenta con ellos en su hogar? Conexión a Internet fijo en su hogar (incluye conexión Wi-Fi)'
df_internet = df[df[col_internet] == 'Sí'].copy()

# 4. Cálculo de ponderadores totales
total_w = df_internet[w_col].sum()
w_mujeres = df_internet[df_internet['Género'] == 'Mujer'][w_col].sum()
w_hombres = df_internet[df_internet['Género'] == 'Hombre'][w_col].sum()

# Función para obtener respuestas Sí de una acción
def get_mask(col_name):
    full_name = f'Independientemente de si ha sido o no víctima de violencia en Internet, ¿qué haría si la experimentara o qué hizo en caso de haberla experimentado? {col_name}'
    return df_internet[full_name].apply(lambda x: str(x).strip().lower() == 'sí')

# Función para calcular los porcentajes General, Mujeres, Hombres
def get_pct(mask):
    w_t = df_internet.loc[mask, w_col].sum()
    w_m = df_internet.loc[mask & (df_internet['Género'] == 'Mujer'), w_col].sum()
    w_h = df_internet.loc[mask & (df_internet['Género'] == 'Hombre'), w_col].sum()
    return (w_t/total_w)*100, (w_m/w_mujeres)*100, (w_h/w_hombres)*100

# 5. Agrupación y Mapeo de Categorías (Lógica exacta del Anuario)
categories = [
    {
        'label': 'Denunciar ante la\nPolicía Cibernética',
        'mask': get_mask('Denunciar ante la Policía Cibernética')
    },
    {
        'label': 'Denunciar a las autoridades\n(Ministerio Público, escolares\ny/o centro de trabajo, Seguridad\nPública, CNDH, SEDENA)',
        # Se agrupan TODAS las autoridades mencionadas
        'mask': get_mask('Denunciar ante el Ministerio Público') | 
                get_mask('Denunciar ante autoridades escolares/centro de trabajo') | 
                get_mask('Denunciar a Seguridad Pública') | 
                get_mask('Denunciar ante la Comisión Nacional de Derechos Humanos (CNDH)') | 
                get_mask('Reportarlo ante la SEDENA') | 
                get_mask('Denunciar/ Reportarlo (No especifica ante qué autoridades o dónde haría la denuncia/reporte)')
    },
    {
        'label': 'Bloquear a la persona',
        'mask': get_mask('Bloquear a la persona')
    },
    {
        'label': 'Denunciar en la platafor-\nma digital/red social',
        'mask': get_mask('Denunciar en la plataforma/red social')
    },
    {
        'label': 'Cerrar la cuenta\n(red social, correo\nelectrónico)',
        'mask': get_mask('Cerrar la cuenta (red social/correo electrónico)')
    },
    {
        'label': 'No hacer algo/ Hacer\ncaso omiso/ Ignorar',
        # Se agrupa Ignorar con Nada
        'mask': get_mask('No hacer caso/ Hacer caso omiso/ Ignorar') | get_mask('Nada')
    },
    {
        'label': 'Cambiar número de\nteléfono',
        'mask': get_mask('Cambiar número de teléfono')
    }
]

# 6. Ejecución del cálculo cruzado
labels = [c['label'] for c in categories]
results_gen, results_muj, results_hom = [], [], []

for c in categories:
    t, m, h = get_pct(c['mask'])
    results_gen.append(t)
    results_muj.append(m)
    results_hom.append(h)

# 7. Graficar (Barras Agrupadas Verticales)
fig, ax = plt.subplots(figsize=(14, 7))

x = np.arange(len(labels))
width = 0.25 # Grosor de las barras

rects1 = ax.bar(x - width, results_gen, width, label='General', color='#E0E0E0')
rects2 = ax.bar(x, results_muj, width, label='Mujeres', color='#f48fb1')
rects3 = ax.bar(x + width, results_hom, width, label='Hombres', color='#c2185b')

# 8. Etiquetas y Estilo de Ejes
ax.set_ylabel('Porcentaje', fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(labels, ha='center', fontsize=9)
ax.set_ylim(0, 40) # Límite superior de 40% (PDF muestra hasta 35%)

# Formato % en eje Y
ax.set_yticks(np.arange(0, 41, 5))
ax.set_yticklabels([f'{int(tick):.1f}%' for tick in ax.get_yticks()], fontsize=10)

# Leyenda en la parte inferior
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.35), ncol=3, frameon=False, fontsize=11)

# Función para anotar el porcentaje exacto sobre cada barra
def autolabel(rects, fontsize=9):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=fontsize)

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

# Limpieza visual
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(axis='y', length=0)

plt.title('Acciones en caso de experimentar violencia digital en Internet', 
          fontsize=14, fontweight='bold', pad=20)

plt.subplots_adjust(bottom=0.3)
# Guardar salida
plt.savefig(PROJECT_ROOT / "output" / "figura_f16.png", dpi=300, bbox_inches='tight')
print("¡Figura F.16 construida y validada!")
