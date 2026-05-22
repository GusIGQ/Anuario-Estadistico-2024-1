# Fichas Técnicas — Reproducción de Gráficas del Anuario Estadístico 2024 IFT

---

## Figura A.1 — Producto Interno Bruto (PIB) y contribución del PIB de los subsectores de telecomunicaciones y radiodifusión

**Enlace de descarga del archivo fuente:**

- URL: <https://www.inegi.org.mx/temas/pib/> → Tabulados → PIBT (PIB Trimestral, Base 2018)

**Archivo local:**

- Ruta: `datos/tabulados_PIBT/PIBT_2.xlsx`
- Hoja: `Tabulado`

**Datos utilizados:**

| Fila | Concepto |
|------|----------|
| 7    | B.1bP - Producto interno bruto |
| 154  | 515 - Radio y televisión |
| 155  | 517 - Telecomunicaciones |

- Columnas: T1, T2, T3, T4 de cada año (columna offset por año: `1 + (año - 1993) * 7 + trimestre`)
- Rango temporal: 2013-T1 a 2024-T2 (46 trimestres)

**Cálculos realizados:**

- Barras (eje izquierdo): `PIB (miles de millones) = Fila 7 ÷ 1,000`
- Línea (eje derecho): `% TyR = (Fila 155 + Fila 154) ÷ Fila 7 × 100`

**Tipo de gráfica:** Barras con gradiente vertical + línea con marcadores circulares (doble eje Y)

**Script:** `scripts/figura_a1.py`
**Output:** `output/Figura_A1.png`

---

## Figura A.3 — Índices de precios (INPC e IPCOM)

**Enlace de descarga del archivo fuente:**

- URL: <https://www.inegi.org.mx/app/indicesdeprecios/> → INPC → Clasificación CCIF → Exportar CSV

**Archivo local:**

- Ruta: `datos/A.3/INP_INP20260310133506.CSV`
- Encoding: `latin-1`

**Datos utilizados:**

| Columna CSV | Concepto |
|-------------|----------|
| 1           | INPC total (Índice Nacional de Precios al Consumidor) |
| 9           | 08 Comunicaciones (IPCOM) |

- Filtro temporal: diciembre de cada año (2010-2023) + julio 2024
- Base: julio 2018 = 100
- El CSV tiene ~26 filas de encabezado; se parsea con `csv.reader` filtrando filas que inician con nombre de mes.

**Cálculos realizados:**

- Sin cálculos adicionales. Se grafican directamente los valores del índice.
- Etiquetas redondeadas a entero (`round()`).

**Tipo de gráfica:** Dos líneas con marcadores (círculos para INPC, cuadrados para IPCOM)

**Script:** `scripts/figura_a3.py`
**Output:** `output/Figura_A3.png`

---

<!-- Agregar más fichas abajo conforme se completen las figuras -->

## Figura A.5 — Inversión Extranjera Directa (IED) en telecomunicaciones

**Script:** `scripts/figura_a5.py`
**Output:** `output/Figura_A5.png`

---

## Figuras A.7, A.8, A.9, A.10 — Hogares con telecomunicaciones y gasto por decil de ingreso

**Enlace de descarga del archivo fuente:**

- URL: <https://www.inegi.org.mx/programas/enigh/nc/2022/> → Microdatos

**Archivos locales:**

- `datos/A.7/microdatos/concentradohogar.csv` — Ingreso corriente (`ing_cor`), factor de expansión (`factor`), gasto en comunicaciones (`comunica`)
- `datos/A.7/microdatos/hogares.csv` — Disponibilidad de servicios: `telefono`, `celular`, `conex_inte`, `tv_paga` (1=sí, 2=no)
- `datos/A.7/microdatos/gastoshogar.csv` — Gastos del hogar por clave (`gasto_tri`, `gas_nm_tri`)
- `datos/A.7/microdatos/gastospersona.csv` — Gastos por persona por clave (`gasto_tri`)

**Claves de gasto ENIGH:**

