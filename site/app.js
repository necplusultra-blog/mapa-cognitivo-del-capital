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
  svg.append('g').attr('transform', `translate(0,${H - mb})`).call(d3.axisBottom(x).ticks(Math.max(3, Math.floor((W - ml) / 70))).tickFormat(d3.format('d')));
  (o.bands || []).forEach((b, i) => svg.append('path').datum(rows).attr('d', d3.area().x((r) => x(r.anio)).y0((r) => y(+r[b[0]])).y1((r) => y(+r[b[1]]))).style('fill', C[0]).style('fill-opacity', i ? 0.3 : 0.14));
  if (o.ref != null) svg.append('line').attr('x1', ml).attr('x2', W - mr).attr('y1', y(o.ref)).attr('y2', y(o.ref)).style('stroke', 'var(--muted)').attr('stroke-dasharray', '3,3');
  series.forEach((s, i) => svg.append('path').datum(rows.filter((r) => r[s.key] != null)).attr('d', d3.line().x((r) => x(r.anio)).y((r) => y(+r[s.key]))).style('fill', 'none').style('stroke', C[(s.c ?? i) % C.length]).style('stroke-width', 2));
  const tip = d3.select(el).append('div').attr('class', 'tip').style('display', 'none');
  const rule = svg.append('line').attr('y1', mt).attr('y2', H - mb).style('stroke', 'var(--muted)').style('display', 'none');
  const vf = o.tipfmt || d3.format(',.2f');
  svg.on('pointermove', (ev) => {
    const yr = Math.round(x.invert(d3.pointer(ev)[0])); const r = rows.find((q) => q.anio === yr); if (!r) return;
    rule.attr('x1', x(yr)).attr('x2', x(yr)).style('display', null);
    tip.style('display', null).text(''); tip.append('div').text(yr).style('font-weight', 600);
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
  const { meta, bandas, ref, quiebres, decadas, masa, mtasas, mmasa } = D;
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
  bars('c-quiebres', quiebres);
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

Promise.all(['meta', 'eeuu_bandas', 'eeuu_referencias', 'eeuu_quiebres', 'eeuu_decadas', 'eeuu_masa', 'mundo_tasas', 'mundo_masa'].map(get)).then(([meta, bandas, ref, quiebres, decadas, masa, mtasas, mmasa]) => {
  D = { meta, bandas, ref, quiebres, decadas, masa, mtasas, mmasa }; draw();
  let t; window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(draw, 150); });
}).catch((e) => { document.querySelector('.lede').insertAdjacentText('afterend', ' No se pudieron cargar los datos: ' + e); });
