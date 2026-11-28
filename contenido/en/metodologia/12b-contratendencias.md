---
seccion: "12b Countertendencies"
id: contratendencias
menu: Countertendencies
---
## Countertendencies

The analysis follows Marx's six counteracting causes (*Capital*, Volume III, ch. XIV). The sixth, the increase in share capital, is extended to interest-bearing capital in general. None is measured by a single indicator: each manifests itself in several series that must be read together with the rate and the mass of surplus value.

**Decomposition by phases.** The rate of profit is written as r = e · (V/K), so that, between two years,

<div class="f">Δln r = Δln e − Δln(K/V)</div>

From 1972, with the hours of productive workers, the value composition is separated into a technical composition and a relative price:

<div class="f">K/V = (K<sub>real</sub> / H) · (P<sub>K</sub> / w) · P<sub>K</sub> = K<sub>current cost</sub> / (quantity index × K<sub>2017</sub> / 100) · w = V / H</div>

The quantity index and the stock at current cost are those of the BEA's private non-residential fixed capital (kcntotl1es00, k1ntotl1es00); K and V are those of the within-industry variant. The cut-off years are the five most frequent break years in the main set of specifications (h = 8, BIC), at least six years apart: the periodisation is not fixed in advance.

**Robustness across the multiverse.** The decomposition is repeated for each business-sector specification without utilisation adjustment and with denominator K (16 per productive-labour criterion: current or historical cost, net or gross, with or without intellectual property, all capital or only productive capital). The median and the 10th and 90th percentiles of the contributions are published, together with the percentage of specifications in which the rate rises and, among the specifications in which the composition rises, the percentage in which Δln e ≥ Δln(K/V) (contratendencias_fases_especificaciones.csv).

**Transfer of labour time through foreign trade.** For each country, h = H / GDP, with H = persons employed × annual hours (PWT 11.0) and GDP in current dollars at market exchange rates (World Bank):

<div class="f">h<sub>X</sub> = Σ<sub>j</sub> X<sub>j</sub> h<sub>j</sub> / Σ<sub>j</sub> X<sub>j</sub> · T<sub>i</sub> = M<sub>i</sub> · h<sub>X</sub> − X<sub>i</sub> · h<sub>i</sub></div>

T > 0 indicates appropriation of alien labour time. The years with at least 100 countries with hours are included (from 2005). It is an approximation without intermediate inputs; a world input-output matrix (OECD ICIO) would make it possible to trace the hours content of each flow (intercambio_horas.csv, intercambio_horas_paises.csv).

**Indicators by countertendency.**

| Countertendency | Indicators | Source |
| --- | --- | --- |
| Raising of the degree of exploitation | rate of surplus value; output per hour and real compensation per hour; weekly hours; multiple jobholding and involuntary part-time work | BEA, BLS (OPHNFB, COMPRNFB, LNS12026619, LNS12032194, CE16OV) |
| Reduction of wages below their value | real hourly wage of production workers; household debt service | BLS (AHETPI), CPI, Federal Reserve (TDSP) |
| Cheapening of constant capital | relative price of investment; technical composition and capital/wage relative price | BEA (A008RD, DPCERG, fixed assets) |
| Relative surplus population | employment rate, ages 25 to 54; U-6; world vulnerable employment and unemployment; productive employees | BLS, ILO via World Bank, WIOD/OECD/ILO |
| Foreign trade | profits received from the rest of the world; world trade to GDP; net transfer of hours by country and income group | BEA (B933RC, A051RC), World Bank, PWT |
| Share capital and interest-bearing capital | financial profits; net interest and dividends of non-financial corporations; net equity issuance; market value of equities and debt of non-financial corporations relative to GDP | BEA (A587RC, A445RC, B471RC, W326RC, B467RC, A466RC, A455RC), Federal Reserve Z.1 |

**Limitations.** The value of labour power is not observed: the real wage is an indication, not a measure of its distance from value. The intensity of labour, platform work and the extension of the working day beyond paid hours do not yet have indicators. The transfer of hours through foreign trade does not trace intermediate inputs.
