import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 1. CÁLCULO DE DATOS EXACTOS

file_path = PROJECT_ROOT / "datos" / "E.5" / "Base de datos_Cuarta Encuesta 2023_MiPymes.xlsx"
# Cargar datos
df = pd.read_excel(file_path)

size_col = 'Clasificación de la empresa por su tamaño'
factor_col = 'Factor de Expansión Final'

# Mapeo de columnas para Internet Fijo
internet_cols = {
    'Más gente conoce la empresa': 'En una escala del 0 al 10, donde 0 es “totalmente en desacuerdo” y 10 es “totalmente de acuerdo”, ¿qué tan de acuerdo está con las siguientes frases? Gracias al Internet, ahora más gente conoce la empresa o negocio.',
    'Están más cerca de sus clientes': 'En una escala del 0 al 10, donde 0 es “totalmente en desacuerdo” y 10 es “totalmente de acuerdo”, ¿qué tan de acuerdo está con las siguientes frases? El Internet permite que la empresa o negocio esté más cerca de sus consumidores.',
    'Hay más ventas/clientes': 'En una escala del 0 al 10, donde 0 es “totalmente en desacuerdo” y 10 es “totalmente de acuerdo”, ¿qué tan de acuerdo está con las siguientes frases? Gracias a la conexión a Internet de la empresa o negocio ahora hay más ventas/clientes',
    'Disminución de costos por proveedores': 'En una escala del 0 al 10, donde 0 es “totalmente en desacuerdo” y 10 es “totalmente de acuerdo”, ¿qué tan de acuerdo está con las siguientes frases? La conexión a Internet ha permitido disminuir los costos al poder encontrar más y mejores proveedores',
    'Desarrollar nuevos productos': 'En una escala del 0 al 10, donde 0 es “totalmente en desacuerdo” y 10 es “totalmente de acuerdo”, ¿qué tan de acuerdo está con las siguientes frases? Contar con Internet ha permitido a la empresa o negocio desarrollar nuevos productos o servicios.',
    'Entrega más rápida o menos costosa': 'En una escala del 0 al 10, donde 0 es “totalmente en desacuerdo” y 10 es “totalmente de acuerdo”, ¿qué tan de acuerdo está con las siguientes frases? El Internet de la empresa o negocio ha permitido que la entrega de productos o servicios sea más rápida o menos costosa.',
    'Empleados hacen más en mismo tiempo': 'En una escala del 0 al 10, donde 0 es “totalmente en desacuerdo” y 10 es “totalmente de acuerdo”, ¿qué tan de acuerdo está con las siguientes frases? El Internet de la empresa ha permitido que los empleados hagan más en el mismo tiempo.'
}

# Mapeo de columnas para Telefonía Fija
telefonia_cols = {
    'Más gente conoce la empresa': 'En una escala del 0 al 10, donde 0 es “totalmente en desacuerdo” y 10 es “totalmente de acuerdo”, ¿qué tan de acuerdo está con las siguientes frases? Gracias a la línea telefónica fija, ahora más gente conoce la empresa o negocio.',
    'Están más cerca de sus clientes': 'En una escala del 0 al 10, donde 0 es “totalmente en desacuerdo” y 10 es “totalmente de acuerdo”, ¿qué tan de acuerdo está con las siguientes frases? La línea telefónica fija permite que la empresa o negocio esté más cerca de sus consumidores.',
    'Hay más ventas/clientes': 'En una escala del 0 al 10, donde 0 es “totalmente en desacuerdo” y 10 es “totalmente de acuerdo”, ¿qué tan de acuerdo está con las siguientes frases? Gracias a la línea telefónica fija de la empresa o negocio ahora hay más ventas / Clientes.',
    'Disminución de costos por proveedores': 'En una escala del 0 al 10, donde 0 es “totalmente en desacuerdo” y 10 es “totalmente de acuerdo”, ¿qué tan de acuerdo está con las siguientes frases? La línea telefónica fija ha permitido disminuir los costos al poder encontrar más y mejores proveedores.',
    'Desarrollar nuevos productos': 'En una escala del 0 al 10, donde 0 es “totalmente en desacuerdo” y 10 es “totalmente de acuerdo”, ¿qué tan de acuerdo está con las siguientes frases? Contar con una línea telefónica fija ha permitido a la empresa o negocio desarrollar nuevos productos o servicios.',
    'Entrega más rápida o menos costosa': 'En una escala del 0 al 10, donde 0 es “totalmente en desacuerdo” y 10 es “totalmente de acuerdo”, ¿qué tan de acuerdo está con las siguientes frases? La línea telefónica de la empresa o negocio ha permitido que la entrega de productos o servicios sea más rápida o menos costosa.',
    'Empleados hacen más en mismo tiempo': 'En una escala del 0 al 10, donde 0 es “totalmente en desacuerdo” y 10 es “totalmente de acuerdo”, ¿qué tan de acuerdo está con las siguientes frases? La línea telefónica fija de la empresa o negocio ha permitido que los empleados hagan más en el mismo tiempo.'
}

