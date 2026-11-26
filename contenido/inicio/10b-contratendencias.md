---
seccion: 10b Contratendencias
menu: Contratendencias
id: contratendencias
oculta: true
---
## El campo de las contratendencias

Marx (2021, pp. 297–307) expone seis causas que contrarrestan la caída tendencial de la tasa de ganancia: la elevación del grado de explotación, la reducción del salario por debajo de su valor, el abaratamiento de los elementos del capital constante, la sobrepoblación relativa, el comercio exterior y el aumento del capital accionario. No son fuerzas externas que corrijan la tendencia desde fuera: las producen las mismas causas que producen la caída. Esta sección reúne, para cada una, indicadores observables, y empieza por la pregunta central: en cada estadio histórico del capitalismo desarrollado, ¿qué sostuvo o hundió la tasa de ganancia?

### Qué movió la tasa en cada fase

La tasa de ganancia puede escribirse como r = e · v/K: sube si sube la tasa de plusvalor e y baja si sube la composición K/V. Las fases no se eligen de antemano: sus límites son los años de quiebre más frecuentes en el multiverso ({{ct-cortes}}). Cada barra mide, en logaritmos, cuánto aportó cada factor al cambio de la tasa en esa fase.

La tasa de ganancia sube si el capital obtiene más plusvalor por cada dólar de salario (tasa de plusvalor) y baja si necesita más capital por cada dólar de salario (composición). En cada periodo, las barras muestran cuánto empujó cada fuerza. Si la barra de la tasa de plusvalor es más alta que la caída por la composición, la tasa de ganancia sube; si no, baja. Así se ve qué contratendencia sostuvo la ganancia en cada etapa y cuándo dejó de hacerlo.
{: .llano }

[[leyenda l-ct-fases]]
[[grafico c-ct-fases]]

Fuentes: BEA: cuentas nacionales (NIPA), PIB por industria y activos fijos; BLS: encuesta de establecimientos (CES, vía FRED). Descomposición propia de la tasa de ganancia por fases (quiebres endógenos).
{: .fuente }

Criterio por ramas, desde 1948. Una barra de la composición por debajo de cero significa que el capital por unidad de capital variable creció y presionó la tasa hacia abajo.
{: .nota }

Desde 1972 la composición en valor puede separarse en dos partes: la composición técnica (capital a precios constantes por hora de trabajo productivo) y el precio relativo del capital respecto del salario por hora. Que la primera empuje hacia abajo mientras la segunda empuja hacia arriba es la forma observable del abaratamiento del capital constante.
{: .nota }

El mismo cálculo, con la composición separada en dos partes: cuánto capital físico hay por hora de trabajo (crece siempre) y cuánto cuesta ese capital comparado con el salario (baja: las máquinas se abaratan respecto del trabajo).
{: .llano }

[[leyenda l-ct-fases-i]]
[[grafico c-ct-fases-i]]

Fuentes: BEA: cuentas nacionales (NIPA), PIB por industria y activos fijos; BLS: encuesta de establecimientos (CES, vía FRED); índices de precios de la inversión y del capital fijo (BEA). Cálculo propio.
{: .fuente }

[[tabla t-ct-fases: Variante | Fase | Cambio de la tasa | Aporte de e | Aporte de K/V | Composición técnica | Precio relativo]]

### ¿Resiste la descomposición a todas las decisiones teóricas?

La misma descomposición, repetida para las 16 especificaciones de cada criterio de trabajo productivo (costo corriente o histórico, neta o bruta, con o sin propiedad intelectual, todo el capital o sólo el de las ramas productivas). Cada celda da la mediana y, entre paréntesis, el rango de los percentiles 10 a 90. La última columna indica en qué porcentaje de las especificaciones en que la composición sube, la elevación de la tasa de plusvalor alcanza a compensarla.
{: .nota }

