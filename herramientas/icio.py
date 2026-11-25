"""F4 v3: valores-trabajo con las tablas mundiales de la OCDE (ICIO; edición 2026, versión «regular»/SML).

El servidor de la OCDE rechaza las descargas automáticas: los zip se bajan a mano desde
https://www.oecd.org/en/data/datasets/inter-country-input-output-tables.html (versión «regular»/SML) y se procesan
localmente (ICIO_TMP=<carpeta con los zip> ICIO_ZIPS="2020-2024_SML.zip ..." ICIO_BORRAR=0 python herramientas/icio.py)
o se suben como adjuntos de la versión «icio-2025» del repositorio para el workflow «ICIO OCDE». El script procesa los
que encuentre. Guarda sólo resultados compactos en datos_cache/externo/icio/. Hoy: 2000–2005 sin 2003 (edición 2025) y 2015–2024
(edición 2026; 2023 y 2024 son proyecciones de la OCDE). El empleo de TiM llega a 2022: después se mantiene su estructura por rama y se escala con la
ocupación total de la PWT (fuente_horas = «TiM 2022 × ocupación PWT»).

Qué calcula, para cada año
--------------------------
Con la matriz mundial completa (unas 80 economías × 50 ramas), el tiempo de trabajo directo e indirecto que contiene un
dólar de producto de cada rama de cada país, con el origen efectivo de los insumos (ya no hace falta el promedio mundial
λ̄ de la versión con tablas nacionales):

    λ = l (I − D_φ A)⁻¹

  l   = horas trabajadas por dólar de producción (ocupados de la base TiM de la OCDE × horas anuales por ocupado de la PWT);
  A   = coeficientes técnicos mundiales; D_φ = diagonal con la fracción capitalista de cada rama proveedora:
        sólo la parte capitalista de una rama transfiere valor a quien le compra.
  φ   = 1 en las ramas productivas; 0 en comercio (G), finanzas (K), inmobiliario (L), administración pública (O) y
        hogares (T); 1 − g en educación (P) y salud (Q), con g la parte pública y sin fines de lucro (publico.py);
        en servicios profesionales (M), la parte de M71, M72 y M74–M75 en la producción de M según WIOD 2014
        (sin servicios jurídicos y contables ni publicidad, que son de circulación).

Para las regiones sin datos de empleo (resto del mundo) se imputa l con la mediana mundial de horas por dólar de valor
agregado de la misma rama y año.

Salidas
-------
icio_ramas.csv.gz : pais, anio, rama, produccion_musd (parte capitalista), fraccion_capitalista, horas_mill,
                    horas_por_dolar (λ), valor_precio (μ_c λ), exportaciones_musd, fuente_horas
icio_paises.csv   : pais, anio, expresion_monetaria_usd_hora (μ_c), desviacion_media, horas_cedidas_mill,
                    horas_recibidas_mill, transferencia_mill_h, horas_totales_mill, transferencia_pct_horas, fuente_horas
icio_registro.txt : diagnóstico (archivos, ramas, correspondencias con TiM, imputaciones)
"""
import io, os, re, sys, time, urllib.request, zipfile

import numpy as np, pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(RAIZ, 'datos_cache', 'externo', 'icio')
TMP = os.environ.get('ICIO_TMP', '/tmp/icio')
# Fuentes, en orden: los archivos que Pablo sube como adjuntos de la versión «icio-2025» del repositorio (el servidor de
# la OCDE rechaza las descargas automáticas desde GitHub Actions) y, si no están, el servidor de la OCDE.
BASES = os.environ.get('ICIO_BASES', 'https://github.com/necplusultra-blog/sismografo-del-capital/releases/download/icio-2025/ '
                       'https://webfs-sti.oecd.org/files/STI-PIE/ICIO/2026/').split()
ZIPS = os.environ.get('ICIO_ZIPS', '1995-2000_SML.zip 2001-2005_SML.zip 2006-2010_SML.zip 2011-2015_SML.zip 2016-2022_SML.zip').split()
ANIOS = range(2000, 2025)
ULT_TIM = 2022   # último año de TiM 2025; después, estructura de 2022 × ocupación total de la PWT
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'}
CERO = {'G', 'K', 'L', 'O', 'T', 'G45', 'G46', 'G47', 'K64', 'K65', 'K66', 'L68', 'O84'}
ALIAS = {'C24A': 'C241_2431', 'C24B': 'C242_2432', 'C241': 'C241_2431', 'C242': 'C242_2432', 'C30A': 'C301', 'C30B': 'C302T309',
         'A01_02': 'A01_02', 'B05_06': 'B05_06', 'B07_08': 'B07_08'}
