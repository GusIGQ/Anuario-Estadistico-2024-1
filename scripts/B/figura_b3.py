"""
Figura B.3 — Distribución de los Servicios Fijos con respecto del total
de hogares en las zonas urbanas.
Fuente: IFT con datos de la ENDUTIH 2023, del INEGI.
Todos los valores se calculan desde el DBF — sin hardcodeo.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from dbfread import DBF

# ── 1. RUTA ──────────────────────────────────────────────────────────────────
DBF_PATH = r"C:\Users\ivan-\Documents\GitHub\anuario\datos\b.3\tic_2023_hogares.DBF"

# ── 2. CARGA ─────────────────────────────────────────────────────────────────
print("Cargando DBF...")
records = list(DBF(DBF_PATH, encoding="latin-1"))
df = pd.DataFrame(records)

for col in ["P4_4", "P4_5", "P5_1", "P5_5", "DOMINIO"]:
    df[col] = df[col].astype(str).str.strip()
df["FAC_HOG"] = pd.to_numeric(df["FAC_HOG"], errors="coerce").fillna(0)

df["internet_fijo"] = ((df["P4_4"] == "1") & (df["P4_5"].isin(["1", "3"]))).astype(int)
df["tv_paga"]       = (df["P5_1"] == "1").astype(int)
df["tel_fija"]      = (df["P5_5"] == "1").astype(int)
df["num_servicios"] = df["internet_fijo"] + df["tv_paga"] + df["tel_fija"]

# ── 3. FILTRO URBANO ─────────────────────────────────────────────────────────
urb   = df[df["DOMINIO"] == "U"].copy()
total = urb["FAC_HOG"].sum()
print(f"Total hogares urbanos ponderados: {total:,.0f}")

# ── 4. CÁLCULO ───────────────────────────────────────────────────────────────
def pct(mask):
    return urb.loc[mask, "FAC_HOG"].sum() / total * 100

v = {
    "tres":    pct(urb["num_servicios"] == 3),
    "dos":     pct(urb["num_servicios"] == 2),
    "uno":     pct(urb["num_servicios"] == 1),
    "ninguno": pct(urb["num_servicios"] == 0),
    "solo_tv":  pct((urb["tv_paga"]==1)        & (urb["internet_fijo"]==0) & (urb["tel_fija"]==0)),
    "solo_tel": pct((urb["tel_fija"]==1)        & (urb["internet_fijo"]==0) & (urb["tv_paga"]==0)),
    "solo_int": pct((urb["internet_fijo"]==1)   & (urb["tv_paga"]==0)      & (urb["tel_fija"]==0)),
    "int_tel":  pct((urb["internet_fijo"]==1)   & (urb["tel_fija"]==1)     & (urb["tv_paga"]==0)),
    "tv_int":   pct((urb["tv_paga"]==1)         & (urb["internet_fijo"]==1) & (urb["tel_fija"]==0)),
    "tv_tel":   pct((urb["tv_paga"]==1)         & (urb["tel_fija"]==1)     & (urb["internet_fijo"]==0)),
}

print("\n── Valores calculados ──")
for k, val in v.items():
    print(f"  {k:12s}: {val:.1f}%")

# ── 5. FIGURA ────────────────────────────────────────────────────────────────
C_NINGUNO = "#1B4F72"
C_UNO     = "#85C1E9"
C_DOS     = "#E74C3C"
C_TRES    = "#F1948A"
C_ACCENT  = "#E74C3C"

fig = plt.figure(figsize=(16, 9), facecolor="white")

# ── Pastel principal ─────────────────────────────────────────────────────────
ax_pie = fig.add_axes([0.22, 0.15, 0.38, 0.72])

sizes  = [v["ninguno"], v["uno"], v["dos"], v["tres"]]
colors = [C_NINGUNO,    C_UNO,   C_DOS,    C_TRES]

wedges, _ = ax_pie.pie(
    sizes,
    colors=colors,
    startangle=90,
    counterclock=False,
    wedgeprops=dict(linewidth=1.5, edgecolor="white"),
)
ax_pie.axis("equal")

# Posición de etiquetas dentro del pastel — se calculan con el ángulo del centroide
import numpy as np

def wedge_center(start_angle, end_angle, r=0.6):
    """Devuelve (x, y) del centroide de un sector."""
    mid = np.deg2rad((start_angle + end_angle) / 2)
    return r * np.cos(mid), r * np.sin(mid)

# Reconstruir ángulos acumulados (mismo orden que pie)
angles = []
cum = 90  # startangle=90, counterclock=False → restamos
for s in sizes:
    deg = s / 100 * 360
    end = cum - deg
    angles.append((cum, end))
    cum = end

labels_pie = {
    0: "Ninguno",
    1: "Un\nservicio",
    2: "Dos\nservicios",
    3: "Tres\nservicios",
}
vals_pie = [v["ninguno"], v["uno"], v["dos"], v["tres"]]

for i, (start, end) in enumerate(angles):
    cx, cy = wedge_center(start, end, r=0.60)
    ax_pie.text(cx, cy, f"{vals_pie[i]:.0f}%",
                ha="center", va="center", fontsize=20,
                fontweight="bold", color="white")
    ax_pie.text(cx, cy - 0.13, labels_pie[i],
                ha="center", va="center", fontsize=8.5, color="white")

# Caja central con total
ax_pie.text(0,  0.05, "Total de hogares en zonas",
            ha="center", fontsize=8, color="#1B4F72")
ax_pie.text(0, -0.06, "urbanas en México:",
            ha="center", fontsize=8, color="#1B4F72")
ax_pie.text(0, -0.21, f"{total:,.0f}",
            ha="center", fontsize=13, fontweight="bold", color="#1B4F72")

# ── Panel "Un servicio" ──────────────────────────────────────────────────────
ax_un = fig.add_axes([0.62, 0.52, 0.36, 0.38])
ax_un.set_xlim(0, 1); ax_un.set_ylim(0, 1); ax_un.axis("off")

ax_un.add_patch(FancyBboxPatch((0.01, 0.01), 0.97, 0.97,
    boxstyle="round,pad=0.02", linewidth=1.5,
    edgecolor="#85C1E9", facecolor="white"))
ax_un.text(0.5, 0.88, "Un servicio", ha="center",
           fontsize=11, fontweight="bold", color="#1B4F72")

xs = [0.18, 0.50, 0.82]
datos_un = [
    ("Solo TV\nRestringida", v["solo_tv"],  C_UNO),
    ("Solo\nTelefonía",      v["solo_tel"], C_UNO),
    ("Solo Internet",        v["solo_int"], C_ACCENT),
]
for (lbl, val, col), x in zip(datos_un, xs):
    ax_un.add_patch(plt.Circle((x, 0.58), 0.10, color=col, zorder=3))
    ax_un.text(x, 0.58, f"{val:.0f}%",
               ha="center", va="center", fontsize=11,
               fontweight="bold", color="white", zorder=4)
    ax_un.text(x, 0.29, lbl, ha="center", va="center",
               fontsize=7.5, color="#555", multialignment="center")

# ── Panel "Dos servicios" ────────────────────────────────────────────────────
ax_dos = fig.add_axes([0.62, 0.10, 0.36, 0.38])
ax_dos.set_xlim(0, 1); ax_dos.set_ylim(0, 1); ax_dos.axis("off")

ax_dos.add_patch(FancyBboxPatch((0.01, 0.01), 0.97, 0.97,
    boxstyle="round,pad=0.02", linewidth=1.5,
    edgecolor="#E74C3C", facecolor="white"))
ax_dos.text(0.5, 0.88, "Dos servicios", ha="center",
            fontsize=11, fontweight="bold", color="#1B4F72")

datos_dos = [
    ("Internet +\nTelefonía",        v["int_tel"], C_DOS),
    ("TV Restringida\n+ Internet",   v["tv_int"],  C_DOS),
    ("TV Restringida\n+ Telefonía",  v["tv_tel"],  C_DOS),
]
for (lbl, val, col), x in zip(datos_dos, xs):
    ax_dos.add_patch(plt.Circle((x, 0.58), 0.10, color=col, zorder=3))
    ax_dos.text(x, 0.58, f"{val:.0f}%",
                ha="center", va="center", fontsize=11,
                fontweight="bold", color="white", zorder=4)
    ax_dos.text(x, 0.29, lbl, ha="center", va="center",
                fontsize=7.5, color="#555", multialignment="center")

# ── Título y fuente ──────────────────────────────────────────────────────────
fig.text(0.50, 0.95,
         "Figura B.3. Distribución de los Servicios Fijos con respecto\n"
         "del total de hogares en las zonas urbanas",
         ha="center", fontsize=13, fontweight="bold", color="#1B4F72")

fig.text(0.05, 0.015,
         "Fuente: IFT con datos de la ENDUTIH 2023, del INEGI. "
         "Datos disponibles en https://www.inegi.org.mx/programas/endutih/2023/\n"
         "Nota: Los porcentajes pueden no sumar 100% debido al redondeo.",
         ha="left", fontsize=7, color="#555")

# ── Guardar ──────────────────────────────────────────────────────────────────
os.makedirs("output", exist_ok=True)
plt.savefig("output/Figura_B3.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.savefig("output/Figura_B3.pdf", bbox_inches="tight", facecolor="white")
print("\nGuardado: output/Figura_B3.png y output/Figura_B3.pdf")
plt.show()