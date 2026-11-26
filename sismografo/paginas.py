"""Construye las páginas del sitio a partir de los textos editables de contenido/.

Cada página es una carpeta de contenido/ con un archivo Markdown por sección. El orden de las secciones es el
orden alfabético de los archivos (por eso empiezan con un número). Las instrucciones de edición están en
contenido/LEEME.md. Este módulo sólo traduce los atajos de ese formato a HTML y los inserta en plantillas/.

Atajos disponibles en los textos:
  {{id}}                     cifra que el sitio llena con los datos (p. ej. {{hm-n}})
  {{.clase}}                 lo mismo, cuando la cifra aparece varias veces (p. ej. {{.hm-fin}})
  [[grafico id]]             un gráfico; [[grafico id corto]] para uno más bajo
  [[leyenda id]]             la leyenda de un gráfico
  [[tabla id: Col 1 | Col 2]] una tabla que el sitio llena con los datos
  [[explorador]]             el explorador de especificaciones del multiverso (explorador.js)
  [[glosario simbolos]]      la tabla de símbolos del glosario (glosario.js, con los datos de site/data/mapa.json)
  [[glosario series]]        el glosario de las series publicadas, por sección, con buscador (glosario.js)
  [[glosario decisiones]]    las decisiones (bifurcaciones) de los multiversos de EE.UU. y mundial, con sus opciones
  [[cifra id | etiqueta | nota]] una cifra destacada; varias seguidas forman una fila
  :::como Título             abre un desplegable de explicación (se cierra con una línea ::: )
  :::como+ Título            lo mismo, pero abierto por defecto
  :::lectura claves | Título una tarjeta de lectura teórica; al pasar sobre ella se destacan en el gráfico las series
                             indicadas (claves separadas por comas; vacío = todas). Se cierra con una línea :::
Encabezado opcional de cada archivo (entre líneas ---): id (ancla), menu (texto del índice lateral),
oculta: si (la sección aparece sólo cuando hay datos), lugar: portada | pie.

La pestaña Mapa no tiene secciones: todos sus textos (cabecera, panel, fichas, símbolos, recorrido guiado, rótulos de
la lámina) viven en contenido/mapa.yml y contenido/en/mapa.yml. Este módulo construye mapa.html (en/map.html) desde
plantillas/mapa.html y escribe site/mapa-textos.js (site/en/mapa-textos.js), que leen mapa-cognitivo.js y
mapa-pagina.js; lo que falte en el YAML se toma de los textos por defecto del código.
"""
import glob, html, os, re

import markdown, yaml

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXT = ['extra', 'attr_list', 'md_in_html', 'sane_lists', 'toc']


def _front(texto):
    """Encabezado YAML entre líneas --- (lo escribe también Pages CMS). Valores vacíos o nulos se ignoran."""
    meta = {}
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', texto, re.S)
    if m:
        datos = yaml.safe_load(m.group(1)) or {}
        meta = {k: (str(v).lower() if isinstance(v, bool) else str(v)) for k, v in datos.items() if v not in (None, '')}
        texto = texto[m.end():]
    return meta, texto


def _inline(s):
    s = re.sub(r'\{\{\.([\w-]+)\}\}', r'<span class="\1">—</span>', s)
    return re.sub(r'\{\{([\w-]+)\}\}', r'<span id="\1">—</span>', s)


