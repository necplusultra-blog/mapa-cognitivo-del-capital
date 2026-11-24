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
AGRO = ['A01', 'A02', 'A03']
VARIANTES = (('educación y salud productivas', True), ('educación y salud fuera', False))
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
    return d['STE_AGGREGATE_EES'], d['STE_AGGREGATE_TOTAL']


def _pwt_dep(dir_datos):
    """Depreciación sobre PIB por país y año (PWT 11.0): δ·K/Y = delta·cn/cgdpo (ambos a PPA corrientes).
    Se mantiene el último valor disponible para los años posteriores."""
    for fn in (os.path.join(dir_datos, 'pwt', 'pwt110.dta'), os.path.join(os.path.dirname(CACHE_ILO), 'pwt110.dta')):
        if os.path.exists(fn):
            x = pd.read_stata(fn, columns=['countrycode', 'year', 'delta', 'cn', 'cgdpo'])
            x['d'] = x.delta.astype(float) * x.cn.astype(float) / x.cgdpo.astype(float)
            return x.pivot_table(index='year', columns='countrycode', values='d')
    return pd.DataFrame()


def _china_params(y, piv, share_ees):
    """China: WIOD no distingue asalariados. Se toma de la OIT el total de asalariados y se asigna a las ramas no
    agrícolas en proporción a su ocupación WIOD (la agricultura china es casi enteramente familiar):
    s_no_agro = asalariados_OIT / (ocupación_OIT × (1 − peso agrícola WIOD)), con tope 1."""
    emp = piv['EMP'].loc['CHN'][y]
    agro = emp.reindex(AGRO).sum() / emp.sum()
    ees, tot = share_ees
    return min(1.0, float(ees.get(y, np.nan) / (tot.get(y, np.nan) * (1 - agro))))


def _pais(c, y, piv, improd, fuera, s_chn=None, agro_fuera=False, metodo_china='no agrícola', share_general=None):
    """Una observación país-año. Devuelve dict con v, pv, cp (moneda nacional), N (miles), H (millones de horas)."""
    fuera = fuera + (AGRO if agro_fuera else [])
    improd = improd + (AGRO if agro_fuera else [])
    codes = piv['VA'].loc[c].index
    prod = [k for k in codes if k not in improd]
    mercado = [k for k in codes if k not in fuera]
    if c == 'CHN':
        if metodo_china == 'general':   # método anterior: participación general de asalariados a todas las ramas
            s = pd.Series(share_general, index=codes)
        else:
            s = pd.Series(s_chn, index=codes); s[s.index.isin(AGRO)] = 0.0
        comp = lambda ks: (piv['COMP'].loc[c].loc[ks, y] * s[ks]).sum()
        N = (piv['EMP'].loc[c].loc[prod, y] * s[prod]).sum(); H = N * HORAS_CHINA / 1000
    else:
        comp = lambda ks: piv['COMP'].loc[c].loc[ks, y].sum()
        N = piv['EMPE'].loc[c].loc[prod, y].sum(); H = piv['H_EMPE'].loc[c].loc[prod, y].sum()
    v = comp(prod)
    cp = piv['LAB'].loc[c].loc[mercado, y].sum() - comp(mercado)
    vam = piv['VA'].loc[c].loc[mercado, y].sum()
    return dict(v=v, cp=cp, vam=vam, pv=vam - cp - v, N=N, H=H)


