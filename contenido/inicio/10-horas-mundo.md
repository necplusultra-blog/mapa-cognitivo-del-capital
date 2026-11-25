---
seccion: "10 Masa mundial en horas"
id: horas-mundo
menu: Masa mundial en horas
oculta: true
---
## Masa mundial de plusvalor en horas de trabajo, 2000–{{hm-fin}}

El mismo criterio que en EE.UU., aplicado rama por rama a {{hm-np}} países que suman la mayor parte de la producción mundial. Hasta {{hm-base}}, cuentas por rama de WIOD. Desde {{.hm-base1}}, cuentas por rama de la OCDE para los países que las publican ({{hm-nocde}} en el último año), cuentas nacionales por rama de la ONU para el excedente de Brasil e India, encuestas de la OIT por sección de actividad para el empleo y las horas de Brasil, Indonesia, India, Rusia, México y Turquía, y extensión agregada de la OIT para China. El tramo punteado marca que todo lo posterior a {{.hm-base0}} se encadena al nivel de WIOD. Para cada país, e = pv/v con los asalariados de las ramas productivas, y la masa de plustrabajo = horas de esos asalariados × e/(1+e). La versión neta resta del plusvalor el consumo de capital fijo de las ramas de mercado.

[[cifra hm-n | Asalariados productivos en el mundo, {{.hm-fin}} (millones) | {{.hm-base0}}: {{hm-n14}}]]
[[cifra hm-masa | Masa anual de plustrabajo, bruta (miles de millones de horas) | 2000: {{hm-masa0}}; {{.hm-base0}}: {{hm-masa14}}]]
[[cifra hm-masan | Masa neta de depreciación (miles de millones de horas) | 2000: {{hm-masan0}}]]
[[cifra hm-e | Tasa de plusvalor mundial en horas, bruta y neta | China aporta {{hm-cn}} de la masa; India, {{hm-in}}]]

### Masa mundial de plustrabajo (miles de millones de horas al año)

Horas de trabajo no pagado que el capital obtiene en un año en los 42 países medidos, que reúnen la mayor parte de la producción mundial. La línea bruta cuenta todo el plustrabajo; la neta descuenta la parte del valor nuevo que sólo repone las máquinas y los edificios gastados. La bruta crece casi sin interrupción; la neta deja de crecer desde 2018. El tramo punteado indica que desde 2015 las cifras se encadenan a las de 2014.
{: .llano }

[[leyenda l-hm]]
[[grafico c-hm]]

<div id="rn-bloque" hidden markdown="1">

### ¿Resiste el estancamiento de la masa neta? Distintas estimaciones de la depreciación de China e India

China e India aportan dos tercios de la masa mundial, y su depreciación es la estimación más incierta de toda la medición. Aquí se recalcula la masa neta con cinco estimaciones alternativas, cambiando sólo la depreciación de esos dos países: más baja y más alta que la central, la del Banco Mundial, la mediana de los demás países y la de 2018 congelada. En todas, la masa neta crece con fuerza entre 2000 y 2018 y después queda prácticamente plana: entre 2018 y el último año cambia {{rn-rango}}. El estancamiento no es un efecto de la estimación de la depreciación.
{: .llano }

[[leyenda l-rn]]
[[grafico c-rn corto]]

[[tabla t-rn: Depreciación de China e India | 2000 | 2018 | Último año | 2000–2018 | 2018–último año]]

:::como ¿Cómo se calculan estas variantes?
Sólo cambia la proporción depreciación/PIB de China e India; los demás países quedan como en la central. **Central:** Penn World Table, δ·K/Y. **PWT × 0,8 y × 1,2:** tasa de depreciación un 20 % menor o mayor. **Banco Mundial:** consumo de capital fijo en % del ingreso nacional bruto (NY.ADJ.DKAP.GN.ZS), con el último dato mantenido en los años siguientes. **Mediana:** la mediana de la depreciación/PIB de los demás países medidos ese año. **Constante desde 2018:** la proporción de 2018 congelada, para aislar el efecto de su aumento posterior. En todos los casos, r = depreciación/PIB × valor agregado de mercado / v; e<sub>neta</sub> = e − r; masa neta = horas × e<sub>neta</sub> / (1 + e<sub>neta</sub>), como en la central. Resultado: `mundo_neta_robustez.csv`.
:::

</div>

### Tasa de plusvalor mundial en horas: plustrabajo / trabajo necesario

Cuántas horas trabaja para el capital un asalariado productivo del mundo por cada hora que trabaja para reponer su salario. Es casi constante: en promedio, el capital mundial no ha elevado el grado de explotación en este siglo. La masa crece porque hay más asalariados, no porque cada uno trabaje más para el capital. La versión neta baja, porque cada hora de trabajo pone en movimiento más capital fijo que hay que reponer.
{: .llano }

