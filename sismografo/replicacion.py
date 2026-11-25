"""Replicación de las series de los autores (F1.2).

Cada serie se construye con la definición publicada por el autor, pero con los datos vigentes de la BEA
(revisión integral de 2023 y siguientes). Se contrasta con los valores que el propio autor publicó. La
diferencia mide dos cosas a la vez: lo que cambió en las cuentas (capitalización de la propiedad intelectual
en 1999 y 2013, revisiones de la remuneración y del capital) y lo que nuestra aproximación no reproduce de su
método. No se busca «acertar» a los números de nadie: se busca saber si las tendencias que cada lectura
interpreta siguen ahí cuando se rehacen con los datos de hoy.

Fuentes de los valores publicados (véase metodología, «Replicación de las series de los autores»):
- Shaikh y Tonak (1994), Measuring the Wealth of Nations, cuadros 5.6 y 5.8.
- Moseley (1991), The Falling Rate of Profit in the Postwar United States Economy, cap. 3; cifras 1947 y 1977
  reproducidas en Moseley (1997), «The Rate of Profit and the Future of Capitalism», RRPE 29 (4).
- Kliman (2010), «Appearance and Essence», MHI; y (2012) The Failure of Capitalist Production, cap. 5.
- Duménil y Lévy (2002), «The Profit Rate: Where and How Much Did It Fall? Did It Recover? (USA 1948-2000)»,
  Review of Radical Political Economics 34 (4), cuadro 3.
- Roberts, «The US rate of profit in 2017» (2 nov. 2018) y «The US rate of profit in 2020» (5 dic. 2021),
  blog The Next Recession.
"""
import os
import numpy as np, pandas as pd
from .eeuu import Datos

