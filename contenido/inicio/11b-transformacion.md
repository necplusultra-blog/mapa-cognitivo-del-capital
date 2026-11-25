---
seccion: "11b La transformación: valores y precios"
id: transformacion
menu: Valores y precios
oculta: true
---
## La transformación: valores y precios, 2000–2014

Todo lo anterior trabaja con magnitudes agregadas: el plusvalor total de un país es la suma de sus ganancias, intereses, rentas, impuestos y sueldos improductivos, y en ese nivel la formación de los precios no cambia ni la masa ni la tasa de plusvalor. Pero los precios no son proporcionales a los valores rama por rama: la competencia entre capitales tiende a igualar las tasas de ganancia, y con ello redistribuye el plusvalor desde las ramas que emplean mucho trabajo vivo hacia las que emplean mucho capital. Esta sección mide esa redistribución con las tablas insumo-producto de 43 países (WIOD, 2000–2014) y la contrasta y extiende hasta 2024 con las tablas mundiales de la OCDE. La educación y la salud entran por su parte capitalista: la que no es pública ni sin fines de lucro.

[[cifra tf-desv | Desviación media de los precios respecto de los valores, {{.tf-anio}} (mediana de los países) | ponderada por la producción]]
[[cifra tf-rho | Correlación entre precio/valor y composición del capital (mediana) | países con correlación positiva: {{tf-pos}}]]
[[cifra tf-pond | Masa mundial de plustrabajo en horas del mercado mundial, último año (miles de millones) | sin ponderar: {{tf-sinpond}}]]
[[cifra tf-cnp | Parte de China en la masa ponderada | peso de una hora china: {{tf-wcn}}; india: {{tf-win}}; de EE.UU.: {{tf-wus}}]]

### ¿Cuánto se apartan los precios de los valores?

Para cada rama se calcula cuántas horas de trabajo, directo e indirecto, contiene un dólar de su producto: las horas trabajadas en la propia rama más las contenidas en los insumos que compra a la parte capitalista de otras ramas productivas, nacionales o importadas. Si los precios fueran proporcionales a esas horas, todas las ramas tendrían el mismo «precio-valor». La línea muestra en cuánto se apartan, en promedio, los precios de mercado de los valores así calculados. La desviación se mide como la distancia entre valor y precio en proporción al precio: una desviación del 20 % significa que, en promedio, el valor de lo que cada rama vende es un 20 % mayor o menor que su precio (no es simétrica: una rama que vende un 20 % por encima de su valor tiene una desviación del 16,7 %).
{: .llano }

[[leyenda l-tf-desv]]
[[grafico c-tf-desv]]

Fuentes: WIOD: tablas insumo-producto nacionales y Cuentas Socioeconómicas 2016 (43 países, 2000–2014); OIT (asalariados de China). Cálculo propio.
{: .fuente }

### Quién cede valor y quién se lo apropia ({{.tf-anio}}, {{.tf-n}} países)

Precio/valor por debajo de 1: la rama vende por debajo del valor que produce y cede plusvalor a otras ramas. Por encima de 1: vende por encima y se apropia plusvalor producido en otras partes. Marx esperaba que las ramas con mucho capital por trabajador (composición alta) vendieran por encima de su valor, y las de mucho trabajo vivo, por debajo. La tabla lo confirma: la agricultura, la pesca, el textil y la hotelería ceden valor; la refinación de petróleo, la minería, la energía, los metales y la química se lo apropian.
{: .llano }

[[tabla t-tf-ramas: Rama | Precio / valor | Composición K/v (mediana)]]

Precio/valor promedio de los 43 países, ponderado por la producción. Composición: stock de capital sobre ingreso del trabajo de la rama, asalariado y por cuenta propia (WIOD).
{: .nota }

### Trabajo incorporado en el comercio exterior (miles de millones de horas)

