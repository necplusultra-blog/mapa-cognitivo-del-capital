"""Datos del «mapa cognitivo»: la visualización central del sitio (fondo de página y pestaña Mapa).

Lee resultados/ y site/data/ y escribe site/data/mapa.json. No calcula nada nuevo: reorganiza lo que
el sitio ya publica para que el grafo tenga la topología real del proyecto.

- El árbol de EE.UU. es el multiverso efectivo: cada hoja es una especificación de
  resultados/eeuu_especificaciones.csv y cada bifurcación es una de las decisiones de metodología §5.
  Sólo hay bifurcación donde las opciones divergen bajo ese nodo (una decisión con un solo valor no se dibuja).
- El árbol mundial reproduce las 24 especificaciones de site/data/mundo_especificaciones.json.
- Las ramas secundarias son las series que publica cada sección del sitio.
- El fondo sismográfico usa las bandas del multiverso (p10–p90) y el número de especificaciones con quiebre por año.

Uso: python -m sismografo.mapa   (también lo llama run.py después de sitio.escribir)
"""
import csv
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Nombre de cada decisión y etiqueta de cada opción, tal como las expone metodología §5.
DIM_EEUU = [
    ('D6', 'Sector', {'corp': 'corporativo total', 'nfc': 'corporativo no financiero', 'empresarial': 'sector empresarial'}, ''),
    ('D1', 'Numerador', {'nos': 'excedente neto de explotación', 'pbt': 'ganancia antes de impuestos',
                         'pat': 'ganancia después de impuestos', 'excedente amplio': 'excedente amplio',
                         'plusvalor ampliado': 'plusvalor ampliado'}, 'Duménil-Lévy, Kliman · Shaikh-Tonak, Moseley'),
    ('D2', 'Qué cuenta como plusvalor', {'a': 'todo productivo', 'b': 'plusvalor ampliado por ramas',
                                         'c': 'corrección intra-rama'}, 'Shaikh-Tonak, Moseley'),
    ('D3', 'Valuación del capital', {'cc': 'costo corriente', 'hc': 'costo histórico'}, 'Duménil-Lévy, Roberts · Kliman'),
    ('D4', 'Neta o bruta', {'neta': 'neta de depreciación', 'bruta': 'bruta'}, ''),
    ('D5', 'Propiedad intelectual', {'incl': 'dentro de K', 'excl': 'fuera de K'}, 'debate sobre la transferencia de valor de los PPI'),
    ('inventarios', 'Existencias', {'False': 'sin existencias', 'True': 'con existencias (Z.1)'}, ''),
    ('D8', 'Utilización de capacidad', {'False': 'sin ajuste', 'True': 'r × (u medio / u)'}, ''),
    ('K', 'Alcance de K', {'todo': 'todo el capital no residencial', 'prod': 'sólo ramas productivas'}, 'Moseley, Shaikh-Tonak'),
    ('denominador', 'Denominador', {'K': 'K', 'K+V': 'K + V'}, 'definición de Marx de la tasa de ganancia'),
]
# Traducción de decisiones y opciones para la versión inglesa del mapa (en/map.html).
EN = {
    'Sector': 'Sector', 'corporativo total': 'all corporations', 'corporativo no financiero': 'non-financial corporations', 'sector empresarial': 'business sector',
    'Numerador': 'Numerator', 'excedente neto de explotación': 'net operating surplus', 'ganancia antes de impuestos': 'profit before tax',
    'ganancia después de impuestos': 'profit after tax', 'excedente amplio': 'broad surplus', 'plusvalor ampliado': 'extended surplus value',
    'Qué cuenta como plusvalor': 'What counts as surplus value', 'todo productivo': 'all labour productive', 'plusvalor ampliado por ramas': 'extended surplus value by industry',
    'corrección intra-rama': 'within-industry correction', 'Valuación del capital': 'Valuation of capital', 'costo corriente': 'current cost', 'costo histórico': 'historical cost',
    'Neta o bruta': 'Net or gross', 'neta de depreciación': 'net of depreciation', 'bruta': 'gross', 'Propiedad intelectual': 'Intellectual property',
    'dentro de K': 'inside K', 'fuera de K': 'outside K', 'Existencias': 'Inventories', 'sin existencias': 'without inventories', 'con existencias (Z.1)': 'with inventories (Z.1)',
    'Utilización de capacidad': 'Capacity utilisation', 'sin ajuste': 'no adjustment', 'Alcance de K': 'Scope of K', 'todo el capital no residencial': 'all non-residential capital',
    'sólo ramas productivas': 'productive industries only', 'Denominador': 'Denominator', 'definición de Marx de la tasa de ganancia': "Marx's definition of the rate of profit",
    'debate sobre la transferencia de valor de los PPI': 'debate on the transfer of value by IPP', 'Medida': 'Measure', 'neta': 'net',
    'tasa interna de retorno (PWT)': 'internal rate of return (PWT)', 'Ponderación': 'Weighting', 'por capital': 'by capital', 'por PIB': 'by GDP',
    'China': 'China', 'con China': 'with China', 'sin China': 'without China', 'Panel': 'Panel', 'balanceado desde 1960': 'balanced since 1960', 'no balanceado': 'unbalanced',
}
# Decisiones que no se aplican a una familia de especificaciones: se muestran como «no aplica», no como una opción elegida.
NO_APLICA = {'corporativa': ('D2', 'K', 'denominador')}
NO_APLICA_EMPRESARIAL = ('inventarios',)