def calcular(dir_datos, dir_out):
    fn = os.path.join(dir_datos, 'wiod', 'Socio_Economic_Accounts.xlsx')
    if not os.path.exists(fn):
        fn = os.path.join(os.path.dirname(CACHE_ILO), 'wiod_sea.xlsx')
    d = pd.read_excel(fn, sheet_name='DATA', engine='calamine')
    yc = [c for c in d.columns if str(c).isdigit()]
    d = d.rename(columns={c: int(c) for c in yc}); Y = [int(c) for c in yc]
    piv = {v: d[d.variable == v].set_index(['country', 'code'])[Y] for v in ('VA', 'COMP', 'LAB', 'EMPE', 'H_EMPE', 'EMP')}
    paises = sorted(d.country.unique())
    share_ees = _ilo_china()
    dep = _pwt_dep(dir_datos)
    filas, excluidos, sens_base = [], [], []
    for variante, publicas_prod in VARIANTES:
        improd = CIRCULACION + FUERA + ([] if publicas_prod else PUBLICAS)
        fuera = FUERA + ([] if publicas_prod else PUBLICAS)
        for c in paises:
            for y in Y:
                s_chn = _china_params(y, piv, share_ees) if c == 'CHN' else None
                o = _pais(c, y, piv, improd, fuera, s_chn)
                if not (o['v'] > 0 and o['N'] > 0 and o['H'] > 0): continue
                e = o['pv'] / o['v']
                if not 0 < e < 8:   # datos anómalos (p. ej. Taiwán en algunos años): se excluyen y se registran
                    excluidos.append(dict(variante=variante, pais=c, anio=y, e=round(float(e), 3))); continue
                dd = float(dep[c].get(y, np.nan)) if c in dep else np.nan
                r = dd * o['vam'] / o['v'] if not np.isnan(dd) else np.nan
                filas.append(dict(variante=variante, pais=c, anio=y, obreros_mill=o['N'] / 1000, horas_mill=o['H'], e=e,
                                  r=r, cp_v=o['cp'] / o['v'], dep_pib=dd, china_estimada=c == 'CHN',
                                  fuente_e='WIOD por rama', fuente_obreros='WIOD por rama', fuente_r='PWT (δ·K/Y × VA de mercado)'))
                # variantes de sensibilidad para India y China (solo año base y para el cuadro de sensibilidad)
                if c in ('IND', 'CHN') and y == Y[-1]:
                    for etiqueta, kw in (('agricultura fuera', dict(agro_fuera=True)),
                                         ('China: método anterior', dict(metodo_china='general', share_general=float(share_ees[0].get(y) / share_ees[1].get(y))))):
                        if etiqueta.startswith('China') and c != 'CHN': continue
                        oo = _pais(c, y, piv, improd, fuera, s_chn, **kw)
                        ee = oo['pv'] / oo['v']
                        sens_base.append(dict(variante=variante, pais=c, caso=etiqueta, obreros_mill=oo['N'] / 1000, horas_mill=oo['H'], e=ee))
    P = pd.DataFrame(filas); P['extension'] = False
    diag = pd.DataFrame(); k_med = None
    try:
        X = extender(P, dep)
        try:
            from sismografo import ocde_ramas
            R = ocde_ramas.calcular(dir_datos, os.path.dirname(CACHE_ILO), piv)
            if not R.empty:
                P, X, calib = calibrar_r(P, X, R)
                calib.to_csv(os.path.join(dir_out, 'mundo_horas_calibracion_depreciacion.csv'), index=False)
                k_med = float(calib[calib.fuente == 'OCDE (país)'].k.median())
                X, diag = combinar_ocde(P, X, R, dep)
                R.to_csv(os.path.join(dir_out, 'mundo_horas_ocde_ramas.csv'), index=False)
        except Exception as e:  # noqa: BLE001
            print('Medición OCDE por rama omitida:', repr(e))
        if not X.empty: P = pd.concat([P, X], ignore_index=True)
    except Exception as e:  # noqa: BLE001
        print('Extensión OIT omitida:', repr(e))
    P['e_neta'] = P.e - P.r
    P['plustrabajo_mill_h'] = P.horas_mill * P.e / (1 + P.e)
    P['plustrabajo_neto_mill_h'] = P.horas_mill * P.e_neta / (1 + P.e_neta)
    P['necesario_mill_h'] = P.horas_mill / (1 + P.e)
    P = P.sort_values(['variante', 'pais', 'anio'])
    P.to_csv(os.path.join(dir_out, 'mundo_horas_paises.csv'), index=False)
    diag.to_csv(os.path.join(dir_out, 'mundo_horas_ocde_diagnostico.csv'), index=False)
    pd.DataFrame(excluidos).to_csv(os.path.join(dir_out, 'mundo_horas_excluidos.csv'), index=False)
    A = agregar(P)
    A.to_csv(os.path.join(dir_out, 'mundo_horas.csv'), index=False)
    S = sensibilidad(P, pd.DataFrame(sens_base), share_ees, piv)
    S.to_csv(os.path.join(dir_out, 'mundo_horas_sensibilidad.csv'), index=False)
    return dict(A=A, P=P, excluidos=excluidos, diag=diag, S=S, k_mediana=k_med)


