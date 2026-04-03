import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# 1. Cargar y preparar datos
ruta_datos = PROJECT_ROOT / "datos" / "F.1.1" / "tr_endutih_usuarios_anual_2023.csv"
print("Cargando la base de datos y calculando valores reales...")
# Cargar datos
df = pd.read_csv(ruta_datos, low_memory=False)
df.columns = df.columns.str.upper()

# 2. Filtrar el Universo Base (Usuarios de Internet mediante celular, 6+ años)
base_celular = df[(pd.to_numeric(df['EDAD'], errors='coerce') >= 6) & 
                  (pd.to_numeric(df['P7_1'], errors='coerce') == 1) &
                  (pd.to_numeric(df['P7_6_4'], errors='coerce') == 1)]

# Denominadores poblacionales base calculados
totales_universo = base_celular.groupby('SEXO')['FAC_PER'].sum()
total_hombres = totales_universo.get(1, 0)
total_mujeres = totales_universo.get(2, 0)

# 3. Diccionario de actividades (Actividad : Columna en ENDUTIH)
# Usamos las que verificamos y aproximaciones para las demás
diccionario_actividades = {
    'Mensajería instantánea': 'P7_16_9',       # (Aproximación)
    'Descargaron aplicaciones': 'P7_11_2',     # (Aproximación)
    'Acceder a redes sociales': 'P7_35_3',     # MATCH EXACTO
    'Contenidos de audio y video': 'P7_17_2',  # MATCH EXACTO
    'Jugar': 'P7_33',                          # (Aproximación)
    'Adquirir bienes o servicios': 'P7_34_2',  # MATCH EXACTO
    'Tránsito y navegación': 'P7_32_1',        # (Aproximación)
    'Acceder a Banca Móvil': 'P7_22_2',        # (Aproximación)
    'Editar fotos o videos': 'P7_36_3'         # (Aproximación)
}

# 4. Cálculo dinámico de porcentajes
nombres_actividades = []
pct_mujeres = []
pct_hombres = []

for actividad, columna in diccionario_actividades.items():
    if columna in base_celular.columns:
        # Filtramos a los que dijeron Sí (1) en la actividad
        positivos = base_celular[pd.to_numeric(base_celular[columna], errors='coerce') == 1]
        sum_pos = positivos.groupby('SEXO')['FAC_PER'].sum()

        # Calculamos el porcentaje real vs el universo
        h_pct = round((sum_pos.get(1, 0) / total_hombres) * 100)
        m_pct = round((sum_pos.get(2, 0) / total_mujeres) * 100)

        nombres_actividades.append(actividad)
        pct_hombres.append(h_pct)
        pct_mujeres.append(m_pct)

# Invertimos las listas para que el orden en la gráfica sea de arriba hacia abajo
nombres_actividades.reverse()
pct_mujeres.reverse()
pct_hombres.reverse()

# 5. Generar la Gráfica Visual
import matplotlib.patches as patches
import textwrap
import os

# Crear grafica
fig, ax = plt.subplots(figsize=(16, 9))
ax.axis('off')
fig.patch.set_facecolor('#f4f4f4')

def get_pct(name):
    if name in nombres_actividades:
        idx = nombres_actividades.index(name)
        return pct_mujeres[idx], pct_hombres[idx]
    return 0, 0

def draw_panel(x, y, w, h, title, icon, pct_m, pct_h, bg_color='#FCECE9'):
    # Fondo del panel
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.03", 
                                 linewidth=0, facecolor=bg_color, edgecolor=None)
    ax.add_patch(box)

    # Icono principal circular (simulado)
    circle = patches.Circle((x + 0.04, y + h - 0.04), radius=0.04, color='white', zorder=2)
    ax.add_patch(circle)
    circle_shadow = patches.Circle((x + 0.042, y + h - 0.042), radius=0.04, color='gray', alpha=0.1, zorder=1)
    ax.add_patch(circle_shadow)

    ax.text(x + 0.04, y + h - 0.04, icon, ha='center', va='center', fontsize=22, zorder=3, fontfamily='Segoe UI Emoji')

    # Título
    wrapped_title = "\n".join(textwrap.wrap(title, width=28))
    ax.text(x + 0.10, y + h - 0.04, wrapped_title, ha='left', va='center', fontsize=11, fontweight='bold', color='#1F3864')

    # Mujeres
    ax.text(x + 0.12, y + 0.08, 'ðŸ‘© Mujeres', ha='center', va='center', fontsize=10, color='#1F3864', fontfamily='Segoe UI Emoji')
    ax.text(x + 0.12, y + 0.03, f'{pct_m}%', ha='center', va='center', fontsize=24, fontweight='bold', color='#1F3864')

    # Hombres
    ax.text(x + w - 0.10, y + 0.08, 'ðŸ‘¨ Hombres', ha='center', va='center', fontsize=10, color='#1F3864', fontfamily='Segoe UI Emoji')
    ax.text(x + w - 0.10, y + 0.03, f'{pct_h}%', ha='center', va='center', fontsize=24, fontweight='bold', color='#1F3864')

