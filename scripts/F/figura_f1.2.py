import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

# 1. Cargar datos
df = pd.read_csv(
    PROJECT_ROOT / "datos" / "F.1.2" / "tr_endutih_usuarios_anual_2023.csv",
    low_memory=False
)
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 2. Filtro base
df_int = df[(df['P7_1'] == 1) & (df['EDAD'] >= 6)].copy()

# Gobierno: OR de las 4 sub-preguntas
df_int['GOB'] = (
    (df_int['P7_35_1'] == 1) | (df_int['P7_35_2'] == 1) |
    (df_int['P7_35_3'] == 1) | (df_int['P7_35_4'] == 1)
).astype(int)

# 3. Totales por sexo
usuarios_sexo = df_int.groupby('SEXO')['FAC_PER'].sum()
tot_m = usuarios_sexo.get(2, 1)
tot_h = usuarios_sexo.get(1, 1)

# 4. Mapeo actividades
actividades = {
    'PelÃ­culas, series y otros\naudiovisuales gratuitos\n(YouTube)':           'P7_13_3',
    'Escuchar mÃºsica gratis\n(Spotify, Google music,\netcÃ©tera)':              'P7_13_4',
    'PelÃ­culas, series y otros\naudiovisuales de pago\n(Netflix, OTT, etc.)': 'P7_13_2',
    'Leer periÃ³dicos,\nrevistas o libros':                                     'P7_13_1',
    'Compras\npor Internet':                                                   'P7_21',
    'InteracciÃ³n con\nel gobierno':                                            'GOB',
    'Jugar en lÃ­nea':                                                          'P7_13_5',
    'Pagos por Internet':                                                      'P7_28',
    'Uso de la banca\nelectrÃ³nica':                                            'P7_33',
    'TV en web (canales\nabiertos por Internet)':                              'P7_13_7',
    'Ventas por Internet':                                                     'P7_19',
    'Radio AM y FM':                                                           'P7_18_1',
}

rows = []
for nombre, col in actividades.items():
    sub = df_int[df_int[col] == 1].groupby('SEXO')['FAC_PER'].sum()
    m = round(sub.get(2, 0) / tot_m * 100)
    h = round(sub.get(1, 0) / tot_h * 100)
    rows.append({'Actividad': nombre, 'Mujeres': m, 'Hombres': h})

data = pd.DataFrame(rows)

# 5. Figura
COLOR_M  = '#E8734A'   # naranja/salmÃ³n â€” mujeres
COLOR_H  = '#3A7DBF'   # azul â€” hombres
COLOR_BG = '#F5F7FA'
COLOR_CARD = '#FFFFFF'

# Crear grafica
fig = plt.figure(figsize=(20, 14), facecolor=COLOR_BG)
fig.suptitle(
    'Figura F.1. Actividades realizadas en Internet',
    fontsize=16, fontweight='bold', color='#1A1A2E', y=0.97
)

# Encabezado: usuarios totales
ax_header = fig.add_axes([0.05, 0.83, 0.90, 0.10])
ax_header.set_facecolor('#E8EEF5')
ax_header.set_xlim(0, 1)
ax_header.set_ylim(0, 1)
ax_header.axis('off')

ax_header.text(0.50, 0.80, 'Usuarios de Internet',
               ha='center', va='top', fontsize=13, fontweight='bold', color='#1A1A2E')

# Mujeres
ax_header.text(0.28, 0.55, f'{tot_m:,.0f}',
               ha='center', va='center', fontsize=18, fontweight='bold', color=COLOR_M)
ax_header.text(0.28, 0.18, 'Mujeres\n(81% del total de mujeres â‰¥6 aÃ±os)',
               ha='center', va='center', fontsize=9, color='#555555')

# Hombres
ax_header.text(0.72, 0.55, f'{tot_h:,.0f}',
               ha='center', va='center', fontsize=18, fontweight='bold', color=COLOR_H)
