# /usr/bin/env python3
# - - coding: utf-8 - -
"""
Script para generar la Figura A.4: InversiÃ³n privada en Telecomunicaciones por tipo de inversiÃ³n
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
import numpy as np
import locale
from pathlib import Path
import sys

# Configurar locale para formato de números en español
try:
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Spanish_Spain.1252')
    except:
        print("No se pudo configurar el locale espaÃ±ol")

# Configurar matplotlib para español
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'

def clean_numeric_column(col):
    """Limpia columnas numÃ©ricas que pueden tener comas y espacios"""
    if pd.isna(col):
        return 0.0
    if isinstance(col, (int, float)):
        return col
    # Convertir a string y limpiar
    col_str = str(col).strip()
    # Si es un guión o está vacío, retornar 0
    if col_str == '-' or col_str == '' or col_str == 'nan':
        return 0.0
    try:
        # Remover espacios y comas, convertir a float
        return float(col_str.replace(',', '').replace(' ', ''))
    except (ValueError, TypeError):
        return 0.0

def main():
    # Rutas de archivos
    base_path = Path(__file__).parent.parent
    data_file = base_path / "datos" / "A.4" / "TD_INVERSION_TELECOM_ITE_VA.csv"
    output_dir = base_path / "output"

    # Crear directorio de salida si no existe
    output_dir.mkdir(exist_ok=True)

    print(f"Leyendo datos desde: {data_file}")

    # Leer el archivo CSV
    try:
        # Cargar datos
        df = pd.read_csv(data_file, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(data_file, encoding='latin1')
        except Exception as e:
            print(f"Error leyendo el archivo: {e}")
            return

    print(f"Datos cargados: {len(df)} filas")
    print(f"Columnas: {list(df.columns)}")
    print(f"AÃ±os disponibles: {sorted(df['ANIO'].unique())}")

    # Usar los nombres exactos de las columnas con espacios
    investment_cols = [' INV_INFRA_E ', ' INV_ACT_NO_TANG_E  ', ' INV_OTRO_ACT_E ', ' INV_NO_ESP_E ', ' INV_TOTAL_E ']

    # Limpiar y convertir columnas numéricas
    for col in investment_cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_numeric_column)

    # Filtrar años 2013-2023 (según la figura)
    df_filtered = df[(df['ANIO'] >= 2013) & (df['ANIO'] <= 2023)].copy()

    print(f"Datos filtrados (2013-2023): {len(df_filtered)} filas")

    # Agrupar por año y sumar inversiones (en miles de pesos)
    yearly_totals = df_filtered.groupby('ANIO')[investment_cols].sum()

    # Convertir a miles de millones de pesos
    yearly_totals_billions = yearly_totals / 1_000_000

    print("Totales por aÃ±o (miles de millones de pesos):")
    print(yearly_totals_billions)

    # Preparar datos para la gráfica
    years = yearly_totals_billions.index.tolist()
    infra = yearly_totals_billions[' INV_INFRA_E '].values
    otros = yearly_totals_billions[' INV_OTRO_ACT_E '].values 
    no_tangibles = yearly_totals_billions[' INV_ACT_NO_TANG_E  '].values
    no_especificada = yearly_totals_billions[' INV_NO_ESP_E '].values
    totals = yearly_totals_billions[' INV_TOTAL_E '].values

    # Configurar la figura
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))

    # Definir colores según la imagen
    colors = {
        'infra': '#2E5984',        # Azul oscuro para infraestructura
        'otros': '#A8CDF0',        # Azul claro para otros activos
        'no_tangibles': '#1A365D', # Azul muy oscuro para activos no tangibles
        'no_especificada': '#E53E3E' # Rojo para no especificada
    }

    # Crear barras apiladas
    width = 0.6
    x_pos = np.arange(len(years))

    # Crear las barras apiladas
    p1 = ax.bar(x_pos, infra, width, color=colors['infra'], label='Infraestructura')
    p2 = ax.bar(x_pos, otros, width, bottom=infra, color=colors['otros'], label='Otros Activos')
    p3 = ax.bar(x_pos, no_tangibles, width, bottom=infra+otros, color=colors['no_tangibles'], label='Activos No Tangibles')
    p4 = ax.bar(x_pos, no_especificada, width, bottom=infra+otros+no_tangibles, color=colors['no_especificada'], label='No Especificada')

    # Configurar ejes
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_title('')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(years)

    # Añadir etiquetas de valores totales y porcentajes
    for i, (year, total) in enumerate(zip(years, totals)):
        # Valor total en la parte superior
        ax.text(i, total + total*0.02, f'${total:.1f}', 
                ha='center', va='bottom', fontweight='bold', fontsize=9)

        # Calcular porcentajes
        if total > 0:
            pct_infra = (infra[i] / total) * 100
            pct_otros = (otros[i] / total) * 100 
            pct_no_tangibles = (no_tangibles[i] / total) * 100
            pct_no_especificada = (no_especificada[i] / total) * 100

            # Añadir porcentajes en las barras (solo si son significativos)
            cumm = 0
            if pct_infra > 5:  # Solo mostrar si es mayor a 5%
                y_pos = cumm + infra[i]/2
                ax.text(i, y_pos, f'{pct_infra:.1f}%', ha='center', va='center', 
                       color='white', fontweight='bold', fontsize=8)
            cumm += infra[i]

            if pct_otros > 5:
                y_pos = cumm + otros[i]/2
                ax.text(i, y_pos, f'{pct_otros:.1f}%', ha='center', va='center',
                       color='black', fontweight='bold', fontsize=8)
            cumm += otros[i]

            if pct_no_tangibles > 5:
                y_pos = cumm + no_tangibles[i]/2  
                ax.text(i, y_pos, f'{pct_no_tangibles:.1f}%', ha='center', va='center',
                       color='white', fontweight='bold', fontsize=8)
            cumm += no_tangibles[i]

            if pct_no_especificada > 5:
                y_pos = cumm + no_especificada[i]/2
                ax.text(i, y_pos, f'{pct_no_especificada:.1f}%', ha='center', va='center',
                       color='white', fontweight='bold', fontsize=8)

    # Configurar leyenda
    ax.legend(loc='upper right', bbox_to_anchor=(1.0, 1.0), frameon=False)

    # Configurar límites del eje Y
    ax.set_ylim(0, max(totals) * 1.1)

    # Eliminar bordes superiores e izquierdos
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Configurar grid sutil
    ax.grid(True, axis='y', alpha=0.3, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)

    # Añadir título y texto descriptivo
    fig.suptitle('Figura A.4. InversiÃ³n privada en Telecomunicaciones por tipo de inversiÃ³n', 
                 fontsize=14, fontweight='bold', color='#CC7A00', x=0.02, y=0.95, ha='left')

    # Añadir cuadro de texto con descripción
    description = ("La inversiÃ³n privada total realizada por los\n"
                  "operadores de telecomunicaciones en 2023\n" 
                  "fue de $55.7 mil millones de pesos. De la cual,\n"
                  "la mayor parte fue dirigida a infraestructura\n"
                  "con un 72.8% del total de la inversiÃ³n en el\n"
                  "sector.")

    # Crear cuadro de texto
    textbox_props = dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='gray')
    ax.text(0.02, 0.98, description, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=textbox_props)

    # Añadir nota al pie
    note = ("Fuente: IFT con datos proporcionados por los operadores de telecomunicaciones. Para cada aÃ±o la inversiÃ³n se presenta acumulada al mes de diciembre.\n"
           "Notas: Cifras en miles de millones de pesos (pesos corrientes de cada aÃ±o). Solo se considera la inversiÃ³n realizada por operadores de servicios de telecomunicaciones.")

    fig.text(0.02, 0.02, note, fontsize=8, style='italic', wrap=True)

    # Ajustar layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.85, bottom=0.15)

    # Guardar la figura
    output_file = output_dir / "Figura_A4.png"
    # Guardar salida
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Figura guardada en: {output_file}")
    plt.close(fig)

if __name__ == "__main__":
    main()
