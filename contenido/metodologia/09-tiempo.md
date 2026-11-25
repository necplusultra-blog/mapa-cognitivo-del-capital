---
seccion: "09 Del dinero al tiempo de trabajo"
id: tiempo
menu: Del dinero al tiempo de trabajo
---
## Del dinero al tiempo de trabajo

Se usa la variante c: obreros de producción y no supervisores de las ramas productivas, desde 1972.

<div class="f">N = Σ empleo productivo · H = Σ empleo × horas semanales × 52</div>

En la lectura macromonetaria, v es el salario efectivamente pagado. La tasa e = pv/v medida en dinero, neta de depreciación (véase §4), expresa entonces la proporción entre plustrabajo y trabajo necesario en la jornada de esos obreros:

<div class="f">trabajo necesario = jornada / (1 + e) · plustrabajo = jornada × e / (1 + e)</div>

La jornada que se divide es una jornada de tiempo completo de 40 horas. La semana media pagada de la encuesta de establecimientos (H / N / 52) no es una jornada: promedia tiempo completo y parcial, y baja sobre todo por la composición del empleo (41 horas en manufactura, 24 en ocio y hospitalidad). Además son horas pagadas, no trabajadas. La masa de plustrabajo usa las horas totales H, que no dependen de esa distinción.

<div class="f">masa de plustrabajo (horas) = H × e / (1 + e) = N × horas por obrero × e / (1 + e)</div>

La descomposición del crecimiento de la masa entre el primer y el último año usa logaritmos: cada factor aporta ln(factor<sub>fin</sub>/factor<sub>inicio</sub>) / ln(masa<sub>fin</sub>/masa<sub>inicio</sub>). Los tres aportes suman 100 %.

La **expresión monetaria del tiempo de trabajo** es (v + pv) / H: el valor nuevo, en dólares, que representa una hora de trabajo productivo. Se presenta en dólares corrientes y deflactada por el deflactor del PIB.

Supuestos: el valor de la fuerza de trabajo se aproxima por el salario pagado; las horas son las horas pagadas que informa la CES; los supervisores de las ramas productivas no forman parte de v, y sus salarios quedan dentro de pv.

### Fuerzas productivas y tiempo disponible

El módulo `fuerzas.py` usa las mismas series para registrar cuánto tiempo libera el desarrollo de la fuerza productiva y en qué lo convierte el capital.

- **Tiempo necesario al nivel de vida de 1972** (EE.UU.): 40 × w̃<sub>1972</sub> / μ̃<sub>t</sub>, donde w̃ es la remuneración real por hora de los obreros productivos (V / H) y μ̃ el valor nuevo real por hora productiva ((V + S) / H), ambos con el deflactor del PIB. Son las horas semanales que bastarían, con la productividad de cada año, para producir el salario real de 1972.
- **Destino del tiempo liberado** respecto de 1972, en una jornada de 40 horas: más consumo obrero = trabajo necesario efectivo − tiempo al nivel de 1972; más plustrabajo = plustrabajo<sub>t</sub> − plustrabajo<sub>1972</sub>; reducción de la jornada de referencia = 0. Las tres partes suman exactamente el tiempo liberado.
- **Mundo:** horas anuales de trabajo productivo, de plustrabajo y necesario (la diferencia) de los países medidos rama por rama, por habitante de esos países (población de la Penn World Table, extrapolada después de su último año con el crecimiento medio de los tres años anteriores), en minutos por día.

**Versión 2.** (a) El tiempo al nivel de vida de 1972 se calcula también con el deflactor del gasto de consumo personal (PCE): 40 × w<sub>1972</sub> × (PCE<sub>t</sub>/PCE<sub>1972</sub>) / μ<sub>t</sub>. Da 6,9 horas en 2025, frente a 6,8 con el deflactor del PIB: el reparto del tiempo liberado apenas cambia (60 % a plustrabajo, 40 % a consumo). (b) Además de la jornada legal de 40 horas, se usa la semana habitual de los asalariados a tiempo completo (OCDE, a partir de la CPS; desde 1979): 41,2 horas en 1979 y 41,0 en 2025. Con ella, el plustrabajo semanal pasa de 27,8 a 31,1 horas. (c) En el mundo, una variante suma las horas de los asalariados de la educación y la salud públicas y sin fines de lucro, trabajo improductivo para el capital pero socialmente necesario: 9 minutos diarios por habitante en 2025, que llevan el total de 74 a 83 minutos.

Supuestos y límites: el deflactor del PIB no es exactamente el de la canasta obrera (el PCE se usa como contraste; tampoco es la canasta obrera, sino el consumo de todos los hogares); el trabajo productivo para el capital no es todo el trabajo socialmente necesario (la variante mundial agrega sólo la educación y la salud públicas; quedan fuera la administración, los cuidados, el trabajo doméstico y el campesino); las cifras no estiman la jornada de una sociedad emancipada, en la que el trabajo necesario incluiría los fondos comunes de reposición, ampliación y servicios. Resultados: `fuerzas_eeuu.csv` y `fuerzas_mundo.csv`.
