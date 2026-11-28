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
# Variante central (decisión del autor): sólo la parte capitalista de educación y salud es productiva; la pública y la
# sin fines de lucro quedan fuera (publico.py). Se obtiene combinando las dos variantes anteriores.
CENTRAL = 'educación y salud públicas fuera'
HORAS_CHINA = 46 * 50   # horas anuales por asalariado (supuesto explícito: 46 h semanales, 50 semanas)
CACHE_ILO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datos_cache', 'ilo_chn_asalariados.csv')


def _ilo_china():
    url = 'https://rplumber.ilo.org/data/indicator/?id=EMP_2EMP_SEX_STE_NB_A&ref_area=CHN&sex=SEX_T&format=.csv'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 mapa-cognitivo-del-capital'})
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
        try:
            from sismografo import un_ramas
            RU = un_ramas.calcular(piv)
            if not RU.empty:
                X, diag_un = combinar_un(P, X, RU)
                RU.to_csv(os.path.join(dir_out, 'mundo_horas_onu_ramas.csv'), index=False)
                diag_un.to_csv(os.path.join(dir_out, 'mundo_horas_onu_diagnostico.csv'), index=False)
        except Exception as e:  # noqa: BLE001
            print('Medición ONU por rama omitida:', repr(e))
        try:
            from sismografo import tim_ramas
            RT = tim_ramas.calcular(share_ees, VARIANTES); diag_tim = pd.DataFrame()
            if not RT.empty:
                X, diag_tim = combinar_un(P, X, RT, etiqueta='OCDE TiM por rama')
                X = combinar_tim_obreros(P, X, RT)
            # Indonesia y Rusia: TiM con el ingreso de los no asalariados imputado (OIT por sección); India, sólo sensibilidad
            RA = tim_ramas.calcular_asalariados(VARIANTES)
            if not RA.empty:
                X, diag_a = combinar_un(P, X, RA, etiqueta='OCDE TiM por rama')
                RT = pd.concat([RT, RA], ignore_index=True); diag_tim = pd.concat([diag_tim, diag_a], ignore_index=True)
            if not RT.empty:
                RT.to_csv(os.path.join(dir_out, 'mundo_horas_tim_ramas.csv'), index=False)
                diag_tim.to_csv(os.path.join(dir_out, 'mundo_horas_tim_diagnostico.csv'), index=False)
        except Exception as e:  # noqa: BLE001
            print('Medición TiM por rama omitida:', repr(e))
        try:
            X, diag_ilo = combinar_ilo(P, X, piv)
            diag_ilo.to_csv(os.path.join(dir_out, 'mundo_horas_ilo_secciones.csv'), index=False)
        except Exception as e:  # noqa: BLE001
            print('Medición OIT por sección omitida:', repr(e))
        if not X.empty: P = pd.concat([P, X], ignore_index=True)
    except Exception as e:  # noqa: BLE001
        print('Extensión OIT omitida:', repr(e))
    G = pd.DataFrame()
    try:
        from sismografo import publico
        G = publico.proporciones(dir_datos, sorted(P.pais.unique()), sorted(P.anio.unique()))
        # EE.UU.: a la parte pública (OIT) se suma la parte sin fines de lucro de la educación y la salud privadas
        u = G.pais == 'USA'
        G.loc[u, 'g'] = G.loc[u, 'g'] + (1 - G.loc[u, 'g']) * 0.46; G.loc[u, 'fuente_g'] += ' + sin fines de lucro (BLS)'
        P = pd.concat([P, publico.variante_privada(P, G, CENTRAL, VARIANTES[0][0], VARIANTES[1][0])], ignore_index=True)
        G.to_csv(os.path.join(dir_out, 'mundo_horas_parte_publica.csv'), index=False)
    except Exception as e:  # noqa: BLE001
        print('Variante con educación y salud públicas fuera omitida:', repr(e))
    try:
        P = ajuste_bloque_b(P, dir_datos)
    except Exception as e:  # noqa: BLE001
        print('Ajustes B3/B4 omitidos:', repr(e))
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


