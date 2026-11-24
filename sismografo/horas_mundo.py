"""Masa mundial de plusvalor en horas de trabajo (WIOD, Cuentas Socioeconómicas 2016; 43 países, 2000–2014).

Mismo criterio por ramas que en EE.UU. (Capítulo Primero, §1.3):
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
    return d['STE_AGGREGATE_EES'] / d['STE_AGGREGATE_TOTAL']


def calcular(dir_datos, dir_out):
    fn = os.path.join(dir_datos, 'wiod', 'Socio_Economic_Accounts.xlsx')
    if not os.path.exists(fn):
        fn = os.path.join(os.path.dirname(CACHE_ILO), 'wiod_sea.xlsx')
    d = pd.read_excel(fn, sheet_name='DATA', engine='calamine')
    yc = [c for c in d.columns if str(c).isdigit()]
    d = d.rename(columns={c: int(c) for c in yc}); Y = [int(c) for c in yc]
    piv = {v: d[d.variable == v].set_index(['country', 'code'])[Y] for v in ('VA', 'COMP', 'LAB', 'EMPE', 'H_EMPE', 'EMP')}
    paises = sorted(d.country.unique())
    share_chn = _ilo_china()
    filas, excluidos = [], []
    for variante, publicas_prod in (('educación y salud productivas', True), ('educación y salud fuera', False)):
        improd = CIRCULACION + FUERA + ([] if publicas_prod else PUBLICAS)
        fuera = FUERA + ([] if publicas_prod else PUBLICAS)
        for c in paises:
            codes = piv['VA'].loc[c].index
            prod = [k for k in codes if k not in improd]
            mercado = [k for k in codes if k not in fuera]
            for y in Y:
                s = float(share_chn.get(y, np.nan)) if c == 'CHN' else 1.0   # China: COMP incluye a los no asalariados
                comp = lambda ks: piv['COMP'].loc[c].loc[ks, y].sum() * s
                v = comp(prod)
                cuenta_propia = piv['LAB'].loc[c].loc[mercado, y].sum() - comp(mercado)
                pv = piv['VA'].loc[c].loc[mercado, y].sum() - cuenta_propia - v
                if c == 'CHN':
                    N = piv['EMP'].loc[c].loc[prod, y].sum() * s
                    H = N * HORAS_CHINA / 1000   # N en miles → millones de horas
                    estimado = True
                else:
                    N = piv['EMPE'].loc[c].loc[prod, y].sum(); H = piv['H_EMPE'].loc[c].loc[prod, y].sum(); estimado = False
                if not (v > 0 and N > 0 and H > 0): continue
                e = pv / v
                if not 0 < e < 8:   # datos anómalos (p. ej. Taiwán en algunos años): se excluyen y se registran
                    excluidos.append(dict(variante=variante, pais=c, anio=y, e=round(float(e), 3))); continue
                filas.append(dict(variante=variante, pais=c, anio=y, obreros_mill=N / 1000, horas_mill=H, e=e,
                                  plustrabajo_mill_h=H * e / (1 + e), necesario_mill_h=H / (1 + e), china_estimada=estimado))
    P = pd.DataFrame(filas)
    P.to_csv(os.path.join(dir_out, 'mundo_horas_paises.csv'), index=False)
    pd.DataFrame(excluidos).to_csv(os.path.join(dir_out, 'mundo_horas_excluidos.csv'), index=False)
    agg = []
    for (var, y), g in P.groupby(['variante', 'anio']):
        for etiqueta, gg in (('con China', g), ('sin China', g[g.pais != 'CHN'])):
            H, Sp = gg.horas_mill.sum(), gg.plustrabajo_mill_h.sum()
            agg.append(dict(variante=var, china=etiqueta, anio=int(y), paises=len(gg), obreros_mill=gg.obreros_mill.sum(),
                            plustrabajo_mmh=Sp / 1000, e_horas=Sp / (H - Sp), semana_horas=H / gg.obreros_mill.sum() / 52,
                            pct_china=float(g.loc[g.pais == 'CHN', 'plustrabajo_mill_h'].sum() / g.plustrabajo_mill_h.sum() * 100)))
    A = pd.DataFrame(agg)
    A.to_csv(os.path.join(dir_out, 'mundo_horas.csv'), index=False)
    return dict(A=A, P=P, excluidos=excluidos)
