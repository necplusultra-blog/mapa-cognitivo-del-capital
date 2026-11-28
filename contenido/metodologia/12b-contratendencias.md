---
seccion: "12b Contratendencias"
id: contratendencias
menu: Contratendencias
---
## Contratendencias

Se siguen las seis causas contrarrestantes de Marx (*El Capital*, Libro III, cap. XIV). La sexta, el aumento del capital accionario, se extiende al capital que devenga interés en general. Ninguna se mide con un único indicador: cada una se manifiesta en varias series que deben leerse junto con la tasa y la masa de plusvalor.

**Descomposición por fases.** La tasa de ganancia se escribe como r = e · (V/K), de modo que, entre dos años,

<div class="f">Δln r = Δln e − Δln(K/V)</div>

Desde 1972, con las horas de los obreros productivos, la composición en valor se separa en una composición técnica y un precio relativo:

<div class="f">K/V = (K<sub>real</sub> / H) · (P<sub>K</sub> / w) · P<sub>K</sub> = K<sub>costo corriente</sub> / (índice de cantidad × K<sub>2017</sub> / 100) · w = V / H</div>

El índice de cantidad y el stock a costo corriente son los del capital fijo privado no residencial del BEA (kcntotl1es00, k1ntotl1es00); K y V son los de la variante intra-rama. Los años de corte son los cinco años de quiebre más frecuentes en el conjunto principal de especificaciones (h = 8, BIC), con al menos seis años de separación: la periodización no se fija de antemano.

**Robustez sobre el conjunto de especificaciones.** La descomposición se repite para cada especificación empresarial sin ajuste por utilización y con denominador K (16 por criterio de trabajo productivo: costo corriente o histórico, neta o bruta, con o sin propiedad intelectual, todo el capital o sólo el productivo). Se publican la mediana y los percentiles 10 y 90 de los aportes, el porcentaje de especificaciones en que la tasa sube y, entre las especificaciones en que la composición sube, el porcentaje en que Δln e ≥ Δln(K/V) (contratendencias_fases_especificaciones.csv).

**Transferencia de tiempo de trabajo por comercio exterior.** Para cada país, h = H / PIB, con H = ocupados × horas anuales (PWT 11.0) y el PIB en dólares corrientes a tipo de cambio de mercado (Banco Mundial):

<div class="f">h<sub>X</sub> = Σ<sub>j</sub> X<sub>j</sub> h<sub>j</sub> / Σ<sub>j</sub> X<sub>j</sub> · T<sub>i</sub> = M<sub>i</sub> · h<sub>X</sub> − X<sub>i</sub> · h<sub>i</sub></div>

T > 0 indica apropiación de tiempo de trabajo ajeno. Se incluyen los años con al menos 100 países con horas (desde 2005). Es una aproximación sin insumos intermedios; una matriz insumo-producto mundial (OCDE ICIO) permitiría rastrear el contenido en horas de cada flujo (intercambio_horas.csv, intercambio_horas_paises.csv).

**Indicadores por contratendencia.**

| Contratendencia | Indicadores | Fuente |
| --- | --- | --- |
| Elevación del grado de explotación | tasa de plusvalor; producto por hora y remuneración real por hora; horas semanales; pluriempleo y tiempo parcial involuntario | BEA, BLS (OPHNFB, COMPRNFB, LNS12026619, LNS12032194, CE16OV) |
| Reducción del salario por debajo de su valor | salario real por hora de los obreros de producción; servicio de la deuda de los hogares | BLS (AHETPI), CPI, Reserva Federal (TDSP) |
| Abaratamiento del capital constante | precio relativo de la inversión; composición técnica y precio relativo capital/salario | BEA (A008RD, DPCERG, activos fijos) |
| Sobrepoblación relativa | tasa de empleo de 25 a 54 años; U-6; empleo vulnerable y desempleo mundiales; asalariados productivos | BLS, OIT vía Banco Mundial, WIOD/OCDE/OIT |
| Comercio exterior | ganancias recibidas del resto del mundo; comercio mundial sobre PIB; transferencia neta de horas por país y grupo de ingreso | BEA (B933RC, A051RC), Banco Mundial, PWT |
| Capital accionario y que devenga interés | ganancias financieras; intereses netos y dividendos de las no financieras; emisión neta de acciones; valor de mercado de las acciones y deuda de las no financieras sobre el PIB | BEA (A587RC, A445RC, B471RC, W326RC, B467RC, A466RC, A455RC), Reserva Federal Z.1 |

**Limitaciones.** El valor de la fuerza de trabajo no se observa: el salario real es un indicio, no una medida de su distancia al valor. La intensidad del trabajo, el trabajo de plataformas y la extensión de la jornada fuera de las horas pagadas todavía no tienen indicadores. La transferencia de horas por comercio exterior no rastrea los insumos intermedios.
