"""Comercio exterior como transferencia de tiempo de trabajo (aproximación de intercambio desigual).

Para cada país i y año t:
  h_i   = H_i / PIB_i                  horas trabajadas por dólar de PIB (H = ocupados × horas anuales, PWT 11.0;
                                       PIB en dólares corrientes a tipo de cambio de mercado, Banco Mundial)
  h_X   = Σ_j X_j h_j / Σ_j X_j        contenido medio en horas de un dólar de exportaciones mundiales
  T_i   = M_i · h_X − X_i · h_i        transferencia neta: horas incorporadas en lo que el país importa menos horas
                                       incorporadas en lo que exporta (positiva = el país se apropia de tiempo ajeno)

Supuestos explícitos: las exportaciones de un país incorporan las horas por dólar promedio de su economía; las
importaciones incorporan el contenido medio de las exportaciones mundiales; no se rastrean los insumos intermedios
(para eso hace falta una matriz insumo-producto mundial); se usan todas las horas trabajadas, no sólo las
productivas. Es una aproximación de la transferencia de valor por comercio exterior que Marx describe: los países
de productividad más alta reciben más trabajo a cambio de menos (El Capital, Libro III, cap. XIV, §V).
"""
import json, os, urllib.request

import numpy as np, pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(RAIZ, 'datos_cache', 'banco_mundial_comercio.csv')
CACHE_GRUPOS = os.path.join(RAIZ, 'datos_cache', 'banco_mundial_grupos.csv')
IND = {'NY.GDP.MKTP.CD': 'pib', 'NE.EXP.GNFS.CD': 'x', 'NE.IMP.GNFS.CD': 'm'}
UA = {'User-Agent': 'Mozilla/5.0 mapa-cognitivo-del-capital'}


def _json(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
        return json.loads(r.read())


def _descargar():
    try:
        filas = []
        for ind, nom in IND.items():
            for pag in range(1, 20):
                d = _json(f'https://api.worldbank.org/v2/country/all/indicator/{ind}?format=json&per_page=20000&date=1990:2025&page={pag}')
                filas += [(x['countryiso3code'], int(x['date']), nom, x['value']) for x in d[1] if x['value'] is not None and x['countryiso3code']]
                if pag >= d[0]['pages']: break
        pd.DataFrame(filas, columns=['iso3', 'anio', 'serie', 'valor']).to_csv(CACHE, index=False)
        g = _json('https://api.worldbank.org/v2/country?format=json&per_page=400')[1]
        pd.DataFrame([(x['id'], x['incomeLevel']['value'], x['region']['value']) for x in g],
                     columns=['iso3', 'ingreso', 'region']).to_csv(CACHE_GRUPOS, index=False)
    except Exception as e:  # noqa: BLE001
        print('Banco Mundial (comercio): se usa la copia guardada', repr(e))


def calcular(dir_datos, dir_out):
    _descargar()
    wb = pd.read_csv(CACHE).pivot_table(index=['iso3', 'anio'], columns='serie', values='valor')
    grupos = pd.read_csv(CACHE_GRUPOS).set_index('iso3')
    fn = os.path.join(dir_datos, 'pwt', 'pwt110.dta')
    if not os.path.exists(fn): fn = os.path.join(RAIZ, 'datos_cache', 'pwt110.dta')
    pwt = pd.read_stata(fn, columns=['countrycode', 'year', 'emp', 'avh'])
    pwt['H'] = pwt.emp.astype(float) * pwt.avh.astype(float) * 1e6        # horas al año
    pwt = pwt.rename(columns={'countrycode': 'iso3', 'year': 'anio'}).set_index(['iso3', 'anio'])[['H']]
    d = wb.join(pwt, how='inner').dropna(subset=['pib', 'x', 'm', 'H'])
    d = d[(d.pib > 0) & (d.H > 0)].reset_index()
    d['h'] = d.H / d.pib
    filas, agregados = [], []
    for y, g in d.groupby('anio'):
        if len(g) < 100: continue   # años con cobertura suficiente de horas trabajadas (PWT)
        hX = (g.x * g.h).sum() / g.x.sum()
        g = g.assign(hX=hX, recibidas=g.m * hX, entregadas=g.x * g.h)
        g['transferencia_horas'] = g.recibidas - g.entregadas
        g['transferencia_pct_horas'] = g.transferencia_horas / g.H * 100
        g['razon_intercambio_horas'] = (g.recibidas / g.m) / (g.entregadas / g.x)   # horas recibidas por hora entregada, por dólar
        g['ingreso'] = g.iso3.map(grupos.ingreso)
        filas.append(g)
        alto = g.ingreso == 'High income'
        fila = dict(anio=int(y), paises=len(g), horas_por_dolar_exportado_mundo=hX,
                    altos_ingresos_mmh=g.loc[alto, 'transferencia_horas'].sum() / 1e9,
                    altos_ingresos_pct_horas=g.loc[alto, 'transferencia_horas'].sum() / g.loc[alto, 'H'].sum() * 100,
                    resto_mmh=g.loc[~alto, 'transferencia_horas'].sum() / 1e9,
                    razon_altos_ingresos=(g.loc[alto, 'recibidas'].sum() / g.loc[alto, 'm'].sum()) / (g.loc[alto, 'entregadas'].sum() / g.loc[alto, 'x'].sum()))
        for c in ('USA', 'CHN', 'IND', 'DEU', 'JPN', 'MEX', 'BRA'):
            r = g[g.iso3 == c]
            fila[f'{c}_mmh'] = float(r.transferencia_horas.iloc[0] / 1e9) if len(r) else np.nan
        agregados.append(fila)
    P = pd.concat(filas, ignore_index=True)
    A = pd.DataFrame(agregados)
    P[['iso3', 'anio', 'ingreso', 'pib', 'x', 'm', 'H', 'h', 'hX', 'transferencia_horas', 'transferencia_pct_horas', 'razon_intercambio_horas']] \
        .to_csv(os.path.join(dir_out, 'intercambio_horas_paises.csv'), index=False)
    A.to_csv(os.path.join(dir_out, 'intercambio_horas.csv'), index=False)
    return dict(A=A, P=P)
