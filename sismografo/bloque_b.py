"""Auditoría, bloque B: supuestos del plusvalor.

Decisión del autor (24 nov. 2026): B3 y B4 forman parte de la medición central. Este módulo los documenta y muestra
cuánto cambian las cifras respecto de la convención de las cuentas nacionales.

B4 — Explotación secundaria (finanzas). El valor agregado de las finanzas entra en el plusvalor, pero la parte que
     pagan los hogares con sus salarios por servicios financieros (intereses implícitos —FISIM— y comisiones) no es
     plusvalor producido, sino plusvalor desplazado desde el salario hacia el capital financiero. Se resta del plusvalor
     en la parte que corresponde a los salarios:
       EE.UU.: gasto de consumo personal en servicios financieros (NIPA 2.4.5, DFNLRC) × remuneración / ingreso personal
               (en eeuu.py);
       Mundo:  consumo final de los hogares de K64–K66 (WIOD) × participación del trabajo (PWT labsh) (en horas_mundo.py).
B3 — Renta comercial (mundo). La renta que los capitales de las ramas de mercado pagan por locales y oficinas es
     plusvalor producido y cedido a la propiedad territorial: se suma (consumo intermedio de L68, WIOD). En EE.UU. ya
     está dentro: el plusvalor del sector empresarial incluye el inmobiliario comercial y excluye sólo la vivienda.
     Después de 2014 (sin tablas WIOD) se mantienen las proporciones de 2014 de cada país.
B5 — Salario social neto (sensibilidad; Shaikh y Tonak, 1994). El Estado cobra impuestos a los trabajadores y les
     devuelve prestaciones. Salario social neto = prestaciones recibidas por los hogares asalariados (prestaciones
     sociales del gobierno + gasto público en educación, × remuneración / ingreso personal) − impuestos que pagan
     (impuestos personales × remuneración / ingreso personal + contribuciones a la seguridad social). Se asigna a los
     obreros productivos en proporción a su remuneración. Si es positivo, el Estado traslada plusvalor al salario; si es
     negativo, los trabajadores financian más de lo que reciben. Variante: e = (S − SSN) / (V + SSN). Desde 1959.
B2 — Supervisión y dirección. EE.UU. ofrece dos cotas: por ramas (supervisores y gerentes en v) e intra-rama (sólo
     obreros de producción y no supervisores; los sueldos de supervisión quedan en el plusvalor). Se registra la parte
     de la remuneración de las ramas productivas que no es de obreros de producción y no supervisores.
"""
import functools, os

import numpy as np, pandas as pd

FIN = ['K64', 'K65', 'K66']
FUERA = ['L68', 'O84', 'T', 'U']


def _ssn(dir_datos):
    """Salario social neto de la economía (millones de USD) y su proporción sobre la remuneración total."""
    from .eeuu import Datos
    D = Datos(dir_datos)
    comp = D.s('N', 'A033RC'); lam = comp / D.s('N', 'A065RC')
    ben = lam * (D.s('N', 'A063RC') + D.s('N', 'G16029').reindex(lam.index))
    imp = lam * D.s('N', 'W055RC') + D.s('N', 'A061RC')
    return ben - imp, comp


def _eeuu(ee, dir_datos=None):
    fh, fht = ee['FH'], ee['FH_TOTAL']
    out = {}
    for prod in ('b', 'c'):
        S, K, V = ee['SK'][f'B|{prod}|cc|neta|ppi-incl|K-todo|noutil']
        S, K, V = (x.reindex(fh.index) for x in (S, K, V))
        out[f'e_{prod}'] = S / V                                                # central: sin los pagos de los hogares
        out[f'e_{prod}_cuentas'] = (S + fh) / V                                 # convención de las cuentas nacionales
        out[f'r_{prod}'] = S / (K + V) * 100
        out[f'r_{prod}_cuentas'] = (S + fh) / (K + V) * 100
        out[f'desplazado_pct_pv_{prod}'] = fh / (S + fh) * 100
    Sb = ee['SK']['B|b|cc|neta|ppi-incl|K-todo|noutil'][0].reindex(fh.index)
    out['fin_hogares_total_pct_pv_b'] = fht / (Sb + fh) * 100
    Vb = ee['SK']['B|b|cc|neta|ppi-incl|K-todo|noutil'][2]; Vc = ee['SK']['B|c|cc|neta|ppi-incl|K-todo|noutil'][2]
    out['supervision_pct_v_ramas'] = (1 - Vc / Vb) * 100
    if dir_datos:
        try:
            ssn, comp = _ssn(dir_datos)
            out['ssn_pct_remuneracion'] = (ssn / comp * 100).reindex(fh.index)
            for prod in ('b', 'c'):
                S, K, V = (x.reindex(fh.index) for x in ee['SK'][f'B|{prod}|cc|neta|ppi-incl|K-todo|noutil'])
                sp = (ssn / comp).reindex(fh.index) * V                         # parte de los obreros productivos
                out[f'e_{prod}_ssn'] = (S - sp) / (V + sp)
        except Exception as e:  # noqa: BLE001
            print('Salario social neto omitido:', repr(e))
    E = pd.DataFrame(out); E.index.name = 'anio'
    sel = [c for c in E.columns if c.endswith(('_c', '_c_cuentas', '_c_ssn')) or c == 'supervision_pct_v_ramas']
    E.loc[E.index < 1972, sel] = np.nan
    return E


