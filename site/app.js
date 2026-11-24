const C = ['var(--c0)', 'var(--c1)', 'var(--c2)', 'var(--c3)', 'var(--c4)', 'var(--c5)'];
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
    svg.append('path').datum(pts.filter((r) => r.anio < cut)).attr('d', ln).attr('data-key', s.key).style('fill', 'none').style('stroke', col).style('stroke-width', 2);
    if (cut !== Infinity) svg.append('path').datum(pts.filter((r) => r.anio >= cut - 1)).attr('d', ln).attr('data-key', s.key).style('fill', 'none').style('stroke', col).style('stroke-width', 2).attr('stroke-dasharray', '4,3');
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

function drawSismo(bandas, quiebres) {
  const el = $('sismo'); if (!el) return; el.replaceChildren();
  const W = el.clientWidth, H = el.clientHeight, mt = 34, mb = 26, pad = Math.max(20, Math.min(56, W * 0.04));
  const rows = bandas.map((r) => ({ ...r, anio: +r.anio }));
  const x = d3.scaleLinear().domain(d3.extent(rows, (r) => r.anio)).range([pad, W - pad]);
  const y = d3.scaleLinear().domain([d3.min(rows, (r) => r.p10), d3.max(rows, (r) => r.p90)]).nice().range([H - mb, mt]);
  const svg = d3.select(el).append('svg').attr('width', W).attr('height', H).attr('aria-hidden', 'true');
  svg.append('path').datum(rows).attr('class', 'banda').attr('d', d3.area().curve(d3.curveMonotoneX).x((r) => x(r.anio)).y0((r) => y(r.p10)).y1((r) => y(r.p90)));
  const traza = svg.append('path').datum(rows).attr('class', 'traza').attr('d', d3.line().curve(d3.curveMonotoneX).x((r) => x(r.anio)).y((r) => y(r.p50)));
  // los tres años con más quiebres detectados, separados al menos cinco años entre sí
  const top = []; [...quiebres].sort((a, b) => b.n - a.n).forEach((q) => { if (top.length < 3 && top.every((t) => Math.abs(t.anio - q.anio) >= 5)) top.push(q); });
  const g = svg.selectAll('g.marca-q').data(top).join('g').attr('class', 'marca-q').attr('transform', (q) => `translate(${x(q.anio)},0)`);
  g.append('line').attr('y1', 6).attr('y2', 22); g.append('text').attr('x', 6).attr('y', 18).text((q) => q.anio);
  const dec = rows.map((r) => r.anio).filter((a) => a % 10 === 0);
  svg.selectAll('text.anio').data(dec).join('text').attr('class', 'anio').attr('x', (a) => x(a)).attr('y', H - 8).attr('text-anchor', 'middle').text((a) => a);
  const ult = rows[rows.length - 1];
  svg.append('circle').attr('cx', x(ult.anio)).attr('cy', y(ult.p50)).attr('r', 3.5).style('fill', 'var(--estilete)');
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches && !drawSismo.hecho) {
    const L = traza.node().getTotalLength();
    traza.attr('stroke-dasharray', `${L} ${L}`).attr('stroke-dashoffset', L).transition().duration(2600).ease(d3.easeCubicInOut).attr('stroke-dashoffset', 0);
  }
  drawSismo.hecho = true;
}

function indiceActivo() {
  const links = [...document.querySelectorAll('.indice a')]; if (!links.length || !('IntersectionObserver' in window)) return;
  const obs = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) links.forEach((a) => a.classList.toggle('activa', a.getAttribute('href') === '#' + e.target.id)); }), { rootMargin: '-30% 0px -60% 0px' });
  document.querySelectorAll('main > section[id]').forEach((s) => obs.observe(s));
}

