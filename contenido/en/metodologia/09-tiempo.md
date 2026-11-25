---
seccion: "09 From money to labour time"
id: tiempo
menu: From money to labour time
---
## From money to labour time

Variant c is used: production and non-supervisory workers in the productive industries, from 1972.

<div class="f">N = Σ productive employment · H = Σ employment × weekly hours × 52</div>

In the macro-monetary reading, v is the wage actually paid. The rate e = pv/v measured in money, net of depreciation (see §4), therefore expresses the ratio between surplus labour and necessary labour in the working day of these workers:

<div class="f">necessary labour = working day / (1 + e) · surplus labour = working day × e / (1 + e)</div>

The working day that is divided is a full-time 40-hour week. The average paid week in the establishment survey (H / N / 52) is not a working day: it averages full-time and part-time work, and it falls mainly because of the composition of employment (41 hours in manufacturing, 24 in leisure and hospitality). Moreover, these are hours paid, not hours worked. The mass of surplus labour uses total hours H, which do not depend on that distinction.

<div class="f">mass of surplus labour (hours) = H × e / (1 + e) = N × hours per worker × e / (1 + e)</div>

The decomposition of the growth of the mass between the first and the last year uses logarithms: each factor contributes ln(factor<sub>end</sub>/factor<sub>start</sub>) / ln(mass<sub>end</sub>/mass<sub>start</sub>). The three contributions sum to 100%.

The **monetary expression of labour time** is (v + pv) / H: the new value, in dollars, that one hour of productive labour represents. It is presented in current dollars and deflated by the GDP deflator.

Assumptions: the value of labour power is approximated by the wage paid; the hours are the paid hours reported by the CES; supervisors in the productive industries are not part of v, and their wages remain within pv.

### Productive forces and disposable time

The module `fuerzas.py` uses the same series to record how much time the development of the productive force frees and what capital turns it into.

- **Necessary time at the 1972 standard of living** (US): 40 × w̃<sub>1972</sub> / μ̃<sub>t</sub>, where w̃ is the real compensation per hour of productive workers (V / H) and μ̃ the real new value per productive hour ((V + S) / H), both with the GDP deflator. These are the weekly hours that would suffice, at each year's productivity, to produce the real wage of 1972.
- **Destination of the time freed** relative to 1972, in a 40-hour working day: more workers' consumption = actual necessary labour − time at the 1972 level; more surplus labour = surplus labour<sub>t</sub> − surplus labour<sub>1972</sub>; reduction of the reference working day = 0. The three parts add up exactly to the time freed.
- **World:** annual hours of productive labour, of surplus labour and of necessary labour (the difference) in the countries measured industry by industry, per inhabitant of those countries (Penn World Table population, extrapolated after its last year with the average growth of the three preceding years), in minutes per day.

**Version 2.** (a) Time at the 1972 standard of living is also calculated with the personal consumption expenditure (PCE) deflator: 40 × w<sub>1972</sub> × (PCE<sub>t</sub>/PCE<sub>1972</sub>) / μ<sub>t</sub>. It gives 6.9 hours in 2025, against 6.8 with the GDP deflator: the division of the time freed barely changes (60% to surplus labour, 40% to consumption). (b) In addition to the legal 40-hour week, the usual week of full-time employees is used (OECD, based on the CPS; from 1979): 41.2 hours in 1979 and 41.0 in 2025. With it, weekly surplus labour rises from 27.8 to 31.1 hours. (c) For the world, one variant adds the hours of employees in public and non-profit education and health, labour that is unproductive for capital but socially necessary: 9 minutes a day per inhabitant in 2025, which take the total from 74 to 83 minutes.

Assumptions and limits: the GDP deflator is not exactly that of the workers' basket (the PCE is used as a check; nor is it the workers' basket, but the consumption of all households); labour productive for capital is not all socially necessary labour (the world variant adds only public education and health; administration, care work, domestic labour and peasant labour are left out); the figures do not estimate the working day of an emancipated society, in which necessary labour would include the common funds for replacement, expansion and services. Results: `fuerzas_eeuu.csv` and `fuerzas_mundo.csv`.
