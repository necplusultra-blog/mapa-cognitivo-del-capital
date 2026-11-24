"""Fase F4: la transformación. Valores-trabajo por rama con las tablas insumo-producto nacionales de WIOD (2000–2014).

Qué se calcula
--------------
1. Valores por rama. Para cada país y año, el tiempo de trabajo directo e indirecto que contiene un dólar de producto
   de cada rama productiva (valor-trabajo verticalmente integrado, en horas por dólar):

       λ_p = (l_p + λ̄_p · M_pp) · (I − A_pp)⁻¹

   l   = horas trabajadas por dólar de producción bruta (todos los ocupados: los trabajadores por cuenta propia que
         producen mercancías también producen valor, aunque no plusvalor);
   A   = coeficientes de insumos nacionales; M = coeficientes de insumos importados;
   λ̄   = contenido medio en horas de un dólar exportado de cada producto en el mundo (promedio ponderado por las
         exportaciones de los 43 países), que valúa los insumos importados. Se resuelve por iteración.
   Sólo entran las ramas productivas (subíndice p). Los insumos que vienen de ramas de circulación (comercio, finanzas,
   servicios jurídicos, publicidad) o de fuera de la producción capitalista (inmobiliario, administración pública,
   educación, salud, hogares) no transfieren valor: son gastos pagados con plusvalor (tratamiento de Shaikh y Tonak).
   Educación y salud quedan fuera en esta primera versión, porque las tablas no separan su parte capitalista.

2. Desviación de los precios respecto de los valores. Con la expresión monetaria del tiempo de trabajo de cada país,
   μ = Σ producción bruta / Σ λ · producción bruta (ramas productivas), el «precio-valor» de un dólar de producto de la
   rama j es v_j = μ · λ_j. Si v_j > 1, el precio de mercado está por debajo del valor (la rama cede valor); si v_j < 1,
   por encima (se apropia valor). Medidas por país y año:
     - desviación absoluta media ponderada por la producción: Σ x_j |v_j − 1| / Σ x_j;
     - correlación de rangos (Spearman) entre precio/valor (1/v_j) y la composición en valor K_j / v_j (stock de capital
       sobre ingreso del trabajo, asalariado y por cuenta propia, WIOD SEA). Marx espera que los precios de producción superen a los
       valores en las ramas de composición alta: correlación positiva.

3. Trabajo incorporado en el comercio exterior (reemplaza, para 2000–2014, la aproximación sin insumos intermedios):
       horas cedidas = Σ_j λ_j · exportaciones_j;  horas recibidas = Σ_j λ̄_j · importaciones_j · (X / M)
   (las importaciones se escalan al valor de las exportaciones para no confundir la transferencia con el déficit).

4. La hora de trabajo en el mercado mundial (2000–último año). Según Marx, el trabajo nacional más productivo cuenta en
   el mercado mundial como trabajo más intenso. Ponderación de cada país: w_c = μ_c / μ_mundo, con μ = PIB en dólares /
   horas trabajadas (Banco Mundial y PWT). Masa mundial ponderada = Σ plustrabajo_c · w_c. Equivale a convertir el
   plusvalor de cada país, medido en dólares, a horas con la expresión monetaria media del mercado mundial.

5. F4 v2 — interpretación de Moseley (central) y variante temporal TSSI (contraste). Por país y año, con las ramas
   productivas y todo en moneda nacional (WIOD SEA; las tablas insumo-producto se convierten con GO_SEA / GO_NIOT):
       c_j = insumos de ramas productivas (nacionales e importados);  v_j = remuneración de los asalariados (COMP);
       K_j = stock nominal de capital fijo;  a_j = ingreso laboral de los trabajadores por cuenta propia (LAB − COMP),
       que produce valor pero no plusvalor;  S = Σ (GO_j − c_j − v_j − a_j), que incluye los insumos de ramas
       improductivas (gastos pagados con plusvalor);  e = S / V;  r = S / (Σ K + Σ V)  (la tasa del sitio, pv/(c + v)).
   Moseley: c y v son las magnitudes dinerarias efectivas y son las mismas para valores y precios de producción:
       valor            W_j  = c_j + a_j + v_j (1 + e)                 (tasa de plusvalor uniforme)
       precio de prod.  PP_j = c_j + a_j + v_j + r (K_j + v_j)
   Σ W = Σ PP = Σ GO, y el plusvalor total es igual a la ganancia total: la transformación sólo redistribuye.
   TSSI: los insumos se valúan a los precios con que entraron a la producción, c_j / (II_PI_t / II_PI_t−1), y el capital
   adelantado es el stock al cierre del año anterior; el valor nuevo es Σ GO − Σ c^T. Con ello cambian S, e y r.
   Medidas: desviación media de los mercados respecto de W y de PP; parte del plusvalor redistribuida
   (Σ |PP − W| / 2 / S); dispersión (coeficiente de variación ponderado por el capital) de las tasas de ganancia
   efectivas por rama frente a las tasas «en valores» e·v_j/(K_j + v_j): si la competencia iguala las tasas, la
   dispersión efectiva debe ser menor que la que habría si cada rama realizara su propio plusvalor.

Interpretación: el sitio trabaja en el nivel agregado macromonetario, donde la transformación no altera ni la masa ni la
tasa de plusvalor totales. Los valores por rama no son «trabajo incorporado» natural: son una aproximación al tiempo
de trabajo socialmente necesario como determinación de la totalidad social, que permite ver cómo la formación de los
precios redistribuye el plusvalor entre ramas y países.
"""
import glob, os, zipfile

