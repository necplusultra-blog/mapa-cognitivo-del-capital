/* Pestaña Glosario — llena las tablas de símbolos, series y decisiones del multiverso.
   Mapa cognitivo del capital — Pablo Jiménez Cea. Licencia MIT.
   Los datos son los mismos que usa el mapa (site/data/mapa.json, que escribe sismografo/mapa.py a partir de
   sismografo/glosario.py), de modo que el glosario y la lámina no pueden diferir.
   Atajos en contenido/glosario/*.md: [[glosario simbolos]], [[glosario series]], [[glosario decisiones]].
   El idioma sale del atributo lang de la página. */
(function () {
  'use strict';
  var EN = /^en/.test(document.documentElement.lang);
  function L(es, en) { return EN ? en : es; }
  var PRE = EN ? '../' : '';
  var may = function (s) { s = String(s || ''); return s.charAt(0).toUpperCase() + s.slice(1); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  /* en la versión inglesa, los enlaces a las secciones del sitio apuntan a sus equivalentes en en/ */
  function ruta(a) { return EN ? a.replace(/^lectura\.html/, 'reading.html').replace(/^metodologia\.html/, 'methodology.html') : a; }
  var cajas = document.querySelectorAll('[data-glosario]');
  if (!cajas.length) return;
  cajas.forEach(function (c) { c.innerHTML = '<p class="nota">' + L('Cargando el glosario…', 'Loading the glossary…') + '</p>'; });

  function simbolos(D) {
    return '<div class="tablewrap"><table class="tabla-glosario"><thead><tr><th>' + L('Símbolo o expresión', 'Symbol or expression') + '</th><th>' + L('Significado', 'Meaning')
      + '</th></tr></thead><tbody>' + (D.simbolos || []).map(function (s) {
        return '<tr><td class="expr">' + esc(EN ? s[3] || s[0] : s[0]) + '</td><td>' + esc(EN ? s[2] : s[1]) + '</td></tr>';
      }).join('') + '</tbody></table></div>';
  }
  function series(D) {
    var fams = D.familias || [], total = fams.reduce(function (n, f) { return n + f.s.length; }, 0);
    var h = '<div class="glosario-buscar"><label for="glosario-filtro">' + L('Buscar una serie', 'Search for a series') + '</label>'
      + '<input id="glosario-filtro" type="search" autocomplete="off" placeholder="' + L('p. ej. K / V, tasa de plusvalor, China, kv_ramas', 'e.g. K / V, rate of surplus value, China, kv_ramas') + '">'
      + '<span class="nota" id="glosario-cuenta" aria-live="polite">' + total + L(' series', ' series') + '</span></div>'
      + '<nav class="glosario-indice" aria-label="' + L('Secciones del glosario', 'Sections of the glossary') + '">' + fams.map(function (f, i) {
        return '<a href="#glosario-f' + i + '">' + esc(EN ? f.n_en || f.n : f.n) + ' <span>' + f.s.length + '</span></a>';
      }).join('') + '</nav>';
    fams.forEach(function (f, i) {
      var g = (EN ? f.g_en : f.g) || [];
      h += '<div class="glosario-familia" id="glosario-f' + i + '"><h3>' + esc(may(EN ? f.n_en || f.n : f.n))
        + ' <a class="ir" href="' + esc(ruta(f.a)) + '">' + L('ver la sección', 'see the section') + ' →</a></h3>'
        + '<div class="tablewrap"><table class="tabla-glosario"><thead><tr><th>' + L('Serie', 'Series') + '</th><th>' + L('Expresión', 'Expression') + '</th><th>'
        + L('Qué mide', 'What it measures') + '</th><th>' + L('Columna en los datos', 'Column in the data') + '</th></tr></thead><tbody>'
        + f.s.map(function (c, j) {
          var x = g[j] || [c, '', ''];
          return '<tr data-buscar="' + esc((x[0] + ' ' + x[1] + ' ' + x[2] + ' ' + c).toLowerCase()) + '"><td>' + esc(x[0]) + '</td><td class="expr">' + esc(x[1] && x[1] !== '—' ? x[1] : '') + '</td><td>' + esc(x[2]) + '</td><td><code>' + esc(c) + '</code></td></tr>';
        }).join('') + '</tbody></table></div></div>';
    });
    return h + '<p class="nota"><a href="' + PRE + 'descargas/glosario_series.csv" download>' + L('Glosario de las series (CSV)', 'Glossary of the series (CSV)') + '</a></p>';
  }
  function decisiones(D) {
    var bloque = function (titulo, dims) {
      return '<h3>' + titulo + '</h3><div class="tablewrap"><table class="tabla-glosario"><thead><tr><th>' + L('Decisión', 'Decision') + '</th><th>' + L('Opciones', 'Options')
        + '</th><th>' + L('Corrientes asociadas', 'Associated readings') + '</th></tr></thead><tbody>' + dims.map(function (d) {
          return '<tr><td>' + esc(d[0]) + '</td><td>' + d[2].map(esc).join(' · ') + '</td><td>' + esc(d[1] || '—') + '</td></tr>';
        }).join('') + '</tbody></table></div>';
    };
    var de = D.eeuu || {}, dm = D.mundo || {};
    return bloque(L('Multiverso de EE.UU.', 'US multiverse') + ' (' + (de.specs || []).length + ')', (EN ? de.dims_en : de.dims) || [])
      + bloque(L('Multiverso mundial', 'World multiverse') + ' (' + (dm.specs || []).length + ')', (EN ? dm.dims_en || dm.dims : dm.dims) || []);
  }
  function filtrar(q) {
    q = q.trim().toLowerCase(); var n = 0;
    document.querySelectorAll('.glosario-familia').forEach(function (F) {
      var vis = 0;
      F.querySelectorAll('tr[data-buscar]').forEach(function (tr) { var si = !q || tr.dataset.buscar.indexOf(q) >= 0; tr.hidden = !si; if (si) vis++; });
      F.hidden = !vis; n += vis;
    });
    var c = document.getElementById('glosario-cuenta'); if (c) c.textContent = n + L(' series', ' series');
  }
  fetch(PRE + 'data/mapa.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }).then(function (D) {
    cajas.forEach(function (c) {
      var t = c.dataset.glosario;
      c.innerHTML = t === 'series' ? series(D) : t === 'decisiones' ? decisiones(D) : simbolos(D);
    });
    var inp = document.getElementById('glosario-filtro');
    if (inp) inp.addEventListener('input', function () { filtrar(inp.value); });
    if (location.hash) { var el = document.getElementById(location.hash.slice(1)); if (el) el.scrollIntoView(); }
  }).catch(function () {
    cajas.forEach(function (c) { c.innerHTML = '<p class="nota">' + L('No se pudo cargar el glosario. Puede descargarlo en ', 'The glossary could not be loaded. You can download it as ') + '<a href="' + PRE + 'descargas/glosario_series.csv">CSV</a>.</p>'; });
  });
})();
