"""
Figura D.5 â€” Â¿CÃ³mo aprendiÃ³ a buscar informaciÃ³n o usar el Internet?
             (Porcentaje de personas usuarias de Internet)

Fuente : IFT, con informaciÃ³n de la Encuesta de Confianza en el Servicio de
         Internet (ECSI) 2024.
Archivo: baseconfianzadigital__1_.csv
         (descargable desde la secciÃ³n "Encuestas a Usuarios" en
          https://bit.ift.org.mx/BitWebApp/descargaDatos.xhtml)
Salida : output/Figura_D5.png

MetodologÃ­a
-----------
Universo  : Personas usuarias de Internet (rescate_internet == 1).
Factor    : fac_per  (factor de expansiÃ³n de personas â‰¥ 18 aÃ±os).
Variables : apren_uso_int_1  (P13_1) â€“ Por su cuenta (Sin ayuda)
            apren_uso_int_2  (P13_2) â€“ CapacitaciÃ³n en el trabajo
            apren_uso_int_3  (P13_3) â€“ Curso en la escuela
            apren_uso_int_4  (P13_4) â€“ Curso en centro comunitario
            apren_uso_int_5  (P13_5) â€“ Curso particular
            apren_uso_int_6  (P13_6) â€“ Amigos o familiares
            apren_uso_int_8  (P13_8) â€“ Otros
            apren_uso_int_9  (P13_9) â€“ NS/NR
FÃ³rmula   : % = SUM(fac_per | var == 1) / SUM(fac_per) Ã— 100

Nota      : Respuesta mÃºltiple â€” los porcentajes no suman 100 %.
            Los porcentajes consideran el diseÃ±o muestral de la encuesta.
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
import matplotlib.ticker as mticker
import numpy as np

# 1. Rutas
DATOS_DIR = os.path.join(PROJECT_ROOT / "datos" / "D.5")
OUT_DIR   = os.path.join(PROJECT_ROOT / "output")

CSV_PATH = os.path.join(PROJECT_ROOT / "datos" / "D.5" / "baseconfianzadigital.csv")

# 2. Carga y filtro
df       = pd.read_csv(CSV_PATH, low_memory=False)
usuarios = df[df["rescate_internet"] == 1].copy()

# 3. Variables en el orden del Anuario
VARS = {
    "apren_uso_int_1": "Por su cuenta",
    "apren_uso_int_2": "CapacitaciÃ³n en\nel trabajo",
    "apren_uso_int_3": "Curso en la escuela",
    "apren_uso_int_4": "Curso en\ncentro comunitario",
    "apren_uso_int_5": "Curso particular",
    "apren_uso_int_6": "Amigos o familiares",
    "apren_uso_int_8": "Otros",
    "apren_uso_int_9": "NS/NR",
}

# 4. Cálculo ponderado
total_pond = usuarios["fac_per"].sum()
resultados = {}
for var, etiqueta in VARS.items():
    n = usuarios[usuarios[var] == 1]["fac_per"].sum()
    resultados[etiqueta] = round(n / total_pond * 100, 1)

# Verificación en consola
print("Valores calculados:")
for etiqueta, pct in resultados.items():
    print(f"  {etiqueta.replace(chr(10),' '):35s}: {pct:.1f}%")

# 5. Estructura para la gráfica
etiquetas = list(resultados.keys())
valores   = list(resultados.values())
n_cat     = len(etiquetas)
x         = np.arange(n_cat)

# Colores: barra destacada (Por su cuenta) en rojo-salmón,
# resto en azul oscuro / azul medio, igual que el Anuario
COLORES = [
    "#E8937A",  # Por su cuenta          â†’ salmÃ³n/rojo (barra mÃ¡s alta)
    "#E8937A",  # CapacitaciÃ³n trabajo   â†’ salmÃ³n
    "#1F4E6B",  # Curso escuela          â†’ azul oscuro
    "#A8D5DC",  # Curso centro comunit.  â†’ azul claro
    "#A8D5DC",  # Curso particular       â†’ azul claro
    "#1F4E6B",  # Amigos o familiares    â†’ azul oscuro
    "#A8D5DC",  # Otros                  â†’ azul claro
    "#A8D5DC",  # NS/NR                  â†’ azul claro
]

# 6. Gráfica
fig, ax = plt.subplots(figsize=(13, 7))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

bars = ax.bar(x, valores, width=0.55, color=COLORES, zorder=3)

# Etiquetas sobre cada barra
for bar, val in zip(bars, valores):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.4,
        f"{val:.1f}%",
        ha="center", va="bottom",
        fontsize=9, fontweight="bold", color="#333333"
    )

# 7. Formato de ejes
ax.set_xticks(x)
ax.set_xticklabels(etiquetas, fontsize=9, ha="center", color="#333333")
ax.set_ylim(0, 65)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{int(v)}%"))
ax.set_yticks(range(0, 70, 10))
ax.tick_params(axis="y", labelsize=9, colors="#555555")

ax.yaxis.grid(True, linestyle="--", linewidth=0.5, color="#CCCCCC", zorder=0)
ax.set_axisbelow(True)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(axis="x", bottom=False)

# 8. Título y notas
ax.set_title(
    "Figura D.5. Â¿CÃ³mo aprendiÃ³ a buscar informaciÃ³n o usar el Internet?\n"
    "(Porcentaje de personas usuarias de Internet)",
    fontsize=11, fontweight="bold", color="#1F4E6B",
    pad=14, loc="left"
)

nota = (
    "Fuente: IFT, con informaciÃ³n de la Encuesta de Confianza en el Servicio de Internet (ECSI) 2024.\n"
    "Nota: Los porcentajes reportados consideran el diseÃ±o muestral de la encuesta."
)
fig.text(0.01, -0.02, nota, fontsize=7.5, color="#555555", ha="left", va="top")

plt.tight_layout()

# 9. Guardar
out_path = os.path.join(OUT_DIR, "Figura_D5.png")
# Guardar salida
plt.savefig(out_path, dpi=150, bbox_inches="tight",
            facecolor="white", edgecolor="none")
plt.close()
print(f"\nFigura guardada en: {out_path}")