| Clave | Concepto | Usada en |
|-------|----------|----------|
| E001 | Teléfono fijo | A.8 (fijas) |
| E002 | Celular | A.10 (móviles) |
| E003 | Internet | A.8 (fijas) |
| E004 | TV de paga | A.8 (fijas) |
| E005 | Paquete (combo) | A.8 (fijas) |

**Metodología común:**

1. **Deciles:** Se ordenan los hogares por `ing_cor` (ingreso corriente trimestral) de `concentradohogar.csv`. Se construyen deciles ponderados por el factor de expansión (`factor`), asignando a cada hogar el decil según su posición acumulada en la distribución ponderada.
2. **"Con telecomunicaciones" (A.7/A.9):** Proporción ponderada de hogares que reportan tener el servicio en `hogares.csv`.
3. **"Disponen y gastan" (A.7/A.9):** Hogares con el servicio Y con gasto en comunicaciones positivo (ver definiciones por figura).
4. **Gasto promedio (A.8/A.10):** Suma de gastos trimestrales (`gasto_tri + gas_nm_tri`) de las claves E correspondientes de `gastoshogar.csv` + `gastospersona.csv`, dividido entre 3 para obtener mensual. Promedio ponderado sobre hogares que "disponen y gastan".
5. **% Gasto/Ingreso (A.8/A.10):** `gasto_mensual / (ing_cor / 3) × 100`, promedio ponderado por decil.

**Definiciones de servicio:**

- **Fijas (A.7, A.8):** `telefono=1` OR `conex_inte=1` OR `tv_paga=1` OR `num_compu>0` (A.7). Para A.8 se mantiene sin `num_compu`.
- **Móviles (A.9, A.10):** `celular=1`

**Definiciones de "disponen y gastan":**

- **A.7 (fijas):** con fijas AND (`comunica` − `gasto_E002`) > 0, donde `gasto_E002` es el gasto trimestral en telefonía celular (clave E002). Esto aísla el gasto fijo restando el componente móvil.
- **A.9 (móviles):** con móviles AND `comunica > 0`.

**Nota metodológica:**
Los valores pueden diferir ligeramente de los publicados por el IFT debido a posibles diferencias en la definición de servicios o la asignación de gastos a categorías fija/móvil. El campo `comunica` de `concentradohogar.csv` es un total pre-agregado por INEGI que incluye todas las fuentes de gasto en comunicaciones (fija + móvil + imputable). Para A.7 se añade `num_compu > 0` como proxy de acceso a internet fijo y se resta `gasto_E002` (celular) de `comunica` para aislar el gasto en fijas.

---

---

### Figura A.7 — Porcentaje de hogares con servicios de telecomunicaciones fijas por decil de ingreso

- **Tipo de gráfica:** Barras horizontales pareadas (rosa: disponen y gastan; azul: con telecomunicaciones fijas)
- **Script:** `scripts/figura_a7.py`
- **Output:** `output/Figura_A7.png`

### Figura A.8 — Gasto promedio y porcentaje de gasto en Servicios de Telecomunicaciones Fijas

- **Tipo de gráfica:** Barras verticales con gradiente (gasto $, eje derecho) + puntos (% gasto/ingreso, eje izquierdo)
- **Script:** `scripts/figura_a8.py`
- **Output:** `output/Figura_A8.png`

### Figura A.9 — Porcentaje de hogares con Servicios de Telecomunicaciones Móviles por decil de ingreso

- **Tipo de gráfica:** Barras horizontales pareadas (rosa: disponen y gastan; azul: con telecomunicaciones móviles)
- **Script:** `scripts/figura_a9.py`
- **Output:** `output/Figura_A9.png`

### Figura A.10 — Gasto promedio y porcentaje de gasto en Servicios de Telecomunicaciones Móviles

- **Tipo de gráfica:** Barras verticales con gradiente (gasto $, eje derecho) + puntos (% gasto/ingreso, eje izquierdo)
- **Script:** `scripts/figura_a10.py`
- **Output:** `output/Figura_A10.png`