def agregar(P):
    agg = []
    for (var, y), g in P.groupby(['variante', 'anio']):
        for etiqueta, gg in (('con China', g), ('sin China', g[g.pais != 'CHN'])):
            H, Sp = gg.horas_mill.sum(), gg.plustrabajo_mill_h.sum()
            gn = gg[gg.e_neta.notna()]
            Hn, Sn = gn.horas_mill.sum(), gn.plustrabajo_neto_mill_h.sum()
            agg.append(dict(variante=var, china=etiqueta, anio=int(y), paises=len(gg), extension=bool(g.extension.any()),
                            obreros_mill=gg.obreros_mill.sum(), plustrabajo_mmh=Sp / 1000, e_horas=Sp / (H - Sp),
                            plustrabajo_neto_mmh=Sn / 1000 * H / Hn if Hn else np.nan, e_horas_neta=Sn / (Hn - Sn) if Hn else np.nan,
                            semana_horas=H / gg.obreros_mill.sum() / 52,
                            pct_china=float(g.loc[g.pais == 'CHN', 'plustrabajo_mill_h'].sum() / g.plustrabajo_mill_h.sum() * 100),
                            pct_india=float(g.loc[g.pais == 'IND', 'plustrabajo_mill_h'].sum() / g.plustrabajo_mill_h.sum() * 100),
                            pct_ocde_rama=float(g.loc[g.fuente_e == 'OCDE por rama', 'plustrabajo_mill_h'].sum() / g.plustrabajo_mill_h.sum() * 100)))
    return pd.DataFrame(agg)