[[leyenda l-hme]]
[[grafico c-hme corto]]

:::como+ ¿Cómo se calcula el número de trabajadores productivos?
**Criterio.** Es productivo el asalariado cuyo salario es dinero invertido como capital y cuyo plustrabajo se convierte en plusvalor. Por eso cuentan los jornaleros eventuales, sea cual sea la duración de su empleo, y los asalariados agrícolas cuando su salario es capital. No cuentan los trabajadores por cuenta propia ni quienes trabajan por un salario que es simple medio de circulación: el Estado (salvo sus empresas que venden mercancías con fines de lucro), las instituciones sin fines de lucro y los hogares empleadores.

1. **2000–{{.hm-base0}} (WIOD, Cuentas Socioeconómicas 2016).** Para cada país se suman los asalariados (EMPE) y sus horas (H_EMPE) de las ramas productivas. Se excluyen las ramas de circulación (comercio G45–G47, finanzas y seguros K64–K66, servicios jurídicos, contables y de dirección M69–M70, publicidad M73) y las que están fuera de la producción capitalista (inmobiliario L68, administración pública O84, hogares T, organismos extraterritoriales U). Educación (P85) y salud (Q) sólo cuentan en su parte capitalista: la parte pagada por el Estado o por instituciones sin fines de lucro queda fuera (véase el paso 6).
2. **China.** WIOD no distingue asalariados en China. Se toma el total de asalariados de las estimaciones modeladas de la OIT y se reparte entre las ramas no agrícolas en proporción a su ocupación en WIOD: s = asalariados OIT / (ocupación OIT × (1 − peso agrícola WIOD)). Los asalariados productivos son la ocupación de las ramas productivas no agrícolas × s. La agricultura china es casi enteramente familiar y no tiene asalariados en las fuentes, así que no aporta. Las horas suponen una jornada de 46 h semanales y 50 semanas (sensibilidad: 44 y 49 h).
3. **Desde {{.hm-base1}}, países de la OCDE (tabla 7 de cuentas nacionales).** Asalariados (SAL) y sus horas, por sección CIIU rev. 4, con el mismo criterio de ramas. La serie se encadena al nivel WIOD de 2014: N<sub>t</sub> = N<sub>WIOD,2014</sub> × N<sub>OCDE,t</sub> / N<sub>OCDE,2014</sub>; las horas por asalariado, igual.
4. **Desde {{.hm-base1}}, países sin asalariados por rama en la OCDE: medición por sección con la OIT.** Para Brasil, Indonesia, India, Rusia, México, Turquía, Chipre y Malta, las encuestas de fuerza de trabajo armonizadas por la OIT dan los asalariados, sus horas y su ingreso medio por sección de actividad. Con una sola encuesta por país, desde el primer año disponible a partir de 2014 (India: 2018; Rusia: 2017), se miden la proporción productiva de los asalariados, las horas semanales de las secciones productivas y la parte productiva de la masa salarial, y con ellas se corrigen el número de asalariados productivos, sus horas y la tasa de plusvalor de la extensión agregada. China no publica asalariados por sección en la OIT; su número y su tasa de plusvalor se miden hasta 2022 con el empleo y el ingreso del trabajo por rama de la OCDE (TiM), y después siguen la extensión agregada.
5. **Desde {{.hm-base1}}, extensión agregada (OIT).** N<sub>t</sub> = N<sub>2014</sub> × asalariados totales<sub>t</sub> / asalariados totales<sub>2014</sub> (estimaciones modeladas de la OIT), manteniendo la proporción productiva de 2014; las horas por ocupado siguen las horas semanales de la OIT. **India:** WIOD cuenta como asalariados a los regulares y a los jornaleros eventuales; la serie de la OIT sólo recoge a los regulares. Para India, N se extiende con la ocupación total de la OIT por la proporción de trabajadores no cuenta propia de las encuestas oficiales (NSS 2011-12 y PLFS 2017-18 a 2023-24).
6. **Educación y salud públicas y sin fines de lucro.** El cálculo se hace dos veces, con toda la educación y la salud dentro y con toda fuera. La estimación central combina ambas según la parte no capitalista g de cada país: g = (ocupados del gobierno general + ocupados de instituciones sin fines de lucro − ocupados de la administración pública) / ocupados de educación y salud, con las cuentas por sector institucional de la OCDE; fuera de ellas, las encuestas de empleo público por actividad de la OIT, y si no hay, la mediana de los países medidos. En EE.UU. se suma la parte sin fines de lucro según el BLS. Las horas necesarias, las de plustrabajo y los asalariados se combinan como (1 − g) × «dentro» + g × «fuera». Las proporciones están en `mundo_horas_parte_publica.csv`. Los asalariados de empresas estatales que venden mercancías con fines de lucro cuentan como productivos: su salario es capital.
7. El total mundial es la suma de los países. La fuente de cada país y año está en [mundo_horas_paises.csv](descargas/).
:::