function barrasFases(id, rows, series) {
  const el = $(id); if (!el) return; el.replaceChildren();
  const W = el.clientWidth || 640, H = 260, mt = 12, mb = 40, mr = 8;
  const etiquetas = rows.map((r) => `${r.desde}–${r.hasta}`);
  const vals = rows.flatMap((r) => series.map((s) => r[s.key] ?? 0));
  const y = d3.scaleLinear().domain(d3.extent([0, ...vals])).nice().range([H - mb, mt]);
  const svg = d3.select(el).append('svg').attr('width', '100%').attr('height', H).attr('viewBox', `0 0 ${W} ${H}`).attr('role', 'img').attr('aria-label', 'Descomposición de la tasa de ganancia por fases');
  const gy = svg.append('g').call(d3.axisLeft(y).ticks(5).tickFormat(d3.format('+.2f')));
  let ml = 0; gy.selectAll('text').each(function () { ml = Math.max(ml, this.getComputedTextLength()); }); ml += 12;
  gy.attr('transform', `translate(${ml},0)`); gy.selectAll('.tick line').attr('x2', W - ml - mr);
  const x0 = d3.scaleBand().domain(etiquetas).range([ml, W - mr]).padding(0.22);
  const x1 = d3.scaleBand().domain(series.map((s) => s.key)).range([0, x0.bandwidth()]).padding(0.08);
  svg.append('g').attr('transform', `translate(0,${H - mb})`).call(d3.axisBottom(x0));
  svg.append('line').attr('x1', ml).attr('x2', W - mr).attr('y1', y(0)).attr('y2', y(0)).style('stroke', 'var(--tinta)');
  const tip = d3.select(el).append('div').attr('class', 'tip').style('display', 'none');
  rows.forEach((r, i) => series.forEach((s, j) => {
    const v = r[s.key]; if (v == null) return;
    svg.append('rect').attr('x', x0(etiquetas[i]) + x1(s.key)).attr('width', x1.bandwidth()).attr('y', y(Math.max(0, v))).attr('height', Math.abs(y(v) - y(0))).style('fill', C[j % C.length])
      .on('pointermove', () => tip.style('display', null).text(`${etiquetas[i]} · ${s.label}: ${d3.format('+.3f')(v)}`).style('left', Math.min(x0(etiquetas[i]), W - 260) + 'px').style('top', '6px'))
      .on('pointerleave', () => tip.style('display', 'none'));
  }));
}

