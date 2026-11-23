"""Las corporaciones de la inteligencia artificial: tasa de ganancia, peso en la tasa agregada y en la masa global.

Fuente: estados financieros de la SEC (XBRL, «company facts»), sin claves. Grupo: Microsoft, Alphabet,
Amazon, Meta, Nvidia, Oracle, Broadcom y AMD (OpenAI y Anthropic no publican estados auditados).

Advertencias de método:
- Son ganancias contables consolidadas mundialmente (incluyen filiales fuera de EE.UU.); el agregado
  corporativo de NIPA es doméstico. La comparación es por eso aproximada.
- El capital es contable, a costo histórico, y los PCGA no capitalizan la I+D propia. Por eso se compara
  con la especificación NIPA no financiera a costo histórico y sin productos de propiedad intelectual.
- La ganancia apropiada no es plusvalor producido. La participación en la masa mundial de ganancia mide
  apropiación (incluidas rentas y transferencias, rama (iii) de D5), no formación de plusvalor.
"""
import json, os, time, urllib.request
import numpy as np, pandas as pd

# La SEC pide identificar las descargas. El contacto se define en la variable de entorno SEC_USER_AGENT
# (en GitHub: Settings › Secrets and variables › Actions › Variables); si falta, se usa un nombre genérico.
UA = os.environ.get('SEC_USER_AGENT') or 'Sismografo del capital research project'
CACHE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datos_cache', 'ia_empresas.csv')
EMPRESAS = {  # nombre: CIK actual y predecesores (Google Inc. antes de Alphabet; Avago antes de Broadcom Inc.)
    'Microsoft': [789019], 'Alphabet': [1652044, 1288776], 'Amazon': [1018724], 'Meta': [1326801],
    'Nvidia': [1045810], 'Oracle': [1341439], 'Broadcom': [1730168, 1441634], 'AMD': [2488],
}
CONCEPTOS = {
    'ganancia_operativa': ['OperatingIncomeLoss'],
    'ganancia_antes_imp': ['IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest',
                           'IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments'],
    'ganancia_neta': ['NetIncomeLoss'],
    'ingresos': ['Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax', 'SalesRevenueNet'],
    'activos': ['Assets'],
    'capital_fijo': ['PropertyPlantAndEquipmentNet',
                     'PropertyPlantAndEquipmentAndFinanceLeaseRightOfUseAssetAfterAccumulatedDepreciationAndAmortization'],
    'existencias': ['InventoryNet'],
    'inversion': ['PaymentsToAcquirePropertyPlantAndEquipment', 'PaymentsToAcquireProductiveAssets'],
    'id': ['ResearchAndDevelopmentExpense', 'ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost'],
}
INSTANTANEOS = {'activos', 'capital_fijo', 'existencias'}


def descargar(dir_datos):
    d = os.path.join(dir_datos, 'sec'); os.makedirs(d, exist_ok=True)
    for ciks in EMPRESAS.values():
        for cik in ciks:
            dest = os.path.join(d, f'CIK{cik:010d}.json')
            for k in range(3):
                try:
                    req = urllib.request.Request(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json', headers={'User-Agent': UA})
                    with urllib.request.urlopen(req, timeout=90) as r: open(dest, 'wb').write(r.read())
                    break
                except Exception as e:  # noqa: BLE001
                    print(f'  SEC {cik} intento {k + 1}: {e}'); time.sleep(2)
            time.sleep(0.3)   # la SEC pide no más de 10 solicitudes por segundo


def _serie(facts, conceptos, instantaneo):
    out = {}
    for c in conceptos:   # se usa el primer concepto disponible para cada año
        for e in facts.get('facts', {}).get('us-gaap', {}).get(c, {}).get('units', {}).get('USD', []):
            f = e.get('frame', '')
            if instantaneo and f.endswith('Q4I'): y = int(f[2:6])
            elif not instantaneo and len(f) == 6 and f.startswith('CY'): y = int(f[2:])
            else: continue
            out.setdefault(y, e['val'] / 1e6)
    # segunda pasada: informes anuales (10-K) sin «frame» de la SEC; el año es el calendario que más cubre
    for c in conceptos:
        for e in facts.get('facts', {}).get('us-gaap', {}).get(c, {}).get('units', {}).get('USD', []):
            if e.get('form') != '10-K' or e.get('fp') != 'FY': continue
            end = pd.Timestamp(e['end'])
            if instantaneo:
                y = (end - pd.DateOffset(months=6)).year
            else:
                if 'start' not in e or not 330 <= (end - pd.Timestamp(e['start'])).days <= 400: continue
                y = (end - pd.DateOffset(months=6)).year
            out.setdefault(y, e['val'] / 1e6)
    return out


def _empresas(dir_datos):
    filas = []
    for nombre, ciks in EMPRESAS.items():
        datos = {}
        for cik in ciks:   # el CIK actual tiene prioridad; los predecesores completan años anteriores
            fn = os.path.join(dir_datos, 'sec', f'CIK{cik:010d}.json')
            if not os.path.exists(fn): continue
            facts = json.load(open(fn))
            for var, conc in CONCEPTOS.items():
                for y, v in _serie(facts, conc, var in INSTANTANEOS).items():
                    datos.setdefault((y, var), v)
        anios = sorted({y for y, _ in datos})
        for y in anios:
            filas.append(dict(anio=y, empresa=nombre, **{v: datos.get((y, v)) for v in CONCEPTOS}))
    return pd.DataFrame(filas)


def _mundo_usd(dir_datos, fin):
    """Masa mundial de ganancia bruta en USD corrientes: Σ (1 − participación salarial PWT) × PIB (Banco Mundial)."""
    url = f'https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json&per_page=20000&date=2000:{fin}'
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=120) as r: wb = json.loads(r.read())[1]
    gdp = pd.DataFrame([(x['countryiso3code'], int(x['date']), x['value']) for x in wb if x['value'] and x['countryiso3code']],
                       columns=['iso3', 'anio', 'pib']).pivot(index='anio', columns='iso3', values='pib')
    pwt = pd.read_stata(os.path.join(dir_datos, 'pwt', 'pwt110.dta'))
    lab = pwt.pivot_table(index='year', columns='countrycode', values='labsh').reindex(range(2000, fin + 1)).ffill()  # años sin PWT: última participación
    cols = sorted(set(gdp.columns) & set(lab.columns))
    masa = ((1 - lab[cols]) * gdp.reindex(lab.index)[cols]).sum(axis=1, min_count=50) / 1e6   # millones de USD
    return masa, int(pwt.year.max())


