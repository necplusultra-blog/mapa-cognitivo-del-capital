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
los tres años anteriores), en minutos por día. Variante: más las horas de los asalariados de la educación y la salud
públicas y sin fines de lucro (improductivo para el capital, socialmente necesario).

v2 (EE.UU.): el tiempo al nivel de vida del primer año también con el deflactor del consumo personal (PCE), y la jornada
efectiva de tiempo completo (horas habituales de la CPS, OCDE) además de la jornada legal de 40 h.
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


def _jornada_tc(dir_datos, anios):
    """Horas habituales semanales de los asalariados de EE.UU. a tiempo completo (OCDE, a partir de la CPS), desde 1979.
    Antes de 1979 se mantiene el valor de 1979 (se marca en la columna jornada_tc_extrapolada)."""
    for fn in (os.path.join(dir_datos, 'ocde', 'ocde_horas_habituales_usa_bruto.csv'), os.path.join(RAIZ, 'datos_cache', 'ocde_horas_habituales_usa_bruto.csv')):
        if os.path.exists(fn): break
    else:
        return None, None
    d = pd.read_csv(fn)
    d = d[(d.SEX == '_T') & (d.AGE == '_T') & (d.WORK_TIME_ARNGMNT == 'FT')].set_index('TIME_PERIOD').OBS_VALUE.sort_index()
    if d.empty: return None, None
    s = d.reindex(sorted(set(d.index) | set(anios))).bfill().ffill().reindex(anios)
    return s, pd.Series([a < d.index.min() or a > d.index.max() for a in anios], index=anios)


def calcular(dir_datos, dir_out, ee, hm=None):
    c = ee['masa']['c'].copy()
    defl = c['expresion_monetaria_hora'] / c['expresion_monetaria_hora_real']   # deflactor del PIB / 100
    H = c['horas_productivas_mill']
    w_real = c['V'] / H / defl
    mu_real = c['expresion_monetaria_hora_real']
    a0 = int(c.index.min())
    w_nom, mu_nom = c['V'] / H, c['expresion_monetaria_hora']
    U = pd.DataFrame({
        'necesario_efectivo_h': c['semana_tc_necesario'],
        'plustrabajo_h': c['semana_tc_plustrabajo'],
        'necesario_nivel_inicial_h': 40 * w_real.loc[a0] / mu_real,
        'parte_necesaria_pct': 100 / (1 + c['e']),
        'valor_nuevo_real_hora_idx': mu_real / mu_real.loc[a0] * 100,
        'salario_real_hora_idx': w_real / w_real.loc[a0] * 100,
    })
    # v2: el salario del primer año valuado con los precios del consumo (deflactor del gasto de consumo personal, PCE):
    # horas que hoy bastarían para producir el valor de la canasta que compraba ese salario
    N = ee.get('N') or {}
    if 'DPCERG' in N:
        pce = pd.Series(N['DPCERG']).reindex(c.index).astype(float)
        U['necesario_nivel_inicial_pce_h'] = 40 * w_nom.loc[a0] * (pce / pce.loc[a0]) / mu_nom
        U['salario_real_hora_pce_idx'] = (w_nom / pce) / (w_nom.loc[a0] / pce.loc[a0]) * 100
    # v2: jornada efectiva de tiempo completo (horas habituales, CPS) en lugar de la jornada legal de 40 h
    J, extrap = _jornada_tc(dir_datos, list(c.index))
    if J is not None:
        U['jornada_tc_h'] = J
        U['jornada_tc_extrapolada'] = extrap
        U['necesario_jornada_tc_h'] = J / (1 + c['e'])
        U['plustrabajo_jornada_tc_h'] = J - U['necesario_jornada_tc_h']
    U.index.name = 'anio'
    z = U.iloc[-1]; i0 = U.iloc[0]
    liberado = float(i0.necesario_efectivo_h - z.necesario_nivel_inicial_h)
    consumo = float(z.necesario_efectivo_h - z.necesario_nivel_inicial_h)
    plus = float(z.plustrabajo_h - i0.plustrabajo_h)
    desc = dict(desde=a0, hasta=int(U.index[-1]), liberado_h=liberado, consumo_h=consumo, plustrabajo_h=plus, jornada_h=0.0,
                consumo_pct=100 * consumo / liberado, plustrabajo_pct=100 * plus / liberado)
    if 'necesario_nivel_inicial_pce_h' in U:
        lib_p = float(i0.necesario_efectivo_h - z.necesario_nivel_inicial_pce_h); con_p = float(z.necesario_efectivo_h - z.necesario_nivel_inicial_pce_h)
        desc.update(liberado_pce_h=lib_p, consumo_pce_h=con_p, consumo_pce_pct=100 * con_p / lib_p, plustrabajo_pce_pct=100 * plus / lib_p)
    if 'jornada_tc_h' in U:
        primer = int(U.index[~U.jornada_tc_extrapolada.astype(bool)][0])
        desc.update(jornada_tc_inicio=float(U.jornada_tc_h.loc[primer]), jornada_tc_anio_inicio=primer, jornada_tc_fin=float(z.jornada_tc_h),
                    plustrabajo_jornada_tc_fin=float(z.plustrabajo_jornada_tc_h), plustrabajo_jornada_tc_inicio=float(U.plustrabajo_jornada_tc_h.loc[primer]))
    U.to_csv(os.path.join(dir_out, 'fuerzas_eeuu.csv'))
    out = dict(eeuu=U, desc=desc, mundo=None)
    if hm is not None:
        from sismografo.horas_mundo import CENTRAL
        P = hm['P']; Q = P[P.variante == CENTRAL]
        # variante: más las horas de los asalariados de la educación y la salud públicas y sin fines de lucro, trabajo
        # improductivo para el capital pero socialmente necesario (diferencia entre la variante con educación y salud
        # productivas y la central)
        Qp = P[P.variante == 'educación y salud productivas'].set_index(['pais', 'anio']).horas_mill
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
            hpub = float(sum(max(0.0, Qp.get((c_, y), np.nan) - g.horas_mill[c_]) for c_ in g.index[ok] if np.isfinite(Qp.get((c_, y), np.nan)))) * 1e6
            m = lambda h: h / hab / 365 * 60
            filas.append(dict(anio=y, paises=int(ok.sum()), poblacion_mill=hab / 1e6, poblacion_pct_mundo=hab / mundo_hab * 100, obreros_mill=float(g.obreros_mill[ok].sum()),
                              obreros_pct_poblacion=float(g.obreros_mill[ok].sum()) * 1e6 / hab * 100,
                              min_productivo_dia=m(hp), min_necesario_dia=m(hp - hs), min_plustrabajo_dia=m(hs),
                              min_plustrabajo_neto_dia=m(hsn), parte_necesaria_pct=(hp - hs) / hp * 100,
                              min_educacion_salud_publicas_dia=m(hpub), min_socialmente_necesario_dia=m(hp + hpub),
                              poblacion_extrapolada=bool(y > ult_pwt)))
        Wd = pd.DataFrame(filas)
        Wd.to_csv(os.path.join(dir_out, 'fuerzas_mundo.csv'), index=False)
        out['mundo'] = Wd
    return out
