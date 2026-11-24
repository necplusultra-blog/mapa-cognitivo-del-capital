"""Masa mundial de plusvalor en horas de trabajo (WIOD, Cuentas Socioeconómicas 2016; 43 países, 2000–2014).

Mismo criterio por ramas que en EE.UU. (véase site/metodologia.html, §3):
- improductivas por circulación: comercio (G45–G47), finanzas y seguros (K64–K66), servicios jurídicos,
  contables y de dirección (M69_M70), publicidad (M73);
- fuera de la producción capitalista: inmobiliario (L68, renta), administración pública (O84),
  hogares empleadores (T), organismos extraterritoriales (U);
- educación (P85) y salud (Q): dos variantes, porque en muchos países son mayoritariamente públicas
  (trabajo intercambiado por rédito).
Para cada país: v = remuneración de los asalariados de las ramas productivas; pv = valor agregado (bruto) de
las ramas de mercado − ingreso laboral imputado a los trabajadores por cuenta propia (LAB − COMP: no son
asalariados del capital) − v; e = pv/v; N = asalariados productivos; H = sus horas. Plustrabajo = H·e/(1+e).
China no informa asalariados ni horas en WIOD: se estiman con la participación de asalariados de la OIT
(estimaciones modeladas) y una jornada anual supuesta; por eso hay una variante sin China.
"""
import json, os, urllib.request
import numpy as np, pandas as pd

CIRCULACION = ['G45', 'G46', 'G47', 'K64', 'K65', 'K66', 'M69_M70', 'M73']
FUERA = ['L68', 'O84', 'T', 'U']
PUBLICAS = ['P85', 'Q']
HORAS_CHINA = 46 * 50   # horas anuales por asalariado (supuesto explícito: 46 h semanales, 50 semanas)
CACHE_ILO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datos_cache', 'ilo_chn_asalariados.csv')


def _ilo_china():
    url = 'https://rplumber.ilo.org/data/indicator/?id=EMP_2EMP_SEX_STE_NB_A&ref_area=CHN&sex=SEX_T&format=.csv'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 sismografo-del-capital'})
        with urllib.request.urlopen(req, timeout=90) as r:
            open(CACHE_ILO, 'wb').write(r.read())
    except Exception as e:  # noqa: BLE001
        print('OIT: se usa la copia guardada', e)
    d = pd.read_csv(CACHE_ILO)
    d = d[d.sex == 'SEX_T'].pivot_table(index='time', columns='classif1', values='obs_value')
    return d['STE_AGGREGATE_EES'] / d['STE_AGGREGATE_TOTAL']


