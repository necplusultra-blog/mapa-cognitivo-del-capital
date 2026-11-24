---
seccion: "05 Quiebres endógenos"
id: quiebres
menu: Quiebres endógenos
---
## Quiebres endógenos

Cuántas especificaciones detectan un quiebre de tendencia en cada año. Ningún corte se fija de antemano.

[[grafico c-quiebres corto]]

### Sensibilidad del detector

[[tabla t-sens: Configuración | Quiebres por especificación | Años más frecuentes (n.º de especificaciones)]]

:::como ¿Cómo se calculan los quiebres?
A cada especificación se le ajustan tendencias lineales por tramos, con hasta 5 quiebres y un tramo mínimo de h años, por programación dinámica (como en Bai y Perron). El número de quiebres m se elige minimizando BIC = n·ln(SCR/n) + k·ln(n), con k = 3m + 2. El gráfico suma, año por año, cuántas especificaciones ponen un quiebre en ese año (configuración base: h = 8, BIC). La tabla repite el cálculo con h = 6 y h = 10, y con el criterio LWZ, más exigente.
:::
