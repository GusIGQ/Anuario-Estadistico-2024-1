import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 1. Cargar los datos (sin hardcodear ningún número de resultados)
df_empleo = pd.read_csv(PROJECT_ROOT / "datos" / "F.2" / "TD_EMPLEO_SEXO_VA.csv", encoding='utf-8-sig')

# 2. Filtrar para el Año 2024 y el Trimestre 2 (junio)
df_2024_q2 = df_empleo[(df_empleo['ANIO'] == 2024) & (df_empleo['TRIM'] == 2)]

# 3. Agrupar por Sexo y sumar columnas de ambos sectores
res = df_2024_q2.groupby('SEXO')[['EMP_RADIO', 'EMP_TELECOM']].sum()

# 4. Extraer los valores dinámicamente de los resultados del dataframe
radio_mujeres = res.loc['Mujeres', 'EMP_RADIO']
radio_hombres = res.loc['Hombres', 'EMP_RADIO']
total_radio = radio_mujeres + radio_hombres

telecom_mujeres = res.loc['Mujeres', 'EMP_TELECOM']
telecom_hombres = res.loc['Hombres', 'EMP_TELECOM']
total_telecom = telecom_mujeres + telecom_hombres

# 5. Configurar la figura (1 fila, 2 columnas)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

# --- Gráfica 1: Radiodifusión ---
labels = ['Mujeres', 'Hombres']
sizes_radio = [radio_mujeres, radio_hombres]
# Colores intentando replicar la infografía
colors_radio = ['#2b6a9c', '#332b57'] 
explode = (0.05, 0) # Separación ligera de la rebanada

_, texts_r, autotexts_r = ax1.pie(
    sizes_radio, 
    explode=explode, 
    labels=labels, 
    colors=colors_radio, 
    autopct='%1.0f%%',
    startangle=180,
    textprops={'fontsize': 12, 'weight': 'bold'}
)
# Hacer los números de porcentaje blancos y más grandes
for text in autotexts_r:
    text.set_color('white') 
    text.set_fontsize(16)

ax1.set_title(f'Radiodifusión\nTotal de personas empleadas: {int(total_radio):,}', 
              fontsize=14, weight='bold', pad=20)

# --- Gráfica 2: Telecomunicaciones ---
sizes_telecom = [telecom_mujeres, telecom_hombres]
colors_telecom = ['#e68c85', '#ed4a57']

_, texts_t, autotexts_t = ax2.pie(
    sizes_telecom, 
    explode=explode, 
    labels=labels, 
    colors=colors_telecom, 
    autopct='%1.0f%%',
    startangle=180,
    textprops={'fontsize': 12, 'weight': 'bold'}
)
for text in autotexts_t:
    text.set_color('white')
    text.set_fontsize(16)

ax2.set_title(f'Telecomunicaciones\nTotal de personas empleadas: {int(total_telecom):,}', 
              fontsize=14, weight='bold', pad=20)

# Ajustar y guardar
fig.suptitle('Figura F.2. Empleo en los sectores de telecomunicaciones y radiodifusión por sexo', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
# Guardar salida
plt.savefig(PROJECT_ROOT / "output" / "figura_f2.png", dpi=300, bbox_inches='tight')
