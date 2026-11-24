"""Excedente por rama fuera de la OCDE: cuentas nacionales oficiales por industria de la ONU.

Fuente: UNdata, base «National Accounts Official Country Data», tabla 2.6 «Output, gross value added and fixed
assets by industries at current prices (ISIC Rev. 4)», descargada desde GitHub Actions con el workflow «Fuentes
externas» (datos_cache/externo/un_206_*.zip). Hoy hay datos útiles para India (2011–2024, año fiscal que empieza en
abril) y Brasil (1995–2022). China e Indonesia sólo publican el valor agregado por rama, sin la remuneración; Rusia,
hasta 2013.

Mismo criterio de ramas que con WIOD y la OCDE, por sección CIIU rev. 4:
  v  = Σ_productivas remuneración de los asalariados
  cp = Σ_mercado ingreso mixto bruto (ingreso de los trabajadores por cuenta propia; si no se publica, cero)
  pv = Σ_mercado valor agregado bruto − cp − v        e = pv / v
  r  = Σ_mercado consumo de capital fijo / v          (excedente bruto − excedente neto, si no se publica)
Las divisiones M69–M70 y M73 se separan de la sección M con su peso en WIOD 2014. Si una serie se interrumpe, la
siguiente se empalma por cociente en el año de traslape. Las series se encadenan al nivel WIOD de 2014
(horas_mundo.combinar_un).
"""
import glob, io, os, re, zipfile

import numpy as np, pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAISES = {'ind': 'IND', 'bra': 'BRA', 'rus': 'RUS', 'idn': 'IDN', 'chn': 'CHN'}
SECC = list('ABCDEFGHIJKLMNOPQRSTU')
IMPROD, FUERA, PUB = ['G', 'K'], ['L', 'O', 'T', 'U'], ['P', 'Q']
ITEMS = {'Equals: VALUE ADDED, GROSS, at basic prices': 'va', 'Compensation of employees': 'comp',
         'MIXED INCOME, GROSS': 'mixto', 'Less: Consumption of fixed capital': 'cfc',
         'OPERATING SURPLUS, GROSS': 'eob', 'OPERATING SURPLUS, NET': 'eon'}


def _leer(fn):
    z = zipfile.ZipFile(fn)
    d = pd.read_csv(io.BytesIO(z.read(z.namelist()[0])), low_memory=False)
    d = d[pd.to_numeric(d.Year, errors='coerce').notna()].copy()
    d['anio'] = d.Year.astype(int)
    d['s'] = d['Sub Item'].astype(str).str.extract(r'\(([A-U])\)$')[0]
    d['item'] = d.Item.map(ITEMS)
    d = d[d.s.notna() & d.item.notna()]
    d['valor'] = pd.to_numeric(d.Value, errors='coerce')
    return d


def _segmentos(d):
    """Cada serie estadística es un segmento; los segmentos se encadenan entre sí en horas_mundo.combinar_un."""
    return d.assign(seg=d.Series)


def calcular(wiod):
    filas = []
    for fn in sorted(glob.glob(os.path.join(RAIZ, 'datos_cache', 'externo', 'un_206_*.zip'))):
        c = PAISES.get(os.path.basename(fn)[7:10])
        if not c: continue
        d = _leer(fn)
        if d.empty or not (d.item == 'comp').any(): continue
        d = _segmentos(d)
        try:
            m = wiod['VA'].loc[c].reindex(['M69_M70', 'M71', 'M72', 'M73', 'M74_M75'])[2014]
            fM = float((m['M69_M70'] + m['M73']) / m.sum())
        except Exception:  # noqa: BLE001
            fM = 0.3
        for seg, dseg in d.groupby('seg'):
          P = dseg.pivot_table(index=['anio', 's'], columns='item', values='valor', aggfunc='sum')
          for variante, publicas_prod in (('educación y salud productivas', True), ('educación y salud fuera', False)):
              fuera = FUERA + ([] if publicas_prod else PUB)
              improd = IMPROD + fuera
              for y in sorted(P.index.get_level_values(0).unique()):
                  g = P.loc[y].reindex(SECC)
                  # secciones faltantes (p. ej. E, publicada junto con B–D): se toman como cero si son pocas
                  if g['va'].isna().sum() > 4 or g['comp'].isna().sum() > 4: continue
                  g = g.fillna({'va': 0, 'comp': 0})
                  peso = pd.Series({s: 0.0 if s in improd else 1.0 for s in SECC}); peso['M'] = 1 - fM
                  merc = [s for s in SECC if s not in fuera]
                  v = float((g.comp * peso).sum())
                  cp = float(g.loc[merc, 'mixto'].fillna(0).sum()) if 'mixto' in g else 0.0
                  vam = float(g.loc[merc, 'va'].sum())
                  if 'cfc' in g and g.loc[merc, 'cfc'].notna().sum() > len(merc) / 2:
                      cfc = float(g.loc[merc, 'cfc'].fillna(0).sum())
                  elif {'eob', 'eon'} <= set(g.columns) and g.loc[merc, 'eon'].notna().sum() > len(merc) / 2:
                      cfc = float((g.loc[merc, 'eob'] - g.loc[merc, 'eon']).fillna(0).sum())
                  else:
                      cfc = np.nan
                  pv = vam - cp - v
                  if v <= 0: continue
                  filas.append(dict(pais=c, variante=variante, segmento=str(seg), anio=int(y), v=v, pv=pv, e=pv / v, r=cfc / v if not np.isnan(cfc) else np.nan,
                                    ingreso_mixto=cp > 0))
    return pd.DataFrame(filas)
