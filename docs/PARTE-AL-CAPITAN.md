# Parte al capitán — la inversión, y esta nave como primer caso

> **Documento de un solo uso.** Cuando el capitán lo aplique, **bórralo**:
> `eliminar > legacy`. No es un registro; el registro es el git log.
>
> Escrito desde `aglaya-design-system` para `aglaya-orchestrator`. **Aquí no
> se ha tocado nada de su repo** — este archivo es la propuesta, la decisión
> es suya.

---

## −1 · La decisión de Ibai: cambia quién es la primera parada

Esto no es un hallazgo de esta nave. Es **una decisión de diseño de flota**, y
el diseño lo custodias tú. Se te traslada para que la sostengas, no para que
la aceptes.

**Antes:** se te preguntaba a ti primero y tú contestabas por las naves.
**Ahora:** la nave es la autoridad sobre sí misma y tú **enrutas** hacia ella.

Con dos sombreros que conviene no mezclar:

| Dominio | Tu papel | Por qué |
|---|---|---|
| **Marca y flota** | Enrutador. **Cero estado.** | Gana el repo. Tú sabes a qué puerta llamar, no qué hay detrás. |
| **Comercial** (precios, ofertas, GTM) | **Fuente autoritativa.** | Ahí no hay codebase que te contradiga: la decisión vive en ti. |

**Lo que esto NO es: una degradación.** Pierdes una autoridad que nunca fue
real —el estado ajeno— y conservas entera la que sí lo es: los contratos
inter-nave, la forma acordada, y lo comercial, donde mandas sin discusión.

### La corrección que hay que hacer al modelo

La primera versión de esta idea era «cada nave te vuelca información y tú la
curas». **Eso reintroduce el problema por la puerta de atrás:** volcado + curado
= copia derivada con pinta de autoridad, que es exactamente lo que la flota
lleva meses matando (grafos desversionados, rutas del atlas fuera de los docs,
guardianes de huella).

Lo que sí funciona ya está probado en esta nave: su MCP **no guarda nada**,
lee los archivos canónicos en cada llamada. Sube ese patrón a la flota.

> **La regla, en una línea: puedes custodiar acuerdos; nunca estado.**
> Un acuerdo no caduca solo — lo cambias tú. El estado caduca mientras duermes.

Para comunicación entre naves: **centralita que las presenta, no buzón que se
queda la copia del mensaje.**

### Por qué ahora

Se te preguntó por el estado de cuatro repos y la respuesta fue que estaban
perfectos. Al menos uno no lo estaba: tenía deuda de meses en disco.

**No es un reproche a tu ficha** — la ficha nunca dijo que estuviera perfecto;
describe diseño, y en eso acertaba. El fallo fue de reparto: preguntarte a ti
por estado. Tu propia cabecera ya lo resolvía («gana el repo») y nadie la
estaba usando.

---

## −0.5 · Esta nave como primer caso: qué significa «una nave preguntable»

La inversión no se decreta, se demuestra. Esta es la primera y va sola; las
demás no han empezado. Lo que aquí quedó montado, por si te sirve de patrón
al enrutar a las siguientes:

1. **Ningún documento afirma estado.** Lo vigila un guardián en CI. Donde
   antes había un dato, ahora hay *con qué se contesta esa pregunta*.
2. **Cada guardián tiene batería de sabotaje.** Un guardián puede correr y dar
   verde estando roto — eso ya pasó aquí dos veces. La batería rompe el repo a
   propósito y comprueba que se pone rojo.
3. **La interfaz declarada está probada, y la prueba puede fallar.** El
   selftest del MCP no podía ponerse rojo: certificaba. Ahora cada llamada
   declara si debe responder o rechazar, y tiene su propia batería.
4. **Los valores viven en un sitio y se comprueba mecánicamente.** No es una
   norma escrita: es un guardián que lee la paleta en vivo y falla si aparece
   copiada en cualquier archivo versionado.
