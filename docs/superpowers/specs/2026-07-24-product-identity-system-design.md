# Spec — Sistema de Identidad de Producto AGLAYA

- **Fecha:** 2026-07-24
- **Repo:** aglaya-design-system (fuente canónica y soberana de la marca)
- **Estado:** aprobado en brainstorming, pendiente de ejecución
- **Cierre acordado:** ejecutar → revisión pormenorizada guiada con el usuario → informe para el orquestador

## 1. Problema

El repo es la fuente soberana de la identidad AGLAYA (tokens, tipografía, voz, logos) y el MCP `aglaya-ds` la sirve en vivo. Pero el MCP hoy solo conoce la **marca madre**: 8 tools nivel-casa (`get_token`, `list_tokens`, `get_voice_rules`, `check_voice`, `is_allowed_word`, `get_logo`, `get_nonnegotiables`). **Cero conciencia de producto.** Una nave que pregunte por su acento, glyph, lockup o voz no recibe nada.

Existe identidad de producto ya diseñada, pero dispersa y fuera del repo:
- `/Volumes/Chankete/AGLAYA/02-productos/productos/` — README + `glyphs/` (3 variantes: white/accent/fill, rejilla 96×96) + `lockups/` (horizontal + stacked) para KANBAN DESK, CRM, OUTREACH y PULSE.
- `/Users/AGLAYA/Desktop/Consent Flow/svg/` — 5 SVG de Mónica Montúfar para el producto CONSENT FLOW (plugin `consent-ledger-wp`).

Objetivo: **absorber, consolidar y sistematizar** esa identidad dentro del repo (no importar SVG sueltos) y exponerla por el MCP, dentro del modelo **MONOLITHIC** ya fijado («AGLAYA encabeza, el producto describe»).

## 2. Decisiones (brainstorming)

| # | Fork | Ruling |
|---|---|---|
| A | Colores de producto vs regla «solo 3 colores / nothing else» | **Dos niveles.** Madre AGLAYA sigue rígida (3 colores, nada más). Para **producto**, su acento es de primera clase: **puede ir en CTA, sin tope del 5%.** La vieja regla «acentos <5%, nunca en CTA» se **elimina** para productos. |
| B | Quién dibuja los glyphs | Lo único humano/sagrado es la marca AGLAYA original (logotipo + isotipo) y CONSENT FLOW (Mónica). Todo lo demás lo dibuja Claude — incluidos los 2 productos nuevos y el redibujo coherente de los existentes. |
| Voz | ¿Voz propia por producto? | **No.** Una sola voz AGLAYA para todos. El MCP devuelve la voz madre para cualquier producto. |
| C | Forma sistematizada | Dir `products/` en el repo + manifiesto `products.json` + tokens de acento reales en `colors_and_type.css`; el MCP lee en vivo (espejo de `brand.py`). |
| D | Specs de componente | **En scope**, pero como iteración limpia aparte (no colapsar con identidad de producto). Ambas cosas listas esta sesión. |
| E | Dónde vive la identidad | **Dentro del repo.** `/Volumes/Chankete` es disco externo montable; el MCP no puede depender de él. Consecuencia: el volumen externo deja de ser autoritativo (como le pasó a aglaya.biz con los tokens). |
| Legal | ¿1 o 2 productos? | **1 producto, 2 funciones** (escáner 21.719 + auditoría 21.719). Roster final = 6. |

## 3. Roster final (6 productos)

| Producto | Acento | Origen / acción |
|---|---|---|
| KANBAN DESK | Cobalt `#4a8fd6` — `oklch(0.72 0.13 250)` | existe · redibujo coherente |
| CRM | Violet `#b073d8` — `oklch(0.72 0.13 300)` | existe · redibujo coherente |
| OUTREACH | Teal `#4eb2ac` — `oklch(0.74 0.10 190)` | existe · redibujo coherente |
| CONSENT FLOW | Carmín `#ae214d` (secundario verde `#5b964d`) | **Mónica · sagrado.** Se envuelve en el sistema, **no se redibuja**. Arte en viewBox 595×234 (formato lockup), sin rejilla 96×96 ni 3 variantes — se mapea a los huecos que pueda llenar; los que falten quedan marcados como ausentes, no inventados. |
| LEGAL REG-TECH | **Propuesto** Gold `oklch(0.78 0.13 80)` (hueco de hue que libera PULSE) | nuevo · Claude dibuja (glyph 3 variantes + lockups) |
| ORQUESTADOR | **Propuesto** Steel desaturado `oklch(0.70 0.04 260)` — el director no compite en croma con lo que enruta | nuevo · Claude dibuja |

**PULSE:** eliminado (regla de marca: eliminar > legacy). Se borran sus 5 archivos (`pulse-glyph-*.svg`, `aglaya-pulse-*.svg` al absorber) + su acento amber; no se archiva. Queda fuera del set (outbound telefónico, no aplica).

Acentos de LEGAL REG-TECH y ORQUESTADOR: propuestos arriba; se confirman visualmente en la revisión pormenorizada.

## 4. Doctrina de dos niveles (no-negociables)