@functools.lru_cache(maxsize=1)
def _cuotas_cache():
    from .transformacion import RAMAS, _leer_niots, ZIP
    if not os.path.exists(ZIP): return pd.DataFrame()
    mercado = [r for r in RAMAS if r not in FUERA]
    filas = []
    for c, d in _leer_niots().items():
        for y in sorted(d.anio.dropna().unique()):
            t = d[d.anio == y]
            uso = t[t.origen.isin(['Domestic', 'Imports'])]
            tot = t[t.origen == 'TOT'].set_index('code')
            va = pd.to_numeric(tot.loc['VA', mercado], errors='coerce').sum()
            if not va > 0: continue
            renta = pd.to_numeric(uso[uso.code == 'L68'][mercado].stack(), errors='coerce').sum()
            fin = pd.to_numeric(uso[uso.code.isin(FIN)]['CONS_h'], errors='coerce').sum()
            filas.append(dict(pais=c, anio=int(y), renta_pct_va=renta / va, fin_hogares_pct_va=fin / va))
    return pd.DataFrame(filas)


def cuotas_wiod():
    """Por país y año (2000–2014): renta pagada por las ramas de mercado y servicios financieros de los hogares,
    como proporción del valor agregado de las ramas de mercado (dólares corrientes, WIOD)."""
    return _cuotas_cache().copy()


def _mundo(hm):
    from .horas_mundo import CENTRAL
    Q = hm['P'][hm['P'].variante == CENTRAL].copy()
    if 'e_sin_ajuste_b' not in Q: return pd.DataFrame()
    k = 1 + Q.e_sin_ajuste_b + Q.cp_v.fillna(0)                                  # VA de mercado / v
    b3, b4 = Q.b3_pct_va.fillna(0), Q.b4_pct_va.fillna(0)
    filas = []
    for nombre, ajuste in (('Central (con B3 y B4)', b3 - b4), ('Convención de las cuentas (sin B3 ni B4)', 0 * b3),
                           ('Sólo B3: + renta comercial', b3), ('Sólo B4: − servicios financieros de los hogares', -b4)):
        e2 = (Q.e_sin_ajuste_b + ajuste * k).clip(lower=0.01)
        Q['_pl'] = Q.horas_mill * e2 / (1 + e2)
        g = Q.groupby('anio').agg(pl=('_pl', 'sum'), h=('horas_mill', 'sum'))
        for y, r in g.iterrows():
            filas.append(dict(anio=int(y), variante=nombre, plustrabajo_mmh=r.pl / 1000, e_horas=r.pl / (r.h - r.pl)))
    return pd.DataFrame(filas)


def calcular(dir_datos, dir_out, ee, hm=None):
    E = _eeuu(ee, dir_datos)
    E.to_csv(os.path.join(dir_out, 'bloque_b_eeuu.csv'))
    M = _mundo(hm) if hm is not None else pd.DataFrame()
    if not M.empty:
        M.to_csv(os.path.join(dir_out, 'bloque_b_mundo.csv'), index=False)
        cuotas_wiod().to_csv(os.path.join(dir_out, 'bloque_b_cuotas_wiod.csv'), index=False)
    return dict(E=E, M=M)
