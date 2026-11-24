---
id: contratendencias
menu: Contratendencias
oculta: si
---
## El campo de las contratendencias

Marx expone seis causas que contrarrestan la caída tendencial de la tasa de ganancia: la elevación del grado de explotación, la reducción del salario por debajo de su valor, el abaratamiento de los elementos del capital constante, la sobrepoblación relativa, el comercio exterior y el aumento del capital accionario. No son fuerzas externas que corrijan la tendencia desde fuera: las producen las mismas causas que producen la caída. Esta sección reúne, para cada una, indicadores observables, y empieza por la pregunta central: en cada fase, ¿qué sostuvo o hundió la tasa de ganancia?

### Qué movió la tasa en cada fase

La tasa de ganancia puede escribirse como r = e · v/K: sube si sube la tasa de plusvalor e y baja si sube la composición K/V. Las fases no se eligen de antemano: sus límites son los años de quiebre más frecuentes en el multiverso ({{ct-cortes}}). Cada barra mide, en logaritmos, cuánto aportó cada factor al cambio de la tasa en esa fase.

[[leyenda l-ct-fases]]
[[grafico c-ct-fases]]

Criterio por ramas, desde 1948. Una barra de la composición por debajo de cero significa que el capital por unidad de capital variable creció y presionó la tasa hacia abajo.
{: .nota }

Desde 1972 la composición en valor puede separarse en dos partes: la composición técnica (capital a precios constantes por hora de trabajo productivo) y el precio relativo del capital respecto del salario por hora. Que la primera empuje hacia abajo mientras la segunda empuja hacia arriba es la forma observable del abaratamiento del capital constante.
{: .nota }

[[leyenda l-ct-fases-i]]
[[grafico c-ct-fases-i]]

[[tabla t-ct-fases: Variante | Fase | Cambio de la tasa | Aporte de e | Aporte de K/V | Composición técnica | Precio relativo]]

:::como ¿Cómo se calcula esta descomposición?
Para cada fase entre los años a<sub>0</sub> y a<sub>1</sub>: Δln r = Δln e − Δln(K/V), con e = S/V y K/V tomados de la sección «La ley bifacética» (plusvalor ampliado neto del sector empresarial; K a costo corriente; V por ramas desde 1948 o intra-rama desde 1972). En la variante intra-rama, K/V = (K<sub>real</sub>/H) · (P<sub>K</sub>/w): K<sub>real</sub> es K deflactado por el precio implícito del capital fijo privado no residencial (stock a costo corriente sobre índice de cantidad del BEA, 2017 = 1); H son las horas de los obreros productivos (BLS) y w = V/H. Los años de corte son los cinco años de quiebre más frecuentes en el multiverso principal (configuración base: tramo mínimo de 8 años, BIC), separados entre sí por al menos seis años. Las descargas incluyen la tabla completa (contratendencias_fases.csv).
:::

### 1. Elevación del grado de explotación

La tasa de plusvalor es el indicador directo (véase la sección «La ley bifacética»). Aquí se compara el producto por hora del sector empresarial no agrícola con la remuneración real por hora: la distancia entre ambas curvas es la parte de la productividad que no vuelve a los trabajadores.

[[leyenda l-ct-a]]
[[grafico c-ct-a]]

### 2. Reducción del salario por debajo de su valor

El valor de la fuerza de trabajo no se observa directamente; lo que sí se observa es el salario real de los obreros de producción y no supervisores. Un salario real que durante décadas queda por debajo de su nivel de 1972, mientras la productividad se multiplica, indica una compresión del salario que la sola elevación de la productividad no explica.

[[leyenda l-ct-b]]
[[grafico c-ct-b]]

### 3. Abaratamiento de los elementos del capital constante

[[leyenda l-ct-c]]
[[grafico c-ct-c corto]]

Índices, 1972 = 100. La composición técnica crece mucho más que la composición en valor porque cada unidad de capital se abarata respecto del trabajo.
{: .nota }

### 4. Sobrepoblación relativa

[[leyenda l-ct-d]]
[[grafico c-ct-d]]

La sobrepoblación relativa no es sólo desempleo: incluye a quienes trabajan por cuenta propia o en el trabajo familiar, disponibles para ser absorbidos por el capital. En la escala mundial, su reabsorción es la principal fuente del crecimiento de la masa de plusvalor (véase la masa mundial en horas).
{: .nota }

### 5. Comercio exterior

[[leyenda l-ct-e]]
[[grafico c-ct-e]]

### 6. Capital accionario y capital que devenga interés

[[leyenda l-ct-f]]
[[grafico c-ct-f]]

La emisión neta de acciones negativa significa que las corporaciones no financieras recompran más acciones de las que emiten: transfieren ganancia a los accionistas en lugar de acumularla.
{: .nota }

:::como ¿De dónde salen estos indicadores?
- **Explotación:** producto por hora (OPHNFB) y remuneración real por hora (COMPRNFB) del sector empresarial no agrícola, BLS vía FRED, reindexados a 1972 = 100.
- **Salario:** ingreso medio por hora de los trabajadores de producción y no supervisores (AHETPI, BLS) dividido por el índice de precios al consumidor (CPIAUCSL), en dólares de 2017. Servicio de la deuda de los hogares sobre el ingreso disponible (TDSP, Reserva Federal) en las descargas.
- **Capital constante:** precio implícito de la inversión no residencial (NIPA A008RD) sobre el índice de precios del consumo personal (DPCERG); composición técnica y precio relativo como en la descomposición por fases.
- **Sobrepoblación relativa:** tasa de empleo de 25 a 54 años (LNS12300060) y subutilización laboral U-6 (U6RATE), BLS; empleo vulnerable y desempleo mundiales, estimaciones modeladas de la OIT publicadas por el Banco Mundial (SL.EMP.VULN.ZS, SL.UEM.TOTL.ZS).
- **Comercio exterior:** ganancias corporativas recibidas del resto del mundo (NIPA B933RC) sobre las ganancias corporativas totales (A051RC), desde 1998; comercio mundial sobre PIB (Banco Mundial, NE.TRD.GNFS.ZS).
- **Capital financiero:** ganancias de las corporaciones financieras sobre las ganancias domésticas (A587RC / A445RC), desde 1998; intereses netos de las corporaciones no financieras sobre su excedente neto (B471RC / W326RC); dividendos sobre ganancia después de impuestos (B467RC / A466RC); emisión neta de acciones de las corporaciones no financieras (Z.1, FU103164103) sobre su valor agregado bruto (A455RC).

Ninguno de estos indicadores mide por sí solo una contratendencia: son manifestaciones observables que deben leerse junto con la tasa y la masa de plusvalor. Todos están en las descargas (contratendencias_indicadores.csv).
:::
