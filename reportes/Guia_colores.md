# Anuario Estadístico — Guía para Gráficas

**Comisión Reguladora de Telecomunicaciones (CRT)**

---

## Colores para operadores

Se usarán para gráficas que requieran distinguir a los diferentes operadores.

| Operador  | Color | Hex         |
| --------- | ----- | ----------- |
| Altán    | 🟥    | `#8e244d` |
| Telcel    | 🟪    | `#753d6a` |
| Sky       | 🟣    | `#b35aba` |
| Megacable | 🟦    | `#5844a0` |
| AT&T      | 🩶    | `#667489` |
| Otros     | 🩶    | `#728781` |
| Telmex    | 🟦    | `#1e6284` |
| Movistar  | 🩵    | `#368491` |
| Bait      | 🟩    | `#1b4044` |
| CFE       | 🟩    | `#4ead82` |
| Totalplay | 🟨    | `#99b554` |
| Izzi      | 🟧    | `#ed8945` |

---

## Colores institucionales

Se recomiendan para gráficas que incluyan información a nivel país y como apoyo para destacar elementos visuales.

### Gobierno de México

| Hex         |
| ----------- |
| `#012f2a` |
| `#006157` |
| `#671435` |
| `#9b2247` |
| `#9d792a` |
| `#d3b771` |

### CRT

| Hex         |
| ----------- |
| `#1a4043` |
| `#4a7d75` |
| `#2D7B8A` |
| `#6cacad` |

---

## Paletas monocromáticas

Se recomienda usarlas en treemaps y mapas coropléticos para mostrar la intensidad de los datos, usando tonalidades claras para valores bajos y oscuras para altos.

### Paleta teal

`#86adae` → `#64a0a1` → `#5c9596` → `#4c7d7e` → `#3b6667` → `#335a5c` → `#234244` → `#132b2d`

### Paleta gris-verde

`#afafaf` → `#737f7c` → `#577771` → `#2d4f4b` → `#012f2a`

### Paleta rosa-vino

`#bca0ab` → `#b18193` → `#a5627c` → `#2d4f4b` → `#8e244d`

### Paleta morado

`#9d97c1` → `#837ba9` → `#696091` → `#4e4478` → `#8e244d`

### Paleta naranja-café

`#e2ba9f` → `#d9a785` → `#d0936b` → `#c68051` → `#bd6d37`

---

## Tipografía y Estilos de Texto

**Fuente:** Noto Sans
**Color de texto general:** `#3c3c3b`

| Elemento                        | Estilo y Tamaño sugerido       |
| ------------------------------- | ------------------------------- |
| Título de la gráfica          | Noto Sans**Bold** (14 pt) |
| Subtítulo de la gráfica       | Noto Sans Medium #3c3c3b        |
| Texto del eje X                 | Noto Sans**Bold** (10 pt) |
| Texto del eje Y                 | Noto Sans Medium (10 pt)        |
| Texto de las etiquetas de datos | Noto Sans**Bold** (9 pt)  |
| Texto de la leyenda             | Noto Sans**Bold** (10 pt) |
| Notas al pie / Fuentes          | Noto Sans Regular (8 pt)        |

> **Nota sobre etiquetas de datos:** Se debe cuidar la posición de las etiquetas (offset) para evitar que los números se solapen entre sí o con las líneas de la gráfica, garantizando una lectura limpia.

---

## Ejes y Cuadrícula

| Elemento                        | Grosor | Color       | Estilo Adicional                                                    |
| ------------------------------- | ------ | ----------- | ------------------------------------------------------------------- |
| Línea base y ejes principales  | 1 pt   | `#7c7c7c` | Quitar bordes superior y derecho.                                   |
| Línea auxiliar (cuadrícula Y) | 1 pt   | `#d1d1d1` | Solo líneas horizontales.                                          |
| Ticks del eje X                 | 0 pt   | `#7c7c7c` | Longitud 0 (invisibles), separación (pad) de 8 pt respecto al eje. |

---

## Guía por tipo de gráfica

### Barras y Líneas — Referencia canónica: Figura A.1

> Esta sección documenta el estilo visual completo implementado en `scripts/A/figura_a1.py`.
> Debe usarse como referencia para cualquier gráfica del mismo tipo (barras + línea con doble eje Y).

---

#### Configuración general de la figura

