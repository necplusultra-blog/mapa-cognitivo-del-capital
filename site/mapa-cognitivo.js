/* Mapa cognitivo del capital — visualización central del sitio.
 *
 * Dos usos con el mismo motor:
 *   - fondo de página:  etiqueta script con src="mapa-cognitivo.js", data-modo="fondo" y defer
 *   - pestaña Mapa:     MapaCognitivo.montar(contenedor, {modo: 'mapa', alSeleccionar: fn})
 *
 * La topología es la del proyecto (site/data/mapa.json, que escribe sismografo/mapa.py): el árbol de EE.UU.
 * es el multiverso efectivo de especificaciones, cada bifurcación es una decisión de metodología §5, los
 * puntos rojos del anillo son los quiebres endógenos de cada especificación y el registro inferior son las
 * bandas p10–p90 y el número de quiebres por año. Sólo la geometría (curvatura, desfases) sale de una semilla
 * fija, de modo que la lámina es reproducible. La textura de las trazas sísmicas es ruido determinista
 * modulado por el número real de quiebres de cada año: es atmósfera, no dato.
 * Sin dependencias.
 */
(function (global) {
  'use strict';
  var W = 1600, H = 900, SEED = 1867, VERSION = 'lámina 1.0';
  var EJE_Y = 470;

  function mulberry(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function ejeY(x) { var t = (x - 40) / 1520; return EJE_Y + Math.sin(t * 5.2 + 0.4) * 9 + Math.sin(t * 15) * 3; }
  function polar(cx, cy, r, a) { return [cx + Math.cos(a) * r, cy + Math.sin(a) * r]; }
  var RAD = Math.PI / 180;

  /* Estaciones del eje: orden de exposición de las categorías. Textos breves: lo que muestra el sitio es
     manifestación fenoménica de la determinación categorial, no su demostración. */
  var ESTACIONES = [
    { k: 'logica_del_capital', x: 120, a: 'lectura.html#estatuto', c: 'K.01',
      t: 'El valor que se valoriza como sujeto de la mediación social. La categoría se expone primero; las series del sitio son su manifestación fenoménica en precios, no su demostración.' },
    { k: 'plusvalor_y_ganancia', x: 520, a: 'index.html#masa-tasa', c: 'K.02',
      t: 'Masa y tasa de plusvalor y de ganancia. Ninguna cuenta nacional las publica: se reconstruyen reclasificando excedente y remuneración según decisiones explícitas, cada una visible como bifurcación del árbol superior.' },
    { k: 'fuerzas_productivas', x: 900, a: 'index.html#fuerzas', c: 'K.03',
      t: 'Desarrollo de las fuerzas productivas: valor nuevo por hora, tiempo necesario y plustrabajo, en EE.UU. y en el mundo.' },
    { k: 'tiempo_disponible', x: 1110, a: 'lectura.html#tiempo-disponible', c: 'K.04',
      t: 'Tiempo de trabajo y tiempo disponible: la medida del valor frente a la riqueza que ya no cabe en ella. Las horas registran la medida; el tiempo liberado registra su contradicción.' },
    { k: 'limites_inmanentes', x: 1380, a: 'lectura.html#asintota', c: 'K.05',
      t: 'Hipótesis del capitalismo limítrofe y sus contratendencias. Lo que el sitio puede mostrar es si una tendencia aparece y bajo qué decisiones, a escala de EE.UU. y del mundo; no mide una distancia a un tope.' }
  ];
  /* Abanicos de series de cada sección del sitio: ángulo (grados, positivo hacia abajo) y radio desde su estación. */
  var ABANICOS = {
    'index.html#masa-tasa': [118, 150], 'index.html#replicacion': [92, 196], 'index.html#trimestral': [64, 128],
    'index.html#fuerzas': [96, 176], 'index.html#tiempo': [-74, 196], 'index.html#horas-mundo': [-108, 258],
    'index.html#contratendencias': [-90, 236], 'index.html#transformacion': [-56, 176], 'index.html#ia': [-140, 160],
    'index.html#mundo': [-26, 150]
  };

  /* ---------------------------------------------------------------- escena (coordenadas de lámina) */
  function construirEscena(D) {
    var R = mulberry(SEED), rr = function (a, b) { return a + (b - a) * R(); };
    var capas = {}, orden = [], nodos = [], etiquetas = [];
    function capa(id, tipo, z) { if (!capas[id]) { capas[id] = { id: id, tipo: tipo, z: z, g: [] }; orden.push(capas[id]); } return capas[id]; }
    function curva(id, z, seg) { capa(id, 's', z).g.push(seg); }
    function bez(p, c) {
      var rm0 = p.r + (c.r - p.r) * 0.52;
      var a = polar(p.cx, p.cy, p.r, p.a), b = polar(p.cx, p.cy, rm0, p.a), d = polar(p.cx, p.cy, rm0, c.a), e = polar(p.cx, p.cy, c.r, c.a);
      return ['c', a[0], a[1], b[0], b[1], d[0], d[1], e[0], e[1]];
    }

    /* ---- registro sismográfico (inferior) */
    var Y0 = 1948, Y1 = 2025, SX0 = 60, SX1 = 1540;
    function xa(y) { return SX0 + (y - Y0) / (Y1 - Y0) * (SX1 - SX0); }
    var Q = {}, qmax = 1; (D.quiebres || []).forEach(function (q) { Q[q[0]] = q[1]; if (q[1] > qmax) qmax = q[1]; });
    function qInterp(x) { var y = Y0 + (x - SX0) / (SX1 - SX0) * (Y1 - Y0), a = Math.floor(y), f = y - a; return ((Q[a] || 0) * (1 - f) + (Q[a + 1] || 0) * f) / qmax; }
    for (var t = 0; t < 8; t++) {
      var y0 = 648 + t * 30, g = rr(0.45, 1.15), pts = [];
      for (var x = SX0 - 30; x <= SX1 + 30; x += 2) {
        var env = 0.6 + 15 * Math.pow(qInterp(Math.max(SX0, Math.min(SX1, x))), 1.3) * g;
        pts.push([x, y0 + (R() - 0.5) * 2 * env * (0.55 + 0.45 * Math.sin(x * 0.19 + t * 1.7))]);
      }
      curva('sis:traza', 2, ['p', pts]);
    }
    var B = D.bandas || [];
    function yb(v) { return 800 - (v - 115) * 1.15; }
    if (B.length) {
      var p90 = B.map(function (b) { return [xa(b[0]), yb(b[5])]; }), p10 = B.map(function (b) { return [xa(b[0]), yb(b[1])]; }).reverse();
      var p75 = B.map(function (b) { return [xa(b[0]), yb(b[4])]; }), p25 = B.map(function (b) { return [xa(b[0]), yb(b[2])]; }).reverse();
      capa('sis:banda90', 'f', 3).g.push(['p', p90.concat(p10)]);
      capa('sis:banda50', 'f', 3).g.push(['p', p75.concat(p25)]);
      curva('sis:p50', 4, ['p', B.map(function (b) { return [xa(b[0]), yb(b[3])]; })]);
    }
    var picos = [];
    (D.quiebres || []).forEach(function (q) { if (q[1] > 0) { curva('sis:pico', 4, ['l', xa(q[0]), 872, xa(q[0]), 872 - q[1] / qmax * 74]); picos.push(q); } });
    curva('sis:regla', 4, ['l', SX0, 872, SX1, 872]);
    for (var yy = Y0; yy <= Y1; yy++) curva('sis:regla', 4, ['l', xa(yy), 872, xa(yy), 872 + (yy % 10 === 0 ? 6 : 2.5)]);
    for (yy = 1950; yy <= 2020; yy += 10) capa('sis:txt', 't', 5).g.push(['t', xa(yy), 889, String(yy), 8.5, 'center']);
    picos.sort(function (a, b) { return b[1] - a[1]; }).slice(0, 5).forEach(function (q) { capa('sis:pico:txt', 't', 5).g.push(['t', xa(q[0]), 872 - q[1] / qmax * 74 - 5, String(q[0]), 8, 'center']); });
    capa('sis:txt', 't', 5).g.push(['t', SX0, 640, 'registro · multiverso EE.UU., percentiles 10–90 (100 = promedio del periodo) · especificaciones con quiebre por año', 8.5, 'left']);

    /* ---- eje categorial */
    var ejePts = []; for (x = 30; x <= 1570; x += 4) ejePts.push([x, ejeY(x)]);
    ['eje:halo', 'eje:medio', 'eje:luz', 'eje:nucleo'].forEach(function (id, i) { curva(id, 20 + i, ['p', ejePts]); });
    ESTACIONES.forEach(function (e, i) {
      e.y = ejeY(e.x);
      var n = { tipo: 'estacion', x: e.x, y: e.y, est: i, clave: e.k, cod: e.c, peso: 3, hijos: [] };
      nodos.push(n); e.nodo = n;
    });

    /* ---- árbol radial genérico (multiverso EE.UU. y mundial) */
    function arbolRadial(def, cfg) {
      var hojas = [], todos = [];
      function rec(n, prof, padre, camino) {
        var N = { tipo: n.s ? 'hoja' : 'decision', prof: prof, padre: padre, hijos: [], dim: n.d, opt: n.o, camino: camino, arbol: cfg.nombre, peso: n.s ? 1 : 1.4 };
        todos.push(N);
        if (n.s) { N.spec = n.s[0]; hojas.push(N); }
        else n.h.forEach(function (h, j) { N.hijos.push(rec(h, prof + 1, N, camino.concat(j))); });
        return N;
      }
      var raiz = rec(def.arbol, 0, null, []);
      var pos = 0, prev = null;
      hojas.forEach(function (h) {
        if (prev) { var k = 0; while (k < h.camino.length && h.camino[k] === prev.camino[k]) k++; pos += 1 + (k === 0 ? 3.2 : k === 1 ? 1.5 : k === 2 ? 0.55 : 0); }
        h.t = pos; prev = h;
      });
      var T = pos || 1;
      function colocar(N) {
        if (N.hijos.length) { N.hijos.forEach(colocar); N.a = (N.hijos[0].a + N.hijos[N.hijos.length - 1].a) / 2; N.n = N.hijos.reduce(function (s, c) { return s + c.n; }, 0); N.r = cfg.r0 + N.prof * cfg.dr + (N.prof ? rr(-4, 4) : 0); }
        else { N.a = cfg.a0 + (cfg.a1 - cfg.a0) * N.t / T; N.n = 1; N.r = cfg.rh; }
        N.cx = cfg.cx; N.cy = cfg.cy;
        var p = polar(cfg.cx, cfg.cy, N.r, N.a); N.x = p[0]; N.y = p[1];
      }
      colocar(raiz);
      var est = ESTACIONES[cfg.est];
      raiz.seg = ['c', est.x, est.y, est.x, est.y + (raiz.y - est.y) * 0.5, raiz.x, raiz.y - (raiz.y - est.y) * 0.5, raiz.x, raiz.y];
      raiz.padreEst = est.nodo;
      curva('ar:0:' + 3, 10, raiz.seg);
      todos.forEach(function (N) {
        nodos.push(N);
        if (!N.padre) return;
        N.seg = bez(N.padre, N);
        var w = 0.32 + 2.5 * Math.pow(N.n / raiz.n, 0.55);
        curva('ar:' + Math.min(9, N.prof) + ':' + Math.round(w * 2), 10, N.seg);
      });
      hojas.forEach(function (h) { capa('hoja', 'd', 14).g.push(['d', h.x, h.y, 1.05]); });
      /* anillo del tiempo: cada radio es una especificación; cada punto rojo, uno de sus quiebres */
      var a0 = cfg.a0 - 0.035, a1 = cfg.a1 + 0.035;
      function rA(y) { return cfg.t0 + (y - cfg.y0) / (cfg.y1 - cfg.y0) * (cfg.t1 - cfg.t0); }
      cfg.rA = rA;
      hojas.forEach(function (h) {
        var s = def.specs[h.spec]; h.datos = s;
        var p = polar(cfg.cx, cfg.cy, cfg.t0, h.a), q = polar(cfg.cx, cfg.cy, cfg.t1, h.a);
        h.pelo = ['l', p[0], p[1], q[0], q[1]];
        curva('pelo', 11, ['l', h.x, h.y, p[0], p[1]]);
        curva('pelo', 11, h.pelo);
        h.quiebres = (s[2] || []).map(function (y) { var z = polar(cfg.cx, cfg.cy, rA(y), h.a); capa('quiebre', 'd', 16).g.push(['d', z[0], z[1], 1.2]); return z; });
      });
      for (var y = Math.ceil(cfg.y0 / 10) * 10; y <= cfg.y1; y += 10) {
        capa('anillo', 's', 12).g.push(['a', cfg.cx, cfg.cy, rA(y), a0, a1]);
        if ((y - 1950) % 30) continue;
        var lp = polar(cfg.cx, cfg.cy, rA(y), cfg.etqA);
        capa('anillo:txt', 't', 17).g.push(['t', lp[0], lp[1], String(y), 7.5, cfg.etqAl]);
      }
      var cuenta = {}, cmax = 1;
      hojas.forEach(function (h) { (h.datos[2] || []).forEach(function (y) { cuenta[y] = (cuenta[y] || 0) + 1; if (cuenta[y] > cmax) cmax = cuenta[y]; }); });
      Object.keys(cuenta).forEach(function (y) { var f = cuenta[y] / cmax; if (f >= 0.5) capa('crisis:' + Math.min(4, Math.ceil((f - 0.5) * 8)), 's', 13).g.push(['a', cfg.cx, cfg.cy, rA(+y), a0, a1]); });
      return { raiz: raiz, hojas: hojas, todos: todos, cfg: cfg, cuenta: cuenta };
    }

    var eeuu = arbolRadial(D.eeuu, { nombre: 'eeuu', est: 1, cx: 520, cy: 482, a0: -168 * RAD, a1: -12 * RAD, r0: 36, dr: 29.5, rh: 312,
      t0: 324, t1: 418, y0: 1948, y1: 2025, etqA: -170 * RAD, etqAl: 'right' });
    var mundo = arbolRadial(D.mundo, { nombre: 'mundo', est: 4, cx: 1380, cy: 488, a0: 22 * RAD, a1: 158 * RAD, r0: 32, dr: 30, rh: 150,
      t0: 160, t1: 214, y0: 1960, y1: (D.meta && D.meta.mundo_fin) || 2023, etqA: 18 * RAD, etqAl: 'left' });
    /* países de cada especificación mundial: un trazo por país del panel */
    var PR = mulberry(SEED + 7);
    mundo.hojas.forEach(function (h, i) {
      var n = h.datos[1] || 0, sp = (mundo.cfg.a1 - mundo.cfg.a0) / Math.max(1, mundo.hojas.length + 6) * 0.42;
      for (var j = 0; j < n; j++) {
        var a = h.a + (j / Math.max(1, n - 1) - 0.5) * 2 * sp, r0 = 222 + PR() * 6, len = 14 + Math.pow(PR(), 1.6) * 52;
        var p = polar(mundo.cfg.cx, mundo.cfg.cy, r0, a), q = polar(mundo.cfg.cx, mundo.cfg.cy, r0 + len, a);
        curva('pais', 11, ['l', p[0], p[1], q[0], q[1]]);
      }
    });
    /* empalmes de las series de EE.UU. (meta.json): clasificaciones industriales SIC → NAICS */
    var emp = (D.meta && D.meta.empalmes) || {}, empNodo = null;
    [1987, 1997].forEach(function (y) { capa('empalme', 's', 15).g.push(['a', eeuu.cfg.cx, eeuu.cfg.cy, eeuu.cfg.rA(y), eeuu.cfg.a0 - 0.02, eeuu.cfg.a1 + 0.02]); });
    var pe = polar(eeuu.cfg.cx, eeuu.cfg.cy, eeuu.cfg.rA(1992), -16 * RAD);
    empNodo = { tipo: 'empalme', x: pe[0], y: pe[1], clave: 'empalme_estadistico', cod: 'K.08', empalmes: emp, peso: 3, hijos: [] };
    nodos.push(empNodo);

    /* ---- abanicos de series por sección */
    var familias = [];
    (D.familias || []).forEach(function (f) {
      var ab = ABANICOS[f.a] || [90, 150], est = ESTACIONES[f.e], phi = ab[0] * RAD, rad = ab[1];
      var sig = Math.min(0.62, 0.07 + f.s.length * 0.016);
      var cfg = { cx: est.x, cy: est.y };
      var F = { tipo: 'familia', nombre: f.n, ancla: f.a, series: f.s, est: f.e, r: rad * 0.42, a: phi, cx: cfg.cx, cy: cfg.cy, hijos: [], peso: 2 };
      var p = polar(cfg.cx, cfg.cy, F.r, phi); F.x = p[0]; F.y = p[1];
      F.seg = ['c', est.x, est.y, est.x + (F.x - est.x) * 0.2, est.y + (F.y - est.y) * 0.6, F.x - (F.x - est.x) * 0.3, F.y - (F.y - est.y) * 0.15, F.x, F.y];
      F.padreEst = est.nodo; F.n = f.s.length;
      curva('ar:1:' + Math.round((0.5 + Math.sqrt(f.s.length) * 0.22) * 2), 10, F.seg);
      nodos.push(F); familias.push(F);
      f.s.forEach(function (s, j) {
        var a = phi + (f.s.length > 1 ? (j / (f.s.length - 1) - 0.5) * 2 * sig : 0), r = rad + (j % 3) * 13 + rr(-3, 3);
        var L = { tipo: 'serie', nombre: s, familia: F, padre: F, r: r, a: a, cx: cfg.cx, cy: cfg.cy, prof: 2, hijos: [], peso: 1, n: 1 };
        var q = polar(cfg.cx, cfg.cy, r, a); L.x = q[0]; L.y = q[1];
        L.seg = bez(F, L); F.hijos.push(L);
        curva('ar:4:1', 10, L.seg);
        capa('serie', 'd', 14).g.push(['d', L.x, L.y, 1.3]);
        nodos.push(L);
      });
    });

    /* ---- nodos clave con etiqueta */
    var bifurcacion = null;
    eeuu.todos.forEach(function (N) { if (!bifurcacion && N.tipo === 'decision' && D.eeuu.claves[N.dim] === 'D2') bifurcacion = N; });
    eeuu.raiz.clave = 'especificacion_multiverso'; eeuu.raiz.cod = 'K.06';
    if (bifurcacion) { bifurcacion.clave = 'bifurcacion_teorica'; bifurcacion.cod = 'K.07'; }
    function etq(n, dx, dy, al, sub) { if (n) etiquetas.push({ n: n, dx: dx, dy: dy, al: al || 'left', sub: sub }); }
    var m = D.meta || {};
    etq(ESTACIONES[0].nodo, -40, 92, 'left', 'eje · exposición categorial');
    etq(ESTACIONES[1].nodo, -250, 118, 'left', 'eje · ' + eeuu.hojas.length + ' especificaciones');
    etq(ESTACIONES[2].nodo, 52, 92, 'left', 'eje · ' + (familias.filter(function (f) { return f.est === 2; })[0] || { n: 0 }).n + ' series');
    etq(ESTACIONES[3].nodo, -46, -62, 'right', 'eje · horas de trabajo');
    etq(ESTACIONES[4].nodo, -62, 50, 'right', 'eje · ' + mundo.hojas.length + ' especificaciones mundiales');
    etq(eeuu.raiz, 70, 40, 'left', 'raíz · ' + D.eeuu.dims.length + ' decisiones');
    etq(bifurcacion, -175, 36, 'right', 'qué cuenta como plusvalor');
    etq(empNodo, 70, -34, 'left', Object.keys(emp).length + ' empalmes SIC → NAICS');

    /* ---- marco de lámina */
    capa('lam', 's', 1).g.push(['p', [[12, 12], [W - 12, 12], [W - 12, H - 12], [12, H - 12], [12, 12]]]);
    for (x = 20; x < W - 12; x += 20) capa('lam', 's', 1).g.push(['l', x, 12, x, 12 + (x % 100 === 0 ? 7 : 3)]);
    for (var y2 = 20; y2 < H - 12; y2 += 20) capa('lam', 's', 1).g.push(['l', 12, y2, 12 + (y2 % 100 === 0 ? 7 : 3), y2]);
    for (x = 100; x < W - 12; x += 200) capa('lam:txt', 't', 1).g.push(['t', x + 3, 26, ('000' + x).slice(-4), 7, 'left']);
    [[12, 12], [W - 12, 12], [12, H - 12], [W - 12, H - 12]].forEach(function (c) {
      capa('lam:reg', 's', 1).g.push(['l', c[0] - 9, c[1], c[0] + 9, c[1]], ['l', c[0], c[1] - 9, c[0], c[1] + 9], ['a', c[0], c[1], 5, 0, Math.PI * 2]);
    });
    var fecha = (m.actualizado || '').slice(0, 10);
    [['mapa cognitivo del capital · ' + VERSION, 9.5],
     ['topología: multiverso efectivo · ' + eeuu.hojas.length + ' + ' + mundo.hojas.length + ' especificaciones · geometría: semilla ' + SEED, 7.5],
     ['datos: ' + (m.actualizado || '—') + (m.commit ? ' · commit ' + m.commit : ''), 7.5]].forEach(function (l, i) {
      capa(i ? 'lam:txt' : 'lam:tit', 't', 1).g.push(['t', W - 26, 34 + i * 13, l[0], l[1], 'right']);
    });

    orden.sort(function (a, b) { return a.z - b.z; });
    return { capas: orden, nodos: nodos, etiquetas: etiquetas, eeuu: eeuu, mundo: mundo, familias: familias, estaciones: ESTACIONES, empalme: empNodo,
      ejePts: ejePts, D: D, fecha: fecha };
  }

  /* ---------------------------------------------------------------- temas */
  function mezcla(a, b, t) {
    var pa = parseInt(a.slice(1), 16), pb = parseInt(b.slice(1), 16);
    var r = (pa >> 16) + (((pb >> 16) - (pa >> 16)) * t), g = ((pa >> 8) & 255) + ((((pb >> 8) & 255) - ((pa >> 8) & 255)) * t), bl = (pa & 255) + (((pb & 255) - (pa & 255)) * t);
    return 'rgb(' + Math.round(r) + ',' + Math.round(g) + ',' + Math.round(bl) + ')';
  }
  var TEMAS = {
    fosforo: {
      fondo: '#06070a', luz: true, acento: '#ff4d6d', texto: '#e9e5ff', tenue: '#7d77aa', etqFondo: 'rgba(6,7,10,.78)',
      estilo: function (id) {
        var p = id.split(':');
        if (p[0] === 'ar') { var d = +p[1], w = +p[2] / 2, t = Math.min(1, d / 8); return { c: t < 0.5 ? mezcla('#f1edff', '#a88bff', t * 2) : mezcla('#a88bff', '#4a3cb8', (t - 0.5) * 2), a: 0.62 - t * 0.2, w: w, halo: 4.5, ha: 0.05 }; }
        return ({
          'sis:traza': { c: '#7476aa', a: 0.3, w: 0.5 }, 'sis:banda90': { c: '#6d4cff', a: 0.07 }, 'sis:banda50': { c: '#8b6cff', a: 0.1 },
          'sis:p50': { c: '#c9bbff', a: 0.75, w: 1, halo: 5, ha: 0.08 }, 'sis:pico': { c: '#ff4d6d', a: 0.7, w: 1.1, halo: 4, ha: 0.08 },
          'sis:regla': { c: '#585a80', a: 0.7, w: 0.6 }, 'sis:txt': { c: '#5e5f86', a: 1 }, 'sis:pico:txt': { c: '#ff7a8f', a: 0.9 },
          'eje:halo': { c: '#6a3dff', a: 0.12, w: 22 }, 'eje:medio': { c: '#8f6bff', a: 0.28, w: 7 }, 'eje:luz': { c: '#b9a5ff', a: 0.7, w: 2.6 }, 'eje:nucleo': { c: '#f6f4ff', a: 1, w: 1.1 },
          'hoja': { c: '#d4caff', a: 0.6 }, 'serie': { c: '#d4caff', a: 0.95 }, 'pelo': { c: '#9f8cff', a: 0.1, w: 0.45 }, 'pais': { c: '#8fa0ff', a: 0.13, w: 0.4 },
          'anillo': { c: '#6c66b0', a: 0.28, w: 0.45, dash: [1.5, 3.5] }, 'anillo:txt': { c: '#6b65a0', a: 1 },
          'crisis:1': { c: '#ff4d6d', a: 0.05, w: 1.2 }, 'crisis:2': { c: '#ff4d6d', a: 0.09, w: 1.6 }, 'crisis:3': { c: '#ff4d6d', a: 0.14, w: 2 }, 'crisis:4': { c: '#ff4d6d', a: 0.2, w: 2.6, halo: 3, ha: 0.06 },
          'quiebre': { c: '#ff4d6d', a: 0.95 }, 'empalme': { c: '#7ddcff', a: 0.5, w: 0.6, dash: [5, 4] },
          'lam': { c: '#3a3b55', a: 0.9, w: 0.6 }, 'lam:reg': { c: '#55567a', a: 0.9, w: 0.6 }, 'lam:txt': { c: '#4f5074', a: 1 }, 'lam:tit': { c: '#9a95c8', a: 1 }
        })[id] || { c: '#ffffff', a: 0.3, w: 0.5 };
      }
    },
    tinta: {
      fondo: null, luz: false, acento: '#b8203a', texto: '#182235', tenue: '#5d6878', etqFondo: 'rgba(237,240,239,.82)',
      estilo: function (id) {
        var p = id.split(':');
        if (p[0] === 'ar') { var d = +p[1], w = +p[2] / 2, t = Math.min(1, d / 8); return { c: t < 0.6 ? '#182235' : '#3b3f7a', a: 0.62 - t * 0.38, w: w * 0.85 }; }
        return ({
          'sis:traza': { c: '#5d6878', a: 0.22, w: 0.5 }, 'sis:banda90': { c: '#6a4c9c', a: 0.08 }, 'sis:banda50': { c: '#6a4c9c', a: 0.12 },
          'sis:p50': { c: '#182235', a: 0.7, w: 0.9 }, 'sis:pico': { c: '#b8203a', a: 0.75, w: 1 }, 'sis:regla': { c: '#5d6878', a: 0.6, w: 0.6 },
          'sis:txt': { c: '#5d6878', a: 1 }, 'sis:pico:txt': { c: '#b8203a', a: 1 },
          'eje:halo': { c: '#6a4c9c', a: 0.06, w: 14 }, 'eje:medio': { c: '#6a4c9c', a: 0.15, w: 5 }, 'eje:luz': { c: '#182235', a: 0.55, w: 2.2 }, 'eje:nucleo': { c: '#182235', a: 0.9, w: 0.9 },
          'hoja': { c: '#182235', a: 0.7 }, 'serie': { c: '#182235', a: 0.75 }, 'pelo': { c: '#182235', a: 0.08, w: 0.45 }, 'pais': { c: '#1d6d78', a: 0.12, w: 0.4 },
          'anillo': { c: '#5d6878', a: 0.35, w: 0.45, dash: [1.5, 3.5] }, 'anillo:txt': { c: '#5d6878', a: 1 },
          'crisis:1': { c: '#b8203a', a: 0.05, w: 1.2 }, 'crisis:2': { c: '#b8203a', a: 0.08, w: 1.6 }, 'crisis:3': { c: '#b8203a', a: 0.12, w: 2 }, 'crisis:4': { c: '#b8203a', a: 0.17, w: 2.6 },
          'quiebre': { c: '#b8203a', a: 0.9 }, 'empalme': { c: '#1d6d78', a: 0.55, w: 0.6, dash: [5, 4] },
          'lam': { c: '#5d6878', a: 0.45, w: 0.6 }, 'lam:reg': { c: '#5d6878', a: 0.6, w: 0.6 }, 'lam:txt': { c: '#5d6878', a: 1 }, 'lam:tit': { c: '#182235', a: 1 }
        })[id] || { c: '#182235', a: 0.3, w: 0.5 };
      }
    }
  };

  /* ---------------------------------------------------------------- dibujo */
  var MONO = "'IBM Plex Mono','JetBrains Mono',ui-monospace,'SF Mono',Menlo,Consolas,monospace";
  function trazar(ctx, g) {
    if (g[0] === 'c') { ctx.moveTo(g[1], g[2]); ctx.bezierCurveTo(g[3], g[4], g[5], g[6], g[7], g[8]); }
    else if (g[0] === 'l') { ctx.moveTo(g[1], g[2]); ctx.lineTo(g[3], g[4]); }
    else if (g[0] === 'p') { var p = g[1]; ctx.moveTo(p[0][0], p[0][1]); for (var i = 1; i < p.length; i++) ctx.lineTo(p[i][0], p[i][1]); }
    else if (g[0] === 'a') { ctx.moveTo(g[1] + Math.cos(g[4]) * g[3], g[2] + Math.sin(g[4]) * g[3]); ctx.arc(g[1], g[2], g[3], g[4], g[5]); }
  }
  function pintarEstatico(ctx, E, tema, v, op) {
    var T = TEMAS[tema], f = v.fw;   // f: factor de grosor (un trazo no engorda al acercarse)
    ctx.save();
    ctx.setTransform(v.dpr, 0, 0, v.dpr, 0, 0);
    ctx.clearRect(0, 0, v.cw, v.ch);
    if (T.fondo && op.fondoPropio !== false) {
      ctx.fillStyle = T.fondo; ctx.fillRect(0, 0, v.cw, v.ch);
    }
    ctx.setTransform(v.dpr * v.z, 0, 0, v.dpr * v.z, v.dpr * (v.cw / 2 - v.cx * v.z), v.dpr * (v.ch / 2 - v.cy * v.z));
    if (T.luz && op.atmosfera !== false) {
      [[520, 330, 560, 'rgba(92,58,200,0.20)'], [1380, 600, 380, 'rgba(70,80,200,0.12)'], [800, 470, 900, 'rgba(40,30,90,0.10)']].forEach(function (g) {
        var gr = ctx.createRadialGradient(g[0], g[1], 0, g[0], g[1], g[2]); gr.addColorStop(0, g[3]); gr.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.fillStyle = gr; ctx.fillRect(g[0] - g[2], g[1] - g[2], g[2] * 2, g[2] * 2);
      });
    }
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    var minW = 0.4 / v.z;
    E.capas.forEach(function (L) {
      if ((op.sinTexto || v.etq === false) && L.tipo === 't') return;
      if (op.sinMarco && L.id.indexOf('lam') === 0) return;
      var s = T.estilo(L.id);
      ctx.globalCompositeOperation = T.luz ? 'lighter' : 'source-over';
      if (L.tipo === 's') {
        ctx.beginPath(); L.g.forEach(function (g) { trazar(ctx, g); });
        ctx.setLineDash(s.dash ? s.dash.map(function (d) { return d * f; }) : []);
        if (s.halo && T.luz) { ctx.strokeStyle = s.c; ctx.globalAlpha = s.ha; ctx.lineWidth = Math.max(minW, (s.w || 0.5) * s.halo * f); ctx.stroke(); }
        ctx.strokeStyle = s.c; ctx.globalAlpha = s.a; ctx.lineWidth = Math.max(minW, (s.w || 0.5) * f); ctx.stroke();
      } else if (L.tipo === 'f') {
        ctx.beginPath(); L.g.forEach(function (g) { trazar(ctx, g); ctx.closePath(); }); ctx.fillStyle = s.c; ctx.globalAlpha = s.a; ctx.fill();
      } else if (L.tipo === 'd') {
        ctx.beginPath(); L.g.forEach(function (g) { var r = Math.max(0.45 / v.z, g[3] * f); ctx.moveTo(g[1] + r, g[2]); ctx.arc(g[1], g[2], r, 0, 6.2832); });
        ctx.fillStyle = s.c; ctx.globalAlpha = s.a; ctx.fill();
        if (T.luz && L.id === 'quiebre') { ctx.globalAlpha = 0.12; ctx.beginPath(); L.g.forEach(function (g) { var r = g[3] * f * 3.2; ctx.moveTo(g[1] + r, g[2]); ctx.arc(g[1], g[2], r, 0, 6.2832); }); ctx.fill(); }
      } else if (L.tipo === 't') {
        ctx.globalCompositeOperation = 'source-over'; ctx.fillStyle = s.c; ctx.globalAlpha = s.a;
        L.g.forEach(function (g) { ctx.font = (g[4] * v.ft) + 'px ' + MONO; ctx.textAlign = g[5]; ctx.textBaseline = 'middle'; ctx.fillText(g[3], g[1], g[2]); });
      }
    });
    ctx.setLineDash([]); ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 1;
    /* nodos clave */
    var clave = E.nodos.filter(function (n) { return n.clave; });
    clave.forEach(function (n) {
      var est = n.tipo === 'estacion', r = (est ? 9 : 6.5) * f;
      if (T.luz) { var gr = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, r * 3); gr.addColorStop(0, 'rgba(235,230,255,.55)'); gr.addColorStop(1, 'rgba(120,80,255,0)'); ctx.fillStyle = gr; ctx.beginPath(); ctx.arc(n.x, n.y, r * 3, 0, 6.2832); ctx.fill(); }
      ctx.strokeStyle = T.luz ? '#cbbcff' : T.texto; ctx.globalAlpha = 0.85; ctx.lineWidth = Math.max(minW, 0.7 * f);
      ctx.beginPath(); ctx.arc(n.x, n.y, r, 0, 6.2832); ctx.stroke();
      if (est) { ctx.beginPath(); ctx.moveTo(n.x - r * 1.7, n.y); ctx.lineTo(n.x - r * 1.15, n.y); ctx.moveTo(n.x + r * 1.15, n.y); ctx.lineTo(n.x + r * 1.7, n.y); ctx.moveTo(n.x, n.y - r * 1.7); ctx.lineTo(n.x, n.y - r * 1.15); ctx.moveTo(n.x, n.y + r * 1.15); ctx.lineTo(n.x, n.y + r * 1.7); ctx.stroke(); }
      ctx.globalAlpha = 1; ctx.fillStyle = T.luz ? '#f8f6ff' : T.texto; ctx.beginPath(); ctx.arc(n.x, n.y, (est ? 2.8 : 2.2) * f, 0, 6.2832); ctx.fill();
    });
    if (!op.sinTexto && v.etq !== false) pintarEtiquetas(ctx, E, T, v, op);
    /* viñeta y grano */
    ctx.setTransform(v.dpr, 0, 0, v.dpr, 0, 0);
    if (T.luz && op.atmosfera !== false) {
      var vg = ctx.createRadialGradient(v.cw / 2, v.ch / 2, Math.min(v.cw, v.ch) * 0.35, v.cw / 2, v.ch / 2, Math.max(v.cw, v.ch) * 0.75);
      vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,0,0.55)'); ctx.fillStyle = vg; ctx.fillRect(0, 0, v.cw, v.ch);
      if (op.grano !== false) { ctx.globalAlpha = 1; ctx.fillStyle = ctx.createPattern(grano(), 'repeat'); ctx.fillRect(0, 0, v.cw, v.ch); }
    }
    ctx.restore();
  }
  var _grano = null;
  function grano() {
    if (_grano) return _grano;
    var c = document.createElement('canvas'); c.width = c.height = 160; var x = c.getContext('2d'), im = x.createImageData(160, 160), R = mulberry(SEED + 3);
    for (var i = 0; i < im.data.length; i += 4) { var v = R() * 255; im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = R() < 0.5 ? 9 : 0; }
    x.putImageData(im, 0, 0); return (_grano = c);
  }
  function cajaEtiqueta(e, ctx, v) {
    var n = e.n, lx = n.x + e.dx, ly = n.y + e.dy, fs = 12.5 * v.ft, fs2 = 8.5 * v.ft;
    ctx.font = '500 ' + fs + 'px ' + MONO; var w1 = ctx.measureText(n.clave).width;
    ctx.font = fs2 + 'px ' + MONO; var w2 = ctx.measureText(n.cod + ' · ' + (e.sub || '')).width;
    var w = Math.max(w1, w2) + 16 * v.ft, h = 34 * v.ft, x0 = e.al === 'right' ? lx - w : lx, y0 = ly - h / 2;
    return { lx: lx, ly: ly, x0: x0, y0: y0, w: w, h: h, fs: fs, fs2: fs2 };
  }
  function pintarEtiquetas(ctx, E, T, v, op) {
    var f = v.fw;
    E.etiquetas.forEach(function (e) {
      var n = e.n, b = cajaEtiqueta(e, ctx, v), ex = e.al === 'right' ? b.x0 + b.w : b.x0, ey = b.ly;
      ctx.globalAlpha = op.alfaEtiquetas || 1;
      ctx.strokeStyle = T.luz ? '#9c8fe6' : T.tenue; ctx.lineWidth = Math.max(0.4 / v.z, 0.6 * f);
      ctx.beginPath(); ctx.moveTo(n.x, n.y); var mx = n.x + (ex - n.x) * 0.55; ctx.lineTo(mx, ey); ctx.lineTo(ex, ey); ctx.stroke();
      ctx.fillStyle = T.luz ? '#cbbcff' : T.texto; ctx.fillRect(ex - 1.6 * f, ey - 1.6 * f, 3.2 * f, 3.2 * f);
      ctx.fillStyle = T.etqFondo; ctx.fillRect(b.x0, b.y0, b.w, b.h);
      ctx.strokeStyle = T.luz ? 'rgba(160,140,255,.35)' : 'rgba(24,34,53,.25)'; ctx.lineWidth = Math.max(0.4 / v.z, 0.5 * f); ctx.strokeRect(b.x0, b.y0, b.w, b.h);
      ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
      ctx.font = b.fs2 + 'px ' + MONO; ctx.fillStyle = T.tenue; ctx.fillText(n.cod + ' · ' + (e.sub || ''), b.x0 + 8 * v.ft, b.y0 + 12.5 * v.ft);
      ctx.font = '500 ' + b.fs + 'px ' + MONO; ctx.fillStyle = T.texto; ctx.fillText(n.clave, b.x0 + 8 * v.ft, b.y0 + 27 * v.ft);
      ctx.globalAlpha = 1;
    });
  }

  /* ---------------------------------------------------------------- consultas para el panel */
  function cadena(n) { var c = []; while (n) { c.push(n); n = n.padre || n.padreEst || null; } return c; }
  function hojasDe(n) { if (n.tipo === 'hoja') return [n]; var r = []; (n.hijos || []).forEach(function (h) { r = r.concat(hojasDe(h)); }); return r; }
  function describir(E, n) {
    var D = E.D, d = { nodo: n, tipo: n.tipo, cod: n.cod, clave: n.clave };
    if (n.tipo === 'estacion') { var e = E.estaciones[n.est]; d.titulo = e.k; d.texto = e.t; d.enlaces = [[e.a, 'leer en el sitio']]; d.sub = 'eje categorial'; }
    if (n.tipo === 'decision' || n.tipo === 'hoja') {
      var def = D[n.arbol], esEEUU = n.arbol === 'eeuu', hs = hojasDe(n);
      d.arbol = esEEUU ? 'multiverso EE.UU.' : 'multiverso mundial';
      d.ruta = cadena(n).reverse().filter(function (x) { return x.padre && x.padre.dim != null; }).map(function (x) { var dm = def.dims[x.padre.dim]; return [dm[0], dm[2][x.opt]]; });
      d.quiebres = {}; hs.forEach(function (h) { (h.datos[2] || []).forEach(function (y) { d.quiebres[y] = (d.quiebres[y] || 0) + 1; }); });
      d.n = hs.length;
      d.enlaces = esEEUU ? [['index.html#multiverso', 'el multiverso en el sitio'], ['metodologia.html#multiverso', 'metodología §5']] : [['index.html#mundo', 'tasa mundial en el sitio'], ['metodologia.html#mundo', 'metodología']];
      if (n.tipo === 'decision') {
        var dm = def.dims[n.dim];
        d.titulo = n.clave || dm[0]; d.sub = n.clave ? dm[0] : 'bifurcación teórica';
        d.decision = dm[0]; d.posicion = dm[1];
        d.opciones = n.hijos.map(function (h) { return [dm[2][h.opt], hojasDe(h).length]; });
        if (n.clave === 'especificacion_multiverso') d.texto = 'Raíz del multiverso efectivo de EE.UU.: cada hoja es una especificación publicada y cada bifurcación, una decisión teórica explícita. Se informa la distribución completa, no una estimación elegida a posteriori.';
        if (n.clave === 'bifurcacion_teorica') { d.texto = 'Qué trabajo es productivo decide qué parte del excedente cuenta como plusvalor. Aquí el plusvalor ampliado se separa en dos criterios: por ramas o con la corrección intra-rama. La variante «todo productivo» cuelga del numerador «excedente amplio».'; d.enlaces.push(['index.html#supuestos', 'qué cuenta como plusvalor']); }
      } else {
        var s = n.datos; d.titulo = s[0]; d.sub = esEEUU ? 'especificación · ' + s[1] : 'especificación mundial · ' + s[1] + ' países';
        d.decisiones = def.dims.map(function (dm, i) { return [dm[0], s[3] && s[3][i] >= 0 ? dm[2][s[3][i]] : '—']; });
        d.anios = s[2] || [];
      }
    }
    if (n.tipo === 'familia') { d.titulo = n.nombre; d.sub = n.series.length + ' series publicadas'; d.series = n.series; d.enlaces = [[n.ancla, 'ver la sección']]; }
    if (n.tipo === 'serie') { d.titulo = n.nombre; d.sub = 'serie · ' + n.familia.nombre; d.enlaces = [[n.familia.ancla, 'ver la sección']]; }
    if (n.tipo === 'empalme') {
      d.titulo = 'empalme_estadistico'; d.sub = 'cambios de clasificación industrial en las series de EE.UU.';
      d.texto = 'Las series del BEA cambian de clasificación (SIC → NAICS). Cada empalme se hace con un factor de nivel explícito; los arcos punteados del anillo marcan esos años.';
      d.empalmes = Object.keys(n.empalmes || {}).map(function (k) { return [k, n.empalmes[k]]; });
      d.enlaces = [['metodologia.html#empalmes', 'metodología: empalmes']];
    }
    return d;
  }

  /* ---------------------------------------------------------------- montaje */
  function montar(cont, op) {
    op = op || {};
    var modo = op.modo || 'mapa';
    var cv = document.createElement('canvas'); cv.className = 'mapa-cognitivo-lienzo';
    cv.setAttribute('role', 'img');
    cv.setAttribute('aria-label', 'Mapa cognitivo del capital: eje categorial, multiverso de especificaciones con sus quiebres y registro sismográfico.');
    cv.style.cssText = 'display:block;width:100%;height:100%;' + (modo === 'mapa' ? 'touch-action:none;cursor:grab;' : '');
    cont.appendChild(cv);
    var est = document.createElement('canvas'), ctx = cv.getContext('2d'), sctx = est.getContext('2d');
    var E = null, tema = op.tema || 'fosforo', sucio = true, sel = null, fijo = null, cam = { x: W / 2, y: H / 2, zoom: 1 };
    var quieto = op.quieto || (global.matchMedia && global.matchMedia('(prefers-reduced-motion: reduce)').matches);
    var v = { cw: 1, ch: 1, dpr: 1, z: 1, cx: W / 2, cy: H / 2, fw: 1, ft: 1 };
    var pulsos = [], pings = [], ultimo = 0, vivo = true;

    function medir() {
      var r = cont.getBoundingClientRect();
      v.cw = Math.max(1, r.width); v.ch = Math.max(1, r.height);
      v.dpr = Math.min(global.devicePixelRatio || 1, modo === 'fondo' ? 1.5 : 2);
      cv.width = est.width = Math.round(v.cw * v.dpr); cv.height = est.height = Math.round(v.ch * v.dpr);
      vista(); sucio = true;
    }
    function vista() {
      var base = modo === 'fondo' ? Math.max(v.cw / W, v.ch / H) * (op.escala || 1) : Math.min(v.cw / (W * 1.0), v.ch / (H * 1.0));
      v.z = base * cam.zoom; v.cx = cam.x; v.cy = cam.y;
      v.fw = Math.pow(cam.zoom, -0.62); v.ft = Math.pow(cam.zoom, -0.72); v.etq = v.z >= 0.42;
    }
    function aMundo(px, py) { return [(px - v.cw / 2) / v.z + v.cx, (py - v.ch / 2) / v.z + v.cy]; }
    function limitar() {
      cam.zoom = Math.max(1, Math.min(9, cam.zoom));
      var hw = v.cw / 2 / (v.z || 1), hh = v.ch / 2 / (v.z || 1);
      cam.x = hw * 2 >= W ? W / 2 : Math.max(hw, Math.min(W - hw, cam.x));
      cam.y = hh * 2 >= H ? H / 2 : Math.max(hh, Math.min(H - hh, cam.y));
    }

    /* pulsos: recorridos raíz → hoja; al llegar, los quiebres de esa especificación destellan */
    function nuevoPulso() {
      var r = Math.random(), pool = r < 0.72 ? E.eeuu.hojas : r < 0.85 ? E.mundo.hojas : null;
      var hoja = pool ? pool[Math.floor(Math.random() * pool.length)] : (function () { var f = E.familias[Math.floor(Math.random() * E.familias.length)]; return f.hijos[Math.floor(Math.random() * f.hijos.length)]; })();
      var segs = cadena(hoja).filter(function (x) { return x.seg; }).map(function (x) { return x.seg; }).reverse();
      pulsos.push({ segs: segs, t: 0, vel: (modo === 'fondo' ? 0.55 : 0.9) * (0.7 + Math.random() * 0.6), hoja: hoja });
    }
    function bz(s, t) { var u = 1 - t; if (s[0] === 'l') return [s[1] + (s[3] - s[1]) * t, s[2] + (s[4] - s[2]) * t]; return [u * u * u * s[1] + 3 * u * u * t * s[3] + 3 * u * t * t * s[5] + t * t * t * s[7], u * u * u * s[2] + 3 * u * u * t * s[4] + 3 * u * t * t * s[6] + t * t * t * s[8]]; }
    function posPulso(p, t) { if (t <= 0) t = 0; var i = Math.min(p.segs.length - 1, Math.floor(t)); return bz(p.segs[i], Math.min(1, t - i)); }

    function cuadro(ts) {
      if (!vivo) return;
      var dt = Math.min(0.05, (ts - (ultimo || ts)) / 1000); ultimo = ts;
      if (sucio) { pintarEstatico(sctx, E, tema, v, op); sucio = false; }
      ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, cv.width, cv.height); ctx.drawImage(est, 0, 0);
      ctx.setTransform(v.dpr * v.z, 0, 0, v.dpr * v.z, v.dpr * (v.cw / 2 - v.cx * v.z), v.dpr * (v.ch / 2 - v.cy * v.z));
      var T = TEMAS[tema], f = v.fw;
      if (sel) resaltar(ctx, sel, T, f);
      if (!quieto) {
        var objetivo = modo === 'fondo' ? (op.pulsos || 7) : 16;
        while (pulsos.length < objetivo) nuevoPulso();
        ctx.globalCompositeOperation = T.luz ? 'lighter' : 'source-over';
        /* destello que recorre el eje */
        var ex = 30 + ((ts / 1000 * 140) % 2200); if (ex < 1600) {
          for (var k = 0; k < 14; k++) { var xx = ex - k * 9; if (xx < 30) break; ctx.globalAlpha = (1 - k / 14) * (T.luz ? 0.55 : 0.35); ctx.fillStyle = T.luz ? '#efeaff' : '#6a4c9c'; ctx.beginPath(); ctx.arc(xx, ejeY(xx), (2.6 - k * 0.12) * f, 0, 6.2832); ctx.fill(); }
        }
        pulsos = pulsos.filter(function (p) {
          p.t += dt * p.vel * (1 + p.t * 0.15);
          if (p.t >= p.segs.length) { if (p.hoja.quiebres) p.hoja.quiebres.forEach(function (q) { pings.push({ x: q[0], y: q[1], t: 0 }); }); return false; }
          for (var j = 0; j < 9; j++) {
            var q = posPulso(p, p.t - j * 0.05); ctx.globalAlpha = (1 - j / 9) * (T.luz ? 0.8 : 0.5);
            ctx.fillStyle = j === 0 ? (T.luz ? '#ffffff' : '#182235') : (T.luz ? '#b9a5ff' : '#6a4c9c');
            ctx.beginPath(); ctx.arc(q[0], q[1], (j === 0 ? 1.9 : 1.4 - j * 0.1) * f, 0, 6.2832); ctx.fill();
          }
          return true;
        });
        pings = pings.filter(function (p) {
          p.t += dt; if (p.t > 1.1) return false;
          ctx.globalAlpha = (1 - p.t / 1.1) * 0.9; ctx.strokeStyle = T.acento; ctx.lineWidth = 0.8 * f;
          ctx.beginPath(); ctx.arc(p.x, p.y, (1.5 + p.t * 9) * f, 0, 6.2832); ctx.stroke(); return true;
        });
        ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 1;
      }
      if (!quieto || sucio) global.requestAnimationFrame(cuadro); else pendiente = false;
    }
    var pendiente = false;
    function pedir() { sucio = true; if (quieto && !pendiente) { pendiente = true; global.requestAnimationFrame(cuadro); } }

    function resaltar(c, n, T, f) {
      c.globalCompositeOperation = T.luz ? 'lighter' : 'source-over';
      c.lineCap = 'round';
      var sub = [], walk = function (x) { (x.hijos || []).forEach(function (h) { if (h.seg) sub.push(h.seg); walk(h); }); };
      if (n.tipo === 'estacion') E.nodos.forEach(function (x) { if (x.padreEst === n) { sub.push(x.seg); walk(x); } }); else walk(n);
      c.beginPath(); sub.forEach(function (s) { trazar(c, s); });
      c.strokeStyle = T.luz ? '#cfc4ff' : '#3b3f7a'; c.globalAlpha = T.luz ? 0.35 : 0.5; c.lineWidth = 0.9 * f; c.stroke();
      var ch = cadena(n).filter(function (x) { return x.seg; });
      c.beginPath(); ch.forEach(function (x) { trazar(c, x.seg); });
      if (T.luz) { c.strokeStyle = '#8f6bff'; c.globalAlpha = 0.35; c.lineWidth = 6 * f; c.stroke(); }
      c.strokeStyle = T.luz ? '#ffffff' : '#182235'; c.globalAlpha = 1; c.lineWidth = 1.5 * f; c.stroke();
      hojasDe(n).forEach(function (h) {
        if (!h.pelo) return;
        c.beginPath(); trazar(c, h.pelo); c.strokeStyle = T.luz ? '#d9d0ff' : '#182235'; c.globalAlpha = n.tipo === 'hoja' ? 0.9 : 0.25; c.lineWidth = 0.7 * f; c.stroke();
        c.fillStyle = T.acento; c.globalAlpha = 1; (h.quiebres || []).forEach(function (q) { c.beginPath(); c.arc(q[0], q[1], (n.tipo === 'hoja' ? 2.6 : 1.6) * f, 0, 6.2832); c.fill(); });
      });
      c.globalAlpha = 1; c.strokeStyle = T.luz ? '#ffffff' : '#182235'; c.lineWidth = 1 * f;
      c.beginPath(); c.arc(n.x, n.y, 7 * f, 0, 6.2832); c.stroke();
      c.globalCompositeOperation = 'source-over';
    }

    function cercano(px, py) {
      var m = aMundo(px, py), lim = 15 / v.z, mejor = null, md = lim * lim;
      E.nodos.forEach(function (n) { var dx = n.x - m[0], dy = n.y - m[1], d = (dx * dx + dy * dy) / (n.peso || 1); if (d < md) { md = d; mejor = n; } });
      return mejor;
    }
    function elegir(n, fijar) {
      if (fijar !== undefined) fijo = fijar ? n : null;
      sel = n; if (op.alSeleccionar) op.alSeleccionar(n ? describir(E, n) : null, !!fijo);
      if (quieto) pedir();
    }

    /* interacción (sólo en la pestaña) */
    if (modo === 'mapa') {
      var ptr = {}, arr = null, movido = false, pinza = 0;
      cv.addEventListener('wheel', function (e) { e.preventDefault(); zoomEn(e.offsetX, e.offsetY, Math.exp(-e.deltaY * 0.0016)); }, { passive: false });
      cv.addEventListener('pointerdown', function (e) { cv.setPointerCapture(e.pointerId); ptr[e.pointerId] = [e.offsetX, e.offsetY]; arr = [e.offsetX, e.offsetY]; movido = false; var k = Object.keys(ptr); if (k.length === 2) { var a = ptr[k[0]], b = ptr[k[1]]; pinza = Math.hypot(a[0] - b[0], a[1] - b[1]); } });
      cv.addEventListener('pointermove', function (e) {
        var pr = ptr[e.pointerId];
        if (pr) {
          ptr[e.pointerId] = [e.offsetX, e.offsetY]; var k = Object.keys(ptr);
          if (k.length === 2) { var a = ptr[k[0]], b = ptr[k[1]], d = Math.hypot(a[0] - b[0], a[1] - b[1]); if (pinza) zoomEn((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, d / pinza); pinza = d; movido = true; return; }
          if (Math.hypot(e.offsetX - arr[0], e.offsetY - arr[1]) > 3) { movido = true; cv.style.cursor = 'grabbing'; cam.x -= (e.offsetX - pr[0]) / v.z; cam.y -= (e.offsetY - pr[1]) / v.z; vista(); limitar(); vista(); pedir(); return; }
        }
        if (fijo || e.pointerType === 'touch') return;
        var n = cercano(e.offsetX, e.offsetY); if (n !== sel) elegir(n);
      });
      function fin(e) {
        delete ptr[e.pointerId]; if (Object.keys(ptr).length < 2) pinza = 0; cv.style.cursor = 'grab';
        if (e.type === 'pointerup' && !movido && !Object.keys(ptr).length) { var n = cercano(e.offsetX, e.offsetY); elegir(n, !!n); }
      }
      cv.addEventListener('pointerup', fin); cv.addEventListener('pointercancel', fin);
      cv.addEventListener('pointerleave', function () { if (!fijo && !Object.keys(ptr).length) elegir(null); });
    }
    function zoomEn(px, py, k) {
      var m = aMundo(px, py); cam.zoom *= k; cam.zoom = Math.max(1, Math.min(9, cam.zoom)); vista();
      cam.x = m[0] - (px - v.cw / 2) / v.z; cam.y = m[1] - (py - v.ch / 2) / v.z; vista(); limitar(); vista(); pedir();
    }

    function encuadreInicial() {
      cam = { x: W / 2, y: H / 2, zoom: 1 };
      if (modo === 'mapa' && v.cw / v.ch < 1.1) { cam.zoom = Math.min(2.6, (v.ch / H) / (v.cw / W)); cam.x = 640; vista(); limitar(); }
      vista();
    }
    function iniciar(D) {
      E = construirEscena(D); medir(); encuadreInicial();
      if (global.ResizeObserver) new ResizeObserver(function () { medir(); pedir(); }).observe(cont); else global.addEventListener('resize', function () { medir(); pedir(); });
      document.addEventListener('visibilitychange', function () { if (!document.hidden && !quieto) { ultimo = 0; global.requestAnimationFrame(cuadro); } });
      global.requestAnimationFrame(cuadro);
      if (op.alListo) op.alListo(api);
    }
    var api = {
      escena: function () { return E; },
      tema: function (t) { tema = t; sucio = true; pedir(); },
      acercar: function (k) { zoomEn(v.cw / 2, v.ch / 2, k); },
      encuadre: function () { encuadreInicial(); pedir(); },
      enfocar: function (n, zoom) { cam.x = n.x; cam.y = n.y; cam.zoom = zoom || 2.4; vista(); limitar(); vista(); elegir(n, true); pedir(); },
      soltar: function () { fijo = null; elegir(null); },
      describir: function (n) { return describir(E, n); },
      png: function (ancho, tipo) { return exportarPNG(E, tema, ancho || 3200, op, tipo); },
      svg: function () { return exportarSVG(E, tema); },
      detener: function () { vivo = false; }
    };
    if (op.datos) iniciar(op.datos);
    else fetch(op.url || 'data/mapa.json').then(function (r) { return r.json(); }).then(iniciar).catch(function (e) { if (global.console) console.warn('mapa cognitivo: sin datos', e); });
    return api;
  }

  /* ---------------------------------------------------------------- exportación */
  function exportarPNG(E, tema, ancho, op, tipo) {
    var c = document.createElement('canvas'), alto = Math.round(ancho * H / W);
    c.width = ancho; c.height = alto;
    var v = { cw: ancho, ch: alto, dpr: 1, z: ancho / W, cx: W / 2, cy: H / 2, fw: 1, ft: 1 };
    pintarEstatico(c.getContext('2d'), E, tema, v, { fondoPropio: (op && op.fondoPropio) !== false, sinTexto: op && op.sinTexto });
    return new Promise(function (ok) { c.toBlob(ok, tipo || 'image/png', 0.92); });
  }
  function exportarSVG(E, tema) {
    var T = TEMAS[tema], o = [];
    function d(g) {
      if (g[0] === 'c') return 'M' + g.slice(1, 3).map(r1).join(' ') + 'C' + g.slice(3).map(r1).join(' ');
      if (g[0] === 'l') return 'M' + r1(g[1]) + ' ' + r1(g[2]) + 'L' + r1(g[3]) + ' ' + r1(g[4]);
      if (g[0] === 'p') return 'M' + g[1].map(function (p) { return r1(p[0]) + ' ' + r1(p[1]); }).join('L');
      if (g[0] === 'a') { var x0 = g[1] + Math.cos(g[4]) * g[3], y0 = g[2] + Math.sin(g[4]) * g[3], x1 = g[1] + Math.cos(g[5]) * g[3], y1 = g[2] + Math.sin(g[5]) * g[3]; return 'M' + r1(x0) + ' ' + r1(y0) + 'A' + r1(g[3]) + ' ' + r1(g[3]) + ' 0 ' + (g[5] - g[4] > Math.PI ? 1 : 0) + ' 1 ' + r1(x1) + ' ' + r1(y1); }
      return '';
    }
    function r1(x) { return Math.round(x * 10) / 10; }
    function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
    o.push('<?xml version="1.0" encoding="UTF-8"?>');
    o.push('<!-- Mapa cognitivo del capital · ' + VERSION + ' · semilla ' + SEED + ' · datos ' + esc((E.D.meta || {}).actualizado || '') + ' -->');
    o.push('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + W + ' ' + H + '" width="' + W + '" height="' + H + '" font-family="' + esc(MONO) + '">');
    if (T.fondo) o.push('<rect width="' + W + '" height="' + H + '" fill="' + T.fondo + '"/>');
    o.push('<g' + (T.luz ? ' style="mix-blend-mode:screen;isolation:isolate"' : '') + ' stroke-linecap="round" stroke-linejoin="round">');
    E.capas.forEach(function (L) {
      var s = T.estilo(L.id);
      if (L.tipo === 's') {
        var path = L.g.map(d).join('');
        if (s.halo && T.luz) o.push('<path d="' + path + '" fill="none" stroke="' + s.c + '" stroke-opacity="' + s.ha + '" stroke-width="' + (s.w || 0.5) * s.halo + '"/>');
        o.push('<path d="' + path + '" fill="none" stroke="' + s.c + '" stroke-opacity="' + s.a + '" stroke-width="' + (s.w || 0.5) + '"' + (s.dash ? ' stroke-dasharray="' + s.dash.join(' ') + '"' : '') + '/>');
      } else if (L.tipo === 'f') o.push('<path d="' + L.g.map(function (g) { return d(g) + 'Z'; }).join('') + '" fill="' + s.c + '" fill-opacity="' + s.a + '"/>');
      else if (L.tipo === 'd') o.push('<g fill="' + s.c + '" fill-opacity="' + s.a + '">' + L.g.map(function (g) { return '<circle cx="' + r1(g[1]) + '" cy="' + r1(g[2]) + '" r="' + g[3] + '"/>'; }).join('') + '</g>');
      else if (L.tipo === 't') o.push('<g fill="' + s.c + '">' + L.g.map(function (g) { return '<text x="' + r1(g[1]) + '" y="' + r1(g[2]) + '" font-size="' + g[4] + '" dominant-baseline="middle" text-anchor="' + ({ left: 'start', right: 'end', center: 'middle' })[g[5]] + '">' + esc(g[3]) + '</text>'; }).join('') + '</g>');
    });
    o.push('</g>');
    E.nodos.filter(function (n) { return n.clave; }).forEach(function (n) {
      o.push('<circle cx="' + r1(n.x) + '" cy="' + r1(n.y) + '" r="' + (n.tipo === 'estacion' ? 9 : 6.5) + '" fill="none" stroke="' + (T.luz ? '#cbbcff' : T.texto) + '" stroke-width=".7"/><circle cx="' + r1(n.x) + '" cy="' + r1(n.y) + '" r="2.6" fill="' + (T.luz ? '#f8f6ff' : T.texto) + '"/>');
    });
    E.etiquetas.forEach(function (e) {
      var n = e.n, lx = n.x + e.dx, ly = n.y + e.dy, w = Math.max(n.clave.length * 7.6, (n.cod + ' · ' + (e.sub || '')).length * 5.2) + 16, x0 = e.al === 'right' ? lx - w : lx, ex = e.al === 'right' ? x0 + w : x0;
      o.push('<path d="M' + r1(n.x) + ' ' + r1(n.y) + 'L' + r1(n.x + (ex - n.x) * 0.55) + ' ' + r1(ly) + 'L' + r1(ex) + ' ' + r1(ly) + '" fill="none" stroke="' + (T.luz ? '#9c8fe6' : T.tenue) + '" stroke-width=".6"/>');
      o.push('<rect x="' + r1(x0) + '" y="' + r1(ly - 17) + '" width="' + r1(w) + '" height="34" fill="' + T.etqFondo + '" stroke="' + (T.luz ? 'rgba(160,140,255,.35)' : 'rgba(24,34,53,.25)') + '" stroke-width=".5"/>');
      o.push('<text x="' + r1(x0 + 8) + '" y="' + r1(ly - 4.5) + '" font-size="8.5" fill="' + T.tenue + '">' + esc(n.cod + ' · ' + (e.sub || '')) + '</text>');
      o.push('<text x="' + r1(x0 + 8) + '" y="' + r1(ly + 10) + '" font-size="12.5" font-weight="500" fill="' + T.texto + '">' + esc(n.clave) + '</text>');
    });
    o.push('</svg>');
    return o.join('\n');
  }

  var MapaCognitivo = { montar: montar, VERSION: VERSION, SEED: SEED };
  global.MapaCognitivo = MapaCognitivo;

  /* ---------------------------------------------------------------- modo fondo automático */
  var yo = document.currentScript;
  if (yo && yo.getAttribute('data-modo') === 'fondo') {
    var arrancar = function () {
      var oscuro = global.matchMedia && global.matchMedia('(prefers-color-scheme: dark)').matches;
      var capa = document.createElement('div'); capa.className = 'mapa-fondo'; capa.setAttribute('aria-hidden', 'true');
      document.body.insertBefore(capa, document.body.firstChild);
      var base = (yo.getAttribute('src') || '').replace(/[^\/]*$/, '');
      var m = montar(capa, { modo: 'fondo', tema: oscuro ? 'fosforo' : 'tinta', url: yo.getAttribute('data-datos') || base + 'data/mapa.json',
        fondoPropio: false, atmosfera: oscuro, grano: false, sinTexto: true, pulsos: 6, escala: 1.02 });
      /* el mapa domina la portada y se retira al leer: baja hasta un 38 % al pasar la primera pantalla */
      var pend = false, atenuar = function () { pend = false; var f = Math.min(1, global.scrollY / (global.innerHeight * 0.9)); capa.style.setProperty('--mapa-desvanecer', (1 - f * 0.62).toFixed(3)); };
      global.addEventListener('scroll', function () { if (!pend) { pend = true; global.requestAnimationFrame(atenuar); } }, { passive: true }); atenuar();
      if (global.matchMedia) global.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) { m.tema(e.matches ? 'fosforo' : 'tinta'); });
    };
    if (document.body) arrancar(); else document.addEventListener('DOMContentLoaded', arrancar);
  }
})(window);
