---
seccion: "10 World mass in hours"
id: horas-mundo
menu: World mass in hours
oculta: true
---
## World mass of surplus value in labour hours, 2000–{{hm-fin}}

The same criterion as for the United States, applied industry by industry to {{hm-np}} countries that together account for most of world output. Up to {{hm-base}}, WIOD industry accounts. From {{.hm-base1}}, OECD industry accounts for the countries that publish them ({{hm-nocde}} in the last year), UN national accounts by industry for the surplus of Brazil and India, ILO surveys by activity section for employment and hours in Brazil, Indonesia, India, Russia, Mexico, Turkey, Cyprus and Malta, OECD employment and labour income by industry (TiM) for China's surplus up to 2022, and the ILO aggregate extension for the number of employees in China. The dotted segment marks that everything after {{.hm-base0}} is chained to the WIOD level. For each country, e = pv/v with the employees of the productive industries, and the mass of surplus labour = hours of those employees × e/(1+e). The net version subtracts from surplus value the consumption of fixed capital of the market industries.

[[cifra hm-n | Productive wage earners worldwide, {{.hm-fin}} (millions) | {{.hm-base0}}: {{hm-n14}}]]
[[cifra hm-masa | Annual mass of surplus labour, gross (billion hours) | 2000: {{hm-masa0}}; {{.hm-base0}}: {{hm-masa14}}]]
[[cifra hm-masan | Mass net of depreciation (billion hours) | 2000: {{hm-masan0}}]]
[[cifra hm-e | World rate of surplus value in hours, gross and net | China contributes {{hm-cn}} of the mass; India, {{hm-in}}]]

### World mass of surplus labour (billion hours per year)

Hours of unpaid labour that capital obtains in a year in the 42 countries measured, which together account for most of world output. The gross line counts all surplus labour; the net line deducts the part of the new value that merely replaces worn-out machines and buildings. The gross line grows with a few dips (2009, the pandemic, 2024); the net line fell after 2007, did not recover its level until 2012 and stops growing from 2018 onwards. The dotted segment indicates that from 2015 the figures are chained to those of 2014.
{: .llano }

[[leyenda l-hm]]
[[grafico c-hm]]

Sources: WIOD, Socio-Economic Accounts 2016 and national input–output tables (2000–2014); OECD: national accounts by industry (tables 6 and 7) and TiM 2025 (China); UN: national accounts, table 2.6 (Brazil and India); ILO (ILOSTAT): employees, employment, hours and labour share; Penn World Table 11.0: depreciation and hours. Own calculation.
{: .fuente }

<div id="rn-bloque" hidden markdown="1">

### Does the stagnation of the net mass hold up? Different estimates of depreciation in China and India

China and India contribute two thirds of the world mass, and their depreciation is the most uncertain estimate in the whole measurement. Here the net mass is recalculated with five alternative estimates, changing only the depreciation of those two countries: lower and higher than the central one, the World Bank's, the median of the other countries, and that of 2018 held fixed. In all of them, the net mass grows strongly between 2000 and 2018 and then stays practically flat: between 2018 and the last year it changes {{rn-rango}}. The stagnation is not an effect of how depreciation is estimated.
{: .llano }

[[leyenda l-rn]]
[[grafico c-rn corto]]

Sources: WIOD, Socio-Economic Accounts 2016 and national input–output tables (2000–2014); OECD: national accounts by industry (tables 6 and 7) and TiM 2025 (China); UN: national accounts, table 2.6 (Brazil and India); ILO (ILOSTAT): employees, employment, hours and labour share; Penn World Table 11.0: depreciation and hours; World Bank: consumption of fixed capital (NY.ADJ.DKAP.GN.ZS). Own calculation.
{: .fuente }

[[tabla t-rn: Depreciation in China and India | 2000 | 2018 | Last year | 2000–2018 | 2018–last year]]

:::como How are these variants calculated?
Only the depreciation/GDP ratio of China and India changes; the other countries remain as in the central estimate. **Central:** Penn World Table, δ·K/Y. **PWT × 0.8 and × 1.2:** a depreciation rate 20% lower or higher. **World Bank:** consumption of fixed capital as a % of gross national income (NY.ADJ.DKAP.GN.ZS), with the last observation carried forward into subsequent years. **Median:** the median depreciation/GDP of the other countries measured in that year. **Constant from 2018:** the 2018 ratio held fixed, to isolate the effect of its subsequent increase. In all cases, r = k · depreciation/GDP × market value added / v, with the same calibration k as in the central estimate (and, for India 2015–2020, the change measured by the UN); e<sub>net</sub> = e − r; net mass = hours × e<sub>net</sub> / (1 + e<sub>net</sub>), as in the central estimate. Result: `mundo_neta_robustez.csv`.
:::

