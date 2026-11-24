const C = ['var(--c0)', 'var(--c1)', 'var(--c2)', 'var(--c3)', 'var(--c4)'];
const f1 = d3.format(',.1f'), f2 = d3.format('.2f'), f0 = d3.format(',.0f');
const get = (n) => fetch(`data/${n}.json`, { cache: 'no-cache' }).then((r) => r.json());
const $ = (id) => document.getElementById(id);
const set = (id, v) => { const el = $(id); if (el) el.textContent = v; };

function legend(id, labels) {
  const el = $(id); el.replaceChildren();
  labels.forEach((l, i) => { const s = document.createElement('span'); const sw = document.createElement('i'); sw.className = 'sw'; sw.style.background = C[i % C.length]; s.append(sw, l); el.append(s); });
}

function lineChart(id, rows, series, o = {}) {
  const el = $(id); el.replaceChildren();
  rows = rows.map((r) => ({ ...r, anio: +r.anio }));
  const W = el.clientWidth || 640, H = o.height || 250, mt = 10, mb = 24, mr = 12;
  const ext = [];
  series.forEach((s) => rows.forEach((r) => { if (r[s.key] != null) ext.push(+r[s.key]); }));
  (o.bands || []).forEach((b) => rows.forEach((r) => ext.push(+r[b[0]], +r[b[1]])));
  if (o.ref != null) ext.push(o.ref);
  const y = d3.scaleLinear().domain(d3.extent(ext)).nice().range([H - mb, mt]);
  const svg = d3.select(el).append('svg').attr('width', '100%').attr('height', H).attr('viewBox', `0 0 ${W} ${H}`).attr('role', 'img').attr('aria-label', o.aria || '');
  const gy = svg.append('g').call(d3.axisLeft(y).ticks(5).tickFormat(o.yfmt || d3.format(',.0f')));
  let ml = 0; gy.selectAll('text').each(function () { ml = Math.max(ml, this.getComputedTextLength()); }); ml += 12;
  gy.attr('transform', `translate(${ml},0)`); gy.selectAll('.tick line').attr('x2', W - ml - mr);
  const x = d3.scaleLinear().domain(d3.extent(rows, (r) => r.anio)).range([ml, W - mr]);
  svg.append('g').attr('transform', `translate(0,${H - mb})`).call(d3.axisBottom(x).ticks(Math.max(3, Math.floor((W - ml) / 70))).tickFormat(o.xlab ? (v) => (o.xlab(v) || '').slice(0, 4) : d3.format('d')));
  (o.bands || []).forEach((b, i) => svg.append('path').datum(rows).attr('d', d3.area().x((r) => x(r.anio)).y0((r) => y(+r[b[0]])).y1((r) => y(+r[b[1]]))).style('fill', C[0]).style('fill-opacity', i ? 0.3 : 0.14));
  if (o.ref != null) svg.append('line').attr('x1', ml).attr('x2', W - mr).attr('y1', y(o.ref)).attr('y2', y(o.ref)).style('stroke', 'var(--muted)').attr('stroke-dasharray', '3,3');
  series.forEach((s, i) => {
    const pts = rows.filter((r) => r[s.key] != null); const cut = o.prov != null && o.prov >= 0 ? o.prov : Infinity;
    const ln = d3.line().x((r) => x(r.anio)).y((r) => y(+r[s.key])); const col = C[(s.c ?? i) % C.length];
    svg.append('path').datum(pts.filter((r) => r.anio < cut)).attr('d', ln).style('fill', 'none').style('stroke', col).style('stroke-width', 2);
    if (cut !== Infinity) svg.append('path').datum(pts.filter((r) => r.anio >= cut - 1)).attr('d', ln).style('fill', 'none').style('stroke', col).style('stroke-width', 2).attr('stroke-dasharray', '4,3');
  });
  const tip = d3.select(el).append('div').attr('class', 'tip').style('display', 'none');
  const rule = svg.append('line').attr('y1', mt).attr('y2', H - mb).style('stroke', 'var(--muted)').style('display', 'none');
  const vf = o.tipfmt || d3.format(',.2f');
  svg.on('pointermove', (ev) => {
    const yr = Math.round(x.invert(d3.pointer(ev)[0])); const r = rows.find((q) => q.anio === yr); if (!r) return;
    rule.attr('x1', x(yr)).attr('x2', x(yr)).style('display', null);
    tip.style('display', null).text(''); tip.append('div').text(o.xlab ? o.xlab(yr) + (r.provisional ? ' (provisional)' : '') : yr).style('font-weight', 600);
    (o.tipExtra ? o.tipExtra(r) : []).concat(series.map((s) => [s.label, r[s.key]])).forEach(([l, v]) => { if (v != null) tip.append('div').text(`${l}: ${vf(+v)}`); });
    tip.style('left', Math.min(Math.max(0, x(yr) + 10), W - 220) + 'px').style('top', '8px');
  }).on('pointerleave', () => { tip.style('display', 'none'); rule.style('display', 'none'); });
}