Cuántas horas de trabajo ajeno recibe cada país por su comercio, contando también el trabajo contenido en los insumos de lo que exporta e importa. Positivo: el país recibe en sus importaciones más horas de las que entrega en sus exportaciones, a igual valor en dólares. Los países de altos ingresos reciben; China e India entregan.
{: .llano }

[[leyenda l-tf-com]]
[[grafico c-tf-com]]

Fuentes: WIOD: tabla insumo-producto mundial y Cuentas Socioeconómicas 2016; Banco Mundial (clasificación por ingreso). Cálculo propio.
{: .fuente }

<div id="tf-icio" hidden markdown="1">

### Hasta {{.tf-ifin}}, con las tablas mundiales de la OCDE

Las tablas de WIOD terminan en 2014. Las tablas mundiales de la OCDE (ICIO, edición 2026) cubren 84 economías y doce regiones del resto del mundo, con el país de origen de cada insumo: el trabajo contenido en lo que un país importa se calcula con las horas del país que lo produjo, no con un promedio mundial. Aquí se usan 2000–2005 (sin 2003) y 2015–{{.tf-ifin}}; los años 2000–2005 vienen de la edición anterior (2025, 80 economías y el resto del mundo) y 2023–2024 son proyecciones de la propia OCDE. Las horas vienen del empleo por rama de la OCDE (TiM), que llega a 2022, y de las horas por ocupado de la Penn World Table. Las medianas abarcan sólo las {{tf-in}} economías con empleo medido. Los niveles no se comparan directamente con los de WIOD: hay más países, en particular de ingresos bajos, otra clasificación de ramas y otro tratamiento de los insumos importados. Lo que se compara es el patrón: quién cede valor, quién lo recibe y cuánto se aparta el precio del valor. Un resultado salta a la vista: China entregaba en su comercio más de 200 mil millones de horas al año a mediados de los 2000 y menos de 80 desde 2020, mientras India entrega 114 mil millones en 2005, 89 en 2016 y 113 en 2024.
{: .llano }

[[cifra tf-idesv | Desviación media de los precios respecto de los valores, {{.tf-ifin}} (mediana de las economías con empleo medido) | tablas mundiales de la OCDE]]
[[cifra tf-icalto | Horas recibidas en el comercio por los países de altos ingresos, {{.tf-ifin}} (miles de millones) | China: {{tf-icchn}} · India: {{tf-icind}}]]

[[leyenda l-tf-idesv]]
[[grafico c-tf-idesv]]

Fuentes: OCDE: tablas insumo-producto mundiales (ICIO, ediciones 2025 y 2026) y empleo por rama (TiM 2025); Penn World Table 11.0 (horas). Cálculo propio.
{: .fuente }

[[leyenda l-tf-icom]]
[[grafico c-tf-icom]]

Fuentes: OCDE: ICIO (ediciones 2025 y 2026) y TiM 2025; Penn World Table 11.0; Banco Mundial (clasificación por ingreso). Cálculo propio.
{: .fuente }

Miles de millones de horas. Positivo: el país recibe en sus importaciones más horas de las que entrega en sus exportaciones, a igual valor en dólares.
{: .nota }

</div>

### La hora de trabajo en el mercado mundial (miles de millones de horas)

Una hora de trabajo en China no cuenta lo mismo que una en EE.UU. en el mercado mundial: el trabajo nacional más productivo cuenta como trabajo más intenso. La línea ponderada convierte las horas de plustrabajo de cada país en horas del mercado mundial, según cuántos dólares produce una hora de trabajo allí comparada con el promedio. Con esa ponderación, el peso de China en la masa mundial es mucho menor, aunque crece rápido.
{: .llano }

[[leyenda l-tf-pond]]
[[grafico c-tf-pond]]

Fuentes: WIOD (tablas insumo-producto y Cuentas Socioeconómicas 2016) y las fuentes de la masa mundial en horas. Cálculo propio.
{: .fuente }

### La transformación según Moseley, con la variante temporal (TSSI) como contraste