function drawCT(CT) {
  const I = CT.indicadores, F = CT.fases;
  const desde = (keys) => I.filter((r) => keys.some((k) => r[k] != null));
  const graf = (id, lid, ser, o = {}) => { const rows = desde(ser.map((x) => x[0])); legend(lid, ser.map((x) => x[1])); lineChart(id, rows, ser.map(([key, label]) => ({ key, label })), o); };
  const pct = { yfmt: (v) => v + ' %', tipfmt: (v) => d3.format('.1f')(v) + ' %' };
  set('ct-cortes', CT.cortes.join(', '));
  const fr = F.filter((r) => r.variante === 'por ramas'), fi = F.filter((r) => r.variante === 'intra-rama');
  legend('l-ct-fases', ['Tasa de plusvalor e', 'Composición K/V (con signo invertido)', 'Cambio de la tasa (Δ ln r)']);
  barrasFases('c-ct-fases', fr, [{ key: 'aporte_explotacion', label: 'e' }, { key: 'aporte_composicion', label: 'K/V' }, { key: 'dln_tasa', label: 'Δ ln r' }]);
  legend('l-ct-fases-i', ['Tasa de plusvalor e', 'Composición técnica (signo invertido)', 'Precio relativo del capital (signo invertido)', 'Cambio de la tasa (Δ ln r)']);
  barrasFases('c-ct-fases-i', fi, [{ key: 'aporte_explotacion', label: 'e' }, { key: 'aporte_comp_tecnica', label: 'técnica' }, { key: 'aporte_precio_relativo', label: 'precio relativo' }, { key: 'dln_tasa', label: 'Δ ln r' }]);
  const tb = $('t-ct-fases'); tb.replaceChildren();
  F.forEach((r) => { const tr = document.createElement('tr'); [r.variante, `${r.desde}–${r.hasta}`, (r.cambio_tasa_pct > 0 ? '+' : '') + f1(r.cambio_tasa_pct) + ' %', d3.format('+.3f')(r.aporte_explotacion), d3.format('+.3f')(r.aporte_composicion), r.aporte_comp_tecnica == null ? '—' : d3.format('+.3f')(r.aporte_comp_tecnica), r.aporte_precio_relativo == null ? '—' : d3.format('+.3f')(r.aporte_precio_relativo)].forEach((t) => { const td = document.createElement('td'); td.textContent = t; tr.append(td); }); tb.append(tr); });
  graf('c-ct-a', 'l-ct-a', [['productividad_hora_idx', 'Producto por hora (1972 = 100)'], ['remuneracion_real_hora_idx', 'Remuneración real por hora (1972 = 100)']], { tipfmt: d3.format('.1f') });
  graf('c-ct-a2', 'l-ct-a2', [['pluriempleo_pct_ocupados', 'EE.UU.: ocupados con más de un empleo'], ['tiempo_parcial_involuntario_pct', 'EE.UU.: tiempo parcial por razones económicas']], pct);
  const tm = $('t-ct-fm'); if (tm) { tm.replaceChildren(); (CT.fases_multiverso || []).forEach((r) => { const tr = document.createElement('tr'); const g = (a, b, c) => `${d3.format('+.3f')(b)} (${d3.format('+.2f')(a)} a ${d3.format('+.2f')(c)})`;
    [r.variante, `${r.desde}–${r.hasta}`, g(r.aporte_e_p10, r.aporte_e_mediana, r.aporte_e_p90), g(r.aporte_kv_p10, r.aporte_kv_mediana, r.aporte_kv_p90), f0(r.pct_tasa_sube) + ' %', r.pct_composicion_sube > 0 ? f0(r.pct_e_compensa) + ' %' : '—'].forEach((t) => { const td = document.createElement('td'); td.textContent = t; tr.append(td); }); tm.append(tr); }); }
  graf('c-ct-b', 'l-ct-b', [['salario_real_obreros_produccion', 'Salario real por hora de los obreros de producción (USD de 2017)']], { tipfmt: (v) => d3.format('.2f')(v) + ' USD' });
  graf('c-ct-c', 'l-ct-c', [['composicion_tecnica_idx', 'Composición técnica: capital real por hora productiva'], ['precio_capital_sobre_salario_idx', 'Precio del capital / salario por hora'], ['precio_relativo_inversion_idx', 'Precio de la inversión / precio del consumo']], { tipfmt: d3.format('.1f'), ref: 100 });
  graf('c-ct-d', 'l-ct-d', [['tasa_empleo_25_54_pct', 'EE.UU.: tasa de empleo de 25 a 54 años'], ['empleo_vulnerable_mundial_pct', 'Mundo: empleo vulnerable (cuenta propia y familiar)'], ['subempleo_u6_pct', 'EE.UU.: subutilización laboral (U-6)'], ['desempleo_mundial_pct', 'Mundo: desempleo']], pct);
  graf('c-ct-e', 'l-ct-e', [['ganancias_del_resto_del_mundo_pct', 'Ganancias recibidas del resto del mundo / ganancias corporativas de EE.UU.'], ['comercio_mundial_pct_pib', 'Comercio mundial / PIB mundial']], pct);
  graf('c-ct-e2', 'l-ct-e2', [['transferencia_horas_altos_ingresos_mmh', 'Países de altos ingresos'], ['transferencia_horas_eeuu_mmh', 'EE.UU.'], ['transferencia_horas_china_mmh', 'China'], ['transferencia_horas_india_mmh', 'India']], { tipfmt: (v) => d3.format(',.0f')(v) + ' mil millones de h', ref: 0 });
  graf('c-ct-f2', 'l-ct-f2', [['acciones_nfc_valor_mercado_pct_pib', 'Valor de mercado de las acciones de las no financieras / PIB'], ['deuda_nfc_pct_pib', 'Deuda de las no financieras / PIB']], pct);
  graf('c-ct-f', 'l-ct-f', [['ganancias_financieras_pct_domesticas', 'Ganancias financieras / ganancias corporativas domésticas'], ['intereses_netos_pct_excedente_nfc', 'Intereses netos / excedente neto (no financieras)'], ['dividendos_pct_ganancia_neta_nfc', 'Dividendos / ganancia después de impuestos (no financieras)'], ['emision_neta_acciones_pct_va_nfc', 'Emisión neta de acciones / valor agregado (no financieras)']], { ...pct, ref: 0 });
}

// Seis lecturas del debate: series, cifras de las tarjetas, tabla y resaltado de líneas
const REFS = [['nfc_ebe_cc', 'No financiero, costo corriente (tipo Duménil-Lévy)'], ['corp_ebe_hc', 'Corporativo, costo histórico (tipo Kliman)'],
  ['emp_todo_cc', 'Empresarial, todo productivo (línea de base)'], ['emp_ramas_cc', 'Plusvalor ampliado por ramas (tipo Shaikh-Tonak)'],
  ['emp_intra_cc', 'Plusvalor ampliado intra-rama, desde 1972 (tipo Moseley)'], ['emp_ramas_cv', 'Plusvalor por ramas sobre c + v (tipo Roberts-Carchedi)']];
