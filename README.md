# Proyecto: Reproducción de Gráficas del Anuario Estadístico 2024 del IFT

## Objetivo

Reproducir **todas las figuras** del Anuario Estadístico 2024 del IFT usando Python,
generando gráficas idénticas al PDF original a partir de los datos fuente descargados
de las páginas del INEGI e IFT. Este Anuario saco de un link: [https://www.ift.org.mx/sites/default/files/contenidogeneral/estadisticas/anuarioestadistico2024vf_0.pdf](https://www.ift.org.mx/sites/default/files/contenidogeneral/estadisticas/anuarioestadistico2024vf_0.pdf).

---

## Flujo de trabajo por cada figura

```
1. Identificar la figura en el PDF
2. Obtener el enlace exacto de descarga del archivo fuente
3. Descargar el archivo (Excel/CSV) a la carpeta de datos correspondiente
4. Leer el archivo e identificar filas, columnas y hojas relevantes
5. Realizar los cálculos necesarios con ayuda de charlie charlie (si aplica)
6. Generar la gráfica con el estilo visual del IFT
7. Documentar todo en la ficha técnica (ver formato abajo)
8. Exportar la gráfica en PNG (200 DPI)
```

## Estructura de carpetas

```
practica 1 - Copy/
│
├── README.md                    ← Este archivo
│
├── datos/                       ← Archivos fuente descargados
│   ├── tabulados_PIBT/          ← PIB Trimestral (INEGI) - YA DESCARGADO
│   ├── telecom_fija/            ← Datos de telecomunicaciones fijas
│   ├── telecom_movil/           ← Datos de telecomunicaciones móviles
│   ├── internet/                ← Datos de internet y banda ancha
│   ├── radiodifusion/           ← Datos de radiodifusión
│   ├── audiovisual/             ← Datos de contenidos audiovisuales
│   ├── mapas/                   ← Shapefiles de México (si se necesitan)
│   └── otros/                   ← Otros archivos fuente
│
├── scripts/                     ← Scripts de Python por figura
│   ├── figura_a1.py             ← Figura A.1 - YA COMPLETADA
│   ├── figura_1_1.py
│   ├── figura_1_2.py
│   └── ...
│
├── output/                      ← Gráficas generadas (PNG)
│   ├── Figura_A1.png
│   ├── Figura_1_1.png
│   └── ...
│
└── reporte/                     ← Documentación y reporte final
    └── fichas_tecnicas.md       ← Ficha técnica de cada figura
```

---

## Formato de ficha técnica por figura

Para cada gráfica se documenta lo siguiente:

```
### Figura X.X — [Título de la figura]

**Enlace de descarga del archivo fuente:**
- URL: [enlace exacto de donde se descargó el archivo]

**Archivo local:**
- Ruta: datos/[carpeta]/[archivo.xlsx]
- Hoja: [nombre de la hoja]

**Datos utilizados:**
- Fila(s): [número de fila y concepto]
- Columna(s): [rango de columnas, trimestres/años]

**Cálculos realizados:**
- [Descripción de fórmulas aplicadas]
- Ejemplo: % TyR = (Fila 155 + Fila 154) / Fila 7 × 100

**Tipo de gráfica:** [barras, línea, pastel, mapa, etc.]

**Script:** scripts/figura_X_X.py
**Output:** output/Figura_X_X.png
```

---

## Ejemplo completado: Figura A.1

### Figura A.1 — Producto Interno Bruto (PIB) y contribución del PIB de los subsectores de telecomunicaciones y radiodifusión

**Enlace de descarga del archivo fuente:**

- URL: [https://www.inegi.org.mx/temas/pib/](https://www.inegi.org.mx/temas/pib/) → Tabulados → PIBT (PIB Trimestral)

**Archivo local:**

- Ruta: datos/tabulados_PIBT/PIBT_2.xlsx
- Hoja: Tabulado

**Datos utilizados:**

- Fila 7: `B.1bP - Producto interno bruto` (PIB total)
- Fila 154: `515 - Radio y televisión`
- Fila 155: `517 - Telecomunicaciones`
- Columnas: T1 a T4 de cada año (cada año ocupa 7 columnas: T1,T2,T3,T4,6M,9M,Anual)
- Rango temporal: 2013-T1 a 2024-T2

**Cálculos realizados:**

- Barras (eje izq): PIB en miles de millones = Fila 7 ÷ 1,000
- Línea (eje der): % TyR = (Fila 155 + Fila 154) ÷ Fila 7 × 100

**Tipo de gráfica:** Barras con gradiente + línea con marcadores (doble eje Y)

**Script:** scripts/figura_a1.py
**Output:** output/Figura_A1.png

---

## Inventario de figuras

| # | Figura | Título                 | Tipo            | Datos fuente               | Estado        |
| - | ------ | ----------------------- | --------------- | -------------------------- | ------------- |
| 1 | A.1    | PIB y contribución TyR | Barras + línea | tabulados_PIBT/PIBT_2.xlsx | ✅ Completada |
| 2 |        |                         |                 |                            | ⬜ Pendiente  |
| 3 |        |                         |                 |                            | ⬜ Pendiente  |

> **Nota:** Completar este inventario conforme se identifiquen las figuras del PDF.
> El usuario proporcionará los enlaces de descarga de cada archivo fuente.

---

## Tipos de gráficas esperadas y herramientas

| Tipo de gráfica               | Librería Python       | Notas                           |
| ------------------------------ | ---------------------- | ------------------------------- |
| Barras verticales/horizontales | matplotlib             | Ya implementado en A.1          |
| Líneas / series de tiempo     | matplotlib             | —                              |
| Pastel / dona                  | matplotlib             | `ax.pie()`                    |
| Barras apiladas                | matplotlib             | `ax.bar(bottom=...)`          |
| Mapas de México               | geopandas + matplotlib | Requiere shapefile de entidades |
| Treemap                        | squarify               | `pip install squarify`        |
| Dispersión / puntos           | matplotlib             | —                              |

---

## Paleta de colores estilo IFT

```python
# Colores principales del Anuario IFT 2024
IFT_PURPURA_OSCURO = '#2B1055'
IFT_PURPURA         = '#7B2D8E'
IFT_AZUL_CLARO      = '#7597C9'
IFT_GRIS            = '#6B6B6B'
IFT_LILA            = '#8B78A8'
IFT_FONDO           = '#F8F8FA'
IFT_TEXTO           = '#333333'
IFT_TEXTO_CLARO     = '#555555'
IFT_BORDE           = '#CCCCCC'
```

---

## Cómo reportar el trabajo

### Opción recomendada: Reporte técnico con fichas

1. **Portada**: Título, nombre, asesor (Iván), fecha
2. **Índice de figuras**: Lista de todas las figuras reproducidas
3. **Por cada figura**:
   - Captura de la gráfica generada
   - Ficha técnica (enlace, archivo, filas, columnas, cálculos)
   - Comparación visual con el original (opcional)
4. **Conclusiones**: Hasta ahora replicamos las figuras A.1 a A.10. Existe discrepancia entre los datos originales y los calculados. Los datos descargados son datos crudos, mientras que el PDF del anuario presenta datos procesados y redondeados.

 El anuario dice  "La información reportada está sujeta a revisiones y a modificaciones derivadas de cambios que realizan los operadores a las cifras previamente reportadas." por lo que es posible que algunas cifras hayan cambiado desde la descarga de los datos, lo cual podría explicar diferencias con el PDF original.

### Formato de entrega

- **PDF**: Más profesional para entrega académica
- **Word (.docx)**: Fácil de editar, se puede generar con python-docx
- **Excel**: Útil si el asesor quiere verificar los datos crudos

---

## Dependencias Python

```bash
py -m pip install pandas openpyxl matplotlib numpy
# Adicionales (instalar cuando se necesiten):
py -m pip install geopandas shapely     # Para mapas
py -m pip install squarify              # Para treemaps  
py -m pip install python-docx           # Para exportar a Word
py -m pip install reportlab             # Para exportar a PDF
```

---

## Vinculo del reporte final

- Índice de figuras: [reporte/indice_figuras.md](reporte/indice_figuras.md)
- Fichas técnicas: [reporte/fichas_tecnicas.md](reporte/fichas_tecnicas.md)
- Complemento técnico A.1-A.10: [README_complemento.md](README_complemento.md)