def calcular(dir_datos, dir_out):
    fn = os.path.join(dir_datos, 'wiod', 'Socio_Economic_Accounts.xlsx')
    if not os.path.exists(fn):
        fn = os.path.join(os.path.dirname(CACHE_ILO), 'wiod_sea.xlsx')
    d = pd.read_excel(fn, sheet_name='DATA', engine='calamine')
    yc = [c for c in d.columns if str(c).isdigit()]
    d = d.rename(columns={c: int(c) for c in yc}); Y = [int(c) for c in yc]
    piv = {v: d[d.variable == v].set_index(['country', 'code'])[Y] for v in ('VA', 'COMP', 'LAB', 'EMPE', 'H_EMPE', 'EMP')}
    paises = sorted(d.country.unique())
    share_chn = _ilo_china()
    filas, excluidos = [], []
    for variante, publicas_prod in (('educación y salud productivas', True), ('educación y salud fuera', False)):
        improd = CIRCULACION + FUERA + ([] if publicas_prod else PUBLICAS)
        fuera = FUERA + ([] if publicas_prod else PUBLICAS)
        for c in paises:
            codes = piv['VA'].loc[c].index
            prod = [k for k in codes if k not in improd]
            mercado = [k for k in codes if k not in fuera]
            for y in Y:
                s = float(share_chn.get(y, np.nan)) if c == 'CHN' else 1.0   # China: COMP incluye a los no asalariados
                comp = lambda ks: piv['COMP'].loc[c].loc[ks, y].sum() * s
                v = comp(prod)
                cuenta_propia = piv['LAB'].loc[c].loc[mercado, y].sum() - comp(mercado)
                pv = piv['VA'].loc[c].loc[mercado, y].sum() - cuenta_propia - v
                if c == 'CHN':
                    N = piv['EMP'].loc[c].loc[prod, y].sum() * s
                    H = N * HORAS_CHINA / 1000   # N en miles → millones de horas
                    estimado = True
                else:
                    N = piv['EMPE'].loc[c].loc[prod, y].sum(); H = piv['H_EMPE'].loc[c].loc[prod, y].sum(); estimado = False
                if not (v > 0 and N > 0 and H > 0): continue
                e = pv / v
                if not 0 < e < 8:   # datos anómalos (p. ej. Taiwán en algunos años): se excluyen y se registran
                    excluidos.append(dict(variante=variante, pais=c, anio=y, e=round(float(e), 3))); continue
                filas.append(dict(variante=variante, pais=c, anio=y, obreros_mill=N / 1000, horas_mill=H, e=e,
                                  plustrabajo_mill_h=H * e / (1 + e), necesario_mill_h=H / (1 + e), china_estimada=estimado))
    P = pd.DataFrame(filas); P['extension'] = False
    try:
        X = extender(P)
        if not X.empty: P = pd.concat([P, X], ignore_index=True)
    except Exception as e:  # noqa: BLE001
        print('Extensión OIT omitida:', repr(e))
    P.to_csv(os.path.join(dir_out, 'mundo_horas_paises.csv'), index=False)
    pd.DataFrame(excluidos).to_csv(os.path.join(dir_out, 'mundo_horas_excluidos.csv'), index=False)
    agg = []
    for (var, y), g in P.groupby(['variante', 'anio']):
        for etiqueta, gg in (('con China', g), ('sin China', g[g.pais != 'CHN'])):
            H, Sp = gg.horas_mill.sum(), gg.plustrabajo_mill_h.sum()
            agg.append(dict(variante=var, china=etiqueta, anio=int(y), paises=len(gg), extension=bool(g.extension.any()), obreros_mill=gg.obreros_mill.sum(),
                            plustrabajo_mmh=Sp / 1000, e_horas=Sp / (H - Sp), semana_horas=H / gg.obreros_mill.sum() / 52,
                            pct_china=float(g.loc[g.pais == 'CHN', 'plustrabajo_mill_h'].sum() / g.plustrabajo_mill_h.sum() * 100)))
    A = pd.DataFrame(agg)
    A.to_csv(os.path.join(dir_out, 'mundo_horas.csv'), index=False)
    return dict(A=A, P=P, excluidos=excluidos)


# ---------------------------------------------------------------------------------------------------------
# Extensión 2015–2025 con la OIT (ILOSTAT). Método de encadenamiento a partir de 2014 (último año WIOD):
#   e_i(t)  = e_i(2014) × [ (1−LS_i,t)/LS_i,t ] / [ (1−LS_i,2014)/LS_i,2014 ]      LS: participación del trabajo (OIT, ODS 10.4.1)
#   N_i(t)  = N_i(2014) × asalariados totales_t / _2014                           (OIT, estimaciones modeladas armonizadas;
#                                                                                 la proporción productiva de 2014 se mantiene)
#   h_i(t)  = h_i(2014) × horas semanales por ocupado_t / _2014                   (OIT; si falta, constante)
#   plustrabajo_i(t) = N_i(t) · h_i(t) · e_i(t)/(1+e_i(t))
# ---------------------------------------------------------------------------------------------------------
ILO = 'https://rplumber.ilo.org/data/indicator/?id={id}&ref_area={c}&format=.csv'
ILO_IND = {'ls': 'LAP_2GDP_NOC_RT_A', 'ees': 'EES_TEES_SEX_ECO_NB_A', 'ees_mod': 'EMP_2EMP_SEX_STE_NB_A', 'hrs': 'HOW_TEMP_SEX_ECO_NB_A'}
SECC_IMPROD = {'G', 'K', 'L', 'O', 'T', 'U'}
# Las series por sección de la OIT combinan encuestas con quiebres (p. ej. Reino Unido, Corea, India): por defecto
# se usa la serie armonizada de asalariados totales estimada por la OIT, que conserva la proporción productiva de 2014.
SECCIONES = False
SECC_PUBLICAS = {'P', 'Q'}


