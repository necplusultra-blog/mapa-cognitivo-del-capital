"""EE.UU.: multiverso de la tasa de ganancia, plusvalor ampliado y quiebres endógenos.

Criterio productivo/improductivo de la investigación «Los límites inmanentes del capital»
(Jiménez Cea). Improductivo: comercio, finanzas y seguros, inmobiliario
y servicios jurídicos. El trabajo que produce software, I+D y otros productos de propiedad
intelectual en empresas capitalistas es productivo.
"""
import csv, collections, itertools, os
import numpy as np, pandas as pd
from .quiebres import breaks
from .descarga import CES_SUPERSECTORES

INICIO = 1948
INICIO_C = 1972   # corrección intra-rama: los datos CES por supersector comienzan en 1972


def _flat(fn):
    d = collections.defaultdict(dict)
    with open(fn) as f:
        r = csv.reader(f); next(r)
        for code, yr, val in r:
            if yr.isdigit():
                try: d[code][int(yr)] = float(val.replace(',', ''))
                except ValueError: pass
    return d


def _fred_anual(path):
    d = pd.read_csv(path, parse_dates=[0])
    return pd.to_numeric(d.iloc[:, 1], errors='coerce').groupby(d.iloc[:, 0].dt.year).mean()


class Datos:
    def __init__(self, dir_datos):
        b = os.path.join(dir_datos, 'bea'); f = os.path.join(dir_datos, 'fred')
        self.dir_fred = f
        self.N = _flat(os.path.join(b, 'NipaDataA.txt'))
        self.F = _flat(os.path.join(b, 'FixedAssets.txt'))
        # último año con datos completos en las series clave
        clave = [self.N['A195RC'], self.N['W326RC'], self.F['k1ptotl2es00'], self.F['k3ntotl1es00']]
        self.FIN = min(max(s) for s in clave)
        self.YEARS = list(range(INICIO, self.FIN + 1))
        self.INV = _fred_anual(os.path.join(f, 'BOGZ1FL105020005A.csv')).reindex(self.YEARS)
        self.CU = _fred_anual(os.path.join(f, 'CUMFNS.csv')).reindex(self.YEARS)
        self.b = b

    def s(self, src, code, default=None):
        src = self.N if src == 'N' else self.F
        if code not in src:
            if default is not None: return pd.Series(default, index=self.YEARS, dtype=float)
            raise KeyError(code)
        return pd.Series(src[code]).reindex(self.YEARS).astype(float)

    def fa(self, prefix, tail):
        return self.s('F', prefix + tail, default=0.0)


U_SIC = ['Wholesale trade', 'Retail trade', 'Finance, insurance, and real estate', 'Legal services']
U_NAICS = ['Wholesale trade', 'Retail trade', 'Finance and insurance', 'Real estate and rental and leasing', 'Legal services']


def _comp_rows(df, names, years):
    comp = df[df[0] == 'COMP']; tot = pd.Series(0.0, index=years)
    for nm in names:
        row = comp[comp[1].astype(str).str.strip() == nm]
        assert len(row) == 1, (nm, len(row))
        tot += pd.Series(pd.to_numeric(row.iloc[0, 2:2 + len(years)], errors='coerce').values, index=years)
    return tot