import numpy as np, pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIP = os.path.join(RAIZ, 'datos_cache', 'externo', 'wiod_niots.zip')
RAMAS = ['A01', 'A02', 'A03', 'B', 'C10-C12', 'C13-C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25',
         'C26', 'C27', 'C28', 'C29', 'C30', 'C31_C32', 'C33', 'D35', 'E36', 'E37-E39', 'F', 'G45', 'G46', 'G47', 'H49', 'H50',
         'H51', 'H52', 'H53', 'I', 'J58', 'J59_J60', 'J61', 'J62_J63', 'K64', 'K65', 'K66', 'L68', 'M69_M70', 'M71', 'M72',
         'M73', 'M74_M75', 'N', 'O84', 'P85', 'Q', 'R_S', 'T', 'U']
NO_VALOR = ['G45', 'G46', 'G47', 'K64', 'K65', 'K66', 'L68', 'M69_M70', 'M73', 'O84', 'P85', 'Q', 'T', 'U']
PROD = np.array([r not in NO_VALOR for r in RAMAS])
HORAS_CHINA = 46 * 50
NOMBRES = {'A01': 'Agricultura', 'A02': 'Silvicultura', 'A03': 'Pesca', 'B': 'Minería', 'C10-C12': 'Alimentos y bebidas',
           'C13-C15': 'Textil y confección', 'C16': 'Madera', 'C17': 'Papel', 'C18': 'Imprenta', 'C19': 'Refinación de petróleo',
           'C20': 'Química', 'C21': 'Farmacéutica', 'C22': 'Caucho y plástico', 'C23': 'Minerales no metálicos',
           'C24': 'Metales básicos', 'C25': 'Productos metálicos', 'C26': 'Computación y electrónica', 'C27': 'Equipo eléctrico',
           'C28': 'Maquinaria', 'C29': 'Automotriz', 'C30': 'Otro equipo de transporte', 'C31_C32': 'Muebles y otras manufacturas',
           'C33': 'Reparación de maquinaria', 'D35': 'Electricidad y gas', 'E36': 'Agua', 'E37-E39': 'Residuos',
           'F': 'Construcción', 'H49': 'Transporte terrestre', 'H50': 'Transporte marítimo', 'H51': 'Transporte aéreo',
           'H52': 'Almacenamiento', 'H53': 'Correo', 'I': 'Alojamiento y comidas', 'J58': 'Edición', 'J59_J60': 'Audiovisual',
           'J61': 'Telecomunicaciones', 'J62_J63': 'Informática', 'M71': 'Arquitectura e ingeniería', 'M72': 'Investigación',
           'M74_M75': 'Otros servicios profesionales', 'N': 'Servicios administrativos', 'R_S': 'Otros servicios'}


