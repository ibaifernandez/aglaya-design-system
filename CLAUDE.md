# CLAUDE.md — aglaya-design-system

## Qué es este repo

**La fuente CANÓNICA y SOBERANA de la identidad de marca AGLAYA** — tokens, tipografía, voz y logos. Todas las superficies AGLAYA **consumen de aquí**, nunca al revés: un token cambia *aquí primero* y las superficies siguen. Nada aguas arriba de esta carpeta es autoritativo.

## Orden de lectura

1. [`README.md`](README.md) — el canon: tokens, tipografía, voz, no-negociables.
2. [`SKILL.md`](SKILL.md) — la skill de marca (fuente de los no-negociables que sirve el MCP).
3. [`docs/CONTRACT.md`](docs/CONTRACT.md) — **el contrato de marca local**: quién manda, en qué orden, cómo se consume y quién NO puede consumir. Versión: la del tag (`git tag --list`), no una tecleada aquí.
4. `aglaya-ds-mcp/` — el **servidor MCP `aglaya-ds`**, read-only. Es la vía programática de consumo de marca para toda la flota. Qué tools expone hoy: la sesión que lo tenga montado, o `aglaya-ds-mcp/server.py`.

## Reglas duras

- Los **no-negociables de marca** los sirve el MCP (`get_nonnegotiables`) desde `SKILL.md` — no los parafrasees: consúltalos.
- **`ui_kits/` SÍ es marca AGLAYA** — es la composición canónica «así va todo junto», construida con los tokens de este repo. Cítala. Los que NO son marca son los **dummies de `aglaya-web`**, que viven en otro repo y tienen cada uno su propio sistema de diseño: **jamás cablear un dummy a esta marca.**
- Regla de marca AGLAYA: **eliminar > legacy**. Lo obsoleto se borra, no se archiva.
- `graphify-out/`: **no se versiona nada**, y los hooks de git de graphify están desinstalados. Decisión de flota: ningún repo guarda su grafo — nada de código lee uno, y un derivado guardado envejece con pinta de autoridad. Se corre a demanda (al entrar en un repo que no conoces, o al auditar) y no se mantiene. Sobre esta nave en concreto: la autoridad son sus archivos canónicos, que el MCP `aglaya-ds` lee en vivo; un grafo aquí sería una copia que caduca sin consumidor.

## AGLAYA · Flota — el capitán

Este repo es una **nave de la flota AGLAYA**. Existe un orquestador (el «capitán», repo `aglaya-orchestrator`). Qué es y qué no:

- **Es enrutador**: sabe qué nave contesta cada pregunta y a quién preguntar cuando no está aquí.
- **Es dueño del diseño**: los contratos inter-nave y la forma acordada de la flota los custodia él — se piden con `contrato("nombre")`.
- **Es ejecutor de lo barato**: hace los pases y arreglos triviales que no merecen abrir un hilo por nave.
- **NO es autoridad sobre el estado de este repo.** Su ficha de esta nave — `ficha("aglaya-design-system")` — describe el diseño acordado, no lo que hay hoy en disco. Si su ficha y este repo se contradicen, **gana el repo** — y hay que avisarle.

**Canal abierto:** MCP **`aglaya-atlas`**, montado en toda sesión de Claude de esta máquina. Contesta leyendo el atlas y citando `archivo:línea`. No hay que esperar un brief: se le pregunta.

**Aquí no se escriben rutas internas del atlas.** El único puntero fijo es el nombre del repo del capitán (`aglaya-orchestrator`); todo lo demás se pregunta por la puerta: `ficha("aglaya-design-system")` para nuestra forma en la flota, `contrato("nombre")` para un contrato concreto, `donde_pregunto("tema")` cuando no se sabe a quién, `buscar("términos")` para lo demás. Los tres primeros contestan citando su fuente, así que no se pierde trazabilidad — se gana que no caduque. Una ruta del atlas copiada aquí se rompe la próxima vez que él reorganice, y nos enteramos tarde.

### Esta sección no lleva estado

Cada pregunta se contesta yendo a mirar. La tercera columna es la que hace el trabajo: nombra el atajo que ya nos ha costado dinero.

| Pregunta | Se contesta con | NUNCA con |
|---|---|---|
| ¿En qué estado está este repo? (HEAD, rama, sucios, sin pushear) | `git status` / `git log` aquí mismo · `repo_estado` del MCP `aglaya-atlas`, que lo deriva de git | una línea de «último pase» ni un marcador de progreso escritos en este archivo · la ficha del atlas |
| ¿El MCP `aglaya-ds` está montado y qué tools expone? | la lista de tools del servidor en la sesión actual · `cd aglaya-ds-mcp && ./.venv/bin/python selftest.py` (con el `python3` del sistema falla: el SDK vive en el venv) | un conteo de tools tecleado aquí · «el MCP está arriba» leído en un doc |
| ¿Qué versión tiene el contrato de marca? | `git tag --list` · la cabecera de [`docs/CONTRACT.md`](docs/CONTRACT.md) | un número de versión tecleado en esta sección |
| ¿Un token, un logo, los no-negociables? | MCP `aglaya-ds` (`get_token`, `get_logo`, `get_nonnegotiables`) sobre `colors_and_type.css` y `SKILL.md` | parafrasear el `README.md` de memoria |
| ¿Qué contrato rige esta marca y quién la consume? | `contrato` y `quien_consume` del MCP `aglaya-atlas` | una lista de consumidores copiada aquí, que envejece a espaldas de todos |
| ¿Precios, ofertas, GTM? | `verdad_comercial` del MCP `aglaya-atlas` | una cifra escrita en este repo |
| ¿Un servicio de la flota responde ahora mismo? | el panel del proveedor · `servicios` y `flags` del MCP `aglaya-atlas` | un doc que diga que está arriba · la salida truncada de un comando |
| ¿Qué afirma el atlas sobre mí, y se lo puede creer? | `contradicciones` del MCP `aglaya-atlas` lista dónde el atlas se hace dueño de estado de esta nave | tratar `ficha` como autoridad sobre este repo: describe el diseño, no el disco |
| ¿Y si la pregunta no cae en ninguna fila? | `donde_pregunto` y `buscar` del MCP `aglaya-atlas` | inventar la respuesta desde esta tabla |

