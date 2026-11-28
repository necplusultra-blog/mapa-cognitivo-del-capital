"""China por rama después de 2014 (F3d v3): empleo y remuneración por rama de la OCDE (Trade in Employment, TiM 2025).

Fuente: OCDE, TiM edición 2025 (dataflow OECD.STI.PIE DSD_TIM_2025@DF_TIM_2025), coherente con las tablas mundiales
ICIO: ocupados (EMPN), remuneración del trabajo (LABR, en dólares) y su proporción del valor agregado (de la que se
obtiene el valor agregado), por rama, 2000–2022. Copia en datos_cache/ocde_tim_2025.csv.gz.

Para China, la remuneración de TiM es el ingreso del trabajo completo (incluye el de los trabajadores por cuenta
propia: en la agricultura supera el valor agregado), como en WIOD. Se aplica el mismo método que con WIOD:
  s_t      = asalariados OIT_t / (ocupación OIT_t × (1 − peso agrícola de la ocupación TiM_t)), con tope 1;
             la agricultura no tiene asalariados (agricultura familiar)
  v_t      = Σ_productivas LABR · s
  pv_t     = Σ_mercado (VA − LABR)        (se excluye todo el ingreso del trabajo, asalariado y por cuenta propia)
  e_t      = pv_t / v_t
Mismo criterio de ramas: circulación G, K y la parte de M que corresponde a servicios jurídicos, contables y
publicidad (su peso en WIOD 2014); fuera de la producción capitalista L, O, T; educación y salud (P, Q) en dos
variantes. La serie se encadena al nivel WIOD de 2014 (horas_mundo.combinar_un), de modo que TiM aporta la variación
medida por rama. No hay consumo de capital fijo por rama: la depreciación sigue la extensión agregada.

Indonesia y Rusia (F3d, nov. 2026; India sólo como sensibilidad): en TiM su remuneración es sólo la de los asalariados (D1), sin el ingreso
mixto (en la agricultura india, 14–17 % del valor agregado frente a 100 % en China). Se aplica entonces la misma regla
que a los países de la OCDE (ocde_ramas.py): el ingreso laboral de los no asalariados de cada sección se imputa con el
salario medio de los asalariados de esa sección,
  cp_j = LABR_j · (1 − s_j) / s_j,   s_j = asalariados / ocupados de la sección j (OIT, encuesta de fuerza de trabajo),
con tope en el valor agregado de la sección (LABR_j + cp_j ≤ VA_j), y
  v = Σ_productivas LABR · peso productivo,   pv = Σ_mercado VA − cp − v.
Los años sin encuesta toman s_j interpolada linealmente entre los años vecinos (o el más cercano en los extremos):
en Indonesia, 2016–2022. En Rusia el nivel de e de TiM (1,44 en 2014) casi coincide con el de WIOD (1,47); en
India, en cambio, la imputación con el salario medio de los asalariados lleva e a 0,79, lejos de la ONU y de WIOD (≈ 3),
porque el ingreso de los cuentapropistas indios es muy inferior al salario medio formal, y la base sería 2020 (pandemia).
Por eso India sigue en la central con la ONU (hasta 2020) y la extensión agregada; su variante TiM (encadenada desde
2020) se publica como sensibilidad (decisión de Pablo, 28 nov. 2026).
"""
import os
import numpy as np, pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FN = os.path.join(RAIZ, 'datos_cache', 'ocde_tim_2025.csv.gz')
FN_M = os.path.join(RAIZ, 'datos_cache', 'wiod_fraccion_productiva_M.csv')
SECC = list('ABCDEFGHIJKLMNOPQRST')
DIR_ILO = os.path.join(RAIZ, 'datos_cache', 'ilo')
# año desde el que TiM aporta la variación por rama (India: después de la ONU)
DESDE_ASAL = {'IND': 2020, 'IDN': 2014, 'RUS': 2014}
CIRC, FUERA, PUB = ['G', 'K'], ['L', 'O', 'T'], ['P', 'Q']


def calcular(share_ees, variantes, paises=('CHN',), desde=2014):
    if not os.path.exists(FN): return pd.DataFrame()
    d = pd.read_csv(FN)
    d = d[d.pais.isin(paises) & d.actividad.isin(SECC) & (d.anio >= desde)]
    fm = pd.read_csv(FN_M).set_index('pais').phi_M if os.path.exists(FN_M) else pd.Series(dtype=float)
    ees, tot = share_ees
    filas = []
    for (c, y), g in d.groupby(['pais', 'anio']):
        g = g.set_index('actividad').reindex(SECC).fillna(0.0)
        if g.VA_musd.sum() <= 0: continue
        agro = g.EMPN_miles['A'] / g.EMPN_miles.sum()
        s = min(1.0, float(ees.get(y, np.nan) / (tot.get(y, np.nan) * (1 - agro))))
        if not np.isfinite(s):
            continue
        sv = pd.Series(s, index=SECC); sv['A'] = 0.0
        phi_m = float(fm.get(c, fm.median() if len(fm) else 0.45))
        for variante, publicas_prod in variantes:
            fuera = FUERA + ([] if publicas_prod else PUB)
            mercado = [k for k in SECC if k not in fuera]
            prod_peso = pd.Series(1.0, index=SECC)
            prod_peso[CIRC + fuera] = 0.0; prod_peso['M'] = phi_m
            v = float((g.LABR_musd * sv * prod_peso).sum())
            # misma definición que con WIOD: pv = VA_m − cp − v, con cp = ingreso laboral de los no asalariados del
            # mercado; los salarios de circulación quedan dentro de pv (auditoría de nov. 2026)
            cp = float((g.LABR_musd * (1 - sv))[mercado].sum())
            pv = float(g.VA_musd[mercado].sum()) - cp - v
            N = float((g.EMPN_miles * sv * prod_peso).sum()) / 1000
            if v > 0:
                filas.append(dict(pais=c, variante=variante, anio=int(y), e=pv / v, r=np.nan, segmento='TiM 2025',
                                  obreros_productivos_mill=N, s_asalariados=s))
    return pd.DataFrame(filas)


