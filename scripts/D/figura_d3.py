"""
Figura D.3 — Horas promedio de uso de internet por grupos de edad
Fuente: ENDUTIH 2023, INEGI

Variable clave: P7_4 — "En promedio, ¿cuántas horas al día utiliza Internet?"
  Valores: 01 = 1 hora o menos, 02 = 2 horas, ..., 12 = 12 horas o más
  IMPORTANTE: el valor ya es numérico (horas), no hay que convertir.

Factor de expansión: FAC_PER
Edad: EDAD

Archivo a usar: tr_endutih_usuarios_anual_2023.csv
  (Solo contiene personas que SÍ declararon usar internet — P7_1 == 1)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import matplotlib.patches as mpatches

# 1. LEER DATOS

# Ajusta esta ruta a donde tienes el archivo en tu máquina
RUTA = PROJECT_ROOT / "datos" / "D.3" / "tr_endutih_usuarios_anual_2023.csv"

# Cargar datos
df = pd.read_csv(RUTA, low_memory=False)

print("Columnas disponibles:", df.columns.tolist())
print(f"Total de registros: {len(df):,}")
print(f"\nDistribución de P7_4 (horas de uso):\n{df['P7_4'].value_counts().sort_index()}")
print(f"\nRango de edades: {df['EDAD'].min()} a {df['EDAD'].max()}")

# 2. LIMPIAR Y PREPARAR

# P7_4 viene como string 01 , 02 , etc. convertir a número
df['horas'] = pd.to_numeric(df['P7_4'], errors='coerce')
df['edad']  = pd.to_numeric(df['EDAD'], errors='coerce')
df['factor'] = pd.to_numeric(df['FAC_PER'], errors='coerce')

# Eliminar registros sin horas o sin factor válido
df_valido = df.dropna(subset=['horas', 'edad', 'factor']).copy()
print(f"\nRegistros válidos para cálculo: {len(df_valido):,}")

# 3. DEFINIR GRUPOS DE EDAD (exactamente como el Anuario)

bins   = [5, 11, 17, 24, 34, 44, 54, 64, 999]
labels = ['6 a 11', '12 a 17', '18 a 24', '25 a 34',
          '35 a 44', '45 a 54', '55 a 64', '65 o más']

df_valido['grupo_edad'] = pd.cut(
    df_valido['edad'],
    bins=bins,
    labels=labels,
    right=True
)

# 4. CALCULAR PROMEDIO PONDERADO POR GRUPO

def promedio_ponderado(grupo):
    return np.average(grupo['horas'], weights=grupo['factor'])

resultado = (
    df_valido
    .dropna(subset=['grupo_edad'])
    .groupby('grupo_edad', observed=True)
    .apply(promedio_ponderado)
    .reset_index()
)
resultado.columns = ['grupo', 'horas_promedio']
resultado['horas_promedio'] = resultado['horas_promedio'].round(1)

print("\n=== RESULTADOS ===")
print(resultado.to_string(index=False))

print("\n=== VALORES ESPERADOS DEL ANUARIO ===")
esperados = {
    '18 a 24': 5.9, '25 a 34': 5.6, '12 a 17': 4.7,
    '35 a 44': 4.5, '45 a 54': 3.8, '55 a 64': 3.3,
    '65 o más': 2.9, '6 a 11': 2.5
}
for g, v in esperados.items():
    calculado = resultado[resultado['grupo'] == g]['horas_promedio'].values
    calc_str = f"{calculado[0]}" if len(calculado) > 0 else "N/A"
    match = "âœ…" if len(calculado) > 0 and abs(calculado[0] - v) < 0.15 else "âš ï¸"
    print(f"  {g:10s}: esperado={v}, calculado={calc_str} {match}")

# 5. CALCULAR EL 71.4% (usuarios de internet / población 6+)

# Para esto necesitas TAMBI N el archivo de residentes (que incluye NO usuarios)
# tr_endutih_residentes_anual_2023.csv tiene TODA la población

# RUTA_RESIDENTES r C: ruta a tr_endutih_residentes_anual_2023.csv
# df_res pd.read_csv(RUTA_RESIDENTES, low_memory False)
# df_res edad pd.to_numeric(df_res EDAD , errors coerce )
# df_res factor pd.to_numeric(df_res FAC_PER , errors coerce )

# total_6mas df_res df_res edad 6 factor .sum()
# usuarios_6mas df_valido df_valido edad 6 factor .sum()
# pct_usuarios (usuarios_6mas / total_6mas) 100
# print(f n% usuarios de internet (6+): pct_usuarios:.1f % ) esperado 71.4%

# 6. GRAFICAR igual que el Anuario

# Orden descendente por horas (como en el Anuario)
orden_anuario = ['18 a 24', '25 a 34', '12 a 17', '35 a 44',
                 '45 a 54', '55 a 64', '65 o más', '6 a 11']

res_ordenado = resultado.set_index('grupo').reindex(orden_anuario).reset_index()

colores = [
    '#E05A4E',  # 18-24  rojo coral oscuro
    '#F08070',  # 25-34  coral claro
    '#2B4E7A',  # 12-17  azul marino
    '#1E6B8A',  # 35-44  azul medio
    '#7EC8C8',  # 45-54  teal claro
    '#5B6EA8',  # 55-64  azul violáceo
    '#7B8DC8',  # 65+    lavanda
    '#48B8C8',  # 6-11   celeste
]

# Crear grafica
fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.bar(
    res_ordenado['grupo'],
    res_ordenado['horas_promedio'],
    color=colores,
    width=0.6,
    zorder=3
)

# Etiquetas encima de cada barra
for bar, val in zip(bars, res_ordenado['horas_promedio']):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.05,
        f'{val}%',
        ha='center', va='bottom',
        fontsize=11, fontweight='bold', color='#333333'
    )

ax.set_ylim(0, 7)
ax.set_yticks(range(0, 8))
ax.set_ylabel('Horas promedio', fontsize=12)
ax.set_xlabel('')
ax.set_title(
    'Figura D.3. Porcentaje de horas promedio de uso de internet por grupos de edad',
    fontsize=13, fontweight='bold', loc='left', pad=15
)
ax.grid(axis='y', linestyle='--', alpha=0.4, zorder=0)
ax.spines[['top', 'right']].set_visible(False)

# Leyenda
leyenda = [mpatches.Patch(color=c, label=g)
           for c, g in zip(colores, orden_anuario)]
ax.legend(handles=leyenda, ncol=8, loc='upper right',
          fontsize=9, frameon=False, bbox_to_anchor=(1, 1.08))

plt.tight_layout()
# Guardar salida
plt.savefig('output/Figura_D3.png', dpi=150, bbox_inches='tight')
print("\nGuardada: Figura_D3.png")
plt.show()
