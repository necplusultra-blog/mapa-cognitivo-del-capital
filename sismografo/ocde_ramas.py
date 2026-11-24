"""Medición por rama de los años recientes con las cuentas nacionales por industria de la OCDE (SNA 2008).

Tabla 6 (DSD_NAMAIN10@DF_TABLE6): valor agregado bruto (B1G), remuneración de los asalariados (D1) y consumo de
capital fijo (P51C) por sección de actividad, en moneda nacional a precios corrientes.
Tabla 7 (DSD_NAMAIN10@DF_TABLE7): asalariados (SAL) y no asalariados (SELF) en personas y en horas trabajadas.

Se aplica el mismo criterio por ramas que con WIOD, a nivel de sección CIIU rev. 4:
- improductivas por circulación: G (comercio), K (finanzas y seguros), M69–M70 (jurídicas, contables, dirección),
  M73 (publicidad);
- fuera de la producción capitalista: L (inmobiliario), O (administración pública), T (hogares), U;
- P (educación) y Q (salud): dos variantes.
Hogares (T) y organismos extraterritoriales (U) faltantes se toman como cero. Si faltan secciones que son todas
productivas y de mercado (p. ej. Japón: E, N, S), su suma se obtiene como residuo del total de la economía (_T).
Cuando un país no informa las divisiones M69–M70 y M73, su peso dentro de la sección M se toma del propio país
en WIOD 2014 (misma variable) y se mantiene constante. Ese supuesto queda registrado en la columna «m_imputado».

Para cada país y año t ≥ 2014:
  v_t     = Σ_productivas D1
  cp_t    = Σ_mercado SELF_personas × (D1 / SAL_personas) de la misma sección   (ingreso laboral imputado a los
            trabajadores por cuenta propia: no son asalariados del capital)
  pv_t    = Σ_mercado B1G − cp_t − v_t                e_t = pv_t / v_t
  r_t     = Σ_mercado P51C / v_t                      (depreciación por unidad de capital variable)
  N_t     = Σ_productivas SAL_personas                H_t = Σ_productivas SAL_horas
Las series se encadenan al nivel WIOD de 2014 (véase horas_mundo.py), de modo que la OCDE aporta la variación
medida por rama y WIOD el nivel. Los cocientes OCDE/WIOD de 2014 se publican como diagnóstico.
"""
import os
import numpy as np, pandas as pd

IMPROD_CIRC = ['G', 'K']
FUERA = ['L', 'O', 'T', 'U']
PUBLICAS = ['P', 'Q']
SECCIONES = list('ABCDEFGHIJKLMNOPQRSTU')
# divisiones WIOD equivalentes, para imputar M69–M70 y M73 cuando falten
WIOD_M = ['M69_M70', 'M71', 'M72', 'M73', 'M74_M75']
WIOD_VAR = {'B1G': 'VA', 'D1': 'COMP', 'P51C': 'VA', 'SAL_PS': 'EMPE', 'SAL_H': 'H_EMPE', 'SELF_PS': 'EMP'}


def _leer(dir_datos, cache):
    out = {}
    for t in ('t6', 't7'):
        fn = os.path.join(dir_datos, 'ocde', f'ocde_{t}.csv')
        if not os.path.exists(fn): fn = os.path.join(cache, f'ocde_{t}.csv')
        if not os.path.exists(fn): return None
        out[t] = pd.read_csv(fn, low_memory=False)
    t6 = out['t6'][['REF_AREA', 'TRANSACTION', 'ACTIVITY', 'TIME_PERIOD', 'OBS_VALUE']].copy()
    t6['var'] = t6.TRANSACTION
    t7 = out['t7'][['REF_AREA', 'TRANSACTION', 'ACTIVITY', 'UNIT_MEASURE', 'TIME_PERIOD', 'OBS_VALUE']].copy()
    t7['var'] = t7.TRANSACTION + '_' + t7.UNIT_MEASURE
    d = pd.concat([t6, t7], ignore_index=True)
    return d.pivot_table(index=['REF_AREA', 'TIME_PERIOD', 'ACTIVITY'], columns='var', values='OBS_VALUE', aggfunc='first')


