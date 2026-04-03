# /usr/bin/env python3
# - - coding: utf-8 - -
"""
Figura A.6 - Ingresos, egresos y margen en el sector de telecomunicaciones.

Calculos:
- Ingresos = suma trimestral de INGRESOS_TOTAL_E / 1,000,000,000
- Margen$ = Ingresos * Margen%
- Egresos = Ingresos - Margen$
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()

def to_number(value: object) -> float:
    if pd.isna(value):
        return 0.0
    text = str(value).strip().replace(",", "")
    if text in {"", "-", "nan", "None"}:
        return 0.0
    try:
        return float(text)
    except ValueError:
        return 0.0

def build_series(data_file: Path) -> pd.DataFrame:
    # Cargar datos
    df = pd.read_csv(data_file, encoding="latin1", low_memory=False)
    df.columns = [c.strip() for c in df.columns]

    df = df[df["I_ANUAL_TRIM"].astype(str).str.strip().eq("Trimestral")].copy()
    df["INGRESOS_TOTAL_E"] = df["INGRESOS_TOTAL_E"].apply(to_number)

    df = df[(df["ANIO"] >= 2017) & (df["ANIO"] <= 2023)].copy()

    ingresos = (
        df.groupby(["ANIO", "TRIM"], as_index=False)["INGRESOS_TOTAL_E"]
        .sum()
        .sort_values(["ANIO", "TRIM"])
    )
    ingresos["ingresos_bn"] = ingresos["INGRESOS_TOTAL_E"] / 1_000_000_000

    # Margen leido de la figura original (2017T1 ... 2023T4).
    margen_pct = [
        20, 17, 15, 13,
        21, 20, 17, 17,
        25, 25, 26, 27,
        22, 15, 17, 17,
        17, 17, 29, 32,
        32, 30, 30, 30,
        31, 30, 33, 29,
    ]

    if len(ingresos) != len(margen_pct):
        raise ValueError(
            f"Esperados 28 trimestres, se encontraron {len(ingresos)} en el archivo."
        )

    ingresos["margen_pct"] = margen_pct
    ingresos["margen_bn"] = ingresos["ingresos_bn"] * ingresos["margen_pct"] / 100.0
    ingresos["egresos_bn"] = ingresos["ingresos_bn"] - ingresos["margen_bn"]

    return ingresos

def make_chart(df: pd.DataFrame, output_png: Path) -> None:
    egresos_color = "#2C6F96"
    margen_color = "#A9CFD5"
    text_color = "#3A4670"

    x = np.arange(len(df))
    width = 0.78

    # Crear grafica
    fig, ax = plt.subplots(figsize=(14.5, 9.0))
    fig.patch.set_facecolor("#F3F4F6")
    ax.set_facecolor("#F3F4F6")

    ax.bar(x, df["egresos_bn"], width=width, color=egresos_color, linewidth=0, label="Egresos")
    ax.bar(
        x,
        df["margen_bn"],
        width=width,
        bottom=df["egresos_bn"],
        color=margen_color,
        linewidth=0,
        label="Margen",
    )

    # Etiquetas de porcentaje de margen y valor total de ingresos.
    for i, row in df.iterrows():
        y_margin_center = row["egresos_bn"] + row["margen_bn"] / 2
        ax.text(
            i,
            y_margin_center,
            f"{int(row['margen_pct'])}%",
            ha="center",
            va="center",
            fontsize=10,
            color=text_color,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.25", fc="#EEF0F5", ec="none"),
        )

        ax.text(
            i,
            row["ingresos_bn"] + 1.2,
            f"{row['ingresos_bn'] * 1000:,.0f}",
            rotation=90,
            ha="center",
            va="bottom",
            fontsize=8.5,
            color="#5C6B91",
        )

    ax.set_ylim(0, float(df["ingresos_bn"].max() * 1.22))

    # Eje X: trimestre en cada barra y ano centrado por bloque de cuatro trimestres.
    trim_labels = ["I", "II", "III", "IV"] * 7
    ax.set_xticks(x)
    ax.set_xticklabels(trim_labels, fontsize=10, color=text_color)

    years = sorted(df["ANIO"].unique())
    for idx, year in enumerate(years):
        center = idx * 4 + 1.5
        ax.text(
            center,
            -8.5,
            str(year),
            ha="center",
            va="top",
            fontsize=10,
            color=text_color,
            fontweight="bold",
            clip_on=False,
        )

    ax.set_yticks([])
    ax.tick_params(left=False, bottom=False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.text(0.03, 0.952, "Figura A.6. ", fontsize=16, fontweight="bold", color=text_color)
    fig.text(
        0.145,
        0.952,
        "Ingresos, egresos y margen en el sector de telecomunicaciones",
        fontsize=16,
        color=text_color,
    )

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.09),
        ncol=2,
        frameon=False,
        fontsize=11,
        labelcolor=text_color,
        handlelength=1.3,
        handletextpad=0.5,
    )

    fig.text(
        0.03,
        0.06,
        "Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones a diciembre de 2023.",
        fontsize=10.5,
        color=text_color,
        fontweight="bold",
    )
    fig.text(
        0.03,
        0.04,
        "Notas: Cifras en miles de millones de pesos (pesos corrientes de cada ano).",
        fontsize=10.5,
        color=text_color,
    )

    fig.subplots_adjust(left=0.05, right=0.99, top=0.9, bottom=0.19)
    output_png.parent.mkdir(parents=True, exist_ok=True)
    # Guardar salida
    fig.savefig(output_png, dpi=240, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)

def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    data_file = repo_root / "datos" / "A.6" / "TD_INGRESOS_TELECOM_ITE_VA.csv"
    output_png = repo_root / "output" / "Figura_A6.png"

    series_df = build_series(data_file)
    make_chart(series_df, output_png)

    print("Figura generada:", output_png)
    print(series_df[["ANIO", "TRIM", "ingresos_bn", "margen_pct", "margen_bn", "egresos_bn"]].to_string(index=False))

if __name__ == "__main__":
    main()
