import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
from pathlib import Path

# Rutas
INPUT  = PROJECT_ROOT / "datos" / "b.16" / "TD_ACC_BAF_XT_XC_VA.csv"
OUTPUT = PROJECT_ROOT / "output" / "Figura_B16.png"
Path(OUTPUT).parent.mkdir(parents=True, exist_ok=True)

# Lectura
df = pd.read_csv(INPUT, encoding="cp1252")

# Normalizar nombre duplicado
df["TECNO_ACCESO_INTERNET"] = df["TECNO_ACCESO_INTERNET"].str.strip()
df["TECNO_ACCESO_INTERNET"] = df["TECNO_ACCESO_INTERNET"].replace(
    {"TecnologÃ­a MÃ³vil": "TecnologÃ­a mÃ³vil"}
)

# Filtros
TECNO_PRINCIPALES = ["Fibra Ã³ptica", "Cable coaxial", "DSL",
                     "TecnologÃ­a mÃ³vil", "Satelital"]

def get_totals(year, mes=12):
    d = df[(df["ANIO"] == year) & (df["MES"] == mes)]
    d = d[d["TECNO_ACCESO_INTERNET"].isin(TECNO_PRINCIPALES)]
    res   = d.groupby("TECNO_ACCESO_INTERNET")["A_RESIDENCIAL_E"].sum()
    nores = d.groupby("TECNO_ACCESO_INTERNET")["A_NO_RESIDENCIAL_E"].sum()
    return res.reindex(TECNO_PRINCIPALES, fill_value=0), \
           nores.reindex(TECNO_PRINCIPALES, fill_value=0)

res23,  nores23  = get_totals(2023)
res22,  nores22  = get_totals(2022)

# Tasas de crecimiento
def tasa(v23, v22):
    return {t: ((v23[t] - v22[t]) / v22[t] * 100) if v22[t] > 0 else 0
            for t in TECNO_PRINCIPALES}

tc_res  = tasa(res23,  res22)
tc_nores = tasa(nores23, nores22)

total_res  = res23.sum()
total_nores = nores23.sum()
tc_total_res  = (total_res  - res22.sum())  / res22.sum()  * 100
tc_total_nores = (total_nores - nores22.sum()) / nores22.sum() * 100

# Colores por tecnología
COLORS = {
    "Fibra Ã³ptica":    "#1B3A6B",   # azul oscuro
    "Cable coaxial":   "#F4956A",   # salmÃ³n
    "DSL":             "#7EC8C8",   # azul claro
    "TecnologÃ­a mÃ³vil":"#B0D8E8",   # azul pÃ¡lido
    "Satelital":       "#E8E8E8",   # gris claro
}
BAR_POS = "#1B3A6B"   # azul para tasas positivas
BAR_NEG = "#7EC8C8"   # azul claro para tasas negativas

