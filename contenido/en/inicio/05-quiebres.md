---
seccion: "05 Endogenous breaks"
id: quiebres
menu: Endogenous breaks
---
## Endogenous breaks

How many specifications detect a break in trend in each year. No break point is fixed in advance.

A statistical procedure searches, in each of the measurements of the multiverse, for the years in which the rate changes course, without anyone telling it where to look. Each bar counts how many measurements show a change of course in that year. The tall bars are the tremors that almost all of them record. They serve to test the periodisations of theory against what the data mark out on their own.
{: .llano }

[[grafico c-quiebres corto]]

### Sensitivity of the detector

The search is repeated with more or less demanding rules. If the same years appear under all of them, they are not an artefact of the method.
{: .llano }

[[tabla t-sens: Configuration | Breaks per specification | Most frequent years (no. of specifications)]]

:::como How are the breaks calculated?
Piecewise linear trends are fitted to each specification, with up to 5 breaks and a minimum segment length of h years, by dynamic programming (as in Bai and Perron, 2003). The number of breaks m is chosen by minimising BIC = n·ln(RSS/n) + k·ln(n), with k = 3m + 2. The chart adds up, year by year, how many specifications place a break in that year (baseline configuration: h = 8, BIC). The table repeats the calculation with h = 6 and h = 10, and with the more demanding LWZ criterion.
:::
