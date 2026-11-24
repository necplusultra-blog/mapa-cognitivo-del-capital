"""Medición por sección de actividad, después de 2014, para los países sin cuentas por rama de la OCDE.

Fuente: ILOSTAT (encuestas de fuerza de trabajo armonizadas por la OIT), por sección CIIU:
  - asalariados por sección (EES_TEES_SEX_ECO_NB);
  - horas semanales efectivas por sección (HOW_TEMP_SEX_ECO_NB);
  - ingreso medio mensual de los asalariados por sección, en moneda nacional (EAR_EMTA_SEX_ECO_CUR_NB);
  - para China, que no publica asalariados por sección, la ocupación por sección CIIU rev. 3 (EMP_TEMP_SEX_ECO_NB),
    sin la agricultura (véase horas_mundo.py: en China los asalariados se reparten entre las ramas no agrícolas).

Para cada país se usa una sola fuente estadística (la que cubre más años desde 2014), para no mezclar encuestas.
Con el mismo criterio de ramas que en WIOD y la OCDE, se calcula en cada año t:
  ps_t = asalariados productivos / asalariados totales
  hp_t = horas semanales medias de los asalariados de las secciones productivas
  q_t  = masa salarial productiva / masa salarial total (asalariados × ingreso medio por sección)
Las divisiones M69–M70 y M73 no se distinguen en las encuestas: su peso en la sección M (y, en CIIU rev. 3, el
peso de L68, M69–M70 y M73 en la sección K) se toma del propio país en WIOD 2014.

Encadenamiento desde el primer año b ≥ 2014 que cubre la fuente (horas_mundo.combinar_ilo):
  N_t = N^agregado_t × ps_t / ps_b          (N^agregado: extensión agregada de la OIT o, en India, NSS/PLFS)
  h_t = h_b × hp_t / hp_b                   (si hay horas por sección)
  1 + e_t = (1 + e^agregado_t) × q_b / q_t  (si cambia la parte productiva de la masa salarial, cambia v)
"""
import os, urllib.request

import numpy as np, pandas as pd

ILO = 'https://rplumber.ilo.org/data/indicator/?id={id}&ref_area={c}&format=.csv'
IND = {'ees': 'EES_TEES_SEX_ECO_NB_A', 'how': 'HOW_TEMP_SEX_ECO_NB_A', 'ear': 'EAR_EMTA_SEX_ECO_CUR_NB_A', 'emp': 'EMP_TEMP_SEX_ECO_NB_A'}
SECC4 = list('ABCDEFGHIJKLMNOPQRSTU')
SECC3 = list('ABCDEFGHIJKLMNOPQ')
# CIIU rev. 4: circulación G, K (+ parte de M); fuera de la producción capitalista L, O, T, U; públicas P, Q
IMPROD4, FUERA4, PUB4 = ['G', 'K'], ['L', 'O', 'T', 'U'], ['P', 'Q']
# CIIU rev. 3: G comercio, J finanzas (circulación); K inmobiliario y servicios a empresas (parte improductiva);
# L administración pública, P hogares, Q extraterritoriales (fuera); M educación, N salud (públicas)
IMPROD3, FUERA3, PUB3 = ['G', 'J'], ['L', 'P', 'Q'], ['M', 'N']


def _ilo(c, ind, dir_cache):
    fn = os.path.join(dir_cache, f'{ind}_{c}.csv')
    try:
        req = urllib.request.Request(ILO.format(id=ind, c=c), headers={'User-Agent': 'Mozilla/5.0 sismografo-del-capital'})
        with urllib.request.urlopen(req, timeout=120) as r:
            txt = r.read()
        if txt.strip().startswith(b'{'): raise IOError(txt[:100])
        open(fn, 'wb').write(txt)
    except Exception as e:  # noqa: BLE001
        if not os.path.exists(fn): print(f'  OIT {ind} {c}: {e}'); return pd.DataFrame()
    d = pd.read_csv(fn)
    if 'sex' in d: d = d[d.sex == 'SEX_T']
    if 'classif2' in d and d.classif2.notna().any() and ind == IND['ear']: d = d[d.classif2 == 'CUR_TYPE_LCU']
    return d