| Parámetro                                      | Valor                                                        |
| ----------------------------------------------- | ------------------------------------------------------------ |
| Tamaño (`figsize`)                           | `(16, 8.5)` pulgadas                                       |
| DPI de exportación                             | `200`                                                      |
| Fondo de la figura (`fig.patch`)              | `white`                                                    |
| Fondo del área del gráfico (`ax.facecolor`) | `#F8F8FA`                                                  |
| Márgenes (`subplots_adjust`)                 | `left=0.08`, `right=0.92`, `top=0.85`, `bottom=0.22` |

---

#### Barras

| Parámetro            | Valor                                        |
| --------------------- | -------------------------------------------- |
| Color de relleno      | `#86adae`                                  |
| Borde                 | ninguno (`edgecolor='none'`)               |
| Ancho (`bar_width`) | `0.72`                                     |
| `zorder`            | `2` (sobre la cuadrícula, bajo la línea) |

---

#### Línea (eje Y derecho)

| Parámetro             | Valor                                   |
| ---------------------- | --------------------------------------- |
| Color de línea        | `#2c3e40`                             |
| Grosor (`linewidth`) | `1` pt                                |
| Marcador               | Círculo (`marker='o'`)               |
| Tamaño del marcador   | `6`                                   |
| Relleno del marcador   | `#2c3e40` (mismo color que la línea) |
| Borde del marcador     | ninguno (`markeredgecolor='none'`)    |
| `zorder`             | `4` (encima de todo)                  |

---

#### Chips / anotaciones de porcentaje

Se colocan únicamente en los trimestres **II** y **IV** sobre los puntos de la línea.

| Parámetro        | Valor                                          |
| ----------------- | ---------------------------------------------- |
| Formato del texto | `f'{pct:.1f}%'`                              |
| Tamaño de fuente | `8` pt                                       |
| Peso de fuente    | `bold`                                       |
| Color de texto    | `#3c3c3b`                                    |
| Offset vertical   | `+12` puntos sobre el punto                  |
| Forma del chip    | `boxstyle='round,pad=0.3,rounding_size=0.8'` |
| Fondo del chip    | `white`                                      |
| Borde del chip    | `#2c3e40`, grosor `0.8` pt                 |

---

#### Ejes Y (izquierdo y derecho)

| Parámetro                  | Eje izquierdo (PIB)       | Eje derecho (%)          |
| --------------------------- | ------------------------- | ------------------------ |
| Color de etiqueta del eje   | `#3c3c3b`               | `#3c3c3b`              |
| Tamaño de etiqueta del eje | `11` pt                 | `11` pt                |
| `labelpad`                | `15`                    | `20`                   |
| Rotación                   | `90°` (default)        | `90°`                 |
| Tamaño de tick labels      | `9` pt                  | `9` pt                 |
| Color de tick labels        | `#3c3c3b`               | `#3c3c3b`              |
| Formato numérico           | Miles con coma:`15,000` | Porcentaje:`1.2%`      |
| Locator (separación)       | `MultipleLocator(5000)` | `MultipleLocator(0.2)` |
| Límites                    | `(0, 30000)`            | `(0, 1.8)`             |

---

#### Eje X — Dos niveles de etiquetas (trimestres + años)

El eje X usa un esquema de **dos líneas**:

1. **Nivel superior (ticks directos):** Solo se muestran `'II'` y `'IV'` (Q2 y Q4). Q1 y Q3 quedan vacíos (`''`).

   - Tamaño: `8` pt | Peso: `normal` | Color: `#3c3c3b`
   - Longitud de ticks: `3` pt | Color de ticks: `#3c3c3b`
2. **Nivel inferior (años, con `ax.text`):** El año se centra entre su primer y último trimestre.

   - Posición Y: `-1700` (unidades del eje izquierdo) — debajo del eje
   - Tamaño: `10` pt | Peso: `bold` | Color: `#3c3c3b`
   - Alineación: `ha='center'`, `va='top'`

---

#### Encabezado de la figura (título con cuadrado decorativo)

El encabezado se construye con **tres anotaciones separadas** sobre el área del gráfico, todas ancladas en `xy=(0, 1), xycoords='axes fraction'` (esquina superior izquierda).