La medición anterior calcula valores en horas. Ésta sigue la interpretación de Moseley (2016), que el mapa cognitivo adopta como central: los costos en dinero —los insumos y los salarios— son los mismos para los valores y para los precios de producción, y lo que cambia es sólo cómo se reparte el plusvalor. En valores, cada rama tendría el plusvalor que producen sus propios obreros; en precios de producción, cada rama recibe una ganancia proporcional al capital que adelanta. La diferencia es el plusvalor que la competencia traslada de unas ramas a otras. La variante temporal (TSSI; Kliman, 2007) valúa los insumos y el capital a los precios con que entraron en la producción: en los años de inflación da tasas más altas, y en la crisis de 2009 converge con la central.
{: .llano }

[[cifra tf-red | Parte del plusvalor que la igualación de las tasas traslada entre ramas, {{.tf-anio}} (mediana de los países) | Moseley]]
[[cifra tf-rm | Tasa de ganancia de las ramas productivas de los 43 países, {{.tf-anio}} (Moseley) | 2000: {{tf-rm0}} · TSSI {{.tf-anio}}: {{tf-rt}}]]
[[cifra tf-cve | Dispersión de las tasas de ganancia efectivas entre ramas (coef. de variación, mediana) | si cada rama realizara su propio plusvalor: {{tf-cvv}}]]
[[cifra tf-igu | Países y años en que la competencia reduce la dispersión de las tasas | desviación del mercado respecto de los valores: {{tf-dv}}; de los precios de producción: {{tf-dpp}}]]

[[leyenda l-tf-mt]]
[[grafico c-tf-mt]]

Fuentes: WIOD: tablas insumo-producto nacionales y Cuentas Socioeconómicas 2016 (incluye acervos de capital); OIT (asalariados de China). Cálculo propio a la manera de Moseley y de la TSSI.
{: .fuente }

Tasa = plusvalor de las ramas productivas / (capital fijo + capital variable anual), en %. 43 países: suma en dólares. La TSSI empieza en 2001 porque necesita los precios del año anterior.
{: .nota }

Las ramas que ganan con la igualación son las de mucho capital por trabajador —agua, audiovisual, electricidad y gas, minería, residuos, telecomunicaciones—; las que ceden plusvalor son las de mucho trabajo vivo: servicios profesionales, la parte capitalista de la educación y la salud, informática y construcción. Las tasas efectivas están más cerca entre sí que las tasas «en valores», como espera la teoría, aunque la igualación es parcial. En cambio, los precios de mercado no quedan sistemáticamente más cerca de los precios de producción que de los valores: sólo en el {{tf-ppm}} de los países y años. Las dos mediciones no coinciden en todas las ramas: la agricultura cede valor medida en horas, pero gana con la igualación en la de Moseley (véase más abajo).
{: .llano }

[[tabla t-tf-mr: Rama ({{.tf-anio}}) | Transferencia por la igualación (% del valor) | Tasa si realizara su propio plusvalor | Tasa efectiva]]

### Por qué la agricultura cede valor en una medición y gana en la otra

Hay dos razones. La primera es que las dos mediciones no responden la misma pregunta. La medición en horas compara el precio de mercado con el valor; la de Moseley, sobre todo, el precio de producción con el valor. Con la de Moseley, la agricultura recibe plusvalor con la igualación de las tasas, porque su precio de producción supera su valor, y su precio de mercado queda algo por encima de su valor (valor/precio {{tf-ag-mo}}). La segunda razón, la decisiva, es la valuación del trabajo por cuenta propia: sólo el {{tf-ag-as}} de los ocupados del campo son asalariados. En horas, cada hora de un campesino cuenta como una hora de trabajo social; en la de Moseley, su trabajo entra por el ingreso en dinero que recibe, que es muy bajo. Si en la medición en horas se cuentan sólo las horas de los asalariados, el valor/precio de la agricultura baja de {{tf-ag-v1}} a {{tf-ag-v1a}}: la agricultura asalariada vende, en promedio, cerca de su valor. En China, que pesa casi el 40 % de la producción agrícola de los 43 países, WIOD no separa a los asalariados; se usa el mismo supuesto que en la masa mundial (asalariados de la OIT en las ramas no agrícolas, ninguno en la agricultura familiar). En la mediana de los países y años, esa valuación explica alrededor del {{tf-ag-expl}} de la distancia entre las dos mediciones. El resto viene de los salarios: en horas, una hora es una hora; en la de Moseley cuenta el salario pagado, y los asalariados del campo ganan menos por hora que el promedio.
{: .llano }