</div>

### World rate of surplus value in hours: surplus labour / necessary labour

How many hours a productive wage earner in the world works for capital for each hour worked to replace his or her wage. It is almost the same at the beginning and at the end of the period (it rises until 2007 and falls until 2012): on average, world capital has not raised the degree of exploitation in this century. The mass grows because there are more wage earners, not because each one works more for capital. The net version falls, because each hour of labour sets in motion more fixed capital that has to be replaced.
{: .llano }

[[leyenda l-hme]]
[[grafico c-hme corto]]

Sources: WIOD, Socio-Economic Accounts 2016 and national input–output tables (2000–2014); OECD: national accounts by industry (tables 6 and 7) and TiM 2025 (China); UN: national accounts, table 2.6 (Brazil and India); ILO (ILOSTAT): employees, employment, hours and labour share; Penn World Table 11.0: depreciation and hours. Own calculation.
{: .fuente }

:::como+ How is the number of productive workers calculated?
**Criterion.** A wage earner is productive when his or her wage is money invested as capital and his or her surplus labour is converted into surplus value. That is why casual labourers count, whatever the duration of their employment, and so do agricultural wage earners when their wage is capital. Own-account (self-employed) workers do not count, nor do those who work for a wage that is a mere means of circulation: the state (except its enterprises that sell commodities for profit), non-profit institutions and employer households.

1. **2000–{{.hm-base0}} (WIOD, Socio-Economic Accounts 2016).** For each country, the employees (EMPE) and their hours (H_EMPE) of the productive industries are added up. Excluded are the circulation industries (trade G45–G47, finance and insurance K64–K66, legal, accounting and management services M69–M70, advertising M73) and those outside capitalist production (real estate L68, public administration O84, households T, extraterritorial organisations U). Education (P85) and health (Q) count only in their capitalist part: the part paid for by the state or by non-profit institutions is left out (see step 6).
2. **China.** WIOD does not distinguish employees in China. The total number of employees is taken from the ILO modelled estimates and distributed among the non-agricultural industries in proportion to their employment in WIOD: s = ILO employees / (ILO employment × (1 − WIOD agricultural share)). Productive employees are the employment of the non-agricultural productive industries × s. Chinese agriculture is almost entirely family-based and has no employees in the sources, so it does not contribute. Hours assume a 46-hour week and 50 weeks (sensitivity: 44 and 49 hours).
3. **From {{.hm-base1}}, OECD countries (national accounts table 7).** Employees (SAL) and their hours, by ISIC Rev. 4 section, with the same industry criterion. The series is chained to the WIOD level of 2014: N<sub>t</sub> = N<sub>WIOD,2014</sub> × N<sub>OECD,t</sub> / N<sub>OECD,2014</sub>; hours per employee likewise.
4. **From {{.hm-base1}}, countries without employees by industry in the OECD data: measurement by section with the ILO.** For Brazil, Indonesia, India, Russia, Mexico, Turkey, Cyprus and Malta, the labour force surveys harmonised by the ILO give the employees, their hours and their mean earnings by activity section. With a single survey per country, from the first year available from 2014 onwards (India: 2018; Russia: 2017), the productive share of employees, the weekly hours of the productive sections and the productive share of the wage bill are measured, and with them the number of productive employees, their hours and the rate of surplus value of the aggregate extension are corrected. China does not publish employees by section in the ILO data; their number and rate of surplus value are measured up to 2022 with OECD employment and labour income by industry (TiM), and thereafter follow the aggregate extension.
5. **From {{.hm-base1}}, aggregate extension (ILO).** N<sub>t</sub> = N<sub>2014</sub> × total employees<sub>t</sub> / total employees<sub>2014</sub> (ILO modelled estimates), keeping the productive share of 2014; hours per person employed follow the ILO weekly hours. **India:** WIOD counts both regular employees and casual labourers as employees; the ILO series only covers regular employees. For India, N is extended with total ILO employment times the share of workers who are not own-account workers in the official surveys (NSS 2011-12 and PLFS 2017-18 to 2023-24).
6. **Public and non-profit education and health.** The calculation is done twice, with all of education and health in and with all of it out. The central estimate combines both according to the non-capitalist share g of each country: g = (general government employment + non-profit institutions employment − public administration employment) / education and health employment, using the OECD accounts by institutional sector; outside them, the ILO surveys of public employment by activity, and where there are none, the median of the countries measured. In the United States the non-profit share according to the BLS is added. Necessary hours, surplus-labour hours and employees are combined as (1 − g) × ‘in’ + g × ‘out’. The shares are in `mundo_horas_parte_publica.csv`. Employees of state enterprises that sell commodities for profit count as productive: their wage is capital.
7. The world total is the sum of the countries. The source for each country and year is in [mundo_horas_paises.csv](descargas/).
:::