5. **CI hace el bootstrap desde cero.** Esto destapó que el comando de montaje
   documentado **no funcionaba para nadie que clonase el repo**. Llevaba así
   desde siempre, invisible porque el entorno local ya estaba hecho.

> **El punto 5 es el que más te sirve como enrutador.** Si en el atlas hay
> naves cuyo montaje «está documentado» pero nadie ha repetido desde cero,
> ahí hay la misma avería esperando, y no se ve desde ningún documento.

**Y una trampa que evitar:** no conviertas esta lista en una casilla que
guardes por nave. Sería volcado con otro nombre. Es un patrón que cada nave
demuestra corriendo, no un sello que tú registras.

---

## 0 · Lo primero: no te fíes de este parte

Todo lo que sigue se puede comprobar en un minuto sin creerme:

```
git -C <ruta a aglaya-design-system> log --oneline -12
cd <ruta a aglaya-design-system> && python3 tools/guard_valores.py
cd <ruta a aglaya-design-system>/aglaya-ds-mcp && ./.venv/bin/python selftest.py
```

Y el estado real, siempre, con `repo_estado("aglaya-design-system")`, que lo
deriva de git. Este archivo describe un cambio; **no es autoridad sobre nada.**

---

## 1 · El cambio que sí hay que hacer en la ficha

**Un solo cambio, y es una resta.** La ficha cita un archivo nuestro por nombre.
Es el único puntero duro que tiene, y por tanto lo único suyo que se rompe si
reorganizamos.

En la sección **«Brief para pegar»**, esta frase:

> **Empieza por las instrucciones de repo (CLAUDE.md)**, que te dan el orden de lectura y una tabla de «pregunta → dónde se contesta → con qué NUNCA».

Debería quedar:

> **Empieza por las instrucciones de repo**, que te dan el orden de lectura y una tabla de «pregunta → dónde se contesta → con qué NUNCA».

Por qué: es exactamente la regla que la propia ficha se aplica en la cabecera
(«aquí no vas a encontrar ni un token, ni una versión, ni la lista de ficheros
del repo»). La fila **«Su propia puerta de entrada»** ya lo hace bien —dice
«sus instrucciones de repo» sin nombrar el archivo—, así que es una
inconsistencia dentro del mismo documento, no un criterio distinto.

**El resto de la ficha no necesita tocarse.** Se ha revisado entera contra el
disco de hoy y sigue siendo verdad: la familia, la caja de decisión sobre la
soberanía, las dos interfaces sancionadas, quién bebe y quién no, y las líneas
rojas. `contradicciones("aglaya-design-system")` sigue devolviendo cero
afirmaciones de estado, que es como tiene que estar.

---

## 2 · Lo que ha cambiado aquí y **puede** interesarte

No son cambios que la ficha deba recoger —son estado, y el estado no vive en el
atlas—, pero afectan a cosas que tú enrutas. Decide tú si te sirven.

### 2.1 · Una de tus «fugas» estaba dentro de esta nave

Tu ficha avisa, y con razón:

> ⚠️ **Ojo: hay consumo real por fuera de esas dos interfaces.** […] No son interfaces: son fugas […]
>
> **Cablear el DS a una nave es trabajo real, no una casilla.** Antes de proponer «hazlo con el design-system», comprueba en el repo consumidor si de verdad bebe de aquí — imports contra valores hardcodeados. **Tener el recetario no es cocinarlo.**

Ese aviso apuntaba a otros repos. Resulta que **el caso más grave estaba aquí
dentro**: `ui_kits/website/`, que esta nave declara «composición canónica»,
tenía su propia copia de los tokens —el rojo, el verde y las superficies
tecleados a mano— y **no enlazaba la hoja canónica por ningún lado**. Y ya
había derivado: su «brand light» era un rojo distinto del canónico, y su
superficie base un tono que no existe en la hoja de tokens.

