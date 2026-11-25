"""Módulo de contratendencias: las seis causas contrarrestantes de Marx (El Capital, Libro III, cap. XIV).

Para cada contratendencia se reúnen indicadores observables (EE.UU. y, donde hay datos, mundo). Además se
descompone el movimiento de la tasa de ganancia por fases:

    r = pv/K = e · (V/K)        ⇒   Δln r = Δln e − Δln(K/V)

y, desde 1972, la composición en valor K/V se separa en una composición técnica y un precio relativo:

    K/V = (K_real / H) · (P_K / w)

donde K_real es el capital a precios de 2017, H las horas de los obreros productivos, P_K el precio implícito del
capital fijo y w la remuneración por hora productiva. Una composición técnica que sube mientras el precio relativo
baja es la forma observable del abaratamiento de los elementos del capital constante.

Las fases no se fijan de antemano: son los años de quiebre que el detector endógeno encuentra con más frecuencia
en el multiverso principal (véase quiebres.py y metodología §7).
"""
import collections, json, os, urllib.request

import numpy as np, pandas as pd

from sismografo.eeuu import Datos, _fred_anual

WB = 'https://api.worldbank.org/v2/country/WLD/indicator/{i}?format=json&per_page=200'
WB_IND = {'SL.EMP.VULN.ZS': 'empleo_vulnerable_mundial_pct', 'SL.UEM.TOTL.ZS': 'desempleo_mundial_pct',
          'NE.TRD.GNFS.ZS': 'comercio_mundial_pct_pib'}
CACHE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datos_cache', 'banco_mundial_contratendencias.csv')


def _banco_mundial():
    filas = []
    try:
        for ind, nombre in WB_IND.items():
            req = urllib.request.Request(WB.format(i=ind), headers={'User-Agent': 'Mozilla/5.0 sismografo-del-capital'})
            with urllib.request.urlopen(req, timeout=90) as r:
                for x in json.loads(r.read())[1]:
                    if x['value'] is not None: filas.append(dict(serie=nombre, anio=int(x['date']), valor=float(x['value'])))
        pd.DataFrame(filas).to_csv(CACHE, index=False)
    except Exception as e:  # noqa: BLE001
        print('Banco Mundial: se usa la copia guardada', repr(e))
    if not os.path.exists(CACHE): return pd.DataFrame()
    return pd.read_csv(CACHE).pivot_table(index='anio', columns='serie', values='valor')


def fases_endogenas(ee, n=5, separacion=6):
    """Años de quiebre más frecuentes en el multiverso principal (configuración base), separados entre sí."""
    cnt = collections.Counter()
    for c in ee['principal']: cnt.update(int(y) for y in ee['M'].loc[c, 'quiebres'])
    elegidos = []
    for y, _ in sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0])):
        if all(abs(y - e) >= separacion for e in elegidos): elegidos.append(y)
        if len(elegidos) == n: break
    return sorted(elegidos)