| Elemento                                            | Descripción                                        | Parámetros clave                                                                                                                                             |
| --------------------------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Cuadrado decorativo**                       | Parche verde redondeado antes del número de figura | `xytext=(0, 30)`, `boxstyle='round,pad=1.6,rounding_size=0.2'`, `facecolor='#4a7d75'`, `edgecolor='none'`, `fontsize=2` (el texto es solo espacios) |
| **Número de figura** (`"Figura A.1."`)     | Bold, alineado después del cuadrado                | `xytext=(15, 30)`, `fontsize=14`, `fontweight='bold'`, `color='#3c3c3b'`                                                                              |
| **Título / subtítulo** (descripción larga) | Medium, continúa en la misma línea                | `xytext=(95, 30)`, `fontsize=14`, `fontweight='medium'`, `color='#3c3c3b'`                                                                            |

> El cuadrado decorativo (`#4a7d75`) actúa como ícono de identificación visual de la sección/figura.
> El número de figura va en **Bold** y el texto descriptivo en **Medium**, ambos en `14 pt`.

---

#### Leyenda

| Parámetro         | Valor                                                                       |
| ------------------ | --------------------------------------------------------------------------- |
| Ubicación         | `lower center` de la figura completa (`fig.legend`)                     |
| `bbox_to_anchor` | `(0.5, 0.08)`                                                             |
| Columnas           | `2`                                                                       |
| Tamaño de fuente  | `10` pt                                                                   |
| Marco              | Sin marco (`frameon=False`)                                               |
| `handlelength`   | `2.5`                                                                     |
| Ícono de barra    | `mpatches.Patch(facecolor='#86adae', edgecolor='none')`                   |
| Ícono de línea   | `Line2D` con `marker='o'`, `markersize=6`, `linewidth=1`, sin borde |

---

#### Notas al pie y Fuente

Las notas y fuente se colocan con `ax.annotate` usando `xycoords='figure fraction'`.

| Parámetro                                        | Valor                                                     |
| ------------------------------------------------- | --------------------------------------------------------- |
| Tamaño de fuente                                 | `8` pt                                                  |
| Color                                             | `#3c3c3b`                                               |
| X de inicio (`x_start`)                         | `0.08` (fracción de figura)                            |
| Ancho de texto envuelto (`textwrap.fill width`) | `225` caracteres                                        |
| Interlineado (`linespacing`)                    | `1.5`                                                   |
| **"Fuente:"**                               | `fontweight='bold'`, posición `y=0.06`               |
| Contenido de Fuente                               | Normal (`fontweight='normal'`), offset `(+35, 0)` pts |
| **"Notas:"**                                | `fontweight='bold'`, posición `y=0.042`              |
| Contenido de Notas                                | Normal (`fontweight='normal'`), offset `(+32, 0)` pts |

> Las etiquetas `"Fuente:"` y `"Notas:"` van en **bold** y el texto que las sigue en **normal**, ambos en `8 pt`.

---

#### Bordes, spines y cuadrícula

| Elemento                             | Valor                                                                                      |
| ------------------------------------ | ------------------------------------------------------------------------------------------ |
| Borde superior (`top`)             | **Oculto** en ambos ejes                                                             |
| Bordes izquierdo, derecho e inferior | Color `#7c7c7c`, visible                                                                 |
| Cuadrícula                          | Solo eje Y (`axis='y'`), color `#d1d1d1`, `linewidth=1`, `alpha=1.0`, `zorder=0` |

---

#### Fuente tipográfica

```python
plt.rcParams['font.family'] = ['Noto Sans', 'DejaVu Sans', 'sans-serif']
```

Fallback en orden: **Noto Sans → DejaVu Sans → sans-serif genérico**.

---

#### Exportación

```python
fig.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white', edgecolor='none')
```

---

### Líneas / Series de Tiempo (2 series) — Referencia canónica: Figura A.3

> Esta sección documenta el estilo visual completo implementado en `scripts/A/figura_a3.py`.
> Debe usarse como referencia para cualquier gráfica de líneas con dos series y un solo eje Y.

---

#### Configuración general de la figura

| Parámetro                                      | Valor                                                        |
| ----------------------------------------------- | ------------------------------------------------------------ |
| Tamaño (`figsize`)                           | `(16, 8.5)` pulgadas                                       |
| DPI de exportación                             | `200`                                                      |
| Fondo de la figura (`fig.patch`)              | `white`                                                    |
| Fondo del área del gráfico (`ax.facecolor`) | `#F8F8FA`                                                  |
| Márgenes (`subplots_adjust`)                 | `left=0.08`, `right=0.92`, `top=0.85`, `bottom=0.22` |

