import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import matplotlib.ticker as mticker

# 1. Cargar datos
df = pd.read_csv(PROJECT_ROOT / "datos" / "B.8" / "TD_TRAF_HIST_TELFIJA_ITE_VA.csv", encoding='latin1')

# 2. Calcular: sumar tráfico de todos los meses por año (acumulado anual)
# La figura muestra minutos acumulados a diciembre de cada año
df_anual = (df[(df['ANIO'] >= 2000) & (df['ANIO'] <= 2023)]
            .groupby('ANIO')['TRAF_E'].sum()
            .reset_index())

# Convertir a millones de minutos (para el eje Y)
df_anual['TRAF_M'] = df_anual['TRAF_E'] / 1_000_000

aÃ±os    = df_anual['ANIO'].values
valores = df_anual['TRAF_M'].values

# 3. Graficar
fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(aÃ±os, valores, color='#2E5F8A', linewidth=2, marker='o', markersize=5,
        zorder=3, label='TrÃ¡fico local del servicio fijo de telefonÃ­a')
ax.fill_between(aÃ±os, valores, alpha=0.12, color='#2E5F8A')

# Etiqueta año 2000
val_2000 = df_anual[df_anual['ANIO'] == 2000]['TRAF_E'].values[0]
ax.annotate(f"{int(val_2000):,}",
            xy=(2000, val_2000 / 1_000),
            xytext=(2001, val_2000 / 1_000 + 3_000),
            fontsize=7.5, color='#2E5F8A', fontweight='bold')

# Etiqueta año 2023
val_2023 = df_anual[df_anual['ANIO'] == 2023]['TRAF_E'].values[0]
ax.annotate(f"{int(val_2023):,}",
            xy=(2023, val_2023 / 1_000),
            xytext=(2020.5, val_2023 / 1_000 + 8_000),
            fontsize=7.5, color='#2E5F8A', fontweight='bold')

# Etiquetas años extremos en eje X
ax.text(2000, -12_000, '2000', ha='center', fontsize=9,
        fontweight='bold', color='#2E5F8A', clip_on=False)
ax.text(2023, -12_000, '2023', ha='center', fontsize=9,
        fontweight='bold', color='#2E5F8A', clip_on=False)

# 4. Formato de ejes
ax.set_xlim(1999.5, 2023.5)
ax.set_ylim(0, 160_000)
ax.set_xticks(aÃ±os)
ax.set_xticklabels(aÃ±os, rotation=90, fontsize=8)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax.tick_params(axis='y', labelsize=8)
ax.yaxis.grid(True, linestyle='--', alpha=0.4)
ax.set_axisbelow(True)
ax.spines[['top', 'right']].set_visible(False)

# 5. Leyenda, título y fuente
ax.legend(loc='upper right', fontsize=9)
ax.set_title('Figura B.8. TrÃ¡fico de minutos del Servicio Fijo de TelefonÃ­a (2000-2023)',
             fontsize=11, fontweight='bold', loc='left', pad=10)
ax.set_ylabel('Millones de minutos', fontsize=9)

fig.text(0.01, -0.05,
         'Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones. '
         'Para cada aÃ±o los datos se presentan acumulados al mes de diciembre.',
         fontsize=7, color='gray')

# 6. Guardar
plt.tight_layout()
# Guardar salida
plt.savefig(PROJECT_ROOT / "output" / "Figura_B8.png", dpi=150, bbox_inches='tight')
print("Figura guardada: Figura_B8.png")

# 7. Imprimir valores calculados
print("\nValores calculados (minutos acumulados por aÃ±o):")
print(df_anual[['ANIO', 'TRAF_E']].to_string(index=False))
