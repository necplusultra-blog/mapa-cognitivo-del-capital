---
seccion: "06b Replication of the authors' series"
id: replicacion
menu: Replication of the authors' series
---
## Replication of the authors' series

The five rates ‘in the manner of’ the authors (previous §) share a common definition so that they can be read together. The replication does the opposite: it rebuilds each series with the definition its author published, using current BEA data, and contrasts it with the values the author reported. The module is `sismografo/replicacion.py`; the results are in `replicacion_series.csv`, `replicacion_contraste.csv` and `replicacion_tendencias.csv` (downloads).

The gap between the published and the rebuilt figures has two sources that cannot be fully separated: the revisions of the accounts (intellectual property enters capital in 1999 — software — and in 2013 — R&D and artistic originals —; the 2023 comprehensive revision corrected compensation, profits and stocks) and whatever the reconstruction does not reproduce of each author's method. That is why the criterion is not to hit their numbers, but to check whether the trends on which each reading builds its diagnosis still appear.

| Author | Published values contrasted | Rebuilt definition |
|---|---|---|
| Shaikh and Tonak (1994) | S\*/V\* and Marxian rate S\*/K\*, 1948–1989 (tables 5.6 and 5.8) | S\* = business net product excluding rented housing − V\*; V\* = compensation of production and non-supervisory workers in the productive industries (from 1972). From 1948, lower bound using all the compensation in those industries. K = net stock (theirs: gross) |
| Moseley (1991; 1997) | S/V, C/V, Uf/V, Us/V and conventional rate in 1977 | V = production and non-supervisory wages in productive industries; Uf = rest of business compensation; C = productive fixed capital + inventories; Us = fixed capital in trade, finance, non-residential real estate, rental and leasing, and legal services; S excluding the business sector's taxes on production net of subsidies |
| Kliman (2010; 2012) | Profit before tax / assets at historical cost, 1978 and 2001 | Corporations; depreciation at historical cost instead of current cost; denominator = net stock at historical cost at the close of the previous year. Also property income and total profit |
| Duménil and Lévy (2002) | Ratios 1982/1948, 2000/1982 and 2000/1948 of the broad rate r_b of corporations (table 3) | (net value added − compensation) / non-residential net stock at current cost; variant without intellectual property |
| Roberts (2018; 2021) | Change 1965–1982 and 1982–1997 in his ‘whole economy’ rate | (national income − compensation) / (private non-residential fixed assets + compensation), at historical and current cost |

**Results.** The following are reproduced: Shaikh and Tonak's rate of surplus value with V\* of production workers (1975–1982, differences below 0.08; in 1985–1989 the rebuilt rate lies between 0.15 and 0.17 above), the trend of their Marxian rate (changes 1975–1982 and 1982–1989 close to the published ones; the level is higher because the net stock is smaller than the gross stock), Moseley's Uf/V ratio in 1977, Kliman's before-tax rate in 1978 and, approximately, in 2001, and the changes in Roberts's rate that he published in 2018 (those of 2021, with a larger 1982–1997 recovery, are approximated less well). Duménil and Lévy's fall from 1948 to 1982 is approximated; their recovery from 1982 to 2000 (+45%) is not: with today's data it is much smaller, with or without intellectual property. Moseley's conventional rate is approximated only under our reading of his identity (S excluding indirect taxes, C including inventories), which the published text does not make explicit.

**Limits.** Shaikh and Tonak's and Moseley's rates of surplus value cannot be rebuilt before 1972, because the wages of production workers by supersector (BLS CES) begin that year; for 1948–1971 there is only the lower bound by industry. Duménil and Lévy impute a compensation to the labour of non-employees in the business sector; here only their corporate sector is replicated, where that imputation is unnecessary. None of the replications incorporates secondary exploitation (B4), because none of the authors deducts it: these are their definitions, not the cognitive map's.