---

#### Líneas

Cada serie usa la misma configuración de estilo, cambiando solo el color.

| Parámetro             | Valor                                                                             |
| ---------------------- | --------------------------------------------------------------------------------- |
| Grosor (`linewidth`) | `2.5` pt                                                                        |
| Marcador               | Círculo (`marker='o'`)                                                         |
| Tamaño del marcador   | `6`                                                                             |
| Relleno del marcador   | Mismo color que la línea                                                         |
| Borde del marcador     | `markeredgecolor` = mismo color de la línea, `markeredgewidth=0` (invisible) |
| `zorder`             | `4` (encima de cuadrícula y barras)                                            |

**Par de colores usado en Figura A.3:**

| Serie                      | Color       |
| -------------------------- | ----------- |
| INPC (verde institucional) | `#006157` |
| IPCOM (morado)             | `#b35aba` |

> Elegir pares con alto contraste entre sí. Sugerencias adicionales:
> `#753d6a` + `#368491` · `#5844a0` + `#ed8945` · `#8e244d` + `#4ead82`

---

#### Chips / etiquetas de datos con anti-colisión

Se colocan en **todos los puntos** de ambas series. Para evitar superposición se aplica lógica dinámica: la serie que está **arriba** recibe offset positivo (`bottom`), la que está **abajo** recibe offset negativo (`top`).

| Condición        | Offset INPC | `va` INPC | Offset IPCOM | `va` IPCOM |
| ----------------- | ----------- | ----------- | ------------ | ------------ |
| `inpc >= ipcom` | `+12` pt  | `bottom`  | `-16` pt   | `top`      |
| `inpc < ipcom`  | `-16` pt  | `top`     | `+12` pt   | `bottom`   |

**Estilo de los chips:**

| Parámetro        | Valor                                                |
| ----------------- | ---------------------------------------------------- |
| Formato del texto | `f'{round(valor)}'` (entero)                       |
| Tamaño de fuente | `8` pt                                             |
| Peso de fuente    | `bold`                                             |
| Color de texto    | `#3c3c3b`                                          |
| Forma del chip    | `boxstyle='round,pad=0.3,rounding_size=0.8'`       |
| Fondo del chip    | `white`                                            |
| Borde del chip    | Color de la serie correspondiente, grosor `0.8` pt |

---

#### Eje Y

| Parámetro             | Valor                                                       |
| ---------------------- | ----------------------------------------------------------- |
| Tamaño de tick labels | `10` pt                                                   |
| Peso de tick labels    | `medium` (forzado con `label.set_fontweight('medium')`) |
| Color de tick labels   | `#3c3c3b`                                                 |
| Locator                | `MultipleLocator(10)`                                     |
| Límites (ejemplo A.3) | `(60, 170)`                                               |

---

#### Eje X

| Parámetro                      | Valor                                        |
| ------------------------------- | -------------------------------------------- |
| Etiquetas                       | Años directos (e.g.`'2010'`, `'2024*'`) |
| Tamaño de fuente               | `10` pt                                    |
| Peso de fuente                  | `bold`                                     |
| Color                           | `#3c3c3b`                                  |
| Longitud de ticks               | `0` (invisibles, `length=0`)             |
| Color de ticks                  | `#7c7c7c`                                  |
| Separación del texto (`pad`) | `8` pt                                     |

---

#### Encabezado de la figura (título con cuadrado decorativo)

Idéntico a la referencia canónica de Figura A.1, con tres anotaciones separadas ancladas en `xy=(0, 1), xycoords='axes fraction'`.

| Elemento                                        | Descripción                                        | Parámetros clave                                                                                                                                   |
| ----------------------------------------------- | --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Cuadrado decorativo**                   | Parche verde redondeado antes del número de figura | `xytext=(0, 34)`, `boxstyle='round,pad=1.6,rounding_size=0.2'`, `facecolor='#4a7d75'`, `edgecolor='none'`, `fontsize=2` (texto = `' '`) |
| **Número de figura** (`"Figura A.3."`) | Bold, alineado tras el cuadrado                     | `xytext=(15, 30)`, `fontsize=14`, `fontweight='bold'`, `color='#3c3c3b'`                                                                    |
| **Título descriptivo**                   | Medium, misma línea                                | `xytext=(100, 30)`, `fontsize=14`, `fontweight='medium'`, `color='#3c3c3b'`                                                                 |

