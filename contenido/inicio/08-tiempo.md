---
seccion: "08 EE.UU. en horas de trabajo"
id: tiempo
menu: EE.UU. en horas de trabajo
---
## Del dinero al tiempo de trabajo: EE.UU.

La masa de plusvalor es el producto de la tasa de plusvalor (pv/v, el grado de explotación) por el número de obreros productivamente explotados. Medida en dinero, la tasa de plusvalor de los obreros productivos expresa la proporción entre plustrabajo y trabajo necesario en su jornada: de cada semana de trabajo, una fracción 1/(1+e) reproduce el valor de su fuerza de trabajo y una fracción e/(1+e) es plustrabajo.

Todo lo de esta sección se refiere **sólo a EE.UU.** y a los obreros de producción y no supervisores de las ramas productivas, desde 1972. La escala mundial en horas está más abajo, en su propia sección.

[[cifra t-n | Obreros productivos explotados en EE.UU., {{.t-fin}} (millones) | {{.t-ini}}: {{t-n0}}]]
[[cifra t-nec | Trabajo necesario en una semana de {{t-sem}} h | {{.t-ini}}: {{t-nec0}}]]
[[cifra t-plus | Plustrabajo semanal por obrero | {{.t-ini}}: {{t-plus0}}]]
[[cifra t-masa | Masa anual de plustrabajo en EE.UU. (miles de millones de horas) | {{.t-ini}}: {{t-masa0}}]]

### EE.UU.: la semana del obrero productivo, dividida en trabajo necesario y plustrabajo (horas)

Una semana de trabajo de un obrero productivo típico de EE.UU., partida en dos. La parte de abajo son las horas en que produce el equivalente de su salario (trabajo necesario); la de arriba, las horas en que trabaja para el capital sin recibir nada a cambio (plustrabajo). Con los años, la parte necesaria se achica porque cada hora produce más, pero cada vez se achica menos: entre 1972 y 1982 se redujo 1,6 horas; entre 2007 y 2025, 0,3. Y el plustrabajo por obrero casi no cambia, porque la semana tiene un largo dado y el trabajo necesario nunca puede llegar a cero.
{: .llano }

Cada año, las horas semanales promedio de un obrero productivo se reparten según la tasa de plusvalor del mismo año: horas necesarias = jornada / (1 + e); plustrabajo = jornada × e / (1 + e). Fuente de las horas: BLS, encuesta de establecimientos (CES).
{: .nota }

[[leyenda l-sem]]
[[grafico c-sem]]

### EE.UU.: masa anual de plustrabajo (miles de millones de horas)

Suma las horas de plustrabajo de todos los obreros productivos de EE.UU. en un año. Se multiplica por más de dos desde 1972, y casi todo ese crecimiento viene de que hay más obreros, no de que cada uno trabaje más horas para el capital. Las caídas coinciden con las recesiones, cuando se despide a millones.
{: .llano }

Horas trabajadas en el año por todos los obreros productivos de EE.UU. × e / (1 + e). Es la suma de las horas impagas, no un promedio.
{: .nota }

[[grafico c-hplus]]

:::como+ ¿Cómo se obtienen estos datos?
1. **Obreros productivos (N).** Suma del empleo de los trabajadores de producción y no supervisores (BLS, encuesta CES, series 06) de los supersectores productivos: minería y explotación forestal, construcción, manufactura, transporte y almacenamiento, servicios públicos, información, servicios profesionales y empresariales, educación y salud privadas, ocio y hospitalidad, otros servicios. Quedan fuera el comercio, las finanzas, el gobierno, los supervisores y la agricultura (la CES no la cubre). Promedio anual, en millones.
2. **Horas (H).** Para cada supersector, empleo × horas semanales promedio pagadas (series 07; en manufactura, AWHMAN) × 52.
3. **Tasa de plusvalor (e).** S/V de la sección anterior, en su variante intra-rama: S es el plusvalor ampliado neto del sector empresarial y V la remuneración de esos mismos obreros (empleo × salario por hora × horas × 52, escalada para incluir prestaciones).
4. **Jornada.** Horas semanales por obrero = H / N / 52; trabajo necesario = jornada / (1 + e); plustrabajo = jornada × e / (1 + e). Esto da el primer gráfico.
5. **Masa de plustrabajo.** H × e / (1 + e) = N × horas por obrero × e / (1 + e), en miles de millones de horas al año. Esto da el segundo gráfico.
6. **Descomposición.** Entre el primer y el último año, cada factor aporta ln(factor<sub>fin</sub>/factor<sub>inicio</sub>) / ln(masa<sub>fin</sub>/masa<sub>inicio</sub>); los tres aportes suman 100 %.

El supuesto clave de la lectura macromonetaria (Moseley) es que v es el salario efectivamente pagado, así que la proporción monetaria pv/v es también la proporción entre plustrabajo y trabajo necesario.
:::

### ¿De dónde viene el crecimiento de la masa de plustrabajo?

{{t-desc-intro}}

La tabla separa ese crecimiento en tres causas: más obreros, jornadas más largas o más cortas, y una proporción mayor de plustrabajo dentro de la jornada.
{: .llano }

[[tabla t-desc: Factor | Se multiplica por | Aporte al crecimiento (en logaritmos)]]

### Expresión monetaria del tiempo de trabajo en EE.UU.

Cuántos dólares de valor nuevo representa, en promedio, una hora de trabajo productivo. Es el puente que permite leer las cifras en dinero como cifras en tiempo de trabajo. En dólares corrientes sube con la inflación; en dólares de 2017 sube mucho menos.
{: .llano }

Valor nuevo (v + pv) por hora de trabajo productivo: cuántos dólares representa una hora de trabajo social productivo. Es la relación que permite pasar del dinero al tiempo y del tiempo al dinero.
{: .nota }

[[leyenda l-melt]]
[[grafico c-melt]]

:::como ¿Cómo se calcula este gráfico?
Expresión monetaria del tiempo de trabajo = (V + S) / H: el valor nuevo creado por los obreros productivos (intra-rama), en dólares, dividido por sus horas. La serie en dólares de 2017 divide por el deflactor del PIB.
:::