function drawLecturas(ref, masa, mtasas, decadas) {
  const en = (k, a) => { const r = ref.find((q) => q.anio === a); return r ? r[k] : null; };
  const ult = (k) => { const v = ref.filter((q) => q[k] != null); return v[v.length - 1]; };
  const p1 = (v) => (v == null ? '—' : f1(v));
  const fin = ref[ref.length - 1].anio;
  document.querySelectorAll('.lx-fin').forEach((e) => { e.textContent = fin; });
  set('lx-ra-48', p1(en('emp_ramas_cc', 1948))); set('lx-ra-82', p1(en('emp_ramas_cc', 1982))); set('lx-ra-u', p1(ult('emp_ramas_cc').emp_ramas_cc) + ` % en ${fin}`);
  set('lx-in-82', p1(en('emp_intra_cc', 1982)));
  const inMax = ref.filter((q) => q.emp_intra_cc != null).reduce((a, b) => (b.emp_intra_cc > a.emp_intra_cc ? b : a));
  set('lx-in-max', `${f1(inMax.emp_intra_cc)} % en ${inMax.anio}`); set('lx-in-u', p1(ult('emp_intra_cc').emp_intra_cc));
  set('lx-dl-65', p1(en('nfc_ebe_cc', 1965))); set('lx-dl-82', p1(en('nfc_ebe_cc', 1982))); set('lx-dl-u', p1(ult('nfc_ebe_cc').nfc_ebe_cc) + ` % en ${fin}`);
  set('lx-dl-rec', d3.format('+.0f')((ult('nfc_ebe_cc').nfc_ebe_cc / en('nfc_ebe_cc', 1982) - 1) * 100) + ' %');
  const klMax = ref.filter((q) => q.anio < 1970).reduce((a, b) => (b.corp_ebe_hc > a.corp_ebe_hc ? b : a));
  set('lx-kl-max', `${f1(klMax.corp_ebe_hc)} % en ${klMax.anio}`); set('lx-kl-19', p1(en('corp_ebe_hc', 2019))); set('lx-kl-u', p1(ult('corp_ebe_hc').corp_ebe_hc));
  set('lx-cv-48', p1(en('emp_ramas_cv', 1948))); set('lx-cv-u', p1(ult('emp_ramas_cv').emp_ramas_cv) + ` % en ${fin}`);
  const w = mtasas.filter((r) => r.neta_K_con != null), w07 = w.find((r) => r.anio === 2007), wz = w[w.length - 1];
  set('lx-w-07', w07 ? f1(w07.neta_K_con) : '—'); set('lx-w-u', `${f1(wz.neta_K_con)} % en ${wz.anio}`);
  const mi = masa.filter((r) => r.e_intra != null), mz = masa[masa.length - 1];
  set('lx-e72', f2(mi[0].e_intra)); set('lx-eu', `${f2(mi[mi.length - 1].e_intra)} en ${mi[mi.length - 1].anio}`);
  const kv = (a) => { const r = masa.find((q) => q.anio === a); return r ? f2(r.kv_ramas) : '—'; };
  set('lx-kv82', kv(1982)); set('lx-kv00', kv(2000)); set('lx-kvu', `${f2(mz.kv_ramas)} en ${mz.anio}`);
  set('lx-dec-rob', String(decadas.filter((r) => r.clase.startsWith('robusto')).length)); set('lx-dec-n', String(decadas.length));
  const tb = $('t-lect');
  if (tb) {
    tb.replaceChildren();
    REFS.forEach(([k, l]) => {
      const u = ult(k), b = en(k, 1982); const tr = document.createElement('tr');
      [l, p1(en(k, 1948)), p1(en(k, 1965)), p1(b), p1(en(k, 2007)), `${p1(u[k])} (${u.anio})`, b ? d3.format('+.0f')((u[k] / b - 1) * 100) + ' %' : '—']
        .forEach((t) => { const td = document.createElement('td'); td.textContent = t; tr.append(td); });
      tb.append(tr);
    });
  }
  const arts = [...document.querySelectorAll('article.lectura')];
  const idx = Object.fromEntries(REFS.map(([k], i) => [k, i]));
  let fija = null;
  const marcar = (a) => {
    const ks = a && a.dataset.series ? a.dataset.series.split(',') : null;
    d3.select('#c-ref').selectAll('path[data-key]').style('opacity', function () { return !a || !ks || ks.includes(this.dataset.key) ? 1 : 0.13; })
      .style('stroke-width', function () { return a && ks && ks.includes(this.dataset.key) ? 3.2 : 2; });
    arts.forEach((x) => x.classList.toggle('activa', x === a));
  };
  arts.forEach((a) => {
    const k = (a.dataset.series || '').split(',')[0];
    a.style.borderLeftColor = k in idx ? C[idx[k] % C.length] : 'var(--tinta)';
    a.onmouseenter = a.onfocus = () => { if (!fija) marcar(a); };
    a.onmouseleave = a.onblur = () => { if (!fija) marcar(null); };
    a.onclick = () => { fija = fija === a ? null : a; marcar(fija || a); };
  });
}

