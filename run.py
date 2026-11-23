"""Sismógrafo del capital — corre el pipeline completo.

    python run.py                 # descarga, calcula y escribe resultados/ y site/data/
    python run.py --sin-descarga  # recalcula con los datos ya descargados
"""
import argparse, json, os
from sismografo import descarga, eeuu, mundo, sitio, trimestral

RAIZ = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--datos', default=os.path.join(RAIZ, 'datos_brutos'))
    ap.add_argument('--sin-descarga', action='store_true')
    a = ap.parse_args()
    if not a.sin_descarga:
        descarga.descargar_todo(a.datos)
    out = os.path.join(RAIZ, 'resultados')
    ee = eeuu.calcular(a.datos, out)
    ee['trim'] = trimestral.calcular(a.datos, out, ee['F'])
    mu = mundo.calcular(a.datos, out)
    meta = sitio.escribir(ee, mu, os.path.join(RAIZ, 'site'))
    import glob, shutil
    desc = os.path.join(RAIZ, 'site', 'descargas'); os.makedirs(desc, exist_ok=True)
    files = sorted(glob.glob(os.path.join(out, '*.csv')))
    for fpath in files: shutil.copy(fpath, desc)
    with open(os.path.join(desc, 'index.html'), 'w') as f:
        f.write('<!DOCTYPE html><meta charset="utf-8"><title>Descargas — Sismógrafo del capital</title>'
                '<link rel="stylesheet" href="../style.css"><main class="sc"><h1>Descargas</h1>'
                f'<p class="muted">Resultados en CSV, actualizados el {meta["actualizado"]}. Licencia CC BY 4.0.</p><ul>'
                + ''.join(f'<li><a href="{os.path.basename(p)}">{os.path.basename(p)}</a></li>' for p in files)
                + '</ul><p><a href="../">← volver</a></p></main>')
    with open(os.path.join(out, 'meta.json'), 'w') as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    print(json.dumps(meta, ensure_ascii=False, indent=1))
