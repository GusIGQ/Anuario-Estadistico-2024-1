import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 1. Leer y filtrar
df = pd.read_csv(PROJECT_ROOT / "datos" / "C.10" / "TD_IHH_TELMOVIL_ITE_VA.csv", encoding='latin1')

df = df[(df['MES'] == 12) & (df['ANIO'].between(2013, 2023))]
df = df.sort_values('ANIO')

years = df['ANIO'].tolist()
values = df['IHH_TELMOVIL_E'].tolist()

# 2. Verificación
print("Verificación valores clave:")
for y, v in zip(years, values):
    print(f"  {y}: {v}")
print(f"\n2013 (Anuario: 5,229): {values[0]}")
print(f"2023 (Anuario: 3,824): {values[-1]}")

# 3. Valores del Anuario (por si hay discrepancias menores)
anuario = {
    2013: 5229, 2014: 5084, 2015: 5227, 2016: 4873, 2017: 4759,
    2018: 4576, 2019: 4558, 2020: 4549, 2021: 4556, 2022: 4162, 2023: 3824
}
# Descomenta la siguiente línea para forzar valores del Anuario:
# values anuario y for y in years

# 4. Figura
fig, ax = plt.subplots(figsize=(11, 7))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

bar_h = 0.55
y_pos = range(len(years))

bars = ax.barh(list(y_pos), values, bar_h,
               color='#2e8b9a', zorder=2)

# Etiquetas al final de cada barra
for i, (v, b) in enumerate(zip(values, bars)):
    ax.text(v + 30, b.get_y() + b.get_height() / 2,
            f'{v:,}', va='center', ha='left',
            fontsize=9, color='#333', fontweight='bold')

# 5. Ejes
ax.set_yticks(list(y_pos))
ax.set_yticklabels([str(y) for y in years], fontsize=9)
ax.set_xlim(0, max(values) * 1.15)
ax.invert_yaxis()   # 2013 arriba, 2023 abajo

ax.xaxis.set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_color('#ccc')
ax.tick_params(colors='#555')

# 6. Título y fuente
fig.text(0.06, 0.97,
         'Figura C.10. Herfindahl-Hirschman (IHH). Concentración de mercado\n'
         '   del servicio móvil de telefonía (2013-2023)',
         fontsize=11, fontweight='bold', color='#1f4e79', va='top')

fig.text(0.06, 0.02,
         'Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones a diciembre de cada año.\n'
         'Nota: Herfindahl-Hirschman (IHH) estimado con respecto al número de líneas del servicio móvil de telefonía.',
         fontsize=7.5, color='#555')

plt.tight_layout(rect=[0, 0.06, 1, 0.93])
# Guardar salida
plt.savefig('output/Figura_C10.png', dpi=150, bbox_inches='tight')
plt.savefig('output/Figura_C10.pdf', bbox_inches='tight')
plt.show()
print("âœ… Figura C.10 guardada en output/")