// Fuerzas productivas y tiempo disponible
function drawFZ(F) {
  if (!F || !F.eeuu || !F.eeuu.length) return;
  $('fuerzas').hidden = false;
  const U = F.eeuu, a = U[0], z = U[U.length - 1], dsc = F.desc, h = (v) => f1(v) + ' h';
  document.querySelectorAll('.fz-ini').forEach((e) => { e.textContent = a.anio; });
  document.querySelectorAll('.fz-fin').forEach((e) => { e.textContent = z.anio; });
  set('fz-niv', h(z.necesario_nivel_inicial_h)); set('fz-nec', h(z.necesario_efectivo_h));
  set('fz-lib', h(dsc.liberado_h)); set('fz-plus-pct', f0(dsc.plustrabajo_pct) + ' %'); set('fz-cons-pct', f0(dsc.consumo_pct) + ' %'); set('fz-jor', '0 h');
  const s1 = [['necesario_efectivo_h', 'Trabajo necesario efectivo'], ['necesario_nivel_inicial_h', `Tiempo que bastaría para el salario real de ${a.anio}`], ['plustrabajo_h', 'Plustrabajo']];
  legend('l-fz', s1.map((x) => x[1]));
  lineChart('c-fz', U, s1.map(([key, label]) => ({ key, label })), { yfmt: (v) => v + ' h', tipfmt: (v) => d3.format('.1f')(v) + ' h', aria: 'Tiempo liberado por la fuerza productiva en EE.UU.' });
  const tb = $('t-fz');
  if (tb) {
    tb.replaceChildren();
    [['Tiempo liberado respecto de ' + a.anio, dsc.liberado_h, 100], ['convertido en plustrabajo', dsc.plustrabajo_h, dsc.plustrabajo_pct],
      ['convertido en más consumo obrero', dsc.consumo_h, dsc.consumo_pct], ['convertido en una jornada normal más corta', dsc.jornada_h, 0]]
      .forEach(([l, v, p]) => { const tr = document.createElement('tr'); [l, f1(v), f0(p) + ' %'].forEach((t) => { const td = document.createElement('td'); td.textContent = t; tr.append(td); }); tb.append(tr); });
  }
  const M = F.mundo || [];
  if (M.length) {
    const m = M[M.length - 1];
    document.querySelectorAll('.fz-wfin').forEach((e) => { e.textContent = m.anio; });
    set('fz-wmin', f0(m.min_productivo_dia) + ' min'); set('fz-wnec', f0(m.min_necesario_dia) + ' min'); set('fz-wpct', f0(m.poblacion_pct_mundo) + ' %');
    const s2 = [['min_productivo_dia', 'Trabajo productivo'], ['min_plustrabajo_dia', 'de él, plustrabajo'], ['min_necesario_dia', 'de él, trabajo necesario']];
    legend('l-fzw', s2.map((x) => x[1]));
    lineChart('c-fzw', M, s2.map(([key, label]) => ({ key, label })), { yfmt: (v) => v + ' min', tipfmt: (v) => d3.format('.0f')(v) + ' min', prov: (M.find((r) => r.poblacion_extrapolada) || {}).anio ?? -1, aria: 'Minutos diarios de trabajo productivo por habitante' });
  }
}

