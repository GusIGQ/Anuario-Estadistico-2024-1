# Índice de Figuras — Anuario Estadístico 2024 del IFT

> **PDF original:** https://www.ift.org.mx/sites/default/files/contenidogeneral/estadisticas/anuarioestadistico2024vf_0.pdf
> **Total de figuras:** 106
> **Completadas:** 6 / 106

---

## Resumen por capítulo

| Capítulo | Tema | Figuras | Completadas |
|----------|------|---------|-------------|
| A | Indicadores Macroeconómicos | A.1 – A.10 (10) | 6 |
| B | Servicios Fijos de Telecomunicaciones | B.1 – B.25 (25) | 0 |
| C | Servicios Móviles de Telecomunicaciones | C.1 – C.16 (16) | 0 |
| D | Disponibilidad y Uso de TIC en Hogares | D.1 – D.11 (11) | 0 |
| E | Encuestas de Satisfacción y MiPymes | E.1 – E.9 (9) | 0 |
| F | Indicadores Sociales y Ciberacoso | F.1 – F.16 (16) | 0 |
| G | Indicadores de Radiodifusión | G.1 (1) | 0 |
| H | Audiencias de TV y Radio | H.1 – H.14 (14) | 0 |
| | **TOTAL** | **106** | **6** |

---

## Fuentes de datos principales

| Fuente | Encuestas / Bases | Figuras que la usan |
|--------|-------------------|---------------------|
| INEGI — PIB Trimestral | Sistema de Cuentas Nacionales | A.1 |
| INEGI — ENOE | Encuesta Nacional de Ocupación y Empleo | A.2, F.2 |
| INEGI — INPC / IPCOM | Índices de Precios | A.3 |
| INEGI — ENIGH | Encuesta Nacional de Ingresos y Gastos de los Hogares | A.7, A.8, A.9, A.10 |
| INEGI — ENDUTIH | Encuesta Nacional sobre Disponibilidad y Uso de TIC en Hogares | B.1-B.3, C.3-C.4, D.1-D.4, F.1-F.2 |
| INEGI — MOCIBA | Módulo sobre Ciberacoso | F.3-F.9 |
| IFT — Operadores de telecomunicaciones | Datos proporcionados por operadores | A.4, A.6, B.4-B.25, C.5-C.16 |
| IFT — Encuesta de Confianza (ECSI) | Encuesta de Confianza en el Servicio de Internet | D.5-D.11 |
| IFT — Encuesta de Satisfacción | 3ª y 4ª Encuesta de Usuarios de Telecomunicaciones | E.1-E.9, F.10-F.16 |
| IFT — BIT Estatal | Banco de Información de Telecomunicaciones | G.1 |
| IFT — Espectro | Datos internos del IFT | C.1, C.2 |
| Secretaría de Economía | Inversión Extranjera Directa | A.5 |
| Nielsen IBOPE | Ratings TV 28 ciudades (MSS TV) | H.1-H.10 |
| INRA | Ratings Radio (software INRAM) | H.11-H.14 |

---

# A. INDICADORES MACROECONÓMICOS

---

### Figura A.1 — Producto Interno Bruto (PIB) y contribución del PIB de los subsectores de telecomunicaciones y radiodifusión
- **Página PDF:** 11
- **Tipo de gráfica:** Barras con gradiente + línea con marcadores (doble eje Y)
- **Fuente PDF:** IFT con datos del INEGI a junio de 2024
- **Enlace de descarga:** https://www.inegi.org.mx/contenidos/programas/pib/2018/tabulados/ori/tabulados_PIBT.zip 
- **Archivo local:** `datos/tabulados_PIBT/PIBT_2.xlsx` · Hoja: `Tabulado`
- **Datos utilizados:**
  - Fila 7: `B.1bP - Producto interno bruto`
  - Fila 154: `515 - Radio y televisión`
  - Fila 155: `517 - Telecomunicaciones`
  - Columnas: T1-T4 por año (cada año = 7 cols: T1, T2, T3, T4, 6M, 9M, Anual)
  - Rango: 2013-T1 a 2024-T2
- **Cálculos:**
  - Barras (eje izq): PIB miles de millones = Fila 7 ÷ 1,000
  - Línea (eje der): % TyR = (Fila 155 + Fila 154) ÷ Fila 7 × 100
- **Script:** `scripts/figura_a1.py`
- **Output:** `output/Figura_A1.png`
- **Estado:** ✅ Completada

---

### Figura A.2 — Empleo en los sectores de telecomunicaciones y radiodifusión
- **Página PDF:** 12
- **Tipo de gráfica:** Barras + línea (pendiente confirmar)
- **Fuente PDF:** IFT con datos de la ENOE del INEGI, cifras a junio 2024
- **Enlace de descarga:** https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/microdatos/enoe_2024_trim2_csv.zip
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_a2.py`
- **Output:** `output/Figura_A2.png`
- **Estado:** ⬜ Pendiente

---

### Figura A.3 — Índices de precios (INPC e IPCOM)
- **Página PDF:** 13
- **Tipo de gráfica:** Líneas (serie de tiempo)
- **Fuente PDF:** IFT con datos del INEGI a julio de 2024
- **Enlace de descarga:** https://www.inegi.org.mx/app/indicesdeprecios/Estructura.aspx?idEstructura=112001300090&T=Índices+de+Precios+al+Consumidor
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_a3.py`
- **Output:** `output/Figura_A3.png`
- **Estado:** ⬜ Pendiente

---