def _ilo(c, ind, dir_cache):
    fn = os.path.join(dir_cache, f'{ind}_{c}.csv')
    try:
        req = urllib.request.Request(ILO.format(id=ind, c=c), headers={'User-Agent': 'Mozilla/5.0 sismografo-del-capital'})
        with urllib.request.urlopen(req, timeout=90) as r:
            txt = r.read()
        if txt.strip().startswith(b'{'): raise IOError(txt[:100])
        open(fn, 'wb').write(txt)
    except Exception as e:  # noqa: BLE001
        if not os.path.exists(fn): print(f'  OIT {ind} {c}: {e}'); return pd.DataFrame()
    d = pd.read_csv(fn)
    if 'sex' in d: d = d[d.sex == 'SEX_T']
    return d


def _serie_anual(s, anios):
    s = s.groupby(level=0).mean().sort_index()
    return s.reindex(sorted(set(s.index) | set(anios))).interpolate(limit_area='inside').ffill().reindex(anios)


def extender(P, hasta=2025):
    dir_cache = os.path.join(os.path.dirname(CACHE_ILO), 'ilo'); os.makedirs(dir_cache, exist_ok=True)
    base = int(P.anio.max()); anios = list(range(base, hasta + 1)); filas = []
    for c in sorted(P.pais.unique()):
        ls = _ilo(c, ILO_IND['ls'], dir_cache)
        if ls.empty: continue
        LS = _serie_anual(ls.set_index('time')['obs_value'] / 100, anios)
        if LS.isna().all(): continue
        odds = (1 - LS) / LS
        ees = _ilo(c, ILO_IND['ees'], dir_cache); mod = _ilo(c, ILO_IND['ees_mod'], dir_cache); hrs = _ilo(c, ILO_IND['hrs'], dir_cache)
        tot_mod = _serie_anual(mod[mod.classif1 == 'STE_AGGREGATE_EES'].set_index('time')['obs_value'], anios) if not mod.empty else None
        h = None
        if not hrs.empty:
            hh = hrs[hrs.classif1.isin(['ECO_SECTOR_TOTAL', 'ECO_AGGREGATE_TOTAL'])]
            if not hh.empty:
                h = _serie_anual(hh.groupby('time')['obs_value'].mean(), anios)
                if h.isna().any(): h = None
        for variante, publicas_prod in (('educación y salud productivas', True), ('educación y salud fuera', False)):
            b = P[(P.pais == c) & (P.variante == variante) & (P.anio == base)]
            if b.empty: continue
            b = b.iloc[0]
            improd = SECC_IMPROD | (set() if publicas_prod else SECC_PUBLICAS)
            N_idx, fuente_n = None, 'constante'
            if SECCIONES and not ees.empty and c != 'CHN':
                secc = ees[ees.classif1.str.match(r'ECO_ISIC4_[A-U]$')].copy()
                # una sola fuente estadística (evita quiebres al cambiar de encuesta): la que cubre el año base
                # y más años posteriores; si ninguna cubre el año base, se usa la serie modelada
                if not secc.empty:
                    cob = secc.groupby('source').time.agg(lambda t: (base in set(t), (t > base).sum()))
                    validas = [k for k, (tiene_base, n) in cob.items() if tiene_base and n > 0]
                    secc = secc[secc.source == max(validas, key=lambda k: cob[k][1])] if validas else secc.iloc[0:0]
                if not secc.empty:
                    secc['s'] = secc.classif1.str[-1]
                    prod = secc[~secc.s.isin(improd)].groupby('time')['obs_value'].sum()
                    prod = prod[prod > 0]
                    if base in prod.index or len(prod) > 1:
                        serie = _serie_anual(prod, anios)
                        if serie.notna().all() and serie[base] > 0:
                            N_idx, fuente_n = serie / serie[base], 'OIT por sección'
            if N_idx is None and tot_mod is not None and tot_mod.notna().all():
                N_idx, fuente_n = tot_mod / tot_mod[base], 'OIT modelada (asalariados totales)'
            if N_idx is None: N_idx = pd.Series(1.0, index=anios)
            h_idx = (h / h[base]) if h is not None else pd.Series(1.0, index=anios)
            for y in anios[1:]:
                e = b.e * odds[y] / odds[base]
                N = b.obreros_mill * N_idx[y]; H = b.horas_mill * N_idx[y] * h_idx[y]
                filas.append(dict(variante=variante, pais=c, anio=y, obreros_mill=N, horas_mill=H, e=e,
                                  plustrabajo_mill_h=H * e / (1 + e), necesario_mill_h=H / (1 + e),
                                  china_estimada=c == 'CHN', extension=True, fuente_obreros=fuente_n,
                                  fuente_horas='OIT' if h is not None else 'constante'))
    return pd.DataFrame(filas)