def _secciones(d, rev):
    pat = r'ECO_ISIC4_[A-U]$' if rev == 4 else r'ECO_ISIC3_[A-Q]$'
    d = d[d.classif1.astype(str).str.match(pat)].copy()
    d['s'] = d.classif1.str[-1]
    return d


def _fuente(d, desde=2014):
    """La fuente con más años ≥ desde; devuelve sus datos."""
    if d.empty: return d
    cob = d[d.time >= desde].groupby('source').time.nunique()
    if cob.empty: return d.iloc[0:0]
    return d[d.source == cob.idxmax()]


def _pesos_wiod(wiod, c):
    """Peso de las divisiones improductivas dentro de M (rev. 4) y de K (rev. 3) en WIOD 2014 (empleo)."""
    try:
        e = wiod['EMPE'].loc[c][2014] if wiod['EMPE'].loc[c][2014].sum() > 0 else wiod['EMP'].loc[c][2014]
        m = e.reindex(['M69_M70', 'M71', 'M72', 'M73', 'M74_M75']).fillna(0)
        k = e.reindex(['L68', 'M69_M70', 'M71', 'M72', 'M73', 'M74_M75', 'N']).fillna(0)
        return float((m['M69_M70'] + m['M73']) / m.sum()), float((k['L68'] + k['M69_M70'] + k['M73']) / k.sum())
    except Exception:  # noqa: BLE001
        return 0.3, 0.4


def indicadores(c, wiod, dir_cache, publicas_productivas=True):
    """Serie anual (≥ 2014) de ps, hp y q para un país; DataFrame vacío si no hay datos por sección."""
    china = c == 'CHN'
    rev = 3 if china else 4
    base = _secciones(_ilo(c, IND['emp'] if china else IND['ees'], dir_cache), rev)
    base = _fuente(base)
    if base.empty: return pd.DataFrame()
    fM, fK = _pesos_wiod(wiod, c)
    if rev == 4:
        improd, fuera, pub, parcial, f = IMPROD4, FUERA4, PUB4, 'M', fM
    else:
        improd, fuera, pub, parcial, f = IMPROD3, FUERA3, PUB3, 'K', fK
    improd = improd + fuera + ([] if publicas_productivas else pub)
    N = base.pivot_table(index='time', columns='s', values='obs_value', aggfunc='mean')
    if china: N = N.drop(columns=['A'], errors='ignore')               # agricultura: trabajo familiar
    # peso productivo de cada sección (1, 0, o 1 − f para la sección parcial)
    peso = pd.Series({s: (0.0 if s in improd else 1.0) for s in N.columns})
    if parcial in peso.index: peso[parcial] = 1 - f
    tot = N.sum(axis=1)
    out = pd.DataFrame({'ps': (N * peso).sum(axis=1) / tot, 'fuente_secciones': base.source.iloc[0]})
    # horas por sección (rev. 4, misma fuente si existe)
    how = _secciones(_ilo(c, IND['how'], dir_cache), 4) if not china else pd.DataFrame()
    if not how.empty:
        how = how[how.source == base.source.iloc[0]] if (how.source == base.source.iloc[0]).any() else _fuente(how)
        Hs = how.pivot_table(index='time', columns='s', values='obs_value', aggfunc='mean').reindex(columns=N.columns)
        w = (N * peso).reindex(Hs.index)
        hp = (Hs * w).sum(axis=1, min_count=1) / w.where(Hs.notna()).sum(axis=1)
        out['hp'] = hp.reindex(out.index)
    # masa salarial por sección (rev. 4)
    ear = _secciones(_ilo(c, IND['ear'], dir_cache), 4) if not china else pd.DataFrame()
    if not ear.empty:
        ear = ear[ear.source == base.source.iloc[0]] if (ear.source == base.source.iloc[0]).any() else _fuente(ear)
        W = ear.pivot_table(index='time', columns='s', values='obs_value', aggfunc='mean').reindex(columns=N.columns)
        masa = (N.reindex(W.index) * W)
        ok = masa.notna().sum(axis=1) >= 0.8 * len(N.columns)
        q = (masa * peso).sum(axis=1) / masa.sum(axis=1)
        out['q'] = q.where(ok).reindex(out.index)
    out = out[out.index >= 2014]
    return out
