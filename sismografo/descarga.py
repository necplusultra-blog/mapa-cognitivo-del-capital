"""Descarga de las fuentes públicas. Todo es reproducible y no requiere claves.

BEA (cuentas nacionales, activos fijos, PIB por industria), FRED (Z.1, G.17, BLS CES)
y Penn World Table 11.0 (dataverse.nl; si falla, las series de la PWT replicadas en FRED).
"""
import os, shutil, socket, time, urllib.request

# Algunos servidores (dataverse → objectstore) anuncian IPv6, que los runners de GitHub no siempre alcanzan:
# se fuerza IPv4.
_orig_gai = socket.getaddrinfo
socket.getaddrinfo = lambda host, port, family=0, *a, **k: _orig_gai(host, port, socket.AF_INET, *a, **k)
CACHE_PWT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datos_cache', 'pwt110.dta')

BEA = 'https://apps.bea.gov'
BEA_FILES = {
    'NipaDataA.txt': f'{BEA}/national/Release/TXT/NipaDataA.txt',
    'NipaDataQ.txt': f'{BEA}/national/Release/TXT/NipaDataQ.txt',
    'SeriesRegister.txt': f'{BEA}/national/Release/TXT/SeriesRegister.txt',
    'FixedAssets.txt': f'{BEA}/national/FixedAssets/Release/TXT/FixedAssets.txt',
    'FaSeriesRegister.txt': f'{BEA}/national/FixedAssets/Release/TXT/SeriesRegister.txt',
    'ValueAdded.xlsx': f'{BEA}/industry/Release/XLS/GDPxInd/ValueAdded.xlsx',
    'GDPbyInd_VA_SIC.xls': f'{BEA}/industry/xls/GDPbyInd_VA_SIC.xls',
    'GDPbyInd_VA_NAICS_1947-1997.xls': f'{BEA}/industry/xls/GDPbyInd_VA_NAICS_1947-1997.xls',
}
FRED_SERIES = ['BOGZ1FL105020005A', 'CUMFNS', 'AWHMAN',
               # contratendencias (véase contratendencias.py)
               'OPHNFB', 'COMPRNFB', 'AHETPI', 'CPIAUCSL', 'TDSP', 'U6RATE', 'LNS12300060', 'BOGZ1FU103164103A',
               'LNS12026619', 'LNS12032194', 'CE16OV', 'NCBEILQ027S', 'BCNSDODNS', 'GDP',
               # depuración de supersectores (eeuu.fraccion_capitalista): jurídicos, contables, salud, educación, asistencia, org. religiosas y civiles
               'CES6054110001', 'CES6054120001', 'USPBS', 'CES6561000001', 'CES6562000001', 'CES6562400001', 'USEHS', 'CES8081300001', 'USSERV']
CES_SUPERSECTORES = {  # código CES: (nombre, productivo según el criterio de la metodología)
    '10000000': ('Minería y explotación forestal', True), '20000000': ('Construcción', True),
    '30000000': ('Manufactura', True), '41420000': ('Comercio mayorista', False),
    '42000000': ('Comercio minorista', False), '43000000': ('Transporte y almacenamiento', True),
    '44220000': ('Electricidad, gas y agua', True), '50000000': ('Información', True),
    '55000000': ('Actividades financieras', False), '60000000': ('Servicios profesionales y empresariales', True),
    '65000000': ('Educación y salud privadas', True), '70000000': ('Ocio y hospitalidad', True),
    '80000000': ('Otros servicios', True),
}
PWT_DTA = 'https://dataverse.nl/api/access/datafile/554030'  # pwt110.dta
WIOD_SEA = 'https://dataverse.nl/api/access/datafile/199095'  # WIOD 2016, Socio_Economic_Accounts.xlsx (2000–2014)
PWT_FRED_VARS = {'LABSHP': 'A156NRUG', 'RKNANP': 'A666NRUG', 'RGDPNA': 'A666NRUG', 'CKSPPP': 'A666NRUG', 'RGDPES': 'A666NRUG'}


UA = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36 '
      'sismografo-del-capital (+https://github.com/necplusultra-blog/sismografo-del-capital)')


def _get(url, dest, tries=3):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
            with urllib.request.urlopen(req, timeout=90) as r, open(dest + '.part', 'wb') as f:
                f.write(r.read())
            with open(dest + '.part', 'rb') as f:
                head = f.read(200).lower()
            if b'<!doctype html' in head or b'<html' in head:
                raise IOError(f'respuesta HTML en lugar de datos: {url}')
            os.replace(dest + '.part', dest)
            return True
        except Exception as e:  # noqa: BLE001
            print(f'  intento {k + 1} falló: {url} ({e})')
            time.sleep(3)
    return False