def ajuste_bloque_b(P, dir_datos):
    """Auditoría B3 y B4 (decisión del autor, 24 nov. 2026), en la medición central:
    B3: + renta que las ramas de mercado pagan por locales y oficinas (consumo intermedio de L68): plusvalor producido y
        cedido a la propiedad territorial;
    B4: − servicios financieros que los hogares pagan con sus salarios (consumo final de K64–K66 × participación del
        trabajo en el ingreso, PWT labsh): plusvalor desplazado desde el salario, no producido.
    Ambas como proporción del valor agregado de las ramas de mercado (WIOD; después de 2014, proporción de 2014).
    e' = e + (b3 − b4) · VA_mercado / v, con VA_mercado / v = 1 + e + cp/v. Se conserva e sin ajuste."""
    from sismografo.bloque_b import cuotas_wiod
    W = cuotas_wiod()
    if W.empty: return P
    W = W.set_index(['pais', 'anio'])
    ult = W.reset_index().sort_values('anio').groupby('pais').last()
    fn = os.path.join(dir_datos, 'pwt', 'pwt110.dta')
    if not os.path.exists(fn): fn = os.path.join(os.path.dirname(CACHE_ILO), 'pwt110.dta')
    ls = pd.read_stata(fn, columns=['countrycode', 'year', 'labsh']).pivot_table(index='year', columns='countrycode', values='labsh')
    ls = ls.reindex(range(int(ls.index.min()), int(P.anio.max()) + 1)).ffill()
    P = P.copy()
    cp = P.groupby(['pais', 'anio']).cp_v.transform('median') if 'cp_v' in P else 0.0
    P['cp_v'] = P.cp_v.fillna(cp) if 'cp_v' in P else 0.0
    def cuota(c, y, k):
        try: return float(W.loc[(c, y), k])
        except KeyError: return float(ult[k].get(c, np.nan))
    P['b3_pct_va'] = [cuota(c, y, 'renta_pct_va') for c, y in zip(P.pais, P.anio)]
    lab = [float(ls[c].get(y, np.nan)) if c in ls else np.nan for c, y in zip(P.pais, P.anio)]
    P['b4_pct_va'] = [cuota(c, y, 'fin_hogares_pct_va') for c, y in zip(P.pais, P.anio)] * pd.Series(lab, index=P.index).fillna(0.55)
    P['e_sin_ajuste_b'] = P.e
    adj = (P.b3_pct_va.fillna(0) - P.b4_pct_va.fillna(0)) * (1 + P.e + P.cp_v.fillna(0))
    P['e'] = (P.e + adj).clip(lower=0.01)
    return P


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
        vc = CENTRAL if (P.variante == CENTRAL).any() else var
        g = P[(P.variante == vc) & (P.anio == y)].copy()
        tot = g.plustrabajo_mill_h.sum()

        def fila(caso, total, obreros, nota):
            out.append(dict(anio=y, caso=caso, plustrabajo_mmh=total / 1000, obreros_mill=obreros,
                            diferencia_pct=(total / tot - 1) * 100, nota=nota))
        fila('Estimación central (bruta)', tot, g.obreros_mill.sum(), '')
        fila('Neta de depreciación', g.plustrabajo_neto_mill_h.sum(), g.obreros_mill.sum(), 'pv − consumo de capital fijo de las ramas de mercado')
        for v_, caso_, nota_ in ((VARIANTES[0][0], 'Educación y salud públicas incluidas', 'contraste: cuenta como productivo el trabajo pagado con impuestos'),
                                 (VARIANTES[1][0], 'Educación y salud enteras fuera', 'contraste: excluye también las escuelas y clínicas capitalistas')):
            gv = P[(P.variante == v_) & (P.anio == y)]
            if vc != v_ and not gv.empty: fila(caso_, gv.plustrabajo_mill_h.sum(), gv.obreros_mill.sum(), nota_)
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
                 f'asalariados productivos de India × {k:.2f} (asalariados OIT / WIOD en {base_wiod}). Contraste: excluye a los jornaleros eventuales, que según el criterio adoptado son productivos')
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
            fila(caso, nuevo, obreros, 'Contraste: excluye la agricultura de ambos países, que según el criterio adoptado es productiva cuando su salario es capital')
        # India con TiM por rama desde 2020 (sensibilidad, no central): factor sobre e desde el último año de TiM
        try:
            from sismografo import tim_ramas
            RI = tim_ramas.calcular_asalariados(VARIANTES, paises=('IND',))
            RI = RI[RI.variante == VARIANTES[1][0]].set_index('anio').e if not RI.empty else pd.Series(dtype=float)   # la razón de TiM no depende mucho de la variante
            if y > base_wiod and len(RI) > 1 and not ind.empty:
                a0, a1 = int(RI.index.min()), int(RI.index.max())
                ec = P[(P.variante == vc) & (P.pais == 'IND')].set_index('anio').e
                if a0 in ec.index and a1 in ec.index and y >= a1:
                    k_e = ec[a0] * RI[a1] / RI[a0] / ec[a1]
                    e_y = float(ind.e.iloc[0]); e_alt = e_y * k_e
                    pt = float(ind.plustrabajo_mill_h.sum())
                    fila(f'India: e por rama con TiM desde {a0}', tot + pt * ((e_alt / (1 + e_alt)) / (e_y / (1 + e_y)) - 1), g.obreros_mill.sum(),
                         f'variación de e por rama de TiM {a0}–{a1} (ingreso de los cuentapropistas imputado con el salario medio de los asalariados de cada sección); e de India × {k_e:.2f}')
        except Exception as e_:  # noqa: BLE001
            print('Sensibilidad India TiM omitida:', repr(e_))
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


