# Fase D — Operaciones y mantenimiento

Auditoría `aglaya-design-system-2026-09-24-mariana` · commit auditado `17d95cc` · modo `report`.

## Cuadro de evidencias — Fase D

| Confianza    | Nº | % de la fase |
|--------------|----|--------------|
| PROVEN       | 11 | 100 %        |
| UNVERIFIABLE | 0  | 0 %          |
| **Total**    | **11** | 100 %    |

Fuente de la evidencia: code-read 6 · tool-external 5 (`gh api`, `git show`) · manual-verification 0.

Salud: 100 % PROVEN.

## Qué no aplica

No hay servicio en marcha, así que no aplican el seguimiento de errores, los logs estructurados, la monitorización de disponibilidad ni las alertas de producción. Aquí el «despliegue» es poner un tag, y lo que se vigila es el CI. El servidor MCP corre en local por stdio.

## Tabla de hallazgos

| ID | Confianza | Dim | Hallazgo | Evidencia | Severidad | Esfuerzo |
|----|-----------|-----|----------|-----------|-----------|----------|
| D-01 | PROVEN | docs | La portada enseña a copiar la marca, que es justo lo que prohíben el contrato y la guía del paquete | `README.md:206`, `:211-219`, `:224-228`, `:254` | MEDIA | 0,5 h |
| D-02 | PROVEN | docs | La portada describe el código de otro repo (aglaya.biz) como si fuera canon | `README.md:107`, `:132`, `:144-145`, `:148`, `:154` | BAJA | 0,5 h |
| D-03 | PROVEN | CI | `main` exige PR, pero no exige que el CI esté en verde ni ninguna aprobación | `evidencia/github-ajustes.txt` | MEDIA | 0,25 h |
| D-04 | PROVEN | entrega | Los tags son la versión publicada y nada impide moverlos ni borrarlos | `evidencia/github-ajustes.txt`, `docs/PACKAGE.md:82` | MEDIA | 0,25 h |
| D-05 | PROVEN | CI | Están apagados el escaneo de secretos, la protección al hacer push, las alertas de vulnerabilidades y Dependabot | `evidencia/github-ajustes.txt` | BAJA | 0,25 h |
| D-06 | PROVEN | CI | Las actions se anclan a tags que pueden moverse, y el repo no exige anclar por SHA | `.github/workflows/huella.yml:31-32`, `:78`, `:138`, `:151`, `:207`, `evidencia/github-ajustes.txt` | BAJA | 0,5 h |
| D-07 | PROVEN | ops | El enganche versionado apunta a una ruta de esta máquina: en cualquier otra bloquea todas las herramientas | `.claude/settings.json:4-11`, `evidencia/mutaciones.txt` | BAJA | 0,5 h |
| D-08 | PROVEN | calidad | No hay linter, formateador ni comprobación de tipos para Python ni para JS | ausencia de configuración; `.github/workflows/huella.yml` | MEDIA | 2 h |
| D-09 | PROVEN | procedencia | Hay un commit en `main` firmado como `github-actions[bot]` que se hizo en una máquina local | `evidencia/git-procedencia.txt` | BAJA | 0,25 h |
| D-10 | PROVEN | runbook | No hay procedimiento escrito para cuando se publica una versión mala | `docs/PACKAGE.md:195-242` | BAJA | 0,5 h |
| D-11 | PROVEN | docs | La lista de comprobaciones a mano de `CLAUDE.md` se deja dos baterías que el CI sí corre | `CLAUDE.md:74-99`, `.github/workflows/huella.yml:57`, `:118` | BAJA | 0,1 h |

**Recuento:** CRÍTICA 0 · ALTA 0 · MEDIA 4 · BAJA 7.

---

## Detalle

### D-01 · La portada enseña a copiar

- **Qué pasa.** La doctrina de la casa es depender del paquete y no copiarlo: «Depender, no vendorizar» (`docs/CONTRACT.md:33`) y «Nada de vendorizar» (`docs/PACKAGE.md:55-56`). La portada pública, que es lo primero que lee un agente, dice lo contrario en cuatro sitios:
  - «a self-contained folder you can drop anywhere» (`README.md:206`);
  - el ejemplo «Use it in production code» enlaza una copia local `./colors_and_type.css` (`README.md:211-219`);
  - «Unzip the folder into your project… The agent reads the tokens, copies assets» (`README.md:224-228`);
  - «copy the hex values… into Figma Variables, Tailwind config» (`README.md:254`).
- **Por qué importa.** Quien lo siga copia el CSS: la deriva que cierran la prueba de mutación y el paquete vuelve a empezar. La sección correcta, «Depend on it from another repo», viene después (`README.md:230-247`).
- **Severidad.** MEDIA (docs: instrucciones de uso que contradicen el contrato).
- **Arreglo.** Poner primero la vía del paquete. Reescribir o quitar las instrucciones de copiar. Para Figma y herramientas sin CSS, apuntar a `get_token` o a `dist/tokens.json`.

