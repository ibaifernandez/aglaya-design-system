# Visor de marca

Una ventana a la marca: **las normas primero, los valores después**. No es
documentación — no guarda ni un dato. Todo lo que enseña lo lee del canon en el
momento de pedirlo.

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