DIM_MUNDO = [
    ('medida', 'Medida', {'bruta': 'bruta', 'neta': 'neta', 'irr': 'tasa interna de retorno (PWT)'}, ''),
    ('ponderacion', 'Ponderación', {'K': 'por capital', 'PIB': 'por PIB'}, ''),
    ('china', 'China', {'con': 'con China', 'sin': 'sin China'}, ''),
    ('panel', 'Panel', {'balanceado-1960': 'balanceado desde 1960', 'no balanceado': 'no balanceado'}, ''),
]


def _json(nombre):
    with open(os.path.join(RAIZ, 'site', 'data', nombre), encoding='utf-8') as f:
        return json.load(f)


def _anios(texto):
    try:
        return [int(x) for x in json.loads(texto)]
    except (TypeError, ValueError):
        return []


def _columnas(filas, fuera=('anio', 'trimestre', 'provisional')):
    """Series de una tabla publicada. Las variantes de una misma medida (columna «medida__variante__…») cuentan una vez."""
    if isinstance(filas, list) and filas and isinstance(filas[0], dict):
        vistas = []
        for k in filas[0]:
            if k in fuera:
                continue
            base = k.split('__')[0]
            if base not in vistas:
                vistas.append(base)
        return vistas
    return []


def _indices(s, dims):
    """Índice de la opción elegida en cada decisión; −1 si la decisión no se aplica a la familia de la especificación."""
    fuera = NO_APLICA.get(s.get('familia'), ()) if s.get('familia') else ()
    if str(s.get('familia', '')).startswith('empresarial'):
        fuera = NO_APLICA_EMPRESARIAL
    return [(-1 if d[0] in fuera else (list(d[2]).index(s[d[0]]) if s[d[0]] in d[2] else -1)) for d in dims]


def _arbol(specs, dims):
    """Árbol de decisiones comprimido: un nodo se divide en la primera decisión que separa a sus especificaciones."""
    def nodo(grupo, desde):
        for j in range(desde, len(dims)):
            clave = dims[j][0]
            valores = []
            for s in grupo:
                if s[clave] not in valores:
                    valores.append(s[clave])
            if len(valores) > 1:
                ops = list(dims[j][2])
                return {'d': j, 'h': [dict(o=ops.index(v) if v in ops else -1, **nodo([s for s in grupo if s[clave] == v], j + 1)) for v in valores]}
        return {'s': [s['i'] for s in grupo]}
    return nodo(specs, 0)


def _conteo_quiebres(eeuu, anios):
    c = {}
    for s in eeuu:
        for y in _anios(s['quiebres']):
            c[y] = c.get(y, 0) + 1
    return [[a, c.get(a, 0)] for a in anios]


FAM_EN = {'masa y tasa de plusvalor': 'mass and rate of surplus value', 'seis lecturas del debate': 'six readings in the debate',
          'series de los autores, rehechas': "the authors' series, reconstructed", 'estimación trimestral': 'quarterly estimate',
          'fuerzas productivas': 'productive forces', 'EE.UU. en horas de trabajo': 'the United States in hours of labour',
          'masa mundial en horas': 'world mass in hours', 'contratendencias': 'countertendencies', 'valores y precios': 'values and prices',
          'corporaciones de la IA': 'AI corporations', 'masa mundial': 'world mass'}