function bars(id, rows) {
  const el = $(id); el.replaceChildren();
  const W = el.clientWidth || 640, H = 200, mb = 24, mt = 10, ml = 34, mr = 8;
  const x = d3.scaleBand().domain(rows.map((r) => r.anio)).range([ml, W - mr]).padding(0.15);
  const y = d3.scaleLinear().domain([0, d3.max(rows, (r) => r.n)]).nice().range([H - mb, mt]);
  const svg = d3.select(el).append('svg').attr('width', '100%').attr('height', H).attr('viewBox', `0 0 ${W} ${H}`).attr('role', 'img').attr('aria-label', 'Quiebres por año');
  svg.append('g').attr('transform', `translate(${ml},0)`).call(d3.axisLeft(y).ticks(4));
  svg.append('g').attr('transform', `translate(0,${H - mb})`).call(d3.axisBottom(x).tickValues(rows.map((r) => r.anio).filter((a) => a % 10 === 0)));
  const tip = d3.select(el).append('div').attr('class', 'tip').style('display', 'none');
  svg.selectAll('rect').data(rows).join('rect').attr('x', (r) => x(r.anio)).attr('width', x.bandwidth()).attr('y', (r) => y(r.n)).attr('height', (r) => y(0) - y(r.n)).style('fill', C[0])
    .on('pointermove', (ev, r) => tip.style('display', null).text(`${r.anio}: ${r.n} especificaciones`).style('left', Math.min(x(r.anio) + 8, W - 190) + 'px').style('top', '8px'))
    .on('pointerleave', () => tip.style('display', 'none'));
}

