# Cómo editar los textos del sitio

Todo el texto del sitio vive en esta carpeta, en archivos Markdown. La forma más cómoda de editarlos es **Pages CMS** (https://app.pagescms.org → repositorio mapa-cognitivo-del-capital): cada página aparece como una colección y cada sección como una entrada, con el texto en un editor Markdown. Al guardar, Pages CMS hace un commit y el sitio se publica solo en unos cinco minutos. La configuración está en `.pages.yml`, en la raíz del repositorio.

También puedes editarlos directamente en GitHub, sin instalar nada:

1. Abre el archivo (por ejemplo, `inicio/08-tiempo.md`).
2. Pulsa el lápiz («Edit this file»).
3. Cambia el texto y pulsa «Commit changes».

En unos cinco minutos, GitHub Actions reconstruye y publica el sitio. El avance se ve en la pestaña «Actions» del repositorio.

## Carpetas

- `inicio/`: la página principal. Hay un archivo por sección y el número inicial fija el orden. Para reordenar secciones, cambia los números de los nombres.
- `lectura/`: la página «Primera lectura de los resultados», la interpretación teórica de la medición.
- `metodologia/`: la página de metodología, también con un archivo por sección.

## Formato

Markdown corriente:

- `**negrita**` y `*cursiva*`.
- `[texto](enlace)` para enlaces.
- `## Título de sección` y `### Subtítulo`.
- Listas que empiezan con `-` o `1.`.
- Tablas con `|`.

Una línea `{: .nota }` justo debajo de un párrafo lo muestra como nota en letra pequeña.

Además hay atajos para los elementos que se llenan con datos. No cambies los identificadores (lo que va después de `grafico`, `tabla`, `cifra` o dentro de `{{ }}`): el programa los usa para encontrar dónde dibujar. Sí puedes cambiar todo el texto que los rodea, las etiquetas y los títulos de las columnas.

| Atajo | Qué hace |
|---|---|
| `{{hm-n}}` | inserta una cifra calculada |
| `{{.hm-fin}}` | igual, para cifras que se repiten (con punto) |
| `[[grafico c-hm]]` | dibuja un gráfico |
| `[[leyenda l-hm]]` | la leyenda de un gráfico |
| `[[tabla t-hm: Col 1 \| Col 2]]` | una tabla; los títulos de columna son editables |
| `[[cifra hm-n \| etiqueta \| nota]]` | una cifra destacada; varias seguidas forman una fila |
| `:::como Título` … `:::` | un desplegable de explicación («¿Cómo se calcula?») |
| `:::como+ Título` … `:::` | lo mismo, abierto por defecto |
| `:::lectura claves \| Título` … `:::` | una tarjeta de lectura teórica (sección «Seis lecturas»); al pasar el cursor se destacan las líneas indicadas en `claves` (separadas por comas; vacío = todas) |

## Encabezado de cada archivo

El bloque entre las dos líneas `---` del comienzo controla la sección:

- `seccion`: el nombre de la entrada en Pages CMS (ordena la lista; no aparece en el sitio).
- `id`: el ancla del enlace (`#tiempo`).
- `menu`: el texto que aparece en el índice lateral. Si falta, la sección no aparece en el índice.
- `oculta: si`: la sección se muestra sólo cuando sus datos están disponibles.
- `lugar: portada` o `lugar: pie`: el texto va en la portada o en el pie de página.

El pie de página está repetido en las tres páginas (`99-pie.md` de cada carpeta): si lo cambias, cámbialo en las tres.

## Diseño

El aspecto visual está en `site/style.css` y el marco de cada página en `plantillas/`. Las fórmulas y los cálculos están en `sismografo/`. Si cambias un método, actualiza también su explicación aquí.

## Explicación en lenguaje llano

Cada gráfico lleva, antes del gráfico, un párrafo que lo explica en palabras simples. Se escribe como un párrafo normal seguido, en la línea siguiente, de `{: .llano }`. El detalle técnico va en el desplegable `:::como`.

## Versión en inglés

El sitio tiene una versión en inglés británico en `site/en/` (index.html, reading.html, methodology.html). Sus textos están en `contenido/en/`, con las mismas carpetas y los mismos nombres de archivo que la versión en español; en Pages CMS aparecen como «Portada (inglés)», «Lectura (inglés)» y «Metodología (inglés)». El marco de esas páginas está en `plantillas/en/`.

- Si cambias un texto en español, cambia también el archivo del mismo nombre en `contenido/en/`. Los atajos (`{{…}}`, `[[…]]`, `:::como`) y los `id` del encabezado deben ser idénticos en las dos versiones; sólo se traducen las partes legibles.
- Convenciones: inglés británico (labour, analyse, -ise), comillas simples, punto decimal y coma de miles (2.05; 1,077), glosario de los artículos del autor (borderline capitalism, tendential fall of the rate of profit, countertendencies, living labour, real subsumption). El glosario completo está en el historial del proyecto (doc 00 del Project).
- Las etiquetas que el código escribe dentro de los gráficos y tablas (leyendas, nombres de países y de ramas, columnas) se traducen en `site/en/i18n.js`. Si una etiqueta nueva aparece en español en la versión inglesa, agrégala ahí.

## Fuente de los datos de cada gráfico

Debajo de cada gráfico va un párrafo con la fuente de los datos, con la clase `fuente`:

```
Fuentes: BEA: cuentas nacionales (NIPA) ...; BLS ... Cálculo propio.
{: .fuente }
```

Es obligatorio: el mapa cognitivo se sostiene en que cada cifra pueda rastrearse hasta su fuente. Si un gráfico cambia de datos, se actualiza su fuente (también en `contenido/en/`, con «Source:» o «Sources:»).
