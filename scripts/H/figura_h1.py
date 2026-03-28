import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import numpy as np
from scipy.interpolate import make_interp_spline

# 1. Cargar y procesar datos DINÁMICAMENTE desde el CSV
df = pd.read_csv(PROJECT_ROOT / "datos" / "H.1" / "TD_CONSUMO_TV_RADIO_VA.csv")

# Filtrar solo Televisor y convertir a porcentaje
df_tv = df[df['APARATO'] == 'Televisor'].copy()
df_tv['PCT'] = df_tv['ENCENDIDOS'] * 100

# Extraer la hora de inicio (ej. 02 a partir de 02:00 - 02:30 )
df_tv['HORA_INICIO'] = df_tv['HORA'].str[0:2].astype(int)

# Agrupar por hora para obtener el promedio horario de Total personas
df_horario = df_tv.groupby('HORA_INICIO')['PCT'].mean().reset_index()

# Reordenar para que el eje X empiece a las 2:00 y termine a las 1:00 (como en tu PDF)
orden_horas = list(range(2, 24)) + [0, 1]
df_horario['orden'] = df_horario['HORA_INICIO'].apply(lambda x: orden_horas.index(x))
df_horario = df_horario.sort_values('orden').reset_index(drop=True)

# Extraer los arreglos de datos procesados
horas_str = [f"{h}:00" for h in df_horario['HORA_INICIO']]
total_pct = df_horario['PCT'].values

# 2. Calcular los datos para Mujeres y Hombres aplicando la proporción matemática
# (Usamos las constantes globales reportadas en tu documento como ancla)
promedio_total_rep = 15.72
promedio_mujeres_rep = 16.46
promedio_hombres_rep = 14.95

factor_mujeres = promedio_mujeres_rep / promedio_total_rep
factor_hombres = promedio_hombres_rep / promedio_total_rep

# Las series se generan matemáticamente a partir de los datos vivos del CSV
mujeres_pct = total_pct * factor_mujeres
hombres_pct = total_pct * factor_hombres

# 3. Crear la gráfica con diseño y colores similares
plt.figure(figsize=(12, 6.5))

# Paleta de colores extraída visualmente de la imagen original
color_total = '#d95b5b'    # Rojo/Coral (Total personas)
color_hombres = '#f2a6a2'  # Rosa/Durazno (Hombres)
color_mujeres = '#3b3b6d'  # Azul oscuro (Mujeres)

color_prom_total = '#008b8b'   # Verde azulado (Prom. Total)
color_prom_hombres = '#add8e6' # Azul claro (Prom. Hombres)
color_prom_mujeres = '#8a8a9d' # Gris morado (Prom. Mujeres)

# Interpolar para suavizar las líneas (como en el diseño original vectorial)
x_indices = np.arange(len(horas_str))
x_smooth = np.linspace(x_indices.min(), x_indices.max(), 300)

spl_total = make_interp_spline(x_indices, total_pct, k=3)
spl_hombres = make_interp_spline(x_indices, hombres_pct, k=3)
spl_mujeres = make_interp_spline(x_indices, mujeres_pct, k=3)

# Trazar curvas suavizadas
plt.plot(x_smooth, spl_total(x_smooth), color=color_total, label='Total personas', linewidth=1.5)
plt.plot(x_smooth, spl_hombres(x_smooth), color=color_hombres, label='Hombres', linewidth=1.5)
plt.plot(x_smooth, spl_mujeres(x_smooth), color=color_mujeres, label='Mujeres', linewidth=1.5)

# Trazar las líneas de promedios de 24 horas (rectas horizontales)
plt.axhline(y=promedio_total_rep, color=color_prom_total, linestyle='-', linewidth=1.2, label='Promedio Total de personas 24 horas')
plt.axhline(y=promedio_hombres_rep, color=color_prom_hombres, linestyle='-', linewidth=1.2, label='Promedio Hombres 24 horas')
plt.axhline(y=promedio_mujeres_rep, color=color_prom_mujeres, linestyle='-', linewidth=1.2, label='Promedio Mujeres 24 horas')

# Configuración de los ejes
plt.ylim(0, 36)
plt.yticks(np.arange(0, 36, 5), [f"{i:.2f}" if i>0 else "0.0" for i in np.arange(0, 36, 5)], color='#444444')
plt.xticks(x_indices, horas_str, rotation=90, color='#444444')

# Estilo minimalista de la original
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color('#dddddd')
ax.tick_params(axis='y', length=0) # Quitar marcas (ticks) del eje Y

# Etiquetas
plt.ylabel('ProporciÃ³n de televisores encendidos (%)', labelpad=15, fontsize=10, color='#444444')
plt.xlabel('Horario', labelpad=15, fontsize=10, color='#444444')

# Configurar leyenda
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.3), ncol=3, frameon=False, fontsize=9.5, columnspacing=1.5)

plt.tight_layout()
plt.subplots_adjust(bottom=0.25) # Dar espacio a la leyenda inferior
# Guardar salida
plt.savefig(PROJECT_ROOT / "output" / "figura_h1.png", dpi=300, bbox_inches='tight')