def _bloques(texto):
    out, cifras, pila = [], [], []

    def volcar():
        if cifras:
            out.append('<div class="cifras">' + ''.join(cifras) + '</div>\n'); cifras.clear()
    for linea in texto.splitlines():
        t = linea.strip()
        m = re.match(r'^\[\[cifra ([\w-]+)\s*\|\s*(.*?)\s*(?:\|\s*(.*?))?\s*\]\]$', t)
        if m:
            i, et, nota = m.groups()
            cifras.append(f'<div class="cifra"><div class="valor" id="{i}">—</div><div class="etiqueta">{et}</div>'
                          + (f'<div class="nota">{nota}</div>' if nota else '') + '</div>')
            continue
        volcar()
        m = re.match(r'^\[\[grafico ([\w-]+)( corto)?\]\]$', t)
        if m:
            out.append(f'<figure class="placa"><div class="chart{" short" if m.group(2) else ""}" id="{m.group(1)}"></div></figure>'); continue
        m = re.match(r'^\[\[glosario (simbolos|símbolos|series|decisiones)\]\]$', t)
        if m:
            cual = m.group(1).replace('í', 'i')
            out.append(f'<div class="glosario" id="glosario-{cual}" data-glosario="{cual}"></div>'); continue
        if t == '[[explorador]]':
            out.append('<figure class="placa"><div class="explorador" id="explorador-especificaciones"></div></figure>'); continue
        m = re.match(r'^\[\[leyenda ([\w-]+)\]\]$', t)
        if m:
            out.append(f'<div class="legend" id="{m.group(1)}"></div>'); continue
        m = re.match(r'^\[\[tabla ([\w-]+):\s*(.*?)\]\]$', t)
        if m:
            i, cols = m.groups()
            if cols.strip() == '*':
                out.append(f'<div class="tablewrap"><table><thead id="{i}-h"></thead><tbody id="{i}"></tbody></table></div>')
            else:
                th = ''.join(f'<th>{c.strip()}</th>' for c in cols.split('|'))
                out.append(f'<div class="tablewrap"><table><thead><tr>{th}</tr></thead><tbody id="{i}"></tbody></table></div>')
            continue
        m = re.match(r'^:::como(\+)?\s+(.*)$', t)
        if m:
            pila.append('</details>')
            out.append(f'\n<details class="como"{" open" if m.group(1) else ""} markdown="1">\n<summary>{m.group(2)}</summary>\n'); continue
        m = re.match(r'^:::lectura\s+([\w,\s-]*?)\s*\|\s*(.*)$', t)
        if m:
            claves = ','.join(k.strip() for k in m.group(1).split(',') if k.strip())
            pila.append('</article>')
            out.append(f'\n<article class="lectura" data-series="{claves}" tabindex="0" markdown="1">\n<h3>{html.escape(m.group(2))}</h3>\n'); continue
        if t == ':::':
            out.append('\n' + (pila.pop() if pila else '</details>') + '\n'); continue
        out.append(linea)
    volcar()
    return _inline('\n'.join(out))


def _md(texto):
    return markdown.markdown(_bloques(texto), extensions=EXT, output_format='html5')


def _version():
    """Marca de versión para app.js y style.css: evita que el navegador use copias viejas después de una actualización."""
    import subprocess, time
    try:
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=RAIZ, text=True).strip() + time.strftime('%y%m%d%H%M')
    except Exception:  # noqa: BLE001
        return time.strftime('%y%m%d%H%M')


# Idiomas: los textos en inglés viven en contenido/en/<página>/ y sus plantillas en plantillas/en/; se publican en site/en/
# con nombres de archivo en inglés. Los enlaces internos de los textos traducidos pueden escribirse con los nombres en
# español: se reescriben al construir.
NOMBRES = {'es': {'inicio': 'index.html', 'lectura': 'lectura.html', 'metodologia': 'metodologia.html', 'glosario': 'glosario.html', 'mapa': 'mapa.html'},
           'en': {'inicio': 'index.html', 'lectura': 'reading.html', 'metodologia': 'methodology.html', 'glosario': 'glossary.html', 'mapa': 'map.html'}}


def _enlaces_en(h):
    h = re.sub(r'href="(\./)?lectura\.html', 'href="reading.html', h)
    h = re.sub(r'href="(\./)?metodologia\.html', 'href="methodology.html', h)
    h = re.sub(r'href="(\./)?glosario\.html', 'href="glossary.html', h)
    h = re.sub(r'href="(\./)?mapa\.html', 'href="map.html', h)
    h = re.sub(r'href="(\./)?descargas/', 'href="../descargas/', h)
    return h