def combinar_un(P, X, RU, etiqueta='ONU por rama (tabla 2.6)'):
    """Tasa de plusvalor y depreciación medidas por rama en las cuentas oficiales de la ONU (véase un_ramas.py),
    encadenadas al nivel WIOD de 2014. Cada serie estadística (segmento) se encadena por separado; entre segmentos,
    y después del último, la variación es la de la extensión agregada."""
    base = int(P.anio.max()); X = X.copy(); diag = []
    for (c, var), R in RU.groupby(['pais', 'variante']):
        m = (X.pais == c) & (X.variante == var)
        b = P[(P.pais == c) & (P.variante == var) & (P.anio == base)]
        if not m.any() or b.empty: continue
        anios = sorted(X.loc[m, 'anio'])
        viejo = pd.concat([pd.Series({base: b.e.iloc[0]}), X.loc[m].set_index('anio').e]).sort_index()
        viejo_r = pd.concat([pd.Series({base: b.r.iloc[0]}), X.loc[m].set_index('anio').r]).sort_index()
        nuevo, nuevo_r = viejo.copy(), viejo_r.copy(); medidos = set(); medidos_r = set()
        for seg, g in R[R.anio >= base].groupby('segmento'):
            g = g.set_index('anio').sort_index()
            a0 = int(g.index.min())
            if a0 not in nuevo.index: continue
            for y in g.index:
                if y == a0 or y not in nuevo.index: continue
                nuevo[y] = nuevo[a0] * g.e[y] / g.e[a0]
                if not pd.isna(g.r.get(a0)) and not pd.isna(g.r.get(y)) and not pd.isna(nuevo_r[a0]):
                    nuevo_r[y] = nuevo_r[a0] * g.r[y] / g.r[a0]; medidos_r.add(y)
                medidos.add(y)
            ult = int(g.index.max())
            for y in [a for a in nuevo.index if a > ult]:
                nuevo[y] = nuevo[ult] * viejo[y] / viejo[ult]
                if not pd.isna(viejo_r[ult]) and viejo_r[ult] != 0: nuevo_r[y] = nuevo_r[ult] * viejo_r[y] / viejo_r[ult]
        for i in X.index[m]:
            y = int(X.at[i, 'anio'])
            X.at[i, 'e'] = nuevo[y]; X.at[i, 'r'] = nuevo_r[y]
            if y in medidos:
                X.at[i, 'fuente_e'] = etiqueta
            if y in medidos_r:
                X.at[i, 'fuente_r'] = 'ONU por rama (CCF), encadenada a la r calibrada de 2014'
        if var == VARIANTES[0][0] and medidos:
            g0 = R[(R.anio == base)]
            diag.append(dict(pais=c, desde=base, hasta=max(medidos), e_wiod_2014=float(b.e.iloc[0]),
                             **{('e_onu_2014' if 'ONU' in etiqueta else 'e_tim_2014'): float(g0.e.iloc[0]) if len(g0) else np.nan}, e_2014_a_ultimo=float(nuevo[max(medidos)] / nuevo[base])))
    return X, pd.DataFrame(diag)


def combinar_tim_obreros(P, X, RT):
    """China: el número de asalariados productivos sigue, hasta 2022, la variación medida por rama con TiM (ocupados de las
    ramas productivas × proporción asalariada s); después, la de la extensión agregada. Horas por asalariado constantes."""
    base = int(P.anio.max()); X = X.copy()
    for (c, var), R in RT.groupby(['pais', 'variante']):
        m = (X.pais == c) & (X.variante == var)
        b = P[(P.pais == c) & (P.variante == var) & (P.anio == base)]
        R = R.set_index('anio').sort_index()
        if not m.any() or b.empty or base not in R.index: continue
        idx = R.obreros_productivos_mill / R.obreros_productivos_mill[base]
        ult = int(R.index.max()); N0 = float(b.obreros_mill.iloc[0])
        viejo = X.loc[m].set_index('anio').obreros_mill
        hpw = float(b.horas_mill.iloc[0] / b.obreros_mill.iloc[0])
        for i in X.index[m]:
            y = int(X.at[i, 'anio'])
            if y <= ult and y in idx.index:
                N = N0 * idx[y]; X.at[i, 'fuente_obreros'] = 'OCDE TiM por rama'
            elif y > ult and ult in viejo.index:
                N = N0 * idx[ult] * viejo[y] / viejo[ult]
            else:
                continue
            X.at[i, 'obreros_mill'] = N; X.at[i, 'horas_mill'] = N * hpw
    return X


