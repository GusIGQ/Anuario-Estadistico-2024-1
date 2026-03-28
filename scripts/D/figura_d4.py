"""
Figura D.4 â€” Uso de dispositivos inteligentes conectados a Internet
Fuente: IFT con datos de la ENDUTIH 2023, del INEGI.
https://www.inegi.org.mx/programas/endutih/2023/

Archivo de entrada : tr_endutih_usuarios2_anual_2023.csv
Salida             : Figura_D4.png

Variables usadas (pregunta 9.1 del cuestionario):
  P9_1_1  â†’ Bocina o asistente del hogar
  P9_1_2  â†’ Sistemas de videovigilancia
  P9_1_3  â†’ Puertas o ventanas con cerrado digital
  P9_1_4  â†’ Dispositivos de ahorro de energÃ­a elÃ©ctrica
  P9_1_5  â†’ Luces o interruptores
  P9_1_6  â†’ ConexiÃ³n elÃ©ctrica (soquet o enchufes)
  P9_1_7  â†’ ElectrodomÃ©sticos
  P9_1_8  â†’ Dispositivos de entretenimiento (Smart TV, DVD, Blu-ray)
  P9_1_9  â†’ AutomÃ³vil o camioneta
  P9_1_10 â†’ Otros dispositivos
  FAC_PER â†’ Factor de expansiÃ³n de persona

Denominador clave:
  El 100% NO es la totalidad de usuarios de internet,
  sino Ãºnicamente las personas que usan AL MENOS UN
  dispositivo IoT (P9_1_1 a P9_1_10 con valor '1').
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
import matplotlib.ticker as mtick
from pathlib import Path

# CONFIGURACI N ajusta esta ruta a tu máquina

RUTA_CSV = Path(
    PROJECT_ROOT / "datos" / "D.4" / "tr_endutih_usuarios2_anual_2023.csv"
)
SALIDA   = Path(PROJECT_ROOT / "output" / "Figura_D4.png")

# 1. LEER DATOS

print("Leyendo datosâ€¦")
# Cargar datos
df = pd.read_csv(RUTA_CSV, low_memory=False)
df["FAC_PER"] = pd.to_numeric(df["FAC_PER"], errors="coerce")
print(f"  Registros totales : {len(df):>10,}")
print(f"  PoblaciÃ³n ponderada: {df['FAC_PER'].sum():>15,.0f}")

# 2. DEFINIR VARIABLES Y ORDEN (igual que el Anuario)

VARS_IOT = [
    "P9_1_1","P9_1_2","P9_1_3","P9_1_4","P9_1_5",
    "P9_1_6","P9_1_7","P9_1_8","P9_1_9","P9_1_10",
]

# Orden descendente exacto del Anuario
ORDEN = [
    ("P9_1_8",  "Dispositivos de\nentretenimiento"),
    ("P9_1_1",  "Bocina o\nasistente del\nhogar"),
    ("P9_1_2",  "Sistemas de\nvideovigilancia"),
    ("P9_1_5",  "Luces o\ninterruptores"),
    ("P9_1_7",  "Electro-\ndomÃ©sticos"),
    ("P9_1_6",  "ConexiÃ³n\nelÃ©ctrica"),
    ("P9_1_3",  "Puertas o\nventanas con\ncerrado digital"),
    ("P9_1_9",  "AutomÃ³vil\no camioneta"),
    ("P9_1_4",  "Dispositivos\nde ahorro de\nenergÃ­a elÃ©ctrica"),
    ("P9_1_10", "Otros\ndispositivos"),
]

# 3. CALCULAR DENOMINADOR
# Solo personas que usan al menos un dispositivo IoT

usa_alguno = (
    df[VARS_IOT]
    .apply(lambda col: col.astype(str).str.strip() == "1")
    .any(axis=1)
)
total_iot = df.loc[usa_alguno, "FAC_PER"].sum()

print(f"\n  Usuarios con â‰¥1 dispositivo IoT (ponderado): {total_iot:,.0f}")
print(f"  ({total_iot / df['FAC_PER'].sum() * 100:.1f}% del total de usuarios)\n")

# 4. CALCULAR PORCENTAJES

ESPERADOS = {
    "P9_1_8": 59.6, "P9_1_1": 55.0, "P9_1_2": 21.0,
    "P9_1_5":  9.9, "P9_1_7":  5.0, "P9_1_6":  5.0,
    "P9_1_3":  3.7, "P9_1_9":  2.9, "P9_1_4":  2.6, "P9_1_10": 0.2,
}

variables, etiquetas, porcentajes = [], [], []
print("=== VALIDACIÃ“N vs ANUARIO ===")
for var, etiq in ORDEN:
    mascara = df[var].astype(str).str.strip() == "1"
    pct     = df.loc[mascara, "FAC_PER"].sum() / total_iot * 100
    esp     = ESPERADOS[var]
    estado  = "âœ…" if abs(pct - esp) < 0.05 else "âš ï¸"
    print(f"  {var:8s}  {etiq.replace(chr(10),' '):42s}  "
          f"calculado={pct:.1f}%  esperado={esp}%  {estado}")
    variables.append(var)
    etiquetas.append(etiq)
    porcentajes.append(round(pct, 1))

# 5. GRAFICAR

COLOR_ALTO = "#C0392B"   # rojo fuerte  â€” barras â‰¥ 10 %
COLOR_BAJO = "#E8A89C"   # rojo claro   â€” barras <  10 %

colores = [COLOR_ALTO if p >= 10 else COLOR_BAJO for p in porcentajes]

# Crear grafica
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor("white")

bars = ax.bar(
    range(len(porcentajes)),
    porcentajes,
    color=colores,
    width=0.55,
    zorder=3,
)

# Etiquetas de valor sobre cada barra
for bar, val in zip(bars, porcentajes):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.6,
        f"{val:.1f}%",
        ha="center", va="bottom",
        fontsize=9.5, fontweight="bold", color="#222222",
    )

# Eje X
ax.set_xticks(range(len(etiquetas)))
ax.set_xticklabels(etiquetas, fontsize=8.5, ha="center", color="#333333",
                   linespacing=1.3)
ax.tick_params(axis="x", length=0, pad=6)

# Eje Y
ax.set_ylim(0, 75)
ax.set_yticks([0, 10, 20, 30, 40, 50, 60, 70])
ax.set_yticklabels(["0.0%","10.0%","20.0%","30.0%",
                    "40.0%","50.0%","60.0%","70.0%"],
                   fontsize=9, color="#555555")
ax.yaxis.set_tick_params(length=0)

# Rejilla y marcos
ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
ax.spines[["top","right","left","bottom"]].set_visible(False)

# Título
ax.set_title(
    "Figura D.4. Uso de dispositivos inteligentes conectados a Internet",
    fontsize=11.5, fontweight="bold", loc="left", pad=14,
    color="#111111",
)

# Nota de fuente
fig.text(
    0.01, -0.02,
    "Fuente: IFT con datos de la ENDUTIH 2023, del INEGI. "
    "Datos disponibles en https://www.inegi.org.mx/programas/endutih/2023/.",
    fontsize=7.5, color="#666666",
)

plt.tight_layout(rect=[0, 0.02, 1, 1])
# Guardar salida
plt.savefig(SALIDA, dpi=150, bbox_inches="tight", facecolor="white")
print(f"\nGuardada: {SALIDA.resolve()}")
plt.show()
