# PACKAGE — cómo se depende de la marca AGLAYA

Este repo publica sus tokens como paquete versionado. Antes de esto la marca
solo se podía **copiar**; ahora se puede **consumir**. Este documento dice qué
se publica, cómo se depende, cómo se versiona y qué pasa cuando un nombre
choca.

Lo que aquí NO se dice: qué superficie consume qué, ni cómo los usa cada
consumidor. Eso es de cada consumidor. Este repo publica.

---

## Qué se publica

El paquete **`@aglaya/design-tokens`**, cuyo contenido es:

| Qué | Qué es |
| --- | --- |
| `colors_and_type.css` | el canon, tal cual. No es una copia adaptada: es el mismo archivo que lee el MCP `aglaya-ds` y que vigilan los guardianes |
| `fonts/` | las tres familias, locales. El CSS las carga con rutas relativas, así que resuelven dentro del paquete sin red. **Son de terceros, bajo OFL 1.1**, y viajan con su licencia al lado — ver [`../fonts/README.md`](../fonts/README.md) |
| `LICENSE` | los términos del material de AGLAYA. No cubre las tipografías ni puede cubrirlas |
| `dist/tokens.json` · `dist/tokens.js` · `dist/tokens.d.ts` | las formas JSON/JS, **derivadas en la instalación** desde el CSS |
| `bin/aglaya-tokens-version` | el comando que imprime cuántas versiones vas por detrás |

`dist/` no está versionado a propósito. Un `tokens.json` commiteado sería una
segunda casa para cada valor de marca —justo lo que [`tools/guard_valores.py`](../tools/guard_valores.py)
persigue dentro del repo y lo que este paquete existe para cerrar fuera—, así
que lo fabrica [`scripts/build-tokens.mjs`](../scripts/build-tokens.mjs) en cada
instalación. npm ejecuta `prepare` también cuando la dependencia viene de git.

---

## Cómo se depende

Dependencia a un **tag por `git+https`**. El repo es público: sin token, sin
llave SSH.

```bash
npm install "git+https://github.com/ibaifernandez/aglaya-design-system.git#v1.1.0"
```

Sustituye el tag por el último publicado — `npx aglaya-tokens-version` te dice
cuál es, y `git ls-remote --tags https://github.com/ibaifernandez/aglaya-design-system.git`
los lista todos.

Reglas de la dependencia, y son duras:

- **Se ancla a un tag, nunca a una rama.** Una rama hace que tu build cambie
  sin que tú lo decidas, y entonces no has ganado control: has cambiado copiar
  por sorprenderte.
- **Nada de `file:`, `link:`, `workspace:` ni rutas relativas.** Funcionan en
  el disco donde se escriben y rompen en producción: el CI del consumidor
  (Netlify, por ejemplo) clona **solo su repo**, y este no está ahí.
  [`tools/guard_paquete.py`](../tools/guard_paquete.py) falla si alguna aparece.
- **Nada de vendorizar.** Copiar el CSS a tu repo pasa todas las pruebas menos
  la única que importa (ver «la prueba de mutación», abajo).

### Vías de consumo

```css
/* CSS — no necesita build. Es la vía principal. */
@import "@aglaya/design-tokens/tokens.css";
```

```js
// JS / JSON — fabricados al instalar.
import tokens from "@aglaya/design-tokens";
import { tokens } from "@aglaya/design-tokens/tokens.json" with { type: "json" };
```

La clave de un token es su nombre CSS completo: `tokens["--color-brand"]`. No
hay versión camelCase a propósito — un segundo vocabulario es un segundo sitio
donde discrepar, y la deriva que este paquete cierra empezó exactamente así.

Si instalas con `--ignore-scripts`, `dist/` no se genera: usa la vía CSS, que
no necesita build.

---

## Semver, explícito

La versión del paquete **es el tag del repo**. Una sola línea de versión, sin
dos numeraciones que se contradigan.

| Cambio | Nivel | Qué le pasa al consumidor |
| --- | --- | --- |
| Cambia el **valor** de un token existente | **parche** | su build no se rompe; **su píxel cambia**. Eso es justo lo que compró |
| Se **añade** un token, una clase `t-*`, una fuente o una vía de export | **menor** | nada de lo suyo cambia |
| Se **renombra** o se **elimina** un token o una clase `t-*` | **MAYOR** | se le rompe el build |
| Se elimina o cambia de forma una vía de `exports`, o sube el mínimo de Node | **MAYOR** | se le rompe el build |
| Se **añaden** términos o avisos legales que antes no se entregaban (la licencia de una fuente, la licencia del repo) | **menor** | no se le rompe nada; cambia lo que legalmente puede hacer |
| Se **retira** o se **restringe** una licencia ya publicada | **MAYOR** | puede perder el derecho a usar lo que ya venía usando |

La regla que resume todo:

> **El nombre de un token es la interfaz. El valor es el contenido.**
> Mover un valor es un parche. Mover un nombre es un mayor — aunque se llame
> «limpieza», aunque el nombre nuevo sea mejor.

Un mayor no se publica sin decir en el mensaje del tag qué nombres se movieron
y a qué. Este repo no lleva CHANGELOG: el registro es el `git log`.

### Licencias