# Área superior: Título General
ax.text(0.02, 0.95, "ðŸ”´ Figura F.1. Actividades en Smartphone, Internet, computadora y uso de redes sociales", 
        fontsize=14, color='#1F3864', fontweight='bold', fontfamily='Segoe UI Emoji')

# Panel izquierdo principal
box_main = patches.FancyBboxPatch((0.02, 0.72), 0.22, 0.18, boxstyle="round,pad=0.02,rounding_size=0.04", 
                             linewidth=0, facecolor='white')
ax.add_patch(box_main)
ax.text(0.13, 0.81, "Aplicaciones instaladas\nmediante Smartphone", ha='center', va='center', 
        fontsize=16, fontweight='bold', color='#1F3864', linespacing=1.5)

# Panel superior Centro (Usuarios totales)
box_tot = patches.FancyBboxPatch((0.26, 0.70), 0.42, 0.22, boxstyle="round,pad=0.02,rounding_size=0.03", 
                             linewidth=0, facecolor='#FCECE9')
ax.add_patch(box_tot)

ax.text(0.47, 0.88, "ðŸ“± Usuarios de Internet mediante Smartphone", ha='center', va='center', 
        fontsize=12, fontweight='bold', color='#1F3864', fontfamily='Segoe UI Emoji')

ax.text(0.33, 0.81, 'ðŸ‘© Mujeres', ha='center', va='center', fontsize=10, color='#1F3864', fontfamily='Segoe UI Emoji')
ax.text(0.33, 0.75, f"{int(total_mujeres):,}", ha='center', va='center', fontsize=22, fontweight='bold', color='#1F3864')
ax.text(0.33, 0.71, "(75% con respecto al total\nde mujeres de 6 años o más)", ha='center', va='center', fontsize=8, color='#666666')

ax.text(0.61, 0.81, 'ðŸ‘¨ Hombres', ha='center', va='center', fontsize=10, color='#1F3864', fontfamily='Segoe UI Emoji')
ax.text(0.61, 0.75, f"{int(total_hombres):,}", ha='center', va='center', fontsize=22, fontweight='bold', color='#1F3864')
ax.text(0.61, 0.71, "(73% con respecto al total\nde hombres de 6 años o más)", ha='center', va='center', fontsize=8, color='#666666')

# Panel superior Derecho
pm, ph = get_pct('Descargaron aplicaciones')
draw_panel(0.70, 0.70, 0.28, 0.22, "Descargaron aplicaciones", "ðŸ“¥", pm, ph, bg_color='#FCECE9')

# Paneles Fila del Medio
w_m, h_m = 0.31, 0.22
y_mid = 0.43
pm, ph = get_pct('Mensajería instantánea')
draw_panel(0.02, y_mid, w_m, h_m, "Mensajería instantánea\n(WhatsApp, Messenger, Twitter, etcétera)", "ðŸ’¬", pm, ph)

pm, ph = get_pct('Acceder a redes sociales')
draw_panel(0.35, y_mid, w_m, h_m, "Acceder a redes sociales\n(Facebook, Instagram, etcétera)", "ðŸ‘¥", pm, ph)

pm, ph = get_pct('Contenidos de audio y video')
draw_panel(0.68, y_mid, 0.30, h_m, "Contenidos de audio y video\n(YouTube, Spotify, etc.)", "ðŸŽµ", pm, ph)

# Paneles Fila Inferior
w_b, h_b = 0.18, 0.25
y_bot = 0.10
spacing = 0.016

pm, ph = get_pct('Jugar')
draw_panel(0.02, y_bot, w_b, h_b, "Jugar (Pokémon go, Candy Crush)", "ðŸŽ®", pm, ph)

pm, ph = get_pct('Tránsito y navegación')
draw_panel(0.02 + 1*(w_b+spacing), y_bot, w_b, h_b, "Tránsito y navegación\n(Google Maps)", "ðŸ—ºï¸", pm, ph)

pm, ph = get_pct('Adquirir bienes o servicios')
draw_panel(0.02 + 2*(w_b+spacing), y_bot, w_b, h_b, "Adquirir bienes/servicios (Uber, Rappi)", "ðŸ›ï¸", pm, ph)

pm, ph = get_pct('Acceder a Banca Móvil')
draw_panel(0.02 + 3*(w_b+spacing), y_bot, w_b, h_b, "Acceder a Banca Móvil (BBVA, Banamex)", "ðŸ¦", pm, ph)

pm, ph = get_pct('Editar fotos o videos')
draw_panel(0.02 + 4*(w_b+spacing), y_bot, w_b, h_b, "Editar fotos o videos", "ðŸ“¸", pm, ph)

# Fuente al pie
ax.text(0.02, 0.04, "Fuente: IFT con datos de la ENDUTIH 2023, del INEGI.", fontsize=9, color='#666666')
ax.text(0.02, 0.01, "Nota: Todos los usuarios se refieren a personas de 6 años o más.", fontsize=9, color='#666666')

# Guardar y mostrar
output_dir = PROJECT_ROOT / "output"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "figura_f1.1.png")
# Guardar salida
fig.suptitle('Figura F.1.1. Actividades en Smartphone, Internet, computadora y uso de redes sociales', fontsize=14, fontweight='bold', y=1.02)
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
print(f"Infografía guardada en: {output_path}")

plt.show()
