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
df = pd.read_csv('Tercera Encuesta 2023_Int&TV.xlsx - Tercera Encuesta 2023_Int&TV.csv', low_memory=False)

# 2. Factor de Expansión (Ponderador)
w_col = 'Factor de ExpansiÃ³n Final Normalizado que considera calibraciÃ³n (post-estratificaciÃ³n) por sexo y grupos de edad 5 (redondeos corregidos) (a cifras del Censo INEGI, 2020)'
df[w_col] = pd.to_numeric(df[w_col], errors='coerce')

# 3. Filtro para usuarios de Internet Fijo
col_internet = 'De la siguiente lista de servicios, Â¿podrÃ­a decirme cuÃ¡les tiene contratados o cuenta con ellos en su hogar? ConexiÃ³n a Internet fijo en su hogar (incluye conexiÃ³n Wi-Fi)'
df_internet = df[df[col_internet] == 'SÃ­'].copy()

# 4. Cálculo de ponderadores totales
total_w = df_internet[w_col].sum()
w_mujeres = df_internet[df_internet['GÃ©nero'] == 'Mujer'][w_col].sum()
w_hombres = df_internet[df_internet['GÃ©nero'] == 'Hombre'][w_col].sum()

# Función para obtener respuestas Sí de una acción
def get_mask(col_name):
    full_name = f'Independientemente de si ha sido o no vÃ­ctima de violencia en Internet, Â¿quÃ© harÃ­a si la experimentara o quÃ© hizo en caso de haberla experimentado? {col_name}'
    return df_internet[full_name].apply(lambda x: str(x).strip().lower() == 'sÃ­')

# Función para calcular los porcentajes General, Mujeres, Hombres
def get_pct(mask):
    w_t = df_internet.loc[mask, w_col].sum()
    w_m = df_internet.loc[mask & (df_internet['GÃ©nero'] == 'Mujer'), w_col].sum()
    w_h = df_internet.loc[mask & (df_internet['GÃ©nero'] == 'Hombre'), w_col].sum()
    return (w_t/total_w)*100, (w_m/w_mujeres)*100, (w_h/w_hombres)*100

# 5. Agrupación y Mapeo de Categorías (Lógica exacta del Anuario)
categories = [
    {
        'label': 'Denunciar ante la\nPolicÃ­a CibernÃ©tica',
        'mask': get_mask('Denunciar ante la PolicÃ­a CibernÃ©tica')
    },
    {
        'label': 'Denunciar a las autoridades\n(Ministerio PÃºblico, escolares\ny/o centro de trabajo, Seguridad\nPÃºblica, CNDH, SEDENA)',
        # Se agrupan TODAS las autoridades mencionadas
        'mask': get_mask('Denunciar ante el Ministerio PÃºblico') | 
                get_mask('Denunciar ante autoridades escolares/centro de trabajo') | 
                get_mask('Denunciar a Seguridad PÃºblica') | 
                get_mask('Denunciar ante la ComisiÃ³n Nacional de Derechos Humanos (CNDH)') | 
                get_mask('Reportarlo ante la SEDENA') | 
                get_mask('Denunciar/ Reportarlo (No especifica ante quÃ© autoridades o dÃ³nde harÃ­a la denuncia/reporte)')
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
        'label': 'Cerrar la cuenta\n(red social, correo\nelectrÃ³nico)',
        'mask': get_mask('Cerrar la cuenta (red social/correo electrÃ³nico)')
    },
    {
        'label': 'No hacer algo/ Hacer\ncaso omiso/ Ignorar',
        # Se agrupa Ignorar con Nada
        'mask': get_mask('No hacer caso/ Hacer caso omiso/ Ignorar') | get_mask('Nada')
    },
    {
        'label': 'Cambiar nÃºmero de\ntelÃ©fono',
        'mask': get_mask('Cambiar nÃºmero de telÃ©fono')
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
ax.set_ylim(0, 40) # LÃ­mite superior de 40% (PDF muestra hasta 35%)

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
print("Â¡Figura F.16 construida y validada!")