### Figura A.4 — Inversión privada en Telecomunicaciones por tipo de inversión
- **Página PDF:** 14
- **Tipo de gráfica:** Barras apiladas / agrupadas
- **Fuente PDF:** IFT con datos proporcionados por los operadores de telecomunicaciones
- **Enlace de descarga:** ⬜ Por identificar (datos del IFT / BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_a4.py`
- **Output:** `output/Figura_A4.png`
- **Estado:** ⬜ Pendiente

---

### Figura A.5 — Inversión Extranjera Directa (IED) en telecomunicaciones
- **Página PDF:** 15
- **Tipo de gráfica:** Barras horizontales agrupadas (2 barras por año)
- **Fuente PDF:** IFT con datos de la Secretaría de Economía a junio de 2024
- **Enlace de descarga:** https://www.gob.mx/se/acciones-y-programas/competitividad-y-normatividad-inversion-extranjera-directa
- **Archivo local:** `datos/A.5/Datos_originales_y_actualizacion__1_.xlsx` (IED total) · `datos/A.5/2025_3T_Flujosportipodeinversion_actu__3_.xlsx` (sector 517)
- **Datos utilizados:**
  - IED total de México: col D (datos actualizados), filas "Enero - diciembre" (2013-2023) y "Enero - junio" (2024)
  - IED telecomunicaciones: hoja "Por sector", fila "517 Telecomunicaciones", Q4 acumulado (2013-2023) y Q2 (2024)
- **Cálculos:** Lectura directa de valores acumulados anuales
- **Script:** `scripts/figura_a5.py`
- **Output:** `output/Figura_A5.png`
- **Estado:** ✅ Completada (datos actualizados al 3T 2025)

---

### Figura A.6 — Ingresos, egresos y margen en el sector de telecomunicaciones
- **Página PDF:** 16
- **Tipo de gráfica:** Barras + línea (pendiente confirmar)
- **Fuente PDF:** IFT con datos proporcionados por los operadores de telecomunicaciones a diciembre de 2023
- **Enlace de descarga:** ⬜ Por identificar (datos del IFT / BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_a6.py`
- **Output:** `output/Figura_A6.png`
- **Estado:** ⬜ Pendiente

---

### Figura A.7 — Porcentaje de hogares con servicios de telecomunicaciones fijas por decil de ingreso
- **Página PDF:** 17
- **Tipo de gráfica:** Barras horizontales pareadas por decil
- **Fuente PDF:** IFT con datos de la ENIGH 2022 del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/enigh/nc/2022/
- **Archivo local:** `datos/A.7/microdatos/concentradohogar.csv`, `datos/A.7/microdatos/hogares.csv`
- **Datos utilizados:** ing_cor, factor, comunica (concentradohogar); telefono, conex_inte, tv_paga (hogares)
- **Cálculos:** Deciles ponderados de ing_cor; % con fijas = telefono=1|conex_inte=1|tv_paga=1; % dg = anterior AND comunica>0
- **Script:** `scripts/figura_a7.py`
- **Output:** `output/Figura_A7.png`
- **Estado:** ✅ Completada

---

### Figura A.8 — Gasto promedio y porcentaje de gasto en Servicios de Telecomunicaciones Fijas de los hogares por decil de ingreso
- **Página PDF:** 18
- **Tipo de gráfica:** Barras con gradiente + puntos (doble eje)
- **Fuente PDF:** IFT con datos de la ENIGH 2022 del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/enigh/nc/2022/
- **Archivo local:** `datos/A.7/microdatos/` (concentradohogar, hogares, gastoshogar, gastospersona)
- **Datos utilizados:** Claves E001, E003, E004, E005 de gastos; ing_cor para % ingreso
- **Cálculos:** Gasto mensual = Σ(gasto_tri + gas_nm_tri)/3 para hogares dg_fijas; % = gasto_mensual/(ing_cor/3)×100
- **Script:** `scripts/figura_a8.py`
- **Output:** `output/Figura_A8.png`
- **Estado:** ✅ Completada

---

### Figura A.9 — Porcentaje de hogares con Servicios de Telecomunicaciones Móviles por decil de ingreso
- **Página PDF:** 19
- **Tipo de gráfica:** Barras horizontales pareadas por decil
- **Fuente PDF:** IFT con datos de la ENIGH 2022 del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/enigh/nc/2022/
- **Archivo local:** `datos/A.7/microdatos/concentradohogar.csv`, `datos/A.7/microdatos/hogares.csv`
- **Datos utilizados:** ing_cor, factor, comunica (concentradohogar); celular (hogares)
- **Cálculos:** Deciles ponderados de ing_cor; % con móviles = celular=1; % dg = anterior AND comunica>0
- **Script:** `scripts/figura_a9.py`
- **Output:** `output/Figura_A9.png`
- **Estado:** ✅ Completada

---

### Figura A.10 — Gasto promedio y porcentaje de gasto en Servicios de Telecomunicaciones Móviles de los hogares por decil de ingreso
- **Página PDF:** 20
- **Tipo de gráfica:** Barras con gradiente + puntos (doble eje)
- **Fuente PDF:** IFT con datos de la ENIGH 2022 del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/enigh/nc/2022/
- **Archivo local:** `datos/A.7/microdatos/` (concentradohogar, hogares, gastoshogar, gastospersona)
- **Datos utilizados:** Clave E002 de gastos; ing_cor para % ingreso
- **Cálculos:** Gasto mensual = Σ(gasto_tri + gas_nm_tri)/3 para hogares dg_moviles; % = gasto_mensual/(ing_cor/3)×100
- **Script:** `scripts/figura_a10.py`
- **Output:** `output/Figura_A10.png`
- **Estado:** ✅ Completada

---

# B. SERVICIOS FIJOS DE TELECOMUNICACIONES

---

### Figura B.1 — Distribución de los Servicios Fijos con respecto del total de hogares a nivel nacional
- **Página PDF:** 21
- **Tipo de gráfica:** Barras horizontales / pastel
- **Fuente PDF:** IFT con datos de la ENDUTIH 2023 del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/endutih/2023/
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b1.py`
- **Output:** `output/Figura_B1.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.2 — Distribución de los Servicios Fijos con respecto del total de hogares en las zonas rurales
- **Página PDF:** 22
- **Tipo de gráfica:** Barras horizontales / pastel
- **Fuente PDF:** IFT con datos de la ENDUTIH 2023 del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/endutih/2023/
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b2.py`
- **Output:** `output/Figura_B2.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.3 — Distribución de los Servicios Fijos con respecto del total de hogares en las zonas urbanas
- **Página PDF:** 23
- **Tipo de gráfica:** Barras horizontales / pastel
- **Fuente PDF:** IFT con datos de la ENDUTIH 2023 del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/endutih/2023/
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b3.py`
- **Output:** `output/Figura_B3.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.4 — Líneas del Servicio Fijo de Telefonía (2000-2023)
- **Página PDF:** 24
- **Tipo de gráfica:** Barras o línea (serie temporal)
- **Fuente PDF:** IFT con datos proporcionados por los operadores a diciembre de cada año
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b4.py`
- **Output:** `output/Figura_B4.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.5 — Líneas del Servicio Fijo de Telefonía por cada 100 hogares (1971-2023)
- **Página PDF:** 25
- **Tipo de gráfica:** Línea (serie temporal larga)
- **Fuente PDF:** IFT con datos de operadores, CONAPO e INEGI
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b5.py`
- **Output:** `output/Figura_B5.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.6 — Líneas del Servicio Fijo de Telefonía Residencial por cada 100 hogares por entidad federativa
- **Página PDF:** 26
- **Tipo de gráfica:** Mapa de México (coropleta) o barras horizontales por estado
- **Fuente PDF:** IFT con datos de operadores y ENDUTIH 2023 del INEGI
- **Enlace de descarga:** ⬜ Por identificar
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b6.py`
- **Output:** `output/Figura_B6.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.7 — Líneas del Servicio Fijo de Telefonía No Residencial por cada 100 unidades económicas por entidad federativa
- **Página PDF:** 27
- **Tipo de gráfica:** Mapa de México (coropleta) o barras horizontales por estado
- **Fuente PDF:** IFT con datos de operadores y DENUE del INEGI
- **Enlace de descarga:** ⬜ Por identificar
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b7.py`
- **Output:** `output/Figura_B7.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.8 — Tráfico de minutos del Servicio Fijo de Telefonía (2000-2023)
- **Página PDF:** 28
- **Tipo de gráfica:** Barras o línea (serie temporal)
- **Fuente PDF:** IFT con datos de operadores (acumulados a diciembre)
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b8.py`
- **Output:** `output/Figura_B8.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.9 — Participación de mercado del Servicio Fijo de Telefonía (2013-2023)
- **Página PDF:** 29
- **Tipo de gráfica:** Barras apiladas 100% o área apilada
- **Fuente PDF:** IFT con datos de operadores a diciembre de cada año
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b9.py`
- **Output:** `output/Figura_B9.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.10 — Herfindahl-Hirschman (IHH). Concentración de mercado del Servicio Fijo de Telefonía (2013-2023)
- **Página PDF:** 30
- **Tipo de gráfica:** Línea con marcadores
- **Fuente PDF:** IFT con datos de operadores a diciembre de cada año
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** IHH = Σ(cuota de mercado²)
- **Script:** `scripts/figura_b10.py`
- **Output:** `output/Figura_B10.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.11 — Accesos del Servicio Fijo de Internet (2000-2023)
- **Página PDF:** 31
- **Tipo de gráfica:** Barras o línea (serie temporal)
- **Fuente PDF:** IFT con datos de operadores a diciembre de cada año
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b11.py`
- **Output:** `output/Figura_B11.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.12 — Accesos del Servicio Fijo de Internet por cada 100 hogares (2000-2023)
- **Página PDF:** 32
- **Tipo de gráfica:** Línea (serie temporal)
- **Fuente PDF:** IFT con datos de operadores, CONAPO e INEGI
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b12.py`
- **Output:** `output/Figura_B12.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.13 — Accesos del Servicio Fijo de Internet Residencial por cada 100 hogares por entidad federativa
- **Página PDF:** 33
- **Tipo de gráfica:** Mapa de México (coropleta)
- **Fuente PDF:** IFT con datos de operadores y ENDUTIH 2023 del INEGI
- **Enlace de descarga:** ⬜ Por identificar
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b13.py`
- **Output:** `output/Figura_B13.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.14 — Accesos del Servicio Fijo de Internet No Residencial por cada 100 unidades económicas por entidad federativa
- **Página PDF:** 34
- **Tipo de gráfica:** Mapa de México (coropleta)
- **Fuente PDF:** IFT con datos de operadores y DENUE del INEGI
- **Enlace de descarga:** ⬜ Por identificar
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b14.py`
- **Output:** `output/Figura_B14.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.15 — Distribución de los accesos del Servicio Fijo de Internet por rangos de velocidad (2013-2023)
- **Página PDF:** 35
- **Tipo de gráfica:** Barras apiladas 100%
- **Fuente PDF:** IFT con datos de operadores a diciembre de cada año
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b15.py`
- **Output:** `output/Figura_B15.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.16 — Distribución de los accesos al servicio fijo de Internet por tecnología de conexión y por segmento
- **Página PDF:** 36
- **Tipo de gráfica:** Barras apiladas o dona
- **Fuente PDF:** IFT con datos de operadores a diciembre de 2023
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b16.py`
- **Output:** `output/Figura_B16.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.17 — Participación de mercado del servicio fijo de Internet (2013-2023)
- **Página PDF:** 37
- **Tipo de gráfica:** Barras apiladas 100% o área apilada
- **Fuente PDF:** Participación calculada con respecto al número de accesos
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b17.py`
- **Output:** `output/Figura_B17.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.18 — Herfindahl-Hirschman (IHH). Concentración de mercado del Servicio Fijo de Internet (2013-2023)
- **Página PDF:** 38
- **Tipo de gráfica:** Línea con marcadores
- **Fuente PDF:** IFT con datos de operadores a diciembre de cada año
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** IHH = Σ(cuota de mercado²)
- **Script:** `scripts/figura_b18.py`
- **Output:** `output/Figura_B18.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.19 — Accesos del Servicio de Televisión Restringida (1998-2023)
- **Página PDF:** 39
- **Tipo de gráfica:** Barras o línea (serie temporal)
- **Fuente PDF:** IFT con datos de operadores a diciembre de cada año
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b19.py`
- **Output:** `output/Figura_B19.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.20 — Accesos del Servicio de Televisión Restringida por cada 100 hogares (1998-2023)
- **Página PDF:** 40
- **Tipo de gráfica:** Línea (serie temporal)
- **Fuente PDF:** IFT con datos de operadores, CONAPO e INEGI
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b20.py`
- **Output:** `output/Figura_B20.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.21 — Accesos del Servicio de Televisión Restringida Residencial por cada 100 hogares por entidad federativa
- **Página PDF:** 41
- **Tipo de gráfica:** Mapa de México (coropleta)
- **Fuente PDF:** IFT con datos de operadores y ENDUTIH 2023 del INEGI
- **Enlace de descarga:** ⬜ Por identificar
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b21.py`
- **Output:** `output/Figura_B21.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.22 — Accesos del Servicio de Televisión Restringida No Residencial por cada 100 unidades económicas por entidad federativa
- **Página PDF:** 42
- **Tipo de gráfica:** Mapa de México (coropleta)
- **Fuente PDF:** IFT con datos de operadores y DENUE del INEGI
- **Enlace de descarga:** ⬜ Por identificar
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b22.py`
- **Output:** `output/Figura_B22.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.23 — Tecnologías de conexión del Servicio de Televisión Restringida por segmento
- **Página PDF:** 43
- **Tipo de gráfica:** Barras apiladas o dona
- **Fuente PDF:** IFT con datos de operadores a diciembre de 2023
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b23.py`
- **Output:** `output/Figura_B23.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.24 — Participación de mercado del Servicio de Televisión Restringida (2014-2023)
- **Página PDF:** 44
- **Tipo de gráfica:** Barras apiladas 100% o área apilada
- **Fuente PDF:** IFT con datos de operadores a diciembre de cada año
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_b24.py`
- **Output:** `output/Figura_B24.png`
- **Estado:** ⬜ Pendiente

---

### Figura B.25 — Herfindahl-Hirschman (IHH). Concentración de mercado del servicio de televisión restringida (2015-2023)
- **Página PDF:** 45
- **Tipo de gráfica:** Línea con marcadores
- **Fuente PDF:** IFT con datos de operadores a diciembre de cada año
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** IHH = Σ(cuota de mercado²)
- **Script:** `scripts/figura_b25.py`
- **Output:** `output/Figura_B25.png`
- **Estado:** ⬜ Pendiente

---

# C. SERVICIOS MÓVILES DE TELECOMUNICACIONES

---

### Figura C.1 — Espectro radioeléctrico (MHz) asignado por banda de frecuencia
- **Página PDF:** 46
- **Tipo de gráfica:** Barras apiladas o diagrama de espectro
- **Fuente PDF:** IFT con datos a agosto de 2024
- **Enlace de descarga:** ⬜ Por identificar (datos internos IFT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_c1.py`
- **Output:** `output/Figura_C1.png`
- **Estado:** ⬜ Pendiente

---

### Figura C.2 — Distribución del espectro radioeléctrico por operador y por banda de frecuencia
- **Página PDF:** 47
- **Tipo de gráfica:** Barras apiladas / treemap
- **Fuente PDF:** IFT con datos a agosto de 2024
- **Enlace de descarga:** ⬜ Por identificar (datos internos IFT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_c2.py`
- **Output:** `output/Figura_C2.png`
- **Estado:** ⬜ Pendiente

---

### Figura C.3 — Porcentaje del uso de los servicios móviles de telecomunicaciones
- **Página PDF:** 48
- **Tipo de gráfica:** Barras agrupadas
- **Fuente PDF:** IFT con datos de la ENDUTIH 2023 del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/endutih/2023/#tabulados
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_c3.py`
- **Output:** `output/Figura_C3.png`
- **Estado:** ⬜ Pendiente

---

### Figura C.4 — Porcentaje del uso de los servicios móviles de telecomunicaciones por zona geográfica
- **Página PDF:** 48
- **Tipo de gráfica:** Barras agrupadas
- **Fuente PDF:** IFT con datos de la ENDUTIH 2023 del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/endutih/2023/#tabulados
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_c4.py`
- **Output:** `output/Figura_C4.png`
- **Estado:** ⬜ Pendiente

---

### Figura C.5 — Líneas del servicio móvil de telefonía (1990-2023)
- **Página PDF:** 49
- **Tipo de gráfica:** Barras o línea (serie temporal)
- **Fuente PDF:** IFT con datos de operadores a diciembre de cada año
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_c5.py`
- **Output:** `output/Figura_C5.png`
- **Estado:** ⬜ Pendiente

---

### Figura C.6 — Líneas del servicio móvil de telefonía por cada 100 habitantes (1990-2023)
- **Página PDF:** 50
- **Tipo de gráfica:** Línea (serie temporal)
- **Fuente PDF:** IFT con datos de operadores, CONAPO, INEGI y estimaciones propias
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_c6.py`
- **Output:** `output/Figura_C6.png`
- **Estado:** ⬜ Pendiente

---

### Figura C.7 — Líneas del servicio móvil de telefonía por cada 100 habitantes por entidad federativa
- **Página PDF:** 51
- **Tipo de gráfica:** Mapa de México (coropleta)
- **Fuente PDF:** IFT con datos de operadores, CONAPO y estimaciones propias
- **Enlace de descarga:** ⬜ Por identificar
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_c7.py`
- **Output:** `output/Figura_C7.png`
- **Estado:** ⬜ Pendiente

---

### Figura C.8 — Tráfico de salida del servicio móvil de telefonía (1997-2023)
- **Página PDF:** 52
- **Tipo de gráfica:** Barras o línea (serie temporal)
- **Fuente PDF:** IFT con datos de operadores (acumulados a diciembre)
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_c8.py`
- **Output:** `output/Figura_C8.png`
- **Estado:** ⬜ Pendiente

---

### Figura C.9 — Participación de mercado del servicio móvil de telefonía (2013-2023)
- **Página PDF:** 53
- **Tipo de gráfica:** Barras apiladas 100% o área apilada
- **Fuente PDF:** IFT con datos de operadores a diciembre de cada año
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_c9.py`
- **Output:** `output/Figura_C9.png`
- **Estado:** ⬜ Pendiente

---

### Figura C.10 — Herfindahl-Hirschman (IHH). Concentración de mercado del servicio móvil de telefonía (2013-2023)
- **Página PDF:** 54
- **Tipo de gráfica:** Línea con marcadores
- **Fuente PDF:** IFT con datos de operadores a diciembre de cada año
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** IHH = Σ(cuota de mercado²)
- **Script:** `scripts/figura_c10.py`
- **Output:** `output/Figura_C10.png`
- **Estado:** ⬜ Pendiente

---

### Figura C.11 — Líneas del servicio móvil de acceso a Internet (2010-2023)
- **Página PDF:** 55
- **Tipo de gráfica:** Barras o línea (serie temporal)
- **Fuente PDF:** IFT con datos de operadores a diciembre de cada año
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_c11.py`
- **Output:** `output/Figura_C11.png`
- **Estado:** ⬜ Pendiente

---

### Figura C.12 — Líneas del servicio móvil de acceso a Internet por cada 100 habitantes (2010-2023)
- **Página PDF:** 56
- **Tipo de gráfica:** Línea (serie temporal)
- **Fuente PDF:** IFT con datos de operadores, CONAPO, INEGI y estimaciones propias
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_c12.py`
- **Output:** `output/Figura_C12.png`
- **Estado:** ⬜ Pendiente

---

### Figura C.13 — Líneas del servicio móvil de acceso a Internet por cada 100 habitantes por entidad federativa
- **Página PDF:** 57
- **Tipo de gráfica:** Mapa de México (coropleta)
- **Fuente PDF:** IFT con datos de operadores, CONAPO y estimaciones propias
- **Enlace de descarga:** ⬜ Por identificar
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_c13.py`
- **Output:** `output/Figura_C13.png`
- **Estado:** ⬜ Pendiente

---

### Figura C.14 — Tráfico del servicio móvil de acceso a Internet (2015-2023)
- **Página PDF:** 58
- **Tipo de gráfica:** Barras o línea (serie temporal)
- **Fuente PDF:** IFT con datos de operadores (acumulados a diciembre)
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_c14.py`
- **Output:** `output/Figura_C14.png`
- **Estado:** ⬜ Pendiente

---

### Figura C.15 — Participación de mercado del servicio móvil de acceso a Internet (2013-2023)
- **Página PDF:** 59
- **Tipo de gráfica:** Barras apiladas 100% o área apilada
- **Fuente PDF:** IFT con datos de operadores a diciembre de cada año
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_c15.py`
- **Output:** `output/Figura_C15.png`
- **Estado:** ⬜ Pendiente

---

### Figura C.16 — Herfindahl-Hirschman (IHH). Concentración de mercado del servicio móvil de acceso a Internet (2013-2023)
- **Página PDF:** 60
- **Tipo de gráfica:** Línea con marcadores
- **Fuente PDF:** IFT con datos de operadores a diciembre de cada año
- **Enlace de descarga:** ⬜ Por identificar (IFT BIT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** IHH = Σ(cuota de mercado²)
- **Script:** `scripts/figura_c16.py`
- **Output:** `output/Figura_C16.png`
- **Estado:** ⬜ Pendiente

---

# D. DISPONIBILIDAD Y USO DE TIC EN HOGARES

---

### Figura D.1 — Disponibilidad de las TIC en los hogares (2010-2023)
- **Página PDF:** 61
- **Tipo de gráfica:** Líneas múltiples (serie temporal)
- **Fuente PDF:** IFT con datos del MODUTIH (2010-2014) y ENDUTIH (2015-2023) del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/endutih/2023/
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_d1.py`
- **Output:** `output/Figura_D1.png`
- **Estado:** ⬜ Pendiente

---

### Figura D.2 — Uso de Smartphone e internet por grupos de edad
- **Página PDF:** 62
- **Tipo de gráfica:** Barras agrupadas por grupo de edad
- **Fuente PDF:** IFT con datos de la ENDUTIH 2023 del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/endutih/2023/
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_d2.py`
- **Output:** `output/Figura_D2.png`
- **Estado:** ⬜ Pendiente

---

### Figura D.3 — Porcentaje de horas promedio de uso de internet por grupos de edad
- **Página PDF:** 63
- **Tipo de gráfica:** Barras agrupadas
- **Fuente PDF:** IFT con datos de la ENDUTIH 2023 del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/endutih/2023/
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_d3.py`
- **Output:** `output/Figura_D3.png`
- **Estado:** ⬜ Pendiente

---

### Figura D.4 — Uso de dispositivos inteligentes conectados a Internet
- **Página PDF:** 64
- **Tipo de gráfica:** Barras horizontales o pictograma
- **Fuente PDF:** IFT con datos de la ENDUTIH 2023 del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/endutih/2023/
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_d4.py`
- **Output:** `output/Figura_D4.png`
- **Estado:** ⬜ Pendiente

---

### Figura D.5 — ¿Cómo aprendió a buscar información o usar el Internet?
- **Página PDF:** 65
- **Tipo de gráfica:** Barras horizontales
- **Fuente PDF:** IFT, Encuesta de Confianza en el Servicio de Internet (ECSI) 2024
- **Enlace de descarga:** ⬜ Por identificar (encuesta IFT ECSI)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_d5.py`
- **Output:** `output/Figura_D5.png`
- **Estado:** ⬜ Pendiente

---

### Figura D.6 — Usuarios que han vivido experiencias negativas al utilizar Internet, por sexo
- **Página PDF:** 66
- **Tipo de gráfica:** Barras agrupadas por sexo
- **Fuente PDF:** IFT, ECSI 2024
- **Enlace de descarga:** ⬜ Por identificar (encuesta IFT ECSI)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_d6.py`
- **Output:** `output/Figura_D6.png`
- **Estado:** ⬜ Pendiente

---

### Figura D.7 — Usuarios que han vivido experiencias negativas al utilizar Internet, por grupo de edad
- **Página PDF:** 67
- **Tipo de gráfica:** Barras agrupadas por grupo de edad
- **Fuente PDF:** IFT, ECSI 2024
- **Enlace de descarga:** ⬜ Por identificar (encuesta IFT ECSI)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_d7.py`
- **Output:** `output/Figura_D7.png`
- **Estado:** ⬜ Pendiente

---

### Figura D.8 — Percepción o grado de confianza que las personas tienen al hacer uso del Internet
- **Página PDF:** 68
- **Tipo de gráfica:** Barras horizontales o escala Likert
- **Fuente PDF:** IFT, ECSI 2024
- **Enlace de descarga:** ⬜ Por identificar (encuesta IFT ECSI)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_d8.py`
- **Output:** `output/Figura_D8.png`
- **Estado:** ⬜ Pendiente

---

### Figura D.9 — Porcentaje de la población usuaria de Internet según nivel de seguridad que consideran tiene realizar diferentes actividades en línea
- **Página PDF:** 69
- **Tipo de gráfica:** Barras apiladas horizontales (escala Likert)
- **Fuente PDF:** IFT, ECSI 2024
- **Enlace de descarga:** ⬜ Por identificar (encuesta IFT ECSI)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_d9.py`
- **Output:** `output/Figura_D9.png`
- **Estado:** ⬜ Pendiente

---

### Figura D.10 — Porcentaje de la población usuaria de Internet según nivel de seguridad que consideran tiene realizar transacciones bancarias en línea
- **Página PDF:** 70
- **Tipo de gráfica:** Barras apiladas horizontales
- **Fuente PDF:** IFT, ECSI 2024
- **Enlace de descarga:** ⬜ Por identificar (encuesta IFT ECSI)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_d10.py`
- **Output:** `output/Figura_D10.png`
- **Estado:** ⬜ Pendiente

---

### Figura D.11 — Porcentaje de la población usuaria de Internet, qué tan seguro es compartir información en redes sociales (por sexo)
- **Página PDF:** 71
- **Tipo de gráfica:** Barras agrupadas por sexo
- **Fuente PDF:** IFT, ECSI 2024
- **Enlace de descarga:** ⬜ Por identificar (encuesta IFT ECSI)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_d11.py`
- **Output:** `output/Figura_D11.png`
- **Estado:** ⬜ Pendiente

---

# E. ENCUESTAS DE SATISFACCIÓN Y MiPymes

---

### Figura E.1 — Índice General de Satisfacción (IGS) por servicio de telecomunicaciones
- **Página PDF:** 72
- **Tipo de gráfica:** Barras agrupadas
- **Fuente PDF:** IFT, 3ª Encuesta 2023, Usuarios de Servicios de Telecomunicaciones
- **Enlace de descarga:** ⬜ Por identificar (encuestas IFT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_e1.py`
- **Output:** `output/Figura_E1.png`
- **Estado:** ⬜ Pendiente

---

### Figura E.2 — Principales hallazgos de la Inteligencia Artificial (IA) y ChatGPT
- **Página PDF:** 73
- **Tipo de gráfica:** Infografía / barras horizontales
- **Fuente PDF:** IFT, Estudio Cualitativo: Conocimiento y Percepción Sobre la IA y ChatGPT 2023
- **Enlace de descarga:** ⬜ Por identificar (estudio IFT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_e2.py`
- **Output:** `output/Figura_E2.png`
- **Estado:** ⬜ Pendiente

---

### Figura E.3 — Índice General de Satisfacción (IGS) por servicio y tamaño de la empresa
- **Página PDF:** 74
- **Tipo de gráfica:** Barras agrupadas
- **Fuente PDF:** IFT, 4ª Encuesta 2022 y 2023, Usuarios de Telecomunicaciones (MiPymes)
- **Enlace de descarga:** ⬜ Por identificar (encuestas IFT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_e3.py`
- **Output:** `output/Figura_E3.png`
- **Estado:** ⬜ Pendiente

---

### Figura E.4 — Servicios de telecomunicaciones que contratan las MiPymes (2022-2023)
- **Página PDF:** 75
- **Tipo de gráfica:** Barras agrupadas
- **Fuente PDF:** IFT, 4ª Encuesta 2023, Usuarios de Telecomunicaciones (MiPymes)
- **Enlace de descarga:** ⬜ Por identificar (encuestas IFT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_e4.py`
- **Output:** `output/Figura_E4.png`
- **Estado:** ⬜ Pendiente

---

### Figura E.5 — Percepción de las MiPymes sobre los beneficios de contar con servicios de Internet fijo y/o telefonía fija
- **Página PDF:** 76
- **Tipo de gráfica:** Barras horizontales
- **Fuente PDF:** IFT, 4ª Encuesta 2023 (MiPymes)
- **Enlace de descarga:** ⬜ Por identificar (encuestas IFT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_e5.py`
- **Output:** `output/Figura_E5.png`
- **Estado:** ⬜ Pendiente

---

### Figura E.6 — Beneficios de vender a través de Internet fijo
- **Página PDF:** 77
- **Tipo de gráfica:** Barras horizontales
- **Fuente PDF:** IFT, 4ª Encuesta 2023 (MiPymes)
- **Enlace de descarga:** ⬜ Por identificar (encuestas IFT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_e6.py`
- **Output:** `output/Figura_E6.png`
- **Estado:** ⬜ Pendiente

---

### Figura E.7 — Dispositivos que usan las MiPymes para realizar sus actividades (2022-2023)
- **Página PDF:** 78
- **Tipo de gráfica:** Barras agrupadas
- **Fuente PDF:** IFT, 4ª Encuesta 2023 (MiPymes)
- **Enlace de descarga:** ⬜ Por identificar (encuestas IFT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_e7.py`
- **Output:** `output/Figura_E7.png`
- **Estado:** ⬜ Pendiente

---

### Figura E.8 — Percepción de las MiPymes sobre los beneficios de contar con una aplicación móvil
- **Página PDF:** 79
- **Tipo de gráfica:** Barras horizontales
- **Fuente PDF:** IFT, 4ª Encuesta 2023 (MiPymes)
- **Enlace de descarga:** ⬜ Por identificar (encuestas IFT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_e8.py`
- **Output:** `output/Figura_E8.png`
- **Estado:** ⬜ Pendiente

---

### Figura E.9 — Servicios de Telecomunicaciones que consideran más importantes las MiPymes para actividades de importación y/o exportación
- **Página PDF:** 80
- **Tipo de gráfica:** Barras horizontales
- **Fuente PDF:** IFT, documento sobre Internet fijo y Telefonía fija en MiPymes (importación/exportación)
- **Enlace de descarga:** ⬜ Por identificar (estudio IFT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_e9.py`
- **Output:** `output/Figura_E9.png`
- **Estado:** ⬜ Pendiente

---

# F. INDICADORES SOCIALES, CIBERACOSO Y VIOLENCIA DIGITAL

---

### Figura F.1 — Actividades en Smartphone, Internet, computadora y uso de redes sociales
- **Página PDF:** 82-85 (4 páginas, gráfica compuesta)
- **Tipo de gráfica:** Barras horizontales / infografía multipágina
- **Fuente PDF:** IFT con datos de la ENDUTIH 2023 del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/endutih/2023/
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_f1.py`
- **Output:** `output/Figura_F1.png` (o múltiples: F1a, F1b, F1c, F1d)
- **Estado:** ⬜ Pendiente

---

### Figura F.2 — Porcentaje de personas empleadas en telecomunicaciones y radiodifusión
- **Página PDF:** 86
- **Tipo de gráfica:** Barras o línea
- **Fuente PDF:** IFT con datos de la ENOE a junio de 2024 del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/enoe/15ymas/
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_f2.py`
- **Output:** `output/Figura_F2.png`
- **Estado:** ⬜ Pendiente

---

### Figura F.3 — Porcentaje de la población de 12 años y más que vivió ciberacoso por entidad federativa
- **Página PDF:** 87
- **Tipo de gráfica:** Mapa de México (coropleta)
- **Fuente PDF:** IFT con datos del MOCIBA 2023 del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/mociba/2023/
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_f3.py`
- **Output:** `output/Figura_F3.png`
- **Estado:** ⬜ Pendiente

---

### Figura F.4 — Porcentaje de la población de 12 años y más que vivió ciberacoso en los últimos 12 meses, por entidad federativa y sexo
- **Página PDF:** 88
- **Tipo de gráfica:** Barras agrupadas por estado y sexo
- **Fuente PDF:** IFT con datos del MOCIBA 2023 del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/mociba/2023/
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_f4.py`
- **Output:** `output/Figura_F4.png`
- **Estado:** ⬜ Pendiente

---

### Figura F.5 — Porcentaje de la población que vivió ciberacoso en los últimos 12 meses, por sexo y rango de edad
- **Página PDF:** 89
- **Tipo de gráfica:** Barras agrupadas
- **Fuente PDF:** IFT con datos del MOCIBA 2023 del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/mociba/2023/
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_f5.py`
- **Output:** `output/Figura_F5.png`
- **Estado:** ⬜ Pendiente

---

### Figura F.6 — Distribución porcentual de las situaciones de ciberacoso experimentadas en los últimos 12 meses, por sexo
- **Página PDF:** 90
- **Tipo de gráfica:** Barras horizontales agrupadas
- **Fuente PDF:** IFT con datos del MOCIBA 2023 del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/mociba/2023/
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_f6.py`
- **Output:** `output/Figura_F6.png`
- **Estado:** ⬜ Pendiente

---

### Figura F.7 — Medidas de seguridad realizadas por las personas que utilizaron Internet o celular inteligente durante los últimos tres meses
- **Página PDF:** 91
- **Tipo de gráfica:** Barras horizontales
- **Fuente PDF:** IFT con datos del MOCIBA 2023 del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/mociba/2023/
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_f7.py`
- **Output:** `output/Figura_F7.png`
- **Estado:** ⬜ Pendiente

---

### Figura F.8 — Porcentaje de población de 12 años y más que vivió ciberacoso por medios digitales
- **Página PDF:** 92
- **Tipo de gráfica:** Pastel / dona o barras
- **Fuente PDF:** IFT con datos del MOCIBA 2023 del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/mociba/2023/
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_f8.py`
- **Output:** `output/Figura_F8.png`
- **Estado:** ⬜ Pendiente

---

### Figura F.9 — Medidas tomadas contra el ciberacoso experimentado
- **Página PDF:** 93
- **Tipo de gráfica:** Barras horizontales
- **Fuente PDF:** IFT con datos del MOCIBA 2023 del INEGI
- **Enlace de descarga:** https://www.inegi.org.mx/programas/mociba/2023/
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_f9.py`
- **Output:** `output/Figura_F9.png`
- **Estado:** ⬜ Pendiente

---

### Figura F.10 — Personas usuarias con mayor riesgo de ser víctimas de Violencia Digital a través de Internet
- **Página PDF:** 94
- **Tipo de gráfica:** Barras o infografía
- **Fuente PDF:** IFT, 3ª Encuesta 2023, Usuarios de Servicios de Telecomunicaciones
- **Enlace de descarga:** ⬜ Por identificar (encuestas IFT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_f10.py`
- **Output:** `output/Figura_F10.png`
- **Estado:** ⬜ Pendiente

---

### Figura F.11 — Personas usuarias con mayor riesgo de ser víctimas de violencia digital a través de Internet, desagregada por sexo
- **Página PDF:** 95
- **Tipo de gráfica:** Barras agrupadas por sexo
- **Fuente PDF:** IFT, 3ª Encuesta 2023
- **Enlace de descarga:** ⬜ Por identificar (encuestas IFT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_f11.py`
- **Output:** `output/Figura_F11.png`
- **Estado:** ⬜ Pendiente

---

### Figura F.12 — Personas usuarias con mayor riesgo de ser víctimas de violencia digital a través del teléfono móvil
- **Página PDF:** 96
- **Tipo de gráfica:** Barras o infografía
- **Fuente PDF:** IFT, 3ª Encuesta 2023
- **Enlace de descarga:** ⬜ Por identificar (encuestas IFT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_f12.py`
- **Output:** `output/Figura_F12.png`
- **Estado:** ⬜ Pendiente

---

### Figura F.13 — Personas usuarias con mayor riesgo de ser víctimas de violencia digital a través del teléfono móvil. Por sexo
- **Página PDF:** 97
- **Tipo de gráfica:** Barras agrupadas por sexo
- **Fuente PDF:** IFT, 3ª Encuesta 2023
- **Enlace de descarga:** ⬜ Por identificar (encuestas IFT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_f13.py`
- **Output:** `output/Figura_F13.png`
- **Estado:** ⬜ Pendiente

---

### Figura F.14 — Medidas preventivas y de protección ante la violencia digital
- **Página PDF:** 98
- **Tipo de gráfica:** Barras horizontales
- **Fuente PDF:** IFT, 3ª Encuesta 2023
- **Enlace de descarga:** ⬜ Por identificar (encuestas IFT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_f14.py`
- **Output:** `output/Figura_F14.png`
- **Estado:** ⬜ Pendiente

---

### Figura F.15 — Acciones para proteger y prevenir la violencia digital en Internet
- **Página PDF:** 99
- **Tipo de gráfica:** Barras horizontales
- **Fuente PDF:** IFT, 3ª Encuesta 2023
- **Enlace de descarga:** ⬜ Por identificar (encuestas IFT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_f15.py`
- **Output:** `output/Figura_F15.png`
- **Estado:** ⬜ Pendiente

---

### Figura F.16 — Acciones en caso de experimentar violencia digital en Internet
- **Página PDF:** 100
- **Tipo de gráfica:** Barras horizontales
- **Fuente PDF:** IFT, 3ª Encuesta 2023
- **Enlace de descarga:** ⬜ Por identificar (encuestas IFT)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_f16.py`
- **Output:** `output/Figura_F16.png`
- **Estado:** ⬜ Pendiente

---

# G. INDICADORES DE RADIODIFUSIÓN

---

### Figura G.1 — Concesiones otorgadas de radiodifusión para AM, FM y TDT, a nivel nacional
- **Página PDF:** 101
- **Tipo de gráfica:** Barras agrupadas o mapa
- **Fuente PDF:** IFT BIT Estatal — Concesiones de radio AM, FM y TDT a diciembre de 2023
- **Enlace de descarga:** https://bitestatal.ift.org.mx/#/estado/Nacional
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_g1.py`
- **Output:** `output/Figura_G1.png`
- **Estado:** ⬜ Pendiente

---

# H. AUDIENCIAS DE TELEVISIÓN Y RADIO

---

### Figura H.1 — Porcentaje de personas que vieron la televisión por hora a nivel nacional (28 ciudades)
- **Página PDF:** 102
- **Tipo de gráfica:** Línea por hora del día
- **Fuente PDF:** Base de Datos de Audiencias-Ratings TV 28 Ciudades de Nielsen IBOPE (MSS TV)
- **Enlace de descarga:** ⬜ No disponible públicamente (Nielsen IBOPE)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_h1.py`
- **Output:** `output/Figura_H1.png`
- **Estado:** ⬜ Pendiente

---

### Figura H.2 — Horas dedicadas y Rating promedio por género en canales nacionales (28 ciudades)
- **Página PDF:** 103
- **Tipo de gráfica:** Barras horizontales agrupadas
- **Fuente PDF:** Nielsen IBOPE (MSS TV)
- **Enlace de descarga:** ⬜ No disponible públicamente
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_h2.py`
- **Output:** `output/Figura_H2.png`
- **Estado:** ⬜ Pendiente

---

### Figura H.3 — Porcentaje de personas que vieron la televisión por hora en Ciudad de México
- **Página PDF:** 104
- **Tipo de gráfica:** Línea por hora del día
- **Fuente PDF:** Nielsen IBOPE (MSS TV)
- **Enlace de descarga:** ⬜ No disponible públicamente
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_h3.py`
- **Output:** `output/Figura_H3.png`
- **Estado:** ⬜ Pendiente

---

### Figura H.4 — Horas dedicadas y Rating promedio por género en canales nacionales (CDMX)
- **Página PDF:** 105
- **Tipo de gráfica:** Barras horizontales agrupadas
- **Fuente PDF:** Nielsen IBOPE (MSS TV)
- **Enlace de descarga:** ⬜ No disponible públicamente
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_h4.py`
- **Output:** `output/Figura_H4.png`
- **Estado:** ⬜ Pendiente

---

### Figura H.5 — Porcentaje de personas que vieron la televisión por hora en Guadalajara
- **Página PDF:** 106
- **Tipo de gráfica:** Línea por hora del día
- **Fuente PDF:** Nielsen IBOPE (MSS TV)
- **Enlace de descarga:** ⬜ No disponible públicamente
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_h5.py`
- **Output:** `output/Figura_H5.png`
- **Estado:** ⬜ Pendiente

---

### Figura H.6 — Horas dedicadas y Rating promedio por género en canales nacionales (Guadalajara)
- **Página PDF:** 107
- **Tipo de gráfica:** Barras horizontales agrupadas
- **Fuente PDF:** Nielsen IBOPE (MSS TV)
- **Enlace de descarga:** ⬜ No disponible públicamente
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_h6.py`
- **Output:** `output/Figura_H6.png`
- **Estado:** ⬜ Pendiente

---

### Figura H.7 — Porcentaje de personas que vieron la televisión por hora en Monterrey
- **Página PDF:** 108
- **Tipo de gráfica:** Línea por hora del día
- **Fuente PDF:** Nielsen IBOPE (MSS TV)
- **Enlace de descarga:** ⬜ No disponible públicamente
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_h7.py`
- **Output:** `output/Figura_H7.png`
- **Estado:** ⬜ Pendiente

---

### Figura H.8 — Horas dedicadas y Rating promedio por género en canales nacionales (Monterrey)
- **Página PDF:** 109
- **Tipo de gráfica:** Barras horizontales agrupadas
- **Fuente PDF:** Nielsen IBOPE (MSS TV)
- **Enlace de descarga:** ⬜ No disponible públicamente
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_h8.py`
- **Output:** `output/Figura_H8.png`
- **Estado:** ⬜ Pendiente

---

### Figura H.9 — Porcentaje de personas que vieron la televisión por hora en 25 ciudades
- **Página PDF:** 110
- **Tipo de gráfica:** Línea por hora del día
- **Fuente PDF:** Nielsen IBOPE (MSS TV)
- **Enlace de descarga:** ⬜ No disponible públicamente
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_h9.py`
- **Output:** `output/Figura_H9.png`
- **Estado:** ⬜ Pendiente

---

### Figura H.10 — Horas dedicadas y Rating promedio por género en canales nacionales (25 ciudades)
- **Página PDF:** 111
- **Tipo de gráfica:** Barras horizontales agrupadas
- **Fuente PDF:** Nielsen IBOPE (MSS TV)
- **Enlace de descarga:** ⬜ No disponible públicamente
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_h10.py`
- **Output:** `output/Figura_H10.png`
- **Estado:** ⬜ Pendiente

---

### Figura H.11 — Proporción de personas que escucharon la radio por hora (%) — Nacional
- **Página PDF:** 112
- **Tipo de gráfica:** Línea por hora del día
- **Fuente PDF:** Base de Datos de INRA a través del software INRAM
- **Enlace de descarga:** ⬜ No disponible públicamente (INRA)
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_h11.py`
- **Output:** `output/Figura_H11.png`
- **Estado:** ⬜ Pendiente

---

### Figura H.12 — Proporción de personas que escucharon la radio por hora (%) — CDMX
- **Página PDF:** 113
- **Tipo de gráfica:** Línea por hora del día
- **Fuente PDF:** Base de Datos de INRA (INRAM)
- **Enlace de descarga:** ⬜ No disponible públicamente
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_h12.py`
- **Output:** `output/Figura_H12.png`
- **Estado:** ⬜ Pendiente

---

### Figura H.13 — Proporción de personas que escucharon la radio por hora (%) — Guadalajara
- **Página PDF:** 114
- **Tipo de gráfica:** Línea por hora del día
- **Fuente PDF:** Base de Datos de INRA (INRAM)
- **Enlace de descarga:** ⬜ No disponible públicamente
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_h13.py`
- **Output:** `output/Figura_H13.png`
- **Estado:** ⬜ Pendiente

---

### Figura H.14 — Proporción de personas que escucharon la radio por hora (%) — Monterrey
- **Página PDF:** 115
- **Tipo de gráfica:** Línea por hora del día
- **Fuente PDF:** Base de Datos de INRA (INRAM)
- **Enlace de descarga:** ⬜ No disponible públicamente
- **Archivo local:** `datos/` — ⬜ Por descargar
- **Datos utilizados:** ⬜ Por identificar
- **Cálculos:** ⬜ Por definir
- **Script:** `scripts/figura_h14.py`
- **Output:** `output/Figura_H14.png`
- **Estado:** ⬜ Pendiente

---

# NOTAS IMPORTANTES

## Figuras con datos NO disponibles públicamente
Las siguientes figuras usan datos propietarios que **no se pueden descargar libremente**:
- **H.1 – H.10**: Nielsen IBOPE (ratings de TV) — requiere licencia
- **H.11 – H.14**: INRA (ratings de radio) — requiere licencia
- **A.4, A.6**: Datos reportados directamente por operadores al IFT
- **D.5 – D.11**: Encuesta de Confianza en el Servicio de Internet (ECSI) del IFT — verificar disponibilidad
- **E.1 – E.9**: Encuestas internas del IFT — verificar si publican los tabulados

## Figuras que requieren mapas de México (coropletas)
Requieren `geopandas` + shapefile de entidades federativas:
- B.6, B.7, B.13, B.14, B.21, B.22, C.7, C.13, F.3

## Figuras que requieren cálculos especiales
- **IHH (Herfindahl-Hirschman):** B.10, B.18, B.25, C.10, C.16 → IHH = Σ(si²) donde si = cuota de mercado del operador i
- **Participación de mercado:** B.9, B.17, B.24, C.9, C.15 → % = accesos del operador / total de accesos × 100