### D-02 · La portada describe el código de aglaya.biz

- **Qué pasa.** En «Visual Foundations», la portada mezcla reglas de marca con observaciones del sitio vivo, que es otro repo:
  - «`global.css` ships `border-radius: 0 !important`» (`README.md:107`);
  - cursor, banner de cookies y skip link fijos (`README.md:132`);
  - skip link y `prefers-reduced-motion` respetado (`README.md:144-145`);
  - el cursor propio (`README.md:148`);
  - la carpeta de iconos del sitio (`README.md:154`).
- **Por qué importa.** Desde aquí no se puede comprobar si esto sigue siendo verdad, y la composición canónica de este repo no implementa ninguna de esas cosas (A-05, A-11; `ui_kits/website/README.md:48`). Es lo que `CLAUDE.md` llama un derivado que envejece con pinta de autoridad, y va contra la dirección del contrato: la marca fluye de aquí hacia fuera, no al revés (`docs/CONTRACT.md:32`).
- **Severidad.** BAJA.
- **Arreglo.** Convertir cada frase en regla (qué debe hacer una superficie) o quitarla.

### D-03 · El CI aconseja, pero no bloquea

- **Qué pasa.** El ruleset «main: solo por PR» está activo, pero sus reglas son tres: `pull_request` con 0 aprobaciones, `non_fast_forward` y `deletion`. No hay regla de checks obligatorios (`evidencia/github-ajustes.txt`). Un PR con los guardianes en rojo se puede fusionar igual.
- **Por qué importa.** Todo el sistema inmune del repo (cuatro guardianes, sus baterías, el selftest, la prueba de mutación) vive en el CI. Lo cazaría todo, B-03 incluido, pero hoy solo avisa.
- **Severidad.** MEDIA (DevOps: el CI existe pero no se exige).
- **Arreglo.** Añadir al ruleset la regla de checks obligatorios con los jobs `guardianes de docs`, `MCP aglaya-ds` y `paquete @aglaya/design-tokens`.

### D-04 · El canal de publicación se puede reescribir

- **Qué pasa.** «La versión del paquete **es el tag del repo**» (`docs/PACKAGE.md:82`), y los consumidores se anclan a `#vX.Y.Z` (`README.md:234`). Pero no hay ningún ruleset sobre tags (`evidencia/github-ajustes.txt`: la lista de rulesets con destino `tag` sale vacía). Cualquiera con permiso de escritura puede mover o borrar un tag publicado.
- **Por qué importa.** Un consumidor con lockfile queda a salvo mientras no reinstale sin él. Uno sin lockfile recibe otra cosa con la misma versión. Hasta ahora se ha hecho bien: un error de v1.3.3 se corrigió publicando v1.3.4 (`git tag --list`), sin mover nada. Pero nada lo garantiza.
- **Severidad.** MEDIA.
- **Arreglo.** Un ruleset de tags `v*` que prohíba actualizarlos y borrarlos.

### D-05 · Las defensas de GitHub están apagadas

- **Qué pasa.** En `security_and_analysis` están desactivados `secret_scanning`, `secret_scanning_push_protection` y `dependabot_security_updates`, y `vulnerability-alerts` devuelve 404, que significa desactivado (`evidencia/github-ajustes.txt`). Tampoco hay configuración de Dependabot: `git ls-files .github` solo lista el workflow.
- **Por qué importa.** En un repo público, el escaneo de secretos es gratis. Es además la única forma de cubrir B-NV-02, porque el enganche no deja buscar secretos desde una sesión.
- **Severidad.** BAJA (endurecimiento).
- **Arreglo.** Activarlas en *Settings › Code security*, y añadir el fichero de configuración de Dependabot (`dependabot.yml`, dentro de `.github`) con los ecosistemas `pip` y `github-actions`.

### D-06 · Actions ancladas a tags

- **Qué pasa.**
  - `actions/checkout@v5`, `actions/setup-python@v6` y `actions/setup-node@v7` van ancladas a tags que su dueño puede mover (`.github/workflows/huella.yml:31-32`, `:78`, `:138`, `:151`, `:207`).
  - El repo tiene `allowed_actions: all` y `sha_pinning_required: false` (`evidencia/github-ajustes.txt`).
  - El job que publica las cifras tiene permiso de escritura (`.github/workflows/huella.yml:201-202`).
- **Severidad.** BAJA. Son actions de primera parte, pero el anclado por SHA es la práctica recomendada para cualquier job que escriba.
- **Arreglo.** Anclar por SHA con un comentario de la versión, y que Dependabot las mantenga (D-05).

### D-07 · El enganche solo funciona en esta máquina

