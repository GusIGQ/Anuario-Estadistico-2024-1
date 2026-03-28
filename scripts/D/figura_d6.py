"""
Figura D.6 â€” Usuarios que han vivido experiencias negativas al utilizar Internet
             y/o realizar actividades en lÃ­nea, por sexo

Fuente : IFT, con informaciÃ³n de la Encuesta de Confianza en el Servicio de
         Internet (ECSI) 2024.
Archivo: baseconfianzadigital__1_.csv
         (descargable desde la secciÃ³n "Encuestas a Usuarios" en
          https://bit.ift.org.mx/BitWebApp/descargaDatos.xhtml)
Salida : output/Figura_D6.png

MetodologÃ­a
-----------
Universo  : Personas usuarias de Internet (rescate_internet == 1),
            mayores de 18 aÃ±os, levantamiento telefÃ³nico.
Factor    : fac_per  (factor de expansiÃ³n de personas â‰¥ 18 aÃ±os,
                      definido en el diccionario de la ECSI 2024).
Sexo      : sexo == 2 â†’ Hombres  |  sexo == 1 â†’ Mujeres
Variables : expp_mensnd  (P25_1_a) â€“ Le han enviado mensajes no deseados
            expp_pubipi  (P25_1_b) â€“ Han publicado informaciÃ³n personal sin permiso
            expp_datpre  (P25_1_d) â€“ Han usado sus datos para pedir prÃ©stamos/crÃ©ditos
            expp_robcon  (P25_1_e) â€“ Han robado sus contraseÃ±as
FÃ³rmula   : % = SUM(fac_per | var == 1) / SUM(fac_per) Ã— 100

Nota      : La encuesta usa respuesta mÃºltiple, por lo que los porcentajes
            no suman 100 %.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import matplotlib.patches as mpatches
import numpy as np

# 1. Rutas

OUT_DIR   = os.path.join(PROJECT_ROOT / "output")
CSV_PATH = os.path.join(PROJECT_ROOT / "datos" / "D.6" / "baseconfianzadigital.csv")

# 2. Carga y filtro
df = pd.read_csv(CSV_PATH, low_memory=False)

# Solo usuarios de Internet
usuarios = df[df["rescate_internet"] == 1].copy()

# 3. Variables de experiencias negativas
VARS = {
    "expp_mensnd": "Recibir mensajes\nno deseados",
    "expp_pubipi": "Han publicado informaciÃ³n\npersonal sin su permiso",
    "expp_datpre": "Han usado sus datos para pedir\nprÃ©stamos o crÃ©ditos sin su permiso",
    "expp_robcon": "Han robado sus contraseÃ±as",
}

GRUPOS = {
    "Hombres": usuarios[usuarios["sexo"] == 2],
    "Mujeres": usuarios[usuarios["sexo"] == 1],
    "Total"  : usuarios,
}

# 4. Cálculo de porcentajes ponderados
resultados = {}
for grupo, sub in GRUPOS.items():
    total_pond = sub["fac_per"].sum()
    resultados[grupo] = {}
    for var in VARS:
        n = sub[sub[var] == 1]["fac_per"].sum()
        resultados[grupo][var] = round(n / total_pond * 100, 1)

# Verificación en consola
print("Valores calculados:")
for grupo in GRUPOS:
    for var, etiqueta in VARS.items():
        print(f"  {grupo:8s} | {etiqueta.replace(chr(10),' ')[:45]:45s} : "
              f"{resultados[grupo][var]:.1f}%")
    print()

# 5. Estructura para la gráfica
categorias = list(VARS.keys())
etiquetas  = list(VARS.values())
n_cat      = len(categorias)

val_hombres = [resultados["Hombres"][v] for v in categorias]
val_mujeres = [resultados["Mujeres"][v] for v in categorias]
val_total   = [resultados["Total"][v]   for v in categorias]

# 6. Colores del Anuario
COLOR_HOMBRES = "#A8D5DC"   # azul-verde claro
COLOR_MUJERES = "#E8937A"   # salmÃ³n / naranja suave
COLOR_TOTAL   = "#1F4E6B"   # azul oscuro

# 7. Gráfica
x      = np.arange(n_cat)
ancho  = 0.22
offset = ancho + 0.02

# Crear grafica
fig, ax = plt.subplots(figsize=(13, 7))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

bars_h = ax.bar(x - offset, val_hombres, width=ancho,
                color=COLOR_HOMBRES, label="Hombres", zorder=3)
bars_m = ax.bar(x,           val_mujeres, width=ancho,
                color=COLOR_MUJERES, label="Mujeres", zorder=3)
bars_t = ax.bar(x + offset,  val_total,   width=ancho,
                color=COLOR_TOTAL,   label="Total",   zorder=3)

# Etiquetas sobre barras
def etiquetar(bars, valores):
    for bar, val in zip(bars, valores):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                f"{val:.1f}%",
                ha="center", va="bottom",
                fontsize=8.5, fontweight="bold",
                color="#333333")

etiquetar(bars_h, val_hombres)
etiquetar(bars_m, val_mujeres)
etiquetar(bars_t, val_total)

# 8. Formato de ejes
ax.set_xticks(x)
ax.set_xticklabels(etiquetas, fontsize=9, ha="center", color="#333333")
ax.set_ylim(0, 75)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.1f}%"))
ax.tick_params(axis="y", labelsize=9, colors="#555555")
ax.set_yticks(range(0, 80, 10))

# Líneas horizontales suaves
ax.yaxis.grid(True, linestyle="--", linewidth=0.5, color="#CCCCCC", zorder=0)
ax.set_axisbelow(True)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(axis="x", bottom=False)

# 9. Leyenda
legend_handles = [
    mpatches.Patch(facecolor=COLOR_HOMBRES, label="Hombres"),
    mpatches.Patch(facecolor=COLOR_MUJERES, label="Mujeres"),
    mpatches.Patch(facecolor=COLOR_TOTAL,   label="Total"),
]
ax.legend(handles=legend_handles, loc="upper right",
          frameon=False, fontsize=9.5,
          handlelength=1.2, handleheight=1.0)

# 10. Títulos y notas
ax.set_title(
    "Figura D.6. Usuarios que han vivido experiencias negativas al utilizar\n"
    "Internet y/o realizar actividades en lÃ­nea, por sexo",
    fontsize=11, fontweight="bold", color="#1F4E6B",
    pad=14, loc="left"
)

nota = (
    "Fuente: IFT, con informaciÃ³n de la Encuesta de Confianza en el Servicio de Internet (ECSI) 2024.\n"
    "Nota: Respuesta mÃºltiple, por lo que la suma no da 100%. La Encuesta de Confianza en el Servicio\n"
    "de Internet (ECSI) 2024 fue levantada mediante entrevistas telefÃ³nicas realizadas a personas de\n"
    "18 aÃ±os y mÃ¡s."
)
fig.text(0.01, -0.04, nota, fontsize=7.5, color="#555555",
         ha="left", va="top", wrap=True)

plt.tight_layout()

# 11. Guardar
out_path = os.path.join(OUT_DIR, "Figura_D6.png")
# Guardar salida
plt.savefig(out_path, dpi=150, bbox_inches="tight",
            facecolor="white", edgecolor="none")
plt.close()
print(f"\nFigura guardada en: {out_path}")
