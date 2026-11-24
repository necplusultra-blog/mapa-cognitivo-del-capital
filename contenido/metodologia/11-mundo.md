---
seccion: "11 Escala mundial"
id: mundo
menu: Escala mundial
---
## Escala mundial

**Tasa (Penn World Table 11.0).**

<div class="f">bruta = (1 − labsh) · cgdpo / cn · neta = ((1 − labsh) · cgdpo − δ · cn) / cn · IRR: tasa interna de retorno real de la PWT</div>

Los países se ponderan por stock de capital (cn) o por PIB (cgdpo), con y sin China, en un panel balanceado desde 1960 o no balanceado. La masa de ganancia bruta en dólares es Σ (1 − labsh) · PIB real. La PWT mide la economía total: no distingue trabajo productivo de improductivo.

**Masa mundial en horas.** Aplica el mismo criterio por ramas del punto 3, país por país, y suma. Hay tres tramos de fuentes; los tres usan las mismas definiciones.

**(a) 2000–2014: WIOD, Cuentas Socioeconómicas 2016** (43 países; Taiwán queda excluido por anomalías). Para cada país:

- **Ramas improductivas por circulación:** comercio (G45–G47), finanzas y seguros (K64–K66), servicios jurídicos, contables y de dirección (M69–M70), publicidad (M73).
- **Fuera de la producción capitalista:** inmobiliario (L68, renta), administración pública (O84), hogares empleadores (T), organismos extraterritoriales (U). Educación (P85) y salud (Q): sólo su parte capitalista es productiva. La parte pública y sin fines de lucro se estima por país (véase «Educación y salud públicas» más abajo).
- **N** = Σ<sub>productivas</sub> asalariados (EMPE) · **H** = Σ<sub>productivas</sub> horas de los asalariados (H\_EMPE) · **v** = Σ<sub>productivas</sub> remuneración (COMP).
- **pv** = Σ<sub>mercado</sub> VA − Σ<sub>mercado</sub> (LAB − COMP) − v. LAB − COMP es el ingreso laboral imputado a los trabajadores por cuenta propia, que no son asalariados del capital.

<div class="f">e = pv / v · plustrabajo = H · e / (1 + e) · trabajo necesario = H / (1 + e) · e mundial en horas = Σ plustrabajo / Σ trabajo necesario</div>

**China.** WIOD no distingue asalariados en China (COMP = LAB). Con la OIT (estimaciones modeladas, `EMP_2EMP_SEX_STE_NB`) se calcula la proporción de asalariados entre los ocupados no agrícolas:

<div class="f">s<sub>t</sub> = asalariados OIT<sub>t</sub> / [ocupados OIT<sub>t</sub> × (1 − peso agrícola WIOD<sub>t</sub>)], con tope 1</div>

En las ramas no agrícolas, la remuneración y la ocupación se multiplican por s; en la agricultura (A01–A03), casi enteramente familiar, s = 0 y toda su remuneración se trata como ingreso de cuenta propia. Horas: 46 h semanales × 50 semanas por asalariado. El método anterior, que aplicaba la proporción de asalariados de toda la economía también a la agricultura, se conserva en el cuadro de sensibilidad (+3 %).

**(b) 2015–último año, países de la OCDE: cuentas nacionales por rama** (tablas 6 y 7 de la OCDE, SNA 2008: `DSD_NAMAIN10@DF_TABLE6` y `@DF_TABLE7`). Mismo criterio a nivel de sección CIIU rev. 4: improductivas G, K, M69–M70, M73; fuera L, O, T, U (y P, Q en la segunda variante).

<div class="f">v = Σ<sub>prod</sub> D1 · cp = Σ<sub>mercado</sub> SELF<sub>personas</sub> × D1/SAL<sub>personas</sub> · pv = Σ<sub>mercado</sub> B1G − cp − v · N = Σ<sub>prod</sub> SAL<sub>personas</sub> · H = Σ<sub>prod</sub> SAL<sub>horas</sub> · r = Σ<sub>mercado</sub> P51C / v</div>

Las series OCDE se encadenan al nivel WIOD de 2014: X<sub>t</sub> = X<sub>WIOD,2014</sub> × X<sub>OCDE,t</sub> / X<sub>OCDE,2014</sub>, para X = e, N, horas por asalariado y r. Así WIOD fija el nivel y la OCDE aporta la variación medida por rama. Reglas de completitud: T y U faltantes valen cero; si faltan secciones todas productivas y de mercado (Japón: E, N, S), su suma se obtiene como residuo del total; si un país no informa M69–M70 y M73, su peso en M se toma de WIOD 2014; una sección sin dato de no asalariados vale cero; e sólo se encadena mientras la imputación de no asalariados sea la misma que en 2014. Corea queda fuera (le faltan secciones improductivas). México, Turquía, Chipre y Malta no publican asalariados por rama: su e sale de la OCDE y su N de la OIT. Después del último año OCDE de cada país, la serie continúa con la variación OIT. Los cocientes OCDE/WIOD de 2014 se publican como diagnóstico (`mundo_horas_ocde_diagnostico.csv`): en la mayoría de los países están entre 0,95 y 1,05 para N y para H.

