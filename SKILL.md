---
name: aglaya-design
description: Use this skill to generate well-branded interfaces and assets for AGLAYA, either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

**This folder is the canonical, sovereign source of the AGLAYA brand** — tokens, typography, voice, logos. `aglaya.biz` and every other AGLAYA-branded surface consume from here, never the reverse. Treat it as the single source of truth; do not derive brand values from any other codebase.

Read the `README.md` file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## File map

- `README.md` — full brand guide (content voice, visual foundations, iconography, forbidden patterns, sample copy)
- `colors_and_type.css` — all tokens as CSS custom properties + ready-to-use `t-*` semantic classes
- `assets/` — logos (white / black / color) + favicons (SVG + PNG)
- `products/` — product identity (monolithic model): 6 products, each with glyphs (white/accent/fill) + lockups, plus `products.json` (the roster's single source of truth). Served live by the MCP.
- `components/` — component specs (`components.json`: button/card/input/badge) served by the MCP.
- `preview/` — design-system specimen cards (colors, type, spacing, components, brand, product identity)
- `ui_kits/website/` — hi-fi React recreation of the marketing site. Start here for any web work.

## Non-negotiables

Reglas de la **marca madre AGLAYA** (aglaya.biz, materiales de agencia, redes). Rígidas: se aplican a toda superficie AGLAYA, salvo donde una superficie de **producto** declare una excepción explícita en `## Non-negotiables — producto`.

- `AGLAYA` always UPPERCASE.
- Zero border-radius. Every corner is square.
- Black canvas (`--color-bg`), red accent (`--color-brand`), green monospace (`--color-corporate-green`). Nothing else. Ask `get_token` for the values — a rule that carries its own hex stops being true the day the hex moves.
- No emoji. No Lucide. No Heroicons. No gradients-as-decoration. No rounded corners except the custom cursor.
- Copy is terse and imperative. No "we believe", no "we're passionate about", no exclamation marks, no rhetorical questions.
- Display type is Outfit Black, UPPERCASE, tight tracking. Body is Inter. Mono is Space Mono with extreme `letter-spacing: 0.3em–0.5em`.
- Signature headline move: line 1 white, line 2 `color: var(--color-brand)`.

## Non-negotiables — producto

Una **superficie de producto** (KANBAN DESK, CRM, OUTREACH, ConsentFlow, LEGAL REG TECH, ORCHESTRATOR, y la propia DESIGN SYSTEM — ver `products/products.json`) hereda TODOS los no-negociables de la marca madre, con una única excepción: su color de acento es de primera clase.

- Hereda todos los no-negociables de la marca madre **excepto la exclusividad de color** («Nothing else»).
- El **acento del producto** (definido en `products/products.json` y como token en `colors_and_type.css`) es color de primera clase: **libre en CTA, sin tope de proporción**.
- El rojo madre (`--color-brand`) no se reemplaza: coexiste con el acento en la superficie del producto. El acento identifica al producto; el rojo sigue siendo el rojo de la marca.
- Todo lo demás sigue vigente sin cambios: radius 0, sin emoji / Lucide / Heroicons, tipografía (Outfit Black / Inter / Space Mono), headline de dos líneas, voz seca e imperativa.
- La marca madre NO adopta acentos de producto: fuera de una superficie de producto, siguen los 3 colores y nada más.