La tabla repite el cálculo con todas las mediciones del multiverso. Si el resultado de una fase se mantiene en casi todas, no depende de la teoría.
{: .llano }

[[tabla t-ct-fm: Criterio | Fase | Aporte de e | Aporte de K/V | Especificaciones en que la tasa sube | e compensa la composición]]

:::como ¿Cómo se calcula esta descomposición?
Para cada fase entre los años a<sub>0</sub> y a<sub>1</sub>: Δln r = Δln e − Δln(K/V), con e = S/V y K/V tomados de la sección «La ley bifacética» (plusvalor ampliado neto del sector empresarial; K a costo corriente; V por ramas desde 1948 o intra-rama desde 1972). En la variante intra-rama, K/V = (K<sub>real</sub>/H) · (P<sub>K</sub>/w): K<sub>real</sub> es K deflactado por el precio implícito del capital fijo privado no residencial (stock a costo corriente sobre índice de cantidad del BEA, 2017 = 1); H son las horas de los obreros productivos (BLS) y w = V/H. Los años de corte son los cinco años de quiebre más frecuentes en el multiverso principal (configuración base: tramo mínimo de 8 años, BIC), separados entre sí por al menos seis años. Las descargas incluyen la tabla completa (contratendencias_fases.csv).
:::

### 1. Elevación del grado de explotación

La tasa de plusvalor es el indicador directo (véase la sección «La ley bifacética»). Aquí se compara el producto por hora del sector empresarial no agrícola con la remuneración real por hora: la distancia entre ambas curvas es la parte de la productividad que no vuelve a los trabajadores.

Si los trabajadores producen más por hora pero su salario real crece menos, la diferencia queda para el capital. La distancia entre las dos líneas es esa diferencia, acumulada desde 1972.
{: .llano }

[[leyenda l-ct-a]]
[[grafico c-ct-a]]

Fuentes: BLS: productividad y costos, sector empresarial no agrícola (vía FRED: OPHNFB, COMPRNFB).
{: .fuente }

La extensión del tiempo de trabajo no aparece en las horas pagadas por establecimiento, que bajan. Dos indicios de su desplazamiento fuera de un solo empleo: la proporción de ocupados con más de un empleo y la de quienes trabajan a tiempo parcial sin quererlo. Ninguno mide la intensidad del trabajo, que sigue sin indicador.
{: .nota }

Dos señales de que el tiempo de trabajo se estira por fuera de las horas pagadas en un empleo: la gente que necesita dos o más empleos y la que trabaja menos horas de las que quiere.
{: .llano }

[[leyenda l-ct-a2]]
[[grafico c-ct-a2 corto]]

Fuente: BLS: encuesta de hogares (Current Population Survey, vía FRED: LNS12026619, LNS12032194, CE16OV). Cálculo propio.
{: .fuente }

### 2. Reducción del salario por debajo de su valor

El valor de la fuerza de trabajo no se observa directamente; lo que sí se observa es el salario real de los obreros de producción y no supervisores. Un salario real que durante décadas queda por debajo de su nivel de 1972, mientras la productividad se multiplica, indica una compresión del salario que la sola elevación de la productividad no explica.

Lo que puede comprar con el salario de una hora un obrero de producción, descontada la inflación.
{: .llano }

[[leyenda l-ct-b]]
[[grafico c-ct-b]]

Fuentes: BLS: salario medio por hora de los obreros de producción y no supervisores (CES, vía FRED: AHETPI) e índice de precios al consumidor (CPIAUCSL). Cálculo propio.
{: .fuente }

### 3. Abaratamiento de los elementos del capital constante

Tres índices sobre las máquinas, edificios y equipos. La composición técnica dice cuánto capital físico hay por hora de trabajo: crece sin parar. Los otros dos dicen cuánto cuesta ese capital comparado con el salario y con el consumo: bajan. El capital necesita cada vez más medios de producción por obrero, pero cada uno es más barato, y eso frena la caída de la tasa.
{: .llano }

