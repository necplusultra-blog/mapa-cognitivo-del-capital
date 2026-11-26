/* Pestaña Mapa — interfaz de la lámina: panel lateral, símbolos y recorrido guiado.
   Mapa cognitivo del capital — Pablo Jiménez Cea. Licencia MIT.
   La usan mapa.html y en/map.html; el idioma sale del atributo lang de la página.
   Necesita mapa-cognitivo.js (motor) y explorador.js (curvas del panel). */
(function () {
  'use strict';
  var EN = /^en/.test(document.documentElement.lang);
  function L(es, en) { return EN ? en : es; }
  var PRE = EN ? '../' : '';
  var panel = document.getElementById('panel'), estado = document.getElementById('estado');
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var di = function (t) { estado.textContent = t; clearTimeout(di.t); di.t = setTimeout(function () { estado.textContent = ''; }, 4000); };
  var mapa = null, E = null;
  var TIPOS = EN ? { hoja: 'specification', decision: 'fork', familia: 'section of the site', serie: 'series', estacion: 'station', empalme: 'splice' }
                 : { hoja: 'especificación', decision: 'bifurcación', familia: 'sección del sitio', serie: 'serie', estacion: 'estación', empalme: 'empalme' };

  /* ------------------------------------------------------------------ panel */
  function sparq(q) {
    var a0 = 1948, a1 = 2025, w = 320, h = 56, mx = Math.max.apply(null, [1].concat(Object.values(q))), barras = '';
    for (var a = a0; a <= a1; a++) { var v = q[a] || 0; if (!v) continue; var x = (a - a0) / (a1 - a0) * (w - 4) + 2, hh = Math.max(1.5, v / mx * (h - 16));
      barras += '<rect x="' + x.toFixed(1) + '" y="' + (h - 12 - hh).toFixed(1) + '" width="2.6" height="' + hh.toFixed(1) + '" rx="1" fill="#ff5c7a"/>'; }
    var ejes = [1950, 1970, 1990, 2010].map(function (a) { var x = (a - a0) / (a1 - a0) * (w - 4) + 2; return '<text x="' + x + '" y="' + (h - 1) + '" font-size="8" fill="#6b68a0" text-anchor="middle">' + a + '</text>'; }).join('');
    return '<svg class="sparq" viewBox="0 0 ' + w + ' ' + h + '" preserveAspectRatio="none" role="img" aria-label="' + L('Quiebres por año', 'Breaks per year') + '"><line x1="0" x2="' + w + '" y1="' + (h - 12) + '" y2="' + (h - 12) + '" stroke="#24263a"/>' + barras + ejes + '</svg>';
  }
  function miniSimbolos() {
    var S = (E.D.simbolos || []).slice(0, 7);
    return '<div class="mini-simbolos">' + S.map(function (s) { return '<b>' + esc(EN ? s[3] || s[0] : s[0]) + '</b><span>' + esc(EN ? s[2] : s[1]) + '</span>'; }).join('') + '</div>'
      + '<button class="boton-texto" data-simbolos>' + L('Todos los símbolos', 'All symbols') + '</button>';
  }
  function inicio() {
    var m = E.D.meta || {};
    var claves = E.nodos.filter(function (n) { return n.clave; }).sort(function (a, b) { return a.cod.localeCompare(b.cod); });
    panel.innerHTML = '<div class="cod">' + L('índice de la lámina', 'index of the plate') + '</div><h2>' + L('Cómo leer el mapa', 'How to read the map') + '</h2>'
      + '<div class="sec cifras"><div><b>' + E.eeuu.hojas.length + '</b><span>' + L('especificaciones EE.UU.', 'US specifications') + '</span></div><div><b>' + E.mundo.hojas.length + '</b><span>' + L('especificaciones mundiales', 'world specifications') + '</span></div><div><b>' + E.familias.reduce(function (s, f) { return s + f.series.length; }, 0) + '</b><span>' + L('series publicadas', 'published series') + '</span></div></div>'
      + '<div class="sec"><p>' + L('La lámina se lee en tres regiones. El <b>eje</b> horizontal expone, de izquierda a derecha, las categorías del capital (01–05). Sobre él, a la izquierda, el <b>multiverso de EE.UU.</b> (A, violeta); a la derecha, el <b>mundial</b> (B, cian): cada bifurcación es una decisión teórica explícita y cada hoja, una especificación publicada. Abajo, el <b>registro</b> (C). Los puntos coral son quiebres de tendencia. ¿Primera vez? Pulse <b>Recorrer</b>.',
        'The plate is read in three regions. The horizontal <b>axis</b> sets out, from left to right, the categories of capital (01–05). Above it, on the left, the <b>US multiverse</b> (A, violet); on the right, the <b>world</b> one (B, cyan): each fork is an explicit theoretical decision and each leaf a published specification. Below, the <b>record</b> (C). The coral dots are breaks in trend. First time? Press <b>Tour</b>.') + '</p></div>'
      + '<div class="sec"><div class="lab">' + L('símbolos frecuentes', 'common symbols') + '</div>' + miniSimbolos() + '</div>'
      + '<div class="sec"><div class="lab">' + L('nodos clave', 'key nodes') + '</div><div class="lista-clave">' + claves.map(function (n) { return '<button data-i="' + E.nodos.indexOf(n) + '"><span>' + esc(n.cod) + '</span>' + esc(n.clave) + '</button>'; }).join('') + '</div></div>'
      + '<div class="sec"><div class="lab">' + L('leyenda', 'key') + '</div><div class="ley">'
      + '<svg width="30" height="10"><path d="M0 5H30" stroke="#f6f4ff" stroke-width="1.6"/></svg><span>' + L('eje categorial (01–05)', 'categorial axis (01–05)') + '</span>'
      + '<svg width="30" height="12"><path d="M0 11C10 11 10 2 30 2" stroke="#9d86ff" fill="none"/></svg><span>' + L('decisión teórica, EE.UU.', 'theoretical decision, US') + '</span>'
      + '<svg width="30" height="12"><path d="M0 11C10 11 10 2 30 2" stroke="#3fc8e0" fill="none"/></svg><span>' + L('decisión teórica, mundo', 'theoretical decision, world') + '</span>'
      + '<svg width="30" height="10"><path d="M0 5H30" stroke="#c9cde6" stroke-opacity=".7"/><circle cx="30" cy="5" r="2" fill="#e6e9ff"/></svg><span>' + L('serie publicada en una sección del sitio', 'series published in a section of the site') + '</span>'
      + '<svg width="30" height="10"><path d="M0 5H30" stroke="#9f8cff" stroke-opacity=".5"/><circle cx="12" cy="5" r="2" fill="#ff5c7a"/><circle cx="22" cy="5" r="2" fill="#ff5c7a"/></svg><span>' + L('una especificación y sus quiebres', 'a specification and its breaks') + '</span>'
      + '<svg width="30" height="10"><path d="M0 5H30" stroke="#7ddcff" stroke-dasharray="5 4"/></svg><span>' + L('empalme estadístico', 'statistical splice') + '</span>'
      + '<svg width="30" height="10"><path d="M0 5H30" stroke="#3d3f6e" stroke-dasharray="1 4"/></svg><span>' + L('guía: un anillo por nivel de decisión', 'guide: one ring per level of decision') + '</span>'
      + '</div></div>'
      + '<div class="sec"><div class="lab">' + L('rueda o pellizco: zoom · arrastrar: mover · clic: fijar · Esc: soltar · al acercarse aparecen las expresiones de cada serie', 'wheel or pinch: zoom · drag: pan · click: pin · Esc: release · zoom in to see the expression of each series') + '</div>'
      + '<div class="sub">' + L('Datos: ', 'Data: ') + esc(m.actualizado || '—') + '. ' + L('Topología real; la geometría sale de una semilla fija', 'Real topology; the geometry comes from a fixed seed') + ' (' + MapaCognitivo.SEED + ').</div></div>';
  }
  function mostrar(d, fijado) {
    if (!d) return inicio();
    var h = fijado ? '<div class="fijado"><span>' + L('Fijado', 'Pinned') + '</span><button class="soltar" data-soltar>' + L('Soltar · Esc', 'Release · Esc') + '</button></div>' : '';
    h += '<div class="cod">' + esc(d.cod ? d.cod + ' · ' + (TIPOS[d.tipo] || d.tipo) : (TIPOS[d.tipo] || d.tipo)) + (d.arbol ? ' · ' + esc(d.arbol) : '') + '</div><h2' + (d.tipo === 'hoja' ? ' class="id"' : '') + '>' + esc(d.titulo) + '</h2><div class="sub">' + esc(d.sub || '') + '</div>';
    if (d.expresion) h += '<div class="formula"><small>' + L('expresión', 'expression') + '</small>' + esc(d.expresion) + '</div>';
    if (d.texto) h += '<div class="sec"><p>' + esc(d.texto) + '</p></div>';
    if (d.columna) h += '<div class="sec"><div class="lab">' + L('columna en los datos', 'column in the data') + '</div><span class="sub"><code>' + esc(d.columna) + '</code> · <a href="' + PRE + 'descargas/glosario_series.csv" download>' + L('glosario de las series (CSV)', 'glossary of the series (CSV)') + '</a></span></div>';
    if (d.opciones) {
      var tot = d.opciones.reduce(function (s, o) { return s + o[1]; }, 0);
      h += '<div class="sec"><div class="lab">' + L('decisión teórica explícita', 'explicit theoretical decision') + ' · ' + esc(d.decision) + (d.posicion ? ' · ' + esc(d.posicion) : '') + '</div><ul>' + d.opciones.map(function (o) { return '<li class="op"><span>' + esc(o[0]) + '</span><span>' + o[1] + L(' esp.', ' spec.') + '</span><span class="barra-op"><i style="width:' + (o[1] / tot * 100).toFixed(1) + '%"></i></span></li>'; }).join('') + '</ul></div>';
    }
    if (d.decisiones) h += '<div class="sec"><div class="lab">' + L('decisiones de esta especificación', 'decisions of this specification') + '</div><dl class="dec">' + d.decisiones.map(function (x) { return '<dt>' + esc(x[0]) + '</dt><dd>' + esc(x[1]) + '</dd>'; }).join('') + '</dl></div>';
    if (d.spec != null || d.grupos || (d.idx && d.idx.length > 1)) h += '<div class="sec"><div class="lab">' + (d.spec != null ? L('tasa de esta especificación frente al multiverso', 'rate of this specification against the multiverse') : d.grupos ? L('mediana de cada opción frente al multiverso', 'median of each option against the multiverse') : L('mediana de esta rama frente al multiverso', 'median of this branch against the multiverse')) + ' · ' + L('100 = promedio del periodo', '100 = period average') + '</div><div class="ex-curva" id="ex-curva"></div><div class="sub" id="ex-niveles"></div></div>';
    if (d.anios) h += '<div class="sec"><div class="lab">' + L('quiebres endógenos detectados', 'endogenous breaks detected') + '</div>' + (d.anios.length ? d.anios.map(function (a) { return '<span class="chip">' + a + '</span>'; }).join('') : '<span class="sub">' + L('ninguno', 'none') + '</span>') + '</div>';
    if (d.quiebres && d.n > 1) h += '<div class="sec"><div class="lab">' + L('quiebres por año en las ', 'breaks per year in the ') + d.n + L(' especificaciones de esta rama', ' specifications of this branch') + '</div>' + sparq(d.quiebres) + '</div>';
    if (d.ruta && d.ruta.length && !d.decisiones) h += '<div class="sec"><div class="lab">' + L('decisiones tomadas hasta aquí', 'decisions taken up to here') + '</div><dl class="dec">' + d.ruta.map(function (x) { return '<dt>' + esc(x[0]) + '</dt><dd>' + esc(x[1]) + '</dd>'; }).join('') + '</dl></div>';
    if (d.series) {
      var gl = d.glosas || [];
      h += '<div class="sec"><div class="lab">' + L('series de esta sección · nombre y expresión', 'series of this section · name and expression') + '</div>' + d.series.map(function (s, i) {
        var g = gl[i] || [s, '', ''];
        return '<button class="serie-it" data-serie="' + i + '"><b>' + esc(g[1] && g[1] !== '—' ? g[1] : s) + '</b><span>' + esc(g[0]) + '</span></button>';
      }).join('') + '</div>';
    }
    if (d.empalmes) h += '<div class="sec"><div class="lab">' + L('factores de empalme (meta.json)', 'splice factors (meta.json)') + '</div><dl class="dec">' + d.empalmes.map(function (e) { return '<dt>' + esc(e[0]) + '</dt><dd>× ' + esc(e[1]) + '</dd>'; }).join('') + '</dl></div>';
    if (d.enlaces) h += '<div class="sec enl">' + d.enlaces.map(function (e) { return '<a href="' + esc(e[0]) + '">' + esc(e[1]) + ' →</a>'; }).join('') + '</div>';
    panel.innerHTML = h;
    panel.scrollTop = 0;
    curvaPanel(d);
  }
  /* curva del explorador: hoja → su tasa; bifurcación → mediana de cada opción; rama → su mediana */
  var COLORES = ['#b9a5ff', '#3fc8e0', '#ffcf6b', '#ff8a9c', '#8fe3a1'], turno = 0;
  var TABLA = PRE + (EN ? 'descargas/eeuu_multiverse_table_en.csv' : 'descargas/eeuu_multiverso_tabla.csv');
  function curvaPanel(d) {
    var caja = document.getElementById('ex-curva'); if (!caja || !window.Explorador) return;
    var t = ++turno;
    Explorador.datos().then(function (D) {
      if (t !== turno) return;
      var lineas, q = null;
      if (d.spec != null) { lineas = [{ v: D.indices[d.spec], n: L('esta especificación', 'this specification'), c: COLORES[0] }]; q = d.anios; }
      else if (d.grupos) lineas = d.grupos.slice(0, 5).map(function (g, i) { return { v: Explorador.medianaDe(D, g[1]), n: g[0] + ' (' + g[1].length + ')', c: COLORES[i] }; });
      else lineas = [{ v: Explorador.medianaDe(D, d.idx), n: L('mediana de la rama', 'median of the branch'), c: COLORES[0] }];
      Explorador.curva(caja, D, lineas, { alto: 190, quiebres: q });
      var nv = document.getElementById('ex-niveles');
      if (nv) nv.innerHTML = (d.spec != null ? L('Tasa', 'Rate') + ': ' + Explorador.niveles(D, d.spec).map(function (x) { return x[0] + ' <b>' + Explorador.fmt(x[1]) + '</b>'; }).join(' · ') + '. ' : '')
        + '<a href="' + TABLA + '" download>' + L('Tabla de las especificaciones (CSV)', 'Table of the specifications (CSV)') + '</a>';
    }).catch(function () { caja.textContent = L('No se pudieron cargar las series.', 'The series could not be loaded.'); });
  }

  /* ------------------------------------------------------------------ símbolos */
  var capaSim = document.getElementById('simbolos'), btnSim = document.getElementById('btn-simbolos');
  function abrirSimbolos(si) {
    if (si === undefined) si = capaSim.hidden;
    if (si && !capaSim.dataset.listo) {
      var S = E.D.simbolos || [];
      var series = [];
      E.familias.forEach(function (F) { F.glosa.forEach(function (g, i) { if (g[1] && /[\/=·−+Σ×]/.test(g[1])) series.push([g[1], g[0], F.nombre, F, i]); }); });
      capaSim.innerHTML = '<div class="cab"><div><h2>' + L('Símbolos y expresiones', 'Symbols and expressions') + '</h2><p>' + L('Qué significa cada letra y cada cociente que aparece en la lámina. Al acercarse al mapa, cada serie muestra su expresión.', 'What each letter and each ratio on the plate means. Zoom into the map and each series shows its expression.') + '</p></div><button class="cerrar" data-cerrar>' + L('Cerrar · Esc', 'Close · Esc') + '</button></div>'
        + '<div class="rejilla">' + S.map(function (s) { return '<div class="simbolo"><b>' + esc(EN ? s[3] || s[0] : s[0]) + '</b><span>' + esc(EN ? s[2] : s[1]) + '</span></div>'; }).join('') + '</div>'
        + '<h3>' + L('Expresiones de las series publicadas', 'Expressions of the published series') + '</h3><div class="rejilla">'
        + series.map(function (s, k) { return '<button class="simbolo serie-it" style="display:block" data-sim="' + k + '"><b>' + esc(s[0]) + '</b><span>' + esc(s[1]) + ' · ' + esc(s[2]) + '</span></button>'; }).join('') + '</div>'
        + '<p class="sub" style="margin-top:16px"><a href="' + PRE + 'descargas/glosario_series.csv" download>' + L('Glosario completo de las series (CSV)', 'Full glossary of the series (CSV)') + '</a></p>';
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
  function construirPasos() { return [
    { t: L('Una lámina, tres regiones', 'One plate, three regions'), z: 1, p: function () { return [800, 450]; },
      x: L('El mapa reúne en una sola imagen todo lo que calcula el sitio. <b>A</b> (violeta): el multiverso de la tasa de ganancia de EE.UU. <b>B</b> (cian): el multiverso mundial. <b>C</b>: el registro del abanico en el tiempo. Todo cuelga de un eje horizontal.',
           'The map gathers everything the site calculates into one image. <b>A</b> (violet): the multiverse of the US rate of profit. <b>B</b> (cyan): the world multiverse. <b>C</b>: the record of the fan over time. Everything hangs from a horizontal axis.') },
    { t: L('01–05 · El eje categorial', '01–05 · The categorial axis'), z: 1.5, n: function () { return E.estaciones[0].nodo; }, p: function () { return [560, 470]; },
      x: L('El eje se lee de izquierda a derecha: <b>lógica del capital</b>, plusvalor y ganancia, fuerzas productivas, tiempo disponible y <b>límites inmanentes</b>. La categoría va primero; las series son su manifestación fenoménica en precios, no su demostración.',
           'The axis reads from left to right: <b>logic of capital</b>, surplus value and profit, productive forces, disposable time and <b>immanent limits</b>. The category comes first; the series are its phenomenal manifestation in prices, not its demonstration.') },
    { t: L('02 · Plusvalor y ganancia', '02 · Surplus value and profit'), z: 2.4, n: function () { return fam('index.html#masa-tasa'); },
      x: L('Cada abanico blanco es una sección del sitio y cada punto, una serie publicada. Aquí, la masa y la tasa de plusvalor. El panel de la derecha da el nombre y la <b>expresión</b> de cada serie.',
           'Each white fan is a section of the site and each dot a published series. Here, the mass and rate of surplus value. The panel on the right gives the name and <b>expression</b> of each series.') },
    { t: L('Leer una expresión: K / V', 'Reading an expression: K / V'), z: 3.4, n: function () { return serieDe('index.html#masa-tasa', 'kv_ramas'); },
      x: L('<code>K / V</code> es la composición de valor del capital: cuánto capital fijo (<code>K</code>) se adelanta por cada dólar de salarios productivos (<code>V</code>). <code>e = pv / v</code> es la tasa de plusvalor. El botón <b>Símbolos</b> reúne todas las letras de la lámina.',
           '<code>K / V</code> is the value composition of capital: how much fixed capital (<code>K</code>) is advanced per dollar of productive wages (<code>V</code>). <code>e = pv / v</code> is the rate of surplus value. The <b>Symbols</b> button gathers every letter on the plate.') },
    { t: L('#06 · El multiverso de especificaciones', '#06 · The multiverse of specifications'), z: 1.9, n: function () { return E.eeuu.raiz; }, p: function () { return [520, 300]; },
      x: L('No hay una sola tasa de ganancia: cada bifurcación es una decisión teórica explícita (qué sector, qué cuenta como plusvalor, cómo se valora el capital…). Los anillos punteados marcan los niveles de decisión; las ' + E.eeuu.hojas.length + ' hojas, las especificaciones publicadas.',
           'There is no single rate of profit: each fork is an explicit theoretical decision (which sector, what counts as surplus value, how capital is valued…). The dotted rings mark the levels of decision; the ' + E.eeuu.hojas.length + ' leaves, the published specifications.') },
    { t: L('#07 · Qué cuenta como plusvalor', '#07 · What counts as surplus value'), z: 2.6, n: function () { return nodoCod('#07'); },
      x: L('Esta bifurcación decide qué trabajo es productivo. El panel muestra la mediana de cada opción frente al abanico completo: se ve si la decisión cambia el <b>movimiento</b> de la tasa o sólo su nivel.',
           'This fork decides which labour is productive. The panel shows the median of each option against the whole fan: you can see whether the decision changes the <b>movement</b> of the rate or only its level.') },
    { t: L('Una especificación', 'One specification'), z: 3, n: hojaEj,
      x: L('Cada hoja es una medición completa, con todas sus decisiones. Ésta es el plusvalor ampliado por ramas a costo corriente. El panel dibuja su curva sobre el abanico y sus niveles en 1948, 1982 y el último año.',
           'Each leaf is a complete measurement, with all its decisions. This one is extended surplus value by industry at current cost. The panel draws its curve over the fan and its levels in 1948, 1982 and the latest year.') },
    { t: L('El anillo del tiempo', 'The ring of time'), z: 2.1, n: hojaEj, p: function () { return [520, 120]; },
      x: L('Cada radio prolonga una especificación a través del tiempo, de 1948 (dentro) a hoy (fuera). Los puntos <b>coral</b> son sus quiebres de tendencia. Donde los puntos de muchas especificaciones se alinean en un arco, el quiebre resiste las decisiones teóricas.',
           'Each spoke extends a specification through time, from 1948 (inside) to today (outside). The <b>coral</b> dots are its breaks in trend. Where the dots of many specifications line up in an arc, the break withstands the theoretical decisions.') },
    { t: L('#08 · Empalmes estadísticos', '#08 · Statistical splices'), z: 2.2, n: function () { return E.empalme; },
      x: L('Las series oficiales cambian de clasificación industrial (SIC → NAICS). Los arcos discontinuos marcan esos años; cada empalme usa un factor explícito, publicado en la metodología.',
           'The official series change industrial classification (SIC → NAICS). The dashed arcs mark those years; each splice uses an explicit factor, published in the methodology.') },
    { t: L('03–04 · Fuerzas productivas y tiempo disponible', '03–04 · Productive forces and disposable time'), z: 1.9, n: function () { return E.estaciones[2].nodo; }, p: function () { return [1010, 470]; },
      x: L('Arriba y abajo del eje, las series del tiempo de trabajo: horas necesarias y de plustrabajo, valor nuevo por hora, minutos productivos por habitante. Registran la medida del valor y el tiempo que la productividad libera.',
           'Above and below the axis, the series of labour time: necessary and surplus-labour hours, new value per hour, productive minutes per inhabitant. They record the measure of value and the time that productivity frees.') },
    { t: L('B · El multiverso mundial', 'B · The world multiverse'), z: 2, n: function () { return E.mundo.raiz; }, p: function () { return [1380, 600]; },
      x: L('A la derecha, la tasa de ganancia mundial con la Penn World Table: ' + E.mundo.hojas.length + ' especificaciones (medida, ponderación, con o sin China, panel). Los trazos finos son los países que entran en cada una.',
           'On the right, the world rate of profit from the Penn World Table: ' + E.mundo.hojas.length + ' specifications (measure, weighting, with or without China, panel). The fine strokes are the countries in each.') },
    { t: L('C · El registro', 'C · The record'), z: 1.6, p: function () { return [800, 770]; },
      x: L('Abajo, el abanico de EE.UU. en el tiempo: bandas de los percentiles 10–90 (100 = promedio del periodo) y, en barras coral, cuántas especificaciones registran un quiebre cada año. Es el sismograma de la lámina.',
           'Below, the US fan over time: bands of the 10th–90th percentiles (100 = period average) and, in coral bars, how many specifications record a break each year. It is the seismogram of the plate.') },
    { t: L('Ahora, explore', 'Now, explore'), z: 1, p: function () { return [800, 450]; },
      x: L('Pinche cualquier nodo para fijarlo; acérquese para leer las expresiones de cada serie. En la portada, el <b>explorador</b> permite elegir una opción en cada bifurcación y ver la curva resultante.',
           'Click any node to pin it; zoom in to read the expression of each series. On the home page, the <b>explorer</b> lets you choose an option at each fork and see the resulting curve.') }
  ]; }
  function pintarGuia() {
    var P = PASOS[paso];
    guia.innerHTML = '<div class="cab"><span>' + L('Recorrido', 'Tour') + ' · ' + ('0' + (paso + 1)).slice(-2) + ' / ' + ('0' + PASOS.length).slice(-2) + '</span><button data-g="salir" aria-label="' + L('Salir del recorrido', 'Exit the tour') + '">✕</button></div>'
      + '<div class="pasos">' + PASOS.map(function (_, i) { return '<i class="' + (i < paso ? 'hecho' : i === paso ? 'ahora' : '') + '"></i>'; }).join('') + '</div>'
      + '<h3>' + P.t + '</h3><p>' + P.x + '</p>'
      + '<div class="ctl"><button data-g="ant"' + (paso ? '' : ' disabled') + '>‹ ' + L('Anterior', 'Back') + '</button><button data-g="auto" aria-pressed="' + auto + '">' + (auto ? L('Pausa', 'Pause') : L('Reproducir', 'Play')) + '</button><button class="sig" data-g="sig">' + (paso < PASOS.length - 1 ? L('Siguiente', 'Next') + ' ›' : L('Terminar', 'Finish')) + '</button></div>';
  }
  function irA(i) {
    if (i < 0) i = 0;
    if (i >= PASOS.length) return salir();
    paso = i; var P = PASOS[i], n = P.n ? P.n() : null, p = P.p ? P.p() : n ? [n.x, n.y] : [800, 450];
    /* en pantallas anchas, el foco se corre hacia arriba a la derecha para que la tarjeta del recorrido no lo tape */
    if (window.innerWidth >= 900 && P.z > 1) { var u = (document.getElementById('lamina').clientWidth / 1600) * P.z; p = [p[0] - 170 / u, p[1] + 90 / u]; }
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
    mapa.soltar(); mapa.volar(800, 450, 1, 1200);
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
    if (guardar) { guardar.save({ filename: nombre, data: blob }).catch(function () { di(L('Descarga cancelada', 'Download cancelled')); }); return; }
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
  document.getElementById('png').onclick = function () { mapa.png(3200).then(function (b) { bajar(b, EN ? 'cognitive-map-of-capital.png' : 'mapa-cognitivo-del-capital.png'); di(L('PNG de 3200 × 1800 px', 'PNG, 3200 × 1800 px')); }); };
  document.getElementById('svg').onclick = function () { bajar(new Blob([mapa.svg()], { type: 'image/svg+xml' }), EN ? 'cognitive-map-of-capital.svg' : 'mapa-cognitivo-del-capital.svg'); di(L('SVG vectorial descargado', 'Vector SVG downloaded')); };
})();