# Valores publicados. tipo: 'nivel' (valor del año) o 'cambio' (variación porcentual entre dos años)
# o 'razon' (cociente entre dos años, en %).
PUBLICADOS = [
    # Shaikh y Tonak (1994), cuadro 5.6 (S*/V*) y 5.8 (tasa marxiana S*/K*, sin ajuste por utilización)
    *[dict(autor='Shaikh y Tonak', serie='st_e', medida='Tasa de plusvalor S*/V*', tipo='nivel', anio=a, valor=v,
           fuente='Shaikh y Tonak (1994), cuadro 5.6') for a, v in
      [(1948, 1.70), (1950, 1.77), (1958, 2.01), (1975, 2.11), (1977, 2.10), (1980, 2.07), (1982, 2.19), (1985, 2.33), (1989, 2.44)]],
    *[dict(autor='Shaikh y Tonak', serie='st_r', medida='Tasa marxiana S*/K* (sin ajuste)', tipo='nivel', anio=a, valor=v,
           fuente='Shaikh y Tonak (1994), cuadro 5.8') for a, v in
      [(1948, 0.39), (1950, 0.38), (1958, 0.36), (1975, 0.33), (1977, 0.33), (1980, 0.30), (1982, 0.29), (1985, 0.34), (1989, 0.35)]],
    # tendencia de la tasa marxiana (el nivel no es comparable: ellos usan el acervo bruto, aquí el neto)
    *[dict(autor='Shaikh y Tonak', serie='st_r', medida='Tasa marxiana S*/K*: variación', tipo='razon', desde=a, anio=b, valor=round(100 * vb / va, 1),
           fuente='Shaikh y Tonak (1994), cuadro 5.8') for a, b, va, vb in [(1975, 1982, 0.33, 0.29), (1982, 1989, 0.29, 0.35), (1975, 1989, 0.33, 0.35)]],
    # Moseley (1991): 1947 y 1977
    *[dict(autor='Moseley', serie=s, medida=m, tipo='nivel', anio=1977, valor=v,
           fuente='Moseley (1991), cap. 3; Moseley (1997)') for s, m, v in
      [('mo_rs', 'Tasa de plusvalor S/V', 1.63), ('mo_cc', 'Composición C/V', 5.03), ('mo_uf', 'Trabajo improductivo Uf/V', 0.94),
       ('mo_us', 'Capital improductivo Us/V', 0.66), ('mo_r', 'Tasa de ganancia convencional', 0.12)]],
    # Kliman (2010): tasa antes de impuestos, costo histórico
    *[dict(autor='Kliman', serie='kl_pat', medida='Ganancia antes de impuestos / activos fijos a costo histórico', tipo='nivel', anio=a, valor=v,
           fuente='Kliman (2010), «Appearance and Essence», fig. 3') for a, v in [(1978, 0.24), (2001, 0.12)]],
    # Duménil y Lévy (2002), cuadro 3: tasa amplia r_b, sector corporativo
    *[dict(autor='Duménil y Lévy', serie='dl_rb', medida='Tasa amplia r_b, sociedades', tipo='razon', desde=a, anio=b, valor=v,
           fuente='Duménil y Lévy (2002), cuadro 3') for a, b, v in [(1948, 1982, 58.5), (1982, 2000, 144.9), (1948, 2000, 84.8)]],
    *[dict(autor='Duménil y Lévy', serie='dl_rb_sinppi', medida='Tasa amplia r_b, sociedades, sin propiedad intelectual', tipo='razon', desde=a, anio=b, valor=v,
           fuente='Duménil y Lévy (2002), cuadro 3') for a, b, v in [(1948, 1982, 58.5), (1982, 2000, 144.9), (1948, 2000, 84.8)]],
    # Roberts: «toda la economía», costo histórico y costo corriente
    *[dict(autor='Roberts', serie=s, medida=m, tipo='cambio', desde=a, anio=b, valor=v, fuente=f) for s, m, a, b, v, f in [
        ('ro_hc', 'Toda la economía, costo histórico', 1965, 1982, -21, 'Roberts (2018)'),
        ('ro_cc', 'Toda la economía, costo corriente', 1965, 1982, -36, 'Roberts (2018)'),
        ('ro_hc', 'Toda la economía, costo histórico', 1982, 1997, 10, 'Roberts (2018)'),
        ('ro_cc', 'Toda la economía, costo corriente', 1982, 1997, 29, 'Roberts (2018)'),
        ('ro_hc', 'Toda la economía, costo histórico', 1965, 1982, -23, 'Roberts (2021)'),
        ('ro_cc', 'Toda la economía, costo corriente', 1965, 1982, -37, 'Roberts (2021)'),
        ('ro_hc', 'Toda la economía, costo histórico', 1982, 1997, 15, 'Roberts (2021)'),
        ('ro_cc', 'Toda la economía, costo corriente', 1982, 1997, 35, 'Roberts (2021)')]],
]

NOMBRES = {
    'st_e': 'Shaikh y Tonak: S*/V* (V* = obreros de producción)', 'st_r': 'Shaikh y Tonak: tasa marxiana S*/K (V* = obreros de producción)',
    'st_e_ramas': 'Shaikh y Tonak: S*/V* (V* = remuneración de las ramas productivas)', 'st_r_ramas': 'Shaikh y Tonak: tasa marxiana S*/K (por ramas)',
    'mo_rs': 'Moseley: S/V', 'mo_cc': 'Moseley: C/V', 'mo_uf': 'Moseley: Uf/V', 'mo_us': 'Moseley: Us/V', 'mo_r': 'Moseley: tasa convencional',
    'kl_pi': 'Kliman: ingreso de propiedad / K histórico (t−1)', 'kl_tp': 'Kliman: ganancia total / K histórico (t−1)',
    'kl_pat': 'Kliman: ganancia antes de impuestos / K histórico (t−1)',
    'dl_rb': 'Duménil y Lévy: r_b, sociedades', 'dl_rb_sinppi': 'Duménil y Lévy: r_b, sociedades, sin propiedad intelectual',
    'dl_rb_snf': 'Duménil y Lévy: r_b, sociedades no financieras',
    'ro_hc': 'Roberts: toda la economía, costo histórico', 'ro_cc': 'Roberts: toda la economía, costo corriente',
}