let D = {};
function draw() {
  const { meta, bandas, ref, quiebres, decadas, masa, mtasas, mmasa, trim, sens } = D;
  set('m-act', meta.actualizado); set('m-fin', meta.eeuu_fin); set('m-wfin', meta.mundo_fin); set('m-n', meta.eeuu_n);
  const last = bandas[bandas.length - 1], b82 = bandas.find((r) => r.anio === 1982);
  set('k-med', f1(last.p50)); set('k-med82', f1(b82.p50));
  const mi = masa.filter((r) => r.e_intra != null);
  set('k-e', f2(mi[mi.length - 1].e_intra)); set('k-e72', f2(mi[0].e_intra));
  set('k-masa', f0(masa[masa.length - 1].masa_ramas)); set('k-masa48', f0(masa[0].masa_ramas));
  const cn = mmasa.filter((r) => r.china_pct_K != null);
  set('k-cn', f1(cn[cn.length - 1].china_pct_K) + ' %'); set('k-cn00', f1(mmasa.find((r) => r.anio === 2000).china_pct_K) + ' %');
  lineChart('c-bandas', bandas, [{ key: 'p50', label: 'Mediana' }], { bands: [['p10', 'p90'], ['p25', 'p75']], ref: 100, tipfmt: d3.format('.1f'), aria: 'Abanico del multiverso de la tasa de ganancia de EE.UU.', tipExtra: (r) => [['P90', r.p90], ['P75', r.p75], ['P25', r.p25], ['P10', r.p10]] });
  const refS = [['nfc_ebe_cc', 'No financiero, EBE, costo corriente (tipo Duménil-Lévy)'], ['corp_ebe_hc', 'Corporativo, EBE, costo histórico (tipo Kliman)'], ['emp_todo_cc', 'Empresarial, todo trabajo productivo'], ['emp_ramas_cc', 'Plusvalor ampliado, por ramas'], ['emp_intra_cc', 'Plusvalor ampliado, corrección intra-rama (desde 1972)']];
  legend('l-ref', refS.map((s) => s[1]));
  lineChart('c-ref', ref, refS.map(([key, label]) => ({ key, label })), { yfmt: (v) => v + ' %', tipfmt: (v) => d3.format('.1f')(v) + ' %', aria: 'Cinco medidas de la tasa de ganancia de EE.UU.' });
  set('m-trim', meta.eeuu_trim_fin);
  const tr = trim.map((r, i) => ({ ...r, anio: i, t: r.trimestre }));
  const trS = [['nfc_ebe', 'No financiero, excedente neto'], ['nfc_despues_imp', 'No financiero, después de impuestos'], ['corp_ebe', 'Corporativo total, excedente neto']];
  legend('l-trim', trS.map((x) => x[1]));
  lineChart('c-trim', tr, trS.map(([key, label]) => ({ key, label })), { yfmt: (v) => v + ' %', tipfmt: (v) => d3.format('.1f')(v) + ' %', xlab: (i) => (tr[Math.round(i)] || {}).t, prov: tr.findIndex((r) => r.provisional), aria: 'Tasa de ganancia corporativa trimestral' });
  bars('c-quiebres', quiebres);
  const ts = $('t-sens'); ts.replaceChildren();
  sens.forEach((r) => { const tr2 = document.createElement('tr'); [r.configuracion, String(r.quiebres_medios), r.anios_mas_frecuentes].forEach((t) => { const td = document.createElement('td'); td.textContent = t; tr2.append(td); }); ts.append(tr2); });
  const tb = $('t-dec'); tb.replaceChildren();
  decadas.forEach((r) => { const tr = document.createElement('tr'); const c = r.clase.includes('baja') ? 'down' : r.clase.includes('sube') ? 'up' : 'dep';
    [[r.tramo], [f1(r.pct_baja) + ' %'], [r.clase, c]].forEach(([t, k]) => { const td = document.createElement('td'); td.textContent = t; if (k) td.className = k; tr.append(td); }); tb.append(tr); });
  legend('l-masa', ['Por ramas (desde 1948)', 'Corrección intra-rama (desde 1972)']);
  lineChart('c-masa', masa, [{ key: 'masa_ramas', label: 'Por ramas' }, { key: 'masa_intra', label: 'Intra-rama' }], { tipfmt: d3.format(',.0f'), aria: 'Masa real de plusvalor' });
  lineChart('c-e', masa, [{ key: 'e_ramas', label: 'Por ramas' }, { key: 'e_intra', label: 'Intra-rama' }], { yfmt: d3.format('.1f'), aria: 'Tasa de plusvalor' });
  set('m-wsrc', `${meta.mundo_fuente}. ${meta.mundo_nbal} países con datos continuos desde 1960 (de ${meta.mundo_n}). Ponderación por stock de capital. Tasas en %.`);
  const wk = Object.keys(mtasas[0]).filter((k) => k !== 'anio');
  const name = { bruta: 'Bruta', neta: 'Neta de depreciación', irr: 'Tasa interna de retorno (PWT)' };
  const wl = wk.map((k) => `${name[k.split('_')[0]]}, ${k.endsWith('con') ? 'con' : 'sin'} China`);
  legend('l-mundo', wl);
  lineChart('c-mundo', mtasas, wk.map((k, i) => ({ key: k, label: wl[i] })), { yfmt: (v) => v + ' %', tipfmt: (v) => d3.format('.1f')(v) + ' %', aria: 'Tasa mundial de ganancia' });
  legend('l-wmasa', ['Masa mundial de ganancia bruta (billones USD 2021)', 'Sin China']);
  lineChart('c-wmasa', mmasa, [{ key: 'masa_mundial', label: 'Mundial' }, { key: 'masa_sin_china', label: 'Sin China' }], { height: 220, tipfmt: d3.format(',.1f'), aria: 'Masa mundial de ganancia' });
}