# Función: gráfica de pastel + barras de tasas
def draw_panel(ax_pie, ax_bar, totals, tc, total, tc_total, title):
    # Pastel
    sizes  = [totals[t] for t in TECNO_PRINCIPALES]
    colors = [COLORS[t] for t in TECNO_PRINCIPALES]
    wedges, _ = ax_pie.pie(
        sizes, colors=colors, startangle=90,
        wedgeprops=dict(width=1, edgecolor="white", linewidth=1.5)
    )
    ax_pie.set_aspect("equal")

    # Etiquetas radiales
    label_cfg = {
        "Fibra Ã³ptica":     (0.55, 0.50, "white",  12, "bold"),
        "Cable coaxial":    (0.70, 0.10, "white",  11, "bold"),
        "DSL":              (0.75,-0.30, "#333333", 10, "bold"),
        "TecnologÃ­a mÃ³vil": (0.85, 0.75, "#333333", 9,  "normal"),
        "Satelital":        (0.88,-0.65, "#333333", 9,  "normal"),
    }
    for t, (rx, ry, fc, fs, fw) in label_cfg.items():
        pct = totals[t] / total * 100
        if pct < 0.05:
            continue
        ax_pie.text(rx, ry, f"{t}\n{pct:.1f}%",
                    ha="center", va="center",
                    fontsize=fs, fontweight=fw, color=fc)

    # Total nacional
    ax_pie.text(0, -1.45, f"Accesos {'residenciales' if 'Res' in title else 'no residenciales'}\na nivel nacional:",
                ha="center", fontsize=8, color="#555555")
    ax_pie.text(0, -1.75, f"{int(total):,}",
                ha="center", fontsize=14, fontweight="bold", color="#1B3A6B")

    # Tasa total
    ax_pie.text(0, -2.1,
                f"Tasa de crecimiento\nanual de {tc_total:.1f}%",
                ha="center", fontsize=8, color="#555555")

    ax_pie.set_title(title, fontsize=13, fontweight="bold",
                     color="#1B3A6B", pad=10)

    # Barras de tasas
    # Solo tecnologías con datos relevantes
    tecno_bar = [t for t in TECNO_PRINCIPALES
                 if abs(tc[t]) > 0.05 and totals[t] > 0
                 and t not in ("Satelital",)]
    vals  = [tc[t] for t in tecno_bar]
    cols  = [BAR_POS if v >= 0 else BAR_NEG for v in vals]
    ypos  = np.arange(len(tecno_bar))

    ax_bar.barh(ypos, vals, color=cols, height=0.5, zorder=3)
    ax_bar.axvline(0, color="#888888", linewidth=0.8, zorder=2)

    for i, (v, t) in enumerate(zip(vals, tecno_bar)):
        offset = 1.5 if v >= 0 else -1.5
        ha = "left" if v >= 0 else "right"
        ax_bar.text(v + offset, i, f"{v:.1f}%",
                    va="center", ha=ha, fontsize=8, fontweight="bold",
                    color="#1B3A6B" if v >= 0 else "#7EC8C8")

    ax_bar.set_yticks(ypos)
    ax_bar.set_yticklabels([t.replace(" ", "\n") for t in tecno_bar], fontsize=8)
    ax_bar.set_xlim(min(vals) * 1.6, max(vals) * 1.6)
    ax_bar.set_title("Tasa de crecimiento anual,\ndiciembre 2022 - diciembre 2023",
                     fontsize=8, color="#555555")
    ax_bar.spines[["top","right","bottom"]].set_visible(False)
    ax_bar.tick_params(axis="x", which="both", bottom=False, labelbottom=False)
    ax_bar.grid(False)

# Layout
fig = plt.figure(figsize=(16, 8))
fig.patch.set_facecolor("white")

# 4 subplots: pastel_res barras_res pastel_nores barras_nores
gs = fig.add_gridspec(1, 4, width_ratios=[2, 1, 2, 1], wspace=0.35,
                      left=0.04, right=0.97, top=0.82, bottom=0.08)

ax_pie_r  = fig.add_subplot(gs[0])
ax_bar_r  = fig.add_subplot(gs[1])
ax_pie_nr = fig.add_subplot(gs[2])
ax_bar_nr = fig.add_subplot(gs[3])

draw_panel(ax_pie_r,  ax_bar_r,  res23,   tc_res,   total_res,   tc_total_res,   "Residencial")
draw_panel(ax_pie_nr, ax_bar_nr, nores23, tc_nores, total_nores, tc_total_nores, "No Residencial")

# Título
fig.text(0.02, 0.95,
         "â— Figura B.16. DistribuciÃ³n de los accesos al servicio fijo de Internet "
         "por tecnologÃ­a de conexiÃ³n y por segmento",
         fontsize=10, fontweight="bold", color="#1B3A6B", va="top")

# Fuente
fig.text(0.02, 0.02,
         "Fuente: IFT con datos de los operadores de telecomunicaciones a diciembre de 2023.",
         fontsize=8, color="#666666")

# Guardar salida
plt.savefig(OUTPUT, dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print(f"Figura guardada en: {OUTPUT}")

# Verificación
print("\nâ”€â”€ Residencial 2023 â”€â”€")
for t in TECNO_PRINCIPALES:
    pct = res23[t] / total_res * 100
    print(f"  {t:25s}: {pct:5.1f}%   tc: {tc_res[t]:+.1f}%")
print(f"  {'TOTAL':25s}: {total_res:,.0f}   tc: {tc_total_res:+.1f}%")

print("\nâ”€â”€ No Residencial 2023 â”€â”€")
for t in TECNO_PRINCIPALES:
    pct = nores23[t] / total_nores * 100
    print(f"  {t:25s}: {pct:5.1f}%   tc: {tc_nores[t]:+.1f}%")
print(f"  {'TOTAL':25s}: {total_nores:,.0f}   tc: {tc_total_nores:+.1f}%")
