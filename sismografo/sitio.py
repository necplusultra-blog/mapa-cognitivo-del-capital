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
        'emp_intra_cc': R['B|c|cc|neta|ppi-incl|K-todo|noutil'],
        'emp_ramas_cv': R['B|b|cc|neta|ppi-incl|K-todo|noutil|den-KV']}) * 100
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
    tiempo = mc[['obreros_productivos_mill', 'horas_plustrabajo_mill', 'semana_horas', 'semana_necesario', 'semana_plustrabajo', 'semana_tc_necesario', 'semana_tc_plustrabajo',
                 'e', 'plusvalor_por_obrero_real', 'expresion_monetaria_hora', 'expresion_monetaria_hora_real']].copy()
    tiempo['horas_plustrabajo_mmh'] = tiempo.pop('horas_plustrabajo_mill') / 1000   # miles de millones de horas
    tiempo = tiempo.astype(float).round(3); tiempo.index.name = 'anio'
    _w(f'{d}/eeuu_tiempo.json', _rows(tiempo))
    # descomposición de la masa de plustrabajo: horas = obreros × horas por obrero × e/(1+e)
    a0, a1 = int(tiempo.index[0]), int(tiempo.index[-1]); t0, t1 = tiempo.loc[a0], tiempo.loc[a1]
    f = {'Número de obreros productivos': t1.obreros_productivos_mill / t0.obreros_productivos_mill,
         'Horas por obrero (extensión de la jornada)': t1.semana_horas / t0.semana_horas,
         'Proporción de plustrabajo e/(1+e)': (t1.e / (1 + t1.e)) / (t0.e / (1 + t0.e))}
    tot = float(np.log(t1.horas_plustrabajo_mmh / t0.horas_plustrabajo_mmh))
    _w(f'{d}/eeuu_descomposicion.json', dict(desde=a0, hasta=a1, factor_total=round(float(np.exp(tot)), 3),
        factores=[dict(factor=k, multiplica=round(float(v), 3), aporte_pct=round(100 * float(np.log(v)) / tot, 1)) for k, v in f.items()]))
    _w(f'{d}/eeuu_trimestral.json', json.loads(ee['trim'].reset_index().to_json(orient='records')))
    _w(f'{d}/eeuu_sensibilidad.json', ee['sens'])
    if ee.get('ia') is not None:
        _w(f'{d}/ia_agregado.json', json.loads(ee['ia']['A'].reset_index().to_json(orient='records')))
        E = ee['ia']['E']
        t = (E.dropna(subset=['ganancia_operativa', 'capital_fijo']).assign(tasa=lambda x: x.ganancia_operativa / x.capital_fijo * 100)
             .pivot_table(index='anio', columns='empresa', values='tasa').round(1))
        _w(f'{d}/ia_empresas.json', json.loads(t.reset_index().to_json(orient='records')))
    RW = mu['RW']
    cols = {f'{m}_{w}_{c}': f'W|{m}|{w}|china-{c}|balanceado-1960' for m in mu['medidas'] for w in ('K',) for c in ('con', 'sin')}
    mt = (RW[list(cols.values())].astype(float).rename(columns={v: k for k, v in cols.items()}) * 100).loc[1960:].round(2)
    mt.index.name = 'anio'; _w(f'{d}/mundo_tasas.json', _rows(mt))
    mm = pd.DataFrame({'masa_mundial': mu['masa']['masa_mundial'] / 1e6, 'masa_sin_china': mu['masa']['masa_sin_china'] / 1e6,
                       'china_pct_K': mu['peso'].get('CN') * 100, 'eeuu_pct_K': mu['peso'].get('US') * 100}).round(2)
    mm.index.name = 'anio'; _w(f'{d}/mundo_masa.json', _rows(mm))
    if mu.get('horas') is not None:
        A = mu['horas']['A']; P = mu['horas']['P']
        piv = A.pivot_table(index='anio', columns=['variante', 'china'], values=['plustrabajo_mmh', 'plustrabajo_neto_mmh', 'e_horas', 'e_horas_neta',
                                                                                 'obreros_mill', 'pct_china', 'pct_india', 'pct_ocde_rama'])
        piv.columns = ['__'.join(c) for c in piv.columns]; piv.index.name = 'anio'
        _w(f'{d}/mundo_horas.json', _rows(piv.astype(float).round(3)))
        ult = int(P.anio.max())
        top = (P[(P.anio == ult) & (P.variante == 'educación y salud públicas fuera')].sort_values('plustrabajo_mill_h', ascending=False)
               [['pais', 'obreros_mill', 'e', 'e_neta', 'plustrabajo_mill_h', 'china_estimada', 'fuente_e', 'fuente_obreros']].head(15))
        top['pct'] = top.plustrabajo_mill_h / P[(P.anio == ult) & (P.variante == 'educación y salud públicas fuera')].plustrabajo_mill_h.sum() * 100
        _w(f'{d}/mundo_horas_paises.json', dict(anio=ult, n_paises=int(P[P.anio == ult].pais.nunique()), base_wiod=int(P[~P.extension].anio.max()), paises=json.loads(top.round(3).to_json(orient='records')),
                                                 excluidos=sorted({x['pais'] for x in mu['horas']['excluidos']}),
                                                 fuentes_e=P[(P.anio == ult) & (P.variante == 'educación y salud públicas fuera')].fuente_e.value_counts().to_dict(),
                                                 sensibilidad=json.loads(mu['horas']['S'].round(3).to_json(orient='records')),
                                                 k_mediana=mu['horas'].get('k_mediana'),
                                                 diagnostico_ocde=json.loads(mu['horas']['diag'].round(3).to_json(orient='records'))))
    tf = ee.get('transformacion')
    if tf and not tf.get('D', pd.DataFrame()).empty:
        D, R, C, W = tf['D'], tf['R'], tf['C'], tf['W']
        ser = D.groupby('anio').agg(desv_mediana=('desviacion_media', 'median'), spearman_mediana=('spearman_precio_valor_composicion', 'median'))
        for c in ('USA', 'DEU', 'CHN', 'IND'):
            ser['desv_' + c] = D[D.pais == c].set_index('anio').desviacion_media
        ser = (ser * 100).round(2); ser['spearman_mediana'] = ser['spearman_mediana'] / 100; ser.index.name = 'anio'
        u = int(R.anio.max()); r = R[R.anio == u]
        ramas = (r.groupby('nombre').apply(lambda t: pd.Series({'precio_valor': (t.precio_valor * t.produccion_musd).sum() / t.produccion_musd.sum(),
                                                               'composicion': t.composicion_K_v.replace([np.inf, -np.inf], np.nan).median()}))
                 .sort_values('precio_valor').reset_index())
        com = C.pivot_table(index='anio', columns='pais', values='transferencia_mill_h') / 1000
        grupos = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datos_cache', 'banco_mundial_grupos.csv')).set_index('iso3').ingreso
        alto = [c for c in com.columns if grupos.get(c) == 'High income']
        comj = pd.DataFrame({'altos_ingresos': com[alto].sum(axis=1), **{c: com.get(c) for c in ('USA', 'DEU', 'JPN', 'CHN', 'IND')}}).round(2)
        comj.index.name = 'anio'
        dd = D[D.anio == u]
        mos = {}
        MT, MR = tf.get('MT', pd.DataFrame()), tf.get('MR', pd.DataFrame())
        if not MT.empty:
            g = MT.groupby(['interpretacion', 'anio'])[['plusvalor_usd_mill', 'capital_usd_mill']].sum()
            agr = (g.plusvalor_usd_mill / g.capital_usd_mill * 100).unstack(0)
            ser2 = pd.DataFrame({'mundo_moseley': agr.get('Moseley'), 'mundo_tssi': agr.get('TSSI')})
            for c in ('USA', 'CHN'):
                for i, k in (('Moseley', 'moseley'), ('TSSI', 'tssi')):
                    ser2[f'{c}_{k}'] = MT[(MT.pais == c) & (MT.interpretacion == i)].set_index('anio').r * 100
            ser2.index.name = 'anio'
            M = MT[MT.interpretacion == 'Moseley']; mu_ = M[M.anio == u]
            rr = MR[MR.anio == u].groupby('nombre').apply(lambda t: pd.Series({
                'transferencia_pct': np.average(t.transferencia_pct_valor, weights=t.produccion_usd_mill),
                'tasa_efectiva': np.average(t.tasa_efectiva.clip(-1, 5), weights=t.produccion_usd_mill) * 100,
                'tasa_en_valores': np.average(t.tasa_en_valores, weights=t.produccion_usd_mill) * 100})).sort_values('transferencia_pct').reset_index()
            mos = dict(serie=_rows(ser2.round(2)), redistribuido_pct=float(mu_.plusvalor_redistribuido_pct.median()),
                       cv_efectivas=float(mu_.cv_tasas_efectivas.median()), cv_valores=float(mu_.cv_tasas_en_valores.median()),
                       pct_igualacion=float((M.cv_tasas_efectivas < M.cv_tasas_en_valores).mean() * 100),
                       pct_pp_mejor=float((M.desv_mercado_pp < M.desv_mercado_valor).mean() * 100),
                       desv_valor=float(mu_.desv_mercado_valor.median() * 100), desv_pp=float(mu_.desv_mercado_pp.median() * 100),
                       ramas=json.loads(rr.round(2).to_json(orient='records')))
        _w(f'{d}/transformacion.json', dict(serie=_rows(ser), anio_ramas=u, ramas=json.loads(ramas.round(3).to_json(orient='records')), moseley=mos,
                                             comercio=_rows(comj), ponderada=json.loads(W.round(3).to_json(orient='records')) if not W.empty else [],
                                             n_paises=int(dd.pais.nunique()), pct_spearman_pos=float((dd.spearman_precio_valor_composicion > 0).mean() * 100)))
    fz = ee.get('fuerzas')
    if fz:
        _w(f'{d}/fuerzas.json', dict(eeuu=_rows(fz['eeuu'].astype(float).round(3)), desc={k: (round(v, 3) if isinstance(v, float) else v) for k, v in fz['desc'].items()},
                                      mundo=json.loads(fz['mundo'].round(3).to_json(orient='records')) if fz.get('mundo') is not None else []))
    rn = ee.get('robustez_neta')
    if rn:
        _w(f'{d}/robustez_neta.json', dict(serie=json.loads(rn['R'].round(2).to_json(orient='records')),
                                            resumen=json.loads(rn['T'].round(2).to_json(orient='records'))))
    bb = ee.get('bloque_b')
    if bb:
        M = bb['M']
        _w(f'{d}/bloque_b.json', dict(eeuu=_rows(bb['E'].astype(float).round(3)),
                                       mundo=json.loads(M.round(3).to_json(orient='records')) if not M.empty else []))
    if ee.get('ct') is not None:
        I = ee['ct']['I'].copy(); I.index.name = 'anio'
        _w(f'{d}/contratendencias.json', dict(indicadores=_rows(I.astype(float).round(3)), fases=json.loads(ee['ct']['F'].round(4).to_json(orient='records')),
                                              fases_multiverso=json.loads(ee['ct']['FM'].round(4).to_json(orient='records')),
                                              cortes=ee['ct']['cortes']))
    me = mu['MW'].reset_index(); me['quiebres'] = me['quiebres'].astype(str)
    _w(f'{d}/mundo_especificaciones.json', json.loads(me.to_json(orient='records')))
    try: sha = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], text=True).strip()
    except Exception: sha = None  # noqa: BLE001
    meta = dict(actualizado=dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC'), commit=sha,
                eeuu_fin=int(ee['fin']), ia=ee.get('ia') is not None, contratendencias=ee.get('ct') is not None, transformacion=bool(ee.get('transformacion')), fuerzas=bool(ee.get('fuerzas')), bloque_b=bool(ee.get('bloque_b')), robustez_neta=bool(ee.get('robustez_neta')), eeuu_trim_fin=str(ee['trim'].index[-1]), eeuu_n=len(ee['principal']), eeuu_n_intra=int(ee['Rc'].shape[1]), empalmes=ee['empalmes'],
                mundo_fin=int(mu['fin']), mundo_horas=mu.get('horas') is not None, mundo_fuente=mu['fuente'], mundo_n=mu['n'], mundo_nbal=mu['nbal'], mundo_medidas=mu['medidas'])
    _w(f'{d}/meta.json', meta)
    return meta
