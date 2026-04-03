"""
Figura D.11 — Porcentaje de la población usuaria de Internet, qué tan seguro es
compartir información en redes sociales (por sexo).

Fuente: IFT, Encuesta de Confianza en el Servicio de Internet (ECSI) 2024.

Metodología:
  - Universo  : rescate_internet == 1  (usuarios de Internet)
  - Agrupación: sexo (1 = Hombres, 2 = Mujeres)
  - Variable  : seg_redes
      1 = Muy seguro | 2 = Seguro | 3 = Ni seguro / Ni inseguro
      4 = Inseguro   | 9 = NS/NR
  - Ponderador: fac_per
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

# ── 1. Carga de Datos ─────────────────────────────────────────────────────────
# Ajusta la ruta si es necesario
DATA_PATH = Path(r"C:\Users\ivan-\Documents\GitHub\anuario\datos\D.11\baseconfianzadigital.csv") 
df = pd.read_csv(DATA_PATH, low_memory=False)

# ── 2. Filtro universo (Usuarios de Internet) ─────────────────────────────────
usuarios = df[df["rescate_internet"] == 1].copy()

# ── 3. Cálculo Ponderado ──────────────────────────────────────────────────────
# Asegurarnos de usar solo Hombres (1) y Mujeres (2) por si hay valores nulos
usuarios = usuarios[usuarios["sexo"].isin([1, 2])]

GRUPOS_SEXO = {
    1: "Mujeres",
    2: "Hombres"
}

CATEGORIAS = {
    1: "Muy seguro",
    2: "Seguro",
    3: "Ni seguro / Ni inseguro",
    4: "Inseguro",
    9: "NS/NR"
}

# Denominadores: Suma de fac_per por sexo y Total global
denominador_sexo = usuarios.groupby("sexo")["fac_per"].sum()
denominador_total = usuarios["fac_per"].sum()

# En las encuestas del IFT, los valores perdidos (NaN) a menudo se agrupan en NS/NR (9.0)
usuarios['seg_redes'] = usuarios['seg_redes'].fillna(9.0)

# Numeradores: Suma cruzando sexo y seg_redes
numerador_sexo = usuarios.groupby(["sexo", "seg_redes"])["fac_per"].sum().unstack(fill_value=0)

# Porcentajes por sexo
porcentajes_sexo = numerador_sexo.div(denominador_sexo, axis=0) * 100
porcentajes_sexo.index = porcentajes_sexo.index.map(GRUPOS_SEXO)

# Porcentajes Totales
numerador_total = usuarios.groupby("seg_redes")["fac_per"].sum()
porcentajes_total = (numerador_total / denominador_total) * 100

# Construir el DataFrame final (Esta es la parte corregida)
df_plot = porcentajes_sexo.copy()
df_plot.loc["Total"] = porcentajes_total  # Agregamos el total de forma directa y segura

# Renombrar columnas con las categorías
df_plot.rename(columns=CATEGORIAS, inplace=True)

# Agregar "Total" y asegurar el formato correcto a nivel columna
df_plot.rename(columns={"Ni seguro / Ni inseguro": "Ni seguro/\nNi inseguro"}, inplace=True)

# Reordenar filas sin problema
orden_filas = ["Hombres", "Mujeres", "Total"]
df_plot = df_plot.reindex(orden_filas)

# Transponer para que las categorías sean el eje Y
df_plot = df_plot.T

# Reordenar de arriba hacia abajo como en la imagen de referencia
orden_y = [
    "NS/NR",
    "Inseguro",
    "Ni seguro/\nNi inseguro",
    "Seguro",
    "Muy seguro"
]
df_plot = df_plot.reindex(orden_y)

# Reordenar las columnas para el trazado de barras de arriba a abajo en cada grupo
orden_col = ["Total", "Mujeres", "Hombres"]
df_plot = df_plot[orden_col]

# ── 4. Configuración de Gráfica ───────────────────────────────────────────────
COLORES = {
    "Total": "#a4d2cf",     # Aquamarine/Teal suave
    "Mujeres": "#f19883",   # Salmón
    "Hombres": "#2b6584"    # Azul oscuro
}

fig, ax = plt.subplots(figsize=(11, 7))

# Parámetros para barras agrupadas
n_grupos = len(df_plot.index)
bar_width = 0.22
indices = np.arange(n_grupos)

# Dibujar las barras
for i, col in enumerate(df_plot.columns):
    # Calcular la posición de cada barra en el grupo
    # Total en -bar_width (más arriba al invertir), Mujeres en 0, Hombres en +bar_width
    offset = (i - 1) * bar_width
    posiciones = indices + offset
    valores = df_plot[col]
    
    barras = ax.barh(
        posiciones, 
        valores, 
        height=bar_width * 0.9, 
        label=col, 
        color=COLORES[col],
        edgecolor='none'
    )
    
    # Etiquetas de datos (Porcentajes) al final de cada barra
    for barra in barras:
        ancho = barra.get_width()
        if ancho > 0:  
            ax.text(
                ancho + 1.0,           # Posición X (un poco a la derecha de la barra)
                barra.get_y() + barra.get_height()/2,  # Posición Y (centro de la barra)
                f"{ancho:.1f}%",       # Texto con 1 decimal
                va='center', 
                ha='left', 
                fontsize=9,
                fontweight='bold',
                color="#333333",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#f5f5f5", edgecolor="none")
            )

# ── 5. Formato de Ejes y Estilo ───────────────────────────────────────────────
ax.set_xlim(0, 68)  
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v)}%"))
ax.set_xticks(range(0, 70, 10))

# Invertir eje Y para que NS/NR quede hasta arriba
ax.invert_yaxis()

# Etiquetas del eje Y (Grupos)
ax.set_yticks(indices)
ax.set_yticklabels(df_plot.index, fontsize=10, color="#555")

# Eliminar espinas
ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
ax.tick_params(axis="both", length=0, labelsize=10, colors="#555")

# Cuadrícula: sin líneas o muy tenues para igualar el aspecto limpio
ax.xaxis.grid(False) 
ax.yaxis.grid(False)

# ── 6. Leyenda y Títulos ──────────────────────────────────────────────────────
# Crear leyenda circular/rectancular debajo del eje X
parches = [
    mpatches.Patch(color=COLORES["Total"], label="Total", capstyle='round'),
    mpatches.Patch(color=COLORES["Mujeres"], label="Mujeres", capstyle='round'),
    mpatches.Patch(color=COLORES["Hombres"], label="Hombres", capstyle='round')
]

ax.legend(
    handles=parches,
    loc="upper center",
    bbox_to_anchor=(0.5, -0.05),
    fontsize=10,
    frameon=False,
    ncol=3,
    handletextpad=0.5,
    handlelength=1.5
)

# Título y Notas (Alineados a la izquierda)
fig.text(
    0.05, 0.93,
    "Figura D.11. Porcentaje de la población usuaria de Internet, qué tan seguro es\n"
    "compartir información, en redes sociales (por sexo)",
    fontsize=12, fontweight="bold", color="#5c627f", ha="left"
)

fig.text(
    0.05, 0.05,
    "Fuente: IFT, con información de la Encuesta de Confianza en el Servicio de Internet (ECSI) 2024.\n"
    "Nota: Respuesta múltiple, por lo que la suma no da 100%. Es importante señalar que los resultados pueden presentar "
    "variaciones que pueden ser explicadas por el error teórico de cada encuesta.",
    fontsize=8, color="#555", ha="left"
)

# Ajuste general del lienzo
plt.subplots_adjust(left=0.18, right=0.95, top=0.85, bottom=0.2)

# Guardar o mostrar
plt.savefig(r"C:\Users\ivan-\Documents\GitHub\anuario\output\Figura_D11.png", dpi=300, facecolor="white", bbox_inches="tight")
plt.savefig(r"C:\Users\ivan-\Documents\GitHub\anuario\output\svg\Figura_D11.svg", dpi=300, format="svg", facecolor="white", bbox_inches="tight")
plt.show()