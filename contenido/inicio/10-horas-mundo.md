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

### Tasa de plusvalor mundial en horas: plustrabajo / trabajo necesario

Cuántas horas trabaja para el capital un asalariado productivo del mundo por cada hora que trabaja para reponer su salario. Es casi constante: en promedio, el capital mundial no ha elevado el grado de explotación en este siglo. La masa crece porque hay más asalariados, no porque cada uno trabaje más para el capital. La versión neta baja, porque cada hora de trabajo pone en movimiento más capital fijo que hay que reponer.
{: .llano }

[[leyenda l-hme]]
[[grafico c-hme corto]]

:::como+ ¿Cómo se calcula el número de trabajadores productivos?
**Criterio.** Es productivo el asalariado cuyo salario es dinero invertido como capital y cuyo plustrabajo se convierte en plusvalor. Por eso cuentan los jornaleros eventuales, sea cual sea la duración de su empleo, y los asalariados agrícolas cuando su salario es capital. No cuentan los trabajadores por cuenta propia ni quienes trabajan por un salario que es simple medio de circulación (Estado, hogares empleadores).

1. **2000–{{.hm-base0}} (WIOD, Cuentas Socioeconómicas 2016).** Para cada país se suman los asalariados (EMPE) y sus horas (H_EMPE) de las ramas productivas. Se excluyen las ramas de circulación (comercio G45–G47, finanzas y seguros K64–K66, servicios jurídicos, contables y de dirección M69–M70, publicidad M73) y las que están fuera de la producción capitalista (inmobiliario L68, administración pública O84, hogares T, organismos extraterritoriales U). Educación (P85) y salud (Q) cuentan como productivas en la variante central y como fuera de la producción capitalista en la otra, porque en muchos países son mayoritariamente públicas.
2. **China.** WIOD no distingue asalariados en China. Se toma el total de asalariados de las estimaciones modeladas de la OIT y se reparte entre las ramas no agrícolas en proporción a su ocupación en WIOD: s = asalariados OIT / (ocupación OIT × (1 − peso agrícola WIOD)). Los asalariados productivos son la ocupación de las ramas productivas no agrícolas × s. La agricultura china es casi enteramente familiar y no tiene asalariados en las fuentes, así que no aporta. Las horas suponen una jornada de 46 h semanales y 50 semanas (sensibilidad: 44 y 49 h).
3. **Desde {{.hm-base1}}, países de la OCDE (tabla 7 de cuentas nacionales).** Asalariados (SAL) y sus horas, por sección CIIU rev. 4, con el mismo criterio de ramas. La serie se encadena al nivel WIOD de 2014: N<sub>t</sub> = N<sub>WIOD,2014</sub> × N<sub>OCDE,t</sub> / N<sub>OCDE,2014</sub>; las horas por asalariado, igual.
4. **Desde {{.hm-base1}}, países sin asalariados por rama en la OCDE: medición por sección con la OIT.** Para Brasil, Indonesia, India, Rusia, México, Turquía, Chipre y Malta, las encuestas de fuerza de trabajo armonizadas por la OIT dan los asalariados, sus horas y su ingreso medio por sección de actividad. Con una sola encuesta por país, desde el primer año disponible a partir de 2014 (India: 2018; Rusia: 2017), se miden la proporción productiva de los asalariados, las horas semanales de las secciones productivas y la parte productiva de la masa salarial, y con ellas se corrigen el número de asalariados productivos, sus horas y la tasa de plusvalor de la extensión agregada. China no publica asalariados por sección: sigue en la extensión agregada.
5. **Desde {{.hm-base1}}, extensión agregada (OIT).** N<sub>t</sub> = N<sub>2014</sub> × asalariados totales<sub>t</sub> / asalariados totales<sub>2014</sub> (estimaciones modeladas de la OIT), manteniendo la proporción productiva de 2014; las horas por ocupado siguen las horas semanales de la OIT. **India:** WIOD cuenta como asalariados a los regulares y a los jornaleros eventuales; la serie de la OIT sólo recoge a los regulares. Para India, N se extiende con la ocupación total de la OIT por la proporción de trabajadores no cuenta propia de las encuestas oficiales (NSS 2011-12 y PLFS 2017-18 a 2023-24).
6. El total mundial es la suma de los países. La fuente de cada país y año está en [mundo_horas_paises.csv](descargas/).
:::