- **Madre AGLAYA** (aglaya.biz, materiales de agencia, redes): rígida como hoy. Canvas negro `#000`, rojo `#e8003d`, verde mono `#9fc243`. Nada más.
- **Superficie de producto**: hereda todo lo anterior **salvo** que el acento del producto es color de primera clase — libre en CTA, sin tope de proporción. El rojo madre y el resto de no-negociables (radius 0, sin emoji/Lucide/Heroicons, tipografía, headline de dos líneas) siguen vigentes.
- `SKILL.md` codifica ambos niveles. `get_nonnegotiables` pasa a distinguir madre vs producto (p. ej. parámetro opcional de scope) leyendo `SKILL.md` en vivo — sin parafrasear.

## 5. Forma sistematizada (dentro del repo)

```
products/
  products.json              ← manifiesto único: id, nombre display, slug, acento (token + hex + oklch),
                                funciones, autor, sagrado(bool), archivos disponibles, notas
  kanban-desk/
    glyphs/   *-white.svg *-accent.svg *-fill.svg   (96×96)
    lockups/  *-lockup.svg (horizontal) *-stacked.svg
  crm/            …
  outreach/       …
  consent-flow/   (arte de Mónica tal cual; variantes ausentes marcadas en el manifiesto)
  legal-reg-tech/ (nuevo)
  orquestador/    (nuevo)
colors_and_type.css          ← + tokens de acento reales: --product-<slug>-accent
```

- Los acentos viven como **tokens reales** en `colors_and_type.css`, no como hex a mano (respeta `guard_huella` y el contrato «consume, no copies»).
- `products.json` es la única fuente de verdad del roster; el MCP y los docs lo leen, no lo duplican.

## 6. Superficie MCP nueva (espejo de `brand.py`, lectura en vivo)

- `list_products()` → roster con acento y funciones.
- `get_product(id)` → ficha completa (nombre, acento, funciones, archivos, sagrado).
- `get_accent(id)` → token + valor del acento.
- `get_glyph(id, variant)` → ruta al SVG (white/accent/fill); error claro si el producto no tiene esa variante (caso CONSENT FLOW).
- `get_lockup(id, layout)` → ruta al SVG (horizontal/stacked).
- Voz de producto → devuelve la voz AGLAYA única (decisión «una sola voz»); documentado para que la nave sepa que es intencional, no un hueco.

Toda ruta se resuelve viva contra `products/`; ningún valor de marca se copia al código del server.

## 7. Iteraciones limpias (esta sesión, sin colapsar objetivos)

1. **Doctrina** — reescribir no-negociables a dos niveles en `SKILL.md`; ajustar `get_nonnegotiables`.
2. **Absorber + sistematizar** — crear `products/` + `products.json`; mover/regenerar glyphs y lockups de KANBAN/CRM/OUTREACH; envolver CONSENT FLOW; **dibujar** LEGAL REG-TECH y ORQUESTADOR; **purgar PULSE**; añadir tokens de acento a `colors_and_type.css`.
3. **Tools MCP de producto** — implementar en `brand.py` + `server.py`; extender `selftest.py`.
4. **Componentes** — extraer specs de `/preview` (botón, tarjeta, input, badge) a datos consultables; tools `get_component` / `list_components`.
5. **Limpieza** — subir la regla huérfana reformulada al DS; reconciliar «nothing else» en README + SKILL; matar PULSE en todo doc; verificar `guard_huella` + batería.
6. **Docs + grafo** — actualizar README, CONTRACT (si aplica), README del MCP; regenerar grafo local (`graphify-out/` esenciales) y enganche al global; avisar al orquestador de lo que su ficha ya no refleja.

## 8. Cierre

- **Revisión pormenorizada guiada**: al terminar, recorrer con el usuario punto por punto lo hecho (roster, glyphs nuevos, doctrina, MCP, componentes, limpieza, docs/grafo).
- **Informe para el orquestador**: tras la revisión, redactar el parte para el capitán (`aglaya-orchestrator`) — qué cambió en esta nave, qué contradice su ficha, qué contratos inter-nave toca (identidad de producto es superficie nueva que la flota puede consumir).

## 9. Fuera de scope

- Rediseñar CONSENT FLOW o la marca AGLAYA madre (sagrados).
- Reintroducir PULSE.
- Voz por producto (decidido: una sola voz).
- Cablear cualquier dummy de `aglaya-web` a esta marca.

## 10. Riesgos / vigilancias

- **CONSENT FLOW no encaja en el molde** (2 colores, formato lockup, sin 3 variantes). Riesgo: forzarlo. Mitigación: envolver, marcar ausencias en el manifiesto, no inventar.
- **`get_nonnegotiables` de dos niveles** puede romper consumidores que asumen respuesta única. Mitigación: scope opcional con default = comportamiento actual (madre).
- **Acentos como tokens** deben pasar `guard_huella` (hex de marca fuera de backticks). Mitigación: definirlos en `colors_and_type.css` (sitio sancionado), nunca sueltos en docs vigilados.
- **Grafo desincronizado**: hay un diff de `graphify-out/` previo; regenerar al final, versionar solo esenciales.
