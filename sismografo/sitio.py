"""Convierte los resultados en los JSON que lee el sitio público (site/data)."""
import datetime as dt, json, os, subprocess
import numpy as np, pandas as pd


def _w(path, obj):
    with open(path, 'w') as f:
        json.dump(obj, f, ensure_ascii=False, allow_nan=False, default=lambda o: None if (isinstance(o, float) and np.isnan(o)) else o)


def _rows(df):
    return json.loads(df.reset_index().to_json(orient='records'))


def escribir(ee, mu, dir_site):
    d = os.path.join(dir_site, 'data'); os.makedirs(d, exist_ok=True)
    R, P = ee['R'], ee['principal']
    N = R[P] / R[P].mean() * 100
    q = lambda p: N.quantile(p, axis=1)
    bandas = pd.DataFrame({'p10': q(.1), 'p25': q(.25), 'p50': q(.5), 'p75': q(.75), 'p90': q(.9)}).round(2)
    bandas.index.name = 'anio'; _w(f'{d}/eeuu_bandas.json', _rows(bandas))
    ref = pd.DataFrame({
        'nfc_ebe_cc': R['C|nfc|nos|cc|neta|ppi-incl|noinv|noutil'], 'corp_ebe_hc': R['C|corp|nos|hc|neta|ppi-incl|noinv|noutil'],
        'emp_todo_cc': R['B|a|cc|neta|ppi-incl|K-todo|noutil'], 'emp_ramas_cc': R['B|b|cc|neta|ppi-incl|K-todo|noutil'],
        'emp_intra_cc': R['B|c|cc|neta|ppi-incl|K-todo|noutil']}) * 100
    ref.index.name = 'anio'; _w(f'{d}/eeuu_referencias.json', _rows(ref.round(2)))
    cnt = {int(y): 0 for y in R.index}
    for c in P:
        for y in ee['M'].loc[c, 'quiebres']: cnt[int(y)] += 1
    _w(f'{d}/eeuu_quiebres.json', [{'anio': y, 'n': n} for y, n in cnt.items()])
    _w(f'{d}/eeuu_decadas.json', ee['trans'])
    mb, mc = ee['masa']['b'], ee['masa']['c']
    masa = pd.DataFrame({'masa_ramas': mb['S_real_2017'] / 1000, 'masa_intra': mc['S_real_2017'] / 1000,
                         'e_ramas': mb['e'], 'e_intra': mc['e'], 'kv_ramas': mb['K_V'], 'kv_intra': mc['K_V']}).round(3)
    masa.index.name = 'anio'; _w(f'{d}/eeuu_masa.json', _rows(masa))
    _w(f'{d}/eeuu_trimestral.json', json.loads(ee['trim'].reset_index().to_json(orient='records')))
    _w(f'{d}/eeuu_sensibilidad.json', ee['sens'])
    RW = mu['RW']
    cols = {f'{m}_{w}_{c}': f'W|{m}|{w}|china-{c}|balanceado-1960' for m in mu['medidas'] for w in ('K',) for c in ('con', 'sin')}
    mt = (RW[list(cols.values())].astype(float).rename(columns={v: k for k, v in cols.items()}) * 100).loc[1960:].round(2)
    mt.index.name = 'anio'; _w(f'{d}/mundo_tasas.json', _rows(mt))
    mm = pd.DataFrame({'masa_mundial': mu['masa']['masa_mundial'] / 1e6, 'masa_sin_china': mu['masa']['masa_sin_china'] / 1e6,
                       'china_pct_K': mu['peso'].get('CN') * 100, 'eeuu_pct_K': mu['peso'].get('US') * 100}).round(2)
    mm.index.name = 'anio'; _w(f'{d}/mundo_masa.json', _rows(mm))
    me = mu['MW'].reset_index(); me['quiebres'] = me['quiebres'].astype(str)
    _w(f'{d}/mundo_especificaciones.json', json.loads(me.to_json(orient='records')))
    try: sha = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], text=True).strip()
    except Exception: sha = None  # noqa: BLE001
    meta = dict(actualizado=dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC'), commit=sha,
                eeuu_fin=int(ee['fin']), eeuu_trim_fin=str(ee['trim'].index[-1]), eeuu_n=len(P), eeuu_n_intra=int(ee['Rc'].shape[1]), empalmes=ee['empalmes'],
                mundo_fin=int(mu['fin']), mundo_fuente=mu['fuente'], mundo_n=mu['n'], mundo_nbal=mu['nbal'], mundo_medidas=mu['medidas'])
    _w(f'{d}/meta.json', meta)
    return meta