[[tabla t-tf-conc: Rama ({{.tf-anio}}) | Asalariados (% de los ocupados) | Valor / precio en horas | En horas, sólo asalariados | Valor / precio, Moseley]]

Valor/precio mayor que 1: la rama vende por debajo de su valor y cede plusvalor. Promedios de los 43 países ponderados por la producción; ramas con menor proporción de asalariados.
{: .nota }

:::como ¿Cómo se calculan los valores y las desviaciones?
1. **Valores por rama.** Para cada país y año, con la tabla insumo-producto nacional de WIOD (en dólares): λ = (l + (λ̄ ∘ φ) · M) · (I − D<sub>φ</sub> A)<sup>−1</sup>, donde D<sub>φ</sub> es la diagonal con la fracción capitalista φ de cada rama proveedora. l = horas trabajadas por dólar de producción (todos los ocupados, incluidos los trabajadores por cuenta propia, porque también producen mercancías; horas de WIOD SEA; en China, 46 h × 50 semanas); A = insumos nacionales por dólar de producto; M = insumos importados; λ̄ = horas medias contenidas en un dólar exportado de cada producto en el mundo (promedio de los 43 países ponderado por sus exportaciones), que se resuelve por iteración.
2. **Ramas que no producen valor.** φ = 1 en las ramas productivas y 0 en el comercio, las finanzas, los servicios jurídicos y contables, la publicidad, el inmobiliario, la administración pública y los hogares: sus insumos no transfieren valor, son gastos pagados con plusvalor (tratamiento de Shaikh y Tonak, 1994). En educación y salud, φ = 1 − g, con g la parte pública y sin fines de lucro del empleo (la misma de la masa mundial): sólo su parte capitalista produce valor y se supone que tiene la misma estructura de costos que la rama entera.
3. **Precio-valor.** μ = Σ φ · producción / Σ λ · φ · producción (dólares por hora, parte capitalista de las ramas productivas); precio-valor de la rama j = μ · λ<sub>j</sub>; precio/valor = 1 / (μ · λ<sub>j</sub>). Desviación media = Σ producción<sub>j</sub> · |μλ<sub>j</sub> − 1| / Σ producción<sub>j</sub>. Correlación: Spearman, entre ramas, de precio/valor con K/v (stock de capital nominal sobre ingreso del trabajo, asalariado y por cuenta propia, WIOD SEA).
4. **Comercio.** Horas entregadas = Σ λ<sub>j</sub> · φ<sub>j</sub> · exportaciones<sub>j</sub>; horas recibidas = Σ λ̄<sub>j</sub> · φ<sub>j</sub> · importaciones<sub>j</sub> × (exportaciones / importaciones), para no confundir la transferencia con el déficit comercial. Cubre los 43 países de WIOD, no el resto del mundo, por eso las cifras son menores que las de la aproximación de la sección de contratendencias, que abarca más de cien países.
5. **Ponderación mundial.** Para cada país, μ<sub>c</sub> = PIB en dólares corrientes / horas trabajadas (Banco Mundial y PWT); peso w<sub>c</sub> = μ<sub>c</sub> / μ medio de las horas productivas de los 42 países. Masa ponderada = Σ plustrabajo<sub>c</sub> × w<sub>c</sub>. El total de horas no cambia; se redistribuye según la productividad nacional en el mercado mundial. Después del último año de la PWT se mantiene el último peso.