:::como+ ¿Cómo se calcula la masa mundial de plusvalor?
1. **Capital variable (v):** remuneración de los asalariados de las ramas productivas (WIOD: COMP; OCDE: D1).
2. **Plusvalor (pv):** valor agregado bruto de las ramas de mercado (todas menos L68, O84, T, U y, en la segunda variante, educación y salud) − ingreso laboral imputado a los trabajadores por cuenta propia − v. Ese ingreso es LAB − COMP en WIOD y, en la OCDE, no asalariados × remuneración media por asalariado de la misma sección. Los salarios de las ramas de circulación quedan dentro de pv: son deducciones de la masa global de plusvalor.
3. **Tasa de plusvalor:** e = pv/v, en moneda nacional, de modo que no hace falta convertir monedas. Desde 2015, e se encadena al nivel WIOD de 2014 con la variación medida por rama en la OCDE (tabla 6) o, donde no la hay, con la participación del trabajo de la OIT: e<sub>t</sub> = e<sub>2014</sub> × [(1 − LS<sub>t</sub>)/LS<sub>t</sub>] / [(1 − LS<sub>2014</sub>)/LS<sub>2014</sub>]. En Brasil e India (2015–2020), e se mide rama por rama con las cuentas nacionales de la ONU (tabla 2.6: remuneración, ingreso mixto y valor agregado por sección) y se encadena igual. En los demás países medidos por sección con la OIT, 1 + e<sub>t</sub> se multiplica por q<sub>b</sub>/q<sub>t</sub>, donde q es la parte productiva de la masa salarial: si crece la masa salarial productiva, crece v y baja e.
4. **Versión neta:** e<sub>neta</sub> = e − r, con r = consumo de capital fijo de las ramas de mercado / v. En la OCDE se mide por rama (P51C). Donde no hay medición, r = (δ·K/Y de la PWT) × valor agregado de mercado / v, calibrado con el cociente OCDE/PWT de 2014 del propio país o, fuera de la OCDE, con la mediana de esos cocientes ({{hm-kmed}}), porque la depreciación de la PWT incluye viviendas y capital público.
5. **Masa en horas:** plustrabajo = H × e / (1 + e) para cada país, sumado sobre todos. La tasa mundial en horas es Σ plustrabajo / Σ trabajo necesario. Las observaciones con e fuera de (0, 8) se excluyen por anomalías de los datos: {{hm-excl}}.
:::

### Los mayores núcleos de plustrabajo, {{.hm-fin}}

Los países donde se produce más plustrabajo. China e India suman casi dos tercios del total.
{: .llano }

[[tabla t-hm: País | Asalariados productivos (millones) | e bruta | e neta | Plustrabajo bruto (miles de millones de horas) | % del total | Fuente de e]]

### Cuánto pesa cada supuesto (variante central, con China)

Cada fila cambia un solo supuesto respecto de la estimación central. Las filas marcadas como contraste no son lecturas alternativas del criterio adoptado: muestran cuánto pesan en la masa mundial los jornaleros eventuales de India y la agricultura asalariada de India y China.
{: .nota }

Cada fila cambia un solo supuesto y muestra cuánto cambia el total. Sirve para saber qué cifras son firmes y cuáles dependen de decisiones.
{: .llano }

[[tabla t-hms: Año | Caso | Plustrabajo (miles de millones de horas) | Asalariados productivos (millones) | Diferencia | Nota]]

:::como Diagnóstico del empalme OCDE–WIOD en 2014
Si las dos fuentes miden lo mismo, los cocientes de 2014 deberían estar cerca de 1. El nivel lo pone WIOD; la OCDE sólo aporta la variación posterior.

[[tabla t-hmd: País | e WIOD | e OCDE | Asalariados OCDE/WIOD | Horas OCDE/WIOD | r PWT | r OCDE | Último año OCDE]]
:::

Advertencias: las cifras posteriores a 2014 son encadenadas, no niveles medidos de nuevo; en los países de la OCDE la variación sí se mide por rama. China es una estimación. No hay corrección intra-rama en la escala mundial. Por diferencias de definición, la e de EE.UU. aquí no coincide con la de la sección de EE.UU.
{: .nota }