[[leyenda l-ct-c]]
[[grafico c-ct-c corto]]

Fuentes: BEA: activos fijos (stock neto a costo corriente y cantidades encadenadas), índices de precios de la inversión y del consumo (NIPA); BLS (CES, vía FRED): horas de los obreros productivos. Cálculo propio.
{: .fuente }

Índices, 1972 = 100. La composición técnica crece mucho más que la composición en valor porque cada unidad de capital se abarata respecto del trabajo.
{: .nota }

### 4. Sobrepoblación relativa

Cuánta gente está disponible para que el capital la emplee: desempleados y subempleados en EE.UU.; en el mundo, desempleados y trabajadores por cuenta propia o familiares. El empleo vulnerable mundial baja porque cientos de millones de personas pasan a trabajar como asalariados.
{: .llano }

[[leyenda l-ct-d]]
[[grafico c-ct-d]]

Fuentes: BLS: Current Population Survey (vía FRED: LNS12300060, U6RATE); Banco Mundial, Indicadores del Desarrollo Mundial con estimaciones modelizadas de la OIT (SL.EMP.VULN.ZS, SL.UEM.TOTL.ZS).
{: .fuente }

La sobrepoblación relativa no es sólo desempleo: incluye a quienes trabajan por cuenta propia o en el trabajo familiar, disponibles para ser absorbidos por el capital. En la escala mundial, su reabsorción es la principal fuente del crecimiento de la masa de plusvalor (véase la masa mundial en horas).
{: .nota }

### 5. Comercio exterior

Qué parte de las ganancias de las corporaciones de EE.UU. proviene del extranjero, y cuánto pesa el comercio en la economía mundial.
{: .llano }

[[leyenda l-ct-e]]
[[grafico c-ct-e]]

Fuentes: BEA: NIPA, ganancias recibidas del resto del mundo y ganancias corporativas (B933RC, A051RC); Banco Mundial: comercio en % del PIB mundial (NE.TRD.GNFS.ZS). Cálculo propio.
{: .fuente }

**Transferencia de tiempo de trabajo por comercio exterior.** En el mercado mundial, los países de productividad más alta reciben más trabajo a cambio de menos. El gráfico estima cuántas horas de trabajo ajeno se apropia cada país o grupo por año: las horas incorporadas en lo que importa menos las incorporadas en lo que exporta, en miles de millones de horas. Positivo significa apropiación; negativo, cesión.
{: .nota }

[[leyenda l-ct-e2]]
[[grafico c-ct-e2]]

Fuente: Penn World Table 11.0 (ocupados y horas anuales) y Banco Mundial (PIB y exportaciones e importaciones en dólares corrientes). Cálculo propio, aproximado.
{: .fuente }

:::como ¿Cómo se calcula la transferencia de horas?
Para cada país, h = horas trabajadas en el año (ocupados × horas anuales por ocupado, Penn World Table 11.0) / PIB en dólares corrientes (Banco Mundial). El contenido medio en horas de un dólar de exportaciones mundiales es h<sub>X</sub> = Σ exportaciones × h / Σ exportaciones. La transferencia neta de un país es importaciones × h<sub>X</sub> − exportaciones × h. Se usan los países con datos de horas (unos 120, desde 2005); los grupos de ingreso son los del Banco Mundial.

Supuestos: lo que un país exporta incorpora las horas por dólar promedio de su economía, y lo que importa, el contenido medio de las exportaciones mundiales; no se rastrean los insumos intermedios, para lo que haría falta una matriz insumo-producto mundial; se cuentan todas las horas trabajadas, no sólo las productivas. La transferencia no crea plusvalor: lo redistribuye entre capitales y formaciones nacionales.
:::

### 6. Capital accionario y capital que devenga interés

Qué parte de la ganancia se va a las finanzas: las ganancias del sector financiero, los intereses y los dividendos que pagan las empresas no financieras, y cuántas acciones emiten o recompran.
{: .llano }