def sensibilidad(P, SB, share_ees, piv):
    """Cuadro de sensibilidad de la masa mundial de plustrabajo (variante principal, con China) en el último año WIOD
    y en el último año de la serie. Cada fila cambia un solo supuesto respecto de la estimación central."""
    var = VARIANTES[0][0]
    base_wiod = int(P.loc[~P.extension, 'anio'].max()); fin = int(P.anio.max())
    out = []
    for y in (base_wiod, fin):
        g = P[(P.variante == var) & (P.anio == y)].copy()
        tot = g.plustrabajo_mill_h.sum()

        def fila(caso, total, obreros, nota):
            out.append(dict(anio=y, caso=caso, plustrabajo_mmh=total / 1000, obreros_mill=obreros,
                            diferencia_pct=(total / tot - 1) * 100, nota=nota))
        fila('Estimación central (bruta)', tot, g.obreros_mill.sum(), '')
        fila('Neta de depreciación', g.plustrabajo_neto_mill_h.sum(), g.obreros_mill.sum(), 'pv − consumo de capital fijo de las ramas de mercado')
        chn = g[g.pais == 'CHN']
        for h in (44, 49):
            dif = chn.plustrabajo_mill_h.sum() * (h * 50 / HORAS_CHINA - 1)
            fila(f'China: {h} h semanales', tot + dif, g.obreros_mill.sum(), 'jornada supuesta (central: 46 h × 50 semanas)')
        ind = g[g.pais == 'IND']
        ees_ind = _ilo_total('IND')
        if ees_ind is not None and not ind.empty:
            k = ees_ind.get(base_wiod, np.nan) / piv['EMPE'].loc['IND'][base_wiod].sum()   # ambos en miles
            fila('India: nivel de asalariados de la OIT', tot - ind.plustrabajo_mill_h.sum() * (1 - k),
                 g.obreros_mill.sum() - ind.obreros_mill.sum() * (1 - k),
                 f'asalariados productivos de India × {k:.2f} (asalariados OIT / asalariados WIOD en {base_wiod}): la serie de la OIT solo recoge el trabajo asalariado regular, no a los jornaleros eventuales')
        # agricultura fuera para India y China: se aplica la razón calculada en el año base WIOD a ambos años
        for caso, paises in (('India y China: agricultura fuera', ('IND', 'CHN')),):
            nuevo, obreros = tot, g.obreros_mill.sum()
            for c in paises:
                sb = SB[(SB.variante == var) & (SB.pais == c) & (SB.caso == 'agricultura fuera')]
                b = P[(P.variante == var) & (P.pais == c) & (P.anio == base_wiod)]
                if sb.empty or b.empty: continue
                sb, b = sb.iloc[0], b.iloc[0]
                pt_b = b.horas_mill * b.e / (1 + b.e); pt_s = sb.horas_mill * sb.e / (1 + sb.e)
                gc = g[g.pais == c].iloc[0]
                nuevo += gc.plustrabajo_mill_h * (pt_s / pt_b - 1); obreros += gc.obreros_mill * (sb.obreros_mill / b.obreros_mill - 1)
            fila(caso, nuevo, obreros, 'las ramas agrícolas (A01–A03) de ambos países se tratan como fuera de la producción capitalista')
        sb = SB[(SB.variante == var) & (SB.caso == 'China: método anterior')]
        if not sb.empty and not chn.empty:
            sb = sb.iloc[0]; b = P[(P.variante == var) & (P.pais == 'CHN') & (P.anio == base_wiod)].iloc[0]
            pt_b = b.horas_mill * b.e / (1 + b.e); pt_s = sb.horas_mill * sb.e / (1 + sb.e)
            fila('China: método anterior (participación general)', tot + chn.plustrabajo_mill_h.sum() * (pt_s / pt_b - 1),
                 g.obreros_mill.sum() + chn.obreros_mill.sum() * (sb.obreros_mill / b.obreros_mill - 1),
                 'participación de asalariados de toda la economía aplicada también a la agricultura')
    return pd.DataFrame(out)


def calibrar_r(P, X, R):
    """La razón PWT δ·K/Y abarca todo el capital fijo (incluidas viviendas y capital público), por lo que aplicada al
    valor agregado de mercado sobrestima la depreciación de las ramas capitalistas. Donde la OCDE mide el consumo de
    capital fijo por rama (P51C), se calibra cada país con k = r_OCDE(2014) / r_PWT(2014); para el resto de los países
    se usa la mediana de esos k. El factor se aplica a toda la serie del país (2000–2025)."""
    var = VARIANTES[0][0]; base = int(P.anio.max())
    ro = R[(R.variante == var) & (R.anio == base)].set_index('pais').r.dropna()
    rp = P[(P.variante == var) & (P.anio == base)].set_index('pais').r
    k = (ro / rp.reindex(ro.index)).dropna()
    k_med = float(k.median())
    kk = {c: float(k.get(c, k_med)) for c in P.pais.unique()}
    P = P.copy(); X = X.copy()
    P['r_pwt_sin_calibrar'] = P.r; X['r_pwt_sin_calibrar'] = X.r
    P['r'] = P.r * P.pais.map(kk); X['r'] = X.r * X.pais.map(kk)
    calib = pd.DataFrame([dict(pais=c, k=v, fuente='OCDE (país)' if c in k.index else 'mediana OCDE') for c, v in sorted(kk.items())])
    return P, X, calib


def _ilo_total(c):
    fn = os.path.join(os.path.dirname(CACHE_ILO), 'ilo', f'{ILO_IND["ees_mod"]}_{c}.csv')
    if not os.path.exists(fn): return None
    d = pd.read_csv(fn); d = d[d.sex == 'SEX_T']
    return d[d.classif1 == 'STE_AGGREGATE_EES'].groupby('time').obs_value.mean()


