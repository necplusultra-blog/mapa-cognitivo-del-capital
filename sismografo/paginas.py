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
  [[cifra id | etiqueta | nota]] una cifra destacada; varias seguidas forman una fila
  :::como Título             abre un desplegable de explicación (se cierra con una línea ::: )
  :::como+ Título            lo mismo, pero abierto por defecto
Encabezado opcional de cada archivo (entre líneas ---): id (ancla), menu (texto del índice lateral),
oculta: si (la sección aparece sólo cuando hay datos), lugar: portada | pie.
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
    out, cifras = [], []

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
            out.append(f'\n<details class="como"{" open" if m.group(1) else ""} markdown="1">\n<summary>{m.group(2)}</summary>\n'); continue
        if t == ':::':
            out.append('\n</details>\n'); continue
        out.append(linea)
    volcar()
    return _inline('\n'.join(out))


def _md(texto):
    return markdown.markdown(_bloques(texto), extensions=EXT, output_format='html5')


def construir(dir_site=None):
    dir_site = dir_site or os.path.join(RAIZ, 'site')
    for pagina in ('inicio', 'lectura', 'metodologia'):
        partes, menu, lugares = [], [], {'portada': [], 'pie': []}
        for fn in sorted(glob.glob(os.path.join(RAIZ, 'contenido', pagina, '*.md'))):
            meta, texto = _front(open(fn, encoding='utf-8').read())
            cuerpo = _md(texto)
            sid = meta.get('id') or re.sub(r'^\d+-', '', os.path.splitext(os.path.basename(fn))[0])
            oculta = ' hidden' if meta.get('oculta', '').lower() in ('si', 'sí', 'true') else ''
            clase = meta.get('clase', 'seccion')
            if meta.get('lugar') in lugares:
                lugares[meta['lugar']].append(cuerpo); continue
            partes.append(f'<section id="{sid}" class="{clase}"{oculta}>\n{cuerpo}\n</section>')
            if meta.get('menu'):
                menu.append(f'<li><a href="#{sid}">{html.escape(meta["menu"])}</a></li>')
        plantilla = open(os.path.join(RAIZ, 'plantillas', f'{pagina}.html'), encoding='utf-8').read()
        salida = (plantilla.replace('{{contenido}}', '\n'.join(partes)).replace('{{menu}}', '\n'.join(menu))
                  .replace('{{portada}}', '\n'.join(lugares['portada'])).replace('{{pie}}', '\n'.join(lugares['pie'])))
        nombre = 'index.html' if pagina == 'inicio' else f'{pagina}.html'
        open(os.path.join(dir_site, nombre), 'w', encoding='utf-8').write(salida)


if __name__ == '__main__':
    construir()
    print('Páginas construidas en site/')
