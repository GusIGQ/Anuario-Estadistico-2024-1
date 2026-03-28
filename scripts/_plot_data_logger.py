"""Utilities to print plotted data for traceability in figure scripts."""

from __future__ import annotations

import os
from typing import Any

def _safe_text(value: Any) -> str:
    try:
        return str(value)
    except Exception:
        return repr(value)

def _to_compact_list(values: Any) -> list[Any]:
    try:
        if hasattr(values, "tolist"):
            data = values.tolist()
        else:
            data = list(values)
    except Exception:
        return []

    if isinstance(data, list) and len(data) > 60:
        return data[:30] + ["..."] + data[-30:]
    return data if isinstance(data, list) else [data]

def _print_series_like(title: str, x_vals: Any, y_vals: Any) -> bool:
    x_list = _to_compact_list(x_vals)
    y_list = _to_compact_list(y_vals)
    n = min(len(x_list), len(y_list))
    if n == 0:
        return False

    print(f"\n{title}")
    print("idx\tx\ty")
    for i in range(n):
        print(f"{i}\t{_safe_text(x_list[i])}\t{_safe_text(y_list[i])}")
    return True

def _print_scatter(title: str, offsets: Any) -> bool:
    try:
        points = offsets.tolist() if hasattr(offsets, "tolist") else list(offsets)
    except Exception:
        return False

    if not points:
        return False

    if len(points) > 80:
        points = points[:40] + [["...", "..."]] + points[-40:]

    print(f"\n{title}")
    print("idx\tx\ty")
    for i, pair in enumerate(points):
        if isinstance(pair, (list, tuple)) and len(pair) >= 2:
            print(f"{i}\t{_safe_text(pair[0])}\t{_safe_text(pair[1])}")
    return True

def _print_pandas_fallback() -> bool:
    try:
        import pandas as pd  # type: ignore
    except Exception:
        return False

    import __main__

    printed = False
    for name, value in vars(__main__).items():
        if isinstance(value, pd.DataFrame):
            if value.empty or len(value) > 500:
                continue
            printed = True
            print(f"\n[datos-procesados][DataFrame] {name} shape={value.shape}")
            try:
                print(value.to_string(index=False))
            except Exception:
                print(value)
        elif isinstance(value, pd.Series):
            if value.empty or len(value) > 500:
                continue
            printed = True
            print(f"\n[datos-procesados][Series] {name} len={len(value)}")
            try:
                print(value.to_string())
            except Exception:
                print(value)

    return printed

def _print_figure_data(fig: Any, origin: str) -> None:
    if os.environ.get("ANUARIO_DISABLE_AUTO_PRINT") == "1":
        return

    if getattr(fig, "_anuario_data_printed", False):
        return

    print(f"\n=== Datos procesados para grafica ({origin}) ===")
    printed = False

    axes = getattr(fig, "axes", []) or []
    for ax_idx, ax in enumerate(axes, start=1):
        for line_idx, line in enumerate(getattr(ax, "lines", []), start=1):
            if _print_series_like(
                f"[Axes {ax_idx}] Linea {line_idx}: {line.get_label()}",
                line.get_xdata(orig=False),
                line.get_ydata(orig=False),
            ):
                printed = True

        for cont_idx, container in enumerate(getattr(ax, "containers", []), start=1):
            patches = getattr(container, "patches", [])
            if not patches:
                continue
            print(f"\n[Axes {ax_idx}] Barras {cont_idx}")
            print("idx\tx\ty")
            local_printed = False
            for i, patch in enumerate(patches):
                try:
                    x_val = patch.get_x() + patch.get_width() / 2
                    y_val = patch.get_height()
                    print(f"{i}\t{_safe_text(x_val)}\t{_safe_text(y_val)}")
                    local_printed = True
                except Exception:
                    continue
            printed = printed or local_printed

        for coll_idx, coll in enumerate(getattr(ax, "collections", []), start=1):
            get_offsets = getattr(coll, "get_offsets", None)
            if callable(get_offsets):
                if _print_scatter(f"[Axes {ax_idx}] Dispersion {coll_idx}", get_offsets()):
                    printed = True

    if not printed:
        printed = _print_pandas_fallback()

    if not printed:
        print("(No se detectaron series trazadas ni DataFrames/Series pequenos para imprimir)")

    setattr(fig, "_anuario_data_printed", True)

def enable_plot_data_logging() -> None:
    """Install Matplotlib save/show hooks once per process."""
    try:
        import matplotlib.figure as mpl_figure  # type: ignore
        import matplotlib.pyplot as plt  # type: ignore
    except Exception:
        return

    if getattr(mpl_figure.Figure, "_anuario_hook_installed", False):
        return

    original_figure_savefig = mpl_figure.Figure.savefig
    original_pyplot_savefig = plt.savefig
    original_show = plt.show

    # Guardar salida
    def wrapped_figure_savefig(self: Any, *args: Any, **kwargs: Any) -> Any:
        _print_figure_data(self, "savefig")
        return original_figure_savefig(self, *args, **kwargs)

    def wrapped_pyplot_savefig(*args: Any, **kwargs: Any) -> Any:
        try:
            _print_figure_data(plt.gcf(), "pyplot.savefig")
        except Exception:
            pass
        return original_pyplot_savefig(*args, **kwargs)

    def wrapped_show(*args: Any, **kwargs: Any) -> Any:
        try:
            _print_figure_data(plt.gcf(), "show")
        except Exception:
            pass
        return original_show(*args, **kwargs)

    mpl_figure.Figure.savefig = wrapped_figure_savefig
    plt.savefig = wrapped_pyplot_savefig
    plt.show = wrapped_show
    setattr(mpl_figure.Figure, "_anuario_hook_installed", True)