**(b′) Desde 2014, países sin asalariados por rama en la OCDE: encuestas de la OIT por sección.** Para Brasil, Indonesia, India, Rusia, México, Turquía, Chipre y Malta se usan las series de ILOSTAT por sección CIIU rev. 4: asalariados (`EES_TEES_SEX_ECO_NB`), horas semanales efectivas (`HOW_TEMP_SEX_ECO_NB`) e ingreso medio mensual en moneda nacional (`EAR_EMTA_SEX_ECO_CUR_NB`), siempre de una sola encuesta por país (la que cubre más años desde 2014). Con el mismo criterio de ramas, y con el peso de M69–M70 y M73 dentro de M tomado de WIOD 2014:

<div class="f">ps = asalariados productivos / asalariados · hp = horas medias de las secciones productivas · q = masa salarial productiva / masa salarial</div>

Desde el primer año b de la encuesta (2014 en la mayoría; India 2018; Rusia 2017), el resultado de la extensión agregada se corrige así:

<div class="f">N<sub>t</sub> = N<sup>agregado</sup><sub>t</sub> × ps<sub>t</sub>/ps<sub>b</sub> · h<sub>t</sub> = h<sub>b</sub> × hp<sub>t</sub>/hp<sub>b</sub> · 1 + e<sub>t</sub> = (1 + e<sup>agregado</sup><sub>t</sub>) × q<sub>b</sub>/q<sub>t</sub></div>

En México y Turquía, e proviene de las cuentas por rama de la OCDE y sólo se corrigen N y h. Después del último año de la encuesta se mantienen las proporciones. China no publica asalariados por sección en ILOSTAT (su encuesta de fuerza de trabajo sólo se difunde agregada desde 2016), así que queda en la extensión agregada. El diagnóstico por país está en `mundo_horas_ilo_secciones.csv`. Limitaciones: la serie de asalariados de India en la OIT sólo recoge a los trabajadores regulares, de modo que su proporción productiva se mide entre ellos; las secciones no separan M69–M70 y M73.

**(b″) Desde 2014, excedente por rama fuera de la OCDE: cuentas nacionales de la ONU (tabla 2.6).** La tabla 2.6 de la base de cuentas nacionales oficiales de la ONU (UNdata, SNA) publica, por sección CIIU rev. 4, el valor agregado, la remuneración de asalariados, el ingreso mixto, el excedente de explotación y el consumo de capital fijo. Con ella, para Brasil e India, la tasa de plusvalor deja de seguir la participación agregada del trabajo y pasa a medirse rama por rama con el mismo criterio que en WIOD y la OCDE:

<div class="f">v = Σ<sub>productivas</sub> remuneración · pv = VA<sub>mercado</sub> − ingreso mixto<sub>mercado</sub> − v · e = pv / v · r = CCF<sub>mercado</sub> / v</div>

Cada serie publicada por el país (una «serie» de la ONU es un segmento con base y método homogéneos) se encadena por separado: su primer año desde 2014 se iguala al valor de la trayectoria anterior y desde ahí manda su variación; después de su último año continúa la variación anterior. Se toleran hasta cuatro secciones faltantes (valen cero) cuando no son productivas de peso. Resultado: Brasil medido en 2015–2020 (cociente ONU/WIOD de 1+e en 2014: 1,10) e India en 2015–2020 (0,89). Los diagnósticos están en `mundo_horas_onu_ramas.csv` y `mundo_horas_onu_diagnostico.csv`. China e Indonesia no tienen la tabla 2.6 en la base de la ONU, y la de Rusia termina en 2013; quedan con la medición anterior. En los países medidos por la ONU no se aplica la corrección q de la OIT a e (sí a N y a las horas).

**(c) 2015–2025, extensión agregada con la OIT** (base de todos los países fuera de la OCDE y único método para China).

<div class="f">e<sub>t</sub> = e<sub>2014</sub> × [(1 − LS<sub>t</sub>)/LS<sub>t</sub>] / [(1 − LS<sub>2014</sub>)/LS<sub>2014</sub>] · N<sub>t</sub> = N<sub>2014</sub> × A<sub>t</sub>/A<sub>2014</sub> · h<sub>t</sub> = h<sub>2014</sub> × hs<sub>t</sub>/hs<sub>2014</sub></div>

