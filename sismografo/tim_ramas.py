"""China por rama después de 2014 (F3d v3): empleo y remuneración por rama de la OCDE (Trade in Employment, TiM 2025).

Fuente: OCDE, TiM edición 2025 (dataflow OECD.STI.PIE DSD_TIM_2025@DF_TIM_2025), coherente con las tablas mundiales
ICIO: ocupados (EMPN), remuneración del trabajo (LABR, en dólares) y su proporción del valor agregado (de la que se
obtiene el valor agregado), por rama, 2000–2022. Copia en datos_cache/ocde_tim_2025.csv.gz.

Para China, la remuneración de TiM es el ingreso del trabajo completo (incluye el de los trabajadores por cuenta
propia: en la agricultura supera el valor agregado), como en WIOD. Se aplica el mismo método que con WIOD:
  s_t      = asalariados OIT_t / (ocupación OIT_t × (1 − peso agrícola de la ocupación TiM_t)), con tope 1;
             la agricultura no tiene asalariados (agricultura familiar)
  v_t      = Σ_productivas LABR · s
  pv_t     = Σ_mercado (VA − LABR)        (se excluye todo el ingreso del trabajo, asalariado y por cuenta propia)
  e_t      = pv_t / v_t
Mismo criterio de ramas: circulación G, K y la parte de M que corresponde a servicios jurídicos, contables y
publicidad (su peso en WIOD 2014); fuera de la producción capitalista L, O, T; educación y salud (P, Q) en dos
variantes. La serie se encadena al nivel WIOD de 2014 (horas_mundo.combinar_un), de modo que TiM aporta la variación
medida por rama. No hay consumo de capital fijo por rama: la depreciación sigue la extensión agregada.
India no se trata aquí: en TiM su remuneración es sólo la de los asalariados, sin el ingreso mixto, y las cuentas de la
ONU ya la miden por rama.
"""
import os
import numpy as np, pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FN = os.path.join(RAIZ, 'datos_cache', 'ocde_tim_2025.csv.gz')
FN_M = os.path.join(RAIZ, 'datos_cache', 'wiod_fraccion_productiva_M.csv')
SECC = list('ABCDEFGHIJKLMNOPQRST')
CIRC, FUERA, PUB = ['G', 'K'], ['L', 'O', 'T'], ['P', 'Q']


def calcular(share_ees, variantes, paises=('CHN',), desde=2014):
    if not os.path.exists(FN): return pd.DataFrame()
    d = pd.read_csv(FN)
    d = d[d.pais.isin(paises) & d.actividad.isin(SECC) & (d.anio >= desde)]
    fm = pd.read_csv(FN_M).set_index('pais').phi_M if os.path.exists(FN_M) else pd.Series(dtype=float)
    ees, tot = share_ees
    filas = []
    for (c, y), g in d.groupby(['pais', 'anio']):
        g = g.set_index('actividad').reindex(SECC).fillna(0.0)
        if g.VA_musd.sum() <= 0: continue
        agro = g.EMPN_miles['A'] / g.EMPN_miles.sum()
        s = min(1.0, float(ees.get(y, np.nan) / (tot.get(y, np.nan) * (1 - agro))))
        if not np.isfinite(s):
            continue
        sv = pd.Series(s, index=SECC); sv['A'] = 0.0
        phi_m = float(fm.get(c, fm.median() if len(fm) else 0.45))
        for variante, publicas_prod in variantes:
            fuera = FUERA + ([] if publicas_prod else PUB)
            mercado = [k for k in SECC if k not in fuera]
            prod_peso = pd.Series(1.0, index=SECC)
            prod_peso[CIRC + fuera] = 0.0; prod_peso['M'] = phi_m
            v = float((g.LABR_musd * sv * prod_peso).sum())
            pv = float((g.VA_musd - g.LABR_musd)[mercado].sum())
            N = float((g.EMPN_miles * sv * prod_peso).sum()) / 1000
            if v > 0:
                filas.append(dict(pais=c, variante=variante, anio=int(y), e=pv / v, r=np.nan, segmento='TiM 2025',
                                  obreros_productivos_mill=N, s_asalariados=s))
    return pd.DataFrame(filas)