6. **Tablas mundiales de la OCDE (F4 v3, 2000–2005 sin 2003, y 2015–2024).** Con la matriz mundial completa de ICIO: edición 2026 para 2015–2024 (84 economías, doce regiones y 50 ramas; 2023 y 2024 son proyecciones de la OCDE) y edición 2025 para 2000–2005 (80 economías y el resto del mundo, mismas 50 ramas): λ = l · (I − D<sub>φ</sub> A)<sup>−1</sup>, sin promedio λ̄, porque cada insumo importado se valúa con las horas del país que lo produjo. l = ocupados por rama (OCDE, TiM 2025) × horas anuales por ocupado (PWT) / producción. TiM llega a 2022; en 2023 y 2024 se mantiene la estructura por rama de 2022 y se escala con la ocupación total de la PWT (2024 = 2023). En servicios profesionales (M), φ es la parte de arquitectura e ingeniería, investigación y otros servicios profesionales en la producción de M según WIOD 2014 (sin jurídicos, contables ni publicidad). Para las regiones sin datos de empleo, l se imputa con la mediana mundial de horas por dólar de valor agregado de la rama; esas regiones entran en la matriz pero no en las medianas del gráfico. Se calcula con `herramientas/icio.py` a partir de los archivos de la OCDE, que pesan cientos de MB y no admiten descargas automáticas; sólo se guardan los resultados compactos. Faltan 2003 (el archivo descargado estaba incompleto) y 2006–2014, cubiertos por WIOD.
7. **Conciliación con la medición de Moseley.** Valor/precio en horas con sólo las horas de los asalariados: l<sub>j</sub> × (asalariados<sub>j</sub> / ocupados<sub>j</sub>), WIOD SEA (en China, la proporción s de la OIT). Se compara con W<sub>j</sub> / producción<sub>j</sub> de la medición de Moseley. Parte de la diferencia explicada = (v1 − v1 sólo asalariados) / (v1 − Moseley), mediana de los países y años, en la agricultura.

Interpretación: los valores por rama no son «trabajo incorporado» como una propiedad física de los productos, sino una aproximación al tiempo de trabajo socialmente necesario como determinación de la totalidad social. Se calculan de manera simultánea (valores y precios del mismo año).

**Moseley y TSSI (F4 v2).** En moneda nacional, por país y año, con la parte capitalista de las ramas productivas (todas las magnitudes de educación y salud multiplicadas por φ): c<sub>j</sub> = insumos de ramas productivas (nacionales e importados, de la tabla insumo-producto convertida con la producción de WIOD SEA); v<sub>j</sub> = remuneración de los asalariados (en China, que WIOD registra sin separar asalariados, remuneración × s, con s la proporción de asalariados de la OIT en las ramas no agrícolas y cero en la agricultura, como en la masa mundial); a<sub>j</sub> = ingreso laboral de los trabajadores por cuenta propia (producen valor, no plusvalor); K<sub>j</sub> = stock nominal de capital. S = Σ (producción − c − v − a), que incluye los insumos de ramas improductivas, pagados con plusvalor; e = S / V; r = S / (Σ K + Σ V). Valor: W<sub>j</sub> = c<sub>j</sub> + a<sub>j</sub> + v<sub>j</sub>(1 + e). Precio de producción: PP<sub>j</sub> = c<sub>j</sub> + a<sub>j</sub> + v<sub>j</sub> + r (K<sub>j</sub> + v<sub>j</sub>). Ambas sumas coinciden con la producción total, y el plusvalor total con la ganancia total. Transferencia = (PP<sub>j</sub> − W<sub>j</sub>) / W<sub>j</sub>; parte redistribuida = Σ |PP − W| / 2 / S. Tasa efectiva = (producción − c − v − a) / (K + v); tasa en valores = e · v / (K + v); dispersión: coeficiente de variación ponderado por el capital. **TSSI:** los insumos se deflactan con el índice de precios de los insumos de cada rama (II_PI<sub>t</sub> / II_PI<sub>t−1</sub>) y el capital adelantado es el stock del año anterior.
:::
