"""Estimación trimestral («nowcast») de la tasa de ganancia corporativa de EE.UU.

Numerador: ganancias trimestrales de NIPA 1.14 (tasa anual desestacionalizada). Denominador: stock neto de
capital fijo a costo corriente (activos fijos del BEA, fin de año), interpolado linealmente por trimestre y,
después del último año publicado, extrapolado con el crecimiento del último año. Los trimestres con K
extrapolado se marcan como provisionales.
"""
import csv, collections, os
import pandas as pd

SERIES = {  # nombre: (ganancia trimestral, stock de capital)
    'nfc_ebe': ('W326RC', 'k1pnofi2es00'), 'nfc_despues_imp': ('W328RC', 'k1pnofi2es00'),
    'corp_ebe': ('W322RC', 'k1ptotl2es00'),
}


def _q(fn):
    d = collections.defaultdict(dict)
    with open(fn) as f:
        r = csv.reader(f); next(r)
        for code, per, val in r:
            if 'Q' in per:
                try: d[code][per] = float(val.replace(',', ''))
                except ValueError: pass
    return d


def calcular(dir_datos, dir_out, F):
    Q = _q(os.path.join(dir_datos, 'bea', 'NipaDataQ.txt'))
    out = {}
    for nombre, (pc, kc) in SERIES.items():
        p = pd.Series(Q[pc]); p.index = pd.PeriodIndex(p.index, freq='Q'); p = p.sort_index()
        p = p[p.index >= pd.Period('1960Q1')]
        K = pd.Series(F[kc]).sort_index(); last = int(K.index.max()); g = K[last] / K[last - 1]
        def kq(per):
            y, q = per.year, per.quarter
            kv = lambda yy: K[yy] if yy <= last else K[last] * g ** (yy - last)
            return kv(y - 1) + (kv(y) - kv(y - 1)) * q / 4
        r = pd.Series([p[i] / kq(i) for i in p.index], index=p.index)
        out[nombre] = r * 100
    df = pd.DataFrame(out).round(3)
    df['provisional'] = [i.year > max(int(max(F[k])) for _, k in SERIES.values()) for i in df.index]
    df.index = df.index.astype(str); df.index.name = 'trimestre'
    df.to_csv(os.path.join(dir_out, 'eeuu_trimestral.csv'))
    return df
