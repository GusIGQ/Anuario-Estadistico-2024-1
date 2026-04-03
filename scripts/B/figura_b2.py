"""
Figura B.2 — Distribución de los Servicios Fijos con respecto del total
de hogares en las zonas rurales.
Fuente: IFT con datos de la ENDUTIH 2023, del INEGI.

Cómo correr:
    python figura_b2.py

Requisitos:
    pip install dbfread pandas matplotlib
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from dbfread import DBF

# ── 1. RUTA AL ARCHIVO ──────────────────────────────────────────────────────
DBF_PATH = r"C:\Users\ivan-\Documents\GitHub\anuario\datos\b.2\tic_2023_hogares.DBF"

# ── 2. CARGA Y PREPARACIÓN ───────────────────────────────────────────────────
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

# ── 3. FILTRO RURAL ──────────────────────────────────────────────────────────
rural = df[df["DOMINIO"] == "R"].copy()
total = rural["FAC_HOG"].sum()

print(f"Total hogares rurales ponderados: {total:,.0f}")

# ── 4. CÁLCULO DE VALORES ────────────────────────────────────────────────────
def pct(mask):
    return rural.loc[mask, "FAC_HOG"].sum() / total * 100

v = {}

# Nivel 1
v["tres"]    = pct(rural["num_servicios"] == 3)
v["dos"]     = pct(rural["num_servicios"] == 2)
v["uno"]     = pct(rural["num_servicios"] == 1)
v["ninguno"] = pct(rural["num_servicios"] == 0)

# Desglose un servicio
v["solo_tv"]  = pct((rural["tv_paga"]==1)        & (rural["internet_fijo"]==0) & (rural["tel_fija"]==0))
v["solo_tel"] = pct((rural["tel_fija"]==1)        & (rural["internet_fijo"]==0) & (rural["tv_paga"]==0))
v["solo_int"] = pct((rural["internet_fijo"]==1)   & (rural["tv_paga"]==0)      & (rural["tel_fija"]==0))

# Desglose dos servicios
v["int_tel"]  = pct((rural["internet_fijo"]==1) & (rural["tel_fija"]==1) & (rural["tv_paga"]==0))
v["tv_int"]   = pct((rural["tv_paga"]==1)       & (rural["internet_fijo"]==1) & (rural["tel_fija"]==0))
v["tv_tel"]   = pct((rural["tv_paga"]==1)       & (rural["tel_fija"]==1) & (rural["internet_fijo"]==0))

# Imprimir para verificación
print("\n── Valores calculados ──")
for k, val in v.items():
    print(f"  {k:12s}: {val:.1f}%")

# ── 5. FIGURA ────────────────────────────────────────────────────────────────
# Colores del Anuario IFT
C_NINGUNO = "#1B4F72"   # azul oscuro
C_UNO     = "#85C1E9"   # azul claro
C_DOS     = "#E74C3C"   # rojo/salmon
C_TRES    = "#F1948A"   # rosa claro
C_ACCENT  = "#E74C3C"

fig = plt.figure(figsize=(16, 9), facecolor="white")

# ── Pastel principal ─────────────────────────────────────────────────────────
ax_pie = fig.add_axes([0.22, 0.15, 0.38, 0.72])

sizes  = [v["ninguno"], v["uno"],   v["dos"],   v["tres"]]
colors = [C_NINGUNO,    C_UNO,      C_DOS,      C_TRES]
labels = ["Ninguno",    "Un\nservicio", "Dos\nservicios", "Tres\nservicios"]

wedges, texts = ax_pie.pie(
    sizes,
    colors=colors,
    startangle=90,
    counterclock=False,
    wedgeprops=dict(linewidth=1.5, edgecolor="white"),
)

# Etiquetas dentro del pastel
offsets = {
    "Ninguno":          (0.38,  0.10),
    "Un\nservicio":     (0.25, -0.38),
    "Dos\nservicios":   (-0.25,-0.28),
    "Tres\nservicios":  (-0.30, 0.20),
}
valores_pct = {
    "Ninguno":          v["ninguno"],
    "Un\nservicio":     v["uno"],
    "Dos\nservicios":   v["dos"],
    "Tres\nservicios":  v["tres"],
}
for label, (ox, oy) in offsets.items():
    val = valores_pct[label]
    ax_pie.text(ox, oy, f"{val:.0f}%", ha="center", va="center",
                fontsize=22, fontweight="bold", color="white")
    ax_pie.text(ox, oy - 0.13, label, ha="center", va="center",
                fontsize=9, color="white")

ax_pie.axis("equal")

# ── Caja central con total ───────────────────────────────────────────────────
ax_pie.text(0, 0.04, "Total de hogares en zonas",
            ha="center", va="center", fontsize=8, color="#1B4F72")
ax_pie.text(0, -0.07, "rurales en México:",
            ha="center", va="center", fontsize=8, color="#1B4F72")
ax_pie.text(0, -0.22, f"{total:,.0f}",
            ha="center", va="center", fontsize=14, fontweight="bold", color="#1B4F72")

# ── Panel "Un servicio" (derecha arriba) ─────────────────────────────────────
ax_un = fig.add_axes([0.62, 0.52, 0.36, 0.38])
ax_un.set_xlim(0, 1)
ax_un.set_ylim(0, 1)
ax_un.axis("off")

# Borde del panel
rect = FancyBboxPatch((0.01, 0.01), 0.97, 0.97,
                       boxstyle="round,pad=0.02",
                       linewidth=1.5, edgecolor="#85C1E9",
                       facecolor="white")
ax_un.add_patch(rect)
ax_un.text(0.5, 0.88, "Un servicio", ha="center", va="center",
           fontsize=11, fontweight="bold", color="#1B4F72")

# Tres mini-barras
datos_un = [
    ("Solo TV\nRestringida", v["solo_tv"],  C_UNO),
    ("Solo\nTelefonía",      v["solo_tel"], C_UNO),
    ("Solo Internet",        v["solo_int"], C_ACCENT),
]
xs = [0.18, 0.50, 0.82]
for (lbl, val, col), x in zip(datos_un, xs):
    # Círculo de color
    circ = plt.Circle((x, 0.58), 0.10, color=col, zorder=3)
    ax_un.add_patch(circ)
    ax_un.text(x, 0.58, f"{val:.0f}%",
               ha="center", va="center", fontsize=12,
               fontweight="bold", color="white", zorder=4)
    ax_un.text(x, 0.30, lbl, ha="center", va="center",
               fontsize=8, color="#555555", multialignment="center")

# ── Panel "Dos servicios" (derecha abajo) ────────────────────────────────────
ax_dos = fig.add_axes([0.62, 0.10, 0.36, 0.38])
ax_dos.set_xlim(0, 1)
ax_dos.set_ylim(0, 1)
ax_dos.axis("off")

rect2 = FancyBboxPatch((0.01, 0.01), 0.97, 0.97,
                        boxstyle="round,pad=0.02",
                        linewidth=1.5, edgecolor="#E74C3C",
                        facecolor="white")
ax_dos.add_patch(rect2)
ax_dos.text(0.5, 0.88, "Dos servicios", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#1B4F72")

datos_dos = [
    ("Internet +\nTelefonía",           v["int_tel"],  C_DOS),
    ("TV Restringida\n+ Internet",      v["tv_int"],   C_DOS),
    ("TV Restringida\n+ Telefonía",     v["tv_tel"],   C_DOS),
]
for (lbl, val, col), x in zip(datos_dos, xs):
    circ = plt.Circle((x, 0.58), 0.10, color=col, zorder=3)
    ax_dos.add_patch(circ)
    ax_dos.text(x, 0.58, f"{val:.0f}%",
                ha="center", va="center", fontsize=12,
                fontweight="bold", color="white", zorder=4)
    ax_dos.text(x, 0.30, lbl, ha="center", va="center",
                fontsize=8, color="#555555", multialignment="center")

# ── Título y fuente ──────────────────────────────────────────────────────────
fig.text(0.50, 0.94,
         "Figura B.2. Distribución de los Servicios Fijos con respecto\n"
         "del total de hogares en las zonas rurales",
         ha="center", va="center", fontsize=13, fontweight="bold", color="#1B4F72")

fig.text(0.05, 0.02,
         "Fuente: IFT con datos de la ENDUTIH 2023, del INEGI. "
         "Datos disponibles en https://www.inegi.org.mx/programas/endutih/2023/\n"
         "Nota: Los porcentajes pueden no sumar 100% debido al redondeo.",
         ha="left", va="center", fontsize=7, color="#555555")

# ── Guardar ──────────────────────────────────────────────────────────────────
os.makedirs("output", exist_ok=True)
plt.savefig("output/Figura_B2.png", dpi=150, bbox_inches="tight",
            facecolor="white")
#plt.savefig("output/Figura_B2.pdf", bbox_inches="tight", facecolor="white")
print("\nGuardado: output/Figura_B2.png y output/Figura_B2.pdf")
plt.show()