def construir(D, ee):
    s = lambda c: D.s('N', c)
    fa = D.fa
    Y = D.YEARS
    R = pd.DataFrame(index=pd.Index(Y, name='anio'))

    # --- Shaikh y Tonak: S* = producto neto empresarial − V*; V* = remuneración en ramas productivas.
    # Es nuestro plusvalor «por ramas» sin la deducción de la explotación secundaria (B4), que ellos no hacen.
    # Su V* son los salarios de los trabajadores productivos (obreros de producción de las ramas productivas): lo más
    # cercano es nuestra corrección intra-rama, disponible desde 1972. Desde 1948 sólo hay la versión por ramas, que
    # cuenta como V* toda la remuneración de las ramas productivas (supervisores incluidos) y es por eso una cota inferior.
    b = ee['masa']['b']; c = ee['masa']['c']
    Sb = b['S'] + ee['FH'].reindex(b.index); Sc_ = c['S'] + ee['FH'].reindex(c.index)
    R['st_e'] = Sc_ / c['V']
    R['st_e_ramas'] = Sb / b['V']
    R['st_r'] = Sc_ / c['K']
    R['st_r_ramas'] = Sb / b['K']

    # --- Moseley: V = salarios de producción y no supervisión en ramas productivas (corrección intra-rama);
    # Uf = el resto de la remuneración empresarial; C = capital de las ramas productivas, con inventarios (su «capital
    # total invertido»); Us = capital fijo de las ramas de circulación. Su identidad RP = (S − Uf)/(C + Us) iguala la tasa
    # convencional con la marxiana corregida; como la ganancia convencional no incluye los impuestos indirectos, aquí
    # S se toma sin ellos (lectura nuestra de su identidad; él remite a las fuentes y métodos de su libro de 1991).
    FHc = ee['FH'].reindex(c.index)
    COMP_BUS = (s('A442RC') + s('W462RC')).reindex(c.index)
    T_ind = s('W056RC').reindex(c.index)
    Sc = c['S'] + FHc - T_ind
    K_unp = sum(fa('k1', t) for t in ('n42001es00', 'n44RT1es00', 'n52001es00', 'n54111es00')).reindex(c.index)
    R['mo_rs'] = Sc / c['V']
    R['mo_uf'] = (COMP_BUS - c['V']) / c['V']
    R['mo_cc'] = (c['K'] - K_unp + D.INV.reindex(c.index)) / c['V']
    R['mo_us'] = K_unp / c['V']
    R['mo_r'] = (R['mo_rs'] - R['mo_uf']) / (R['mo_cc'] + R['mo_us'])

    # --- Kliman: sociedades, depreciación y activos a costo histórico; capital adelantado = acervo al cierre del año anterior.
    Dcc, Dhc = fa('m1', 'ptotl2es00'), fa('m3', 'ptotl2es00')
    Khc_1 = fa('k3', 'ptotl2es00').shift(1)
    nva_hc = s('A451RC') - Dhc
    R['kl_pi'] = (nva_hc - s('A442RC')) / Khc_1                 # ingreso de propiedad: valor agregado neto − remuneración
    R['kl_tp'] = (s('W322RC') + Dcc - Dhc) / Khc_1              # ganancia total: excedente neto de explotación
    R['kl_pat'] = (s('A445RC') + Dcc - Dhc) / Khc_1             # ganancia antes de impuestos (con IVA)

    # --- Duménil y Lévy: r_b = (producto neto − remuneración) / capital fijo no residencial a costo corriente.
    K = fa('k1', 'ntotl2es00')
    nva = s('A439RC')                                           # valor agregado neto de las sociedades (NIPA 1.14, línea 3)
    R['dl_rb'] = (nva - s('A442RC')) / K
    ip_inv, ip_dep, ip_k = fa('i3', 'ntotl2ip00'), fa('m1', 'ntotl2ip00'), fa('k1', 'ntotl2ip00')
    R['dl_rb_sinppi'] = (nva - s('A442RC') - ip_inv + ip_dep) / (K - ip_k)
    R['dl_rb_snf'] = (s('A457RC') - s('A460RC')) / fa('k1', 'nnofi2es00')

    # --- Roberts: plusvalor = ingreso nacional − remuneración; C = activos fijos privados no residenciales; r = s/(C+v).
    sv, v = s('A032RC') - s('A033RC'), s('A033RC')
    R['ro_hc'] = sv / (fa('k3', 'ntotl1es00') + v)
    R['ro_cc'] = sv / (fa('k1', 'ntotl1es00') + v)
    return R