def _leer_niots():
    """{pais: DataFrame del archivo}; cada archivo tiene todos los años."""
    out = {}
    z = zipfile.ZipFile(ZIP)
    for n in sorted(z.namelist()):
        if not n.endswith('.xlsx'): continue
        c = os.path.basename(n)[:3]
        with z.open(n) as f:
            d = pd.read_excel(f, sheet_name='National IO-tables', header=None)
        cols = list(d.iloc[0]); d = d.iloc[2:].copy(); d.columns = ['anio', 'code', 'desc', 'origen'] + cols[4:]
        d['anio'] = pd.to_numeric(d.anio, errors='coerce')
        out[c] = d
    return out


def _sea(dir_datos):
    for fn in (os.path.join(dir_datos, 'wiod', 'Socio_Economic_Accounts.xlsx'), os.path.join(RAIZ, 'datos_cache', 'wiod_sea.xlsx')):
        if os.path.exists(fn): break
    s = pd.read_excel(fn, sheet_name='DATA')
    s = s.melt(id_vars=['country', 'variable', 'description', 'code'], var_name='anio', value_name='v')
    s['anio'] = pd.to_numeric(s.anio.astype(str).str.replace('_', ''), errors='coerce')
    return s.pivot_table(index=['country', 'anio', 'code'], columns='variable', values='v')


def _matrices(d, y):
    t = d[d.anio == y]
    dom = t[t.origen == 'Domestic'].set_index('code').reindex(RAMAS)
    imp = t[t.origen == 'Imports'].set_index('code').reindex(RAMAS)
    tot = t[t.origen == 'TOT'].set_index('code')
    x = pd.to_numeric(tot.loc['GO', RAMAS], errors='coerce').fillna(0).values.astype(float)
    Zd = dom[RAMAS].apply(pd.to_numeric, errors='coerce').fillna(0).values.astype(float)
    Zm = imp[RAMAS].apply(pd.to_numeric, errors='coerce').fillna(0).values.astype(float)
    exp = pd.to_numeric(dom['EXP'], errors='coerce').fillna(0).values.astype(float)
    fd = ['CONS_h', 'CONS_np', 'CONS_g', 'GFCF', 'INVEN']                         # la columna GO de las importaciones viene en cero
    imp_tot = Zm.sum(axis=1) + imp[fd].apply(pd.to_numeric, errors='coerce').fillna(0).values.astype(float).sum(axis=1)
    with np.errstate(divide='ignore', invalid='ignore'):
        A = np.where(x > 0, Zd / x, 0.0); M = np.where(x > 0, Zm / x, 0.0)
    return x, A, M, exp.clip(min=0), imp_tot.clip(min=0)


def _horas(S, c, y):
    try:
        g = S.loc[(c, y)].reindex(RAMAS)
    except KeyError:
        return None
    emp = g['EMP'].astype(float)
    if c == 'CHN' or g.get('H_EMPE') is None or g['H_EMPE'].isna().all():
        return (emp * HORAS_CHINA / 1000).fillna(0).values                       # millones de horas
    he, empe = g['H_EMPE'].astype(float), g['EMPE'].astype(float)
    hpp = (he / empe).where(empe > 0)
    hpp = hpp.fillna((he.sum() / empe.sum()) if empe.sum() > 0 else 2.0)        # horas (en miles) por ocupado
    return (emp * hpp).fillna(0).values


