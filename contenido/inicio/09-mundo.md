---
seccion: "09 Tasa mundial"
id: mundo
menu: Tasa mundial
---
## Mundo: tasa y masa de ganancia

{{m-wsrc}}
{: .nota }

La tasa de ganancia de la economía mundial, sumando 79 países con los datos de la Penn World Table. Se mantiene estable durante casi medio siglo y cae desde 2008, en buena parte por el peso creciente de China, donde se acumuló una masa enorme de capital en poco tiempo. Sin China, la caída es menor.
{: .llano }

[[leyenda l-mundo]]
[[grafico c-mundo]]

### Masa mundial de ganancia bruta

La masa total de ganancia del mundo, en dólares constantes. Mientras la tasa cae, la masa sigue creciendo: el mismo patrón de dos caras que en EE.UU.
{: .llano }

[[leyenda l-wmasa]]
[[grafico c-wmasa corto]]

:::como ¿Cómo se calculan estos gráficos?
**Tasas** (Penn World Table 11.0, por país): bruta = (1 − labsh)·cgdpo / cn; neta = ((1 − labsh)·cgdpo − δ·cn) / cn; tasa interna de retorno real (irr) de la propia PWT. labsh es la participación del trabajo, cgdpo el PIB a PPA corrientes, cn el stock de capital a PPA corrientes y δ la tasa de depreciación. El promedio mundial pondera cada país por su stock de capital, en el panel de países con datos continuos desde 1960, con y sin China. Otras ponderaciones y paneles están en las descargas (mundo_especificaciones.csv).

**Masa:** Σ (1 − labsh)·rgdpna sobre el mismo panel, en billones de dólares de 2021 (rgdpna: PIB real de cuentas nacionales). La PWT mide la economía total: no distingue trabajo productivo e improductivo, así que esta masa es ganancia bruta en sentido amplio, no plusvalor. Para eso está la sección siguiente.
:::