function drawHM(H, Pz, meta) {
  $('horas-mundo').hidden = false;
  const k = (v, c) => `__educación y salud ${v}__${c}`, K = k('productivas', 'con China');
  const z = H[H.length - 1], a = H[0], b = H.find((r) => r.anio === Pz.base_wiod) || a;
  set('hm-fin', z.anio); document.querySelectorAll('.hm-fin').forEach((e) => { e.textContent = z.anio; });
  document.querySelectorAll('.hm-base0').forEach((e) => { e.textContent = Pz.base_wiod; });
  document.querySelectorAll('.hm-base1').forEach((e) => { e.textContent = Pz.base_wiod + 1; });
  set('hm-np', String(Pz.n_paises || '—')); set('hm-base', Pz.base_wiod);
  set('hm-nocde', String((Pz.fuentes_e || {})['OCDE por rama'] || 0));
  set('hm-n', f0(z['obreros_mill' + K])); set('hm-n14', f0(b['obreros_mill' + K]));
  set('hm-masa', f0(z['plustrabajo_mmh' + K])); set('hm-masa0', f0(a['plustrabajo_mmh' + K])); set('hm-masa14', f0(b['plustrabajo_mmh' + K]));
  set('hm-masan', f0(z['plustrabajo_neto_mmh' + K])); set('hm-masan0', f0(a['plustrabajo_neto_mmh' + K]));
  set('hm-e', f2(z['e_horas' + K]) + ' · ' + f2(z['e_horas_neta' + K]));
  set('hm-cn', f1(z['pct_china' + K]) + ' %'); set('hm-in', f1(z['pct_india' + K]) + ' %');
  const ser = [['plustrabajo_mmh' + K, 'Bruta (central)'], ['plustrabajo_neto_mmh' + K, 'Neta de depreciación'],
    ['plustrabajo_mmh' + k('productivas', 'sin China'), 'Bruta, sin China'], ['plustrabajo_mmh' + k('fuera', 'con China'), 'Bruta, educación y salud fuera']];
  legend('l-hm', ser.map((x) => x[1]));
  lineChart('c-hm', H, ser.map(([key, label]) => ({ key, label })), { tipfmt: d3.format(',.0f'), prov: Pz.base_wiod + 1, aria: 'Masa mundial de plustrabajo en horas' });
  const se = [['e_horas' + K, 'Bruta'], ['e_horas_neta' + K, 'Neta de depreciación']];
  legend('l-hme', se.map((x) => x[1]));
  lineChart('c-hme', H, se.map(([key, label]) => ({ key, label })), { yfmt: d3.format('.1f'), tipfmt: d3.format('.2f'), prov: Pz.base_wiod + 1, aria: 'Tasa de plusvalor mundial en horas' });
  const fila = (tb, vals) => { const tr = document.createElement('tr'); vals.forEach((t) => { const td = document.createElement('td'); td.textContent = t; tr.append(td); }); tb.append(tr); };
  const tb = $('t-hm'); tb.replaceChildren();
  Pz.paises.forEach((r) => fila(tb, [r.pais + (r.china_estimada ? ' (estimado)' : ''), f1(r.obreros_mill), f2(r.e), r.e_neta == null ? '—' : f2(r.e_neta), f1(r.plustrabajo_mill_h / 1000), f1(r.pct) + ' %', r.fuente_e || '—']));
  const ts = $('t-hms'); ts.replaceChildren();
  (Pz.sensibilidad || []).forEach((r) => fila(ts, [r.anio, r.caso, f0(r.plustrabajo_mmh), f0(r.obreros_mill), (r.diferencia_pct > 0 ? '+' : '') + f1(r.diferencia_pct) + ' %', r.nota || '']));
  const td = $('t-hmd'); td.replaceChildren();
  const g = (x, f) => (x == null ? '—' : f(x));
  (Pz.diagnostico_ocde || []).forEach((r) => fila(td, [r.pais, g(r.e_wiod_2014, f2), g(r.e_ocde_2014, f2), g(r.N_ocde_sobre_wiod, f2), g(r.H_ocde_sobre_wiod, f2), g(r.r_pwt_2014, f2), g(r.r_ocde_2014, f2), g(r.ultimo_anio_e, String)]));
  set('hm-kmed', Pz.k_mediana == null ? '—' : f2(Pz.k_mediana));
  set('hm-excl', Pz.excluidos.length ? Pz.excluidos.join(', ') : 'ninguna');
}