def calcular(dir_datos, dir_out, mundo_paises=None):
    if not os.path.exists(ZIP):
        print('Transformación: faltan las tablas insumo-producto de WIOD (datos_cache/externo/wiod_niots.zip)'); return {}
    N = _leer_niots(); S = _sea(dir_datos)
    anios = sorted({int(a) for d in N.values() for a in d.anio.dropna().unique()})
    p = PROD; I = np.eye(p.sum())
    ramas_f, desv_f, com_f = [], [], []
    for y in anios:
        datos = {}
        for c, d in N.items():
            x, A, M, exp, imp = _matrices(d, y)
            H = _horas(S, c, y)
            if H is None or x.sum() <= 0: continue
            with np.errstate(divide='ignore', invalid='ignore'):
                l = np.where(x > 0, H / x, 0.0)                                          # horas por dólar
            datos[c] = (x, A, M, exp, imp, l)
        lbar = np.zeros(p.sum()); lam = {}
        for _ in range(8):                                                               # converge en pocas vueltas
            for c, (x, A, M, exp, imp, l) in datos.items():
                Ainv = np.linalg.pinv(I - A[np.ix_(p, p)])
                lam[c] = (l[p] + lbar @ M[np.ix_(p, p)]) @ Ainv
            num = sum(lam[c] * datos[c][3][p] for c in lam); den = sum(datos[c][3][p] for c in lam)
            with np.errstate(divide='ignore', invalid='ignore'):
                nuevo = np.where(den > 0, num / den, 0.0)
            if np.allclose(nuevo, lbar, rtol=1e-6): break
            lbar = nuevo
        for c, (x, A, M, exp, imp, l) in datos.items():
            xp, lp = x[p], lam[c]
            ok = (xp > 0) & (lp > 0)
            mu = xp[ok].sum() / (lp[ok] * xp[ok]).sum()                                   # dólares por hora
            v = mu * lp
            try:
                g = S.loc[(c, y)].reindex(RAMAS)
                comp = (g['K'].astype(float) / g['LAB'].astype(float)).values[p]   # LAB incluye el ingreso laboral de los no asalariados
            except KeyError:
                comp = np.full(p.sum(), np.nan)
            for j, r in enumerate(np.array(RAMAS)[p]):
                if ok[j]:
                    ramas_f.append(dict(pais=c, anio=y, rama=r, nombre=NOMBRES.get(r, r), produccion_musd=xp[j],
                                        horas_por_dolar=lp[j], valor_precio=v[j], precio_valor=1 / v[j], composicion_K_v=comp[j]))
            mad = float((xp[ok] * np.abs(v[ok] - 1)).sum() / xp[ok].sum())
            cc = pd.DataFrame({'pv': 1 / v[ok], 'k': comp[ok]}).replace([np.inf, -np.inf], np.nan).dropna()
            rho = float(cc.pv.rank().corr(cc.k.rank())) if len(cc) > 5 else np.nan
            desv_f.append(dict(pais=c, anio=y, ramas=int(ok.sum()), desviacion_media=mad, spearman_precio_valor_composicion=rho,
                               expresion_monetaria_usd_hora=mu))
            Xp, Mp = exp[p].sum(), imp[p].sum()
            hx = float((lp * exp[p]).sum()); hm = float((lbar * imp[p]).sum())
            if Xp > 0 and Mp > 0:
                hrec = hm * Xp / Mp
                com_f.append(dict(pais=c, anio=y, horas_cedidas_mill=hx, horas_recibidas_mill=hrec, transferencia_mill_h=hrec - hx,
                                  horas_totales_mill=float(datos[c][5][p] @ x[p]), transferencia_pct_horas=(hrec - hx) / float(datos[c][5][p] @ x[p]) * 100))
    R = pd.DataFrame(ramas_f); D = pd.DataFrame(desv_f); C = pd.DataFrame(com_f)
    R.to_csv(os.path.join(dir_out, 'transformacion_ramas.csv'), index=False)
    D.to_csv(os.path.join(dir_out, 'transformacion_desviaciones.csv'), index=False)
    C.to_csv(os.path.join(dir_out, 'transformacion_comercio.csv'), index=False)
    MT, MR = moseley_tssi(N, S, anios)
    MT.to_csv(os.path.join(dir_out, 'transformacion_moseley_tssi.csv'), index=False)
    MR.to_csv(os.path.join(dir_out, 'transformacion_moseley_ramas.csv'), index=False)
    W = ponderacion_mundial(dir_datos, mundo_paises) if mundo_paises is not None else pd.DataFrame()
    if not W.empty: W.to_csv(os.path.join(dir_out, 'transformacion_masa_ponderada.csv'), index=False)
    return dict(R=R, D=D, C=C, W=W, MT=MT, MR=MR)


