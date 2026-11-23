"""EE.UU.: multiverso de la tasa de ganancia, plusvalor ampliado y quiebres endógenos.

Criterio productivo/improductivo: Capítulo Primero de «Los límites inmanentes del capital»
(Jiménez Cea), sección 1.3 y nota 2. Improductivo: comercio, finanzas y seguros, inmobiliario
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


def v_produccion(D):
    """Corrección intra-rama (D2c): salarios de trabajadores de producción y no supervisores en
    supersectores productivos (BLS CES), escalados por la razón remuneración/salarios del sector empresarial."""
    tot = None
    for code, (nm, prod) in CES_SUPERSECTORES.items():
        if not prod: continue
        emp = _fred_anual(os.path.join(D.dir_fred, f'CES{code}06.csv'))
        ahe = _fred_anual(os.path.join(D.dir_fred, f'CES{code}08.csv'))
        hrs_path = os.path.join(D.dir_fred, f'CES{code}07.csv')
        hrs = _fred_anual(hrs_path if os.path.exists(hrs_path) and code != '30000000' else os.path.join(D.dir_fred, 'AWHMAN.csv'))
        pay = emp * 1000 * ahe * hrs * 52 / 1e6   # millones de USD
        tot = pay if tot is None else tot + pay
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

    def bus(prod, val, gross, ipp, kscope, util):
        kc, dc = ('k1', 'm1') if val == 'cc' else ('k3', 'm3')
        sub = lambda pre, t: D.fa(pre, f'ntotl1{t}') - D.fa(pre, f'ntotl8{t}') - D.fa(pre, f'ntotl5{t}')
        K = sub(kc, 'es00'); Dv = sub(dc, 'es00')
        S_ = GVA - V[prod]
        if not gross: S_ = S_ - Dv
        if ipp == 'excl':
            S_ = S_ - sub('i3', 'ip00') + (0 if gross else sub(dc, 'ip00')); K = K - sub(kc, 'ip00')
        if kscope == 'prod':
            for t in ('n42001es00', 'n44RT1es00', 'n52001es00', 'n54111es00'): K = K - D.fa(kc, t)
        r = S_ / K
        return (r * (D.CU.mean() / D.CU) if util else r), S_, K

    rows, meta = [], []
    for sector, profit, val, gross, ipp, inv, util in itertools.product(['corp', 'nfc'], ['nos', 'pbt', 'pat'], ['cc', 'hc'], [False, True], ['incl', 'excl'], [False, True], [False, True]):
        sid = f'C|{sector}|{profit}|{val}|{"bruta" if gross else "neta"}|ppi-{ipp}|{"inv" if inv else "noinv"}|{"util" if util else "noutil"}'
        rows.append(corp(sector, profit, val, gross, ipp, inv, util).rename(sid))
        meta.append(dict(id=sid, familia='corporativa', D6=sector, D1=profit, D2='a', D3=val, D4='bruta' if gross else 'neta', D5=ipp, inventarios=inv, D8=util, K='todo'))
    for prod, val, gross, ipp, kscope, util in itertools.product(['a', 'b', 'c'], ['cc', 'hc'], [False, True], ['incl', 'excl'], ['todo', 'prod'], [False, True]):
        if prod == 'a' and kscope == 'prod': continue
        sid = f'B|{prod}|{val}|{"bruta" if gross else "neta"}|ppi-{ipp}|K-{kscope}|{"util" if util else "noutil"}'
        rows.append(bus(prod, val, gross, ipp, kscope, util)[0].rename(sid))
        meta.append(dict(id=sid, familia={'a': 'empresarial: todo productivo', 'b': 'empresarial: plusvalor ampliado (por ramas)', 'c': 'empresarial: plusvalor ampliado (corrección intra-rama)'}[prod],
                         D6='empresarial', D1='excedente amplio' if prod == 'a' else 'plusvalor ampliado', D2=prod, D3=val, D4='bruta' if gross else 'neta', D5=ipp, inventarios=False, D8=util, K=kscope))
    R = pd.concat(rows, axis=1); M = pd.DataFrame(meta).set_index('id')
    principal = [c for c in R.columns if not c.startswith('B|c|')]
    Rc = R[[c for c in R.columns if c.startswith('B|c|')]].loc[INICIO_C:]
    assert R[principal].notna().all().all(), R[principal].columns[R[principal].isna().any()].tolist()

    yrs = np.array(Y)
    M['quiebres'] = [breaks(R[c].values, yrs) if c in principal else breaks(Rc[c].values, np.array(Rc.index)) for c in M.index]

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

    R.to_csv(os.path.join(dir_out, 'eeuu_multiverso_tasas.csv'), index_label='anio')
    M.to_csv(os.path.join(dir_out, 'eeuu_especificaciones.csv'))
    for k, v in masa.items(): v.to_csv(os.path.join(dir_out, f'eeuu_masa_plusvalor_{k}.csv'), index_label='anio')
    pd.DataFrame({'COMP_U': COMP_U, 'V_ramas': V['b'], 'V_intra_rama': V['c'], 'COMP_empresarial': COMP_BUS}).to_csv(os.path.join(dir_out, 'eeuu_salarios.csv'), index_label='anio')
    return dict(R=R, M=M, principal=principal, Rc=Rc, trans=trans, masa=masa, empalmes=empalmes, fin=D.FIN)
