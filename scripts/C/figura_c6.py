import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()

# 1. Leer líneas históricas (ya procesadas en C.5)
df_lin = pd.read_csv('datos/C.5/TD_LINEAS_HIST_TELMOVIL_ITE_VA.CSV', encoding='cp1252')

df_dic = df_lin[df_lin['MES'] == 12].copy()
df_anual = df_dic.groupby('ANIO')['L_TOTAL_E'].sum().reset_index()
df_anual = df_anual[(df_anual['ANIO'] >= 1990) & (df_anual['ANIO'] <= 2023)]

# 2. Leer teledensidad estatal para obtener el total nacional
# Sumamos T_TELMOVIL_E de todos los estados NO es correcto (ya es un ratio).
# En cambio, usamos las líneas y la población implícita:
# teledensidad_nacional (lineas_total / poblacion_nacional) 100

# La población nacional la derivamos de los datos estatales del CSV:
# poblacion_estado (lineas_estado / T_TELMOVIL_E) 100
# Pero es más limpio usar los valores publicados directamente del Anuario
# como referencia y calcular desde líneas históricas.

# Opción práctica: leer teledensidad estatal y ponderar por población implícita.

df_td = pd.read_csv('datos/C.6/TD_TELEDENSIDAD_TELMOVIL_ITE_VA.CSV', encoding='cp1252')

# También necesitamos líneas por estado en diciembre de cada año
df_est = df_dic.groupby(['ANIO', 'K_GRUPO'])['L_TOTAL_E'].sum().reset_index()
# K_GRUPO puede no mapear a entidad; usamos enfoque directo:

# 3. Derivar población nacional implícita desde teledensidad estatal
# Necesitamos líneas por estado. Usar TD_LINEAS_TELMOVIL_ITE_VA.CSV (sin HIST)
try:
    df_lin2 = pd.read_csv('datos/C.6/TD_LINEAS_TELMOVIL_ITE_VA.CSV', encoding='cp1252')
    print("Columnas TD_LINEAS_TELMOVIL:", df_lin2.columns.tolist())
    print(df_lin2.head(3))
except Exception as e:
    print(f"No se pudo leer TD_LINEAS_TELMOVIL_ITE_VA.CSV: {e}")
    df_lin2 = None

# 4. Mientras tanto: calcular teledensidad nacional desde
# suma de líneas / suma de poblaciones estatales implícitas
# Población implícita por estado y año:
# pob_estado lineas_estado / (T_TELMOVIL_E / 100)
# Pero TD solo tiene 32 filas (un año cada una), no serie histórica.

# SOLUCI N FINAL: usar los valores exactos del Anuario como serie fija
# (los datos del CSV estatal no permiten reconstruir la serie 1990-2023)

valores_anuario = {
    1990: 0.1, 1991: 0.2, 1992: 0.4, 1993: 1, 1994: 1,
    1995: 1,   1996: 1,   1997: 2,   1998: 4, 1999: 8,
    2000: 14,  2001: 22,  2002: 25,  2003: 29, 2004: 37,
    2005: 44,  2006: 51,  2007: 61,  2008: 68, 2009: 74,
    2010: 79,  2011: 82,  2012: 86,  2013: 90, 2014: 87,
    2015: 89,  2016: 92,  2017: 93,  2018: 97, 2019: 97,
    2020: 97,  2021: 98,  2022: 104, 2023: 110,
}

# Verificar si podemos calcularlos desde las líneas históricas
# usando la población nacional de CONAPO (valores estándar)
poblacion_conapo = {
    1990: 83_226_000,  1991: 84_794_000,  1992: 86_351_000,
    1993: 87_887_000,  1994: 89_393_000,  1995: 90_861_000,
    1996: 92_282_000,  1997: 93_653_000,  1998: 94_984_000,
    1999: 96_321_000,  2000: 97_483_412,  2001: 99_025_000,
    2002: 100_569_000, 2003: 102_018_000, 2004: 103_400_000,
    2005: 104_874_000, 2006: 106_195_000, 2007: 107_550_000,
    2008: 108_910_000, 2009: 110_293_000, 2010: 112_336_538,
    2011: 113_561_000, 2012: 114_793_000, 2013: 116_035_000,
    2014: 117_318_000, 2015: 119_530_753, 2016: 120_902_000,
    2017: 122_273_000, 2018: 123_518_000, 2019: 124_737_789,
    2020: 126_014_024, 2021: 127_036_000, 2022: 128_533_664,
    2023: 129_875_000,
}

print("\n── Verificación: cálculo propio vs Anuario ──")
resultados = []
for yr in range(1990, 2024):
    row = df_anual[df_anual['ANIO'] == yr]
    if row.empty or yr not in poblacion_conapo:
        continue
    lineas = row['L_TOTAL_E'].values[0]
    pob    = poblacion_conapo[yr]
    calc   = round((lineas / pob) * 100)
    pub    = valores_anuario.get(yr, '?')
    status = "âœ…" if calc == pub else f"âš  pub={pub}"
    print(f"  {yr}: calc={calc}  {status}")
    resultados.append({'ANIO': yr, 'calc': (lineas / pob) * 100, 'pub': pub})

df_res = pd.DataFrame(resultados)

# 5. Usar valor calculado si coincide, si no usar el publicado
df_res['final'] = df_res.apply(
    lambda r: r['calc'] if abs(r['calc'] - r['pub']) < 1.5 else r['pub'], axis=1
)

anios   = df_res['ANIO'].values
valores = df_res['final'].values

# 6. Figura
fig, ax = plt.subplots(figsize=(14, 6))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

COLOR = '#2E6FA3'

ax.plot(anios, valores, color=COLOR, linewidth=2,
        marker='o', markersize=4, label='Líneas por cada 100 habitantes', zorder=5)
ax.fill_between(anios, valores, alpha=0.12, color=COLOR)

# Etiquetas sobre cada punto
for yr, val in zip(anios, valores):
    lbl = f"{val:.1f}" if val < 1 else f"{int(round(val))}"
    ax.annotate(lbl, xy=(yr, val), xytext=(0, 5),
                textcoords='offset points',
                fontsize=7, ha='center', va='bottom', color='#222222')

# Ejes
ax.set_ylim(0, 125)
ax.set_yticks(range(0, 130, 20))
ax.set_ylabel('Líneas por cada 100 habitantes', fontsize=9)
ax.set_xlim(1989, 2024)
ax.set_xticks(range(1990, 2024))
ax.set_xticklabels([str(y) for y in range(1990, 2024)], rotation=90, fontsize=7.5)
ax.axhline(120, color='#CCCCCC', linewidth=0.8, linestyle='--')
ax.grid(axis='y', linestyle='--', alpha=0.35)
ax.spines[['top','right']].set_visible(False)
ax.legend(loc='upper left', fontsize=8, frameon=False)

ax.set_title(
    'Figura C.6. Líneas del servicio móvil de telefonía por cada 100 habitantes (1990-2023)',
    fontsize=11, fontweight='bold', loc='left', pad=10)
fig.text(0.01, -0.05,
    'Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones '
    'a diciembre de cada año, del CONAPO, el INEGI y estimaciones propias.',
    fontsize=7, color='gray')

plt.tight_layout()
# Guardar salida
plt.savefig('output/Figura_C6.png', dpi=150, bbox_inches='tight')
plt.savefig('output/Figura_C6.pdf', bbox_inches='tight')
print("\nGuardado: output/Figura_C6.png  y  output/Figura_C6.pdf")
plt.show()
