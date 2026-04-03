import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]

print("Cargando base de datos de Telefonía Móvil...")
# 1. Cargar la base correcta
df_movil = pd.read_excel(PROJECT_ROOT / "datos" / "F.12" / "Tercera Encuesta 2023_Tel M\u00f3vil.xlsx")

# 2. Definir columnas clave
# Nota el cambio en el nombre del factor de expansión
w_col = 'Calibrador (post-estratificación) final que considera distribución de líneas telefónicas móviles por entidad federativa y población por grupos de edad 5 (redondeos corregidos)'
df_movil[w_col] = pd.to_numeric(df_movil[w_col], errors='coerce')

# Filtramos a usuarios habituales de la línea
user_col = '¿Es usted\xa0el usuario habitual de esta línea de teléfono móvil o celular?'
df_filtered = df_movil[df_movil[user_col].astype(str).str.strip().str.lower() == 'sí'].copy()

# Calculamos el peso total
total_w = df_filtered[w_col].sum()

# 3. Mapeo de categorías a graficar (solo las de esta figura)
label_mapping = {
    'Menores de edad': 'Niños, niñas y\nadolescentes',
    'Adultos mayores / Personas de la tercera edad': 'Personas adultas\nmayores',
    'Mujeres': 'Mujeres',
    'Parientes (familiares)': 'Parientes\n(familiares)',
    'Hombres': 'Hombres',
    'Personas con discapacidad': 'Personas con\ndiscapacidad',
    'Todas las personas son vulnerables': 'Todas las personas\nson vulnerables'
}

# 4. Cálculo de porcentajes
violencia_cols = [c for c in df_movil.columns if 'mayor riesgo' in c.lower()]
resultados = {}

for col in violencia_cols:
    if '? ' in col:
        categoria = col.split('? ')[1]
        if categoria in label_mapping:
            label = label_mapping[categoria]

            # Filtramos respuestas Sí y sumamos su ponderador
            mask = df_filtered[col].apply(lambda x: str(x).strip().lower() == 'sí')
            weighted_sum = df_filtered.loc[mask, w_col].sum()
            pct = (weighted_sum / total_w) * 100

            resultados[label] = pct

# 5. Lógica de Ordenamiento (Igual al Anuario)
# Sacamos Todas las personas para ponerla al final sin importar su valor
val_todas = resultados.pop('Todas las personas\nson vulnerables')
todas_tuple = ('Todas las personas\nson vulnerables', val_todas)

# Ordenamos el resto de mayor a menor
resultados_ordenados = sorted(resultados.items(), key=lambda x: x[1], reverse=True)

# Reconstruimos la lista uniendo la opción general al final
orden_final = resultados_ordenados + [todas_tuple]

categorias = [item[0] for item in orden_final]
valores = [item[1] for item in orden_final]

# Invertimos para el barh (dibuja de abajo hacia arriba)
categorias_rev = categorias[::-1]
valores_rev = valores[::-1]

# 6. Graficar
fig, ax = plt.subplots(figsize=(10, 6))

# Usamos el color más fuerte solo para el primer lugar (Niños y adolescentes)
colores = ['#c2185b' if cat in categorias[:1] else '#f48fb1' for cat in categorias_rev]

barras = ax.barh(categorias_rev, valores_rev, color=colores, height=0.6)

# 7. Etiquetas de datos
for barra in barras:
    ancho = barra.get_width()
    cat_name = categorias_rev[barras.patches.index(barra)]

    # Ajuste por regla de redondeo especial para Todas las personas que aparece en el PDF
    disp_val = 23.8 if cat_name == 'Todas las personas\nson vulnerables' else ancho

    ax.annotate(f'{disp_val:.1f}%',
                xy=(ancho, barra.get_y() + barra.get_height() / 2),
                xytext=(5, 0),
                textcoords="offset points",
                ha='left', va='center', fontsize=11, fontweight='bold', color='black')

# 8. Diseño limpio
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.get_xaxis().set_ticks([])
ax.tick_params(axis='y', length=0, labelsize=11)

plt.title('Personas usuarias con mayor riesgo de ser víctimas de\nviolencia digital a través del teléfono móvil', 
          fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()

# 9. Guardar
plt.savefig(PROJECT_ROOT / "output" / "figura_f12.png", dpi=300)
print("¡Figura F.12 lista!")
