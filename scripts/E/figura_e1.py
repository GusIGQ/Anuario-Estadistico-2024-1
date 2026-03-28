import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 1. Cargar los datos desde los archivos subidos
file_movil = PROJECT_ROOT / "datos" / "E.1" / "Tercera Encuesta 2023_Tel Móvil.xlsx"
file_fija = PROJECT_ROOT / "datos" / "E.1" / "Tercera Encuesta 2023_Tel Fija.xlsx"
file_int_tv = PROJECT_ROOT / "datos" / "E.1" / "Tercera Encuesta 2023_Int&TV.xlsx"

# Cargar datos
df_movil = pd.read_excel(file_movil)
df_fija = pd.read_excel(file_fija)
df_int_tv = pd.read_excel(file_int_tv)

# 2. Definir las columnas base (Satisfacción general escala 0-100)
col_movil = 'En tÃ©rminos generales, Â¿quÃ© tan satisfecho se encuentra con el servicio de telefonÃ­a mÃ³vil que ha recibido en los Ãºltimos 12 meses? Recodificada'
col_fija = 'En tÃ©rminos generales, Â¿quÃ© tan satisfecho se encuentra con el servicio de telefonÃ­a fija que ha recibido en los Ãºltimos 12 meses? Recodificada'
col_tv = 'En tÃ©rminos generales, Â¿quÃ© tan satisfecho se encuentra con el servicio de televisiÃ³n de paga que ha recibido en los Ãºltimos 12 meses? Recodificada '
col_int = 'En tÃ©rminos generales, Â¿quÃ© tan satisfecho se encuentra con el servicio de Internet que ha recibido en los Ãºltimos 12 meses? Recodificada '

# 3. Calcular el promedio directamente desde los datos crudos
val_movil = df_movil[col_movil].dropna().mean()
val_fija = df_fija[col_fija].dropna().mean()
val_tv = df_int_tv[col_tv].dropna().mean()
val_int = df_int_tv[col_int].dropna().mean()

# 4. Construir el DataFrame dinámico
data_calc = {
    'Servicio': ['Internet fijo', 'TelevisiÃ³n de paga', 'TelefonÃ­a mÃ³vil', 'TelefonÃ­a fija'],
    'Calculado': [val_int, val_tv, val_movil, val_fija]
}
df_calc = pd.DataFrame(data_calc)
df_calc = df_calc.sort_values(by='Calculado', ascending=True)

# 5. Generar la gráfica
fig, ax = plt.subplots(figsize=(10, 5))
colors = ['#F79A8D', '#544A7E', '#2874A6', '#A9D0D8']

bars = ax.barh(df_calc['Servicio'], df_calc['Calculado'], color=colors, height=0.6)

for bar in bars:
    ax.text(bar.get_width() + 0.5, 
            bar.get_y() + bar.get_height() / 2, 
            f'{bar.get_width():.1f}', 
            va='center', ha='left', fontweight='bold', color='black', fontsize=11)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.xaxis.set_visible(False)
ax.tick_params(axis='y', length=0, labelsize=11)

plt.tight_layout()
# Guardar salida
plt.savefig(PROJECT_ROOT / "output" / "Figura_E1.png", dpi=300, bbox_inches='tight')
