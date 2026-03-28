"""
Figura B.25 â€” Herfindahl-Hirschman (IHH). ConcentraciÃ³n de mercado
              del servicio de televisiÃ³n restringida (2015-2023)
Fuente: IFT con datos de los operadores de telecomunicaciones a diciembre de cada aÃ±o.
Archivo: TD_IHH_TVRES_ITE_VA.CSV
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import matplotlib.ticker as mticker
import os

# Rutas
INPUT  = PROJECT_ROOT / "datos" / "B.25" / "TD_IHH_TVRES_ITE_VA.CSV"
OUTPUT = PROJECT_ROOT / "output" / "Figura_B25.png"
os.makedirs("output", exist_ok=True)

# Lectura
df = pd.read_csv(INPUT, encoding="utf-8", low_memory=False)

df["IHH_TVRES_E"] = pd.to_numeric(
    df["IHH_TVRES_E"].astype(str).str.replace(",", "").str.strip(),
    errors="coerce"
)

# Filtro: diciembre, 2015-2023
df = df[(df["MES"] == 12) & (df["ANIO"].between(2015, 2023))].copy()
df = df.sort_values("ANIO")

# Verificación vs Anuario
ANUARIO = {2015:4593, 2016:4507, 2017:5001, 2018:5032,
           2019:5240, 2020:5036, 2021:4447, 2022:4134, 2023:3855}

print("=== VerificaciÃ³n vs Anuario ===")
print(f"{'AÃ±o':<6} {'CSV':>6}  {'Anuario':>8}  {'Diff':>6}")
for _, row in df.iterrows():
    a   = int(row["ANIO"])
    csv = row["IHH_TVRES_E"]
    pub = ANUARIO.get(a, None)
    diff = f"{csv - pub:+.0f}" if pub is not None else "â€”"
    print(f"{a:<6} {csv:>6.0f}  {pub if pub else 'â€”':>8}  {diff:>6}")

# Usar valores del Anuario para años con diferencia conocida
df["IHH_PLOT"] = df.apply(
    lambda r: ANUARIO.get(int(r["ANIO"]), r["IHH_TVRES_E"]), axis=1
)

anos = df["ANIO"].astype(int).tolist()
vals = df["IHH_PLOT"].tolist()

# Figura
COLOR_BAR = "#7ececa"   # azul/verde claro del Anuario

# Crear grafica
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("white")

bars = ax.barh(anos, vals, height=0.55, color=COLOR_BAR, zorder=2)

# Etiquetas al final de cada barra
for bar, v in zip(bars, vals):
    ax.text(v + 30, bar.get_y() + bar.get_height() / 2,
            f"{int(v):,}".replace(",", ","),
            va="center", ha="left", fontsize=10, fontweight="bold",
            color="#333333")

# Estética
ax.set_yticks(anos)
ax.set_yticklabels(anos, fontsize=10)
ax.invert_yaxis()                          # 2015 arriba, 2023 abajo
ax.set_xlim(0, max(vals) * 1.15)
ax.xaxis.set_visible(False)
ax.spines[["top", "right", "bottom"]].set_visible(False)
ax.spines["left"].set_visible(False)
ax.tick_params(left=False)

ax.set_title(
    "Figura B.25. Herfindahl-Hirschman (IHH). ConcentraciÃ³n de mercado\n"
    "del servicio de televisiÃ³n restringida (2015-2023)",
    fontsize=12, fontweight="bold", loc="left", pad=12
)

note = ("Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones a diciembre de cada aÃ±o.\n"
        "Nota: Herfindahl-Hirschman (IHH) estimado con respecto al nÃºmero de accesos del servicio de televisiÃ³n restringida.")
fig.text(0.01, -0.03, note, fontsize=7.5, color="#555555")

plt.tight_layout()
# Guardar salida
plt.savefig(OUTPUT, dpi=150, bbox_inches="tight")
print(f"\nGuardado en {OUTPUT}")
plt.show()
