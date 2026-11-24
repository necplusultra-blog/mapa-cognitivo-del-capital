---
seccion: "12c La transformación"
id: transformacion
menu: La transformación
---
## La transformación: valores y precios

**Nivel agregado.** El sismógrafo trabaja en el nivel macromonetario (Moseley; cercano a la «nueva interpretación» de Foley y Duménil): el plusvalor total es, por construcción, la suma de ganancias, intereses, rentas, impuestos a la producción y sueldos improductivos, y la expresión monetaria del tiempo de trabajo traduce dinero a horas. En ese nivel, el problema de la transformación no altera la masa ni la tasa de plusvalor. Lo que sí altera es la distribución del plusvalor entre ramas y países, que es lo que mide esta fase.

**Fuente.** Tablas insumo-producto nacionales de WIOD (versión de noviembre de 2016), 43 países, 56 ramas, 2000–2014, en millones de dólares, con la matriz de insumos nacionales y la de insumos importados; horas y ocupados de las cuentas socioeconómicas de WIOD.

**Valores.** Para las ramas productivas p:

<div class="f">λ<sub>p</sub> = (l<sub>p</sub> + λ̄<sub>p</sub> M<sub>pp</sub>) (I − A<sub>pp</sub>)<sup>−1</sup></div>

l<sub>j</sub> = horas trabajadas por todos los ocupados de la rama / producción bruta. Las horas de los no asalariados se aproximan con las horas por asalariado de la misma rama (H\_EMPE / EMPE × EMP); en China, 46 h × 50 semanas por ocupado. Los trabajadores por cuenta propia cuentan para el valor (producen mercancías) aunque no para el plusvalor. λ̄<sub>j</sub> = Σ<sub>c</sub> λ<sub>cj</sub> X<sub>cj</sub> / Σ<sub>c</sub> X<sub>cj</sub>: contenido medio en horas de un dólar exportado del producto j. Se resuelve por iteración hasta que λ̄ no cambia.

Las ramas de circulación (G, K, M69–M70, M73) y las que están fuera de la producción capitalista (L, O, P, Q, T, U) no producen valor, y sus productos usados como insumos no transfieren valor: son gastos pagados con plusvalor (Shaikh y Tonak). Educación y salud quedan enteras fuera porque las tablas no separan su parte capitalista.

**Precios y valores.** μ = Σ<sub>p</sub> x<sub>j</sub> / Σ<sub>p</sub> λ<sub>j</sub> x<sub>j</sub> (dólares por hora); precio-valor<sub>j</sub> = μ λ<sub>j</sub>; desviación media = Σ x<sub>j</sub> |μλ<sub>j</sub> − 1| / Σ x<sub>j</sub>. La correlación de rangos de Spearman entre precio/valor y la composición K/v (stock de capital nominal sobre ingreso del trabajo de la rama, LAB) contrasta la expectativa de Marx: los precios de producción superan a los valores donde la composición es alta.

**Comercio exterior.** Horas entregadas = Σ λ<sub>j</sub> X<sub>j</sub>; horas recibidas = Σ λ̄<sub>j</sub> M<sub>j</sub> × (X / M), con X y M las exportaciones e importaciones de productos de ramas productivas (las importaciones incluyen insumos y demanda final).

**Ponderación del mercado mundial.** w<sub>c</sub> = μ<sub>c</sub> / μ̄, con μ<sub>c</sub> = PIB en dólares corrientes / horas trabajadas (Banco Mundial, PWT) y μ̄ el promedio ponderado por las horas productivas de los 42 países de la masa mundial. Masa ponderada = Σ plustrabajo<sub>c</sub> w<sub>c</sub>. Se usan tipos de cambio de mercado, no paridades de poder adquisitivo, porque se trata de la valoración en el mercado mundial.

**Interpretación de la transformación (F4 v2; decisión de Pablo, 24 nov. 2026).** La interpretación central es la de Moseley: el capital constante y el variable se toman como las magnitudes dinerarias efectivamente adelantadas, idénticas en la determinación de los valores y de los precios de producción, de modo que la transformación sólo redistribuye el plusvalor total entre ramas. Valor de la rama j: W<sub>j</sub> = c<sub>j</sub> + a<sub>j</sub> + v<sub>j</sub>(1 + e); precio de producción: PP<sub>j</sub> = c<sub>j</sub> + a<sub>j</sub> + v<sub>j</sub> + r(K<sub>j</sub> + v<sub>j</sub>), con e = S/V y r = S/(K + V) del país, y a<sub>j</sub> el ingreso laboral de los no asalariados. Como contraste se calcula la variante temporal de sistema único (TSSI; Kliman y Freeman): los insumos se valúan a los precios con que entraron en la producción (índice de precios de los insumos de la rama del año anterior) y el capital adelantado es el stock al cierre del año anterior; el valor nuevo es la producción menos esos insumos. Resultados: `transformacion_moseley_tssi.csv` (por país y año) y `transformacion_moseley_ramas.csv` (por rama).

**Decisiones pendientes y límites.** Los valores en horas de la primera parte son simultáneos (valores y precios del mismo año). Las tablas nacionales no dicen de qué país vienen los insumos importados; se valúan con el promedio mundial de cada producto. WIOD termina en 2014; la OCDE publica tablas mundiales hasta 2020 (ICIO), que permitirían extender la serie.