:::como+ ¿Cómo se calcula la masa mundial de plusvalor?
1. **Capital variable (v):** remuneración de los asalariados de las ramas productivas (WIOD: COMP; OCDE: D1).
2. **Plusvalor (pv):** valor agregado bruto de las ramas de mercado (todas menos L68, O84, T, U y la parte no capitalista de educación y salud) − ingreso laboral imputado a los trabajadores por cuenta propia − v. Ese ingreso es LAB − COMP en WIOD y, en la OCDE, no asalariados × remuneración media por asalariado de la misma sección. Los salarios de las ramas de circulación quedan dentro de pv: son deducciones de la masa global de plusvalor.
3. **Tasa de plusvalor:** e = pv/v, en moneda nacional, de modo que no hace falta convertir monedas. Desde 2015, e se encadena al nivel WIOD de 2014 con la variación medida por rama en la OCDE (tabla 6) o, donde no la hay, con la participación del trabajo de la OIT: e<sub>t</sub> = e<sub>2014</sub> × [(1 − LS<sub>t</sub>)/LS<sub>t</sub>] / [(1 − LS<sub>2014</sub>)/LS<sub>2014</sub>]. En Brasil e India (2015–2020), e se mide rama por rama con las cuentas nacionales de la ONU (tabla 2.6: remuneración, ingreso mixto y valor agregado por sección) y se encadena igual. En China (2015–2022), e se mide rama por rama con el empleo y el ingreso del trabajo por rama de la OCDE (TiM 2025, coherente con sus tablas mundiales) y se encadena igual. En los demás países medidos por sección con la OIT, 1 + e<sub>t</sub> se multiplica por q<sub>b</sub>/q<sub>t</sub>, donde q es la parte productiva de la masa salarial: si crece la masa salarial productiva, crece v y baja e.
4. **Versión neta:** e<sub>neta</sub> = e − r, con r = consumo de capital fijo de las ramas de mercado / v. En la OCDE se mide por rama (P51C). Donde no hay medición, r = (δ·K/Y de la PWT) × valor agregado de mercado / v, calibrado con el cociente OCDE/PWT de 2014 del propio país o, fuera de la OCDE, con la mediana de esos cocientes ({{hm-kmed}}), porque la depreciación de la PWT incluye viviendas y capital público.
5. **Masa en horas:** plustrabajo = H × e / (1 + e) para cada país, sumado sobre todos. La tasa mundial en horas es Σ plustrabajo / Σ trabajo necesario. Las observaciones con e fuera de (0, 8) se excluyen por anomalías de los datos: {{hm-excl}}.
:::

### Los mayores núcleos de plustrabajo, {{.hm-fin}}

Los países donde se produce más plustrabajo. China e India suman casi dos tercios del total.
{: .llano }

[[tabla t-hm: País | Asalariados productivos (millones) | e bruta | e neta | Plustrabajo bruto (miles de millones de horas) | % del total | Fuente de e]]

### Cuánto pesa cada supuesto (estimación central, con China)

Cada fila cambia un solo supuesto respecto de la estimación central. Las filas marcadas como contraste no son lecturas alternativas del criterio adoptado: muestran cuánto pesan en la masa mundial los jornaleros eventuales de India y la agricultura asalariada de India y China.
{: .nota }

Cada fila cambia un solo supuesto y muestra cuánto cambia el total. Sirve para saber qué cifras son firmes y cuáles dependen de decisiones.
{: .llano }

[[tabla t-hms: Año | Caso | Plustrabajo (miles de millones de horas) | Asalariados productivos (millones) | Diferencia | Nota]]

:::como Diagnóstico del empalme OCDE–WIOD en 2014
Si las dos fuentes miden lo mismo, los cocientes de 2014 deberían estar cerca de 1. El nivel lo pone WIOD; la OCDE sólo aporta la variación posterior.

[[tabla t-hmd: País | e WIOD | e OCDE | Asalariados OCDE/WIOD | Horas OCDE/WIOD | r PWT | r OCDE | Último año OCDE]]
:::

Advertencias: las cifras posteriores a 2014 son encadenadas, no niveles medidos de nuevo; en los países de la OCDE la variación sí se mide por rama. China es una estimación. No hay corrección intra-rama en la escala mundial. La suma mundial cuenta horas de trabajo explotado, no tiempo de trabajo abstracto del mercado mundial: según Marx, el trabajo nacional más productivo cuenta en el mercado mundial como trabajo más intenso, y esa ponderación queda para la fase de la transformación. Por diferencias de definición, la e de EE.UU. aquí no coincide con la de la sección de EE.UU.
{: .nota }
