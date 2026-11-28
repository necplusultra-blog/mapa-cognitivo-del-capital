/* Mapa cognitivo del capital — figura central del sitio (lámina 3.0, estilo de figura académica).
 *
 * Dos usos con el mismo motor:
 *   - fondo de página:  etiqueta script con src="mapa-cognitivo.js", data-modo="fondo" y defer
 *   - pestaña Mapa:     MapaCognitivo.montar(contenedor, {modo: 'mapa', alSeleccionar: fn})
 *
 * La figura tiene cuatro paneles ordenados sobre el eje de exposición categorial (estaciones 01–05):
 *   A  Estados Unidos: árbol de decisiones teóricas de los cálculos de la tasa de ganancia (anillos interiores,
 *      un anillo por decisión) y corona temporal de cada cálculo con sus quiebres estructurales.
 *   B  Mundo: el mismo esquema con la Penn World Table; las barras exteriores dan el número de países.
 *   C  Series publicadas en el sitio, agrupadas por la sección en que aparecen.
 *   D  Registro: percentiles 10–90 y 25–75 y mediana de los cálculos de EE.UU., y número de cálculos con
 *      quiebre en cada año.
 * Todo lo que se dibuja sale de site/data/mapa.json (sismografo/mapa.py): no hay elementos decorativos ni
 * aleatorios. La disposición es fija (sin semilla aleatoria); SEED se conserva sólo como identificador.
 * Sin dependencias.
 */