:::como+ How is the world mass of surplus value calculated?
1. **Variable capital (v):** compensation of the employees of the productive industries (WIOD: COMP; OECD: D1).
2. **Surplus value (pv):** gross value added of the market industries (all except L68, O84, T, U and the non-capitalist part of education and health) − labour income imputed to own-account workers − v. That income is LAB − COMP in WIOD and, in the OECD data, non-employees × mean compensation per employee in the same section. The wages of the circulation industries remain within pv: they are deductions from the total mass of surplus value.
3. **Rate of surplus value:** e = pv/v, in national currency (with two adjustments from the section [what counts as surplus value](#supuestos): e' = e + (B3 − B4) · (1 + e + cp/v), where B3 adds the rent that the market industries pay for premises and offices (surplus value produced and ceded to landed property) and B4 subtracts the financial services that households pay for out of their wages (surplus value displaced from the wage), both as shares of market value added; floor of 0.01), so that no currency conversion is needed. From 2015, e is chained to the WIOD level of 2014 with the change measured by industry in the OECD data (table 6) or, where there is none, with the ILO labour share: e<sub>t</sub> = e<sub>2014</sub> × [(1 − LS<sub>t</sub>)/LS<sub>t</sub>] / [(1 − LS<sub>2014</sub>)/LS<sub>2014</sub>]. In Brazil and India (2015–2020), e is measured industry by industry with the UN national accounts (table 2.6: compensation, mixed income and value added by section) and chained in the same way. In China (2015–2022), e is measured industry by industry with OECD employment and labour income by industry (TiM 2025, consistent with its world tables) and chained in the same way. In the other countries measured by section with the ILO (and in Brazil and India after 2020, re-anchored in the last UN year), 1 + e<sub>t</sub> is multiplied by q<sub>b</sub>/q<sub>t</sub>, where q is the productive share of the wage bill: if the productive wage bill grows, v grows and e falls.
4. **Net version:** e<sub>net</sub> = e − r, with r = consumption of fixed capital of the market industries / v. In the OECD data it is measured by industry (P51C). Where there is no measurement, r = (PWT δ·K/Y) × market value added / v, calibrated with the country's own 2014 OECD/PWT ratio or, outside the OECD, with the median of those ratios ({{hm-kmed}}), because PWT depreciation includes dwellings and public capital.
5. **Mass in hours:** surplus labour = H × e / (1 + e) for each country, summed over all of them. The world rate in hours is Σ surplus labour / Σ necessary labour. Observations for the WIOD years with e outside (0, 8) are excluded because of data anomalies: {{hm-excl}}.
:::

### The largest centres of surplus labour, {{.hm-fin}}

The countries where most surplus labour is produced. China and India together account for almost two thirds of the total.
{: .llano }

[[tabla t-hm: Country | Productive wage earners (millions) | Gross e | Net e | Gross surplus labour (billion hours) | % of total | Source of e]]

### How much each assumption weighs (central estimate, with China)

Each row changes a single assumption relative to the central estimate. The rows marked as contrast are not alternative readings of the adopted criterion: they show how much the casual labourers of India and the agricultural wage labour of India and China weigh in the world mass.
{: .nota }

Each row changes a single assumption and shows how much the total changes. It serves to tell which figures are firm and which depend on decisions.
{: .llano }

[[tabla t-hms: Year | Case | Surplus labour (billion hours) | Productive wage earners (millions) | Difference | Note]]

:::como Diagnostics of the OECD–WIOD splice in 2014
If the two sources measure the same thing, the 2014 ratios should be close to 1. WIOD sets the level; the OECD only supplies the subsequent change. The column ‘r PWT’ is Penn World Table depreciation without calibration: its distance from ‘r OECD’ is what the calibration corrects.

[[tabla t-hmd: Country | e WIOD | e OECD | Employees OECD/WIOD | Hours OECD/WIOD | r PWT | r OECD | Last OECD year]]
:::

Caveats: the figures after 2014 are chained, not newly measured levels; in the OECD countries the change is indeed measured by industry. China is an estimate. There is no within-industry correction at the world scale. The world sum counts hours of exploited labour, not abstract labour time of the world market: according to Marx, the more productive national labour counts on the world market as more intensive labour, and that weighting is left for the transformation phase. Because of differences in definition, the e of the United States here does not coincide with that of the United States section.
{: .nota }
