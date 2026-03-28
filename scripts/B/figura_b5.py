import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 1. Cargar datos
df = pd.read_csv(PROJECT_ROOT / "datos" / "B.5" / "TD_PENETRACION_H_TELFIJA_ITE_VA.csv", encoding='latin1')

# 2. Filtrar: solo diciembre (MES 12), rango 1971-2023
# La columna P_H_TELFIJA_E ya contiene el cálculo: líneas / 100 hogares
df_plot = df[(df['MES'] == 12) & (df['ANIO'] >= 1971) & (df['ANIO'] <= 2023)].copy()

anios   = df_plot['ANIO'].values
valores = df_plot['P_H_TELFIJA_E'].values

# 3. Graficar
fig, ax = plt.subplots(figsize=(16, 6))

bars = ax.bar(anios, valores, color='#5B8DB8', width=0.7, zorder=2)

# Etiquetas sobre cada barra
for anio, val, bar in zip(anios, valores, bars):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
            str(int(val)), ha='center', va='bottom', fontsize=6.5, color='#333333')

# 4. Formato de ejes
ax.set_xlim(1970.2, 2023.8)
ax.set_ylim(0, 90)
ax.set_xticks(anios)
ax.set_xticklabels(anios, rotation=90, fontsize=7.5)
ax.yaxis.grid(True, linestyle='--', alpha=0.4)
ax.set_axisbelow(True)
ax.spines[['top', 'right']].set_visible(False)
ax.tick_params(axis='y', labelsize=8)

# 5. Título y fuente
ax.set_title('Figura B.5. LÃ­neas del Servicio Fijo de TelefonÃ­a por cada 100 hogares (1971-2023)',
             fontsize=11, fontweight='bold', loc='left', pad=10)
ax.set_ylabel('LÃ­neas por cada 100 hogares', fontsize=9)

fig.text(0.01, -0.04,
         'Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones '
         'a diciembre de cada aÃ±o, del CONAPO y el INEGI.',
         fontsize=7, color='gray')

# 6. Guardar
plt.tight_layout()
# Guardar salida
plt.savefig(PROJECT_ROOT / "output" / "Figura_B5.png", dpi=150, bbox_inches='tight')
print("Figura guardada: Figura_B5.png")

# 7. Imprimir valores calculados
print("\nValores calculados (lÃ­neas por cada 100 hogares, diciembre):")
print(df_plot[['ANIO', 'P_H_TELFIJA_E']].to_string(index=False))