def calcular(dir_datos, dir_out, ee):
    D = Datos(dir_datos); Y = D.YEARS; f = D.dir_fred
    fred = lambda s: _fred_anual(os.path.join(f, s + '.csv')).reindex(Y) if os.path.exists(os.path.join(f, s + '.csv')) else pd.Series(np.nan, index=Y)
    N = lambda c: D.s('N', c, default=np.nan)
    b, c = ee['masa']['b'], ee['masa']['c']
    I = pd.DataFrame(index=pd.Index(Y, name='anio'))

    # A) Elevación del grado de explotación
    I['e_ramas'] = b['e']; I['e_intra'] = c['e'].reindex(Y)
    prod, salreal = fred('OPHNFB'), fred('COMPRNFB')
    I['productividad_hora_idx'] = prod / prod.get(1972) * 100
    I['remuneracion_real_hora_idx'] = salreal / salreal.get(1972) * 100
    I['semana_horas_productivas'] = c['semana_horas'].reindex(Y)
    ocup = fred('CE16OV')
    I['pluriempleo_pct_ocupados'] = fred('LNS12026619') / ocup * 100          # extensión del tiempo de trabajo fuera de un empleo
    I['tiempo_parcial_involuntario_pct'] = fred('LNS12032194') / ocup * 100

    # B) Reducción del salario por debajo de su valor
    ahe, cpi = fred('AHETPI'), fred('CPIAUCSL')
    I['salario_real_obreros_produccion'] = ahe / cpi * cpi.get(2017)          # USD de 2017 por hora
    I['servicio_deuda_hogares_pct_ingreso'] = fred('TDSP')

    # C) Abaratamiento de los elementos del capital constante
    I['precio_relativo_inversion_idx'] = (N('A008RD') / N('DPCERD3') if 'DPCERD3' in D.N else N('A008RD') / N('DPCERG'))
    I['precio_relativo_inversion_idx'] = I['precio_relativo_inversion_idx'] / I['precio_relativo_inversion_idx'].get(1972) * 100
    I['composicion_valor_ramas'] = b['K_V']; I['composicion_valor_intra'] = c['K_V'].reindex(Y)
    Kq, Kcc = D.s('F', 'kcntotl1es00', default=np.nan), D.s('F', 'k1ntotl1es00', default=np.nan)
    PK = Kcc / (Kq * Kcc.get(2017) / 100)                                       # precio implícito del capital, 2017 = 1
    Kreal = c['K'].reindex(Y) / PK                                              # capital empresarial a precios de 2017
    H = c['horas_productivas_mill'].reindex(Y) * 1e6; w = c['V'].reindex(Y) * 1e6 / H
    I['composicion_tecnica_idx'] = (Kreal / H) / (Kreal / H).get(1972) * 100
    I['precio_capital_sobre_salario_idx'] = (PK / w) / (PK / w).get(1972) * 100

    # D) Sobrepoblación relativa
    I['subempleo_u6_pct'] = fred('U6RATE')
    I['tasa_empleo_25_54_pct'] = fred('LNS12300060')
    I['obreros_productivos_mill'] = c['obreros_productivos_mill'].reindex(Y)

    # E) Comercio exterior
    I['ganancias_del_resto_del_mundo_pct'] = N('B933RC') / N('A051RC') * 100

    # F) Capital accionario y capital que devenga interés
    I['ganancias_financieras_pct_domesticas'] = N('A587RC') / N('A445RC') * 100
    I['intereses_netos_pct_excedente_nfc'] = N('B471RC') / N('W326RC') * 100
    I['dividendos_pct_ganancia_neta_nfc'] = N('B467RC') / N('A466RC') * 100
    I['emision_neta_acciones_pct_va_nfc'] = fred('BOGZ1FU103164103A') / N('A455RC') * 100
    pib = fred('GDP') * 1000                                                     # millones de USD
    I['acciones_nfc_valor_mercado_pct_pib'] = fred('NCBEILQ027S') / pib * 100
    I['deuda_nfc_pct_pib'] = fred('BCNSDODNS') / pib * 100

    W = _banco_mundial()
    if not W.empty:
        # el agregado mundial del último año se calcula con pocos países y puede saltar (comercio: 56,7 % en 2024 →
        # 68,5 % en 2025); se descarta el último dato si se aparta más de 5 puntos del anterior
        for col in W.columns:
            s = W[col].dropna()
            if len(s) > 1 and abs(s.iloc[-1] - s.iloc[-2]) > 5: W.loc[s.index[-1], col] = np.nan
        I = I.join(W.reindex(I.index))
    if mh := ee.get('horas_mundo'):
        A = mh['A']; a = A[(A.variante == 'educación y salud públicas fuera') & (A.china == 'con China')].set_index('anio')
        I['asalariados_productivos_mundo_mill'] = a['obreros_mill'].reindex(I.index)
        I['pct_china_india_masa_mundial'] = (a['pct_china'] + a['pct_india']).reindex(I.index)
        I['semana_horas_productivas_mundo'] = a['semana_horas'].reindex(I.index)
    if (ic := ee.get('intercambio')) is not None:
        X = ic['A'].set_index('anio')
        for col, nom in (('altos_ingresos_mmh', 'transferencia_horas_altos_ingresos_mmh'), ('razon_altos_ingresos', 'razon_intercambio_horas_altos_ingresos'),
                         ('altos_ingresos_pct_horas', 'transferencia_pct_horas_altos_ingresos'), ('USA_mmh', 'transferencia_horas_eeuu_mmh'),
                         ('CHN_mmh', 'transferencia_horas_china_mmh'), ('IND_mmh', 'transferencia_horas_india_mmh')):
            I[nom] = X[col].reindex(I.index)
    I.to_csv(os.path.join(dir_out, 'contratendencias_indicadores.csv'))

    # descomposición de la tasa por fases endógenas
    cortes = fases_endogenas(ee)
    filas = []
    for var, M, ini in (('por ramas', b, Y[0]), ('intra-rama', c, int(c.index[0]))):
        lims = [ini] + [y for y in cortes if y > ini + 2] + [Y[-1]]
        for a0, a1 in zip(lims[:-1], lims[1:]):
            r0, r1 = M['r'].get(a0), M['r'].get(a1)
            de = np.log(M['e'].get(a1) / M['e'].get(a0)); dk = np.log(M['K_V'].get(a1) / M['K_V'].get(a0))
            fila = dict(variante=var, desde=a0, hasta=a1, cambio_tasa_pct=(r1 / r0 - 1) * 100, dln_tasa=np.log(r1 / r0),
                        aporte_explotacion=de, aporte_composicion=-dk, compensacion=(de / dk) if dk > 0 else np.nan)
            if var == 'intra-rama':
                fila['aporte_comp_tecnica'] = -np.log(I['composicion_tecnica_idx'].get(a1) / I['composicion_tecnica_idx'].get(a0))
                fila['aporte_precio_relativo'] = -np.log(I['precio_capital_sobre_salario_idx'].get(a1) / I['precio_capital_sobre_salario_idx'].get(a0))
            filas.append(fila)
    F = pd.DataFrame(filas)
    F.to_csv(os.path.join(dir_out, 'contratendencias_fases.csv'), index=False)
    FM = fases_multiverso(ee, cortes, Y)
    FM.to_csv(os.path.join(dir_out, 'contratendencias_fases_multiverso.csv'), index=False)
    return dict(I=I, F=F, FM=FM, cortes=cortes)