// Auditoría, bloque B: supuestos del plusvalor (sensibilidad)
function drawBB(B) {
  if (!B || !B.eeuu || !B.eeuu.length) return;
  $('supuestos').hidden = false;
  const E = B.eeuu, z = E[E.length - 1], e72 = E.find((r) => r.anio === 1972) || E[0], e48 = E[0];
  document.querySelectorAll('.bb-fin').forEach((e) => { e.textContent = z.anio; });
  set('bb-fh', f1(z.fin_hogares_pct_pv_b) + ' %'); set('bb-fh48', f1(e48.fin_hogares_pct_pv_b) + ' %');
  set('bb-sup', f0(z.supervision_pct_v_ramas) + ' %'); set('bb-sup72', f0(e72.supervision_pct_v_ramas) + ' %');
  set('bb-ec', f2(z.e_c_b4)); set('bb-ec0', f2(z.e_c));
  const s1 = [['r_b', 'Por ramas, pv/(c + v)'], ['r_b_b4', 'Por ramas, sin servicios financieros de los hogares'], ['r_c', 'Intra-rama, pv/(c + v)'], ['r_c_b4', 'Intra-rama, sin servicios financieros de los hogares']];
  legend('l-bb', s1.map((x) => x[1]));
  lineChart('c-bb', E, s1.map(([key, label]) => ({ key, label })), { yfmt: (v) => v + ' %', tipfmt: (v) => d3.format('.1f')(v) + ' %', aria: 'Tasa de ganancia de EE.UU. con y sin los servicios financieros de los hogares' });
  const s2 = [['fin_hogares_pct_pv_b', 'Servicios financieros pagados por los hogares / plusvalor (por ramas)'], ['supervision_pct_v_ramas', 'Remuneración que no es de obreros de producción y no supervisores / v por ramas']];
  legend('l-bb2', s2.map((x) => x[1]));
  lineChart('c-bb2', E, s2.map(([key, label]) => ({ key, label })), { yfmt: (v) => v + ' %', tipfmt: (v) => d3.format('.1f')(v) + ' %', aria: 'Explotación secundaria y supervisión' });
  const M = B.mundo || [], tb = $('t-bbm');
  if (M.length && tb) {
    tb.replaceChildren();
    const anios = [...new Set(M.map((r) => r.anio))].sort(); const sel = [anios[0], 2014, anios[anios.length - 1]].filter((a, i, x) => anios.includes(a) && x.indexOf(a) === i);
    const vars = ['base', 'B3: + renta comercial', 'B4: − servicios financieros de los hogares', 'B3 y B4'];
    vars.forEach((v) => { const tr = document.createElement('tr'); const base = (a) => M.find((r) => r.anio === a && r.variante === 'base');
      const cel = [v === 'base' ? 'Central' : v];
      sel.forEach((a) => { const r = M.find((q) => q.anio === a && q.variante === v); cel.push(r ? `${f0(r.plustrabajo_mmh)} (e = ${f2(r.e_horas)})` : '—'); });
      const u = M.find((q) => q.anio === sel[sel.length - 1] && q.variante === v), b = base(sel[sel.length - 1]);
      cel.push(u && b ? d3.format('+.1f')((u.plustrabajo_mmh / b.plustrabajo_mmh - 1) * 100) + ' %' : '—');
      cel.forEach((t) => { const td = document.createElement('td'); td.textContent = t; tr.append(td); }); tb.append(tr); });
    set('bb-a0', String(sel[0])); set('bb-a1', String(sel[1])); set('bb-a2', String(sel[2]));
  }
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
  legend('l-ref', REFS.map((s) => s[1]));
  lineChart('c-ref', ref, REFS.map(([key, label]) => ({ key, label })), { yfmt: (v) => v + ' %', tipfmt: (v) => d3.format('.1f')(v) + ' %', aria: 'Seis medidas de la tasa de ganancia de EE.UU., a la manera de las corrientes del debate' });
  drawLecturas(ref, masa, mtasas, decadas);
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
  lineChart('c-masa', masa, [{ key: 'masa_ramas', label: 'Por ramas' }, { key: 'masa_intra', label: 'Intra-rama' }], { tipfmt: d3.format(',.0f'), aria: 'Masa de plusvalor en poder de compra' });
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
  const k = (v, c) => `__educación y salud ${v}__${c}`, K = k('públicas fuera', 'con China');
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
    ['plustrabajo_mmh' + k('públicas fuera', 'sin China'), 'Bruta, sin China'], ['plustrabajo_mmh' + k('productivas', 'con China'), 'Bruta, con educación y salud públicas']];
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