def _encadenar(base, idx_o, idx_i, anios):
    """Índice relativo al año base: el de la OCDE mientras exista sin interrupción; después, el de la OIT
    empalmado en el último año OCDE."""
    out, ultimo = {}, None
    for y in anios:
        if idx_o is not None and y in idx_o.index and not pd.isna(idx_o[y]) and (ultimo is None or ultimo == y - 1):
            out[y] = idx_o[y]; ultimo = y
        else:
            out[y] = (out[ultimo] * idx_i[y] / idx_i[ultimo]) if ultimo is not None else idx_i[y]
    return pd.Series(out), ultimo


def combinar_ocde(P, X, R, dep):
    """Sustituye la extensión OIT por la medición OCDE por rama donde existe (véase ocde_ramas.py)."""
    base = int(P.anio.max()); anios = list(range(base, int(X.anio.max()) + 1)); filas, diag = [], []
    reemplazados = set()
    for (c, var), r in R.groupby(['pais', 'variante']):
        r = r.set_index('anio').sort_index()
        b = P[(P.pais == c) & (P.variante == var) & (P.anio == base)]
        xi = X[(X.pais == c) & (X.variante == var)].set_index('anio')
        if b.empty or xi.empty or base not in r.index: continue
        b = b.iloc[0]
        ilo = pd.concat([pd.DataFrame([dict(anio=base, e=b.e, obreros_mill=b.obreros_mill, horas_mill=b.horas_mill, r=b.r)]).set_index('anio'),
                         xi[['e', 'obreros_mill', 'horas_mill', 'r']]]).reindex(anios)
        # el excedente solo es comparable en el tiempo si la imputación de no asalariados es la misma todos los años
        cp = r.cuenta_propia_imputada
        r_e = r.e.where(cp == cp.get(base)) if base in cp.index else r.e
        idx_e, ult_e = _encadenar(base, r_e / r_e[base], ilo.e / ilo.e[base], anios)
        tieneN = not pd.isna(r.N_mill.get(base))
        idx_N, ult_N = _encadenar(base, (r.N_mill / r.N_mill[base]) if tieneN else None, ilo.obreros_mill / ilo.obreros_mill[base], anios)
        hpw_i = ilo.horas_mill / ilo.obreros_mill
        tieneH = tieneN and not pd.isna(r.H_mill.get(base))
        idx_hpw, _ = _encadenar(base, ((r.H_mill / r.N_mill) / (r.H_mill[base] / r.N_mill[base])) if tieneH else None, hpw_i / hpw_i[base], anios)
        tieneR = not pd.isna(r.r.get(base)) and not pd.isna(b.r)
        if tieneR:
            idx_r, ult_r = _encadenar(base, r.r / r.r[base], ilo.r / ilo.r[base], anios)
        for y in anios[1:]:
            e = b.e * idx_e[y]; N = b.obreros_mill * idx_N[y]; H = b.horas_mill * idx_N[y] * idx_hpw[y]
            rr = b.r * idx_r[y] if tieneR else ilo.r[y]
            filas.append(dict(variante=var, pais=c, anio=y, obreros_mill=N, horas_mill=H, e=e, r=rr, cp_v=b.cp_v,
                              dep_pib=xi.dep_pib.get(y, np.nan), china_estimada=False, extension=True,
                              fuente_e='OCDE por rama' if ult_e is not None and y <= ult_e else 'OIT (participación del trabajo)',
                              fuente_obreros='OCDE por rama' if ult_N is not None and y <= ult_N else xi.fuente_obreros.get(y, 'OIT'),
                              fuente_horas='OCDE por rama' if tieneH and ult_N is not None and y <= ult_N else xi.fuente_horas.get(y, 'OIT'),
                              fuente_r='OCDE por rama (P51C)' if tieneR and y <= ult_r else 'PWT (δ·K/Y × VA de mercado)'))
        reemplazados.add((c, var))
        if var == VARIANTES[0][0]:
            diag.append(dict(pais=c, e_wiod_2014=b.e, e_ocde_2014=r.e[base], N_ocde_sobre_wiod=(r.N_mill[base] / b.obreros_mill) if tieneN else np.nan,
                             H_ocde_sobre_wiod=(r.H_mill[base] / b.horas_mill) if tieneH else np.nan,
                             r_pwt_2014=b.r, r_ocde_2014=r.r.get(base, np.nan), ultimo_anio_e=ult_e, ultimo_anio_N=ult_N if tieneN else None,
                             cuenta_propia_imputada=bool(cp.get(base, False)), m_imputado=bool(r.m_imputado.any()), residuo=bool(r.residuo.any())))
    resto = X[[(c, v) not in reemplazados for c, v in zip(X.pais, X.variante)]]
    return pd.concat([resto, pd.DataFrame(filas)], ignore_index=True), pd.DataFrame(diag)


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