- **Qué pasa.** `.claude/settings.json:4-11` versiona un enganche `PreToolUse` que se aplica a todas las herramientas y ejecuta `python3` sobre una ruta absoluta de otro repo en este disco. En cualquier otra máquina esa ruta no existe:
  - `python3` sale con código 2 (`evidencia/mutaciones.txt`: `exit=2`);
  - para Claude Code, un código 2 en `PreToolUse` bloquea la herramienta, que es exactamente como este mismo enganche ha bloqueado varias órdenes durante esta auditoría;
  - resultado: una sesión en la nube, o un colaborador que clone el repo, no puede usar ninguna herramienta.
- **Matiz.** Puede ser deliberado (cerrar en falso), pero no está escrito. `.gitignore:33-38` explica por qué el enganche se versiona, no qué pasa fuera de esta máquina.
- **Severidad.** BAJA.
- **Arreglo.** Documentarlo si es intencionado, o hacer que el enganche falle con un mensaje claro cuando falta el script.

### D-08 · Sin linter, formateador ni tipos

- **Qué pasa.** No hay configuración de ESLint, Prettier, ruff, mypy, Black, EditorConfig ni pre-commit: la búsqueda en `git ls-files` sale vacía, y `aglaya-ds-mcp/pyproject.toml` no tiene secciones `[tool.ruff]`, `[tool.mypy]` ni `[tool.black]`. El CI corre guardianes y pruebas, pero ninguna comprobación estática (`.github/workflows/huella.yml`).
- **Severidad.** MEDIA según el rubric de DevOps («no linter/types»). Hay atenuante: el código de producto es pequeño y está muy probado.
- **Arreglo.** Pasar `ruff` y `mypy --strict` sobre `aglaya-ds-mcp/brand.py` y `tools/`, y `node --check` o ESLint sobre `scripts/` y `bin/`.

### D-09 · Un commit de `main` con la identidad del bot

- **Qué pasa.** `d74d06e` («ci(cifras): publicar las cifras…») figura con autor y committer `github-actions[bot]`, sin firma, y con fecha `-0300`, la zona horaria de esta máquina y no la de un runner (`evidencia/git-procedencia.txt`). Entró por el PR #29 (`41af907`). GitHub lo atribuye a la cuenta del bot.
- **Contexto.** `tools/publicar_cifras.sh:141-142` configura esa identidad, pero solo dentro de su repositorio temporal (`git -C "$PUB"`), así que no es él quien la dejó global. La causa no se puede determinar desde el repo.
- **Severidad.** BAJA. Es la procedencia de un único commit, pero en un repo donde el propio CI firma como bot confunde quién escribió qué.
- **Arreglo.** Firmar commits (con el modo vigilante de GitHub) y comprobar `git config --global user.name` antes de hacer commit.

### D-10 · No está escrito qué hacer con una versión mala

- **Qué pasa.** «Publicar una versión» explica cómo publicar (`docs/PACKAGE.md:195-242`), pero no qué hacer si lo publicado está mal. Una búsqueda de rollback, revertir, retirar o release mala en `docs/PACKAGE.md`, `README.md` y `CLAUDE.md` sale vacía. En la práctica ya pasó y se resolvió publicando otra versión (v1.3.3 → v1.3.4); falta escribirlo.
- **Severidad.** BAJA (runbook de un procedimiento no crítico).
- **Arreglo.** Un párrafo con la regla: no se mueve el tag, se publica un parche encima y se avisa a los consumidores.

### D-11 · `CLAUDE.md` no lista todo lo que corre el CI

- **Qué pasa.** La lista «Todo corre en CI … y a mano» (`CLAUDE.md:74-99`) no incluye `tools/test_publicar_cifras.sh` ni `tools/test_parsers_comentarios.sh`, y el CI corre las dos (`.github/workflows/huella.yml:57`, `:118`).
- **Severidad.** BAJA.

---

## Verificaciones en positivo

- **El CI cubre lo importante y comprueba que sus propias pruebas no ensucian el árbol** (`.github/workflows/huella.yml:59-62`, `:120-127`, `:164-171`, `:179-182`). Cada guardián tiene una batería de sabotaje que demuestra que muerde.
- **La publicación está escrita paso a paso,** con la comprobación antes del push y el porqué de cada orden (`docs/PACKAGE.md:195-242`).
- **`dist/` no se versiona, y el CI lo comprueba** (`.github/workflows/huella.yml:164-171`; `tools/guard_paquete.py`).
- **El orden de lectura y las reglas de la nave están escritos** (`CLAUDE.md`). Las decisiones se documentan donde viven, con fecha y motivo. No hay ADRs formales, pero no faltan decisiones sin escribir.
- **El CI de `main` está en verde en el commit auditado** (`gh run list --branch main`).
