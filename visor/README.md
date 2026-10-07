# Visor de marca

Una ventana a la marca: **las normas primero, los valores después**. No es
documentación — no guarda ni un dato. Todo lo que enseña lo lee del canon en el
momento de pedirlo.

## Para qué pantalla está hecho

**El visor es para ordenador.** Decisión de Ibai del 2026-10-07, escrita aquí
porque es aquí donde se mide: lo que se vea mal en ancho de móvil **no es un
defecto del visor**, y una medición que lo señale no cuenta como hallazgo.

Está escrito porque ya costó trabajo: en el PR #51 se midió en las dos ramas
que a 375 px la ficha de componente se salía 247 px de su caja, y se dio por
hallazgo bueno. Con la decisión tomada, esa clase de medición deja de contar
**para el visor** — pero eso solo lo sabía quien estuvo en la conversación.

**Lo que esto NO es:**

- **No es permiso para que el visor se rompa.** Lo que deja de ser defecto es
  el ancho de móvil, no la legibilidad: **el scroll horizontal en escritorio
  sigue siendo un fallo**, y fue justo lo que pidió Ibai en la tarjeta que dio
  origen a esta herramienta.
- **No se deshace lo ya construido.** Lo que el PR #51 arregló en estrecho está
  mergeado y no estorba; nadie lo revierte.
- **No vale para el resto de la nave.** Aquí no se ha dejado de medir en los
  dos anchos: solo el visor queda fuera.

### Lo que sí se mide en los dos anchos, y por qué

| Qué | Por qué se mide estrecho también |
|---|---|
| [`ui_kits/`](../ui_kits) | Es **marca AGLAYA**: la composición canónica «así va todo junto», que [`CLAUDE.md`](../CLAUDE.md) manda citar. Lo que se enseñe ahí roto se copia roto. |
| [`components/components.json`](../components/components.json) | Es lo que el MCP sirve a **toda la flota** con `get_component`: una ficha no se mira aquí, se consume desde otra nave y se pinta en la pantalla que sea. |

La diferencia no es de rigor, es de destino: **esas dos salen de esta casa; el
visor se mira aquí.** Para ser exactos sobre qué significa «salir»: ni
`ui_kits/` ni `components/` viajan dentro del paquete npm —`files` de
[`package.json`](../package.json) entrega el CSS, las fuentes, `bin/`,
`scripts/`, `dist/`, la licencia y dos documentos—; lo que sale de aquí es su
**contenido**, servido en vivo por el MCP y citado como referencia. El visor no
sale de ninguna de las dos formas.

## Cómo se arranca

Desde la raíz del repo:

```bash
python3 visor/servidor.py
```

Abre `http://127.0.0.1:8788`. **No hace falta instalar nada**: el `python3` del
sistema basta, porque `aglaya-ds-mcp/brand.py` no tiene dependencias — se
comprobó antes de escribir esto, y por eso el visor no arrastra el venv del MCP.
Se corta con Ctrl-C.

## Qué enseña, y de dónde lo saca

| Pestaña | Qué | De dónde |
|---|---|---|
| Normas | no-negociables de marca madre y de producto | `brand.get_nonnegotiables()` y `…("product")` |
| Valores | tokens en los dos modos, con su muestra, y el contraste de cada pareja | `brand.list_tokens(mode=…)` sobre `colors_and_type.css` |
| Voz | reglas de voz, vocabulario y frases vetadas | `brand.get_voice_rules()` |
| Componentes y productos | fichas y acentos | `brand.list_components()`, `get_component()`, `list_products()`, `get_accent()` |

**La regla que decide el diseño entero: no hay un segundo intérprete.** Las
normas salen del **mismo lector que usa el MCP**, así que lo que ves aquí es
exactamente lo que recibe cualquier nave que pregunte — no «las normas según la
web». El CSS canónico se sirve tal cual, sin copiarlo: los colores de la
pantalla los pinta `colors_and_type.css`.

Lo único que el visor calcula por su cuenta es el **contraste**, y lo hace en un
solo sitio, con los valores que el canon acaba de servir. Dos calculadoras del
mismo número son dos números que algún día discrepan.

## Sobre el contraste que verás

El número es un **suelo, no un veredicto**, como dice el canon: por debajo no
hay nada que discutir; por encima sigue decidiendo el ojo.

Las parejas no se cruzan todas contra todas. Las tintas `--fg-on-*` son **para
rellenos** —la blanca sobre el rojo de marca, la negra sobre el acento de un
producto, con la excepción del carmín de ConsentFlow— y se miden contra su
relleno. Cruzarlas con las superficies fabricaba ocho parejas que nadie pinta
nunca y las enseñaba en rojo; **un visor que enseña un fallo inventado hace
dudar del canon que está bien**.

## Qué NO hace

- **No escribe.** Ni un fichero.
- **No ejecuta guardianes ni baterías.** Un visor lee; un panel que ejecuta es
  otra cosa y otra decisión.
- **No viaja en el paquete.** `files` de `package.json` no lo incluye, y no se
  toca: esto es herramienta de casa, no marca entregada. Lo vigila
  `tools/guard_paquete.py`.
- **No sustituye a `preview/`.** Las 23 muestras siguen donde estaban. Qué
  cubre el visor de cada una está medido en la entrega de la tarjeta
  `6bce7501`; **si se borran o no, lo decide Ibai**, no esta herramienta.
- **No sirve el repo.** Fuera de `/api/*`, solo entrega el CSS canónico, sus
  dos ficheros propios y las tipografías de `fonts/`, comprobando que la ruta
  no se sale de ahí.
