---
seccion: "02b Explorador de especificaciones"
id: explorador
menu: Explorador de especificaciones
---
## Explorador: una especificación a la vez

Elija una opción en cada bifurcación y el gráfico dibuja la tasa de ganancia que resulta de esa combinación de decisiones, sobre el abanico de todo el multiverso.

El abanico de arriba resume cientos de mediciones; aquí se puede mirar cada una por separado. Cada menú es una decisión teórica: qué sector se mide, qué se cuenta como ganancia o como plusvalor, cómo se valora el capital, si se incluye la propiedad intelectual, etc. Al cambiar una opción, el explorador busca la especificación publicada que la usa y que conserva el mayor número posible de las demás decisiones; si una decisión no tiene sentido para esa familia de especificaciones (por ejemplo, el criterio de trabajo productivo en las series corporativas), su menú queda en «no aplica». La línea de color es la especificación elegida; las líneas punteadas, los años en que esa especificación muestra un quiebre de tendencia. Debajo se informan su nivel en tres años y su identificador. Lo que interesa comparar es la forma de la curva con la del abanico: dónde la decisión teórica cambia el movimiento y dónde sólo cambia el nivel. La misma información está en el [mapa](mapa.html) (al pinchar una hoja o una bifurcación) y, completa, en la [tabla de las especificaciones](descargas/eeuu_multiverso_tabla.csv).
{: .llano }

[[explorador]]

Fuentes: BEA: cuentas nacionales (NIPA), PIB por industria y activos fijos; BLS: encuesta de establecimientos (CES, vía FRED); Reserva Federal: utilización de capacidad (G.17) y existencias (Z.1, vía FRED). Cálculo propio de 288 especificaciones principales (1948–) y 64 de la familia intra-rama (1972–).
{: .fuente }

:::como ¿Cómo se calcula este gráfico?
Cada especificación es la tasa anual r = numerador / denominador definida por sus decisiones (véase la [metodología, §5](metodologia.html#multiverso)). La serie elegida se divide por su propio promedio del periodo y se multiplica por 100, igual que en el abanico; las especificaciones intra-rama comienzan en 1972 y su promedio se toma desde ese año. El abanico de fondo (percentiles 10–90 y 25–75 y mediana) es el de las 288 especificaciones principales. Los quiebres son los que el procedimiento de Bai y Perron detecta en esa especificación (metodología, §7). Los niveles se dan en porcentaje, sin normalizar.

La tabla descargable tiene una fila por especificación, con sus decisiones en palabras, la tasa (%) en 1948, 1982 y el último año, y los años de quiebre. Este modo de exponer todas las combinaciones razonables de decisiones, en lugar de una sola estimación, es lo que Steegen, Tuerlinckx, Gelman y Vanpaemel (2016) llaman análisis de multiverso.
:::