def fases_multiverso(ee, cortes, Y):
    """La misma descomposición para cada especificación empresarial del multiverso (criterio por ramas o intra-rama;
    costo corriente o histórico; neta o bruta; con o sin propiedad intelectual; todo el capital o sólo el productivo;
    sin ajuste por utilización y con denominador K). Resume la distribución de los aportes en cada fase."""
    filas = []
    for fam, pref in (('por ramas', 'B|b|'), ('intra-rama', 'B|c|')):
        specs = {k: v for k, v in ee['SK'].items() if k.startswith(pref)}
        if not specs: continue
        ini = Y[0] if fam == 'por ramas' else int(ee['masa']['c'].index[0])
        lims = [ini] + [y for y in cortes if y > ini + 2] + [Y[-1]]
        for a0, a1 in zip(lims[:-1], lims[1:]):
            de, dk, dr = [], [], []
            for S, K, V in specs.values():
                e0, e1, k0, k1 = S.get(a0) / V.get(a0), S.get(a1) / V.get(a1), K.get(a0) / V.get(a0), K.get(a1) / V.get(a1)
                if min(e0, e1, k0, k1) <= 0 or any(pd.isna([e0, e1, k0, k1])): continue
                de.append(np.log(e1 / e0)); dk.append(np.log(k1 / k0)); dr.append(np.log(e1 / e0) - np.log(k1 / k0))
            de, dk, dr = map(np.array, (de, dk, dr))
            q = lambda x, p: float(np.percentile(x, p))
            filas.append(dict(variante=fam, desde=a0, hasta=a1, especificaciones=len(de),
                              aporte_e_p10=q(de, 10), aporte_e_mediana=q(de, 50), aporte_e_p90=q(de, 90),
                              aporte_kv_p10=q(-dk, 10), aporte_kv_mediana=q(-dk, 50), aporte_kv_p90=q(-dk, 90),
                              dln_tasa_mediana=q(dr, 50), pct_tasa_sube=float((dr > 0).mean() * 100),
                              pct_composicion_sube=float((dk > 0).mean() * 100),
                              pct_e_compensa=float(((dk > 0) & (de >= dk)).sum() / max((dk > 0).sum(), 1) * 100)))
    return pd.DataFrame(filas)
