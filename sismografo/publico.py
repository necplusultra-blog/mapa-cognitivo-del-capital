"""Parte de la educación y la salud (secciones P y Q) que no es producción capitalista.

Criterio (decisión del autor): el trabajo pagado con plusvalor apropiado por el Estado mediante impuestos es
improductivo, aunque produzca valores de uso; lo mismo el de las instituciones sin fines de lucro, cuyo salario no es
capital que se valoriza. En cambio, el trabajo asalariado por empresas estatales que venden mercancías con fines de
lucro es productivo: su salario es capital adelantado por el Estado como capitalista.

Proporción no capitalista de P + Q, por país y año:
  g = (ocupados del gobierno general S13 + ocupados de las instituciones sin fines de lucro S15 − ocupados de O) / ocupados de P + Q
con tope entre 0 y 1 (OCDE: empleo por sector institucional y tabla 7). La administración pública (O) es casi toda
gobierno; el resto del empleo público y sin fines de lucro se concentra en educación, salud y asistencia social. Como S15
incluye también organizaciones religiosas y civiles (sección S), g tiende a sobrestimarse un poco.
Fuera de la OCDE: encuestas de empleo público por actividad de la OIT (EMP_PUBL_SEX_ECO_NB), cuando dan una proporción
plausible (entre 0,2 y 1); si no, la mediana de los países medidos. Antes del primer año con dato se mantiene ese dato.
"""
import os
import numpy as np, pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _ocde(dir_datos):
    fs = os.path.join(dir_datos, 'ocde', 'ocde_sectores.csv'); f7 = os.path.join(dir_datos, 'ocde', 'ocde_t7.csv')
    if not (os.path.exists(fs) and os.path.exists(f7)): return {}
    S = pd.read_csv(fs); T = pd.read_csv(f7)
    S = S[S.UNIT_MEASURE == 'PS'].pivot_table(index=['REF_AREA', 'TIME_PERIOD'], columns='SECTOR', values='OBS_VALUE', aggfunc='first')
    T = T[(T.TRANSACTION == 'EMP') & (T.UNIT_MEASURE == 'PS')].pivot_table(index=['REF_AREA', 'TIME_PERIOD'], columns='ACTIVITY', values='OBS_VALUE', aggfunc='first')
    out = {}
    for c in sorted(set(S.index.get_level_values(0)) & set(T.index.get_level_values(0))):
        s, t = S.loc[c], T.loc[c]
        if 'S13' not in s or not {'O', 'P', 'Q'} <= set(t.columns): continue
        # misma escala: S y T pueden venir en miles o en unidades; se normaliza con el total S1 / _T
        esc = (s['S1'] / t['_T']).median() if 'S1' in s and '_T' in t else 1.0
        g = ((s['S13'] + s.get('S15', 0).fillna(0)) / esc - t['O']) / (t['P'] + t['Q'])
        g = g.dropna().clip(0, 1)
        if len(g): out[c] = g
    return out


def _ilo(paises):
    from sismografo.ilo_ramas import _ilo as ilo, _secciones
    cache = os.path.join(RAIZ, 'datos_cache', 'ilo'); os.makedirs(cache, exist_ok=True)
    out = {}
    for c in paises:
        pub = ilo(c, 'EMP_PUBL_SEX_ECO_NB_A', cache); tot = ilo(c, 'EMP_TEMP_SEX_ECO_NB_A', cache)
        if pub.empty or tot.empty: continue
        for rev, ss in ((4, ('P', 'Q')), (3, ('M', 'N'))):
            a, b = _secciones(pub, rev), _secciones(tot, rev)
            if a.empty or b.empty: continue
            a = a.groupby(['time', 's']).obs_value.first().unstack(); b = b.groupby(['time', 's']).obs_value.first().unstack()
            if not set(ss) <= set(a.columns) & set(b.columns): continue
            g = ((a[ss[0]] + a[ss[1]]) / (b[ss[0]] + b[ss[1]])).dropna()
            g = g[(g >= 0.2) & (g <= 1)]
            if len(g): out[c] = pd.concat([out.get(c, pd.Series(dtype=float)), g]).groupby(level=0).mean()
    return out


def proporciones(dir_datos, paises, anios):
    """DataFrame (pais × anio) con g y la fuente de cada país."""
    O = _ocde(dir_datos)
    I = _ilo([c for c in paises if c not in O])
    filas = []
    med = float(np.nanmedian([s.median() for s in list(O.values()) + list(I.values())])) if (O or I) else 0.6
    for c in paises:
        if c in O: s, fuente = O[c], 'OCDE (sectores institucionales)'
        elif c in I: s, fuente = I[c], 'OIT (empleo público por actividad)'
        else: s, fuente = pd.Series({2014: med}), 'mediana de los países medidos'
        s.index = s.index.astype(int)
        s = s.reindex(sorted(set(s.index) | set(anios))).interpolate(limit_area='inside').bfill().ffill()
        for y in anios: filas.append(dict(pais=c, anio=int(y), g=float(s[y]), fuente_g=fuente))
    return pd.DataFrame(filas)


def variante_privada(P, G, nombre, var_prod, var_fuera):
    """Combina las variantes «productivas» y «fuera» en proporción a la parte capitalista (1 − g) de P y Q. Las
    horas necesarias, las de plustrabajo (bruto y neto), los obreros y las horas son sumas por sección, así que la
    combinación lineal reproduce la medición con sólo la parte capitalista de P y Q."""
    a = P[P.variante == var_prod].set_index(['pais', 'anio']); b = P[P.variante == var_fuera].set_index(['pais', 'anio'])
    idx = a.index.intersection(b.index); a, b = a.loc[idx], b.loc[idx]
    s = 1 - G.set_index(['pais', 'anio']).g.reindex(idx).fillna(G.g.median())
    def comb(x, y): return y + s * (x - y)
    nec = comb(a.horas_mill / (1 + a.e), b.horas_mill / (1 + b.e))
    plus = comb(a.horas_mill * a.e / (1 + a.e), b.horas_mill * b.e / (1 + b.e))
    en_a, en_b = a.e - a.r, b.e - b.r
    plusn = comb(a.horas_mill * en_a / (1 + en_a), b.horas_mill * en_b / (1 + en_b))
    N = comb(a.obreros_mill, b.obreros_mill); H = nec + plus
    X = a.copy()
    X['variante'] = nombre; X['obreros_mill'] = N; X['horas_mill'] = H; X['e'] = plus / nec
    X['r'] = X['e'] - plusn / (H - plusn)
    X['g_publico'] = 1 - s
    return X.reset_index()
