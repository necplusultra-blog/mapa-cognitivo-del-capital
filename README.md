# Sismógrafo del capital

**Observatorio público y reproducible de la tasa y la masa de ganancia y de plusvalor, organizado como un multiverso de especificaciones teóricamente explícitas.**

El objetivo del sismógrafo es dar cuenta de las tendencias fundamentales de la producción capitalista contemporánea, mediante el estudio de diversos datos empíricos y el cruce de las principales interpretaciones marxistas, que se ponen a leer los mismos datos. Registra también el estado de las fuerzas productivas: el tiempo que libera la reducción relativa del trabajo necesario y en qué lo convierte el capital.

Un sismógrafo no predice el terremoto: registra temblores y rupturas. Este repositorio descarga datos públicos, recalcula cientos de especificaciones de la tasa de ganancia y detecta de forma endógena sus quiebres de tendencia. Cada especificación está ligada a una decisión teórica del debate marxista (trabajo productivo e improductivo, costo histórico o corriente, propiedad intelectual, etc.), para mostrar qué conclusiones resisten todas las decisiones y cuáles dependen de la teoría que se adopte.

Sitio público: https://necplusultra-blog.github.io/sismografo-del-capital/

## Qué calcula

- **EE.UU., desde 1948.** 240 especificaciones en una ventana común, más 32 con corrección intra-rama desde 1972.
  - Sector corporativo y no financiero: excedente neto, ganancia antes y después de impuestos.
  - Sector empresarial: *plusvalor ampliado* según el criterio de trabajo productivo declarado en la metodología del sitio.
  - Bifurcaciones: costo corriente o histórico, neta o bruta, propiedad intelectual dentro o fuera del capital, existencias, utilización de capacidad, y capital total o sólo productivo.
- **Masa real de plusvalor, tasa de plusvalor S/V y composición K/V**, por ramas y con corrección intra-rama (trabajadores de producción y no supervisores, BLS).
- **Quiebres endógenos** por especificación: tendencias lineales por tramos con selección por BIC, más un análisis de sensibilidad (tramo mínimo de 6, 8 o 10 años; criterio BIC o LWZ). Ningún corte se fija de antemano.
- **Estimación trimestral** de la tasa corporativa: ganancias trimestrales sobre capital interpolado. Los trimestres con capital extrapolado se marcan como provisionales.
- **Mundo**: núcleo reducido con la Penn World Table 11.0 (tasa bruta, neta y tasa interna de retorno), ponderada por capital o PIB, con y sin China.

Los resultados muestran la manifestación fenoménica de determinaciones categoriales; no las demuestran.

## Actualización

El flujo de trabajo `.github/workflows/actualizar.yml`:
- corre automáticamente el día 3 de cada mes;
- se puede lanzar con un clic desde **Actions › Actualizar el sismógrafo › Run workflow**;
- descarga los datos, recalcula todo, guarda los resultados versionados en `resultados/` y `site/data/`, y publica el sitio.

Los datos cambian cuando las fuentes publican: el BEA, cada trimestre y en su revisión anual de septiembre; la Penn World Table, cada pocos años.

## Uso local

```bash
pip install -r requirements.txt
python run.py                 # descarga, calcula y escribe resultados/ y site/data/
python run.py --sin-descarga  # recalcula con datos ya descargados en datos_brutos/
python -m http.server -d site # para ver el sitio en http://localhost:8000
```

## Fuentes

Todas son públicas y no requieren claves:
- U.S. Bureau of Economic Analysis: cuentas nacionales, activos fijos, PIB por industria (SIC y NAICS).
- Federal Reserve: cuentas financieras Z.1 y utilización de capacidad G.17, vía FRED.
- Bureau of Labor Statistics: CES, vía FRED.
- Penn World Table 11.0 (Feenstra, Inklaar y Timmer, 2015).

## Licencias y cita

- Código: MIT (`LICENSE`).
- Datos derivados, gráficos y textos: CC BY 4.0 (`LICENSE-DATA.md`).
- Para citar, véase `CITATION.cff`.

Investigación doctoral de Pablo Ignacio Jiménez Cea, *Los límites inmanentes del capital* (Doctorado en Sociología, ICSyH-BUAP; candidatura aprobada, conclusión prevista en agosto de 2029). Marco teórico: Jiménez Cea, P. I. (2026). The immanent dialectic of capital: Falling rate of profit and the crisis of late capitalism. *Capital & Class*. https://doi.org/10.1177/03098168261503922

Jiménez Cea, P. I. (2026). *Sismógrafo del capital: multiverso de la tasa de ganancia* [software y datos]. https://github.com/necplusultra-blog/sismografo-del-capital
