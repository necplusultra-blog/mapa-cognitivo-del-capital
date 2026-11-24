"""Fuerzas productivas y tiempo disponible.

La reducción relativa del tiempo de trabajo necesario es la forma en que el capital desarrolla la fuerza productiva
social; el capital convierte en plustrabajo el tiempo que esa reducción libera. Este módulo no calcula la jornada de una
sociedad futura: muestra, con las mismas series del sismógrafo, cuánto tiempo libera el desarrollo de la fuerza
productiva y en qué se convierte bajo la relación de capital.

EE.UU. (obreros productivos, variante intra-rama, desde 1972), para una jornada de tiempo completo de 40 horas:
  - necesario efectivo      = 40 / (1 + e)                          (horas en que el obrero reproduce su salario)
  - necesario a nivel 1972  = 40 · w̃₁₉₇₂ / μ̃_t                      (horas que bastarían, con la productividad de cada
                                                                     año, para reproducir el salario real de 1972)
    w̃ = remuneración real por hora de los obreros productivos (V / H, deflactor del PIB);
    μ̃ = valor nuevo real por hora productiva ((V + S) / H, deflactor del PIB), la expresión monetaria real del tiempo.
  - el tiempo liberado respecto de 1972 (necesario₁₉₇₂ − necesario a nivel 1972) se reparte exactamente en:
      más consumo obrero      = necesario efectivo − necesario a nivel 1972
      más plustrabajo         = plustrabajo_t − plustrabajo₁₉₇₂
      jornada normal más corta = 0 (la jornada de referencia es la misma; la jornada legal de 40 h rige desde 1940)

Mundo (países medidos rama por rama, variante central): horas anuales de trabajo productivo, necesario y plustrabajo
por habitante de esos mismos países (población de la Penn World Table; después de su último año, crecimiento medio de
los tres años anteriores), en minutos por día.
"""
import json, os

import numpy as np, pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _poblacion(dir_datos, paises, anios):
    fn = os.path.join(dir_datos, 'pwt', 'pwt110.dta')
    if not os.path.exists(fn): fn = os.path.join(RAIZ, 'datos_cache', 'pwt110.dta')
    pw = pd.read_stata(fn, columns=['countrycode', 'year', 'pop'])
    pw = pw.pivot_table(index='year', columns='countrycode', values='pop').astype(float)   # todos los países (para la parte mundial)
    ult = int(pw.index.max())
    for y in [a for a in anios if a > ult]:                                     # extrapolación geométrica
        g = (pw.loc[ult] / pw.loc[ult - 3]) ** (1 / 3)
        pw.loc[y] = pw.loc[y - 1] * g
    return pw.sort_index(), ult


def calcular(dir_datos, dir_out, ee, hm=None):
    c = ee['masa']['c'].copy()
    defl = c['expresion_monetaria_hora'] / c['expresion_monetaria_hora_real']   # deflactor del PIB / 100
    H = c['horas_productivas_mill']
    w_real = c['V'] / H / defl
    mu_real = c['expresion_monetaria_hora_real']
    a0 = int(c.index.min())
    U = pd.DataFrame({
        'necesario_efectivo_h': c['semana_tc_necesario'],
        'plustrabajo_h': c['semana_tc_plustrabajo'],
        'necesario_nivel_inicial_h': 40 * w_real.loc[a0] / mu_real,
        'parte_necesaria_pct': 100 / (1 + c['e']),
        'valor_nuevo_real_hora_idx': mu_real / mu_real.loc[a0] * 100,
        'salario_real_hora_idx': w_real / w_real.loc[a0] * 100,
    })
    U.index.name = 'anio'
    z = U.iloc[-1]; i0 = U.iloc[0]
    liberado = float(i0.necesario_efectivo_h - z.necesario_nivel_inicial_h)
    consumo = float(z.necesario_efectivo_h - z.necesario_nivel_inicial_h)
    plus = float(z.plustrabajo_h - i0.plustrabajo_h)
    desc = dict(desde=a0, hasta=int(U.index[-1]), liberado_h=liberado, consumo_h=consumo, plustrabajo_h=plus, jornada_h=0.0,
                consumo_pct=100 * consumo / liberado, plustrabajo_pct=100 * plus / liberado)
    U.to_csv(os.path.join(dir_out, 'fuerzas_eeuu.csv'))
    out = dict(eeuu=U, desc=desc, mundo=None)
    if hm is not None:
        from sismografo.horas_mundo import CENTRAL
        P = hm['P']; Q = P[P.variante == CENTRAL]
        anios = sorted(int(a) for a in Q.anio.unique())
        pop, ult_pwt = _poblacion(dir_datos, Q.pais.unique(), anios)
        filas = []
        for y in anios:
            g = Q[Q.anio == y].set_index('pais')
            p = pop.loc[y].reindex(g.index)
            ok = p.notna() & g.horas_mill.notna()
            hab = float(p[ok].sum()) * 1e6
            mundo_hab = float(pop.loc[y].sum()) * 1e6
            hp = float(g.horas_mill[ok].sum()) * 1e6; hs = float(g.plustrabajo_mill_h[ok].sum()) * 1e6
            hsn = float(g.plustrabajo_neto_mill_h[ok].sum()) * 1e6
            m = lambda h: h / hab / 365 * 60
            filas.append(dict(anio=y, paises=int(ok.sum()), poblacion_mill=hab / 1e6, poblacion_pct_mundo=hab / mundo_hab * 100, obreros_mill=float(g.obreros_mill[ok].sum()),
                              obreros_pct_poblacion=float(g.obreros_mill[ok].sum()) * 1e6 / hab * 100,
                              min_productivo_dia=m(hp), min_necesario_dia=m(hp - hs), min_plustrabajo_dia=m(hs),
                              min_plustrabajo_neto_dia=m(hsn), parte_necesaria_pct=(hp - hs) / hp * 100,
                              poblacion_extrapolada=bool(y > ult_pwt)))
        Wd = pd.DataFrame(filas)
        Wd.to_csv(os.path.join(dir_out, 'fuerzas_mundo.csv'), index=False)
        out['mundo'] = Wd
    return out