function drawIA(A, E) {
  if (!A || !A.length) return;
  $('ia').hidden = false;
  const last = A[A.length - 1];
  set('ia-fin', last.anio); set('ia-pct-corp', f1(last.pct_ganancia_ia_en_corporativas) + ' %');
  set('ia-pct-mundo', f1(last.pct_ganancia_ia_en_masa_mundial) + ' %'); set('ia-pct-inv', f1(last.pct_inversion_ia_en_inversion_privada) + ' %');
  const s1 = [['tasa_ia_sobre_activos', 'Grupo IA: ganancia operativa / activos totales'], ['tasa_nfc_hc_sin_ppi', 'No financiero EE.UU. (costo histórico, sin propiedad intelectual)'], ['tasa_nfc_sin_ia', 'No financiero EE.UU. sin el grupo IA']];
  legend('l-ia1', s1.map((x) => x[1]));
  lineChart('c-ia1', A, s1.map(([key, label]) => ({ key, label })), { yfmt: (v) => v + ' %', tipfmt: (v) => d3.format('.1f')(v) + ' %', aria: 'Tasa de ganancia del grupo IA' });
  const s2 = [['pct_ganancia_ia_en_corporativas', 'Ganancias corporativas de EE.UU.'], ['pct_inversion_ia_en_inversion_privada', 'Inversión privada no residencial de EE.UU.'], ['pct_ganancia_ia_en_masa_mundial', 'Masa mundial de ganancia bruta']];
  legend('l-ia2', s2.map((x) => x[1]));
  lineChart('c-ia2', A, s2.map(([key, label]) => ({ key, label })), { yfmt: (v) => v + ' %', tipfmt: (v) => d3.format('.2f')(v) + ' %', aria: 'Peso del grupo IA' });
  const yrs = E.slice(-4); const emp = Object.keys(E[0]).filter((k) => k !== 'anio').sort();
  const h = $('t-ia-h'); h.replaceChildren(); const hr = document.createElement('tr');
  ['Empresa', ...yrs.map((r) => String(r.anio))].forEach((t) => { const th = document.createElement('th'); th.textContent = t; hr.append(th); }); h.append(hr);
  const tb = $('t-ia'); tb.replaceChildren();
  emp.forEach((e) => { const tr = document.createElement('tr'); [e, ...yrs.map((r) => (r[e] == null ? '—' : f0(r[e])))].forEach((t) => { const td = document.createElement('td'); td.textContent = t; tr.append(td); }); tb.append(tr); });
}

