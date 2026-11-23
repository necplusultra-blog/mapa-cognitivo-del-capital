"""Mundo: núcleo reducido con la Penn World Table 11.0 (economía total, sin división productivo/improductivo).

Con la PWT completa: tasa bruta (1−labsh)·cgdpo/cn, neta ((1−labsh)·cgdpo − δ·cn)/cn y la tasa interna de
retorno real (irr) de la propia PWT. Sin ella (réplica parcial en FRED): sólo la bruta con Y/K a precios constantes.
"""
import glob, itertools, os
import numpy as np, pandas as pd
from .quiebres import breaks

G7 = ['US', 'JP', 'DE', 'GB', 'FR', 'IT', 'CA']


def _panel_completo(path):
    import pycountry
    d = pd.read_stata(path)
    iso2 = {c.alpha_3: c.alpha_2 for c in pycountry.countries}
    d['cc'] = d['countrycode'].map(iso2)
    d = d.dropna(subset=['cc'])
    piv = lambda v: d.pivot_table(index='year', columns='cc', values=v)
    lab, cg, cn, de, irr, rg, rn = (piv(v) for v in ('labsh', 'cgdpo', 'cn', 'delta', 'irr', 'rgdpna', 'rnna'))
    return dict(bruta=(1 - lab) * cg / cn, neta=((1 - lab) * cg - de * cn) / cn, irr=irr,
                peso_K=cn, peso_PIB=cg, masa=(1 - lab) * rg, fuente='PWT 11.0 completa (dataverse.nl)')


def _panel_fred(dirp):
    def load(v, unit):
        out = {}
        for f in glob.glob(os.path.join(dirp, f'{v}??{unit}.csv')):
            cc = os.path.basename(f)[len(v):len(v) + 2]
            x = pd.read_csv(f, parse_dates=[0])
            out[cc] = pd.Series(pd.to_numeric(x.iloc[:, 1], errors='coerce').values, index=x.iloc[:, 0].dt.year)
        return pd.DataFrame(out)
    lab, kn, yn, cn, ye = (load(v, u) for v, u in (('LABSHP', 'A156NRUG'), ('RKNANP', 'A666NRUG'), ('RGDPNA', 'A666NRUG'), ('CKSPPP', 'A666NRUG'), ('RGDPES', 'A666NRUG')))
    return dict(bruta=(1 - lab) * yn / kn, peso_K=cn, peso_PIB=ye, masa=(1 - lab) * yn, fuente='PWT 11.0 parcial (réplica en FRED)')


def calcular(dir_datos, dir_out):
    dirp = os.path.join(dir_datos, 'pwt'); dta = os.path.join(dirp, 'pwt110.dta')
    P = _panel_completo(dta) if os.path.exists(dta) else _panel_fred(dirp)
    medidas = [m for m in ('bruta', 'neta', 'irr') if m in P]
    fin = int(P['bruta'].dropna(how='all').index.max())
    Y = list(range(1950, fin + 1))
    for k in medidas + ['peso_K', 'peso_PIB', 'masa']: P[k] = P[k].reindex(Y)
    cols = sorted(c for c in set.intersection(*(set(P[k].columns) for k in medidas + ['peso_K', 'peso_PIB'])) if P['bruta'][c].notna().any())
    ok = P['bruta'][cols].notna() & P['peso_K'][cols].notna() & P['peso_PIB'][cols].notna()
    balanced = [c for c in cols if ok.loc[1960:, c].all()]
    rows, meta = [], []
    for med, w, china, panel in itertools.product(medidas, ['K', 'PIB'], ['con', 'sin'], ['balanceado-1960', 'no balanceado']):
        use = balanced if panel.startswith('bal') else cols
        if china == 'sin': use = [c for c in use if c != 'CN']
        valid = ok[use] & P[med][use].notna()
        W = P['peso_' + w][use].where(valid)
        r = (P[med][use] * W).sum(axis=1) / W.sum(axis=1)
        yrs = list(range(1960, fin + 1)) if panel.startswith('bal') else Y
        r = r.reindex(yrs)
        sid = f'W|{med}|{w}|china-{china}|{panel}'
        rows.append(r.rename(sid))
        meta.append(dict(id=sid, medida=med, ponderacion=w, china=china, panel=panel, n_paises=len(use),
                         quiebres=breaks(r.values, np.array(yrs))))
    RW = pd.concat(rows, axis=1).sort_index(); MW = pd.DataFrame(meta).set_index('id')
    nb = [c for c in balanced if c != 'CN']
    masa = pd.DataFrame({'masa_mundial': P['masa'][balanced].sum(axis=1), 'masa_sin_china': P['masa'][nb].sum(axis=1)}).loc[1960:]
    peso = pd.DataFrame({k: P['peso_K'][k] / P['peso_K'][balanced].sum(axis=1) for k in ('US', 'CN', 'MX', 'CL') if k in cols}).loc[1960:]
    paises = P['bruta'][[c for c in ['US', 'CN', 'MX', 'CL', 'DE', 'JP', 'KR', 'IN', 'BR'] if c in cols]]
    RW.to_csv(os.path.join(dir_out, 'mundo_tasas.csv'), index_label='anio'); MW.to_csv(os.path.join(dir_out, 'mundo_especificaciones.csv'))
    masa.to_csv(os.path.join(dir_out, 'mundo_masa.csv'), index_label='anio'); peso.to_csv(os.path.join(dir_out, 'mundo_peso_capital.csv'), index_label='anio')
    paises.to_csv(os.path.join(dir_out, 'paises_tasa_bruta.csv'), index_label='anio')
    return dict(RW=RW, MW=MW, masa=masa, peso=peso, paises=paises, fuente=P['fuente'], n=len(cols), nbal=len(balanced), fin=fin, medidas=medidas)