function drawTF(T) {
  $('transformacion').hidden = false;
  const S = T.serie, z = S[S.length - 1];
  set('tf-desv', f1(z.desv_mediana) + ' %'); set('tf-rho', f2(z.spearman_mediana)); set('tf-pos', f0(T.pct_spearman_pos) + ' %');
  document.querySelectorAll('.tf-anio').forEach((e) => { e.textContent = T.anio_ramas; });
  document.querySelectorAll('.tf-n').forEach((e) => { e.textContent = T.n_paises; });
  const s1 = [['desv_mediana', 'Mediana de los países'], ['desv_USA', 'EE.UU.'], ['desv_DEU', 'Alemania'], ['desv_CHN', 'China'], ['desv_IND', 'India']];
  legend('l-tf-desv', s1.map((x) => x[1]));
  lineChart('c-tf-desv', S, s1.map(([key, label]) => ({ key, label })), { yfmt: (v) => v + ' %', tipfmt: (v) => d3.format('.1f')(v) + ' %', aria: 'Desviación media de los precios respecto de los valores' });
  const tb = $('t-tf-ramas'); tb.replaceChildren();
  T.ramas.forEach((r) => { const tr = document.createElement('tr'); [r.nombre, f2(r.precio_valor), r.composicion == null ? '—' : f1(r.composicion)].forEach((t) => { const td = document.createElement('td'); td.textContent = t; tr.append(td); }); tb.append(tr); });
  const s2 = [['altos_ingresos', 'Países de altos ingresos (de los 43)'], ['USA', 'EE.UU.'], ['DEU', 'Alemania'], ['JPN', 'Japón'], ['CHN', 'China'], ['IND', 'India']];
  legend('l-tf-com', s2.map((x) => x[1]));
  lineChart('c-tf-com', T.comercio, s2.map(([key, label]) => ({ key, label })), { tipfmt: (v) => d3.format(',.0f')(v) + ' mil millones de h', ref: 0, aria: 'Trabajo incorporado en el comercio exterior' });
  const MS = T.moseley;
  if (MS && MS.serie) {
    set('tf-red', f0(MS.redistribuido_pct) + ' %'); set('tf-cve', f2(MS.cv_efectivas)); set('tf-cvv', f2(MS.cv_valores)); set('tf-igu', f0(MS.pct_igualacion) + ' %');
    set('tf-dv', f1(MS.desv_valor) + ' %'); set('tf-dpp', f1(MS.desv_pp) + ' %'); set('tf-ppm', f0(MS.pct_pp_mejor) + ' %');
    const z2 = MS.serie[MS.serie.length - 1], a2 = MS.serie[0];
    set('tf-rm0', f1(a2.mundo_moseley) + ' %'); set('tf-rm', f1(z2.mundo_moseley) + ' %'); set('tf-rt', f1(z2.mundo_tssi) + ' %');
    const s4 = [['mundo_moseley', '43 países: Moseley (central)'], ['mundo_tssi', '43 países: TSSI'], ['USA_moseley', 'EE.UU.: Moseley'], ['USA_tssi', 'EE.UU.: TSSI'], ['CHN_moseley', 'China: Moseley'], ['CHN_tssi', 'China: TSSI']];
    legend('l-tf-mt', s4.map((x) => x[1]));
    lineChart('c-tf-mt', MS.serie, s4.map(([key, label]) => ({ key, label })), { yfmt: (v) => v + ' %', tipfmt: (v) => d3.format('.1f')(v) + ' %', aria: 'Tasa de ganancia de las ramas productivas, Moseley y TSSI' });
    const tm = $('t-tf-mr');
    if (tm) { tm.replaceChildren(); MS.ramas.forEach((r) => { const tr = document.createElement('tr'); [r.nombre, d3.format('+.1f')(r.transferencia_pct) + ' %', f1(r.tasa_en_valores) + ' %', f1(r.tasa_efectiva) + ' %'].forEach((t) => { const td = document.createElement('td'); td.textContent = t; tr.append(td); }); tm.append(tr); }); }
  }
  if (T.ponderada && T.ponderada.length) {
    const W = T.ponderada, w = W[W.length - 1];
    set('tf-pond', f0(w.plustrabajo_ponderado_mmh)); set('tf-sinpond', f0(w.plustrabajo_mmh)); set('tf-cnp', f1(w.pct_china_ponderado) + ' %');
    set('tf-wcn', f2(w.peso_china)); set('tf-win', f2(w.peso_india)); set('tf-wus', f2(w.peso_eeuu));
    const s3 = [['plustrabajo_mmh', 'Horas de trabajo explotado (sin ponderar)'], ['plustrabajo_ponderado_mmh', 'Horas del mercado mundial (ponderadas por productividad)']];
    legend('l-tf-pond', s3.map((x) => x[1]));
    lineChart('c-tf-pond', W, s3.map(([key, label]) => ({ key, label })), { tipfmt: d3.format(',.0f'), aria: 'Masa mundial de plustrabajo ponderada' });
  }
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
  set('t-sem', '40'); set('t-nec', f1(z.semana_tc_necesario) + ' h'); set('t-nec0', f1(a.semana_tc_necesario) + ' h');
  set('t-plus', f1(z.semana_tc_plustrabajo) + ' h'); set('t-plus0', f1(a.semana_tc_plustrabajo) + ' h');
  set('t-masa', f1(z.horas_plustrabajo_mmh)); set('t-masa0', f1(a.horas_plustrabajo_mmh));
  legend('l-sem', ['Trabajo necesario (semana de 40 h)', 'Plustrabajo (semana de 40 h)', 'Semana media pagada (tiempo completo y parcial)']);
  lineChart('c-sem', T, [{ key: 'semana_tc_necesario', label: 'Necesario' }, { key: 'semana_tc_plustrabajo', label: 'Plustrabajo' }, { key: 'semana_horas', label: 'Semana media pagada' }], { yfmt: (v) => v + ' h', tipfmt: (v) => d3.format('.1f')(v) + ' h', aria: 'Trabajo necesario y plustrabajo semanal' });
  lineChart('c-hplus', T, [{ key: 'horas_plustrabajo_mmh', label: 'Plustrabajo' }], { tipfmt: d3.format(',.1f'), aria: 'Masa anual de plustrabajo en horas' });
  set('t-desc-intro', `Entre ${Dc.desde} y ${Dc.hasta} la masa anual de plustrabajo se multiplica por ${f2(Dc.factor_total)}: horas de plustrabajo = obreros × horas por obrero × e/(1+e).`);
  const tb = $('t-desc'); tb.replaceChildren();
  Dc.factores.forEach((r) => { const tr = document.createElement('tr'); [r.factor, f2(r.multiplica), f1(r.aporte_pct) + ' %'].forEach((t) => { const td = document.createElement('td'); td.textContent = t; tr.append(td); }); tb.append(tr); });
  legend('l-melt', ['USD corrientes por hora', 'USD de 2017 por hora']);
  lineChart('c-melt', T, [{ key: 'expresion_monetaria_hora', label: 'Corrientes' }, { key: 'expresion_monetaria_hora_real', label: 'De 2017' }], { tipfmt: (v) => d3.format('.1f')(v) + ' USD', aria: 'Expresión monetaria del tiempo de trabajo' });
}