def comp_improductiva(D):
    """Remuneración en ramas improductivas, empalmada SIC72 (1947–86) → NAICS (1987–96) → NAICS (1997–)."""
    sic = pd.read_excel(os.path.join(D.b, 'GDPbyInd_VA_SIC.xls'), sheet_name='72SIC_Components of VA', header=None, engine='calamine')
    ys = [int(float(y)) for y in sic.iloc[0, 2:] if pd.notna(y)]
    A = _comp_rows(sic, U_SIC, ys)
    nai = pd.read_excel(os.path.join(D.b, 'GDPbyInd_VA_NAICS_1947-1997.xls'), sheet_name='1987-97_02NAICS_VA Components', header=None, engine='calamine')
    ys = [int(float(y)) for y in nai.iloc[0, 2:] if pd.notna(y)]
    C = _comp_rows(nai, U_NAICS, ys)
    va = pd.read_excel(os.path.join(D.b, 'ValueAdded.xlsx'), sheet_name='TVA113-A', header=None, engine='calamine')
    hdr_row = va.index[va.iloc[:, 0].astype(str).str.strip() == 'Line'][0]
    hdr = va.iloc[hdr_row]
    ycols = [c for c in va.columns if str(hdr[c]).split('.')[0].isdigit()]
    ys = [int(str(hdr[c]).split('.')[0]) for c in ycols]
    lab = va[1].fillna('').astype(str)
    Dd = pd.Series(0.0, index=ys)
    for nm in U_NAICS:
        idx = [i for i in va.index if lab[i].strip() == nm]
        assert len(idx) == 1, (nm, idx)
        assert lab[idx[0] + 1].strip() == 'Compensation of employees'
        Dd += pd.Series(pd.to_numeric(va.loc[idx[0] + 1, ycols], errors='coerce').values, index=ys)
    r1 = Dd[1997] / C[1997]; Cs = C * r1
    r2 = Cs[1987] / A[1987]; As = A * r2
    U = pd.concat([As[As.index < 1987], Cs[(Cs.index >= 1987) & (Cs.index < 1997)], Dd[Dd.index >= 1997]])
    return U.reindex(D.YEARS), {'1997 NAICS/NAICS87-97': round(r1, 4), '1987 NAICS/SIC72': round(r2, 4)}


# Proporción de los empleos de cada supersector que no corresponde a capital que se valoriza (2022, BLS y
# Nonprofit Employment Data Project, GMU): instituciones sin fines de lucro (501(c)(3)). El BLS indica que estas
# proporciones casi no cambian entre 2007 y 2022; se mantienen constantes.
ONG_EDU, ONG_SALUD, ONG_ASIST, ONG_ORG = 0.70, 0.43, 0.40, 0.60


def fraccion_capitalista(D, code):
    """Fracción de los obreros de producción de un supersector CES que es trabajo asalariado por capital productivo.
    - Servicios profesionales y empresariales: se restan servicios jurídicos (5411) y contables (5412), ramas de
      circulación (el criterio por ramas de V_b sólo puede separar los jurídicos; véase metodología §3). La publicidad (5418) no tiene serie mensual en FRED.
    - Educación y salud privadas: se resta la parte empleada por instituciones sin fines de lucro.
    - Otros servicios: se resta la parte sin fines de lucro de las organizaciones religiosas, civiles y similares (813).
    Antes de 1990 (sin detalle por industria) se usa la proporción de 1990."""
    f = lambda s: _fred_anual(os.path.join(D.dir_fred, s + '.csv')).reindex(D.YEARS)
    try:
        if code == '60000000':
            r = 1 - (f('CES6054110001') + f('CES6054120001')) / f('USPBS')
        elif code == '65000000':
            salud = f('CES6562000001') - f('CES6562400001')
            r = 1 - (ONG_EDU * f('CES6561000001') + ONG_SALUD * salud + ONG_ASIST * f('CES6562400001')) / f('USEHS')
        elif code == '80000000':
            r = 1 - ONG_ORG * f('CES8081300001') / f('USSERV')
        else:
            return pd.Series(1.0, index=D.YEARS)
        return r.bfill().ffill()
    except FileNotFoundError:
        return pd.Series(1.0, index=D.YEARS)


def v_produccion(D):
    """Corrección intra-rama (D2c): salarios de trabajadores de producción y no supervisores en
    supersectores productivos (BLS CES), escalados por la razón remuneración/salarios del sector empresarial."""
    tot = None; D.N_prod = None; D.H_prod = None
    for code, (nm, prod) in CES_SUPERSECTORES.items():
        if not prod: continue
        emp = _fred_anual(os.path.join(D.dir_fred, f'CES{code}06.csv'))
        ahe = _fred_anual(os.path.join(D.dir_fred, f'CES{code}08.csv'))
        hrs_path = os.path.join(D.dir_fred, f'CES{code}07.csv')
        hrs = _fred_anual(hrs_path if os.path.exists(hrs_path) and code != '30000000' else os.path.join(D.dir_fred, 'AWHMAN.csv'))
        emp = emp * fraccion_capitalista(D, code).reindex(emp.index).fillna(1.0)
        pay = emp * 1000 * ahe * hrs * 52 / 1e6   # millones de USD
        tot = pay if tot is None else tot + pay
        n_, h_ = emp / 1000, emp * 1000 * hrs * 52 / 1e6        # millones de trabajadores; millones de horas al año
        D.N_prod = n_ if D.N_prod is None else D.N_prod + n_
        D.H_prod = h_ if D.H_prod is None else D.H_prod + h_
    markup = (D.s('N', 'A442RC') + D.s('N', 'W462RC')) / (D.s('N', 'A443RC') + D.s('N', 'W463RC'))
    return (tot.reindex(D.YEARS) * markup)


