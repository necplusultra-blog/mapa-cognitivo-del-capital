# Cómo editar los textos del sitio

Todo el texto del sitio vive en esta carpeta, en archivos Markdown. La forma más cómoda de editarlos es **Pages CMS** (https://app.pagescms.org → repositorio sismografo-del-capital): cada página aparece como una colección y cada sección como una entrada, con el texto en un editor Markdown. Al guardar, Pages CMS hace un commit y el sitio se publica solo en unos cinco minutos. La configuración está en `.pages.yml`, en la raíz del repositorio.

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

## Encabezado de cada archivo

El bloque entre las dos líneas `---` del comienzo controla la sección:

- `id`: el ancla del enlace (`#tiempo`).
- `menu`: el texto que aparece en el índice lateral. Si falta, la sección no aparece en el índice.
- `oculta: si`: la sección se muestra sólo cuando sus datos están disponibles.
- `lugar: portada` o `lugar: pie`: el texto va en la portada o en el pie de página.

## Diseño

El aspecto visual está en `site/style.css` y el marco de cada página en `plantillas/`. Las fórmulas y los cálculos están en `sismografo/`. Si cambias un método, actualiza también su explicación aquí.