def ponderacion_mundial(dir_datos, P, variante='educación y salud públicas fuera'):
    """Masa mundial de plustrabajo con cada hora nacional ponderada por la expresión monetaria relativa de su país."""
    from sismografo.intercambio import CACHE
    if not os.path.exists(CACHE): return pd.DataFrame()
    wb = pd.read_csv(CACHE).pivot_table(index=['iso3', 'anio'], columns='serie', values='valor')
    fn = os.path.join(dir_datos, 'pwt', 'pwt110.dta')
    if not os.path.exists(fn): fn = os.path.join(RAIZ, 'datos_cache', 'pwt110.dta')
    pwt = pd.read_stata(fn, columns=['countrycode', 'year', 'emp', 'avh'])
    pwt['H'] = pwt.emp.astype(float) * pwt.avh.astype(float) * 1e6
    pwt = pwt.rename(columns={'countrycode': 'iso3', 'year': 'anio'}).set_index(['iso3', 'anio'])[['H']]
    d = wb[['pib']].join(pwt, how='inner').dropna()
    d = d[(d.pib > 0) & (d.H > 0)]
    mu = (d.pib / d.H).rename('mu').reset_index().rename(columns={'iso3': 'pais'})
    mu = mu.pivot_table(index='anio', columns='pais', values='mu')
    Q = P[P.variante == variante]
    anios = sorted(Q.anio.unique()); mu = mu.reindex(sorted(set(mu.index) | set(anios))).ffill()
    filas = []
    for y in anios:
        g = Q[Q.anio == y].set_index('pais')
        m = mu.loc[y].reindex(g.index)
        ok = m.notna()
        if ok.sum() < 30: continue
        h = g.horas_mill[ok]; mw = float((m[ok] * h).sum() / h.sum())               # μ medio de las horas productivas
        w = m[ok] / mw
        filas.append(dict(anio=int(y), paises=int(ok.sum()), plustrabajo_mmh=float(g.plustrabajo_mill_h[ok].sum() / 1000),
                          plustrabajo_ponderado_mmh=float((g.plustrabajo_mill_h[ok] * w).sum() / 1000),
                          asalariados_ponderados_mill=float((g.obreros_mill[ok] * w).sum()),
                          peso_china=float(w.get('CHN', np.nan)), peso_india=float(w.get('IND', np.nan)), peso_eeuu=float(w.get('USA', np.nan)),
                          pct_china_ponderado=float((g.plustrabajo_mill_h[ok] * w).get('CHN', 0) / (g.plustrabajo_mill_h[ok] * w).sum() * 100)))
    return pd.DataFrame(filas)


def _cv(x, w):
    """Coeficiente de variación ponderado."""
    ok = np.isfinite(x) & np.isfinite(w) & (w > 0)
    if ok.sum() < 5: return np.nan
    m = np.average(x[ok], weights=w[ok])
    return float(np.sqrt(np.average((x[ok] - m) ** 2, weights=w[ok])) / abs(m)) if m else np.nan


