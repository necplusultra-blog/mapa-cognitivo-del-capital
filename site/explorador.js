/* Explorador de las especificaciones de la tasa de ganancia de EE.UU.
   Mapa cognitivo del capital — Pablo Jiménez Cea. Licencia MIT (código), CC BY 4.0 (datos).

   Dos usos:
   1. En la portada, un elemento <div id="explorador-especificaciones"> se convierte en un selector por bifurcación:
      se elige una opción en cada decisión teórica y se dibuja la tasa de la especificación resultante
      junto a la mediana y las bandas del conjunto.
   2. En el mapa (mapa.html, en/map.html), el panel llama a Explorador.curva() al pinchar una hoja
      (una especificación) o una bifurcación (las medianas de cada opción).

   Datos: data/mapa.json (decisiones y especificaciones) y data/mapa_series.json (tasa anual en %,
   en el mismo orden), que escribe sismografo/mapa.py. Sin dependencias (SVG a mano). */
(function () {
  'use strict';
  var SCRIPT = document.currentScript;
  var BASE = SCRIPT ? SCRIPT.src.replace(/[^/]*$/, '') : '';
  var EN = /^en/.test(document.documentElement.lang);
  function L(es, en) { return EN ? en : es; }
  var NS = 'http://www.w3.org/2000/svg';
  var cache = null;

  function datos() {
    if (cache) return cache;
    var j = function (n) { return fetch(BASE + 'data/' + n).then(function (r) { if (!r.ok) throw new Error(n); return r.json(); }); };
    cache = Promise.all([window.MAPA_DATOS ? Promise.resolve(window.MAPA_DATOS) : j('mapa.json'), j('mapa_series.json')]).then(function (r) {
      var m = r[0], s = r[1];
      return { mapa: m, anios: s.anios, tasas: s.eeuu, indices: s.eeuu.map(indice) };
    });
    return cache;
  }

  /* cada especificación se divide por su propio promedio del periodo (= 100), como el abanico del sitio */
  function indice(serie) {
    var t = 0, n = 0;
    serie.forEach(function (v) { if (v != null) { t += v; n++; } });
    var m = n ? t / n : null;
    return serie.map(function (v) { return v == null || !m ? null : v / m * 100; });
  }
  function mediana(arr) {
    var a = arr.filter(function (v) { return v != null; }).sort(function (x, y) { return x - y; });
    if (!a.length) return null;
    var k = (a.length - 1) / 2;
    return (a[Math.floor(k)] + a[Math.ceil(k)]) / 2;
  }
  /* mediana por año de un grupo de especificaciones (índices de mapa.json) */
  function medianaDe(D, idx) {
    return D.anios.map(function (_, t) { return mediana(idx.map(function (i) { return D.indices[i][t]; })); });
  }

  function el(tag, at, padre) {
    var e = document.createElementNS(NS, tag);
    for (var k in at) e.setAttribute(k, at[k]);
    if (padre) padre.appendChild(e);
    return e;
  }
  var COL = ['var(--estilete, #b8203a)', 'var(--c1, #1d6d78)', 'var(--c3, #a8731a)', 'var(--c2, #6a4c9c)', 'var(--c5, #2f7a3f)'];

  /* Dibuja en el contenedor: bandas p10–p90 y p25–p75 y mediana del conjunto principal (mapa.json → bandas)
     y encima las líneas pedidas: [{v: [índice por año], n: 'etiqueta'}]. */
  function curva(cont, D, lineas, op) {
    op = op || {};
    cont.innerHTML = '';
    var W = Math.max(240, cont.clientWidth || 300), H = op.alto || Math.round(Math.min(300, Math.max(170, W * 0.5)));
    var ml = 34, mr = 8, mt = 8, mb = 22;
    var B = D.mapa.bandas, a0 = D.anios[0], a1 = D.anios[D.anios.length - 1];
    var lo = 1e9, hi = -1e9;
    B.forEach(function (b) { lo = Math.min(lo, b[1]); hi = Math.max(hi, b[5]); });
    lineas.forEach(function (l) { l.v.forEach(function (v) { if (v != null) { lo = Math.min(lo, v); hi = Math.max(hi, v); } }); });
    lo = Math.floor(lo / 10) * 10; hi = Math.ceil(hi / 10) * 10;
    var x = function (a) { return ml + (a - a0) / (a1 - a0) * (W - ml - mr); };
    var y = function (v) { return mt + (hi - v) / (hi - lo) * (H - mt - mb); };
    var svg = el('svg', { viewBox: '0 0 ' + W + ' ' + H, width: W, height: H, role: 'img', class: 'explorador-svg',
      'aria-label': op.aria || L('Tasa de ganancia de la especificación frente al conjunto', 'Rate of profit of the specification against the whole set') }, cont);
    var paso = hi - lo > 120 ? 40 : 20;
    for (var v = Math.ceil(lo / paso) * paso; v <= hi; v += paso) {
      el('line', { x1: ml, x2: W - mr, y1: y(v), y2: y(v), stroke: 'var(--reticula, #d3dbd9)', 'stroke-width': v === 100 ? 1.2 : 0.6, 'stroke-dasharray': v === 100 ? '3,3' : '' }, svg);
      el('text', { x: ml - 5, y: y(v) + 3.5, 'text-anchor': 'end', class: 'ex-eje' }, svg).textContent = v;
    }
    for (var a = Math.ceil(a0 / 10) * 10; a <= a1; a += 10) el('text', { x: x(a), y: H - 6, 'text-anchor': 'middle', class: 'ex-eje' }, svg).textContent = a;
    var area = function (i, j) {
      var d = B.map(function (b, k) { return (k ? 'L' : 'M') + x(b[0]).toFixed(1) + ',' + y(b[i]).toFixed(1); }).join('');
      return d + B.slice().reverse().map(function (b) { return 'L' + x(b[0]).toFixed(1) + ',' + y(b[j]).toFixed(1); }).join('') + 'Z';
    };
    el('path', { d: area(1, 5), fill: 'var(--tinta, #182235)', 'fill-opacity': 0.07 }, svg);
    el('path', { d: area(2, 4), fill: 'var(--tinta, #182235)', 'fill-opacity': 0.09 }, svg);
    el('path', { d: B.map(function (b, k) { return (k ? 'L' : 'M') + x(b[0]).toFixed(1) + ',' + y(b[3]).toFixed(1); }).join(''), fill: 'none', stroke: 'var(--gris, #5d6878)', 'stroke-width': 1.4 }, svg);
    lineas.forEach(function (l, i) {
      var d = '', pen = false;
      l.v.forEach(function (v, t) {
        if (v == null) { pen = false; return; }
        d += (pen ? 'L' : 'M') + x(D.anios[t]).toFixed(1) + ',' + y(v).toFixed(1); pen = true;
      });
      el('path', { d: d, fill: 'none', stroke: l.c || COL[i % COL.length], 'stroke-width': l.w || 2, 'stroke-linejoin': 'round' }, svg);
    });
    (op.quiebres || []).forEach(function (q) { el('line', { x1: x(q), x2: x(q), y1: mt, y2: H - mb, stroke: 'var(--estilete, #b8203a)', 'stroke-opacity': 0.45, 'stroke-dasharray': '2,3' }, svg); });
    var ley = document.createElement('div'); ley.className = 'ex-ley';
    var item = function (c, t, banda) { return '<span><i style="' + (banda ? 'background:' + c + ';opacity:.25;height:9px' : 'background:' + c) + '"></i>' + t + '</span>'; };
    ley.innerHTML = lineas.map(function (l, i) { return item(l.c || COL[i % COL.length], esc(l.n)); }).join('')
      + item('var(--gris, #5d6878)', L('mediana de las especificaciones', 'median of the specifications'))
      + item('var(--tinta, #182235)', L('percentiles 10–90 y 25–75', '10th–90th and 25th–75th percentiles'), true);
    cont.appendChild(ley);
    return svg;
  }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var fmt = function (v) { return v == null ? '—' : v.toFixed(1).replace('.', EN ? '.' : ',') + ' %'; };

  /* niveles (%) de una especificación en tres años de referencia */
  function niveles(D, i) {
    var fin = D.anios[D.anios.length - 1];
    return [1948, 1982, fin].map(function (a) { var t = D.anios.indexOf(a); return [a, t >= 0 ? D.tasas[i][t] : null]; });
  }

  /* ------------------------------------------------------------------ explorador de la portada */
  function montar(cont) {
    cont.innerHTML = '<p class="ex-cargando">' + L('Cargando las especificaciones…', 'Loading the specifications…') + '</p>';
    datos().then(function (D) {
      var E = D.mapa.eeuu, dims = EN && E.dims_en ? E.dims_en : E.dims, specs = E.specs;
      var inicial = specs.findIndex(function (s) { return s[0] === 'B|b|cc|neta|ppi-incl|K-todo|noutil'; });
      var actual = inicial >= 0 ? inicial : 0;
      cont.innerHTML = '';
      var form = document.createElement('div'); form.className = 'ex-selectores'; cont.appendChild(form);
      var sels = dims.map(function (dm, j) {
        var usadas = {};
        specs.forEach(function (s) { if (s[3][j] >= 0) usadas[s[3][j]] = true; });
        var lab = document.createElement('label');
        lab.innerHTML = '<span>' + esc(dm[0]) + '</span>';
        var sel = document.createElement('select');
        dm[2].forEach(function (op, k) { if (usadas[k]) { var o = document.createElement('option'); o.value = k; o.textContent = op; sel.appendChild(o); } });
        var na = document.createElement('option'); na.value = -1; na.textContent = L('no aplica', 'not applicable'); na.hidden = true; sel.appendChild(na);
        sel.addEventListener('change', function () { elegir(j, +sel.value); });
        lab.appendChild(sel); form.appendChild(lab);
        return sel;
      });
      var fig = document.createElement('div'); fig.className = 'ex-grafico'; cont.appendChild(fig);
      var info = document.createElement('div'); info.className = 'ex-info'; cont.appendChild(info);
      function elegir(j, v) {
        var cur = specs[actual][3], mejor = -1, pm = -1;
        specs.forEach(function (s, i) {
          if (s[3][j] !== v) return;
          var p = s[3].reduce(function (n, k, d) { return n + (k === cur[d] ? 1 : 0); }, 0);
          if (p > pm) { pm = p; mejor = i; }
        });
        if (mejor >= 0) actual = mejor;
        pintar();
      }
      function pintar() {
        var s = specs[actual];
        sels.forEach(function (sel, j) { sel.value = s[3][j]; sel.disabled = s[3][j] < 0; sel.parentNode.classList.toggle('na', s[3][j] < 0); });
        curva(fig, D, [{ v: D.indices[actual], n: L('esta especificación', 'this specification') }], { quiebres: s[2] });
        var nv = niveles(D, actual);
        info.innerHTML = '<div><span class="ex-lab">' + L('especificación', 'specification') + '</span> <code>' + esc(s[0]) + '</code></div>'
          + '<div><span class="ex-lab">' + L('tasa en', 'rate in') + '</span> ' + nv.map(function (x) { return x[0] + ': <b>' + fmt(x[1]) + '</b>'; }).join(' · ') + '</div>'
          + '<div><span class="ex-lab">' + L('quiebres endógenos', 'endogenous breaks') + '</span> ' + (s[2] && s[2].length ? s[2].join(' · ') : L('ninguno', 'none')) + '</div>';
      }
      pintar();
      var t; window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(pintar, 150); });
    }).catch(function () { cont.innerHTML = '<p class="ex-cargando">' + L('No se pudieron cargar las especificaciones.', 'The specifications could not be loaded.') + '</p>'; });
  }

  window.Explorador = { datos: datos, curva: curva, medianaDe: medianaDe, niveles: niveles, indice: indice, fmt: fmt };
  function auto() { var c = document.getElementById('explorador-especificaciones'); if (c) montar(c); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', auto); else auto();
})();
