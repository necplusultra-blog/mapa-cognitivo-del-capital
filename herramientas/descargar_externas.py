"""Descarga fuentes externas que no son accesibles desde el entorno de desarrollo y las guarda en
datos_cache/externo/ (se ejecuta en GitHub Actions con el workflow «Fuentes externas»).
Uso: python herramientas/descargar_externas.py URL=archivo [URL=archivo ...]  (o lee herramientas/externas.txt)"""
import os, sys, time, urllib.request

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datos_cache', 'externo')
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'}


def main():
    os.makedirs(DEST, exist_ok=True)
    pares = sys.argv[1:] or [l.strip() for l in open(os.path.join(os.path.dirname(__file__), 'externas.txt')) if l.strip() and not l.startswith('#')]
    log = []
    for par in pares:
        nombre, url = par.split(' ', 1)
        for intento in range(3):
            try:
                with urllib.request.urlopen(urllib.request.Request(url.strip(), headers=UA), timeout=300) as r:
                    datos = r.read(); ctype = r.headers.get('Content-Type')
                open(os.path.join(DEST, nombre), 'wb').write(datos)
                log.append(f'OK {nombre} {len(datos)} bytes {ctype} {url}'); break
            except Exception as e:  # noqa: BLE001
                if intento == 2: log.append(f'ERROR {nombre} {e!r} {url}')
                time.sleep(5)
    open(os.path.join(DEST, 'registro.txt'), 'w').write('\n'.join(log) + '\n')
    print('\n'.join(log))


if __name__ == '__main__':
    main()