# Función para promedio ponderado excluyendo Ns/Nc
def promedio_ponderado(df_subset, col_name):
    temp = df_subset[[col_name, factor_col]].copy()
    temp = temp[pd.notna(temp[col_name])]
    temp = temp[temp[col_name] != 'Ns/Nc']
    if len(temp) == 0: return 0.0
    temp[col_name] = pd.to_numeric(temp[col_name])
    suma_ponderada = (temp[col_name] * temp[factor_col]).sum()
    peso_total = temp[factor_col].sum()
    return suma_ponderada / peso_total

beneficios = list(internet_cols.keys())
sizes = ['Micro', 'Pequeña', 'Mediana']

datos_int = {s: [promedio_ponderado(df[df[size_col] == s], internet_cols[b]) for b in beneficios] for s in sizes}
datos_tel = {s: [promedio_ponderado(df[df[size_col] == s], telefonia_cols[b]) for b in beneficios] for s in sizes}

# 2. GENERACI N DE LA GRÁFICA

colores = {'Micro': '#f19a9b', 'Pequeña': '#297b93', 'Mediana': '#ea5b60'}

# Invertir el orden para que coincida visualmente de arriba hacia abajo
beneficios.reverse()
for s in sizes:
    datos_int[s].reverse()
    datos_tel[s].reverse()

y = np.arange(len(beneficios))
alto_barra = 0.25

# Crear grafica
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), sharey=True)

# Gráfico 1: Internet Fijo
ax1.barh(y + alto_barra, datos_int['Micro'], alto_barra, label='Micro', color=colores['Micro'])
ax1.barh(y, datos_int['Pequeña'], alto_barra, label='Pequeña', color=colores['Pequeña'])
ax1.barh(y - alto_barra, datos_int['Mediana'], alto_barra, label='Mediana', color=colores['Mediana'])
ax1.set_title('Internet Fijo', fontsize=14, pad=15)
ax1.set_xlim(0, 10)

# Gráfico 2: Telefonía Fija
ax2.barh(y + alto_barra, datos_tel['Micro'], alto_barra, label='Micro', color=colores['Micro'])
ax2.barh(y, datos_tel['Pequeña'], alto_barra, label='Pequeña', color=colores['Pequeña'])
ax2.barh(y - alto_barra, datos_tel['Mediana'], alto_barra, label='Mediana', color=colores['Mediana'])
ax2.set_title('Telefonía Fija', fontsize=14, pad=15)
ax2.set_xlim(0, 10)

# Etiquetas de texto en las barras
def autolabel_horizontal(ax, rects):
    for rect in rects:
        width = rect.get_width()
        if width > 0:
            ax.annotate(f'{width:.1f}',
                        xy=(width, rect.get_y() + rect.get_height() / 2),
                        xytext=(3, 0),  
                        textcoords="offset points",
                        ha='left', va='center', fontsize=9)

for ax in [ax1, ax2]:
    for container in ax.containers:
        autolabel_horizontal(ax, container)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.grid(True, linestyle='--', alpha=0.7)

ax1.set_yticks(y)
ax1.set_yticklabels(beneficios, fontsize=11)

fig.suptitle('Figura E.5. Percepción sobre los beneficios de contar con servicios fijos', fontsize=14, fontweight='bold', y=1.02)
handles, labels = ax1.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.05), frameon=False, fontsize=12)

plt.tight_layout()
# Guardar salida
plt.savefig('grafica_beneficios_promedio.png', dpi=300, bbox_inches='tight')
print("¡Cálculo finalizado y Gráfica guardada exitosamente como 'grafica_beneficios_promedio.png'!")