def calcular(dir_datos, dir_out, F, N):
    E = _empresas(dir_datos)
    if E.empty or E['empresa'].nunique() < len(EMPRESAS):
        if not os.path.exists(CACHE): raise RuntimeError('sin datos de la SEC ni copia en caché')
        print('IA: la SEC no respondió; se usa la copia guardada en datos_cache/'); E = pd.read_csv(CACHE)
    else:
        os.makedirs(os.path.dirname(CACHE), exist_ok=True); E.to_csv(CACHE, index=False)
    E.to_csv(os.path.join(dir_out, 'ia_empresas.csv'), index=False)
    # huecos de un año en los saldos (p. ej. Broadcom en la fusión de 2016): interpolación lineal dentro de cada empresa
    E = E.sort_values(['empresa', 'anio'])
    for v in INSTANTANEOS:
        E[v] = E.groupby('empresa')[v].transform(lambda x: x.interpolate(limit=1, limit_area='inside'))
    E['ganancia_antes_imp'] = E['ganancia_antes_imp'].fillna(E['ganancia_operativa'])   # si falta, la operativa
    completos = E.dropna(subset=['ganancia_operativa', 'capital_fijo', 'activos'])
    n = completos.groupby('anio').empresa.nunique()
    anios = [int(y) for y in n.index if n[y] == len(EMPRESAS) and y >= 2010]
    G = completos[completos.anio.isin(anios)].groupby('anio')[list(CONCEPTOS)].sum(min_count=1)
    Y = list(G.index)
    s = lambda src, c: pd.Series(src[c]).reindex(Y).astype(float)
    # NIPA no financiero a costo histórico, sin PPI (comparable con la contabilidad PCGA)
    p_nfc = s(N, 'W326RC') + s(F, 'm1pnofi2es00') - s(F, 'm3pnofi2es00') - s(F, 'i3nnofi2ip00') + s(F, 'm3nnofi2ip00')
    k_nfc = s(F, 'k3pnofi2es00') - s(F, 'k3nnofi2ip00')
    A = pd.DataFrame({
        'tasa_ia_sobre_capital_fijo': G['ganancia_operativa'] / G['capital_fijo'] * 100,
        'tasa_ia_sobre_activos': G['ganancia_operativa'] / G['activos'] * 100,
        'tasa_nfc_hc_sin_ppi': p_nfc / k_nfc * 100,
        'tasa_nfc_sin_ia': (p_nfc - G['ganancia_operativa']) / (k_nfc - G['capital_fijo']) * 100,
        'pct_ganancia_ia_en_nfc': G['ganancia_operativa'] / p_nfc * 100,
        'pct_ganancia_ia_en_corporativas': G['ganancia_antes_imp'] / s(N, 'A445RC') * 100,
        'pct_inversion_ia_en_inversion_privada': G['inversion'] / s(F, 'i3ntotl1es00') * 100,
        'inversion_ia_sobre_capital_fijo_ia': G['inversion'] / G['capital_fijo'] * 100,
        'ganancia_operativa_ia_mmd': G['ganancia_operativa'] / 1000, 'inversion_ia_mmd': G['inversion'] / 1000,
    })
    try:
        masa, pwt_fin = _mundo_usd(dir_datos, max(Y))
        A['pct_ganancia_ia_en_masa_mundial'] = G['ganancia_antes_imp'] / masa.reindex(Y) * 100
        A['masa_mundial_estimada'] = [y > pwt_fin for y in Y]
    except Exception as e:  # noqa: BLE001
        print('IA: no se pudo estimar la masa mundial en USD:', e)
    A.index.name = 'anio'
    A = A.round(3)
    A.to_csv(os.path.join(dir_out, 'ia_agregado.csv'))
    return dict(A=A, E=E, empresas=list(EMPRESAS))
