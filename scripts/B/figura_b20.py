import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import matplotlib.ticker as ticker

# 1. Leer datos
df = pd.read_csv(PROJECT_ROOT / "datos" / "b.20" / "TD_PENETRACION_H_TVRES_ITE_VA.csv")

# 2. Filtrar diciembre, rango 1998-2023
df_plot = (df[(df['MES'] == 12) &
              (df['ANIO'] >= 1998) &
              (df['ANIO'] <= 2023)]
           .sort_values('ANIO')
           .reset_index(drop=True))

anios  = df_plot['ANIO'].tolist()
valores = df_plot['P_H_TVRES_E'].tolist()

# 3. Figura
fig, ax = plt.subplots(figsize=(14, 6))

COLOR_BARRA  = '#B8CCE4'   # azul claro IFT
COLOR_BORDE  = '#2E5FA3'   # azul oscuro IFT
COLOR_LABEL  = '#1F3864'

bars = ax.bar(anios, valores,
              color=COLOR_BARRA,
              edgecolor=COLOR_BORDE,
              linewidth=0.6,
              width=0.7)

# 4. Etiquetas sobre cada barra
for bar, val in zip(bars, valores):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.8,
            str(val),
            ha='center', va='bottom',
            fontsize=7.5, color=COLOR_LABEL, fontweight='bold')

# 5. Etiquetas destacadas en extremos (1998 y 2023)
for idx in [0, -1]:
    bar = bars[idx]
    val = valores[idx]
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.8,
            str(val),
            ha='center', va='bottom',
            fontsize=9, color=COLOR_BORDE, fontweight='bold')

# 6. Eje X
ax.set_xticks(anios)
ax.set_xticklabels([str(a) for a in anios],
                   rotation=90, fontsize=8, color='#444')

# 7. Eje Y
ax.set_ylim(0, max(valores) * 1.18)
ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
ax.tick_params(axis='y', labelsize=8, colors='#444')
ax.set_ylabel('Accesos por cada 100 hogares', fontsize=9, color='#444')

# 8. Línea naranja de acento (estilo IFT)
ax.axhline(y=0, color=COLOR_BORDE, linewidth=1.2)

# 9. Título y fuente
ax.set_title(
    'Figura B.20. Accesos del Servicio de Televisión Restringida\n'
    'por cada 100 hogares (1998-2023)',
    fontsize=11, color=COLOR_LABEL, fontweight='bold', pad=12)

fig.text(
    0.01, -0.04,
    'Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones '
    'a diciembre de cada año, del CONAPO y el INEGI.',
    fontsize=7.5, color='#666', style='italic')

# 10. Estética general
ax.spines[['top', 'right', 'left']].set_visible(False)
ax.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.5)

plt.tight_layout()
# Guardar salida
plt.savefig(PROJECT_ROOT / "output" / "Figura_B20.png", dpi=150, bbox_inches='tight')
plt.show()
print("âœ… Guardado en output/Figura_B20.png")