- **LS**: participación del trabajo en el ingreso (OIT, ODS 10.4.1, `LAP_2GDP_NOC_RT`).
- **A**: asalariados totales, estimaciones modeladas y armonizadas de la OIT (`EMP_2EMP_SEX_STE_NB`); la proporción productiva de 2014 se mantiene. Las series por sección (`EES_TEES_SEX_ECO_NB`) tienen quiebres de encuesta y no se usan.
- **India**: WIOD cuenta como asalariados a los regulares y a los jornaleros eventuales, como las encuestas NSS; la serie de asalariados de la OIT sólo recoge a los regulares (91 millones en 2014, frente a 315 millones en WIOD) y crece un 64 % hasta 2025. Por eso, para India, A<sub>t</sub> = ocupados OIT<sub>t</sub> × (1 − proporción de cuenta propia<sub>t</sub>), con la proporción de cuenta propia en estatus usual de NSS 2011-12 (52,2 %) y PLFS 2017-18 (52,2 %), 2021-22 (55,8 %), 2022-23 (57,3 %) y 2023-24 (58,4 %), interpolada y mantenida después del último dato. Resultado: +13 % de asalariados entre 2014 y 2025, en vez de +64 %.
- **hs**: horas semanales por ocupado (`HOW_TEMP_SEX_ECO_NB`); si faltan, constantes.

**Versión neta de depreciación.** e<sub>neta</sub> = e − r, con r = consumo de capital fijo de las ramas de mercado / v. En los países de la OCDE, r se mide por rama (P51C) desde 2014. En los demás años y países:

<div class="f">r = k · (δ·K/Y)<sub>PWT</sub> × VA<sub>mercado</sub> / v · con VA<sub>mercado</sub>/v = 1 + e + cp/v en los años encadenados</div>

(δ·K/Y)<sub>PWT</sub> = delta · cn / cgdpo de la Penn World Table (último valor mantenido después de 2023). Como esa depreciación abarca todo el capital fijo, incluidas viviendas y capital público, se calibra con k = r<sub>OCDE,2014</sub> / r<sub>PWT,2014</sub> del propio país o, fuera de la OCDE, con la mediana de esos cocientes (0,76). La tabla de calibración está en `mundo_horas_calibracion_depreciacion.csv`. En la versión neta, la caída de e tras 2008 refleja sobre todo el alza de la depreciación medida por la PWT en China e India; es una estimación, no una medición por rama.

**Sensibilidad** (`mundo_horas_sensibilidad.csv`). Cada fila cambia un solo supuesto: versión neta; jornada china de 44 o 49 h; India con el nivel de asalariados de la OIT (sólo regulares); agricultura de India y China fuera de la producción capitalista; método anterior para China. **Criterio adoptado** (decisión teórica del autor): los jornaleros eventuales son trabajadores productivos siempre que su plustrabajo se convierta en plusvalor, sea cual sea la duración de su empleo; el trabajo agrícola es productivo siempre que el salario de esos obreros sea dinero invertido como capital, y no dinero gastado como simple medio de circulación para comprar un trabajo improductivo. Por eso la estimación central los incluye. Las filas «India: nivel de asalariados de la OIT» y «agricultura fuera» no son interpretaciones alternativas del criterio: muestran cuánto pesan esos trabajadores en la masa (entre 11 % y 22 %). El límite práctico del criterio es estadístico: las cuentas no permiten separar a los jornaleros contratados por empresas capitalistas de los contratados por hogares para su consumo; los segundos sólo se excluyen cuando aparecen en la rama de hogares empleadores (T).

Otras advertencias: no hay corrección intra-rama; por diferencias de definición, la e de EE.UU. en esta serie no coincide con la de la sección de EE.UU.; las observaciones con e fuera de (0, 8) se excluyen y se registran en `mundo_horas_excluidos.csv`. La fuente de e, N y r de cada país y año está en `mundo_horas_paises.csv`.

**Educación y salud públicas y sin fines de lucro.** El cálculo completo se hace con educación y salud dentro (variante «productivas») y fuera (variante «fuera»). La estimación central combina ambas con la parte no capitalista g de cada país y año:

<div class="f">g = (ocupados S13 + ocupados S15 − ocupados O) / ocupados (P + Q), entre 0 y 1</div>

S13 es el gobierno general y S15 las instituciones sin fines de lucro (OCDE, empleo por sector institucional, `DSD_NAMAIN10@DF_TABLE3_EMP_SECTOR`); O, P y Q vienen de la tabla 7. Fuera de esas cuentas se usa la proporción de empleo público en P + Q de las encuestas de la OIT (`EMP_PUBL_SEX_ECO_NB`), cuando es plausible (entre 0,2 y 1), y si no hay, la mediana de los países medidos. En EE.UU., a la parte pública se suma la parte sin fines de lucro del BLS. Como N, H, las horas necesarias y las de plustrabajo son sumas por sección, la combinación lineal (1 − g) · dentro + g · fuera reproduce la medición con sólo la parte capitalista de educación y salud. Límites: S15 incluye también organizaciones religiosas y civiles, de modo que g tiende a sobrestimarse; las encuestas de empleo público de la OIT son heterogéneas; China, Rusia, Canadá, Australia, Países Bajos, Noruega, Suecia y Chipre usan la mediana. Detalle en `mundo_horas_parte_publica.csv`.

**Empresas estatales.** Los asalariados de empresas del Estado que venden mercancías con fines de lucro cuentan como productivos (decisión del autor): su salario es capital adelantado por el Estado. No se separan, porque las cuentas por rama los incluyen junto con los de las empresas privadas.
