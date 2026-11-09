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
npm install "git+https://github.com/ibaifernandez/aglaya-design-system.git#v1.6.0"
```

Sustituye el tag por el último publicado — `npm exec --no -- aglaya-tokens-version` te dice
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

### Si no tienes Node: el paquete de Python

**Es la vía oficial para quien no tiene Node.** No es un apaño ni una
alternativa de segunda: entrega lo mismo que la de npm —se comprueba clave a
clave en cada PR, `tools/guard_vias.py`— y se ancla a un tag igual que ella.

La misma marca, por la puerta del otro ecosistema. Existe desde que el primer
consumidor de la flota sin npm —un panel en Python— tuvo que elegir entre
copiarse el CSS o quedarse fuera.

```bash
pip install "git+https://github.com/ibaifernandez/aglaya-design-system@v1.6.0"
```

```python
from aglaya_tokens import TOKENS, MODES, VERSION, mode, css_path, fonts_path

TOKENS["--color-brand"]        # el valor del modo por defecto
mode("light")["--color-bg"]    # un modo completo: la base más lo que redefine
css_path()                     # el colors_and_type.css canónico, para servirlo
```

**Las mismas reglas, sin excepciones:** se ancla a un tag, nada de rutas de
disco en las dependencias, y nada de vendorizar. Y el mismo nombre de token:
`--color-brand`, no `color_brand`.

**Los valores no viajan guardados dentro.** `scripts/backend_tokens.py` los
deriva de `colors_and_type.css` al instalar —es el `prepare` de npm por la
puerta de Python— leyendo el canon con `aglaya-ds-mcp/brand.py`, el mismo
lector que usa el MCP. Por eso no hay un cuarto parser de CSS en la casa, y por
eso las dos vías publican mapas idénticos: se ha medido token a token.

Consecuencia que conviene saber: **`pip install --no-build-isolation` sobre un
árbol sin `setuptools` falla**, y falla a propósito. Un paquete que se instalara
sin derivar entregaría valores viejos sin decirlo.

Y el aviso de atraso también está en su idioma:

```bash
aglaya-tokens-version            # ¿voy por detrás?
aglaya-tokens-version --strict   # sale 1 si lo estás: gate de CI
```

### Lo que NO es vía de consumo: bajarse el CSS de una URL

**Descartado, y conviene saber por qué**, porque es lo primero que se le ocurre
a un consumidor sin npm y ya se propuso una vez aquí.

Bajar `colors_and_type.css` de una URL cruda del repositorio en el despliegue
tiene tres vicios, y el tercero es el que decide:

1. Convierte una dirección que el alojamiento regala en una **promesa de este
   repo**. Mover el archivo, renombrarlo o hacer privado el repositorio rompe al
   consumidor, y aquí no se entera nadie.
2. Le entrega un archivo que su código **no puede leer**: puede servir el CSS al
   navegador, pero no preguntar «¿cuánto vale `--color-brand`?» desde su
   lenguaje.
3. Lo deja **sin el aviso de atraso**. La pregunta «¿cuánto voy por detrás?» es
   la ventaja entera de depender en vez de copiar, y por esa vía no se puede
   hacer.

**Ninguna dirección de descarga directa de este repositorio es interfaz
pública.** No lo es hoy y no se convierte en una por usarla: si lo fuera, mover
o renombrar el CSS canónico pasaría a ser MAYOR, y este repo no abre esa puerta.
Quien no tenga Node usa el paquete de Python de arriba.

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
npm exec --no -- aglaya-tokens-version
```

**El `--no` es la mitad de la instrucción, no un adorno.** Ejecuta el binario
que este paquete instala y se niega a bajar nada: si el paquete no está, sale
con 1 y lo dice. `npx` a secas busca el nombre en el registro público cuando no
lo encuentra en el proyecto, y **en un CI, sin terminal interactiva, npm asume
`--yes` e instala sin preguntar** — así que un nombre que hoy está libre se
convierte mañana en código ajeno corriendo dentro del CI de un consumidor.

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

Monta **tres** consumidores, y el tercero existe desde que la marca se entrega
por dos ecosistemas:

| | Qué hace | Qué tiene que pasar |
|---|---|---|
| A | depende del paquete de npm | el valor **cambia** |
| B | se copió el CSS | el valor **no cambia** (control negativo) |
| C | depende del paquete de Python | el valor **cambia** |

Sin B la prueba no demostraría nada —un script que siempre dijera «cambió»
pasaría igual—, y sin C una de las dos vías podría guardar una copia dentro sin
que nadie lo notara.

---

## Publicar una versión

El cambio de token va primero; la publicación es lo que lo hace existir para
los demás.

Antes de publicar, la nave entera tiene que estar verde — los guardianes, sus
baterías, el MCP y la prueba de mutación (ver [`../CLAUDE.md`](../CLAUDE.md)).

**A `main` no se sube nada directamente, tampoco una release.** `main` solo
acepta cambios por PR. Por eso la release va en dos pasos, y el tag se pone
**después** del merge, sobre el commit que ya está en `origin/main`.

**1 · Una rama y su PR** con el cambio de versión. En el mismo commit se suben
las dos instrucciones de instalación (la de [`../README.md`](../README.md) y la
de «Cómo se depende» en este fichero) al tag nuevo: si no, salen viejas en cuanto se
publica.

```bash
git switch -c release/v1.1.1 origin/main
npm version patch --no-git-tag-version
git commit -am "release: tokens v1.1.1"
git push -u origin release/v1.1.1
gh pr create --fill
```

**2 · Después del merge, el tag.** Se busca el commit que puso esa versión en
`package.json` y se etiqueta ese. Así funciona igual con los tres métodos de
merge (merge, squash y rebase): el commit de merge no lleva la versión si el PR
entró por squash o por rebase, porque entonces no existe.

Se toma el **más antiguo** de los commits que tocan esa versión (`--reverse` y
`head -1`), no el último: si ya entró otra release detrás, el último es el que
**quitó** la versión, y el tag saldría con el `package.json` equivocado.

```bash
git fetch origin
git tag v1.1.1 "$(git log --reverse --format=%H -S'"version": "1.1.1"' origin/main -- package.json | head -1)"
```

**Qué contiene el árbol de ese tag, dicho en voz alta porque hoy hay que
deducirlo.** El árbol de un tag de release **no contiene** lo que entrara en
`main` después de que su rama saliera: el tag marca **el artefacto publicado**,
no el estado del repositorio ese día. Es la consecuencia directa del comando de
arriba, y es deliberada — así el árbol del tag es **exactamente el que alguien
midió y aprobó de una pieza**; apuntar al commit de merge metería dentro lo que
entró en medio, que se aprobó en otra medición.

**Y no afecta a ningún consumidor**, que es la parte sin la cual esta frase
alarma en vez de informar: lo que se instala no es el árbol. Medido sobre
instalaciones hechas desde el tag, el `.gitignore` no viaja en ninguno de los
dos paquetes — cero ficheros en el de npm y cero en el de Python. A quien le
importa el detalle es a quien **clona el tag para trabajar dentro**, no a quien
depende.

**Los tags del remoto son inmutables.** No se borran y no se mueven: sin
excepciones y sin actores de bypass. Un tag mal puesto no se corrige — se
publica otra versión.

**Las comprobaciones van antes del push, porque el push es lo que publica.** Si
una falla, no se sube nada: se borra el tag local con `git tag -d v1.1.1` y se
mira por qué.

```bash
git show v1.1.1:package.json | grep -q '"version": "1.1.1"' \
  && git merge-base --is-ancestor v1.1.1 origin/main \
  && git push origin v1.1.1
```

---

## Lo que aceptamos al publicar

Dicho en voz alta, porque es una obligación operativa que antes no existía:

- **Cada cambio de token exige publicación.** Cambiarlo en el CSS ya no basta:
  hasta que no hay tag, el consumidor no lo ve.
- **Un token roto aquí puede romper el build de un consumidor.** Antes no podía
  pasar, porque nadie dependía de nada.

Ese es el precio. Lo que se compra con él es que la deriva **se imprime** en
vez de ocurrir en silencio.