Reglas que siguen vigentes:
- **Antes de un cambio estructural** (tokens, voz, contrato de marca, tools del MCP), consulta el registro de contratos del atlas — toda superficie AGLAYA consume de este repo.
- **El capitán puede haber tocado docs de este repo**: sus commits van identificados. Este repo no lleva CHANGELOG — el registro es el git log.

**Esto lo vigila un script.** [`tools/guard_huella.py`](tools/guard_huella.py) lee esta sección y falla si reaparece una fecha de pase, un marcador de progreso `N/N`, un conteo, una versión a mano, un precio, un sello de `verificado`, un «está `encendido`» o un valor de marca en hexadecimal copiado a mano. Solo vigila esta sección — el resto del archivo tiene versiones y conteos legítimos. Exime lo que va entre acentos graves, y solo el fragmento: si necesitas nombrar un patrón, entrecomíllalo; no ensanches la exención.

Y **al guardián lo vigila su propia batería**: [`tools/test_guard_huella.sh`](tools/test_guard_huella.sh) sabotea este archivo con cada forma prohibida y comprueba que cada una se pone roja. Existe porque un guardián puede correr y dar verde estando roto — así se cazaron un patrón ciego a las MAYÚSCULAS y un precio que se colaba. Si tocas las reglas, corre la batería.

**Y los punteros los vigila el segundo guardián.** [`tools/guard_punteros.py`](tools/guard_punteros.py) recorre los `.md` versionados (salvo `graphify-out/`, regenerable) y falla por dos motivos: un **enlace markdown a un archivo propio que no está donde dice** —la avería de reorganizar el repo y dejar el puntero atrás— y **una ruta interna del atlas del capitán**, que caduca en cuanto él reorganiza. Aquí los acentos graves **no eximen**, al revés que en el guardián de la huella: una ruta se escribe casi siempre entrecomillada, así que eximirlas lo dejaría sin nada que morder. Su batería es [`tools/test_guard_punteros.sh`](tools/test_guard_punteros.sh), que además comprueba lo legítimo (enlaces externos, anclas, globs) para que no dé rojos falsos, y que no encontrar docs salga rojo en vez de dar un verde vacío.

**Y los valores los vigila el tercero.** [`tools/guard_valores.py`](tools/guard_valores.py) lee la paleta de `colors_and_type.css` **en vivo** y falla si uno de esos valores aparece copiado a mano en cualquier otro archivo versionado — en hexadecimal, con alfa, en forma corta o escrito como `rgb()`. Además cruza `products/products.json` contra los tokens del CSS, porque ese manifiesto es un segundo domicilio legítimo y desviarse en silencio sería mentir con cara de canon. **No lleva ni un valor dentro**: cambia el rojo y persigue el nuevo; añade un acento de producto y queda protegido sin tocarlo. No vigila el negro ni el blanco puros (genéricos, darían rojos falsos) ni los SVG de `assets/` y `products/`, que llevan el color pintado dentro: eso es el artefacto, no una cita, y si el color cambia hay que reexportarlos a mano. Los acentos graves **no eximen**, como en el de punteros. Su batería es [`tools/test_guard_valores.sh`](tools/test_guard_valores.sh).

**Y el MCP se prueba a sí mismo.** [`aglaya-ds-mcp/selftest.py`](aglaya-ds-mcp/selftest.py) llama a cada tool declarando si debe responder o debe rechazar — la segunda mitad importa: sin ella, un servidor que nunca falla pasaría el test trivialmente. [`aglaya-ds-mcp/zerocopy_test.py`](aglaya-ds-mcp/zerocopy_test.py) edita el CSS canónico en caliente y comprueba que la respuesta cambia sin reiniciar. Y [`aglaya-ds-mcp/test_selftest.sh`](aglaya-ds-mcp/test_selftest.sh) rompe el servidor de tres formas para comprobar que el selftest se pone rojo — existe porque la versión anterior no podía: un rechazo viaja con `isError` en falso y colaba.

Todo corre en CI ([`.github/workflows/huella.yml`](.github/workflows/huella.yml)) y a mano:

```
python3 tools/guard_huella.py
bash tools/test_guard_huella.sh
python3 tools/guard_punteros.py
bash tools/test_guard_punteros.sh
python3 tools/guard_valores.py
bash tools/test_guard_valores.sh
```

El MCP necesita su venv (ver [`aglaya-ds-mcp/README.md`](aglaya-ds-mcp/README.md)); con el `python3` del sistema falla por dependencias:

```
cd aglaya-ds-mcp && ./.venv/bin/python selftest.py
cd aglaya-ds-mcp && ./.venv/bin/python zerocopy_test.py
cd aglaya-ds-mcp && bash test_selftest.sh
```
