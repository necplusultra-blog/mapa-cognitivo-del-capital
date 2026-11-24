"""Auditoría, bloque B: supuestos del plusvalor que deben explicitarse. Se calculan como sensibilidad; la medición
central no cambia hasta que el autor decida.

B4 — Explotación secundaria (finanzas). El valor agregado de las finanzas entra en el plusvalor, pero la parte que
     pagan los hogares por servicios financieros (intereses implícitos —FISIM— y comisiones) sale del salario y de
     otros ingresos, no del trabajo productivo: es una deducción del ingreso, no plusvalor producido. Variante: se
     resta del plusvalor el consumo de servicios financieros de los hogares.
       EE.UU.: gasto de consumo personal en servicios financieros (NIPA 2.4.5, DFNLRC = FISIM + comisiones).
       Mundo:  consumo final de los hogares de productos K64–K66 (WIOD, nacional e importado).
     Es una cota superior: también pagan servicios financieros los hogares capitalistas.
B3 — Renta comercial (mundo). El inmobiliario (L68) queda fuera del plusvalor, pero la renta que los capitales de las
     ramas de mercado pagan por locales y oficinas es plusvalor cedido a la propiedad territorial. Variante: se suma el
     consumo intermedio de productos L68 por las ramas de mercado (WIOD). En EE.UU. ya está dentro: el plusvalor del
     sector empresarial incluye el inmobiliario comercial y excluye sólo la vivienda.
     Después de 2014 (sin tablas WIOD) se mantiene la proporción de 2014 de cada país.
B2 — Supervisión y dirección. EE.UU. ofrece las dos cotas: por ramas (todos los asalariados de las ramas
     productivas, supervisores y gerentes incluidos, cuentan en v) e intra-rama (sólo obreros de producción y no
     supervisores; los sueldos de supervisión quedan en el plusvalor). Se registra la parte de la remuneración de
     las ramas productivas que corresponde a supervisores y gerentes. En el mundo sólo existe la cota por ramas.
"""
import os

import numpy as np, pandas as pd

FIN = ['K64', 'K65', 'K66']
FUERA = ['L68', 'O84', 'T', 'U']


def _eeuu(ee, dir_datos):
    from .eeuu import Datos
    D = Datos(dir_datos)
    fh = D.s('N', 'DFNLRC')                                                     # servicios financieros de los hogares
    out = {}
    for prod in ('b', 'c'):
        S, K, V = ee['SK'][f'B|{prod}|cc|neta|ppi-incl|K-todo|noutil']
        S, K, V = (x.reindex(fh.index) for x in (S, K, V))
        out[f'e_{prod}'] = S / V
        out[f'e_{prod}_b4'] = (S - fh) / V
        out[f'r_{prod}'] = S / (K + V) * 100
        out[f'r_{prod}_b4'] = (S - fh) / (K + V) * 100
        out[f'fin_hogares_pct_pv_{prod}'] = fh / S * 100
    Vb = ee['SK']['B|b|cc|neta|ppi-incl|K-todo|noutil'][2]; Vc = ee['SK']['B|c|cc|neta|ppi-incl|K-todo|noutil'][2]
    out['supervision_pct_v_ramas'] = (1 - Vc / Vb) * 100
    E = pd.DataFrame(out); E.index.name = 'anio'
    E.loc[E.index < 1972, [c for c in E.columns if c.endswith(('_c', '_c_b4')) or c in ('supervision_pct_v_ramas', 'fin_hogares_pct_pv_c')]] = np.nan
    c = ee['masa']['c']
    H = c['horas_productivas_mill']
    E['plustrabajo_mmh_c'] = H * E['e_c'] / (1 + E['e_c']) / 1000
    E['plustrabajo_mmh_c_b4'] = H * E['e_c_b4'] / (1 + E['e_c_b4']) / 1000
    return E


def _cuotas_wiod():
    """Por país y año (2000–2014): renta pagada por las ramas de mercado y servicios financieros de los hogares,
    como proporción del valor agregado de las ramas de mercado (dólares corrientes, WIOD)."""
    from .transformacion import RAMAS, _leer_niots, ZIP
    if not os.path.exists(ZIP): return pd.DataFrame()
    mercado = [r for r in RAMAS if r not in FUERA]
    filas = []
    for c, d in _leer_niots().items():
        for y in sorted(d.anio.dropna().unique()):
            t = d[d.anio == y]
            uso = t[t.origen.isin(['Domestic', 'Imports'])]
            tot = t[t.origen == 'TOT'].set_index('code')
            va = pd.to_numeric(tot.loc['VA', mercado], errors='coerce').sum()
            if not va > 0: continue
            renta = pd.to_numeric(uso[uso.code == 'L68'][mercado].stack(), errors='coerce').sum()
            fin = pd.to_numeric(uso[uso.code.isin(FIN)]['CONS_h'], errors='coerce').sum()
            filas.append(dict(pais=c, anio=int(y), renta_pct_va=renta / va, fin_hogares_pct_va=fin / va))
    return pd.DataFrame(filas)


def _mundo(hm):
    from .horas_mundo import CENTRAL
    Q = hm['P'][hm['P'].variante == CENTRAL].copy()
    W = _cuotas_wiod()
    if W.empty: return pd.DataFrame(), W
    W = W.set_index(['pais', 'anio'])
    ult = W.reset_index().sort_values('anio').groupby('pais').last()            # proporción del último año WIOD
    def cuota(r, k):
        try: return W.loc[(r.pais, r.anio), k]
        except KeyError: return ult[k].get(r.pais, np.nan)
    Q['b3'] = Q.apply(lambda r: cuota(r, 'renta_pct_va'), axis=1)
    Q['b4'] = Q.apply(lambda r: cuota(r, 'fin_hogares_pct_va'), axis=1)
    k = 1 + Q.e + Q.cp_v                                                         # VA de mercado / v
    filas = []
    for nombre, ajuste in (('base', 0), ('B3: + renta comercial', Q.b3.fillna(0)), ('B4: − servicios financieros de los hogares', -Q.b4.fillna(0)),
                           ('B3 y B4', Q.b3.fillna(0) - Q.b4.fillna(0))):
        e2 = (Q.e + ajuste * k).clip(lower=0)
        Q['_pl'] = Q.horas_mill * e2 / (1 + e2)
        g = Q.groupby('anio').agg(pl=('_pl', 'sum'), h=('horas_mill', 'sum'))
        for y, r in g.iterrows():
            filas.append(dict(anio=int(y), variante=nombre, plustrabajo_mmh=r.pl / 1000, e_horas=r.pl / (r.h - r.pl)))
    return pd.DataFrame(filas), W.reset_index()


def calcular(dir_datos, dir_out, ee, hm=None):
    E = _eeuu(ee, dir_datos)
    E.to_csv(os.path.join(dir_out, 'bloque_b_eeuu.csv'))
    M, W = (_mundo(hm) if hm is not None else (pd.DataFrame(), pd.DataFrame()))
    if not M.empty:
        M.to_csv(os.path.join(dir_out, 'bloque_b_mundo.csv'), index=False)
        W.to_csv(os.path.join(dir_out, 'bloque_b_cuotas_wiod.csv'), index=False)
    return dict(E=E, M=M, W=W)