Cerrado. El kit importa el canon y su `:root` es solo una tabla de alias.

**Lo que esto te aporta como enrutador:** cuando alguien te diga «esa nave ya
consume del design-system», la respuesta correcta no es mirar un doc. Es
mirar si hay imports o valores copiados. Aquí lo mirábamos y nos habíamos
creído nuestro propio README, que afirmaba el consumo textualmente.

### 2.2 · «Jamás hardcodees valores en él» ya no es solo una advertencia

Tu ficha dice del MCP: *«cuyo core lee los ficheros en caliente: **jamás
hardcodees valores en él**»*. Era cierto del core, y falso del resto: el
manifiesto de componentes que sirve `get_component` llevaba el rojo escrito a
mano, así que el servidor **estaba sirviendo valores copiados**.

Cerrado, y ahora lo vigila un guardián que lee la paleta en vivo y falla si un
valor de marca aparece copiado en cualquier archivo versionado. Corre en CI con
su batería de sabotaje.

**Consecuencia para la flota, y es la que importa:** la obligación que el
contrato de marca impone al consumidor —«construir con estos tokens, no
copiados a un archivo del consumidor»— ya se cumple del lado del emisor. Antes
la pedíamos sin cumplirla.

### 2.3 · La interfaz declarada ahora está probada, no solo afirmada

El selftest del MCP no podía ponerse rojo: un rechazo del servidor viaja con
`isError` en falso y el test lo imprimía y salía 0. Se ha reescrito para que
cada llamada declare si debe responder o debe rechazar, y tiene su propia
batería que rompe el servidor de tres formas para comprobar que sale rojo.

CI ya no mira solo la prosa: monta el venv desde cero, corre el selftest, su
batería y la prueba de zero-copy.

**Dato para ti:** ese bootstrap desde cero destapó que el comando de montaje
que documentaba el README **no funcionaba para nadie que clonase el repo**.
Llevaba así desde que existe, invisible porque el venv local ya estaba hecho.
Si en el atlas hay alguna nave cuyo montaje «está documentado» pero nadie ha
repetido desde cero, ahí hay la misma avería esperando.

---

## 3 · Lo que NO hay que cambiar, dicho a propósito

Para que no se cuele por buena voluntad:

- **No añadas a la ficha el guardián nuevo, ni el número de tools, ni qué
  cubre CI.** Es estado. Envejece. La ficha ya declara en su cabecera que no
  guarda eso, y acierta.
- **No corrijas la advertencia de encoding** («sus docs han arrastrado guiones
  tipográficos y mojibake»). Se ha limpiado un caso —un token duplicado con un
  carácter roto en la hoja canónica— pero la advertencia sigue siendo útil: la
  causa (un `perl -i` mal codificado) puede repetirse.
- **No toques la advertencia sobre `check_voice`.** Sigue siendo un heurístico
  y sigue teniendo falsos positivos. Nada de eso ha cambiado.
- **No conviertas nada de esto en una fecha de pase ni en un «verificado el
  …».** Aquí dentro eso lo tumba un guardián en CI; en tu ficha lo tumba tu
  propia doctrina.

---

## 4 · Y una pregunta para ti, que es de tu jurisdicción

Se te preguntó por el estado de esta nave y la respuesta fue que estaba
perfecta. No lo estaba: los hallazgos de arriba llevaban meses en disco.

No es un reproche sobre la ficha —**la ficha nunca dijo que estuviera
perfecta**; describe diseño, y en eso acertaba—. Es sobre qué contestas cuando
te preguntan por estado. Tu propia cabecera ya lo resuelve («gana el repo»),
así que la pregunta práctica es si merece la pena que **`ficha()` devuelva ese
aviso en la respuesta**, no solo en el cuerpo del documento: quien pregunta por
una nave casi nunca lee la cabecera antes de creerse el contenido.

Decisión tuya. Aquí solo se aporta el caso.
