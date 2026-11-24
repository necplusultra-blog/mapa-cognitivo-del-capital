---
seccion: "05 Quiebres endógenos"
id: quiebres
menu: Quiebres endógenos
---
## Quiebres endógenos

Cuántas especificaciones detectan un quiebre de tendencia en cada año. Ningún corte se fija de antemano.

Un procedimiento estadístico busca, en cada una de las mediciones del multiverso, los años en que la tasa cambia de rumbo, sin que nadie le diga dónde buscar. Cada barra cuenta en cuántas mediciones aparece un cambio de rumbo en ese año. Las barras altas son los temblores que casi todas registran. Sirven para contrastar las periodizaciones de la teoría con lo que los datos marcan por sí solos.
{: .llano }

[[grafico c-quiebres corto]]

### Sensibilidad del detector

La búsqueda se repite con reglas más o menos exigentes. Si los mismos años aparecen con todas, no son un efecto del método.
{: .llano }

[[tabla t-sens: Configuración | Quiebres por especificación | Años más frecuentes (n.º de especificaciones)]]

:::como ¿Cómo se calculan los quiebres?
A cada especificación se le ajustan tendencias lineales por tramos, con hasta 5 quiebres y un tramo mínimo de h años, por programación dinámica (como en Bai y Perron). El número de quiebres m se elige minimizando BIC = n·ln(SCR/n) + k·ln(n), con k = 3m + 2. El gráfico suma, año por año, cuántas especificaciones ponen un quiebre en ese año (configuración base: h = 8, BIC). La tabla repite el cálculo con h = 6 y h = 10, y con el criterio LWZ, más exigente.
:::