# India: WIOD cuenta como asalariados a los trabajadores regulares y a los jornaleros eventuales (casual labour), como
# las encuestas NSS; la serie modelada de asalariados de la OIT solo recoge a los regulares y crece mucho más rápido.
# Por eso el número de asalariados de India se extiende con la ocupación total de la OIT por la proporción de
# trabajadores no cuenta propia (regulares + eventuales) de las encuestas oficiales, en estatus usual (ps+ss):
#   NSS 68.ª ronda 2011-12: 52,2 % cuenta propia; PLFS 2017-18: 52,2 %; 2021-22: 55,8 %; 2022-23: 57,3 %; 2023-24: 58,4 %.
# El año agrícola julio–junio se asigna al año calendario en que termina; entre puntos se interpola y después del
# último se mantiene constante.
INDIA_CUENTA_PROPIA = {2012: 0.522, 2018: 0.522, 2022: 0.558, 2023: 0.573, 2024: 0.584}


def _india_cuenta_propia(anios):
    s = pd.Series(INDIA_CUENTA_PROPIA)
    return s.reindex(sorted(set(s.index) | set(anios))).interpolate(limit_area='inside').ffill().bfill().reindex(anios)


def extender(P, dep=None, hasta=2025):
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
        for variante, publicas_prod in VARIANTES:
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
            if N_idx is None and c == 'IND' and not mod.empty:
                ocup = _serie_anual(mod[mod.classif1 == 'STE_AGGREGATE_TOTAL'].set_index('time')['obs_value'], anios)
                asal = ocup * (1 - _india_cuenta_propia(anios))
                if asal.notna().all():
                    N_idx, fuente_n = asal / asal[base], 'OIT ocupación total × proporción asalariada NSS/PLFS'
            if N_idx is None and tot_mod is not None and tot_mod.notna().all():
                N_idx, fuente_n = tot_mod / tot_mod[base], 'OIT modelada (asalariados totales)'
            if N_idx is None: N_idx = pd.Series(1.0, index=anios)
            h_idx = (h / h[base]) if h is not None else pd.Series(1.0, index=anios)
            dser = dep[c] if dep is not None and c in dep else None
            for y in anios[1:]:
                e = b.e * odds[y] / odds[base]
                N = b.obreros_mill * N_idx[y]; H = b.horas_mill * N_idx[y] * h_idx[y]
                dd = float(dser.reindex(range(base, y + 1)).ffill().get(y, np.nan)) if dser is not None else np.nan
                # r = D/v = (D/VA) · (VA de mercado / v), con VA de mercado / v = 1 + e + cp/v (cp/v del año base)
                r = dd * (1 + e + b.cp_v) if not np.isnan(dd) else np.nan
                filas.append(dict(variante=variante, pais=c, anio=y, obreros_mill=N, horas_mill=H, e=e, r=r, cp_v=b.cp_v,
                                  dep_pib=dd, china_estimada=c == 'CHN', extension=True, fuente_e='OIT (participación del trabajo)',
                                  fuente_obreros=fuente_n, fuente_horas='OIT' if h is not None else 'constante',
                                  fuente_r='PWT (δ·K/Y × VA de mercado)'))
    return pd.DataFrame(filas)