NO_IND = {'TLS', 'VA', 'OUT', 'TOTAL', 'TAXSUB', 'VALU'}
LOG = []


def log(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def bajar(nombre):
    os.makedirs(TMP, exist_ok=True)
    dest = os.path.join(TMP, nombre)
    if os.path.exists(dest) and zipfile.is_zipfile(dest): return dest
    for base in BASES:
        try:
            t0 = time.time()
            with urllib.request.urlopen(urllib.request.Request(base + nombre, headers=UA), timeout=600) as r, open(dest, 'wb') as f:
                while True:
                    b = r.read(1 << 22)
                    if not b: break
                    f.write(b)
            if zipfile.is_zipfile(dest):
                log(f'descargado {base + nombre}: {os.path.getsize(dest) / 1e6:.0f} MB en {time.time() - t0:.0f} s'); return dest
            log(f'{base + nombre}: el archivo recibido no es un zip')
        except Exception as e:  # noqa: BLE001
            log(f'no disponible {base + nombre}: {e!r}')
    return None


def _anio(nombre):
    m = re.search(r'(19|20)\d\d', os.path.basename(nombre))
    return int(m.group(0)) if m else None


def leer_tabla(f):
    """Lee una tabla ICIO. Las etiquetas son «PAÍS_RAMA»; las regiones del resto del mundo tienen país con guion bajo
    (p. ej. «A2_X_C26»), por eso la rama se identifica por sufijo con la lista de ramas de un país conocido."""
    d = pd.read_csv(f, index_col=0)
    d.index = d.index.astype(str).str.strip(); d.columns = d.columns.astype(str).str.strip()
    cand = [r for r in d.index if r not in NO_IND and r in d.columns]
    ref = next((p for p in ('USA', 'DEU', 'FRA') if any(r.startswith(p + '_') for r in cand)), None)
    inds = sorted({r[len(ref) + 1:] for r in cand if r.startswith(ref + '_')}, key=len, reverse=True)
    def partir(r):
        for k in inds:
            if r.endswith('_' + k): return r[:-(len(k) + 1)], k
        return None, None
    filas = [r for r in cand if partir(r)[0] is not None]
    out = 'OUT' if 'OUT' in d.columns else ('TOTAL' if 'TOTAL' in d.columns else None)
    Z = d.loc[filas, filas].to_numpy(dtype=np.float64)
    x = d.loc[filas, out].to_numpy(dtype=np.float64) if out else d.loc['OUT', filas].to_numpy(dtype=np.float64)
    va = d.loc['VA', filas].to_numpy(dtype=np.float64) if 'VA' in d.index else x - Z.sum(axis=0)
    sf = set(filas)
    fdc = [c for c in d.columns if c not in sf and c != out and '_' in c]
    F = d.loc[filas, fdc].to_numpy(dtype=np.float64)
    pr = [partir(r) for r in filas]
    pais_f = np.array([a for a, _ in pr]); rama_f = np.array([b for _, b in pr])
    pais_fd = np.array([c.rsplit('_', 1)[0] for c in fdc])
    return dict(Z=np.nan_to_num(Z), x=np.nan_to_num(x), va=np.nan_to_num(va), F=np.nan_to_num(F), pais=pais_f, rama=rama_f, pais_fd=pais_fd)


def insumos():
    tim = pd.read_csv(os.path.join(RAIZ, 'datos_cache', 'ocde_tim_2025.csv.gz'))
    tim = tim.set_index(['pais', 'actividad', 'anio']).EMPN_miles
    pwt = pd.read_stata(os.path.join(RAIZ, 'datos_cache', 'pwt110.dta'), columns=['countrycode', 'year', 'avh', 'emp'])
    avh = pwt[['countrycode', 'year', 'avh']].dropna().set_index(['countrycode', 'year']).avh
    insumos.emp = pwt[['countrycode', 'year', 'emp']].dropna().set_index(['countrycode', 'year']).emp
    fg = os.path.join(RAIZ, 'resultados', 'mundo_horas_parte_publica.csv')
    G = pd.read_csv(fg).set_index(['pais', 'anio']).g if os.path.exists(fg) else pd.Series(dtype=float)
    fm = pd.read_csv(os.path.join(RAIZ, 'datos_cache', 'wiod_fraccion_productiva_M.csv')).set_index('pais').phi_M
    fm = fm[(fm > 0.05) & (fm < 0.95)]
    return tim, avh, G, fm


def _serie_cercana(s, pais, anio, defecto):
    try:
        z = s.xs(pais, level=0)
    except KeyError:
        return defecto
    z = z.dropna()
    if not len(z): return defecto
    return float(z.iloc[(z.index.to_series() - anio).abs().argmin()])


def calcular_anio(T, y, tim, avh, G, fm):
    Z, x, va, F, pais, rama, pais_fd = T['Z'], T['x'], T['va'], T['F'], T['pais'], T['rama'], T['pais_fd']
    n = len(x)
    gmed = float(G.median()) if len(G) else 0.75; fmmed = float(fm.median()) if len(fm) else 0.45
    phi = np.ones(n)
    for k in range(n):
        r = rama[k]; c = pais[k]
        if r in CERO or r.startswith(('G4', 'K6', 'L6', 'O8')): phi[k] = 0.0
        elif r.startswith('P') or r.startswith('Q'): phi[k] = 1 - np.clip(_serie_cercana(G, c, y, gmed), 0, 1)
        elif r == 'M' or r.startswith('M_'): phi[k] = float(fm.get(c, fmmed))
    # horas
    horas = np.full(n, np.nan); fuente = np.array(['imputada'] * n, dtype=object)
    codigos_tim = set(tim.index.get_level_values(1))
    sin_tim = set()
    yt = min(y, ULT_TIM)
    emp = getattr(insumos, 'emp', pd.Series(dtype=float))
    def escala(c):
        if y <= ULT_TIM: return 1.0
        a = _serie_cercana(emp, c, min(y, 2023), np.nan); b = _serie_cercana(emp, c, ULT_TIM, np.nan)
        return a / b if np.isfinite(a) and np.isfinite(b) and b > 0 else 1.0
    esc = {c: escala(c) for c in np.unique(pais)}
    etiqueta = 'TiM' if y <= ULT_TIM else 'TiM 2022 × ocupación PWT'
    for k in range(n):
        c, r = pais[k], rama[k]
        cod = r if r in codigos_tim else ALIAS.get(r)
        h_obr = _serie_cercana(avh, c, y, np.nan)
        if not np.isfinite(h_obr): h_obr = 2000.0
        e = tim.get((c, cod, yt), np.nan) * esc[c] if cod else np.nan
        if cod is None: sin_tim.add(r)
        if np.isfinite(e):
            horas[k] = e * h_obr / 1000; fuente[k] = etiqueta                    # millones de horas
    # ramas sin correspondencia exacta en un país con datos: horas del total del país por dólar de valor agregado
    for c in np.unique(pais):
        m = pais == c
        tot = tim.get((c, '_T', yt), np.nan) * esc[c]
        if np.isfinite(tot) and np.isnan(horas[m]).any():
            h_obr = _serie_cercana(avh, c, y, 2000.0)
            resto = tot * h_obr / 1000 - np.nansum(horas[m])
            hueco = m & np.isnan(horas)
            if resto > 0 and va[hueco].sum() > 0:
                horas[hueco] = resto * va[hueco] / va[hueco].sum(); fuente[hueco] = 'TiM (repartida por valor agregado)'
    # regiones sin empleo: mediana mundial de horas por dólar de valor agregado de la rama
    with np.errstate(divide='ignore', invalid='ignore'):
        hva = pd.DataFrame({'rama': rama, 'r': horas / va})[np.isfinite(horas / va) & (va > 0)].groupby('rama').r.median()
    falt = np.isnan(horas)
    horas[falt] = np.array([hva.get(r, np.nan) for r in rama[falt]]) * va[falt]
    horas = np.nan_to_num(horas)
    with np.errstate(divide='ignore', invalid='ignore'):
        l = np.where(x > 0, horas / x, 0.0)
        A = np.where(x[None, :] > 0, Z / x[None, :], 0.0)
    Mm = np.eye(n) - phi[:, None] * A
    lam = np.linalg.solve(Mm.T, l)                                                     # λ (I − D_φ A) = l
    filas_r, filas_p = [], []
    for c in np.unique(pais):
        m = pais == c
        w = phi[m] * x[m]; lp = lam[m]
        ok = (w > 0) & (lp > 0)
        if ok.sum() < min(10, m.sum() // 2) or w[ok].sum() <= 0: continue
        mu = w[ok].sum() / (lp[ok] * w[ok]).sum()
        v = mu * lp
        otros_col = pais != c
        exp = Z[m][:, otros_col].sum(axis=1) + F[m][:, pais_fd != c].sum(axis=1)
        flujos = np.concatenate([Z[~m][:, m], F[~m][:, pais_fd == c]], axis=1).sum(axis=1)   # lo que c compra a cada rama extranjera
        ex = exp * phi[m]; im = flujos * phi[~m]
        hx = float((lp * ex).sum()); hm = float((lam[~m] * im).sum())
        htot = float((horas[m] * phi[m]).sum())
        for j in np.where(ok)[0]:
            filas_r.append(dict(pais=c, anio=y, rama=rama[m][j], produccion_musd=w[j], fraccion_capitalista=phi[m][j],
                                horas_mill=horas[m][j], horas_por_dolar=lp[j], valor_precio=v[j], exportaciones_musd=exp[j],
                                fuente_horas=fuente[m][j]))
        p = dict(pais=c, anio=y, expresion_monetaria_usd_hora=mu, desviacion_media=float((w[ok] * np.abs(v[ok] - 1)).sum() / w[ok].sum()),
                 horas_totales_mill=htot, fuente_horas='TiM' if np.char.startswith(fuente[m].astype(str), 'TiM').mean() > .5 else 'imputada')
        if ex.sum() > 0 and im.sum() > 0:
            hrec = hm * ex.sum() / im.sum()
            p.update(horas_cedidas_mill=hx, horas_recibidas_mill=hrec, transferencia_mill_h=hrec - hx,
                     transferencia_pct_horas=(hrec - hx) / htot * 100 if htot > 0 else np.nan)
        filas_p.append(p)
    return filas_r, filas_p, sin_tim


def main():
    os.makedirs(DEST, exist_ok=True)
    tim, avh, G, fm = insumos()
    log(f'TiM: {tim.index.get_level_values(0).nunique()} economías; g: {len(G)} observaciones; φ_M: {len(fm)} países')
    R, P = [], []
    for nombre in ZIPS:
        z = bajar(nombre)
        if not z: continue
        with zipfile.ZipFile(z) as zf:
            nombres = [i for i in zf.namelist() if i.lower().endswith('.csv')]
            log(f'{nombre}: {nombres}')
            for i in nombres:
                y = _anio(i)
                if y not in ANIOS: continue
                t0 = time.time()
                with zf.open(i) as f:
                    T = leer_tabla(io.TextIOWrapper(f, encoding='utf-8'))
                if y == 2000 or not R: log(f'  {y}: {len(T["x"])} filas; ramas = {sorted(str(r) for r in set(T["rama"]))}; economías = {len(set(T["pais"]))}; demanda final = {T["F"].shape[1]} columnas')
                r, p, sin = calcular_anio(T, y, tim, avh, G, fm)
                if sin: log(f'  {y}: ramas sin código TiM: {sorted(sin)}')
                R += r; P += p
                log(f'  {y}: {len(p)} economías calculadas en {time.time() - t0:.0f} s')
        if os.environ.get('ICIO_BORRAR', '1') == '1': os.remove(z)
    if not R:
        print('No se encontró ningún archivo ICIO: no se cambian los resultados guardados.'); return
    pd.DataFrame(R).to_csv(os.path.join(DEST, 'icio_ramas.csv.gz'), index=False, compression='gzip', float_format='%.6g')
    pd.DataFrame(P).to_csv(os.path.join(DEST, 'icio_paises.csv'), index=False, float_format='%.6g')
    open(os.path.join(DEST, 'icio_registro.txt'), 'w').write('\n'.join(LOG) + '\n')


if __name__ == '__main__':
    sys.exit(main())