ax_header.text(0.72, 0.18, 'Hombres\n(81% del total de hombres â‰¥6 aÃ±os)',
               ha='center', va='center', fontsize=9, color='#555555')

# Separador
ax_header.axvline(0.50, ymin=0.1, ymax=0.9, color='#CCCCCC', lw=1)

# Tarjetas de actividades
n_cols = 6
n_rows = 2
cards = data.values.tolist()   # [nombre, %M, %H]

# Layout: 2 filas x 6 columnas
left_margin  = 0.03
bottom_start = 0.06
card_w = 0.152
card_h = 0.34
h_gap  = 0.012
v_gap  = 0.04

for idx, (nombre, m, h) in enumerate(cards):
    row = idx // n_cols
    col = idx  % n_cols

    x = left_margin + col * (card_w + h_gap)
    y = bottom_start + (n_rows - 1 - row) * (card_h + v_gap)

    ax = fig.add_axes([x, y, card_w, card_h])
    ax.set_facecolor(COLOR_CARD)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Borde de tarjeta
    for spine_pos in ['left', 'right', 'top', 'bottom']:
        ax.spines[spine_pos].set_visible(True)
        ax.spines[spine_pos].set_color('#DDDDDD')
        ax.spines[spine_pos].set_linewidth(0.8)

    # Título de actividad
    ax.text(0.50, 0.95, nombre,
            ha='center', va='top', fontsize=7.5, color='#333333',
            multialignment='center', linespacing=1.3)

    # Mujeres
    ax.text(0.22, 0.42, 'Mujeres', ha='center', va='bottom',
            fontsize=7, color='#666666')
    ax.text(0.22, 0.38, f'{m}%', ha='center', va='top',
            fontsize=20, fontweight='bold', color=COLOR_M)

    # Hombres
    ax.text(0.78, 0.42, 'Hombres', ha='center', va='bottom',
            fontsize=7, color='#666666')
    ax.text(0.78, 0.38, f'{h}%', ha='center', va='top',
            fontsize=20, fontweight='bold', color=COLOR_H)

    # Mini barra comparativa
    bar_y   = 0.10
    bar_h_r = 0.07
    bar_max = 100

    # Fondo
    ax.add_patch(mpatches.FancyBboxPatch(
        (0.05, bar_y), 0.90, bar_h_r,
        boxstyle='round,pad=0', facecolor='#EEEEEE', edgecolor='none'))

    # Barra mujeres (izquierda, naranja)
    w_m = 0.45 * (m / bar_max)
    ax.add_patch(mpatches.FancyBboxPatch(
        (0.05, bar_y), w_m, bar_h_r,
        boxstyle='round,pad=0', facecolor=COLOR_M, edgecolor='none', alpha=0.85))

    # Barra hombres (derecha, azul)
    w_h = 0.45 * (h / bar_max)
    ax.add_patch(mpatches.FancyBboxPatch(
        (0.50, bar_y), w_h, bar_h_r,
        boxstyle='round,pad=0', facecolor=COLOR_H, edgecolor='none', alpha=0.85))

# Leyenda y fuente
patch_m = mpatches.Patch(color=COLOR_M, label='Mujeres')
patch_h = mpatches.Patch(color=COLOR_H, label='Hombres')
fig.legend(handles=[patch_m, patch_h],
           loc='lower center', ncol=2,
           fontsize=9, frameon=False, bbox_to_anchor=(0.5, 0.005))

fig.text(
    0.05, 0.01,
    'Fuente: IFT con datos de la ENDUTIH 2023, del INEGI.\n'
    'Nota: Los porcentajes se calculan respecto del total de usuarios de Internet de cada sexo. '
    'Usuarios = personas de 6 aÃ±os o mÃ¡s.',
    fontsize=7, color='#777777', va='bottom'
)

# Guardar
plt.savefig('output/Figura_F1.2.png', dpi=150, bbox_inches='tight',
            facecolor=COLOR_BG) 
print("âœ…  Guardado: output/Figura_F1.2.png")
plt.show()