def construir(dir_site=None):
    dir_site = dir_site or os.path.join(RAIZ, 'site')
    version = _version()
    for lang in ('es', 'en'):
        base_c = os.path.join(RAIZ, 'contenido') if lang == 'es' else os.path.join(RAIZ, 'contenido', 'en')
        base_p = os.path.join(RAIZ, 'plantillas') if lang == 'es' else os.path.join(RAIZ, 'plantillas', 'en')
        destino = dir_site if lang == 'es' else os.path.join(dir_site, 'en')
        for pagina in ('inicio', 'lectura', 'metodologia', 'glosario'):
            archivos = sorted(glob.glob(os.path.join(base_c, pagina, '*.md')))
            fn_p = os.path.join(base_p, f'{pagina}.html')
            if not archivos or not os.path.exists(fn_p): continue
            partes, menu, lugares = [], [], {'portada': [], 'pie': []}
            for fn in archivos:
                meta, texto = _front(open(fn, encoding='utf-8').read())
                cuerpo = _md(texto)
                sid = meta.get('id') or re.sub(r'^\d+-', '', os.path.splitext(os.path.basename(fn))[0])
                oculta = ' hidden' if meta.get('oculta', '').lower() in ('si', 'sí', 'true', 'yes') else ''
                clase = meta.get('clase', 'seccion')
                if meta.get('lugar') in lugares:
                    lugares[meta['lugar']].append(cuerpo); continue
                partes.append(f'<section id="{sid}" class="{clase}"{oculta}>\n{cuerpo}\n</section>')
                if meta.get('menu'):
                    menu.append(f'<li><a href="#{sid}">{html.escape(meta["menu"])}</a></li>')
            plantilla = open(fn_p, encoding='utf-8').read()
            salida = (plantilla.replace('{{contenido}}', '\n'.join(partes)).replace('{{menu}}', '\n'.join(menu))
                      .replace('{{portada}}', '\n'.join(lugares['portada'])).replace('{{pie}}', '\n'.join(lugares['pie']))
                      .replace('{{version}}', version))
            if lang == 'en': salida = _enlaces_en(salida)
            os.makedirs(destino, exist_ok=True)
            open(os.path.join(destino, NOMBRES[lang][pagina]), 'w', encoding='utf-8').write(salida)
        _mapa(lang, base_c, base_p, destino, version)


# ---------------------------------------------------------------- pestaña Mapa
MD_MAPA = {'parrafo', 'texto'}   # campos de mapa.yml que admiten Markdown (se convierten a HTML)


def _md_linea(t):
    """Markdown de una línea o un párrafo, sin el <p> que lo envuelve."""
    h = markdown.markdown(str(t), extensions=['extra'], output_format='html5').strip()
    return re.sub(r'^<p>(.*)</p>$', r'\1', h, flags=re.S)


def _convertir(x, clave=''):
    if isinstance(x, dict): return {k: _convertir(v, k) for k, v in x.items()}
    if isinstance(x, list): return [_convertir(v, clave) for v in x]
    if x is None: return ''
    return _md_linea(x) if clave in MD_MAPA else str(x)


def textos_mapa(lang='es'):
    fn = os.path.join(RAIZ, 'contenido', 'mapa.yml') if lang == 'es' else os.path.join(RAIZ, 'contenido', 'en', 'mapa.yml')
    if not os.path.exists(fn): return {}
    return yaml.safe_load(open(fn, encoding='utf-8')) or {}


def _mapa(lang, base_c, base_p, destino, version):
    """site/mapa-textos.js y mapa.html (en/map.html) a partir de contenido/mapa.yml y plantillas/mapa.html."""
    import json
    crudo = textos_mapa(lang)
    tx = _convertir(crudo)
    os.makedirs(destino, exist_ok=True)
    with open(os.path.join(destino, 'mapa-textos.js'), 'w', encoding='utf-8') as f:
        f.write('/* Generado por sismografo/paginas.py a partir de contenido/' + ('' if lang == 'es' else 'en/')
                + 'mapa.yml: no editar aquí. */\nwindow.MAPA_TEXTOS = ' + json.dumps(tx, ensure_ascii=False, indent=1) + ';\n')
    fn_p = os.path.join(base_p, 'mapa.html')
    if not os.path.exists(fn_p): return
    cab = crudo.get('cabecera') or {}

    def campo(m):
        k = m.group(1)
        v = cab.get(k)
        if v in (None, ''): return m.group(0)
        return _md_linea(v) if k == 'titulo' else html.escape(str(v), quote=True)
    salida = open(fn_p, encoding='utf-8').read().replace('{{version}}', version)
    salida = re.sub(r'\{\{cabecera\.(\w+)\}\}', campo, salida)
    open(os.path.join(destino, NOMBRES[lang]['mapa']), 'w', encoding='utf-8').write(salida)


if __name__ == '__main__':
    construir()
    print('Páginas construidas en site/')