def calcular(dir_datos, cache, wiod):
    """wiod: dict variable → DataFrame indexado por (país, código) con columnas de años (de horas_mundo)."""
    D = _leer(dir_datos, cache)
    if D is None: return pd.DataFrame()
    filas = []
    for c in sorted(D.index.get_level_values(0).unique()):
        dc = D.loc[c]
        for variante, publicas_prod in (('educación y salud productivas', True), ('educación y salud fuera', False)):
            fuera = FUERA + ([] if publicas_prod else PUBLICAS)
            improd = IMPROD_CIRC + fuera
            for y in sorted(dc.index.get_level_values(0).unique()):
                g = dc.loc[y]
                if 'B1G' not in g or 'D1' not in g: continue
                sec = g.reindex(SECCIONES).copy()
                tot = g.loc['_T'] if '_T' in g.index else None
                prod = [s for s in SECCIONES if s not in improd]
                mercado = [s for s in SECCIONES if s not in fuera]
                residual = False
                for var in sec.columns:
                    if sec[var].isna().all(): continue
                    sec.loc[['T', 'U'], var] = sec.loc[['T', 'U'], var].fillna(0)   # hogares y extraterritoriales: casi nulos
                    falta = sec.index[sec[var].isna()].tolist()
                    # secciones faltantes que son todas productivas y de mercado (p. ej. Japón: E, N, S): se completan
                    # con el residuo del total de la economía, porque solo importa su suma
                    if falta and tot is not None and not pd.isna(tot.get(var)) and 'M' not in falta \
                            and all(f in prod and f in mercado for f in falta):
                        sec.loc[falta, var] = 0.0
                        sec.loc[falta[0], var] = float(tot[var] - sec[var].sum())
                        residual = True
                if sec[['B1G', 'D1']].isna().any().any(): continue
                imputado = False

                def m_improd(var):
                    """Parte improductiva de la sección M (M69–M70 + M73) para la variable var."""
                    nonlocal imputado
                    if var not in g: return 0.0
                    partes = [g[var].get(k, np.nan) for k in ('M69_70', 'M73')]
                    if not any(pd.isna(p) for p in partes): return float(sum(partes))
                    imputado = True
                    w = WIOD_VAR[var]
                    try:
                        m = wiod[w].loc[c].reindex(WIOD_M)[2014]
                        share = (m['M69_M70'] + m['M73']) / m.sum()
                    except (KeyError, ZeroDivisionError):
                        share = 0.25
                    return float(sec[var]['M'] * share) if not pd.isna(sec[var]['M']) else 0.0


                def suma(var, secs, m_parte):
                    if var not in sec: return np.nan
                    x = sec[var].reindex(secs)
                    if x.isna().any(): return np.nan
                    tot = float(x.sum())
                    if 'M' in secs and m_parte: tot -= m_improd(var)
                    return tot
                v = suma('D1', prod, True)
                # ingreso imputado a los no asalariados, sección por sección
                cp = np.nan
                if {'SELF_PS', 'SAL_PS'} <= set(sec.columns):
                    x = sec.reindex(mercado)
                    # una sección sin dato de no asalariados (p. ej. electricidad) se toma como cero
                    if x.SELF_PS.notna().sum() >= len(mercado) - 4 and not x[['SAL_PS', 'D1']].isna().any().any():
                        cp = float((x.SELF_PS.fillna(0) * x.D1 / x.SAL_PS.replace(0, np.nan)).fillna(0).sum())
                bm = suma('B1G', mercado, False)
                pv = bm - (0 if pd.isna(cp) else cp) - v
                cfc = suma('P51C', mercado, False)
                N = suma('SAL_PS', prod, True); H = suma('SAL_H', prod, True)
                filas.append(dict(pais=c, variante=variante, anio=int(y), v=v, pv=pv, e=pv / v,
                                  r=(cfc / v) if not pd.isna(cfc) else np.nan, N_mill=N / 1000 if not pd.isna(N) else np.nan,
                                  H_mill=H if not pd.isna(H) else np.nan, cuenta_propia_imputada=not pd.isna(cp), residuo=residual,
                                  m_imputado=imputado))
    return pd.DataFrame(filas)
