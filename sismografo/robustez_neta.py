"""Robustez de la masa mundial neta de plustrabajo frente a la depreciación de China e India.

La masa neta resta del plusvalor el consumo de capital fijo de las ramas de mercado. China e India pesan dos tercios
de la masa, y su depreciación es la estimación más incierta (Penn World Table: δ·K/Y). Pregunta: ¿el estancamiento de
la masa neta desde 2018 depende de esa estimación?

Variantes (sólo cambia la depreciación de CHN e IND; el resto de los países queda igual):
  - central: PWT 11.0, δ·K/Y;
  - PWT × 0,8 y × 1,2: δ un 20 % menor o mayor;
  - Banco Mundial: consumo de capital fijo en % del INB (NY.ADJ.DKAP.GN.ZS); después del último dato, el último valor;
  - mediana: la mediana de la depreciación/PIB de los demás países medidos ese año;
  - constante desde 2018: la proporción de 2018 se mantiene fija (aísla el efecto de su aumento posterior).
Fórmula, igual que en horas_mundo.py: r = dep/PIB · VA_mercado / v;  e_neta = e − r;
plustrabajo neto = horas · e_neta / (1 + e_neta).
"""
import json, os, urllib.request

import numpy as np, pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(RAIZ, 'datos_cache', 'banco_mundial_cfc.csv')
PAISES = ['CHN', 'IND']


def _banco_mundial():
    url = ('https://api.worldbank.org/v2/country/CHN;IND/indicator/NY.ADJ.DKAP.GN.ZS'
           '?format=json&per_page=500&date=1990:2030')
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            js = json.load(r)[1]
        df = pd.DataFrame([dict(pais=x['countryiso3code'], anio=int(x['date']), cfc_pct_inb=x['value'])
                           for x in js if x['value'] is not None])
        if len(df): df.to_csv(CACHE, index=False)
    except Exception as e:  # noqa: BLE001
        print('Banco Mundial (CFC) sin conexión; uso el caché:', repr(e))
        df = pd.read_csv(CACHE) if os.path.exists(CACHE) else pd.DataFrame()
    return df


def calcular(dir_out, hm):
    from .horas_mundo import CENTRAL
    Q = hm['P'][hm['P'].variante == CENTRAL].copy()
    Q = Q[Q.dep_pib.notna() & Q.r.notna()]
    k = Q.r / Q.dep_pib                                                          # VA_mercado / v por país y año
    bm = _banco_mundial()
    piv = bm.pivot_table(index='anio', columns='pais', values='cfc_pct_inb') / 100 if len(bm) else pd.DataFrame()
    if len(piv): piv = piv.reindex(range(int(piv.index.min()), int(Q.anio.max()) + 1)).ffill()
    med = Q[~Q.pais.isin(PAISES)].groupby('anio').dep_pib.median()
    d18 = Q[Q.anio == 2018].set_index('pais').dep_pib
    def dep_alt(var):
        d = Q.dep_pib.copy()
        m = Q.pais.isin(PAISES)
        if var == 'PWT × 0,8': d[m] = Q.dep_pib[m] * 0.8
        elif var == 'PWT × 1,2': d[m] = Q.dep_pib[m] * 1.2
        elif var == 'Banco Mundial (CFC / INB)' and len(piv):
            d[m] = [piv[c].get(y, np.nan) if c in piv else np.nan for c, y in zip(Q.pais[m], Q.anio[m])]
        elif var == 'Mediana de los demás países': d[m] = Q.anio[m].map(med).values
        elif var == 'Constante desde 2018': d[m & (Q.anio > 2018)] = Q.pais[m & (Q.anio > 2018)].map(d18).values
        return d.fillna(Q.dep_pib)
    filas = []
    for var in ('Central (PWT)', 'PWT × 0,8', 'PWT × 1,2', 'Banco Mundial (CFC / INB)', 'Mediana de los demás países', 'Constante desde 2018'):
        d = dep_alt(var)
        en = Q.e - d * k
        pn = Q.horas_mill * en / (1 + en)
        g = pn.groupby(Q.anio).sum() / 1000
        for y, v in g.items():
            filas.append(dict(variante=var, anio=int(y), plustrabajo_neto_mmh=float(v)))
    R = pd.DataFrame(filas)
    res = []
    for var, g in R.groupby('variante', sort=False):
        s = g.set_index('anio').plustrabajo_neto_mmh
        res.append(dict(variante=var, m2000=s.get(2000), m2018=s.get(2018), mfin=s.iloc[-1], anio_fin=int(s.index[-1]),
                        cambio_2018_fin_pct=(s.iloc[-1] / s.get(2018) - 1) * 100, max_anio=int(s.idxmax()),
                        cambio_2000_2018_pct=(s.get(2018) / s.get(2000) - 1) * 100))
    T = pd.DataFrame(res)
    dch = pd.DataFrame({'pwt': Q[Q.pais.isin(PAISES)].set_index(['pais', 'anio']).dep_pib})
    R.to_csv(os.path.join(dir_out, 'mundo_neta_robustez.csv'), index=False)
    T.to_csv(os.path.join(dir_out, 'mundo_neta_robustez_resumen.csv'), index=False)
    return dict(R=R, T=T, dep=dch, bm=piv)