> Nota: el cuadrado usa `xytext=(0, 34)` y el texto `xytext=(15, 30)` / `(100, 30)` — ligera variación respecto a A.1 que usa `(0, 30)`.

---

#### Leyenda

| Parámetro         | Valor                                                   |
| ------------------ | ------------------------------------------------------- |
| Ubicación         | `lower center` de la figura completa (`fig.legend`) |
| `bbox_to_anchor` | `(0.5, 0.12)`                                         |
| Columnas           | `2`                                                   |
| Marco              | Sin marco (`frameon=False`)                           |
| `handlelength`   | `2.5`                                                 |
| Color de etiquetas | `labelcolor='#3c3c3b'`                                |
| Estilo de fuente   | `prop={'weight': 'bold', 'size': 10}`                 |

> La leyenda de A.3 usa `bbox_to_anchor=(0.5, 0.12)` (más alta que A.1 que usa `0.08`) para dejar espacio a las notas al pie.

---

#### Notas al pie y Fuente

Mismo esquema que la referencia A.1, sin `textwrap.fill` (texto corto en línea directa).

| Parámetro          | Valor                                            |
| ------------------- | ------------------------------------------------ |
| Tamaño de fuente   | `8` pt                                         |
| Color               | `#3c3c3b`                                      |
| X de inicio         | `0.08` (fracción de figura)                   |
| **"Fuente:"** | `fontweight='bold'`, posición `y=0.06`      |
| Contenido de Fuente | `fontweight='normal'`, offset `(+35, 0)` pts |
| **"Notas:"**  | `fontweight='bold'`, posición `y=0.042`     |
| Contenido de Notas  | `fontweight='normal'`, offset `(+32, 0)` pts |

---

#### Bordes, spines y cuadrícula

| Elemento                    | Valor                                                                                 |
| --------------------------- | ------------------------------------------------------------------------------------- |
| Borde superior (`top`)    | **Oculto**                                                                      |
| Borde derecho (`right`)   | **Oculto**                                                                      |
| Bordes izquierdo e inferior | Color `#7c7c7c`, `linewidth=1` (aplicado con `for spine in ax.spines.values()`) |
| Cuadrícula                 | Solo eje Y (`axis='y'`), color `#d1d1d1`, `linewidth=1`, `zorder=0`           |

> A diferencia de A.1 (doble eje), aquí solo se ocultan `top` y `right`; el borde derecho no existe como eje secundario.

---

#### Fuente tipográfica

```python
plt.rcParams['font.family'] = 'Noto Sans'
```

> A.3 usa solo `'Noto Sans'` (sin lista de fallback). Para mayor robustez se recomienda el estilo de A.1: `['Noto Sans', 'DejaVu Sans', 'sans-serif']`.

---

#### Exportación

```python
fig.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white', edgecolor='none')
```

---

### Líneas / Series de Tiempo (múltiples series)

Utilizar colores contrastantes en una paleta armoniosa o en una misma gama cromática donde el contraste se note. Mantener el mismo estilo de grosor (2.5 pt) y marcadores circulares sólidos.

**Sugerencias:** `#978bc4` `#ed8945` `#b35aba` `#4c7d7e` `#86adae` `#335a5c`

---

### Treemap

Dependiendo la información se puede optar por paleta monocromática o con colores de operadores.

**Paleta monocromática:**
`#132b2d` `#234244` `#335a5c` `#3b6667` `#4c7d7e` `#5c9596` `#64a0a1` `#86adae`

**Paleta operadores:** ver tabla de Colores para operadores.

---

### Pastel / Dona

Utilizar colores contrastantes y de una misma gama cromática. Si la información se divide por operadores, usar el color que le corresponda a cada uno.

**Paleta monocromática:**
`#132b2d` `#234244` `#335a5c` `#3b6667` `#4c7d7e` `#5c9596` `#64a0a1` `#86adae`

**Paleta operadores:** ver tabla de Colores para operadores.

---

### Barras y Dispersión

Utilizar colores que contrasten entre sí.

**Sugerencias:** `#64a0a1` + `#ed8945`

---

### Mapa coroplético

Los colores deben reflejar la intensidad de los datos, usando tonalidades claras para valores bajos y oscuras para altos.

**Sugerencia:** `#afafaf` → `#737f7c` → `#63918b` → `#2d4f4b` → `#012f2a`
