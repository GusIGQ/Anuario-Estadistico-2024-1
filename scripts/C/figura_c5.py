import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
import matplotlib.ticker as mticker
import numpy as np

# 1. Lectura
df = pd.read_csv(
    'datos/C.5/TD_LINEAS_HIST_TELMOVIL_ITE_VA.csv',
    encoding='cp1252'
)

# 2. Filtrar diciembre de cada año
df_dic = df[df['MES'] == 12].copy()

# 3. Agrupar por año y sumar líneas
cols = [
    'L_PREPAGO_E',
    'L_POSPAGO_E',
    'L_POSPAGOC_E',       # pospago controlado
    'L_POSPAGOL_E',       # pospago libre
    'L_NO_ESPECIFICADO_E',
    'L_TOTAL_E',
]
df_anual = df_dic.groupby('ANIO')[cols].sum().reset_index()

# 4. Filtrar 1990 2023
df_anual = df_anual[(df_anual['ANIO'] >= 1990) & (df_anual['ANIO'] <= 2023)].copy()

# 5. Convertir a millones
for c in cols:
    df_anual[c] = df_anual[c] / 1_000_000

# 6. Verificación rápida
check = {1990: 0.1, 2000: 14.1, 2013: 101.4, 2023: 144.7}
print("── Verificación ──")
for yr, expected in check.items():
    row = df_anual[df_anual['ANIO'] == yr]
    if not row.empty:
        calc = round(row['L_TOTAL_E'].values[0], 1)
        status = "âœ…" if calc == expected else f"âš  esperado {expected}"
        print(f"  {yr}: {calc}M  {status}")

# 7. Paleta (igual al Anuario)
COLOR_PREPAGO   = '#7EC8C8'   # azul/verde claro
COLOR_POSPAGO   = '#2E6FA3'   # azul medio
COLOR_POSPC     = '#1A3A5C'   # azul oscuro (controlado)
COLOR_POSPL     = '#F4845F'   # salmón/naranja (libre)
COLOR_NOESP     = '#A8C8E0'   # gris azulado (sin segmento)
COLOR_TOTAL     = '#E63946'   # rojo (línea total)

anios  = df_anual['ANIO'].values
prepago = df_anual['L_PREPAGO_E'].values
pospc   = df_anual['L_POSPAGOC_E'].values
pospl   = df_anual['L_POSPAGOL_E'].values
pospago = df_anual['L_POSPAGO_E'].values   # pospago genérico (años <2017)
noesp   = df_anual['L_NO_ESPECIFICADO_E'].values
total   = df_anual['L_TOTAL_E'].values

# 8. Figura
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# Área rellena apilada: prepago + pospago genérico + controlado + libre + sin seg
ax.stackplot(
    anios,
    prepago, pospago, pospc, pospl, noesp,
    labels=[
        'Líneas Prepago',
        'Líneas Pospago',
        'Líneas Pospago controlado',
        'Líneas Pospago libre',
        'Líneas sin segmento especificado',
    ],
    colors=[COLOR_PREPAGO, COLOR_POSPAGO, COLOR_POSPC, COLOR_POSPL, COLOR_NOESP],
    alpha=0.85
)

# Línea de totales encima
ax.plot(anios, total, color=COLOR_TOTAL, linewidth=2,
        marker='o', markersize=3, label='Líneas totales', zorder=5)

# 9. Etiquetas en extremos (1990 y 2023)
def label(ax, x, y, txt, ha='left'):
    ax.annotate(
        txt,
        xy=(x, y), xytext=(4 if ha == 'left' else -4, 4),
        textcoords='offset points',
        fontsize=8, fontweight='bold', color=COLOR_TOTAL,
        ha=ha, va='bottom'
    )

label(ax, anios[0],  total[0],  f"{total[0]:.1f}",  ha='right')
label(ax, anios[-1], total[-1], f"{total[-1]:.1f}", ha='left')

# Etiquetas intermedias visibles en el Anuario
etiquetas = {
    2000: None, 2001: None, 2002: None, 2003: None, 2004: None,
    2005: None, 2006: None, 2007: None, 2008: None, 2009: None,
    2010: None, 2011: None, 2012: None, 2013: None, 2014: None,
    2015: None, 2016: None, 2017: None, 2018: None, 2019: None,
    2020: None, 2021: None, 2022: None,
}
# Sólo etiquetamos los valores visibles en la figura del Anuario
visible = {
    2000: 14.1, 2004: 38.5, 2005: 47.1, 2006: 55.4, 2007: 66.6,
    2008: 75.4, 2009: 83.2, 2010: 90.5, 2011: 94.6, 2012: 101.4,
    2013: 104.9, 2014: 106.7, 2015: 107.7, 2016: 111.7, 2017: 114.3,
    2018: 120.2, 2019: 122.9, 2020: 122.0, 2021: 126.5, 2022: 136.0,
}
for yr, val in visible.items():
    row = df_anual[df_anual['ANIO'] == yr]
    if not row.empty:
        v = row['L_TOTAL_E'].values[0]
        ax.annotate(
            f"{v:.1f}",
            xy=(yr, v), xytext=(0, 5),
            textcoords='offset points',
            fontsize=6.5, color='#333333',
            ha='center', va='bottom'
        )

# 10. Ejes y formato
ax.yaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, _: f'{int(x):,}'.replace(',', ',')
))
ax.set_ylim(0, 170_000_000 / 1e6 * 1e6)   # eje en unidades absolutas â†’ millones
ax.yaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, _: f'{x:,.0f}'
))

# Reescalar eje Y a valores en millones (ya convertidos)
ax.set_ylim(0, 170)
ax.yaxis.set_major_locator(mticker.MultipleLocator(20))
ax.set_ylabel('Millones de Líneas', fontsize=9)

ax.set_xlim(1989, 2024)
ax.set_xticks(range(1990, 2024))
ax.set_xticklabels(
    [str(y) for y in range(1990, 2024)],
    rotation=90, fontsize=7
)

ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.spines[['top', 'right']].set_visible(False)

# 11. Leyenda
handles, labels_leg = ax.get_legend_handles_labels()
ax.legend(
    handles, labels_leg,
    loc='upper left', fontsize=7.5,
    frameon=False, ncol=2
)

# 12. Título y fuente
ax.set_title(
    'Figura C.5. Líneas del servicio móvil de telefonía (1990-2023)',
    fontsize=11, fontweight='bold', loc='left', pad=10
)
fig.text(
    0.01, -0.04,
    'Fuente: IFT con datos de los operadores de telecomunicaciones a diciembre de cada año.\n'
    'Nota: A partir del tercer trimestre de 2017, se agregó la desagregación por pospago libre y pospago controlado.',
    fontsize=7, color='gray'
)

plt.tight_layout()
# Guardar salida
plt.savefig('output/Figura_C5.png', dpi=150, bbox_inches='tight')
plt.savefig('output/Figura_C5.pdf', bbox_inches='tight')
print("\nGuardado: output/Figura_C5.png y output/Figura_C5.pdf")
plt.show()
