---
seccion: "11b La transformación: valores y precios"
id: transformacion
menu: Valores y precios
oculta: true
---
## La transformación: valores y precios, 2000–2014

Todo lo anterior trabaja con magnitudes agregadas: el plusvalor total de un país es la suma de sus ganancias, intereses, rentas, impuestos y sueldos improductivos, y en ese nivel la formación de los precios no cambia ni la masa ni la tasa de plusvalor. Pero los precios no son proporcionales a los valores rama por rama: la competencia entre capitales tiende a igualar las tasas de ganancia, y con ello redistribuye el plusvalor desde las ramas que emplean mucho trabajo vivo hacia las que emplean mucho capital. Esta sección mide esa redistribución con las tablas insumo-producto de 43 países (WIOD, 2000–2014).

[[cifra tf-desv | Desviación media de los precios respecto de los valores, {{.tf-anio}} (mediana de los países) | ponderada por la producción]]
[[cifra tf-rho | Correlación entre precio/valor y composición del capital (mediana) | países con correlación positiva: {{tf-pos}}]]
[[cifra tf-pond | Masa mundial de plustrabajo en horas del mercado mundial, último año (miles de millones) | sin ponderar: {{tf-sinpond}}]]
[[cifra tf-cnp | Parte de China en la masa ponderada | peso de una hora china: {{tf-wcn}}; india: {{tf-win}}; de EE.UU.: {{tf-wus}}]]

### ¿Cuánto se apartan los precios de los valores?

Para cada rama se calcula cuántas horas de trabajo, directo e indirecto, contiene un dólar de su producto: las horas trabajadas en la propia rama más las contenidas en los insumos que compra a otras ramas productivas, nacionales o importadas. Si los precios fueran proporcionales a esas horas, todas las ramas tendrían el mismo «precio-valor». La línea muestra en cuánto se apartan, en promedio, los precios de mercado de los valores así calculados. Una desviación del 20 % significa que, en promedio, cada rama vende su producto un 20 % por encima o por debajo de su valor.
{: .llano }

[[leyenda l-tf-desv]]
[[grafico c-tf-desv]]

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

### La hora de trabajo en el mercado mundial (miles de millones de horas)

Una hora de trabajo en China no cuenta lo mismo que una en EE.UU. en el mercado mundial: el trabajo nacional más productivo cuenta como trabajo más intenso. La línea ponderada convierte las horas de plustrabajo de cada país en horas del mercado mundial, según cuántos dólares produce una hora de trabajo allí comparada con el promedio. Con esa ponderación, el peso de China en la masa mundial es mucho menor, aunque crece rápido.
{: .llano }

[[leyenda l-tf-pond]]
[[grafico c-tf-pond]]

:::como ¿Cómo se calculan los valores y las desviaciones?
1. **Valores por rama.** Para cada país y año, con la tabla insumo-producto nacional de WIOD (en dólares): λ<sub>p</sub> = (l<sub>p</sub> + λ̄<sub>p</sub> · M<sub>pp</sub>) · (I − A<sub>pp</sub>)<sup>−1</sup>. l = horas trabajadas por dólar de producción (todos los ocupados, incluidos los trabajadores por cuenta propia, porque también producen mercancías; horas de WIOD SEA; en China, 46 h × 50 semanas); A = insumos nacionales por dólar de producto; M = insumos importados; λ̄ = horas medias contenidas en un dólar exportado de cada producto en el mundo (promedio de los 43 países ponderado por sus exportaciones), que se resuelve por iteración.
2. **Ramas que no producen valor.** Sólo entran las ramas productivas. Los insumos que vienen del comercio, las finanzas, los servicios jurídicos y la publicidad, el inmobiliario, la administración pública, la educación, la salud y los hogares no transfieren valor: son gastos pagados con plusvalor (tratamiento de Shaikh y Tonak). Educación y salud quedan fuera porque las tablas no separan su parte capitalista.
3. **Precio-valor.** μ = Σ producción / Σ λ · producción (dólares por hora, ramas productivas); precio-valor de la rama j = μ · λ<sub>j</sub>; precio/valor = 1 / (μ · λ<sub>j</sub>). Desviación media = Σ producción<sub>j</sub> · |μλ<sub>j</sub> − 1| / Σ producción<sub>j</sub>. Correlación: Spearman, entre ramas, de precio/valor con K/v (stock de capital nominal sobre ingreso del trabajo, asalariado y por cuenta propia, WIOD SEA).
4. **Comercio.** Horas entregadas = Σ λ<sub>j</sub> · exportaciones<sub>j</sub>; horas recibidas = Σ λ̄<sub>j</sub> · importaciones<sub>j</sub> × (exportaciones / importaciones), para no confundir la transferencia con el déficit comercial. Sólo productos de ramas productivas. Cubre los 43 países de WIOD, no el resto del mundo, por eso las cifras son menores que las de la aproximación de la sección de contratendencias, que abarca más de cien países.
5. **Ponderación mundial.** Para cada país, μ<sub>c</sub> = PIB en dólares corrientes / horas trabajadas (Banco Mundial y PWT); peso w<sub>c</sub> = μ<sub>c</sub> / μ medio de las horas productivas de los 42 países. Masa ponderada = Σ plustrabajo<sub>c</sub> × w<sub>c</sub>. El total de horas no cambia; se redistribuye según la productividad nacional en el mercado mundial. Después del último año de la PWT se mantiene el último peso.

Interpretación: los valores por rama no son «trabajo incorporado» como una propiedad física de los productos, sino una aproximación al tiempo de trabajo socialmente necesario como determinación de la totalidad social. Se calculan de manera simultánea (valores y precios del mismo año); la variante temporal (TSSI) está pendiente.
:::