function drawTiempo(T, Dc) {
  const a = T[0], z = T[T.length - 1];
  document.querySelectorAll('.t-fin').forEach((e) => { e.textContent = z.anio; });
  document.querySelectorAll('.t-ini').forEach((e) => { e.textContent = a.anio; });
  set('t-n', f1(z.obreros_productivos_mill)); set('t-n0', f1(a.obreros_productivos_mill));
  set('t-sem', f1(z.semana_horas)); set('t-nec', f1(z.semana_necesario) + ' h'); set('t-nec0', f1(a.semana_necesario) + ' h');
  set('t-plus', f1(z.semana_plustrabajo) + ' h'); set('t-plus0', f1(a.semana_plustrabajo) + ' h');
  set('t-masa', f1(z.horas_plustrabajo_mmh)); set('t-masa0', f1(a.horas_plustrabajo_mmh));
  legend('l-sem', ['Trabajo necesario', 'Plustrabajo']);
  lineChart('c-sem', T, [{ key: 'semana_necesario', label: 'Necesario' }, { key: 'semana_plustrabajo', label: 'Plustrabajo' }], { yfmt: (v) => v + ' h', tipfmt: (v) => d3.format('.1f')(v) + ' h', aria: 'Trabajo necesario y plustrabajo semanal' });
  lineChart('c-hplus', T, [{ key: 'horas_plustrabajo_mmh', label: 'Plustrabajo' }], { tipfmt: d3.format(',.1f'), aria: 'Masa anual de plustrabajo en horas' });
  set('t-desc-intro', `Entre ${Dc.desde} y ${Dc.hasta} la masa anual de plustrabajo se multiplica por ${f2(Dc.factor_total)}: horas de plustrabajo = obreros × horas por obrero × e/(1+e).`);
  const tb = $('t-desc'); tb.replaceChildren();
  Dc.factores.forEach((r) => { const tr = document.createElement('tr'); [r.factor, f2(r.multiplica), f1(r.aporte_pct) + ' %'].forEach((t) => { const td = document.createElement('td'); td.textContent = t; tr.append(td); }); tb.append(tr); });
  legend('l-melt', ['USD corrientes por hora', 'USD de 2017 por hora']);
  lineChart('c-melt', T, [{ key: 'expresion_monetaria_hora', label: 'Corrientes' }, { key: 'expresion_monetaria_hora_real', label: 'De 2017' }], { tipfmt: (v) => d3.format('.1f')(v) + ' USD', aria: 'Expresión monetaria del tiempo de trabajo' });
}

Promise.all(['meta', 'eeuu_bandas', 'eeuu_referencias', 'eeuu_quiebres', 'eeuu_decadas', 'eeuu_masa', 'mundo_tasas', 'mundo_masa', 'eeuu_trimestral', 'eeuu_sensibilidad'].map(get)).then(([meta, bandas, ref, quiebres, decadas, masa, mtasas, mmasa, trim, sens]) => {
  D = { meta, bandas, ref, quiebres, decadas, masa, mtasas, mmasa, trim, sens }; draw();
  Promise.all([get('eeuu_tiempo'), get('eeuu_descomposicion')]).then(([T, Dc]) => { D.T = T; D.Dc = Dc; drawTiempo(T, Dc); });
  if (meta.mundo_horas) Promise.all([get('mundo_horas'), get('mundo_horas_paises')]).then(([H, Pz]) => { D.H = H; D.Pz = Pz; drawHM(H, Pz, meta); });
  if (meta.ia) Promise.all([get('ia_agregado'), get('ia_empresas')]).then(([A, E]) => { D.iaA = A; D.iaE = E; drawIA(A, E); });
  let t; window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(() => { draw(); if (D.T) drawTiempo(D.T, D.Dc); if (D.H) drawHM(D.H, D.Pz, D.meta); if (D.iaA) drawIA(D.iaA, D.iaE); }, 150); });
}).catch((e) => { document.querySelector('.lede').insertAdjacentText('afterend', ' No se pudieron cargar los datos: ' + e); });