def _proporcion_asalariados(c, anios):
    """s_j por sección CIIU rev. 4 y año (asalariados / ocupados, OIT), de una sola fuente estadística; interpolada."""
    try:
        E = pd.read_csv(os.path.join(DIR_ILO, f'EES_TEES_SEX_ECO_NB_A_{c}.csv'))
        O = pd.read_csv(os.path.join(DIR_ILO, f'EMP_TEMP_SEX_ECO_NB_A_{c}.csv'))
    except FileNotFoundError:
        return None
    def piv(d):
        d = d[(d.sex == 'SEX_T') & d.classif1.str.match(r'ECO_ISIC4_[A-U]$')].copy()
        d['sec'] = d.classif1.str[-1]
        return d
    E, O = piv(E), piv(O)
    if E.empty or O.empty: return None
    # la fuente con más años desde 2014, común a las dos tablas
    fuentes = [f for f in E.source.unique() if f in set(O.source)]
    if not fuentes: return None
    f = max(fuentes, key=lambda x: E[(E.source == x) & (E.time >= 2014)].time.nunique())
    e = E[E.source == f].pivot_table(index='time', columns='sec', values='obs_value')
    o = O[O.source == f].pivot_table(index='time', columns='sec', values='obs_value')
    sh = (e / o.replace(0, np.nan)).clip(upper=1.0).reindex(columns=SECC)
    sh = sh.reindex(sorted(set(sh.index) | set(anios))).interpolate(method='index', limit_area='inside').ffill().bfill()
    return sh.loc[[a for a in anios if a in sh.index]], f


def calcular_asalariados(variantes, paises=('IDN', 'RUS')):
    """Países cuya remuneración en TiM es sólo la de los asalariados: se imputa el ingreso de los no asalariados
    (véase la docstring del módulo). Devuelve el mismo formato que calcular(), con segmento propio."""
    if not os.path.exists(FN): return pd.DataFrame()
    d = pd.read_csv(FN)
    fm = pd.read_csv(FN_M).set_index('pais').phi_M if os.path.exists(FN_M) else pd.Series(dtype=float)
    filas = []
    for c in paises:
        g0 = d[(d.pais == c) & d.actividad.isin(SECC) & (d.anio >= DESDE_ASAL.get(c, 2014))]
        if g0.empty: continue
        r = _proporcion_asalariados(c, sorted(g0.anio.unique()))
        if r is None: continue
        S, fuente = r
        phi_m = float(fm.get(c, fm.median() if len(fm) else 0.45))
        for y, g in g0.groupby('anio'):
            if y not in S.index: continue
            g = g.set_index('actividad').reindex(SECC).fillna(0.0)
            if g.VA_musd.sum() <= 0: continue
            sv = S.loc[y].reindex(SECC)
            sv = sv.fillna(float(np.nanmedian(sv.values)) if sv.notna().any() else 1.0).clip(lower=0.02)
            cp_j = (g.LABR_musd * (1 - sv) / sv).clip(lower=0)
            cp_j = np.minimum(cp_j, (g.VA_musd - g.LABR_musd).clip(lower=0))      # tope: el valor agregado de la sección
            for variante, publicas_prod in variantes:
                fuera = FUERA + ([] if publicas_prod else PUB)
                mercado = [k for k in SECC if k not in fuera]
                prod_peso = pd.Series(1.0, index=SECC)
                prod_peso[CIRC + fuera] = 0.0; prod_peso['M'] = phi_m
                v = float((g.LABR_musd * prod_peso).sum())
                cp = float(cp_j[mercado].sum())
                pv = float(g.VA_musd[mercado].sum()) - cp - v
                N = float((g.EMPN_miles * sv * prod_peso).sum()) / 1000
                if v > 0:
                    filas.append(dict(pais=c, variante=variante, anio=int(y), e=pv / v, r=np.nan,
                                      segmento='TiM 2025 + OIT (' + fuente + ')', obreros_productivos_mill=N,
                                      s_asalariados=float((g.EMPN_miles * sv).sum() / g.EMPN_miles.sum())))
    return pd.DataFrame(filas)