PAISES_ILO = ['BRA', 'CHN', 'IDN', 'IND', 'RUS', 'MEX', 'TUR', 'CYP', 'MLT']


def combinar_ilo(P, X, piv):
    """Medición por sección (OIT) para los países sin asalariados por rama en la OCDE (véase ilo_ramas.py)."""
    from sismografo import ilo_ramas
    dir_cache = os.path.join(os.path.dirname(CACHE_ILO), 'ilo')
    base_wiod = int(P.anio.max()); X = X.copy(); diag = []
    for c in PAISES_ILO:
        for variante, publicas_prod in VARIANTES:
            m = (X.pais == c) & (X.variante == variante)
            if not m.any(): continue
            ind = ilo_ramas.indicadores(c, piv, dir_cache, publicas_prod)
            if ind.empty or ind.ps.dropna().empty: continue
            b = int(ind.ps.dropna().index.min())
            anios = sorted(X.loc[m, 'anio'])
            ind = ind.reindex(sorted(set(ind.index) | set(anios))).sort_index()
            ps = ind.ps.ffill(); hp = ind.get('hp', pd.Series(dtype=float)).ffill(); q = ind.get('q', pd.Series(dtype=float)).ffill()
            fila_b = P[(P.pais == c) & (P.variante == variante) & (P.anio == b)] if b == base_wiod else X[m & (X.anio == b)]
            if fila_b.empty: continue
            hpw_b = float(fila_b.horas_mill.iloc[0] / fila_b.obreros_mill.iloc[0])
            tiene_h = b in hp.index and not pd.isna(hp.get(b)) and hp.notna().sum() > 1
            tiene_q = b in q.index and not pd.isna(q.get(b)) and q.notna().sum() > 1
            # si la ONU o TiM midieron e por rama (Brasil, India, China, Indonesia, Rusia), la corrección q se reancla en
            # el último año medido por rama, para no aplicar de nuevo la variación de q de los años que ya se midieron
            # (auditoría de nov. 2026; extendida a TiM en F3d, 28 nov. 2026)
            un = X.loc[m & X.fuente_e.astype(str).str.match(r'^(ONU|OCDE TiM)'), 'anio']
            qb = int(un.max()) if len(un) and int(un.max()) in q.index and not pd.isna(q.get(int(un.max()))) else b
            for i in X.index[m & (X.anio >= b)]:
                y = int(X.at[i, 'anio'])
                N = X.at[i, 'obreros_mill'] * ps[y] / ps[b]
                H = N * hpw_b * hp[y] / hp[b] if tiene_h else X.at[i, 'horas_mill'] * ps[y] / ps[b]
                X.at[i, 'obreros_mill'], X.at[i, 'horas_mill'] = N, H
                X.at[i, 'fuente_obreros'] = f'OIT por sección ({ind.fuente_secciones.dropna().iloc[0]})'
                if tiene_h: X.at[i, 'fuente_horas'] = 'OIT por sección'
                if tiene_q and y >= qb and X.at[i, 'fuente_e'] not in ('OCDE por rama', 'ONU por rama (tabla 2.6)', 'OCDE TiM por rama'):
                    X.at[i, 'e'] = (1 + X.at[i, 'e']) * q[qb] / q[y] - 1
                    X.at[i, 'fuente_e'] = 'OIT (participación del trabajo) + masa salarial por sección'
            if variante == VARIANTES[0][0]:
                ult = int(ind.ps.dropna().index.max())
                diag.append(dict(pais=c, fuente=ind.fuente_secciones.dropna().iloc[0], desde=b, hasta=ult,
                                 ps_inicio=ps[b], ps_fin=ps[ult], horas_por_seccion=tiene_h, masa_salarial_por_seccion=tiene_q,
                                 hp_inicio=hp.get(b) if tiene_h else np.nan, hp_fin=hp.get(ult) if tiene_h else np.nan,
                                 q_inicio=q.get(b) if tiene_q else np.nan, q_fin=q.get(ult) if tiene_q else np.nan))
    return X, pd.DataFrame(diag)


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
                             r_pwt_2014=b.get('r_pwt_sin_calibrar', b.r), r_ocde_2014=r.r.get(base, np.nan), ultimo_anio_e=ult_e, ultimo_anio_N=ult_N if tieneN else None,
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
        req = urllib.request.Request(ILO.format(id=ind, c=c), headers={'User-Agent': 'Mozilla/5.0 mapa-cognitivo-del-capital'})
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
