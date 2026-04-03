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
df = pd.read_csv(PROJECT_ROOT / "datos" / "B.4" / "TD_LINEAS_HIST_TELFIJA_ITE_VA.csv", encoding='latin1')

# 2. Calcular: sumar líneas totales por año, solo diciembre (MES 12)
df_dic = df[df['MES'] == 12].groupby('ANIO')['L_TOTAL_E'].sum().reset_index()
df_plot = df_dic[(df_dic['ANIO'] >= 2000) & (df_dic['ANIO'] <= 2023)].copy()

# 3. Graficar
fig, ax = plt.subplots(figsize=(14, 6))

# Línea y área
ax.plot(df_plot['ANIO'], df_plot['L_TOTAL_E'],
        color='#2E5F8A', linewidth=2, marker='o', markersize=5, zorder=3,
        label='Líneas totales')
ax.fill_between(df_plot['ANIO'], df_plot['L_TOTAL_E'],
                alpha=0.15, color='#2E5F8A')

# Etiqueta año 2000
val_2000 = df_plot.loc[df_plot['ANIO'] == 2000, 'L_TOTAL_E'].values[0]
ax.annotate(f"{int(val_2000):,}",
            xy=(2000, val_2000),
            xytext=(2000.2, val_2000 + 450_000),
            fontsize=8, color='#2E5F8A', fontweight='bold')

# Etiqueta año 2023
val_2023 = df_plot.loc[df_plot['ANIO'] == 2023, 'L_TOTAL_E'].values[0]
ax.annotate(f"{int(val_2023):,}",
            xy=(2023, val_2023),
            xytext=(2021.8, val_2023 + 450_000),
            fontsize=8, color='#2E5F8A', fontweight='bold')

# 4. Formato de ejes
ax.set_xlim(1999.5, 2023.5)
ax.set_ylim(10_000_000, 32_000_000)
ax.set_xticks(df_plot['ANIO'])
ax.set_xticklabels(df_plot['ANIO'], rotation=90, fontsize=8)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax.tick_params(axis='y', labelsize=8)

# Grid
ax.yaxis.grid(True, linestyle='--', alpha=0.5)
ax.set_axisbelow(True)
ax.spines[['top', 'right']].set_visible(False)

# 5. Leyenda, título y fuente
ax.legend(loc='upper left', fontsize=9)
ax.set_title('Figura B.4. Líneas del Servicio Fijo de Telefonía (2000-2023)',
             fontsize=11, fontweight='bold', loc='left', pad=10)
ax.set_ylabel('Líneas totales', fontsize=9)

fig.text(0.01, -0.05,
         'Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones a diciembre de cada año.',
         fontsize=7, color='gray')

# 6. Guardar
plt.tight_layout()
# Guardar salida
plt.savefig(PROJECT_ROOT / "output" / "Figura_B4.png", dpi=150, bbox_inches='tight')
print("Figura guardada: figura_B4_lineas_telfija.png")

# 7. Imprimir valores calculados
print("\nValores calculados (diciembre de cada año):")
print(df_plot.to_string(index=False))
