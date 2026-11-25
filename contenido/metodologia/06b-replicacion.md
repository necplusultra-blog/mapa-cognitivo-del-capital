---
seccion: "06b Replicación de las series de los autores"
id: replicacion
menu: Replicación de las series de los autores
---
## Replicación de las series de los autores

Las cinco tasas «a la manera de» los autores (§ anterior) comparten una definición común para que se puedan leer juntas. La replicación hace lo contrario: rehace cada serie con la definición que su autor publicó, con los datos vigentes de la BEA, y la contrasta con los valores que el autor informó. El módulo es `sismografo/replicacion.py`; los resultados están en `replicacion_series.csv`, `replicacion_contraste.csv` y `replicacion_tendencias.csv` (descargas).

La diferencia entre lo publicado y lo rehecho tiene dos fuentes que no se pueden separar del todo: las revisiones de las cuentas (la propiedad intelectual entra al capital en 1999 —software— y en 2013 —I+D y originales artísticos—; la revisión integral de 2023 corrigió la remuneración, las ganancias y los acervos) y lo que la reconstrucción no reproduce del método de cada autor. Por eso el criterio no es acertar a sus números, sino comprobar si las tendencias sobre las que cada lectura construye su diagnóstico siguen apareciendo.

| Autor | Valores publicados que se contrastan | Definición rehecha |
|---|---|---|
| Shaikh y Tonak (1994) | S\*/V\* y tasa marxiana S\*/K\*, 1948–1989 (cuadros 5.6 y 5.8) | S\* = producto neto empresarial sin vivienda arrendada − V\*; V\* = remuneración de los obreros de producción y no supervisores de las ramas productivas (desde 1972). Desde 1948, cota inferior con toda la remuneración de esas ramas. K = acervo neto (ellos: bruto) |
| Moseley (1991; 1997) | S/V, C/V, Uf/V, Us/V y tasa convencional en 1977 | V = salarios de producción y no supervisión en ramas productivas; Uf = resto de la remuneración empresarial; C = capital fijo productivo + inventarios; Us = capital fijo de comercio, finanzas, inmobiliario no residencial, alquiler y servicios jurídicos; S sin los impuestos a la producción netos de subsidios del sector empresarial |
| Kliman (2010; 2012) | Ganancia antes de impuestos / activos a costo histórico, 1978 y 2001 | Sociedades; depreciación a costo histórico en lugar de la corriente; denominador = acervo neto a costo histórico del cierre del año anterior. También ingreso de propiedad y ganancia total |
| Duménil y Lévy (2002) | Razones 1982/1948, 2000/1982 y 2000/1948 de la tasa amplia r_b de las sociedades (cuadro 3) | (valor agregado neto − remuneración) / acervo neto no residencial a costo corriente; variante sin propiedad intelectual |
| Roberts (2018; 2021) | Variación 1965–1982 y 1982–1997 de su tasa «toda la economía» | (ingreso nacional − remuneración) / (activos fijos privados no residenciales + remuneración), a costo histórico y corriente |

**Resultados.** Se reproducen la tasa de plusvalor de Shaikh y Tonak con V\* de obreros de producción (1975–1982, diferencias menores a 0,08; en 1985–1989 la rehecha queda entre 0,15 y 0,17 por encima), la tendencia de su tasa marxiana (variaciones 1975–1982 y 1982–1989 cercanas a las publicadas; el nivel es mayor porque el acervo neto es menor que el bruto), la proporción Uf/V de Moseley en 1977, la tasa antes de impuestos de Kliman en 1978 y, de manera aproximada, en 2001, y las variaciones de la tasa de Roberts que él publicó en 2018 (las de 2021, con una recuperación 1982–1997 mayor, se aproximan peor). La caída de 1948 a 1982 de Duménil y Lévy se aproxima; su recuperación de 1982 a 2000 (+45 %) no: con los datos de hoy es mucho menor, con o sin propiedad intelectual. La tasa convencional de Moseley se aproxima sólo bajo nuestra lectura de su identidad (S sin impuestos indirectos, C con inventarios), que el texto publicado no explicita.

**Límites.** La tasa de plusvalor de Shaikh y Tonak y la de Moseley no se pueden rehacer antes de 1972, porque los salarios de los obreros de producción por supersector (BLS CES) empiezan ese año; para 1948–1971 sólo hay la cota inferior por ramas. Duménil y Lévy imputan una remuneración al trabajo de los no asalariados en el sector empresarial; aquí sólo se replica su sector corporativo, donde esa imputación no es necesaria. Ninguna de las réplicas incorpora la explotación secundaria (B4), porque ninguno de los autores la deduce: son sus definiciones, no la del mapa cognitivo.
