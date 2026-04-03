import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import matplotlib.ticker as mticker

# 1. Leer y limpiar
df = pd.read_csv(PROJECT_ROOT / "datos" / "C.9" / "TD_MARKET_SHARE_TELMOVIL_ITE_VA.csv", encoding='latin1')

df['MARKET_SHARE'] = (df['MARKET_SHARE']
                      .astype(str)
                      .str.replace('%', '')
                      .str.strip())
df['MARKET_SHARE'] = pd.to_numeric(df['MARKET_SHARE'], errors='coerce')

# 2. Filtrar diciembre 2013-2023
df = df[(df['MES'] == 12) & (df['ANIO'].between(2013, 2023))]

# 3. Mapeo a 4 grupos
# AT&T absorbió NEXTEL (2015) e IUSACELL-UNEF N (2015)
def mapear_grupo(nombre):
    if nombre == 'América Móvil':
        return ' América Móvil'
    elif nombre == 'TELEFÓNICA':
        return 'Telefónica'
    elif nombre in ('AT&T', 'IUSACELL-UNEFÓN', 'NEXTEL'):
        return 'AT&T'
    else:
        return 'Otros'

df['GRUPO_FIGURA'] = df['GRUPO'].apply(mapear_grupo)

# 4. Agrupar por año y grupo
pivot = (df.groupby(['ANIO', 'GRUPO_FIGURA'])['MARKET_SHARE']
           .sum()
           .unstack(fill_value=0))

# Orden de columnas orden visual de abajo hacia arriba
orden = [' América Móvil', 'Telefónica', 'AT&T', 'Otros']
pivot = pivot.reindex(columns=orden, fill_value=0)

years = pivot.index.tolist()

# 5. Verificación contra Anuario
print("Verificación valores clave:")
print(f"2013  América Móvil : {pivot.loc[2013,' América Móvil']:.2f}%  (Anuario: 68.86%)")
print(f"2023  América Móvil : {pivot.loc[2023,' América Móvil']:.2f}%  (Anuario: 57.31%)")
print(f"2023 AT&T          : {pivot.loc[2023,'AT&T']:.2f}%  (Anuario: 15.56%)")
print(f"2023 Telefónica    : {pivot.loc[2023,'Telefónica']:.2f}%  (Anuario: 15.09%)")
print(f"2023 Otros         : {pivot.loc[2023,'Otros']:.2f}%  (Anuario: 11.99%)")
print()

# 6. Colores (igual al Anuario)
colores = {
    ' América Móvil': '#e84040',   # rojo
    'Telefónica':    '#f4a460',   # salmón/naranja
    'AT&T':          '#1f3864',   # azul marino oscuro
    'Otros':         '#a8d4e6',   # azul claro
}

# 7. Graficar barras apiladas
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

bar_w = 0.55
x = range(len(years))
bottom = [0] * len(years)

for grupo in orden:
    vals = pivot[grupo].values
    bars = ax.bar(x, vals, bar_w, bottom=bottom,
                  color=colores[grupo], label=grupo, zorder=2)

    # Etiquetas dentro de cada segmento (solo si 1%)
    for i, (v, b) in enumerate(zip(vals, bottom)):
        if v >= 1.0:
            ax.text(i, b + v / 2, f'{v:.2f}%',
                    ha='center', va='center',
                    fontsize=7.5, color='white', fontweight='bold')

    bottom = [b + v for b, v in zip(bottom, vals)]

# 8. Ejes y estilo
ax.set_xticks(list(x))
ax.set_xticklabels([str(y) for y in years], fontsize=9)
ax.set_ylim(0, 115)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{int(v)}%'))
ax.tick_params(colors='#555')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#ccc')
ax.spines['bottom'].set_color('#ccc')

# 9. Leyenda
handles = [plt.Rectangle((0,0),1,1, color=colores[g]) for g in orden]
ax.legend(handles, orden, loc='lower center',
          bbox_to_anchor=(0.5, -0.12),
          ncol=4, fontsize=9, frameon=False)

# 10. Título y fuente
fig.text(0.06, 0.97,
         'Figura C.9. Participación de mercado del servicio móvil de telefonía (2013-2023)',
         fontsize=11, fontweight='bold', color='#1f4e79', va='top')

fig.text(0.06, 0.02,
         'Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones a diciembre de cada año.\n'
         'Nota: Participación de mercado calculada con respecto al número de líneas del servicio móvil de telefonía.',
         fontsize=7.5, color='#555')

plt.tight_layout(rect=[0, 0.06, 1, 0.95])
# Guardar salida
plt.savefig('output/Figura_C9.png', dpi=150, bbox_inches='tight')
plt.savefig('output/Figura_C9.pdf', bbox_inches='tight')
plt.show()
print("âœ… Figura C.9 guardada en output/")