def construir(destino=None):
    destino = destino or os.path.join(RAIZ, 'site', 'data', 'mapa.json')
    with open(os.path.join(RAIZ, 'resultados', 'eeuu_especificaciones.csv'), encoding='utf-8') as f:
        filas = list(csv.DictReader(f))
    eeuu = [dict(r, i=i) for i, r in enumerate(filas)]
    mundo = [dict(r, i=i, quiebres=r['quiebres']) for i, r in enumerate(_json('mundo_especificaciones.json'))]
    meta = _json('meta.json')
    fz = _json('fuerzas.json')
    ct = _json('contratendencias.json')
    tr = _json('transformacion.json')
    familias = [  # estación del eje · ancla del sitio · etiqueta · series publicadas
        (1, 'index.html#masa-tasa', 'masa y tasa de plusvalor', _columnas(_json('eeuu_masa.json'))),
        (1, 'index.html#referencias', 'seis lecturas del debate', _columnas(_json('eeuu_referencias.json'))),
        (1, 'index.html#replicacion', 'series de los autores, rehechas', _columnas(_json('replicacion.json').get('serie'))),
        (1, 'index.html#trimestral', 'estimación trimestral', _columnas(_json('eeuu_trimestral.json'))),
        (2, 'index.html#fuerzas', 'fuerzas productivas', _columnas(fz.get('eeuu')) + _columnas(fz.get('mundo'))),
        (3, 'index.html#tiempo', 'EE.UU. en horas de trabajo', _columnas(_json('eeuu_tiempo.json'))),
        (3, 'index.html#horas-mundo', 'masa mundial en horas', _columnas(_json('mundo_horas.json'))),
        (4, 'index.html#contratendencias', 'contratendencias', _columnas(ct.get('indicadores'))),
        (4, 'index.html#transformacion', 'valores y precios', _columnas(tr.get('serie')) + _columnas(tr.get('comercio'))),
        (4, 'index.html#ia', 'corporaciones de la IA', _columnas(_json('ia_empresas.json')) + _columnas(_json('ia_agregado.json'))),
        (4, 'index.html#mundo', 'masa mundial', _columnas(_json('mundo_masa.json'))),
    ]
    salida = {
        'meta': {k: meta.get(k) for k in ('actualizado', 'commit', 'eeuu_fin', 'eeuu_n', 'eeuu_n_intra', 'mundo_fin', 'mundo_n', 'mundo_nbal', 'empalmes')},
        'eeuu': {
            'dims': [[d[1], d[3], list(d[2].values())] for d in DIM_EEUU],
            'dims_en': [[EN.get(d[1], d[1]), ' · '.join(EN.get(x.strip(), x.strip()) for x in d[3].split('·')) if d[3] else '', [EN.get(v, v) for v in d[2].values()]] for d in DIM_EEUU],
            'claves': [d[0] for d in DIM_EEUU],
            'specs': [[s['id'], s['familia'], _anios(s['quiebres']), _indices(s, DIM_EEUU)] for s in eeuu],
            'arbol': _arbol(eeuu, DIM_EEUU),
        },
        'mundo': {
            'dims': [[d[1], d[3], list(d[2].values())] for d in DIM_MUNDO],
            'dims_en': [[EN.get(d[1], d[1]), d[3], [EN.get(v, v) for v in d[2].values()]] for d in DIM_MUNDO],
            'claves': [d[0] for d in DIM_MUNDO],
            'specs': [[s['id'], int(s.get('n_paises') or 0), _anios(s['quiebres']), [list(d[2]).index(s[d[0]]) if s[d[0]] in d[2] else -1 for d in DIM_MUNDO]] for s in mundo],
            'arbol': _arbol(mundo, DIM_MUNDO),
        },
        'bandas': [[b['anio'], b['p10'], b['p25'], b['p50'], b['p75'], b['p90']] for b in _json('eeuu_bandas.json')],
        # quiebres por año contados sobre las mismas 288 + 64 especificaciones del árbol (no sólo las 288 principales)
        'quiebres': _conteo_quiebres(eeuu, [b['anio'] for b in _json('eeuu_bandas.json')]),
        'familias': [{'e': e, 'a': a, 'n': n, 'n_en': FAM_EN.get(n, n), 's': s} for e, a, n, s in familias if s],
    }
    with open(destino, 'w', encoding='utf-8') as f:
        json.dump(salida, f, ensure_ascii=False, separators=(',', ':'))
    return salida


if __name__ == '__main__':
    d = construir()
    print('mapa.json:', len(d['eeuu']['specs']), 'especificaciones EE.UU.,', len(d['mundo']['specs']), 'mundiales,',
          sum(len(f['s']) for f in d['familias']), 'series en', len(d['familias']), 'familias')