(function (global) {
  'use strict';
  var W = 1500, H = 960, SEED = 1867, VERSION = 'lámina 3.0';
  var EN = /^en/.test((document.documentElement.lang || '').toLowerCase());
  function L(es, en) { return EN ? en : es; }
  /* Textos editables: contenido/mapa.yml (o contenido/en/mapa.yml) → mapa-textos.js → window.MAPA_TEXTOS.
     T('lamina.titulo_a', es, en, {n: …}) devuelve el texto del YAML si existe y, si no, el de aquí.
     Las llaves {n}, {eeuu}… se reemplazan por los valores que se pasan en el último argumento. */
  function T(clave, es, en, vars) {
    var v = clave.split('.').reduce(function (o, k) { return o == null ? o : o[k]; }, global.MAPA_TEXTOS || null);
    var s = (typeof v === 'string' && v.trim()) ? v : (EN ? en : es);
    return vars ? s.replace(/\{(\w+)\}/g, function (m, k) { return k in vars ? vars[k] : m; }) : s;
  }
  function ruta(a) { if (!EN) return a; return a.replace(/^lectura\.html/, 'reading.html').replace(/^metodologia\.html/, 'methodology.html'); }
  function may(s) { s = String(s || ''); return s.charAt(0).toUpperCase() + s.slice(1); }
  function polar(cx, cy, r, a) { return [cx + Math.cos(a) * r, cy + Math.sin(a) * r]; }
  var RAD = Math.PI / 180;

  /* ---------------------------------------------------------------- disposición (coordenadas de la figura) */
  var EJE_Y = 450, EJE_X0 = 28, EJE_X1 = 1480;
  var GEO = {
    A: { cx: 410, cy: EJE_Y, a0: -174 * RAD, a1: -6 * RAD, r0: 30, rh: 268, t0: 282, t1: 372 },
    B: { cx: 1215, cy: EJE_Y, a0: -174 * RAD, a1: -6 * RAD, r0: 28, rh: 140, t0: 152, t1: 212, p0: 222, p1: 272 },
    C: { bus: 542, etq: 576, nodo: 606, hoja: 664, x0: 28, x1: 1480 },
    D: { x0: 92, x1: 1466, y0: 782, y1: 888, b0: 944, b1: 906, v0: 55, v1: 155 }
  };
  function ejeY() { return EJE_Y; }

  /* Estaciones del eje: orden de exposición de las categorías. Lo que muestra el sitio es manifestación
     fenoménica de la determinación categorial, no su demostración. */
  var ESTACIONES = [
    { k: T('lamina.estaciones.0.nombre', 'Lógica del capital', 'Logic of capital'), x: 64, a: 'lectura.html#estatuto', c: '#01',
      t: T('lamina.estaciones.0.descripcion', 'El valor que se valoriza como sujeto de la mediación social. La categoría se expone primero; las series del sitio son su manifestación fenoménica en precios, no su demostración.',
           'Self-valorising value as the subject of social mediation. The category is set out first; the series on the site are its phenomenal manifestation in prices, not its demonstration.') },
    { k: T('lamina.estaciones.1.nombre', 'Plusvalor y ganancia', 'Surplus value and profit'), x: GEO.A.cx, a: 'index.html#masa-tasa', c: '#02',
      t: T('lamina.estaciones.1.descripcion', 'Masa y tasa de plusvalor y de ganancia. Ninguna cuenta nacional las publica: se reconstruyen reclasificando excedente y remuneración según decisiones teóricas explícitas, cada una visible como un anillo del panel A.',
           'Mass and rate of surplus value and of profit. No national account publishes them: they are reconstructed by reclassifying surplus and compensation according to explicit theoretical decisions, each visible as a ring in panel A.') },
    { k: T('lamina.estaciones.2.nombre', 'Fuerzas productivas', 'Productive forces'), x: 700, a: 'index.html#fuerzas', c: '#03',
      t: T('lamina.estaciones.2.descripcion', 'Desarrollo de las fuerzas productivas: valor nuevo por hora, tiempo necesario y plustrabajo, en EE.UU. y en el mundo.',
           'Development of the productive forces: new value per hour, necessary time and surplus labour, in the United States and the world.') },
    { k: T('lamina.estaciones.3.nombre', 'Tiempo disponible', 'Disposable time'), x: 930, a: 'lectura.html#tiempo-disponible', c: '#04',
      t: T('lamina.estaciones.3.descripcion', 'Tiempo de trabajo y tiempo disponible: la medida del valor frente a la riqueza que ya no cabe en ella. Las horas registran la medida; el tiempo liberado registra su contradicción.',
           'Labour time and disposable time: the measure of value against the wealth that no longer fits within it. Hours record the measure; freed time records its contradiction.') },
    { k: T('lamina.estaciones.4.nombre', 'Límites inmanentes', 'Immanent limits'), x: GEO.B.cx, a: 'lectura.html#asintota', c: '#05',
      t: T('lamina.estaciones.4.descripcion', 'Hipótesis del capitalismo limítrofe y sus contratendencias. Lo que el sitio puede mostrar es si una tendencia aparece y bajo qué decisiones, a escala de EE.UU. y del mundo; no mide una distancia a un tope.',
           'The hypothesis of borderline capitalism and its countertendencies. What the site can show is whether a tendency appears and under which decisions, for the United States and the world; it does not measure a distance to a ceiling.') }
  ];

  /* ---------------------------------------------------------------- escena */
  function construirEscena(D) {
    var capas = {}, orden = [], nodos = [];
    function capa(id, tipo, z) { if (!capas[id]) { capas[id] = { id: id, tipo: tipo, z: z, g: [] }; orden.push(capas[id]); } return capas[id]; }
    function trazo(id, z, seg) { capa(id, 's', z).g.push(seg); }
    /* texto: ['t', x, y, cadena, tamaño, alineación, opciones {f: 'serif'|'sans', w: peso, rot: ángulo, it: cursiva}] */
    function texto(id, z, x, y, s, t, al, o) { capa(id, 't', z).g.push(['t', x, y, String(s), t, al || 'left', o || {}]); }
    function bez(p, c) {
      var rm = p.r + (c.r - p.r) * 0.5;
      var a = polar(p.cx, p.cy, p.r, p.a), b = polar(p.cx, p.cy, rm, p.a), d = polar(p.cx, p.cy, rm, c.a), e = polar(p.cx, p.cy, c.r, c.a);
      return ['c', a[0], a[1], b[0], b[1], d[0], d[1], e[0], e[1]];
    }
    var m = D.meta || {};

    /* ---- eje de exposición categorial */
    trazo('eje', 20, ['l', EJE_X0, EJE_Y, EJE_X1, EJE_Y]);
    texto('eje:tit', 21, EJE_X1, EJE_Y + 36, T('lamina.eje_titulo', 'orden de exposición categorial →', 'order of categorial exposition →'), 13, 'right', { f: 'sans', it: true });
    ESTACIONES.forEach(function (e, i) {
      e.y = EJE_Y;
      var n = { tipo: 'estacion', x: e.x, y: e.y, est: i, clave: e.k, cod: e.c, peso: 3, hijos: [] };
      nodos.push(n); e.nodo = n;
      trazo('eje:marca', 21, ['l', e.x, EJE_Y - 6, e.x, EJE_Y + 6]);
      texto('est:num', 22, e.x, EJE_Y + 18, '0' + (i + 1), 13.5, i === 0 ? 'left' : 'center', { f: 'sans', w: 600 });
      texto('est:nom', 22, e.x, EJE_Y + 36, e.k, 16, i === 0 ? 'left' : 'center', { f: 'serif' });
    });

    /* ---- árbol radial de decisiones (paneles A y B) */
    function arbolRadial(def, cfg) {
      if (EN && def.dims_en) def.dims = def.dims_en;
      var hojas = [], todos = [], pmax = 0;
      function rec(n, prof, padre, camino) {
        var N = { tipo: n.s ? 'hoja' : 'decision', prof: prof, padre: padre, hijos: [], dim: n.d, opt: n.o, camino: camino, arbol: cfg.nombre, peso: n.s ? 1 : 1.4 };
        todos.push(N);
        if (n.s) { N.spec = n.s[0]; hojas.push(N); }
        else { pmax = Math.max(pmax, prof); n.h.forEach(function (h, j) { N.hijos.push(rec(h, prof + 1, N, camino.concat(j))); }); }
        return N;
      }
      var raiz = rec(def.arbol, 0, null, []);
      /* separación angular: más espacio donde las ramas se separan antes (lectura del árbol) */
      var pos = 0, prev = null;
      hojas.forEach(function (h) {
        if (prev) { var k = 0; while (k < h.camino.length && h.camino[k] === prev.camino[k]) k++; pos += 1 + (k === 0 ? 3.2 : k === 1 ? 1.5 : k === 2 ? 0.55 : 0); }
        h.t = pos; prev = h;
      });
      var Tt = pos || 1, dr = (cfg.rh - cfg.r0 - 14) / Math.max(1, pmax);
      cfg.dr = dr; cfg.pmax = pmax;
      function colocar(N) {
        if (N.hijos.length) { N.hijos.forEach(colocar); N.a = (N.hijos[0].a + N.hijos[N.hijos.length - 1].a) / 2; N.n = N.hijos.reduce(function (s, c) { return s + c.n; }, 0); N.r = cfg.r0 + N.prof * dr; }
        else { N.a = cfg.a0 + (cfg.a1 - cfg.a0) * N.t / Tt; N.n = 1; N.r = cfg.rh; }
        N.cx = cfg.cx; N.cy = cfg.cy;
        var p = polar(cfg.cx, cfg.cy, N.r, N.a); N.x = p[0]; N.y = p[1];
      }
      colocar(raiz);
      var est = ESTACIONES[cfg.est];
      raiz.seg = ['l', est.x, est.y, raiz.x, raiz.y];
      raiz.padreEst = est.nodo;
      var pref = cfg.nombre === 'mundo' ? 'bw' : 'ar';
      trazo(pref + ':0:4', 10, raiz.seg);
      todos.forEach(function (N) {
        nodos.push(N);
        if (!N.padre) return;
        N.seg = bez(N.padre, N);
        var w = 0.35 + 2.4 * Math.pow(N.n / raiz.n, 0.55);
        trazo(pref + ':' + Math.min(9, N.prof) + ':' + Math.round(w * 2), 10, N.seg);
      });
      hojas.forEach(function (h) { capa(pref + ':hoja', 'd', 14).g.push(['d', h.x, h.y, 1.1]); });
      /* guías: un anillo por nivel de decisión, numerado en el extremo izquierdo */
      var ext = cfg.a0 - 3.2 * RAD;
      for (var pr = 0; pr <= pmax; pr++) {
        var rr = cfg.r0 + pr * dr;
        capa('guia', 's', 9).g.push(['a', cfg.cx, cfg.cy, rr, cfg.a0 - 0.02, cfg.a1 + 0.02]);
        var q = polar(cfg.cx, cfg.cy, rr, ext);
        texto('guia:num', 17, q[0], q[1], String(pr + 1), 11, 'center', { f: 'sans', w: 600 });
      }
      capa('guia', 's', 9).g.push(['a', cfg.cx, cfg.cy, cfg.rh, cfg.a0 - 0.02, cfg.a1 + 0.02]);
      /* nivel → decisión más frecuente en ese nivel (para la leyenda) */
      var porNivel = [];
      todos.forEach(function (N) { if (N.hijos.length) { var c = porNivel[N.prof] || (porNivel[N.prof] = {}); c[N.dim] = (c[N.dim] || 0) + 1; } });
      var niveles = porNivel.map(function (c) { var mejor = null; Object.keys(c).forEach(function (k) { if (mejor === null || c[k] > c[mejor]) mejor = k; }); return def.dims[+mejor][0]; });
      /* corona temporal: cada radio prolonga una especificación de y0 (dentro) a y1 (fuera); puntos = quiebres */
      var a0 = cfg.a0 - 0.02, a1 = cfg.a1 + 0.02;
      function rA(y) { return cfg.t0 + (y - cfg.y0) / (cfg.y1 - cfg.y0) * (cfg.t1 - cfg.t0); }
      cfg.rA = rA;
      hojas.forEach(function (h) {
        var s = def.specs[h.spec]; h.datos = s;
        var p = polar(cfg.cx, cfg.cy, cfg.t0, h.a), q = polar(cfg.cx, cfg.cy, cfg.t1, h.a);
        h.pelo = ['l', p[0], p[1], q[0], q[1]];
        trazo(pref + ':radio', 11, ['l', h.x, h.y, p[0], p[1]]);
        trazo(pref + ':radio', 11, h.pelo);
        h.quiebres = (s[2] || []).map(function (y) { var z = polar(cfg.cx, cfg.cy, rA(y), h.a); capa('quiebre', 'd', 16).g.push(['d', z[0], z[1], 1.05]); return z; });
      });
      for (var y = Math.ceil(cfg.y0 / 10) * 10; y <= cfg.y1; y += 10) {
        capa('decada', 's', 12).g.push(['a', cfg.cx, cfg.cy, rA(y), a0, a1]);
        if ((y - 1950) % 30) continue;
        var lp = polar(cfg.cx, cfg.cy, rA(y), cfg.a1 + 2.6 * RAD);
        texto('decada:txt', 17, lp[0], lp[1], String(y), 11, 'center', { f: 'sans', rot: cfg.a1 + 2.6 * RAD + Math.PI / 2 });
      }
      [cfg.t0, cfg.t1].forEach(function (r) { capa('corona', 's', 12).g.push(['a', cfg.cx, cfg.cy, r, a0, a1]); });
      var cuenta = {}, cmax = 1;
      hojas.forEach(function (h) { (h.datos[2] || []).forEach(function (y) { cuenta[y] = (cuenta[y] || 0) + 1; if (cuenta[y] > cmax) cmax = cuenta[y]; }); });
      var crisis = [];
      Object.keys(cuenta).forEach(function (y) { if (cuenta[y] / hojas.length >= 0.5) { crisis.push(+y); capa('crisis', 's', 13).g.push(['a', cfg.cx, cfg.cy, rA(+y), a0, a1]); } });
      return { raiz: raiz, hojas: hojas, todos: todos, cfg: cfg, cuenta: cuenta, niveles: niveles, crisis: crisis };
    }

    var finEEUU = m.eeuu_fin || 2025, finMundo = m.mundo_fin || 2023;
    var eeuu = arbolRadial(D.eeuu, { nombre: 'eeuu', est: 1, cx: GEO.A.cx, cy: GEO.A.cy, a0: GEO.A.a0, a1: GEO.A.a1, r0: GEO.A.r0, rh: GEO.A.rh,
      t0: GEO.A.t0, t1: GEO.A.t1, y0: 1948, y1: finEEUU });
    var mundo = arbolRadial(D.mundo, { nombre: 'mundo', est: 4, cx: GEO.B.cx, cy: GEO.B.cy, a0: GEO.B.a0, a1: GEO.B.a1, r0: GEO.B.r0, rh: GEO.B.rh,
      t0: GEO.B.t0, t1: GEO.B.t1, y0: 1960, y1: finMundo });
    /* B: número de países de cada especificación mundial (barra radial proporcional) */
    var pmaxPaises = Math.max.apply(null, [1].concat(mundo.hojas.map(function (h) { return h.datos[1] || 0; })));
    mundo.hojas.forEach(function (h) {
      var n = h.datos[1] || 0, p = polar(GEO.B.cx, GEO.B.cy, GEO.B.p0, h.a), q = polar(GEO.B.cx, GEO.B.cy, GEO.B.p0 + (GEO.B.p1 - GEO.B.p0) * n / pmaxPaises, h.a);
      trazo('pais', 11, ['l', p[0], p[1], q[0], q[1]]);
    });
    var lpB = polar(GEO.B.cx, GEO.B.cy, GEO.B.p1 + 4, GEO.B.a0 - 1.5 * RAD);
    texto('decada:txt', 17, lpB[0], lpB[1], T('lamina.b_paises', 'n.º de países (máx. {n})', 'no. of countries (max. {n})', { n: pmaxPaises }), 11.5, 'right', { f: 'sans', it: true });

    /* empalmes de las series de EE.UU. (meta.json): clasificaciones industriales SIC → NAICS */
    var emp = m.empalmes || {};
    var aniosEmp = Object.keys(emp).map(function (k) { return +k.slice(0, 4); }).filter(function (y) { return y > 1900; });
    if (!aniosEmp.length) aniosEmp = [1987, 1997];
    aniosEmp.forEach(function (y) { capa('empalme', 's', 15).g.push(['a', GEO.A.cx, GEO.A.cy, eeuu.cfg.rA(y), GEO.A.a0 - 0.02, GEO.A.a1 + 0.02]); });
    var ym = aniosEmp.reduce(function (s, y) { return s + y; }, 0) / aniosEmp.length;
    var pe = polar(GEO.A.cx, GEO.A.cy, eeuu.cfg.rA(ym), -60 * RAD);
    var empNodo = { tipo: 'empalme', x: pe[0], y: pe[1], clave: T('lamina.empalme_nombre', 'Empalme estadístico', 'Statistical splice'), cod: '#08', empalmes: emp, peso: 3, hijos: [] };
    nodos.push(empNodo);

    /* ---- C: series publicadas, por sección, colgando de su estación */
    var familias = [], fams = (D.familias || []).slice().map(function (f, i) { return { f: f, i: i }; });
    fams.sort(function (a, b) { return a.f.e - b.f.e || a.i - b.i; });
    var peso = fams.map(function (x) { return 2 + Math.sqrt(x.f.s.length); }), tot = peso.reduce(function (s, x) { return s + x; }, 0);
    var x = GEO.C.x0, anchoTot = GEO.C.x1 - GEO.C.x0, porEst = {};
    fams.forEach(function (x0, i) {
      var f = x0.f, w = peso[i] / tot * anchoTot, fx = x + w / 2, est = ESTACIONES[f.e];
      var F = { tipo: 'familia', nombre: may(EN ? (f.n_en || f.n) : f.n), ancla: f.a, series: f.s, glosa: (EN ? f.g_en : f.g) || [], est: f.e, x: fx, y: GEO.C.nodo, ancho: w, hijos: [], peso: 2, n: f.s.length };
      F.seg = ['p', [[est.x, EJE_Y + 46], [est.x, GEO.C.bus], [fx, GEO.C.bus], [fx, F.y]]];
      F.padreEst = est.nodo;
      (porEst[f.e] = porEst[f.e] || []).push(F);
      trazo('fam:tronco', 10, ['l', fx, GEO.C.bus, fx, F.y]);
      nodos.push(F); familias.push(F);
      var pad = 7, xs0 = x + pad, xs1 = x + w - pad, ns = f.s.length;
      f.s.forEach(function (s, j) {
        var sx = ns > 1 ? xs0 + (xs1 - xs0) * j / (ns - 1) : fx;
        var S = { tipo: 'serie', nombre: s, glosa: F.glosa[j] || [s, '', ''], familia: F, padre: F, x: sx, y: GEO.C.hoja, prof: 2, hijos: [], peso: 1, n: 1 };
        S.seg = ['c', fx, F.y, fx, F.y + 34, sx, S.y - 30, sx, S.y]; F.hijos.push(S);
        trazo('fam:rama', 10, S.seg);
        capa('serie', 'd', 14).g.push(['d', S.x, S.y, 1.5]);
        nodos.push(S);
      });
      capa('fam:nodo', 'd', 14).g.push(['d', fx, F.y, 2.4]);
      F.lineas = partir(F.nombre, w - 8, 14.5);
      x += w;
    });
    /* barra de cada estación hacia sus secciones */
    Object.keys(porEst).forEach(function (k) {
      var est = ESTACIONES[+k], fs = porEst[k], xa = Math.min(est.x, fs[0].x), xb = Math.max(est.x, fs[fs.length - 1].x);
      trazo('fam:bus', 10, ['l', est.x, EJE_Y + 46, est.x, GEO.C.bus]);
      trazo('fam:bus', 10, ['l', xa, GEO.C.bus, xb, GEO.C.bus]);
    });

    /* ---- D: registro temporal de los cálculos de EE.UU. */
    var G = GEO.D, Y0 = 1948, Y1 = finEEUU;
    function xa(y) { return G.x0 + (y - Y0) / (Y1 - Y0) * (G.x1 - G.x0); }
    function yb(v) { return G.y1 - (v - G.v0) / (G.v1 - G.v0) * (G.y1 - G.y0); }
    var B = D.bandas || [];
    if (B.length) {
      var lo = Math.min.apply(null, B.map(function (b) { return b[1]; })), hi = Math.max.apply(null, B.map(function (b) { return b[5]; }));
      G.v0 = Math.floor((lo - 5) / 20) * 20; G.v1 = Math.ceil((hi + 5) / 20) * 20;
      var p90 = B.map(function (b) { return [xa(b[0]), yb(b[5])]; }), p10 = B.map(function (b) { return [xa(b[0]), yb(b[1])]; }).reverse();
      var p75 = B.map(function (b) { return [xa(b[0]), yb(b[4])]; }), p25 = B.map(function (b) { return [xa(b[0]), yb(b[2])]; }).reverse();
      capa('d:banda90', 'f', 3).g.push(['p', p90.concat(p10)]);
      capa('d:banda50', 'f', 3).g.push(['p', p75.concat(p25)]);
      trazo('d:p50', 4, ['p', B.map(function (b) { return [xa(b[0]), yb(b[3])]; })]);
    }
    var paso = (G.v1 - G.v0) > 80 ? 40 : 20; G.v0 = Math.floor(G.v0 / paso) * paso; G.v1 = Math.ceil(G.v1 / paso) * paso;
    for (var v = G.v0; v <= G.v1; v += paso) {
      trazo(v === 100 ? 'd:ref' : 'd:rejilla', 2, ['l', G.x0, yb(v), G.x1, yb(v)]);
      texto('d:txt', 5, G.x0 - 8, yb(v), String(v), 11.5, 'right', { f: 'sans' });
    }
    texto('d:txt', 5, G.x0 - 34, (G.y0 + G.y1) / 2, T('lamina.d_eje_y', 'índice (100 = promedio)', 'index (100 = average)'), 11, 'center', { f: 'sans', it: true, rot: -Math.PI / 2 });
    var Q = {}, qmax = 1; (D.quiebres || []).forEach(function (q) { Q[q[0]] = q[1]; if (q[1] > qmax) qmax = q[1]; });
    (D.quiebres || []).forEach(function (q) { if (q[1] > 0) trazo('d:barra', 4, ['l', xa(q[0]), G.b0, xa(q[0]), G.b0 - q[1] / qmax * (G.b0 - G.b1)]); });
    trazo('d:base', 4, ['l', G.x0, G.b0, G.x1, G.b0]);
    for (var yy = 1950; yy <= Y1; yy += 10) { trazo('d:base', 4, ['l', xa(yy), G.b0, xa(yy), G.b0 + 5]); texto('d:txt', 5, xa(yy), G.b0 + 15, String(yy), 12, 'center', { f: 'sans' }); }
    (D.quiebres || []).slice().sort(function (a, b) { return b[1] - a[1]; }).slice(0, 5).forEach(function (q) { texto('d:pico', 5, xa(q[0]), G.b0 - q[1] / qmax * (G.b0 - G.b1) - 8, String(q[0]), 11.5, 'center', { f: 'sans', w: 600 }); });
    texto('d:ley', 5, G.x1, G.y0 - 10, T('lamina.d_leyenda', 'bandas: percentiles 10–90 y 25–75 · línea: mediana', 'bands: 10th–90th and 25th–75th percentiles · line: median'), 12, 'right', { f: 'sans', it: true });
    texto('d:ley', 5, G.x1, G.b1 - 8, T('lamina.d_barras', 'barras: cálculos con quiebre estructural en el año (de {n})', 'bars: calculations with a structural break in the year (of {n})', { n: eeuu.hojas.length }), 12, 'right', { f: 'sans', it: true });

    /* ---- títulos de panel (estilo de figura) */
    function titulo(x, y, letra, t, sub) {
      texto('panel:letra', 30, x, y, letra, 26, 'left', { f: 'serif', w: 700 });
      texto('panel:tit', 30, x + 26, y, t, 18.5, 'left', { f: 'serif', w: 600 });
      if (sub) sub.forEach(function (s, i) { texto('panel:sub', 30, x + 26, y + 22 + i * 16, s, 13, 'left', { f: 'sans' }); });
    }
    titulo(26, 34, 'A', T('lamina.titulo_a', 'Estados Unidos: {n} cálculos de la tasa de ganancia, {y0}–{y1}', 'United States: {n} calculations of the rate of profit, {y0}–{y1}', { n: eeuu.hojas.length, y0: 1948, y1: finEEUU }),
      [T('lamina.sub_a', 'Anillos interiores: decisiones teóricas · corona: cada cálculo en el tiempo', 'Inner rings: theoretical decisions · outer band: each calculation over time')]);
    titulo(938, 34, 'B', T('lamina.titulo_b', 'Mundo: {n} cálculos con la Penn World Table, {y0}–{y1}', 'World: {n} calculations with the Penn World Table, {y0}–{y1}', { n: mundo.hojas.length, y0: 1960, y1: finMundo }),
      [T('lamina.sub_b', 'Mismo esquema que A; barras exteriores: países incluidos', 'Same layout as A; outer bars: countries included')]);
    titulo(26, 514, 'C', T('lamina.titulo_c', 'Series publicadas, por sección ({n})', 'Published series, by section ({n})', { n: familias.reduce(function (s, f) { return s + f.n; }, 0) }));
    titulo(26, 744, 'D', T('lamina.titulo_d', 'Dispersión de los cálculos de EE.UU. y quiebres estructurales, {y0}–{y1}', 'Spread of the US calculations and structural breaks, {y0}–{y1}', { y0: 1948, y1: finEEUU }));
    /* leyenda de los anillos de A (columna entre A y B) */
    var lx = 800, ly = 122;
    texto('ley:tit', 30, lx, ly, T('lamina.leyenda_anillos', 'Anillos de A, del centro hacia fuera', 'Rings of A, from the centre outwards'), 13, 'left', { f: 'sans', w: 600 });
    eeuu.niveles.forEach(function (nm, i) { texto('ley:num', 30, lx + 8, ly + 22 + i * 18, String(i + 1), 12, 'center', { f: 'sans', w: 600 }); texto('ley:txt', 30, lx + 20, ly + 22 + i * 18, nm, 12.5, 'left', { f: 'sans' }); });
    var ly2 = ly + 22 + eeuu.niveles.length * 18 + 8;
    [[T('lamina.leyenda_hojas', 'cálculos (hojas)', 'calculations (leaves)'), 'hoja'], [T('lamina.leyenda_corona', 'corona: años {y0}–{y1}', 'outer band: years {y0}–{y1}', { y0: 1948, y1: finEEUU }), 'corona'],
     [T('lamina.leyenda_quiebre', 'quiebre estructural', 'structural break'), 'quiebre'], [T('lamina.leyenda_crisis', 'año con quiebre en ≥ 50 %', 'year with breaks in ≥ 50%'), 'crisis'],
     [T('lamina.leyenda_empalme', 'empalme SIC → NAICS', 'SIC → NAICS splice'), 'empalme']].forEach(function (l, i) {
      var yy2 = ly2 + i * 18; capa('ley:sim:' + l[1], l[1] === 'hoja' || l[1] === 'quiebre' ? 'd' : 's', 30).g.push(l[1] === 'hoja' || l[1] === 'quiebre' ? ['d', lx + 8, yy2, 2.2] : ['l', lx + 1, yy2, lx + 15, yy2]);
      texto('ley:txt', 30, lx + 20, yy2, l[0], 12.5, 'left', { f: 'sans' });
    });
    /* pie de la figura */
    var fecha = (m.actualizado || '').slice(0, 10);
    texto('pie', 30, W - 20, 12, T('lamina.pie', 'Mapa cognitivo del capital · datos: {fecha}', 'Cognitive Map of Capital · data: {fecha}', { fecha: m.actualizado || '—' }) + (m.commit ? ' · commit ' + m.commit : ''), 9.5, 'right', { f: 'sans' });

    /* ---- nodos clave */
    var bifurcacion = null, dimD2 = (D.eeuu.claves || []).indexOf('D2');
    eeuu.todos.forEach(function (N) { if (!bifurcacion && N.tipo === 'decision' && N.dim === dimD2) bifurcacion = N; });
    eeuu.raiz.clave = T('lamina.raiz_nombre', 'Árbol de decisiones de EE.UU.', 'US decision tree'); eeuu.raiz.cod = '#06';
    if (bifurcacion) { bifurcacion.clave = T('lamina.bifurcacion_nombre', 'Qué cuenta como plusvalor', 'What counts as surplus value'); bifurcacion.cod = '#07'; }

    orden.sort(function (a, b) { return a.z - b.z; });
    var zonas = {
      todo: [W / 2, H / 2], A: [GEO.A.cx, 250], B: [GEO.B.cx, 330], C: [754, 600], D: [780, 860], eje: [560, EJE_Y + 20], leyenda: [880, 230]
    };
    return { capas: orden, nodos: nodos, etiquetas: [], eeuu: eeuu, mundo: mundo, familias: familias, estaciones: ESTACIONES, empalme: empNodo,
      D: D, fecha: fecha, zonas: zonas, W: W, H: H };
  }
  /* parte un rótulo en líneas que quepan en un ancho dado (aprox. 0,5 em por carácter en la sans condensada) */
  function partir(s, ancho, t) {
    var max = Math.max(6, Math.floor(ancho / (t * 0.5))), pal = s.split(' '), out = [], l = '';
    pal.forEach(function (p) { if ((l + ' ' + p).trim().length > max && l) { out.push(l); l = p; } else l = (l + ' ' + p).trim(); });
    if (l) out.push(l);
    return out.slice(0, 3);
  }

  /* ---------------------------------------------------------------- temas
     nocturno (pestaña Mapa y fondo oscuro): tinta sobre pizarra, sin brillos.
     tinta (fondo claro): la misma figura sobre papel. Los nombres «fosforo»/«tinta» se conservan por compatibilidad. */
  var PALETAS = {
    fosforo: { fondo: '#0f1217', texto: '#e8e4d8', tenue: '#9b978b', regla: '#3a3f48', A: '#d6c39a', B: '#8cc0bd', C: '#aab4c2', Q: '#e2673f', E: '#7ea6d8', etqFondo: 'rgba(15,18,23,.86)' },
    tinta: { fondo: null, texto: '#1c2331', tenue: '#5d6878', regla: '#c3c9c8', A: '#6b4f1f', B: '#1d6d78', C: '#4a5566', Q: '#b8361f', E: '#2f5f9a', etqFondo: 'rgba(237,240,239,.86)' }
  };
  function estilo(P, id) {
    var p = id.split(':');
    if (p[0] === 'ar' || p[0] === 'bw') {
      var col = p[0] === 'ar' ? P.A : P.B;
      if (p[1] === 'hoja') return { c: col, a: 0.75 };
      if (p[1] === 'radio') return { c: col, a: 0.13, w: 0.45 };
      var d = +p[1], w = +p[2] / 2, t = Math.min(1, d / 8); return { c: col, a: 0.85 - t * 0.35, w: w };
    }
    return ({
      'eje': { c: P.texto, a: 0.9, w: 1.4 }, 'eje:marca': { c: P.texto, a: 0.9, w: 1.2 }, 'eje:tit': { c: P.tenue, a: 1 },
      'est:num': { c: P.texto, a: 1 }, 'est:nom': { c: P.texto, a: 0.92 },
      'guia': { c: P.tenue, a: 0.28, w: 0.5, dash: [1, 3] }, 'guia:num': { c: P.tenue, a: 1 },
      'decada': { c: P.tenue, a: 0.25, w: 0.4 }, 'decada:txt': { c: P.tenue, a: 1 }, 'corona': { c: P.tenue, a: 0.55, w: 0.6 },
      'crisis': { c: P.Q, a: 0.35, w: 1.1 }, 'quiebre': { c: P.Q, a: 0.9 }, 'empalme': { c: P.E, a: 0.75, w: 0.8, dash: [4, 3] },
      'pais': { c: P.B, a: 0.65, w: 1.1 },
      'fam:tronco': { c: P.C, a: 0.7, w: 1 }, 'fam:bus': { c: P.C, a: 0.7, w: 1 }, 'fam:rama': { c: P.C, a: 0.45, w: 0.55 }, 'fam:nodo': { c: P.texto, a: 1 }, 'serie': { c: P.C, a: 0.95 },
      'd:banda90': { c: P.A, a: 0.16 }, 'd:banda50': { c: P.A, a: 0.24 }, 'd:p50': { c: P.texto, a: 0.95, w: 1.3 },
      'd:rejilla': { c: P.regla, a: 0.6, w: 0.5 }, 'd:ref': { c: P.tenue, a: 0.8, w: 0.7, dash: [3, 3] }, 'd:barra': { c: P.Q, a: 0.85, w: 2.2 }, 'd:base': { c: P.tenue, a: 0.8, w: 0.7 },
      'd:txt': { c: P.tenue, a: 1 }, 'd:pico': { c: P.Q, a: 1 }, 'd:ley': { c: P.tenue, a: 1 },
      'panel:letra': { c: P.texto, a: 1 }, 'panel:tit': { c: P.texto, a: 1 }, 'panel:sub': { c: P.tenue, a: 1 },
      'ley:tit': { c: P.texto, a: 1 }, 'ley:num': { c: P.A, a: 1 }, 'ley:txt': { c: P.tenue, a: 1 },
      'ley:sim:hoja': { c: P.A, a: 1 }, 'ley:sim:corona': { c: P.tenue, a: 0.8, w: 1 }, 'ley:sim:quiebre': { c: P.Q, a: 1 }, 'ley:sim:crisis': { c: P.Q, a: 0.6, w: 1.6 }, 'ley:sim:empalme': { c: P.E, a: 0.9, w: 1, dash: [4, 3] },
      'pie': { c: P.tenue, a: 0.9 }
    })[id] || { c: P.texto, a: 0.4, w: 0.5 };
  }

  /* ---------------------------------------------------------------- dibujo */
  var SERIF = "'Newsreader','Iowan Old Style',Georgia,serif";
  var SANS = "'IBM Plex Sans Condensed','Arial Narrow',system-ui,sans-serif";
  function trazar(ctx, g) {
    if (g[0] === 'c') { ctx.moveTo(g[1], g[2]); ctx.bezierCurveTo(g[3], g[4], g[5], g[6], g[7], g[8]); }
    else if (g[0] === 'l') { ctx.moveTo(g[1], g[2]); ctx.lineTo(g[3], g[4]); }
    else if (g[0] === 'p') { var p = g[1]; ctx.moveTo(p[0][0], p[0][1]); for (var i = 1; i < p.length; i++) ctx.lineTo(p[i][0], p[i][1]); }
    else if (g[0] === 'a') { ctx.moveTo(g[1] + Math.cos(g[4]) * g[3], g[2] + Math.sin(g[4]) * g[3]); ctx.arc(g[1], g[2], g[3], g[4], g[5]); }
  }
  function fuente(o, px) { return (o.it ? 'italic ' : '') + (o.w || 400) + ' ' + px + 'px ' + (o.f === 'serif' ? SERIF : SANS); }
  function pintarEstatico(ctx, E, tema, v, op) {
    var P = PALETAS[tema] || PALETAS.fosforo, f = v.fw;
    ctx.save();
    ctx.setTransform(v.dpr, 0, 0, v.dpr, 0, 0);
    ctx.clearRect(0, 0, v.cw, v.ch);
    if (P.fondo && op.fondoPropio !== false) { ctx.fillStyle = P.fondo; ctx.fillRect(0, 0, v.cw, v.ch); }
    ctx.setTransform(v.dpr * v.z, 0, 0, v.dpr * v.z, v.dpr * (v.cw / 2 - v.cx * v.z), v.dpr * (v.ch / 2 - v.cy * v.z));
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    var minW = 0.45 / v.z, minT = 9.5 / v.z;
    E.capas.forEach(function (Lc) {
      if ((op.sinTexto || v.etq === false) && Lc.tipo === 't') return;
      if (Lc.id === 'pie' && !op.exportar) return;
      var s = estilo(P, Lc.id);
      if (Lc.tipo === 's') {
        ctx.beginPath(); Lc.g.forEach(function (g) { trazar(ctx, g); });
        ctx.setLineDash(s.dash ? s.dash.map(function (d) { return d * f; }) : []);
        ctx.strokeStyle = s.c; ctx.globalAlpha = s.a; ctx.lineWidth = Math.max(minW, (s.w || 0.5) * f); ctx.stroke();
      } else if (Lc.tipo === 'f') {
        ctx.beginPath(); Lc.g.forEach(function (g) { trazar(ctx, g); ctx.closePath(); }); ctx.fillStyle = s.c; ctx.globalAlpha = s.a; ctx.fill();
      } else if (Lc.tipo === 'd') {
        ctx.beginPath(); Lc.g.forEach(function (g) { var r = Math.max(0.5 / v.z, g[3] * f); ctx.moveTo(g[1] + r, g[2]); ctx.arc(g[1], g[2], r, 0, 6.2832); });
        ctx.fillStyle = s.c; ctx.globalAlpha = s.a; ctx.fill();
      } else if (Lc.tipo === 't') {
        ctx.fillStyle = s.c; ctx.globalAlpha = s.a; ctx.textBaseline = 'middle';
        Lc.g.forEach(function (g) {
          var o = g[6] || {}, px = Math.max(g[4] * v.ft, minT);
          ctx.font = fuente(o, px); ctx.textAlign = g[5];
          if (o.rot) { ctx.save(); ctx.translate(g[1], g[2]); ctx.rotate(o.rot); ctx.fillText(g[3], 0, 0); ctx.restore(); }
          else ctx.fillText(g[3], g[1], g[2]);
        });
      }
    });
    ctx.setLineDash([]); ctx.globalAlpha = 1;
    if (!op.sinTexto && v.etq !== false) pintarRotulos(ctx, E, P, v);
    /* marcadores de los nodos clave: anillo y número */
    E.nodos.filter(function (n) { return n.cod; }).forEach(function (n) {
      var est = n.tipo === 'estacion', r = (est ? 5 : 6) * f;
      ctx.globalAlpha = 1; ctx.fillStyle = P.fondo || '#edf0ef'; ctx.beginPath(); ctx.arc(n.x, n.y, r, 0, 6.2832); ctx.fill();
      ctx.strokeStyle = n.tipo === 'empalme' ? P.E : P.texto; ctx.lineWidth = Math.max(minW, 1.1 * f); ctx.stroke();
      ctx.fillStyle = n.tipo === 'empalme' ? P.E : P.texto; ctx.beginPath(); ctx.arc(n.x, n.y, 1.8 * f, 0, 6.2832); ctx.fill();
      if (est || op.sinTexto || v.etq === false) return;
      var px = Math.max(12 * v.ft, minT); ctx.font = fuente({ f: 'sans', w: 600 }, px); ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
      var etq = n.cod.slice(1) + ' ' + n.clave, tx = n.x + r + 4 * f, ty = n.y;
      ctx.globalAlpha = 0.9; ctx.fillStyle = P.etqFondo; var tw = ctx.measureText(etq).width; ctx.fillRect(tx - 2 * f, ty - px * 0.65, tw + 4 * f, px * 1.3);
      ctx.globalAlpha = 1; ctx.fillStyle = n.tipo === 'empalme' ? P.E : P.texto; ctx.fillText(etq, tx, ty);
    });
    ctx.restore();
  }
  /* rótulos de las secciones (C) y, al acercarse, el nombre y la expresión de cada serie */
  function pintarRotulos(ctx, E, P, v) {
    var minT = 9.5 / v.z, f = v.fw, cerca = v.z >= 1.15;   // las expresiones aparecen cuando la escala real lo permite
    ctx.textBaseline = 'middle';
    E.familias.forEach(function (F) {
      var px = Math.max(14.5 * v.ft, minT), lin = F.lineas || [F.nombre];
      ctx.font = fuente({ f: 'serif', w: 600 }, px); ctx.textAlign = 'center'; ctx.fillStyle = P.texto; ctx.globalAlpha = 1;
      lin.forEach(function (l, i) { ctx.fillText(l, F.x, GEO.C.etq + (i - lin.length + 1) * px * 1.15); });
      ctx.font = fuente({ f: 'sans' }, Math.max(11 * v.ft, minT)); ctx.fillStyle = P.tenue;
      ctx.textAlign = 'left'; ctx.fillText(String(F.n), F.x + 6 * f, F.y);
      if (!cerca) return;
      var plena = v.famSel === F;
      ctx.font = fuente({ f: 'sans' }, Math.max(8.8 * v.ft, minT * 0.9));
      F.hijos.forEach(function (S) {
        var g = S.glosa || [S.nombre, '', ''], opr = g[1] && /[\/=·−+Σ×]/.test(g[1]);
        if (!plena && !opr) return;
        var txt = plena ? (opr ? g[1] + '  ' : '') + g[0] : g[1].replace(/ · 1982 = 100$/, '');
        if (txt.length > 46) txt = txt.slice(0, 45) + '…';
        ctx.save(); ctx.translate(S.x, S.y + 5 * f); ctx.rotate(Math.PI / 2); ctx.textAlign = 'left'; ctx.fillStyle = P.tenue; ctx.fillText(txt, 0, 0); ctx.restore();
      });
    });
    ctx.globalAlpha = 1;
  }

  /* ---------------------------------------------------------------- consultas para el panel */
  function cadena(n) { var c = []; while (n) { c.push(n); n = n.padre || n.padreEst || null; } return c; }
  function hojasDe(n) { if (n.tipo === 'hoja') return [n]; var r = []; (n.hijos || []).forEach(function (h) { r = r.concat(hojasDe(h)); }); return r; }
  function describir(E, n) {
    var D = E.D, d = { nodo: n, tipo: n.tipo, cod: n.cod, clave: n.clave };
    if (n.tipo === 'estacion') { var e = E.estaciones[n.est]; d.titulo = e.k; d.texto = e.t; d.enlaces = [[ruta(e.a), T('lamina.enlace_leer', 'leer en el sitio', 'read on the site')]]; d.sub = T('lamina.sub_estacion', 'eje de exposición categorial', 'axis of categorial exposition'); }
    if (n.tipo === 'decision' || n.tipo === 'hoja') {
      var def = D[n.arbol], esEEUU = n.arbol === 'eeuu', hs = hojasDe(n);
      d.arbol = esEEUU ? T('lamina.arbol_eeuu', 'cálculos de EE.UU. (panel A)', 'US calculations (panel A)') : T('lamina.arbol_mundo', 'cálculos mundiales (panel B)', 'world calculations (panel B)');
      d.ruta = cadena(n).reverse().filter(function (x) { return x.padre && x.padre.dim != null; }).map(function (x) { var dm = def.dims[x.padre.dim]; return [dm[0], dm[2][x.opt]]; });
      d.quiebres = {}; hs.forEach(function (h) { (h.datos[2] || []).forEach(function (y) { d.quiebres[y] = (d.quiebres[y] || 0) + 1; }); });
      d.n = hs.length;
      if (esEEUU) d.idx = hs.map(function (h) { return h.spec; });   // para la curva del explorador (explorador.js)
      d.enlaces = esEEUU ? [['index.html#multiverso', T('lamina.enlace_multiverso', 'los cálculos en el sitio', 'the calculations on the site')], [ruta('metodologia.html#multiverso'), T('lamina.enlace_metodologia_5', 'metodología §5', 'methodology §5')]] : [['index.html#mundo', T('lamina.enlace_mundo', 'tasa mundial en el sitio', 'world rate on the site')], [ruta('metodologia.html#mundo'), T('lamina.enlace_metodologia', 'metodología', 'methodology')]];
      if (n.tipo === 'decision') {
        var dm = def.dims[n.dim];
        d.titulo = n.clave || dm[0]; d.sub = n.clave ? dm[0] : T('lamina.sub_bifurcacion', 'bifurcación teórica', 'theoretical fork');
        d.decision = dm[0]; d.posicion = dm[1];
        d.opciones = n.hijos.map(function (h) { return [dm[2][h.opt], hojasDe(h).length]; });
        if (esEEUU) d.grupos = n.hijos.map(function (h) { return [dm[2][h.opt], hojasDe(h).map(function (x) { return x.spec; })]; });
        if (n.cod === '#06') d.texto = T('lamina.raiz_descripcion', 'Raíz del árbol de decisiones de EE.UU.: cada hoja es un cálculo publicado de la tasa de ganancia y cada bifurcación, una decisión teórica explícita de la literatura marxista. Se informa la distribución completa de los resultados, no una estimación elegida a posteriori.',
          'Root of the US decision tree: each leaf is a published calculation of the rate of profit and each fork an explicit theoretical decision from the Marxist literature. The full distribution of results is reported, not an estimate chosen after the fact.');
        if (n.cod === '#07') { d.texto = T('lamina.bifurcacion_descripcion', 'Qué trabajo es productivo decide qué parte del excedente cuenta como plusvalor. Aquí el plusvalor ampliado se separa en dos criterios: por ramas o con la corrección intra-rama. La variante «todo productivo» cuelga del numerador «excedente amplio».',
          'Which labour is productive decides which part of the surplus counts as surplus value. Here extended surplus value splits into two criteria: by industry or with the within-industry correction. The ‘all labour productive’ variant hangs from the ‘broad surplus’ numerator.'); d.enlaces.push(['index.html#supuestos', T('lamina.enlace_plusvalor', 'qué cuenta como plusvalor', 'what counts as surplus value')]); }
      } else {
        var s = n.datos; d.spec = n.spec; d.titulo = s[0]; d.sub = esEEUU ? T('lamina.sub_especificacion', 'cálculo · {familia}', 'calculation · {familia}', { familia: (EN && def.fam_en && def.fam_en[s[1]] || s[1]) }) : T('lamina.sub_especificacion_mundial', 'cálculo mundial · {n} países', 'world calculation · {n} countries', { n: s[1] });
        d.decisiones = def.dims.map(function (dm, i) { return [dm[0], s[3] && s[3][i] >= 0 ? dm[2][s[3][i]] : T('lamina.no_aplica', 'no aplica a esta familia', 'not applicable to this family')]; });
        d.anios = s[2] || [];
      }
    }
    if (n.tipo === 'familia') { d.titulo = n.nombre; d.sub = T('lamina.sub_familia', '{n} series publicadas', '{n} published series', { n: n.series.length }); d.series = n.series; d.glosas = n.glosa; d.enlaces = [[n.ancla, T('lamina.enlace_seccion', 'ver la sección', 'see the section')]]; }
    if (n.tipo === 'serie') {
      var g = n.glosa || [n.nombre, '', ''];
      d.titulo = g[0]; d.sub = T('lamina.sub_serie', 'serie · {familia}', 'series · {familia}', { familia: n.familia.nombre }); d.columna = n.nombre; d.expresion = g[1]; d.texto = g[2];
      d.enlaces = [[n.familia.ancla, T('lamina.enlace_seccion', 'ver la sección', 'see the section')]];
    }
    if (n.tipo === 'empalme') {
      d.titulo = n.clave; d.sub = T('lamina.empalme_subtitulo', 'cambios de clasificación industrial en las series de EE.UU.', 'changes of industrial classification in the US series');
      d.texto = T('lamina.empalme_descripcion', 'Las series del BEA cambian de clasificación (SIC → NAICS). Cada empalme se hace con un factor de nivel explícito; los arcos discontinuos de la corona del panel A marcan esos años.', 'The BEA series change classification (SIC → NAICS). Each splice uses an explicit level factor; the dashed arcs in the outer band of panel A mark those years.');
      d.empalmes = Object.keys(n.empalmes || {}).map(function (k) { return [k, n.empalmes[k]]; });
      d.enlaces = [[ruta('metodologia.html#empalmes'), T('lamina.enlace_empalmes', 'metodología: empalmes', 'methodology: splices')]];
    }
    return d;
  }

  /* ---------------------------------------------------------------- montaje */
  function montar(cont, op) {
    op = op || {};
    var modo = op.modo || 'mapa';
    var cv = document.createElement('canvas'); cv.className = 'mapa-cognitivo-lienzo';
    cv.setAttribute('role', 'img');
    cv.setAttribute('aria-label', T('lamina.aria', 'Figura del mapa cognitivo del capital: (A) árbol de decisiones teóricas y registro temporal de los cálculos de la tasa de ganancia de EE.UU.; (B) los cálculos mundiales; (C) las series publicadas por sección; (D) dispersión de los cálculos y quiebres estructurales.',
      'Figure of the cognitive map of capital: (A) decision tree and time record of the calculations of the US rate of profit; (B) the world calculations; (C) the published series by section; (D) spread of the calculations and structural breaks.'));
    /* posición absoluta: el lienzo no debe influir en el tamaño de su contenedor (evita un bucle de redimensionado) */
    cv.style.cssText = 'display:block;position:absolute;inset:0;width:100%;height:100%;' + (modo === 'mapa' ? 'touch-action:none;cursor:grab;' : '');
    cont.appendChild(cv);
    var est = document.createElement('canvas'), ctx = cv.getContext('2d'), sctx = est.getContext('2d');
    var E = null, tema = op.tema || 'fosforo', sucio = true, sel = null, fijo = null, cam = { x: W / 2, y: H / 2, zoom: 1 };
    var quieto = op.quieto || (global.matchMedia && global.matchMedia('(prefers-reduced-motion: reduce)').matches);
    var v = { cw: 1, ch: 1, dpr: 1, z: 1, cx: W / 2, cy: H / 2, fw: 1, ft: 1 };
    var vivo = true, vuelo = null, pendiente = false;

    function medir() {
      var r = cont.getBoundingClientRect();
      v.cw = Math.max(1, r.width); v.ch = Math.max(1, r.height);
      v.dpr = Math.min(global.devicePixelRatio || 1, modo === 'fondo' ? 1.5 : 2);
      cv.width = est.width = Math.round(v.cw * v.dpr); cv.height = est.height = Math.round(v.ch * v.dpr);
      vista(); sucio = true;
    }
    function vista() {
      var base = modo === 'fondo' ? Math.max(v.cw / W, v.ch / H) * (op.escala || 1) : Math.min(v.cw / W, v.ch / H) * 0.985;
      v.z = base * cam.zoom; v.cx = cam.x; v.cy = cam.y;
      v.fw = Math.pow(cam.zoom, -0.62); v.ft = Math.pow(cam.zoom, -0.72); v.etq = v.z >= 0.3; v.zoom = cam.zoom; v.rotulos = modo === 'mapa';
    }
    function aMundo(px, py) { return [(px - v.cw / 2) / v.z + v.cx, (py - v.ch / 2) / v.z + v.cy]; }
    function limitar() {
      cam.zoom = Math.max(1, Math.min(9, cam.zoom));
      var hw = v.cw / 2 / (v.z || 1), hh = v.ch / 2 / (v.z || 1);
      cam.x = hw * 2 >= W ? W / 2 : Math.max(hw, Math.min(W - hw, cam.x));
      cam.y = hh * 2 >= H ? H / 2 : Math.max(hh, Math.min(H - hh, cam.y));
    }

    /* la figura es estática: sólo se repinta al mover la cámara, al seleccionar o durante un vuelo del recorrido */
    function cuadro(ts) {
      pendiente = false;
      if (!vivo) return;
      if (vuelo) {
        var u = Math.min(1, (ts - (vuelo.t0 || (vuelo.t0 = ts))) / vuelo.ms), k = u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
        cam.x = vuelo.a.x + (vuelo.b.x - vuelo.a.x) * k; cam.y = vuelo.a.y + (vuelo.b.y - vuelo.a.y) * k;
        cam.zoom = Math.exp(Math.log(vuelo.a.zoom) + (Math.log(vuelo.b.zoom) - Math.log(vuelo.a.zoom)) * k);
        vista(); limitar(); vista(); sucio = true;
        if (u >= 1) { var fin = vuelo.fin; vuelo = null; if (fin) fin(); }
      }
      if (sucio) { pintarEstatico(sctx, E, tema, v, op); sucio = false; }
      ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, cv.width, cv.height); ctx.drawImage(est, 0, 0);
      if (sel) {
        ctx.setTransform(v.dpr * v.z, 0, 0, v.dpr * v.z, v.dpr * (v.cw / 2 - v.cx * v.z), v.dpr * (v.ch / 2 - v.cy * v.z));
        resaltar(ctx, sel, PALETAS[tema] || PALETAS.fosforo, v.fw);
      }
      if (vuelo) pedirCuadro();
    }
    function pedirCuadro() { if (!pendiente) { pendiente = true; global.requestAnimationFrame(cuadro); } }
    function pedir() { sucio = true; pedirCuadro(); }

    function resaltar(c, n, P, f) {
      c.lineCap = 'round';
      var sub = [], walk = function (x) { (x.hijos || []).forEach(function (h) { if (h.seg) sub.push(h.seg); walk(h); }); };
      if (n.tipo === 'estacion') E.nodos.forEach(function (x) { if (x.padreEst === n) { sub.push(x.seg); walk(x); } }); else walk(n);
      c.beginPath(); sub.forEach(function (s) { trazar(c, s); });
      c.strokeStyle = P.texto; c.globalAlpha = 0.45; c.lineWidth = 0.9 * f; c.stroke();
      var ch = cadena(n).filter(function (x) { return x.seg; });
      c.beginPath(); ch.forEach(function (x) { trazar(c, x.seg); });
      c.strokeStyle = P.texto; c.globalAlpha = 1; c.lineWidth = 1.8 * f; c.stroke();
      hojasDe(n).forEach(function (h) {
        if (!h.pelo) return;
        c.beginPath(); trazar(c, h.pelo); c.strokeStyle = P.texto; c.globalAlpha = n.tipo === 'hoja' ? 0.95 : 0.22; c.lineWidth = 0.8 * f; c.stroke();
        c.fillStyle = P.Q; c.globalAlpha = 1; (h.quiebres || []).forEach(function (q) { c.beginPath(); c.arc(q[0], q[1], (n.tipo === 'hoja' ? 2.8 : 1.7) * f, 0, 6.2832); c.fill(); });
      });
      c.globalAlpha = 1; c.strokeStyle = P.texto; c.lineWidth = 1.2 * f;
      c.beginPath(); c.arc(n.x, n.y, 8 * f, 0, 6.2832); c.stroke();
    }

    function cercano(px, py) {
      var mm = aMundo(px, py), lim = 15 / v.z, mejor = null, md = lim * lim;
      E.nodos.forEach(function (n) { var dx = n.x - mm[0], dy = n.y - mm[1], d = (dx * dx + dy * dy) / (n.peso || 1); if (d < md) { md = d; mejor = n; } });
      return mejor;
    }
    function elegir(n, fijar) {
      if (fijar !== undefined) fijo = fijar ? n : null;
      var fam = n ? (n.tipo === 'familia' ? n : n.tipo === 'serie' ? n.familia : null) : null;
      if (fam !== v.famSel) { v.famSel = fam; sucio = true; }
      sel = n; if (op.alSeleccionar) op.alSeleccionar(n ? describir(E, n) : null, !!fijo);
      pedirCuadro();
    }

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
      var fin = function (e) {
        delete ptr[e.pointerId]; if (Object.keys(ptr).length < 2) pinza = 0; cv.style.cursor = 'grab';
        if (e.type === 'pointerup' && !movido && !Object.keys(ptr).length) { var n = cercano(e.offsetX, e.offsetY); elegir(n, !!n); }
      };
      cv.addEventListener('pointerup', fin); cv.addEventListener('pointercancel', fin);
      cv.addEventListener('pointerleave', function () { if (!fijo && !Object.keys(ptr).length) elegir(null); });
    }
    function zoomEn(px, py, k) {
      var mm = aMundo(px, py); cam.zoom *= k; cam.zoom = Math.max(1, Math.min(9, cam.zoom)); vista();
      cam.x = mm[0] - (px - v.cw / 2) / v.z; cam.y = mm[1] - (py - v.ch / 2) / v.z; vista(); limitar(); vista(); pedir();
    }
    function encuadreInicial() {
      cam = { x: W / 2, y: H / 2, zoom: 1 };
      if (modo === 'mapa' && v.cw / v.ch < 1.1) { cam.zoom = Math.min(2.6, (v.ch / H) / (v.cw / W)); cam.x = GEO.A.cx + 60; vista(); limitar(); }
      vista();
    }
    function iniciar(D) {
      E = construirEscena(D); medir(); encuadreInicial();
      if (global.ResizeObserver) new ResizeObserver(function () { medir(); pedir(); }).observe(cont); else global.addEventListener('resize', function () { medir(); pedir(); });
      /* las fuentes del sitio pueden llegar después del primer dibujo */
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { pedir(); });
      pedir();
      if (op.alListo) op.alListo(api);
    }
    var api = {
      escena: function () { return E; },
      tema: function (t) { tema = t; pedir(); },
      acercar: function (k) { zoomEn(v.cw / 2, v.ch / 2, k); },
      encuadre: function () { encuadreInicial(); pedir(); },
      /* vuelo suave de la cámara hacia un punto de la figura (recorrido guiado); con movimiento reducido, salto */
      volar: function (x, y, zoom, ms, fin) {
        var b = { x: x, y: y, zoom: Math.max(1, Math.min(9, zoom || 1)) };
        if (quieto || !ms) { cam = b; vista(); limitar(); vista(); pedir(); if (fin) fin(); return; }
        vuelo = { a: { x: cam.x, y: cam.y, zoom: cam.zoom }, b: b, ms: ms, fin: fin, t0: 0 }; pedirCuadro();
      },
      fijar: function (n) { elegir(n, !!n); },
      camara: function () { return { x: cam.x, y: cam.y, zoom: cam.zoom }; },
      enfocar: function (n, zoom) { cam.x = n.x; cam.y = n.y; cam.zoom = zoom || 2.4; vista(); limitar(); vista(); elegir(n, true); pedir(); },
      soltar: function () { fijo = null; elegir(null); },
      describir: function (n) { return describir(E, n); },
      png: function (ancho, tipo) { return exportarPNG(E, tema, ancho || 3000, op, tipo); },
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
    var v = { cw: ancho, ch: alto, dpr: 1, z: ancho / W, cx: W / 2, cy: H / 2, fw: 1, ft: 1, zoom: 1 };
    pintarEstatico(c.getContext('2d'), E, tema, v, { fondoPropio: true, exportar: true, sinTexto: op && op.sinTexto });
    return new Promise(function (ok) { c.toBlob(ok, tipo || 'image/png', 0.92); });
  }
  function exportarSVG(E, tema) {
    var P = PALETAS[tema] || PALETAS.fosforo, o = [];
    function r1(x) { return Math.round(x * 10) / 10; }
    function d(g) {
      if (g[0] === 'c') return 'M' + g.slice(1, 3).map(r1).join(' ') + 'C' + g.slice(3).map(r1).join(' ');
      if (g[0] === 'l') return 'M' + r1(g[1]) + ' ' + r1(g[2]) + 'L' + r1(g[3]) + ' ' + r1(g[4]);
      if (g[0] === 'p') return 'M' + g[1].map(function (p) { return r1(p[0]) + ' ' + r1(p[1]); }).join('L');
      if (g[0] === 'a') { var x0 = g[1] + Math.cos(g[4]) * g[3], y0 = g[2] + Math.sin(g[4]) * g[3], x1 = g[1] + Math.cos(g[5]) * g[3], y1 = g[2] + Math.sin(g[5]) * g[3]; return 'M' + r1(x0) + ' ' + r1(y0) + 'A' + r1(g[3]) + ' ' + r1(g[3]) + ' 0 ' + (g[5] - g[4] > Math.PI ? 1 : 0) + ' 1 ' + r1(x1) + ' ' + r1(y1); }
      return '';
    }
    function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
    function tx(x, y, s, t, al, op2, color, alfa) {
      var tr = op2.rot ? ' transform="rotate(' + r1(op2.rot / RAD) + ' ' + r1(x) + ' ' + r1(y) + ')"' : '';
      return '<text x="' + r1(x) + '" y="' + r1(y) + '" font-size="' + t + '" font-family="' + esc(op2.f === 'serif' ? SERIF : SANS) + '"' + (op2.w ? ' font-weight="' + op2.w + '"' : '') + (op2.it ? ' font-style="italic"' : '')
        + ' fill="' + color + '"' + (alfa < 1 ? ' fill-opacity="' + alfa + '"' : '') + ' dominant-baseline="middle" text-anchor="' + ({ left: 'start', right: 'end', center: 'middle' })[al] + '"' + tr + '>' + esc(s) + '</text>';
    }
    o.push('<?xml version="1.0" encoding="UTF-8"?>');
    o.push('<!-- ' + L('Mapa cognitivo del capital', 'Cognitive Map of Capital') + ' · ' + VERSION + ' · ' + L('datos', 'data') + ' ' + esc((E.D.meta || {}).actualizado || '') + ' -->');
    o.push('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + W + ' ' + H + '" width="' + W + '" height="' + H + '">');
    if (P.fondo) o.push('<rect width="' + W + '" height="' + H + '" fill="' + P.fondo + '"/>');
    o.push('<g stroke-linecap="round" stroke-linejoin="round">');
    E.capas.forEach(function (Lc) {
      var s = estilo(P, Lc.id);
      if (Lc.tipo === 's') o.push('<path d="' + Lc.g.map(d).join('') + '" fill="none" stroke="' + s.c + '" stroke-opacity="' + s.a + '" stroke-width="' + (s.w || 0.5) + '"' + (s.dash ? ' stroke-dasharray="' + s.dash.join(' ') + '"' : '') + '/>');
      else if (Lc.tipo === 'f') o.push('<path d="' + Lc.g.map(function (g) { return d(g) + 'Z'; }).join('') + '" fill="' + s.c + '" fill-opacity="' + s.a + '"/>');
      else if (Lc.tipo === 'd') o.push('<g fill="' + s.c + '" fill-opacity="' + s.a + '">' + Lc.g.map(function (g) { return '<circle cx="' + r1(g[1]) + '" cy="' + r1(g[2]) + '" r="' + g[3] + '"/>'; }).join('') + '</g>');
      else if (Lc.tipo === 't') Lc.g.forEach(function (g) { o.push(tx(g[1], g[2], g[3], g[4], g[5], g[6] || {}, s.c, s.a)); });
    });
    o.push('</g>');
    E.familias.forEach(function (F) { (F.lineas || [F.nombre]).forEach(function (l, i, a) { o.push(tx(F.x, GEO.C.etq + (i - a.length + 1) * 16.7, l, 14.5, 'center', { f: 'serif', w: 600 }, P.texto, 1)); }); });
    E.nodos.filter(function (n) { return n.cod; }).forEach(function (n) {
      var col = n.tipo === 'empalme' ? P.E : P.texto;
      o.push('<circle cx="' + r1(n.x) + '" cy="' + r1(n.y) + '" r="' + (n.tipo === 'estacion' ? 5 : 6) + '" fill="' + (P.fondo || '#edf0ef') + '" stroke="' + col + '" stroke-width="1.1"/><circle cx="' + r1(n.x) + '" cy="' + r1(n.y) + '" r="1.8" fill="' + col + '"/>');
      if (n.tipo !== 'estacion') o.push(tx(n.x + 10, n.y, n.cod.slice(1) + ' ' + n.clave, 10, 'left', { f: 'sans', w: 600 }, col, 1));
    });
    o.push('</svg>');
    return o.join('\n');
  }

  var MapaCognitivo = { montar: montar, VERSION: VERSION, SEED: SEED, W: W, H: H };
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
        fondoPropio: false, sinTexto: true, escala: 1.02 });
      /* la figura acompaña la portada y se retira al leer: baja hasta un 38 % al pasar la primera pantalla */
      var pend = false, atenuar = function () { pend = false; var f = Math.min(1, global.scrollY / (global.innerHeight * 0.9)); capa.style.setProperty('--mapa-desvanecer', (1 - f * 0.62).toFixed(3)); };
      global.addEventListener('scroll', function () { if (!pend) { pend = true; global.requestAnimationFrame(atenuar); } }, { passive: true }); atenuar();
      if (global.matchMedia) global.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) { m.tema(e.matches ? 'fosforo' : 'tinta'); });
    };
    if (document.body) arrancar(); else document.addEventListener('DOMContentLoaded', arrancar);
  }
})(window);