SECT = {
    'corp': dict(nos='W322RC', pbt='A445RC', pat='W273RC', k='ptotl2es00', ip='ntotl2ip00'),
    'nfc': dict(nos='W326RC', pbt='A463RC', pat='W328RC', k='pnofi2es00', ip='nnofi2ip00'),
}


def calcular(dir_datos, dir_out):
    os.makedirs(dir_out, exist_ok=True)
    D = Datos(dir_datos); Y = D.YEARS
    COMP_U, empalmes = comp_improductiva(D)
    COMP_BUS = D.s('N', 'A442RC') + D.s('N', 'W462RC')
    # el PIB por industria puede ir un año detrás de las cuentas nacionales: se extiende la última proporción
    COMP_U = (COMP_U / COMP_BUS).ffill() * COMP_BUS
    V = {'a': COMP_BUS, 'b': COMP_BUS - COMP_U, 'c': v_produccion(D)}
    GVA = D.s('N', 'A195RC') - (D.s('N', 'A2009C') - D.s('N', 'B701RC'))   # empresarial sin vivienda arrendada
    # Explotación secundaria (auditoría B4; decisión del autor, 24 nov. 2026): los servicios financieros que los hogares
    # pagan con sus salarios (FISIM y comisiones, NIPA 2.4.5) son plusvalor desplazado desde el salario, no plusvalor
    # producido. Se restan del plusvalor ampliado en la parte que corresponde a los salarios (remuneración / ingreso
    # personal). Las especificaciones corporativas («a la manera de» los autores) no cambian.
    D.FH_TOTAL = D.s('N', 'DFNLRC')
    D.FH = D.FH_TOTAL * D.s('N', 'A033RC') / D.s('N', 'A065RC')
    GVA = GVA - D.FH
    DEFL = D.s('N', 'A191RD')

    def corp(sector, profit, val, gross, ipp, inv, util):
        S = SECT[sector]; kc, dc = ('k1', 'm1') if val == 'cc' else ('k3', 'm3')
        p = D.s('N', S[profit]); K = D.fa(kc, S['k'])
        Dcc, Dv = D.fa('m1', S['k']), D.fa(dc, S['k'])
        p = p + Dcc - Dv
        if gross: p = p + Dv
        if ipp == 'excl':
            p = p - D.fa('i3', S['ip']) + (0 if gross else D.fa(dc, S['ip'])); K = K - D.fa(kc, S['ip'])
        if inv: K = K + D.INV
        r = p / K
        return r * (D.CU.mean() / D.CU) if util else r

    def bus(prod, val, gross, ipp, kscope, util, den='K'):
        """den='K+V': denominador = capital fijo adelantado + capital variable (flujo salarial anual del año).
        El flujo anual supone una rotación al año del capital variable; con más rotaciones el v adelantado sería menor."""
        kc, dc = ('k1', 'm1') if val == 'cc' else ('k3', 'm3')
        sub = lambda pre, t: D.fa(pre, f'ntotl1{t}') - D.fa(pre, f'ntotl8{t}') - D.fa(pre, f'ntotl5{t}')
        K = sub(kc, 'es00'); Dv = sub(dc, 'es00')
        S_ = GVA - V[prod]
        if not gross: S_ = S_ - Dv
        if ipp == 'excl':
            S_ = S_ - sub('i3', 'ip00') + (0 if gross else sub(dc, 'ip00')); K = K - sub(kc, 'ip00')
        if kscope == 'prod':
            # K sólo de ramas productivas: se quita el capital de comercio, finanzas y seguros, servicios jurídicos,
            # inmobiliario no residencial y alquiler (las ramas que §3 declara improductivas). Si la PPI ya salió de K
            # (ipp='excl'), de esas ramas sólo se quitan equipo y estructuras, para no restar su PPI dos veces.
            # Coherencia con V(b): como los salarios de esas ramas quedan en S, también su depreciación se paga con
            # plusvalor y no se resta del numerador (auditoría de nov. 2026).
            sufs = ('eq00', 'st00') if ipp == 'excl' else ('es00',)
            ramas = ('n42001', 'n44RT1', 'n52001', 'n54111', 'n53201', 'p53101')
            K_u = sum(D.fa(kc, r + s) for r in ramas for s in sufs) - D.fa(kc, 'r53101es00')
            D_u = sum(D.fa(dc, r + s) for r in ramas for s in sufs) - D.fa(dc, 'r53101es00')
            K = K - K_u
            if not gross: S_ = S_ + D_u
        r = S_ / (K + V[prod]) if den == 'K+V' else S_ / K
        return (r * (D.CU.mean() / D.CU) if util else r), S_, K

    rows, meta, SK = [], [], {}
    for sector, profit, val, gross, ipp, inv, util in itertools.product(['corp', 'nfc'], ['nos', 'pbt', 'pat'], ['cc', 'hc'], [False, True], ['incl', 'excl'], [False, True], [False, True]):
        sid = f'C|{sector}|{profit}|{val}|{"bruta" if gross else "neta"}|ppi-{ipp}|{"inv" if inv else "noinv"}|{"util" if util else "noutil"}'
        rows.append(corp(sector, profit, val, gross, ipp, inv, util).rename(sid))
        meta.append(dict(id=sid, familia='corporativa', D6=sector, D1=profit, D2='a', D3=val, D4='bruta' if gross else 'neta', D5=ipp, inventarios=inv, D8=util, K='todo', denominador='K'))
    for prod, val, gross, ipp, kscope, util, den in itertools.product(['a', 'b', 'c'], ['cc', 'hc'], [False, True], ['incl', 'excl'], ['todo', 'prod'], [False, True], ['K', 'K+V']):
        if prod == 'a' and kscope == 'prod': continue
        sid = f'B|{prod}|{val}|{"bruta" if gross else "neta"}|ppi-{ipp}|K-{kscope}|{"util" if util else "noutil"}' + ('|den-KV' if den == 'K+V' else '')
        r_, S_b, K_b = bus(prod, val, gross, ipp, kscope, util, den)
        rows.append(r_.rename(sid))
        if not util and den == 'K': SK[sid] = (S_b, K_b, V[prod])   # para la descomposición de contratendencias
        meta.append(dict(id=sid, familia={'a': 'empresarial: todo productivo', 'b': 'empresarial: plusvalor ampliado (por ramas)', 'c': 'empresarial: plusvalor ampliado (corrección intra-rama)'}[prod],
                         D6='empresarial', D1='excedente amplio' if prod == 'a' else 'plusvalor ampliado', D2=prod, D3=val, D4='bruta' if gross else 'neta', D5=ipp, inventarios=False, D8=util, K=kscope, denominador=den))
    R = pd.concat(rows, axis=1); M = pd.DataFrame(meta).set_index('id')
    principal = [c for c in R.columns if not c.startswith('B|c|')]
    Rc = R[[c for c in R.columns if c.startswith('B|c|')]].loc[INICIO_C:]
    assert R[principal].notna().all().all(), R[principal].columns[R[principal].isna().any()].tolist()

    yrs = np.array(Y)
    M['quiebres'] = [breaks(R[c].values, yrs) if c in principal else breaks(Rc[c].values, np.array(Rc.index)) for c in M.index]

    # sensibilidad del detector de quiebres (F1.4)
    configs = [('h=6, BIC', 6, 'bic'), ('h=8, BIC (base)', 8, 'bic'), ('h=10, BIC', 10, 'bic'), ('h=8, LWZ', 8, 'lwz')]
    sens = []
    for etiqueta, h, crit in configs:
        cnt = collections.Counter()
        nq = []
        for c in principal:
            b = M.loc[c, 'quiebres'] if (h, crit) == (8, 'bic') else breaks(R[c].values, yrs, h=h, crit=crit)
            cnt.update(b); nq.append(len(b))
        top = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))[:6]
        sens.append(dict(configuracion=etiqueta, quiebres_medios=round(float(np.mean(nq)), 2),
                         anios_mas_frecuentes=', '.join(f'{y} ({n})' for y, n in top)))
    pd.DataFrame(sens).to_csv(os.path.join(dir_out, 'eeuu_sensibilidad_quiebres.csv'), index=False)

    # robustez decenal (sólo el multiverso principal, ventana común)
    Rp = R[principal]
    dec = pd.Series([f'{(y // 10) * 10}s' if y < 2020 else f'2020–{str(D.FIN)[2:]}' for y in Y], index=Y)
    DM = Rp.groupby(dec).mean(); DM = DM.loc[sorted(DM.index)]
    trans = []
    for a, b in zip(DM.index[:-1], DM.index[1:]):
        down = float((np.sign(DM.loc[b] - DM.loc[a]) < 0).mean())
        trans.append(dict(tramo=f'{a} → {b}', pct_baja=round(100 * down, 1), clase='robusto: baja' if down >= .9 else 'robusto: sube' if down <= .1 else 'dependiente de la teoría'))

    masa = {}
    for prod in ('b', 'c'):
        r, S_, K = bus(prod, 'cc', False, 'incl', 'todo', False)
        masa[prod] = pd.DataFrame({'S': S_, 'S_real_2017': S_ / DEFL * 100, 'V': V[prod], 'K': K, 'e': S_ / V[prod], 'K_V': K / V[prod], 'r': r})
    masa['c'] = masa['c'].loc[INICIO_C:]
    # Del dinero al tiempo de trabajo (lectura macromonetaria): la tasa de plusvalor medida en dinero es la
    # proporción plustrabajo/trabajo necesario de los obreros productivos. Masa = e × número de obreros.
    c = masa['c']; N_ = D.N_prod.reindex(c.index); H_ = D.H_prod.reindex(c.index)
    c['obreros_productivos_mill'] = N_
    c['horas_productivas_mill'] = H_
    c['horas_plustrabajo_mill'] = H_ * c['e'] / (1 + c['e'])
    c['semana_horas'] = H_ / N_ / 52
    c['semana_necesario'] = c['semana_horas'] / (1 + c['e'])
    c['semana_plustrabajo'] = c['semana_horas'] - c['semana_necesario']
    # Semana media pagada (CES): promedio de tiempo completo y parcial; baja sobre todo por composición. Para la
    # jornada de un obrero de tiempo completo se usa la semana legal de 40 h con la misma e.
    c['semana_tc_necesario'] = 40 / (1 + c['e'])
    c['semana_tc_plustrabajo'] = 40 - c['semana_tc_necesario']
    c['plusvalor_por_obrero_real'] = c['S_real_2017'] / N_                       # USD de 2017 por obrero productivo
    c['expresion_monetaria_hora'] = (c['S'] + c['V']) / H_                        # USD corrientes de valor nuevo por hora
    c['expresion_monetaria_hora_real'] = c['expresion_monetaria_hora'] / DEFL.reindex(c.index) * 100
    masa['c'] = c

    R.to_csv(os.path.join(dir_out, 'eeuu_tasas_especificaciones.csv'), index_label='anio')
    M.to_csv(os.path.join(dir_out, 'eeuu_especificaciones.csv'))
    for k, v in masa.items(): v.to_csv(os.path.join(dir_out, f'eeuu_masa_plusvalor_{k}.csv'), index_label='anio')
    pd.DataFrame({'COMP_U': COMP_U, 'V_ramas': V['b'], 'V_intra_rama': V['c'], 'COMP_empresarial': COMP_BUS}).to_csv(os.path.join(dir_out, 'eeuu_salarios.csv'), index_label='anio')
    return dict(FH=D.FH, FH_TOTAL=D.FH_TOTAL, F=D.F, N=D.N, sens=sens, R=R, M=M, principal=principal, Rc=Rc, trans=trans, masa=masa, empalmes=empalmes, fin=D.FIN, SK=SK)