def moseley_tssi(N, S, anios):
    """F4 v2: valores y precios de producción con la interpretación de Moseley y la variante temporal (TSSI)."""
    p = PROD; rp = np.array(RAMAS)[p]
    filas, ramas = [], []
    for c, d in N.items():
        prev = None
        for y in anios:
            x, A, M, exp, imp, = _matrices(d, y)[:5]
            try:
                g = S.loc[(c, y)].reindex(RAMAS).astype(float)
            except KeyError:
                prev = None; continue
            go_sea = g['GO'].values
            if x.sum() <= 0 or not np.nansum(go_sea) > 0: prev = None; continue
            fx = np.nansum(go_sea) / x.sum()                                     # moneda nacional por dólar
            Z = (A + M) * x                                                      # insumos (columnas = rama que compra)
            cj = Z[np.ix_(p, p)].sum(axis=0) * fx                                # insumos productivos, moneda nacional
            GO = x[p] * fx; v = g['COMP'].values[p]; K = g['K'].values[p]
            ce = np.where(np.isfinite(g['LAB'].values[p]), g['LAB'].values[p], v) - v  # ingreso laboral de los no asalariados
            ce = np.where(np.isfinite(ce) & (ce > 0), ce, 0.0)
            ok = (GO > 0) & np.isfinite(v) & np.isfinite(K) & (K > 0)
            if ok.sum() < 10: prev = None; continue
            def medir(cc, KK, var):
                Sx = float((GO[ok] - cc[ok] - v[ok] - ce[ok]).sum()); V = float(v[ok].sum())
                e = Sx / V; r = Sx / (float(KK[ok].sum()) + V)
                W = cc + ce + v * (1 + e); PP = cc + ce + v + r * (KK + v)
                with np.errstate(divide='ignore', invalid='ignore'):
                    rate = (GO - cc - v - ce) / (KK + v); rate_w = e * v / (KK + v)
                res = dict(pais=c, anio=y, interpretacion=var, e=e, r=r,
                           desv_mercado_valor=float((GO[ok] * np.abs(W[ok] / GO[ok] - 1)).sum() / GO[ok].sum()),
                           desv_mercado_pp=float((GO[ok] * np.abs(PP[ok] / GO[ok] - 1)).sum() / GO[ok].sum()),
                           plusvalor_redistribuido_pct=float(np.abs(PP[ok] - W[ok]).sum() / 2 / Sx * 100),
                           cv_tasas_efectivas=_cv(rate[ok], (KK + v)[ok]), cv_tasas_en_valores=_cv(rate_w[ok], (KK + v)[ok]),
                           plusvalor_usd_mill=Sx / fx, capital_usd_mill=(float(KK[ok].sum()) + V) / fx)
                return res, W, PP, rate, rate_w
            res, W, PP, rate, rate_w = medir(cj, K, 'Moseley')
            filas.append(res)
            for j in np.where(ok)[0]:
                ramas.append(dict(pais=c, anio=y, rama=rp[j], nombre=NOMBRES.get(rp[j], rp[j]), produccion_usd_mill=GO[j] / fx,
                                  valor_sobre_precio=W[j] / GO[j], pp_sobre_precio=PP[j] / GO[j], transferencia_pct_valor=(PP[j] - W[j]) / W[j] * 100,
                                  tasa_efectiva=rate[j], tasa_en_valores=rate_w[j], tasa_general=res['r']))
            if prev is not None:
                pi = g['II_PI'].values[p] / prev['II_PI']
                pi = np.where(np.isfinite(pi) & (pi > 0), pi, np.nanmedian(pi[np.isfinite(pi) & (pi > 0)]) if np.isfinite(pi).any() else 1.0)
                Kp = np.where(np.isfinite(prev['K']) & (prev['K'] > 0), prev['K'], K)
                filas.append(medir(cj / pi, Kp, 'TSSI')[0])
            prev = dict(II_PI=g['II_PI'].values[p], K=K)
    return pd.DataFrame(filas), pd.DataFrame(ramas)