Lo que el consumidor recibe y bajo qué términos:

- **Las tipografías son de terceros**, bajo SIL Open Font License 1.1, y cada
  familia viaja con su archivo de licencia dentro de `fonts/`. La licencia de
  este repo no las cubre ni puede cubrirlas. Detalle y procedencia:
  [`../fonts/README.md`](../fonts/README.md).
- **El resto del material es de AGLAYA**, con todos los derechos reservados —
  ver [`../LICENSE`](../LICENSE). Que el repo sea público es el mecanismo de
  entrega que necesita un CI ajeno, no una cesión de derechos.
- **Ninguna familia entra en `fonts/` sin su licencia al lado.** Lo empareja
  por nombre [`../tools/guard_paquete.py`](../tools/guard_paquete.py), así que
  también protege a la familia que todavía no existe.

---

## Cuántas versiones vas por detrás

Esta es la ventaja entera de depender frente a copiar. Copiar tampoco duele el
primer día: duele siete semanas después, cuando nadie sabe desde cuándo. Un
consumidor que copia no tiene forma de preguntar. Uno que depende, sí:

```bash
npx aglaya-tokens-version
```

- Al día → sale `0`.
- Atrasado → imprime el último publicado y la lista de versiones que faltan.
- `--strict` → sale `1` cuando va por detrás. Es el gate para un paso de CI.
- `--json` → la misma respuesta para automatizar.
- Si hay un **mayor** por delante lo dice aparte, porque la acción es distinta:
  no es «vas tarde», es «te van a romper nombres de token».
- Si **no puede mirar** (sin red, sin git, sin tags) sale `2`. «No pude
  comprobar» nunca se imprime como «estás al día»: ese verde vacío es cómo se
  desactiva una comprobación el primer día que falla la red.

---

## La colisión de nombres

**El caso concreto.** El primer consumidor ya tiene un custom property llamado
`--color-surface-2` con un valor distinto del que ese nombre tiene aquí: lo que
allí se llama `--color-surface-2` es, en la rampa canónica, el escalón
`--color-surface-3`. Mismo nombre, cosa distinta. Eso no es un detalle de
integración: es la definición de la deriva, y ya había ocurrido antes de que
nadie lo mirara.

**La decisión de este repo: se renombra en el consumidor. No hay mapa de
alias, y no lo va a haber.**

Por qué, dicho una vez para que no se relitigue:

- Un mapa de alias nos obliga a cargar el vocabulario equivocado de cada
  consumidor, y a cargarlo para siempre. **Congela la deriva dentro del
  contrato** en vez de cerrarla.
- Regla de marca AGLAYA: **eliminar > legacy**. Lo obsoleto se borra.
- La dirección del contrato es esta carpeta → el consumidor
  (ver [`CONTRACT.md`](CONTRACT.md)). Un alias la invierte: nos haría seguir a
  quien tiene que seguirnos.

**Qué implica, en la práctica, para quien consume:**

- **Los nombres del paquete ganan.** Si tienes un custom property con un nombre
  que el paquete declara, el tuyo sobra: bórralo o renómbralo. No hay empate
  posible — dos declaraciones del mismo nombre no conviven, gana la última que
  cargue, y depender del orden de carga es peor que la copia.
- **El paquete no prefija ni namespacea para esquivar la colisión.** Un
  `--aglaya-color-surface-2` sería un segundo vocabulario para el mismo color,
  que es la avería otra vez con otro nombre.
- **Para migrar**, compara tu `:root` contra el del paquete instalado — están
  en `dist/tokens.json`, y el MCP `aglaya-ds` sirve lo mismo en vivo con
  `list_tokens`. Quédate solo con lo que el paquete no declara.
- **Un token que necesitas y aquí no existe se pide aquí**, no se inventa allí.
  Se publica como menor y lo tienes en la siguiente versión. Inventarlo en tu
  repo es empezar la deriva de cero, con la lección ya pagada.

---

## La prueba que separa consumir de copiar

```bash
bash tools/test_mutacion.sh
```

Mueve un valor en el canon, reinstala en un consumidor de prueba y comprueba
que el valor entregado cambia **sin tocar un solo archivo fuente del
consumidor**. Una copia vendorizada pasa cualquier otra comprobación y falla
esta por construcción — por eso es la única que decide.

---

## Publicar una versión

El cambio de token va primero; la publicación es lo que lo hace existir para
los demás.

```bash
npm version patch --no-git-tag-version
```

```bash
git commit -am "release: tokens v1.1.1" && git tag v1.1.1 && git push origin main --tags
```

Antes de publicar, la nave entera tiene que estar verde — los guardianes, sus
baterías, el MCP y la prueba de mutación (ver [`../CLAUDE.md`](../CLAUDE.md)).

---

## Lo que aceptamos al publicar

Dicho en voz alta, porque es una obligación operativa que antes no existía:

- **Cada cambio de token exige publicación.** Cambiarlo en el CSS ya no basta:
  hasta que no hay tag, el consumidor no lo ve.
- **Un token roto aquí puede romper el build de un consumidor.** Antes no podía
  pasar, porque nadie dependía de nada.

Ese es el precio. Lo que se compra con él es que la deriva **se imprime** en
vez de ocurrir en silencio.