def contrastar(R):
    filas = []
    for p in PUBLICADOS:
        x = R[p['serie']]
        if p['tipo'] == 'nivel':
            rec = x.get(p['anio'], np.nan)
            dif = rec - p['valor']
        elif p['tipo'] == 'razon':
            rec = 100 * x.get(p['anio'], np.nan) / x.get(p['desde'], np.nan); dif = rec - p['valor']
        else:
            rec = 100 * (x.get(p['anio'], np.nan) / x.get(p['desde'], np.nan) - 1); dif = rec - p['valor']
        tramo = str(p['anio']) if p['tipo'] == 'nivel' else f"{p['desde']}–{p['anio']}"
        if np.isnan(rec): juicio = 'sin datos comparables'
        elif p['serie'] == 'st_r' and p['tipo'] == 'nivel': juicio = 'nivel no comparable (acervo bruto frente a neto)'
        elif p['tipo'] == 'nivel': e = abs(dif) / abs(p['valor']); juicio = 'reproduce' if e <= .10 else 'aproxima' if e <= .25 else 'no reproduce'
        else:
            mismo = np.sign(rec - (100 if p['tipo'] == 'razon' else 0)) == np.sign(p['valor'] - (100 if p['tipo'] == 'razon' else 0))
            juicio = 'reproduce' if abs(dif) <= 5 and mismo else 'aproxima' if abs(dif) <= 12 and mismo else 'misma dirección, otra magnitud' if mismo else 'no reproduce'
        filas.append(dict(autor=p['autor'], serie=p['serie'], medida=p['medida'], tipo=p['tipo'], tramo=tramo,
                          publicado=p['valor'], reconstruido=rec, diferencia=dif, juicio=juicio, fuente=p['fuente']))
    return pd.DataFrame(filas)


def tendencias(R):
    """Lo que interesa a la lectura: ¿cae de 1965 (o del máximo de la posguerra) a 1982 y se recupera después?"""
    filas = []
    for k in ['st_e', 'st_e_ramas', 'st_r', 'st_r_ramas', 'mo_rs', 'mo_r', 'kl_pi', 'kl_tp', 'kl_pat', 'dl_rb', 'dl_rb_sinppi', 'ro_hc', 'ro_cc']:
        x = R[k].dropna()
        a0 = int(x.index[0]); a1 = int(x.index[-1])
        g = lambda a, b: 100 * (x[b] / x[a] - 1) if a in x.index and b in x.index else np.nan
        filas.append(dict(serie=k, nombre=NOMBRES[k], desde=a0, hasta=a1, inicio=x.iloc[0], v1965=x.get(1965, np.nan), v1982=x.get(1982, np.nan),
                          v1997=x.get(1997, np.nan), final=x.iloc[-1], cambio_1965_1982=g(1965, 1982), cambio_1982_1997=g(1982, 1997),
                          cambio_1997_final=g(1997, a1), cambio_total=g(a0, a1)))
    return pd.DataFrame(filas)


def calcular(dir_datos, dir_out, ee):
    D = Datos(dir_datos)
    R = construir(D, ee)
    C = contrastar(R)
    T = tendencias(R)
    R.to_csv(os.path.join(dir_out, 'replicacion_series.csv'))
    C.to_csv(os.path.join(dir_out, 'replicacion_contraste.csv'), index=False)
    T.to_csv(os.path.join(dir_out, 'replicacion_tendencias.csv'), index=False)
    return dict(R=R, C=C, T=T)