Promise.all(['meta', 'eeuu_bandas', 'eeuu_referencias', 'eeuu_quiebres', 'eeuu_decadas', 'eeuu_masa', 'mundo_tasas', 'mundo_masa', 'eeuu_trimestral', 'eeuu_sensibilidad'].map(get)).then(([meta, bandas, ref, quiebres, decadas, masa, mtasas, mmasa, trim, sens]) => {
  D = { meta, bandas, ref, quiebres, decadas, masa, mtasas, mmasa, trim, sens }; draw(); drawSismo(bandas, quiebres); indiceActivo();
  Promise.all([get('eeuu_tiempo'), get('eeuu_descomposicion')]).then(([T, Dc]) => { D.T = T; D.Dc = Dc; drawTiempo(T, Dc); });
  if (meta.mundo_horas) Promise.all([get('mundo_horas'), get('mundo_horas_paises')]).then(([H, Pz]) => { D.H = H; D.Pz = Pz; drawHM(H, Pz, meta); });
  if (meta.contratendencias) get('contratendencias').then((CT) => { D.CT = CT; $('contratendencias').hidden = false; drawCT(CT); });
  if (meta.transformacion) get('transformacion').then((TF) => { D.TF = TF; drawTF(TF); });
  if (meta.bloque_b) get('bloque_b').then((BB) => { D.BB = BB; drawBB(BB); });
  if (meta.fuerzas) get('fuerzas').then((FZ) => { D.FZ = FZ; drawFZ(FZ); });
  if (meta.ia) Promise.all([get('ia_agregado'), get('ia_empresas')]).then(([A, E]) => { D.iaA = A; D.iaE = E; drawIA(A, E); });
  let t; window.addEventListener('resize', () => { clearTimeout(t); t = setTimeout(() => { draw(); drawSismo(D.bandas, D.quiebres); if (D.T) drawTiempo(D.T, D.Dc); if (D.H) drawHM(D.H, D.Pz, D.meta); if (D.iaA) drawIA(D.iaA, D.iaE); if (D.CT) drawCT(D.CT); if (D.TF) drawTF(D.TF); if (D.FZ) drawFZ(D.FZ); if (D.BB) drawBB(D.BB); }, 150); });
}).catch((e) => { const l = document.querySelector('.lede'); if (l) l.insertAdjacentText('afterend', ' No se pudieron cargar los datos: ' + e); });
