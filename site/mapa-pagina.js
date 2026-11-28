/* Pestaña Mapa — interfaz de la lámina: panel lateral, símbolos y recorrido guiado.
   Mapa cognitivo del capital — Pablo Jiménez Cea. Licencia MIT.
   La usan mapa.html y en/map.html; el idioma sale del atributo lang de la página.
   Necesita mapa-cognitivo.js (motor) y explorador.js (curvas del panel). */
(function () {
  'use strict';
  var EN = /^en/.test(document.documentElement.lang);
  function L(es, en) { return EN ? en : es; }
  /* Textos editables: contenido/mapa.yml (contenido/en/mapa.yml) → mapa-textos.js → window.MAPA_TEXTOS.
     T('panel.titulo', es, en, vars): el texto del YAML si existe; si no, el de aquí. {n}, {eeuu}… se reemplazan con vars. */
  var TX = window.MAPA_TEXTOS || {};
  function T(clave, es, en, vars) {
    var v = clave.split('.').reduce(function (o, k) { return o == null ? o : o[k]; }, TX);
    var s = (typeof v === 'string' && v.trim()) ? v : (EN ? en : es);
    return vars ? s.replace(/\{(\w+)\}/g, function (m, k) { return k in vars ? vars[k] : m; }) : s;
  }
  var PRE = EN ? '../' : '';
  var panel = document.getElementById('panel'), estado = document.getElementById('estado');
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var di = function (t) { estado.textContent = t; clearTimeout(di.t); di.t = setTimeout(function () { estado.textContent = ''; }, 4000); };
  var mapa = null, E = null;
  var TIPOS = { hoja: T('ficha.tipo_hoja', 'cálculo', 'calculation'), decision: T('ficha.tipo_decision', 'bifurcación', 'fork'),
                familia: T('ficha.tipo_familia', 'sección del sitio', 'section of the site'), serie: T('ficha.tipo_serie', 'serie', 'series'),
                estacion: T('ficha.tipo_estacion', 'estación', 'station'), empalme: T('ficha.tipo_empalme', 'empalme', 'splice') };
  /* etiquetas accesibles de la guía y de la capa de símbolos */
  document.getElementById('guia').setAttribute('aria-label', T('recorrido.aria', 'Recorrido guiado', 'Guided tour'));
  document.getElementById('simbolos').setAttribute('aria-label', T('simbolos.titulo', 'Símbolos y expresiones', 'Symbols and expressions'));

  /* ------------------------------------------------------------------ panel */
  function sparq(q) {
    var a0 = 1948, a1 = 2025, w = 320, h = 56, mx = Math.max.apply(null, [1].concat(Object.values(q))), barras = '';
    for (var a = a0; a <= a1; a++) { var v = q[a] || 0; if (!v) continue; var x = (a - a0) / (a1 - a0) * (w - 4) + 2, hh = Math.max(1.5, v / mx * (h - 16));
      barras += '<rect x="' + x.toFixed(1) + '" y="' + (h - 12 - hh).toFixed(1) + '" width="2.6" height="' + hh.toFixed(1) + '" rx="1" fill="#e2673f"/>'; }
    var ejes = [1950, 1970, 1990, 2010].map(function (a) { var x = (a - a0) / (a1 - a0) * (w - 4) + 2; return '<text x="' + x + '" y="' + (h - 1) + '" font-size="8" fill="#9b978b" text-anchor="middle">' + a + '</text>'; }).join('');
    return '<svg class="sparq" viewBox="0 0 ' + w + ' ' + h + '" preserveAspectRatio="none" role="img" aria-label="' + T('ficha.quiebres_aria', 'Quiebres por año', 'Breaks per year') + '"><line x1="0" x2="' + w + '" y1="' + (h - 12) + '" y2="' + (h - 12) + '" stroke="#262b33"/>' + barras + ejes + '</svg>';
  }
  function miniSimbolos() {
    var S = (E.D.simbolos || []).slice(0, 7);
    return '<div class="mini-simbolos">' + S.map(function (s) { return '<b>' + esc(EN ? s[3] || s[0] : s[0]) + '</b><span>' + esc(EN ? s[2] : s[1]) + '</span>'; }).join('') + '</div>'
      + '<button class="boton-texto" data-simbolos>' + T('panel.boton_todos_simbolos', 'Todos los símbolos', 'All symbols') + '</button>';
  }
  function inicio() {
    var m = E.D.meta || {};
    var claves = E.nodos.filter(function (n) { return n.clave; }).sort(function (a, b) { return a.cod.localeCompare(b.cod); });
    panel.innerHTML = '<div class="cod">' + T('panel.antetitulo', 'cómo leer la figura', 'how to read the figure') + '</div><h2>' + T('panel.titulo', 'Cuatro paneles sobre un eje', 'Four panels on one axis') + '</h2>'
      + '<div class="sec cifras"><div><b>' + E.eeuu.hojas.length + '</b><span>' + T('panel.cifra_eeuu', 'cálculos de EE.UU. (A)', 'US calculations (A)') + '</span></div><div><b>' + E.mundo.hojas.length + '</b><span>' + T('panel.cifra_mundo', 'cálculos mundiales (B)', 'world calculations (B)') + '</span></div><div><b>' + E.familias.reduce(function (s, f) { return s + f.series.length; }, 0) + '</b><span>' + T('panel.cifra_series', 'series publicadas (C)', 'published series (C)') + '</span></div></div>'
      + '<div class="sec"><p>' + T('panel.parrafo', 'La tasa de ganancia no tiene una sola medida: depende de decisiones teóricas en disputa. El panel <b>A</b> muestra, para EE.UU., todos los cálculos que resultan de combinar las decisiones de la literatura marxista contemporánea (un anillo por decisión) y la trayectoria de cada uno en el tiempo; <b>B</b>, lo mismo para el mundo. <b>C</b> reúne las series del sitio por sección y <b>D</b>, la dispersión de los cálculos y sus quiebres. ¿Primera vez? Pulse <b>Recorrer</b>.',
        'The rate of profit has no single measure: it depends on contested theoretical decisions. Panel <b>A</b> shows, for the United States, every calculation that results from combining the decisions of contemporary Marxist literature (one ring per decision) and the path of each over time; <b>B</b> does the same for the world. <b>C</b> gathers the site’s series by section and <b>D</b> the spread of the calculations and their breaks. First time? Press <b>Tour</b>.') + '</p></div>'
      + '<div class="sec"><div class="lab">' + T('panel.rotulo_simbolos', 'símbolos frecuentes', 'common symbols') + '</div>' + miniSimbolos() + '</div>'
      + '<div class="sec"><div class="lab">' + T('panel.rotulo_nodos', 'nodos clave', 'key nodes') + '</div><div class="lista-clave">' + claves.map(function (n) { return '<button data-i="' + E.nodos.indexOf(n) + '"><span>' + esc(n.cod) + '</span>' + esc(n.clave) + '</button>'; }).join('') + '</div></div>'
      + '<div class="sec"><div class="lab">' + T('panel.rotulo_leyenda', 'leyenda', 'key') + '</div><div class="ley">'
      + '<svg width="30" height="10"><path d="M0 5H30" stroke="#e8e4d8" stroke-width="1.4"/></svg><span>' + T('panel.leyenda_eje', 'eje de exposición categorial (01–05)', 'axis of categorial exposition (01–05)') + '</span>'
      + '<svg width="30" height="12"><path d="M0 11C10 11 10 2 30 2" stroke="#d6c39a" fill="none"/></svg><span>' + T('panel.leyenda_decision_eeuu', 'decisión teórica, EE.UU. (A)', 'theoretical decision, US (A)') + '</span>'
      + '<svg width="30" height="12"><path d="M0 11C10 11 10 2 30 2" stroke="#8cc0bd" fill="none"/></svg><span>' + T('panel.leyenda_decision_mundo', 'decisión teórica, mundo (B)', 'theoretical decision, world (B)') + '</span>'
      + '<svg width="30" height="10"><path d="M0 5H30" stroke="#d6c39a" stroke-opacity=".35"/><circle cx="12" cy="5" r="2" fill="#e2673f"/><circle cx="22" cy="5" r="2" fill="#e2673f"/></svg><span>' + T('panel.leyenda_especificacion', 'un cálculo en el tiempo y sus quiebres estructurales', 'one calculation over time and its structural breaks') + '</span>'
      + '<svg width="30" height="10"><path d="M0 5H30" stroke="#e2673f" stroke-opacity=".6" stroke-width="1.6"/></svg><span>' + T('panel.leyenda_crisis', 'año con quiebre en al menos la mitad de los cálculos', 'year with a break in at least half of the calculations') + '</span>'
      + '<svg width="30" height="10"><path d="M0 5H30" stroke="#7ea6d8" stroke-dasharray="4 3"/></svg><span>' + T('panel.leyenda_empalme', 'empalme estadístico SIC → NAICS', 'SIC → NAICS statistical splice') + '</span>'
      + '<svg width="30" height="10"><path d="M2 2V8M2 8H28" stroke="#aab4c2" fill="none"/><circle cx="28" cy="8" r="2" fill="#aab4c2"/></svg><span>' + T('panel.leyenda_serie', 'serie publicada en una sección del sitio (C)', 'series published in a section of the site (C)') + '</span>'
      + '</div></div>'
      + '<div class="sec"><div class="lab">' + T('panel.ayuda', 'rueda o pellizco: zoom · arrastrar: mover · clic: fijar · Esc: soltar · al acercarse aparecen las expresiones de cada serie', 'wheel or pinch: zoom · drag: pan · click: pin · Esc: release · zoom in to see the expression of each series') + '</div>'
      + '<div class="sub">' + T('panel.nota_datos', 'Datos: {fecha}. Todo lo dibujado sale de los datos publicados; nada es decorativo.', 'Data: {fecha}. Everything drawn comes from the published data; nothing is decorative.', { fecha: esc(m.actualizado || '—') }) + '</div><div class="cita-doi">' + T('panel.cita', 'Cómo citar: Jiménez Cea (2026), <i>Mapa cognitivo del capital</i>, DOI', 'How to cite: Jiménez Cea (2026), <i>Cognitive Map of Capital</i>, DOI') + ' <a href="https://doi.org/10.5281/zenodo.24551894">10.5281/zenodo.24551894</a></div></div>';
  }
  function mostrar(d, fijado) {
    if (!d) return inicio();
    var h = fijado ? '<div class="fijado"><span>' + T('ficha.fijado', 'Fijado', 'Pinned') + '</span><button class="soltar" data-soltar>' + T('ficha.soltar', 'Soltar · Esc', 'Release · Esc') + '</button></div>' : '';
    h += '<div class="cod">' + esc(d.cod ? d.cod + ' · ' + (TIPOS[d.tipo] || d.tipo) : (TIPOS[d.tipo] || d.tipo)) + (d.arbol ? ' · ' + esc(d.arbol) : '') + '</div><h2' + (d.tipo === 'hoja' ? ' class="id"' : '') + '>' + esc(d.titulo) + '</h2><div class="sub">' + esc(d.sub || '') + '</div>';
    if (d.expresion) h += '<div class="formula"><small>' + T('ficha.expresion', 'expresión', 'expression') + '</small>' + esc(d.expresion) + '</div>';
    if (d.texto) h += '<div class="sec"><p>' + esc(d.texto) + '</p></div>';
    if (d.columna) h += '<div class="sec"><div class="lab">' + T('ficha.columna', 'columna en los datos', 'column in the data') + '</div><span class="sub"><code>' + esc(d.columna) + '</code> · <a href="' + PRE + 'descargas/glosario_series.csv" download>' + T('ficha.glosario_csv', 'glosario de las series (CSV)', 'glossary of the series (CSV)') + '</a></span></div>';
    if (d.opciones) {
      var tot = d.opciones.reduce(function (s, o) { return s + o[1]; }, 0);
      h += '<div class="sec"><div class="lab">' + T('ficha.decision_explicita', 'decisión teórica explícita', 'explicit theoretical decision') + ' · ' + esc(d.decision) + (d.posicion ? ' · ' + esc(d.posicion) : '') + '</div><ul>' + d.opciones.map(function (o) { return '<li class="op"><span>' + esc(o[0]) + '</span><span>' + o[1] + ' ' + T('ficha.abrev_especificaciones', 'cálculos', 'calculations') + '</span><span class="barra-op"><i style="width:' + (o[1] / tot * 100).toFixed(1) + '%"></i></span></li>'; }).join('') + '</ul></div>';
    }
    if (d.decisiones) h += '<div class="sec"><div class="lab">' + T('ficha.decisiones_especificacion', 'decisiones de este cálculo', 'decisions of this calculation') + '</div><dl class="dec">' + d.decisiones.map(function (x) { return '<dt>' + esc(x[0]) + '</dt><dd>' + esc(x[1]) + '</dd>'; }).join('') + '</dl></div>';
    if (d.spec != null || d.grupos || (d.idx && d.idx.length > 1)) h += '<div class="sec"><div class="lab">' + (d.spec != null ? T('ficha.curva_especificacion', 'tasa de este cálculo frente al conjunto', 'rate of this calculation against the whole set') : d.grupos ? T('ficha.curva_opciones', 'mediana de cada opción frente al conjunto', 'median of each option against the whole set') : T('ficha.curva_rama', 'mediana de esta rama frente al conjunto', 'median of this branch against the whole set')) + ' · ' + T('ficha.base_100', '100 = promedio del periodo', '100 = period average') + '</div><div class="ex-curva" id="ex-curva"></div><div class="sub" id="ex-niveles"></div></div>';
    if (d.anios) h += '<div class="sec"><div class="lab">' + T('ficha.quiebres', 'quiebres estructurales detectados', 'structural breaks detected') + '</div>' + (d.anios.length ? d.anios.map(function (a) { return '<span class="chip">' + a + '</span>'; }).join('') : '<span class="sub">' + T('ficha.ninguno', 'ninguno', 'none') + '</span>') + '</div>';
    if (d.quiebres && d.n > 1) h += '<div class="sec"><div class="lab">' + T('ficha.quiebres_rama', 'quiebres por año en los {n} cálculos de esta rama', 'breaks per year in the {n} calculations of this branch', { n: d.n }) + '</div>' + sparq(d.quiebres) + '</div>';
    if (d.ruta && d.ruta.length && !d.decisiones) h += '<div class="sec"><div class="lab">' + T('ficha.ruta', 'decisiones tomadas hasta aquí', 'decisions taken up to here') + '</div><dl class="dec">' + d.ruta.map(function (x) { return '<dt>' + esc(x[0]) + '</dt><dd>' + esc(x[1]) + '</dd>'; }).join('') + '</dl></div>';
    if (d.series) {
      var gl = d.glosas || [];
      h += '<div class="sec"><div class="lab">' + T('ficha.series_seccion', 'series de esta sección · nombre y expresión', 'series of this section · name and expression') + '</div>' + d.series.map(function (s, i) {
        var g = gl[i] || [s, '', ''];
        return '<button class="serie-it" data-serie="' + i + '"><b>' + esc(g[1] && g[1] !== '—' ? g[1] : s) + '</b><span>' + esc(g[0]) + '</span></button>';
      }).join('') + '</div>';
    }
    if (d.empalmes) h += '<div class="sec"><div class="lab">' + T('ficha.empalmes', 'factores de empalme (meta.json)', 'splice factors (meta.json)') + '</div><dl class="dec">' + d.empalmes.map(function (e) { return '<dt>' + esc(e[0]) + '</dt><dd>× ' + esc(e[1]) + '</dd>'; }).join('') + '</dl></div>';
    if (d.enlaces) h += '<div class="sec enl">' + d.enlaces.map(function (e) { return '<a href="' + esc(e[0]) + '">' + esc(e[1]) + ' →</a>'; }).join('') + '</div>';
    panel.innerHTML = h;
    panel.scrollTop = 0;
    curvaPanel(d);
  }
  /* curva del explorador: hoja → su tasa; bifurcación → mediana de cada opción; rama → su mediana */
  var COLORES = ['#d6c39a', '#8cc0bd', '#e2673f', '#aab4c2', '#c9a0dc'], turno = 0;
  var TABLA = PRE + (EN ? 'descargas/eeuu_specifications_table_en.csv' : 'descargas/eeuu_tabla_especificaciones.csv');
  function curvaPanel(d) {
    var caja = document.getElementById('ex-curva'); if (!caja || !window.Explorador) return;
    var t = ++turno;
    Explorador.datos().then(function (D) {
      if (t !== turno) return;
      var lineas, q = null;
      if (d.spec != null) { lineas = [{ v: D.indices[d.spec], n: T('ficha.esta_especificacion', 'este cálculo', 'this calculation'), c: COLORES[0] }]; q = d.anios; }
      else if (d.grupos) lineas = d.grupos.slice(0, 5).map(function (g, i) { return { v: Explorador.medianaDe(D, g[1]), n: g[0] + ' (' + g[1].length + ')', c: COLORES[i] }; });
      else lineas = [{ v: Explorador.medianaDe(D, d.idx), n: T('ficha.mediana_rama', 'mediana de la rama', 'median of the branch'), c: COLORES[0] }];
      Explorador.curva(caja, D, lineas, { alto: 190, quiebres: q });
      var nv = document.getElementById('ex-niveles');
      if (nv) nv.innerHTML = (d.spec != null ? T('ficha.tasa', 'Tasa', 'Rate') + ': ' + Explorador.niveles(D, d.spec).map(function (x) { return x[0] + ' <b>' + Explorador.fmt(x[1]) + '</b>'; }).join(' · ') + '. ' : '')
        + '<a href="' + TABLA + '" download>' + T('ficha.tabla_csv', 'Tabla de los cálculos (CSV)', 'Table of the calculations (CSV)') + '</a>';
    }).catch(function () { caja.textContent = T('ficha.error_series', 'No se pudieron cargar las series.', 'The series could not be loaded.'); });
  }

  /* ------------------------------------------------------------------ símbolos */
  var capaSim = document.getElementById('simbolos'), btnSim = document.getElementById('btn-simbolos');
  function abrirSimbolos(si) {
    if (si === undefined) si = capaSim.hidden;
    if (si && !capaSim.dataset.listo) {
      var S = E.D.simbolos || [];
      var series = [];
      E.familias.forEach(function (F) { F.glosa.forEach(function (g, i) { if (g[1] && /[\/=·−+Σ×]/.test(g[1])) series.push([g[1], g[0], F.nombre, F, i]); }); });
      capaSim.innerHTML = '<div class="cab"><div><h2>' + T('simbolos.titulo', 'Símbolos y expresiones', 'Symbols and expressions') + '</h2><p>' + T('simbolos.intro', 'Qué significa cada letra y cada cociente que aparece en la figura. Al acercarse al panel C, cada serie muestra su expresión.', 'What each letter and each ratio in the figure means. Zoom into panel C and each series shows its expression.') + '</p></div><button class="cerrar" data-cerrar>' + T('simbolos.cerrar', 'Cerrar · Esc', 'Close · Esc') + '</button></div>'
        + '<div class="rejilla">' + S.map(function (s) { return '<div class="simbolo"><b>' + esc(EN ? s[3] || s[0] : s[0]) + '</b><span>' + esc(EN ? s[2] : s[1]) + '</span></div>'; }).join('') + '</div>'
        + '<h3>' + T('simbolos.subtitulo_series', 'Expresiones de las series publicadas', 'Expressions of the published series') + '</h3><div class="rejilla">'
        + series.map(function (s, k) { return '<button class="simbolo serie-it" style="display:block" data-sim="' + k + '"><b>' + esc(s[0]) + '</b><span>' + esc(s[1]) + ' · ' + esc(s[2]) + '</span></button>'; }).join('') + '</div>'
        + '<p class="sub" style="margin-top:16px"><a href="' + (EN ? 'glossary.html' : 'glosario.html') + '">' + T('simbolos.enlace_glosario', 'Glosario completo: símbolos y series', 'Full glossary: symbols and series') + ' →</a> · <a href="' + PRE + 'descargas/glosario_series.csv" download>' + T('simbolos.enlace_csv', 'Glosario de las series (CSV)', 'Glossary of the series (CSV)') + '</a></p>';
      capaSim._series = series; capaSim.dataset.listo = '1';
    }
    capaSim.hidden = !si; btnSim.setAttribute('aria-pressed', String(si));
    if (si) capaSim.querySelector('[data-cerrar]').focus();
  }
  capaSim.addEventListener('click', function (e) {
    if (e.target.closest('[data-cerrar]')) return abrirSimbolos(false);
    var b = e.target.closest('[data-sim]'); if (!b) return;
    var s = capaSim._series[+b.dataset.sim]; abrirSimbolos(false); mapa.enfocar(s[3].hijos[s[4]], 3);
  });

  /* ------------------------------------------------------------------ recorrido guiado */
  var guia = document.getElementById('guia'), paso = -1, auto = true, reloj = null, t0 = 0, DUR = 11000;
  function nodoCod(c) { return E.nodos.filter(function (n) { return n.cod === c; })[0]; }
  function fam(a) { return E.familias.filter(function (f) { return f.ancla === a; })[0]; }
  function hojaEj() { return E.eeuu.hojas.filter(function (h) { return h.datos[0] === 'B|b|cc|neta|ppi-incl|K-todo|noutil'; })[0] || E.eeuu.hojas[0]; }
  function serieDe(a, c) { var F = fam(a); return F && F.hijos.filter(function (s) { return s.nombre === c; })[0]; }
  var PASOS = null;
  /* Pasos por defecto: la cámara (z, n, p) de cada clave y sus textos. Si contenido/mapa.yml trae recorrido.pasos,
     el orden y los textos salen de ahí; cada paso conserva la cámara de su clave (una clave desconocida = vista general). */
  function Z(k) { return function () { return E.zonas[k]; }; }
  function pasosPorDefecto() { return [
    { k: 'regiones', t: L('Una figura, cuatro paneles', 'One figure, four panels'), z: 1, p: Z('todo'),
      x: L('La figura reúne en una sola imagen lo que calcula el sitio. <b>A</b>: los cálculos de la tasa de ganancia de EE.UU. <b>B</b>: los cálculos mundiales. <b>C</b>: las series publicadas, por sección. <b>D</b>: la dispersión de los cálculos y sus quiebres en el tiempo. Todo se ordena sobre el eje horizontal.',
           'The figure gathers what the site calculates into one image. <b>A</b>: the calculations of the US rate of profit. <b>B</b>: the world calculations. <b>C</b>: the published series, by section. <b>D</b>: the spread of the calculations and their breaks over time. Everything is ordered along the horizontal axis.') },
    { k: 'eje', t: L('01–05 · Orden de exposición categorial', '01–05 · Order of categorial exposition'), z: 1.5, n: function () { return E.estaciones[0].nodo; }, p: Z('eje'),
      x: L('El eje se lee de izquierda a derecha: <b>lógica del capital</b>, plusvalor y ganancia, fuerzas productivas, tiempo disponible y <b>límites inmanentes</b>. La categoría va primero; las series son su manifestación fenoménica en precios y en horas, no su demostración.',
           'The axis reads from left to right: <b>logic of capital</b>, surplus value and profit, productive forces, disposable time and <b>immanent limits</b>. The category comes first; the series are its phenomenal manifestation in prices and hours, not its demonstration.') },
    { k: 'multiverso', t: L('A · Los cálculos posibles de la tasa de ganancia', 'A · The possible calculations of the rate of profit'), z: 1.6, n: function () { return E.eeuu.raiz; }, p: Z('A'),
      x: L('No hay una sola manera de medir la tasa de ganancia: cada bifurcación del árbol es una decisión teórica explícita de la literatura marxista (qué sector, qué cuenta como plusvalor, cómo se valora el capital…). Las {eeuu} hojas son los cálculos que resultan de combinarlas; se publican todos, no uno elegido.',
           'There is no single way of measuring the rate of profit: each fork in the tree is an explicit theoretical decision from the Marxist literature (which sector, what counts as surplus value, how capital is valued…). The {eeuu} leaves are the calculations that result from combining them; all are published, not one chosen.') },
    { k: 'niveles', t: L('Leer los anillos de A', 'Reading the rings of A'), z: 2.2, p: Z('leyenda'),
      x: L('Cada anillo numerado corresponde a una decisión, del centro hacia fuera; la leyenda dice cuál. Después de las hojas viene la <b>corona</b>: cada cálculo prolongado en el tiempo, con sus quiebres estructurales en rojo.',
           'Each numbered ring corresponds to a decision, from the centre outwards; the key says which. After the leaves comes the <b>outer band</b>: each calculation extended over time, with its structural breaks in red.') },
    { k: 'bifurcacion', t: L('07 · Qué cuenta como plusvalor', '07 · What counts as surplus value'), z: 2.6, n: function () { return nodoCod('#07'); },
      x: L('Esta bifurcación decide qué trabajo es productivo. El panel de la derecha muestra la mediana de cada opción frente al conjunto: se ve si la decisión cambia el <b>movimiento</b> de la tasa o sólo su nivel.',
           'This fork decides which labour is productive. The panel on the right shows the median of each option against the whole set: you can see whether the decision changes the <b>movement</b> of the rate or only its level.') },
    { k: 'especificacion', t: L('Un cálculo', 'One calculation'), z: 3, n: hojaEj,
      x: L('Cada hoja es un cálculo completo, con todas sus decisiones. Éste es el plusvalor ampliado por ramas a costo corriente. El panel dibuja su curva sobre las bandas del conjunto y sus niveles en 1948, 1982 y el último año.',
           'Each leaf is a complete calculation, with all its decisions. This one is extended surplus value by industry at current cost. The panel draws its curve over the bands of the whole set and its levels in 1948, 1982 and the latest year.') },
    { k: 'anillo', t: L('La corona del tiempo', 'The outer band of time'), z: 2.1, n: hojaEj, p: function () { return [E.eeuu.cfg.cx, 120]; },
      x: L('Cada radio prolonga un cálculo de 1948 (dentro) al último año (fuera). Los puntos <b>rojos</b> son sus quiebres estructurales. Cuando los puntos de muchos cálculos se alinean en un arco, el quiebre resiste las decisiones teóricas; los arcos rojos marcan los años en que lo registra al menos la mitad.',
           'Each spoke extends a calculation from 1948 (inside) to the latest year (outside). The <b>red</b> dots are its structural breaks. When the dots of many calculations line up in an arc, the break withstands the theoretical decisions; the red arcs mark the years in which at least half record one.') },
    { k: 'empalmes', t: L('08 · Empalmes estadísticos', '08 · Statistical splices'), z: 2.2, n: function () { return E.empalme; },
      x: L('Las series oficiales cambian de clasificación industrial (SIC → NAICS). Los arcos discontinuos azules marcan esos años; cada empalme usa un factor explícito, publicado en la metodología.',
           'The official series change industrial classification (SIC → NAICS). The dashed blue arcs mark those years; each splice uses an explicit factor, published in the methodology.') },
    { k: 'mundo', t: L('B · Los cálculos mundiales', 'B · The world calculations'), z: 2, n: function () { return E.mundo.raiz; }, p: Z('B'),
      x: L('A la derecha, la tasa de ganancia mundial con la Penn World Table: {mundo} cálculos (medida, ponderación, con o sin China, panel de países). Las barras exteriores dan el número de países de cada uno.',
           'On the right, the world rate of profit from the Penn World Table: {mundo} calculations (measure, weighting, with or without China, country panel). The outer bars give the number of countries in each.') },
    { k: 'plusvalor', t: L('C · Las series del sitio', 'C · The series of the site'), z: 2.3, n: function () { return fam('index.html#masa-tasa'); },
      x: L('Debajo del eje, cada sección del sitio cuelga de la categoría que expone, y cada punto es una serie publicada. El panel de la derecha da el nombre y la <b>expresión</b> de cada serie.',
           'Below the axis, each section of the site hangs from the category it sets out, and each dot is a published series. The panel on the right gives the name and <b>expression</b> of each series.') },
    { k: 'expresion', t: L('Leer una expresión: K / V', 'Reading an expression: K / V'), z: 3.4, n: function () { return serieDe('index.html#masa-tasa', 'kv_ramas'); },
      x: L('<code>K / V</code> es la composición de valor del capital: cuánto capital fijo (<code>K</code>) se adelanta por cada dólar de salarios productivos (<code>V</code>). <code>e = pv / v</code> es la tasa de plusvalor. El botón <b>Símbolos</b> reúne las letras de la figura; la pestaña <b>Glosario</b> las explica todas.',
           '<code>K / V</code> is the value composition of capital: how much fixed capital (<code>K</code>) is advanced per dollar of productive wages (<code>V</code>). <code>e = pv / v</code> is the rate of surplus value. The <b>Symbols</b> button gathers the letters in the figure; the <b>Glossary</b> tab explains them all.') },
    { k: 'fuerzas', t: L('03–04 · Fuerzas productivas y tiempo disponible', '03–04 · Productive forces and disposable time'), z: 1.9, n: function () { return E.estaciones[2].nodo; }, p: function () { return [810, 560]; },
      x: L('Las series del tiempo de trabajo: horas necesarias y de plustrabajo, valor nuevo por hora, minutos productivos por habitante. Registran la medida del valor y el tiempo que la productividad libera.',
           'The series of labour time: necessary and surplus-labour hours, new value per hour, productive minutes per inhabitant. They record the measure of value and the time that productivity frees.') },
    { k: 'registro', t: L('D · Dispersión y quiebres', 'D · Spread and breaks'), z: 1.6, p: Z('D'),
      x: L('Abajo, los cálculos de EE.UU. en el tiempo: bandas de los percentiles 10–90 y 25–75 (100 = promedio del periodo de cada cálculo), la mediana y, en barras rojas, cuántos cálculos registran un quiebre estructural cada año.',
           'Below, the US calculations over time: bands of the 10th–90th and 25th–75th percentiles (100 = each calculation’s period average), the median and, in red bars, how many calculations record a structural break each year.') },
    { k: 'explorar', t: L('Ahora, explore', 'Now, explore'), z: 1, p: Z('todo'),
      x: L('Pinche cualquier nodo para fijarlo; acérquese para leer las expresiones de cada serie. En la portada, el <b>explorador</b> permite elegir una opción en cada decisión y ver la curva resultante.',
           'Click any node to pin it; zoom in to read the expression of each series. On the home page, the <b>explorer</b> lets you choose an option at each decision and see the resulting curve.') }
  ]; }
  function construirPasos() {
    var base = pasosPorDefecto(), lista = TX.recorrido && TX.recorrido.pasos, porClave = {};
    if (!Array.isArray(lista) || !lista.length) return base;
    base.forEach(function (P) { porClave[P.k] = P; });
    var vars = { eeuu: E.eeuu.hojas.length, mundo: E.mundo.hojas.length };
    var sust = function (t) { return String(t || '').replace(/\{(\w+)\}/g, function (m, k) { return k in vars ? vars[k] : m; }); };
    return lista.filter(function (it) { return it && (it.titulo || it.texto); }).map(function (it) {
      var P = porClave[it.clave] || { z: 1, p: Z('todo') };
      return { k: it.clave, t: sust(it.titulo) || P.t, x: sust(it.texto) || P.x, z: P.z, n: P.n, p: P.p };
    });
  }
  function pintarGuia() {
    var P = PASOS[paso];
    guia.innerHTML = '<div class="cab"><span>' + T('recorrido.rotulo', 'Recorrido', 'Tour') + ' · ' + ('0' + (paso + 1)).slice(-2) + ' / ' + ('0' + PASOS.length).slice(-2) + '</span><button data-g="salir" aria-label="' + T('recorrido.salir', 'Salir del recorrido', 'Exit the tour') + '">✕</button></div>'
      + '<div class="pasos">' + PASOS.map(function (_, i) { return '<i class="' + (i < paso ? 'hecho' : i === paso ? 'ahora' : '') + '"></i>'; }).join('') + '</div>'
      + '<h3>' + P.t + '</h3><p>' + P.x + '</p>'
      + '<div class="ctl"><button data-g="ant"' + (paso ? '' : ' disabled') + '>‹ ' + T('recorrido.anterior', 'Anterior', 'Back') + '</button><button data-g="auto" aria-pressed="' + auto + '">' + (auto ? T('recorrido.pausa', 'Pausa', 'Pause') : T('recorrido.reproducir', 'Reproducir', 'Play')) + '</button><button class="sig" data-g="sig">' + (paso < PASOS.length - 1 ? T('recorrido.siguiente', 'Siguiente', 'Next') + ' ›' : T('recorrido.terminar', 'Terminar', 'Finish')) + '</button></div>';
  }
  function irA(i) {
    if (i < 0) i = 0;
    if (i >= PASOS.length) return salir();
    paso = i; var P = PASOS[i], n = P.n ? P.n() : null, p = P.p ? P.p().slice() : n ? [n.x, n.y] : E.zonas.todo.slice();
    /* en pantallas anchas, el foco se corre hacia arriba a la derecha para que la tarjeta del recorrido no lo tape */
    if (window.innerWidth >= 900 && P.z > 1) { var u = (document.getElementById('lamina').clientWidth / MapaCognitivo.W) * P.z; p = [p[0] - 170 / u, p[1] + 90 / u]; }
    mapa.fijar(n || null);
    mapa.volar(p[0], p[1], P.z, 1600);
    pintarGuia(); t0 = performance.now();
  }
  function tic() {
    if (paso < 0) return;
    var el = guia.querySelector('.pasos i.ahora');
    if (auto) {
      var f = Math.min(1, (performance.now() - t0) / DUR);
      if (el) el.style.setProperty('--avance', f.toFixed(3));
      if (f >= 1 && paso < PASOS.length - 1) irA(paso + 1);
    } else if (el) el.style.setProperty('--avance', '0');
    reloj = requestAnimationFrame(tic);
  }
  function empezar() {
    abrirSimbolos(false); PASOS = PASOS || construirPasos();
    guia.hidden = false; document.getElementById('btn-recorrer').setAttribute('aria-pressed', 'true');
    auto = !(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
    irA(0); cancelAnimationFrame(reloj); reloj = requestAnimationFrame(tic);
    guia.querySelector('.sig').focus();
  }
  function salir() {
    paso = -1; cancelAnimationFrame(reloj); guia.hidden = true; document.getElementById('btn-recorrer').setAttribute('aria-pressed', 'false');
    mapa.soltar(); mapa.volar(MapaCognitivo.W / 2, MapaCognitivo.H / 2, 1, 1200);
  }
  guia.addEventListener('click', function (e) {
    var b = e.target.closest('[data-g]'); if (!b) return;
    var g = b.dataset.g;
    if (g === 'salir') salir();
    if (g === 'ant') irA(paso - 1);
    if (g === 'sig') irA(paso + 1);
    if (g === 'auto') { auto = !auto; t0 = performance.now(); pintarGuia(); }
  });

  /* ------------------------------------------------------------------ descargas y mandos */
  var guardar = null; if (window.claude && window.claude.use) window.claude.use('downloads').then(function (d) { guardar = d; }).catch(function () {});
  function bajar(blob, nombre) {
    if (guardar) { guardar.save({ filename: nombre, data: blob }).catch(function () { di(T('mensajes.descarga_cancelada', 'Descarga cancelada', 'Download cancelled')); }); return; }
    var u = URL.createObjectURL(blob), a = document.createElement('a'); a.href = u; a.download = nombre; document.body.appendChild(a); a.click(); a.remove(); setTimeout(function () { URL.revokeObjectURL(u); }, 5000);
  }
  mapa = MapaCognitivo.montar(document.getElementById('lamina'), {
    modo: 'mapa', grano: false, url: PRE + 'data/mapa.json', alSeleccionar: function (d, f) { mostrar(d, f); },
    alListo: function (a) { mapa = a; E = a.escena(); inicio(); if (/[#&]recorrido/.test(location.hash)) empezar(); }, datos: window.MAPA_DATOS
  });
  panel.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    if (b.hasAttribute('data-soltar')) return mapa.soltar();
    if (b.hasAttribute('data-simbolos')) return abrirSimbolos(true);
    if (b.dataset.i) return mapa.enfocar(E.nodos[+b.dataset.i], 2.2);
    if (b.dataset.serie != null && E._famSel) mapa.enfocar(E._famSel.hijos[+b.dataset.serie], 3);
  });
  /* recordar la familia mostrada en el panel, para que su lista de series lleve a cada serie */
  var mostrarBase = mostrar;
  mostrar = function (d, f) { if (d && d.tipo === 'familia') E._famSel = d.nodo; else if (d && d.tipo === 'serie') E._famSel = d.nodo.familia; mostrarBase(d, f); };
  document.addEventListener('keydown', function (e) {
    if (e.target.closest && e.target.closest('input, select, textarea')) return;
    if (e.key === 'Escape') { if (!capaSim.hidden) return abrirSimbolos(false); if (paso >= 0) return salir(); mapa.soltar(); }
    if (paso >= 0 && e.key === 'ArrowRight') irA(paso + 1);
    if (paso >= 0 && e.key === 'ArrowLeft') irA(paso - 1);
    if (e.key === '+' || e.key === '=') mapa.acercar(1.3);
    if (e.key === '-') mapa.acercar(1 / 1.3);
  });
  document.getElementById('btn-recorrer').onclick = function () { if (paso >= 0) salir(); else empezar(); };
  btnSim.onclick = function () { abrirSimbolos(); };
  document.getElementById('mas').onclick = function () { mapa.acercar(1.35); };
  document.getElementById('menos').onclick = function () { mapa.acercar(1 / 1.35); };
  document.getElementById('encuadre').onclick = function () { mapa.encuadre(); };
  document.getElementById('png').onclick = function () { mapa.png(3000).then(function (b) { bajar(b, EN ? 'cognitive-map-of-capital.png' : 'mapa-cognitivo-del-capital.png'); di(T('mensajes.png', 'PNG de 3000 × 1920 px', 'PNG, 3000 × 1920 px')); }); };
  document.getElementById('svg').onclick = function () { bajar(new Blob([mapa.svg()], { type: 'image/svg+xml' }), EN ? 'cognitive-map-of-capital.svg' : 'mapa-cognitivo-del-capital.svg'); di(T('mensajes.svg', 'SVG vectorial descargado', 'Vector SVG downloaded')); };
})();