def fred_csv(series, dest_dir):
    return _get(f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}', os.path.join(dest_dir, series + '.csv'))


def _con_cache(url, dest, nombre):
    cache = os.path.join(os.path.dirname(CACHE_PWT), nombre)
    if _get(url, dest):
        os.makedirs(os.path.dirname(cache), exist_ok=True); shutil.copy(dest, cache); return True
    if os.path.exists(cache):
        print(f'{nombre}: la fuente no respondió; se usa la copia guardada'); shutil.copy(cache, dest); return True
    return False


PAISES_OCDE = ['AUS', 'AUT', 'BEL', 'BGR', 'CAN', 'CHE', 'CYP', 'CZE', 'DEU', 'DNK', 'ESP', 'EST', 'FIN', 'FRA', 'GBR', 'GRC',
               'HRV', 'HUN', 'IRL', 'ITA', 'JPN', 'KOR', 'LTU', 'LUX', 'LVA', 'MEX', 'MLT', 'NLD', 'NOR', 'POL', 'PRT', 'ROU',
               'SVK', 'SVN', 'SWE', 'TUR', 'USA']
ACT_OCDE = list('ABCDEFGHIJKLMNOPQRSTU') + ['M69_70', 'M69', 'M70', 'M73', '_T']
OCDE = 'https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN10@{df},/{key}?startPeriod=2014&format=csvfile'


def descargar_ocde(dir_datos):
    """Cuentas nacionales por rama de la OCDE: tabla 6 (valor agregado, remuneración, consumo de capital fijo)
    y tabla 7 (asalariados y no asalariados, personas y horas), desde 2014."""
    d = os.path.join(dir_datos, 'ocde'); os.makedirs(d, exist_ok=True)
    areas, acts = '+'.join(PAISES_OCDE), '+'.join(ACT_OCDE)
    for nombre, df, key in (('t6', 'DF_TABLE6', f'A.{areas}.S1.S1.B1G+D1+P51C._Z.{acts}._Z.XDC.V.N.'),
                            ('t7', 'DF_TABLE7', f'A.{areas}.S1.S1.SAL+SELF+EMP._Z.{acts}._Z.PS+H._Z.N.')):
        _con_cache(OCDE.format(df=df, key=key), os.path.join(d, f'ocde_{nombre}.csv'), f'ocde_{nombre}.csv')
    # empleo por sector institucional (gobierno general S13, instituciones sin fines de lucro S15): parte pública de P y Q
    _con_cache(OCDE.format(df='DF_TABLE3_EMP_SECTOR', key=f'A.{areas}.S1+S13+S15._Z.EMP._Z._Z._Z.PS._Z.N.'),
               os.path.join(d, 'ocde_sectores.csv'), 'ocde_sectores.csv')


def descargar_todo(dir_datos, mundo=True):
    os.makedirs(dir_datos, exist_ok=True)
    bea = os.path.join(dir_datos, 'bea'); os.makedirs(bea, exist_ok=True)
    for name, url in BEA_FILES.items():
        print('BEA', name); assert _get(url, os.path.join(bea, name)), name
    fred = os.path.join(dir_datos, 'fred'); os.makedirs(fred, exist_ok=True)
    ids = list(FRED_SERIES) + [f'CES{c}{t}' for c in CES_SUPERSECTORES for t in ('06', '07', '08')]
    for s in ids:
        fred_csv(s, fred)
    if mundo:
        descargar_ocde(dir_datos)
        w = os.path.join(dir_datos, 'wiod'); os.makedirs(w, exist_ok=True)
        _con_cache(WIOD_SEA, os.path.join(w, 'Socio_Economic_Accounts.xlsx'), 'wiod_sea.xlsx')
        pwt = os.path.join(dir_datos, 'pwt'); os.makedirs(pwt, exist_ok=True)
        dest = os.path.join(pwt, 'pwt110.dta')
        if _get(PWT_DTA, dest):
            os.makedirs(os.path.dirname(CACHE_PWT), exist_ok=True); shutil.copy(dest, CACHE_PWT)
        elif os.path.exists(CACHE_PWT):
            print('PWT: dataverse no respondió; se usa la copia guardada en datos_cache/')
            shutil.copy(CACHE_PWT, dest)
        else:
            print('PWT completa no disponible: se usa la réplica parcial en FRED')
            import pycountry
            from concurrent.futures import ThreadPoolExecutor
            ids = [f'{v}{c.alpha_2}{u}' for c in pycountry.countries for v, u in PWT_FRED_VARS.items()]
            with ThreadPoolExecutor(8) as ex:
                list(ex.map(lambda s: _get(f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={s}', os.path.join(pwt, s + '.csv'), tries=1), ids))