[[leyenda l-ct-f]]
[[grafico c-ct-f]]

Fuentes: BEA: NIPA (A587RC, A445RC, B471RC, W326RC, B467RC, A466RC, A455RC); Reserva Federal: cuentas financieras Z.1 (vía FRED: BOGZ1FU103164103A). Cálculo propio.
{: .fuente }

El capital ficticio son títulos sobre plustrabajo futuro. El valor de mercado de las acciones de las corporaciones no financieras crece mucho más que su deuda y que el producto: su validación exige una masa de plusvalor que todavía no se ha producido.
{: .nota }

El valor en bolsa de las corporaciones no financieras de EE.UU. comparado con el producto del país, y su deuda. El valor en bolsa pasa de un tercio a más del doble del producto: son títulos que sólo pueden pagarse con plustrabajo que todavía no se ha producido.
{: .llano }

[[leyenda l-ct-f2]]
[[grafico c-ct-f2 corto]]

Fuentes: Reserva Federal: cuentas financieras Z.1 (vía FRED: NCBEILQ027S, BCNSDODNS); BEA: PIB (GDP). Cálculo propio.
{: .fuente }

La emisión neta de acciones negativa significa que las corporaciones no financieras recompran más acciones de las que emiten: transfieren ganancia a los accionistas en lugar de acumularla.
{: .nota }

:::como ¿De dónde salen estos indicadores?
- **Explotación:** producto por hora (OPHNFB) y remuneración real por hora (COMPRNFB) del sector empresarial no agrícola, BLS vía FRED, reindexados a 1972 = 100.
- **Salario:** ingreso medio por hora de los trabajadores de producción y no supervisores (AHETPI, BLS) dividido por el índice de precios al consumidor (CPIAUCSL), en dólares de 2017. Servicio de la deuda de los hogares sobre el ingreso disponible (TDSP, Reserva Federal) en las descargas.
- **Capital constante:** precio implícito de la inversión no residencial (NIPA A008RD) sobre el índice de precios del consumo personal (DPCERG); composición técnica y precio relativo como en la descomposición por fases.
- **Sobrepoblación relativa:** tasa de empleo de 25 a 54 años (LNS12300060) y subutilización laboral U-6 (U6RATE), BLS; empleo vulnerable y desempleo mundiales, estimaciones modeladas de la OIT publicadas por el Banco Mundial (SL.EMP.VULN.ZS, SL.UEM.TOTL.ZS).
- **Comercio exterior:** ganancias corporativas recibidas del resto del mundo (NIPA B933RC) sobre las ganancias corporativas totales (A051RC), desde 1998; comercio mundial sobre PIB (Banco Mundial, NE.TRD.GNFS.ZS).
- **Extensión del tiempo de trabajo:** ocupados con más de un empleo (LNS12026619, desde 1994) y a tiempo parcial por razones económicas (LNS12032194), sobre el total de ocupados (CE16OV), BLS.
- **Transferencia por comercio exterior:** véase el desplegable de la transferencia de horas.
- **Capital ficticio:** valor de mercado de las acciones emitidas por las corporaciones no financieras (Z.1, NCBEILQ027S) y su deuda en títulos y préstamos (BCNSDODNS), sobre el PIB (GDP).
- **Capital financiero:** ganancias de las corporaciones financieras sobre las ganancias domésticas (A587RC / A445RC), desde 1998; intereses netos de las corporaciones no financieras sobre su excedente neto (B471RC / W326RC); dividendos sobre ganancia después de impuestos (B467RC / A466RC); emisión neta de acciones de las corporaciones no financieras (Z.1, FU103164103) sobre su valor agregado bruto (A455RC).

Ninguno de estos indicadores mide por sí solo una contratendencia: son manifestaciones observables que deben leerse junto con la tasa y la masa de plusvalor. Todos están en las descargas (contratendencias_indicadores.csv).
:::
