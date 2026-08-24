# AGLAYA Design System

> **AGLAYA — The Uncomfortable AI·gency.** AI systems, automation and sovereign infrastructure for high-performance teams. Black brutalist aesthetic, high-contrast, zero decoration.

> **This folder is the CANONICAL, SOVEREIGN source of the AGLAYA brand identity** — design tokens, typography, voice, and logos. `aglaya.biz` and every other AGLAYA-branded surface **consume from here, not the other way around.** When a token, rule, or asset changes, it changes *here first*; downstream surfaces follow. Nothing upstream of this folder is authoritative.

`AGLAYA` is always written in full caps. The tagline _"The Uncomfortable AI·gency"_ — where `AI` sits inside `AGENCY` as a deliberate typographic collision — signals the core thesis: AGLAYA replaces agency labor with owned AI systems.

Clients are **founders and ops leads at high-performance companies** — not early-stage startups. AGLAYA qualifies them out on purpose (see `AntiClient` below).

---

## Sources

| Source | Location | Notes |
| ------ | -------- | ----- |
| **Design tokens (canonical)** | `colors_and_type.css` | the single source of truth — everything else follows |
| Historical origin | Astro + Tailwind v4, GitHub `ibaifernandez/aglaya.biz` | where the tokens were *first authored*; the site now **consumes** this package, it no longer defines the brand |
| Logos (canonical) | `assets/` (SVG canonical + PNG derivatives) | white / black / brand-red variants |
| Fonts | `fonts/` (Outfit, Inter, Space Mono) | all local, no CDN |

The tokens were first authored inside the live Astro codebase, but that codebase is **no longer authoritative**: this folder is now the canonical, sovereign definition of the brand, and `aglaya.biz` consumes it. This package depends on nothing upstream.

---

## Index

Root files:
- **`README.md`** — this document
- **`colors_and_type.css`** — all design tokens as CSS custom properties + semantic classes
- **`SKILL.md`** — Agent Skill entry point
- **`CLAUDE.md`** — repo instructions: reading order, hard rules, and the fleet section
- **`LICENSE`** — terms for AGLAYA's own material: all rights reserved. It does not cover the fonts, which are third-party under OFL 1.1 and keep their own terms

Folders:
- **`assets/`** — logos (white / black / brand-red), favicons (SVG), PNG fallbacks
- **`fonts/`** — local font files (Outfit variable + statics, Inter 100–900 + italics, Space Mono) — no CDN. Third-party, redistributed under SIL Open Font License 1.1; each family ships its licence beside it (`fonts/README.md`)
- **`preview/`** — design-system specimen cards (colors, type, spacing, components, brand). They read their values from `colors_and_type.css` at paint time, so a specimen cannot show a value the canon no longer holds
- **`products/`** — per-product identity: `products.json` (the roster) plus glyphs and lockups
- **`components/`** — `components.json`, the component specs served by `get_component`
- **`ui_kits/website/`** — full AGLAYA.biz homepage recreation. It imports `colors_and_type.css`; its own `:root` is aliases only, no values
- **`aglaya-ds-mcp/`** — the `aglaya-ds` MCP server (read-only) and its tests
- **`tools/`** — the guards that keep this repo honest, each with a sabotage battery, plus the mutation test that separates consuming from copying
- **`docs/`** — `CONTRACT.md`, the local brand contract, and `PACKAGE.md`, how other repos depend on it
- **`package.json`** — the manifest for `@aglaya/design-tokens`; `scripts/` derives the JSON/JS token forms at install time and `bin/` ships the "how far behind are you" command. `dist/` is generated, never committed

Counts are deliberately absent: `ls` knows, and a number typed here is wrong the
first time someone adds a file. This list said "22 specimen cards" while there
were 23.

---

## Content Fundamentals

> Los títulos de esta sección están en inglés a propósito y **no se traducen**:
> `aglaya-ds-mcp/brand.py` los busca por texto exacto (`_section`) para servir el
> canon por el MCP. El título es interfaz; el contenido es el canon. Traducir un
> título dejaría a la flota entera sin esa regla, en silencio.

### Voice

Breve, conciso, accionable, declarativo, técnico y preciso.

A AGLAYA le importa más **decir correctamente qué ocurre** que caer bien a los receptores de su comunicación.

«La Agencia Incómoda» del sobrenombre de AGLAYA es literal: **AGLAYA no suaviza malas noticias ni adorna conclusiones.** Tampoco utiliza cautelas rituales para evitar pronunciarse o suavizar el choque cuando la evidencia sí invita a hacerlo.

Dicha incomodidad, no obstante, no consiste en ser agresivo. Consiste en **mantener el criterio incluso cuando agradar resulta lo más fácil e incluso comercialmente inteligente**.

### Evidence

> **Ser asertivo no es un tono. Es lo que se puede respaldar.**

La evidencia determina hasta dónde puede llegar la voz.

- Lo que AGLAYA prohíbe es **decirle al cliente lo que quiere oír**, no elogiarle. El elogio merecido se dice. Lo que nunca ocurre es que el cliente dicte el diagnóstico. Metáfora odontológica: «*Si hay que sacar el premolar 44, se saca el premolar 44; no se empasta el incisivo 41 porque es lo que ha pedido el paciente*».
- **Directo no es duro.** Es sin adornos, no ser duro con pura gratuidad.
- **Afirmar más de lo que respalda la evidencia no es convicción, es fanfarronería.** Es el mismo fallo que vender algo como invencible, apuntando en la dirección contraria.
- Cuando la evidencia permite una conclusión clara, se dice con claridad. Cuando no la permite, **la incertidumbre también se dice con claridad**.
- Una inferencia es una inferencia y se presenta como tal. La ausencia de un problema concreto no implica que «todo está bien». Un dato desconocido no se rellena con diarrea verbal.

> **AGLAYA sostiene la conclusión más clara que la evidencia le permite sostener: ni palabras de más para impresionar, ni de menos para agradar (o viceversa).**

### Pronouns

- **«Tú»** para dirigirse directamente al fundador, operador o responsable que debe comprender o decidir algo: *«Tú lo posees.»*
- **«Nosotros»** únicamente para acciones que realmente ejecuta AGLAYA: *«Lo construimos.»*
- Evitar fórmulas impersonales cuando oculten quién hace qué.
- Nunca usar como relleno: "Nuestro equipo…"; "Creemos que…"; "Nos apasiona…"; "Estamos encantados de…"; "Esperamos poder…".

### Casing

- **`AGLAYA`** siempre en mayúsculas.
- Titulares y antetítulos de display: **MAYÚSCULAS**.
- Cuerpo de texto: frase normal.
- Etiquetas monoespaciadas: **MAYÚSCULAS**, con espaciado amplio.
- Las mayúsculas son estructura visual, no una forma de gritar.

### Signature terms
Used consistently across the site; treat these as protected brand vocabulary:

**Regla de precisión** (canon, 24-ago-2026): no se fuerza el vocabulario de marca
cuando hacerlo hace del significado de algo uno más difícil de comprender o
digerir. Un *lead* puede llamarse lead cuando esa sea la entidad comercial
exacta. Una métrica puede llamarse métrica. Un proceso puede llamarse proceso si
no constituye realmente un protocolo. **La marca sirve a la verdad. La verdad no
se deforma para servir a la marca.**

Por eso `Signal` y `Protocol` ya no vetan esas palabras: abajo son preferencias,
no prohibiciones. Lo que sigue vetado es lo que el canon prohíbe expresamente.

| Term | Usage |
| --- | --- |
| **Sovereignty** / **Sovereign** | The thing AGLAYA sells. |
| **Systems** (not "solutions", not "tools") | The thing AGLAYA ships. Preferred over the vetoed words when what is being described really is a system. |
| **Architecture** / **Infrastructure** | What the system is made of. |
| **Operational truth** | What the audit surfaces. |
| **Signal** | Data that matters. Preferred over lead, metric or input — but per the precision rule, a lead may be called a lead when that is the exact commercial entity. |
| **Protocol** | Preferred over process or steps when the thing really is a protocol. A process that is not a protocol may be called a process. |
| **Zero-filter** | Qualifier on diagnostics: findings arrive unsoftened. It claims something about how AGLAYA reports — which AGLAYA controls — never about how a system behaves. That is why it survives the retirement of absolute promises and "Zero-leak" does not. |
| **Dispatch** | The newsletter. Never "newsletter". |

### Signature terms — castellano

El mismo vocabulario para el copy en castellano. **Un nombre se queda, una idea
se traduce:** una cabecera no es un concepto. Cada fila lleva su original inglés
entre paréntesis para que el par se vea; los vetos son las palabras que un
redactor español teclea sin pensar.

Dos filas van sin veto a propósito. En inglés `control` y `process` se pueden
vetar; en castellano «control de acceso» y «proceso de compra» son frases
inocentes y corrientes, y un guardián que grita de más lo desactiva el primero
que lo sufra — entonces no protege nada. Quedan sin veto hasta que el corrector
sepa vetar frases en vez de palabras sueltas.

| Término | Uso |
| --- | --- |
| **Autonomía / Autónomo** (Sovereignty) | Lo que AGLAYA vende. **La asimetría con la tabla inglesa es deliberada, no una errata**: en español «soberanía» parece aludir a política más que ninguna otra cosa. Cuando alguien puede hacer algo por su cuenta no es «soberano», es «autónomo». `Sovereignty` se queda en inglés; aquí no. Quien lo «arregle» estará deshaciendo una decisión de marca. |
| **sistemas** (Systems) | Lo que AGLAYA entrega. Nunca "soluciones", nunca "solución", nunca "herramientas", nunca "herramienta". |
| **arquitectura / infraestructura** (Architecture / Infrastructure) | De qué está hecho el sistema. |
| **verdad operativa** (Operational truth) | Lo que la auditoría saca a la superficie. |
| **señal** (Signal) | El dato que importa. Preferido frente a lead o métrica — pero por la regla de precisión, un lead puede llamarse lead cuando esa sea la entidad comercial exacta, y una métrica puede llamarse métrica. |
| **protocolo** (Protocol) | Preferido cuando la cosa es de verdad un protocolo. Un proceso que no lo sea puede llamarse proceso. |
| **sin filtros** (Zero-filter) | Calificador sobre cómo AGLAYA informa: los hallazgos llegan sin suavizar. Afirma algo que AGLAYA controla —su propio reporte—, nunca cómo se comporta un sistema. Por eso sobrevive al retiro de las promesas absolutas y "Zero-leak" no. El rótulo Zero-Filter Diagnostics no se traduce: es un nombre, no una idea. |
| **Dispatch** | El boletín. No se traduce, y ese es justo el motivo: traducirlo lo convierte en la palabra vetada. Nunca "boletín", nunca "boletines". |

### Forbidden patterns

Las frases van **entre comillas dobles rectas** porque `brand.py` (`_forbidden_phrases`)
solo persigue lo entrecomillado así. Una prohibición escrita sin comillas se lee
aquí y **no la persigue `check_voice`**: se vería como regla y no lo sería.

- "We believe…" / "We're passionate about…" / "Our mission is…" / "Creemos que…" / "Nos apasiona…" / "Nuestra misión es…"
- "Estamos encantados…" / "Esperamos poder…"
- "Solutions" / "Soluciones" cuando solo sustituye vagamente a sistemas
- "Synergy" / "Sinergias"
- "partner with you" / "trusted partner" / "Journey" / "Transform your business" / "Transforma tu negocio" — se veta **la frase, no la palabra**: un socio real puede llamarse partner, y por la regla de precisión la marca no prevalece sobre el término exacto. Lo que se persigue es el cliché, no el sustantivo.
- "Innovador" / "Innovative" / "Revolucionario" / "Revolutionary" / "World-class" / "Best-in-class", o equivalentes sin prueba
- Exclamation marks — signos de exclamación en copy de producto
- Emoji in product copy (the codebase contains zero emoji)
- Rhetorical questions used for sales warmth — preguntas retóricas utilizadas únicamente para fabricar cercanía comercial
- Superlativos sin evidencia
- Agresividad utilizada como sustituto de criterio
- "Zero-leak", y cualquier promesa absoluta de que un sistema no fallará. **El software gotea —y el software con IA dentro gotea más—.** AGLAYA no promete invulnerabilidad, ausencia total de errores ni comportamiento perfecto cuando no puede demostrarlo. En lugar de una promesa absoluta se nombra la propiedad concreta que sí puede acreditarse: datos almacenados localmente; cero solicitudes externas; fuentes servidas localmente; dependencias versionadas; revisión humana obligatoria; evidencia trazable; comportamiento observado bajo unas condiciones determinadas. Cuanto más específica sea la afirmación, menos necesita parecer impresionante.

### What this voice does not cover

These rules govern **tone and brand vocabulary**. They do not govern commercial or
legal argument, and `check_voice` does not look at it: a text can come back clean
here and still be unpublishable.

The language rules that carry legal risk — how compliance may be claimed, whether a
fine may be used as a selling argument, the exact wording a consent checkbox is
allowed to use — are not brand rules and do not live in this repo. They live in the
captain's commercial material (repo `aglaya-orchestrator`) and are asked for through
the `aglaya-atlas` MCP, `verdad_comercial`.

They are **named here, never copied**. A legal rule copied into this repo would go
stale the day the contract moves, and nobody would find out — while it kept reading
like canon. Passing the brand corrector is not permission to publish.

### Sample copy

> **Hero.** _"The agency is dead. Long live the system."_
> _"Most teams don't need an agency. They need their own infrastructure. We build it. You own it. The system keeps running when we're not in the room."_

> **Problem card.** _"Stop building your empire on rented soil. When you hire a traditional agency, you are merely financing their portfolio."_

> **Anti-Client.** _"If you are looking for a partner to validate your current inefficiencies, find a traditional agency. If you need to build a sovereign engine, let's talk."_

> **Form state.** `SYNCING...` → `SYNCED` / `DATA_SYNCHRONIZED` / `ERROR_DURING_TRANSMISSION. REATTEMPT_REQUIRED.`

> **Footer.** _"Sovereign systems. Zero platform dependency theatre."_

Monospace labels behave as terminal output — `REF_ID:`, `LOGIC_NODE_001`, `EXCLUSION_PRINCIPLE_01`, `PLATFORM_FEES: 0.00`, `SYSTEM_INTEGRITY_OK`. Use them as structural chrome, not decoration.

---

## Visual Foundations

### Palette
Pure black is the canvas — `--color-bg`. Not near-black. **Black.** Card surfaces step up in ~4-value increments (`--color-surface`, `--color-surface-2`, `--color-surface-3`) to create depth without ever introducing grey warmth. The only saturated color is **AGLAYA Red** (`--color-brand`) — used surgically for the logo accent, brand type spans, primary CTAs, focus rings, and the second line of two-line headlines. **Corporate Green** (`--color-corporate-green`) is reserved for monospace eyebrows, code tags, and "applied logic" annotations — it never appears as a fill or button.

> The values are not written in this file, on purpose. They live in
> `colors_and_type.css` and answer to `get_token` / `list_tokens("color")`.
> This section used to spell out the black, the three surface steps, the red
> and the green; the day any of them moves, a README that names them is
> quietly wrong while looking like the canon. Ask for them.

**This palette governs the master brand** (`aglaya.biz`, agency materials, social). Product surfaces add exactly one first-class **product accent** each (KANBAN DESK cobalt, CRM violet, OUTREACH teal, ConsentFlow carmín, LEGAL REG TECH gold, ORCHESTRATOR steel, plus the DESIGN SYSTEM house itself in corporate green) — the single source is [`products/products.json`](products/products.json), served live by the MCP (`get_accent`, `list_products`). On its own product surface the accent is unrestricted — allowed on CTAs, no proportion cap — per the product tier of the non-negotiables (`get_nonnegotiables(scope="product")`). It never leaks onto the master, and the master never adopts a product accent: outside a product surface, the three colors above are still the whole palette.

### Typography
- **Display: Outfit Black (900).** Always uppercase, tracking tighter than normal (`-0.02em` to `-0.04em`), leading `~0.94–1.1`. Headlines routinely hit `9rem+` at large viewports.
- **Body: Inter 400–500.** Sentence case, generous leading (`1.6`), often set at `--color-muted` (45% white) against pure black — the contrast is intentionally softened on long-form to force scanability to the display type.
- **Mono: Space Mono 400/700.** UPPERCASE, extreme tracking (`0.3em–0.5em`), used for eyebrows, codetags, annotations, and terminal-style status strings.

Headlines frequently split across lines with the **second line colored brand red** (`heading2Class="text-brand"` in `SectionHeader`). This is the signature headline move.

### Backgrounds
No illustrations. No photography in chrome. No gradients-as-decoration. What you get instead:
- **Scanlines** — `linear-gradient` striped overlays at `50%` stops, `2–4px` bands, opacity `0.02–0.07`, applied to hero and card hover states.
- **Grid lines** — `60×60px` brand-red grid at `3%` opacity (`.bg-grid`).
- **Reactive aura** — a 900px radial gradient of the brand red at 10% (`--aura-brand`, derived from `--color-brand`) follows the mouse on `body::before` (desktop hover-capable only).
- **Blurred orbs** — single `500×500px` brand-red blob at `blur(120px)`, `5%` opacity, one per hero section max. Used sparingly.
- **Noise** — SVG `fractalNoise` turbulence at `1.5%` opacity, fixed to viewport.
- **Marquee** — slowly-crawling UPPERCASE display text at `20%` white, rotated `-1deg`, used as a rhythm break between sections.

### Animation
- **Easing: `cubic-bezier(0.16, 1, 0.3, 1)`** (the "Apple" out-expo). Used on every hover, reveal, and transition. Never `ease`, never `linear` except for marquees.
- **Durations:** `150ms` (micro), `300ms` (default), `500–700ms` (section reveals / card hovers).
- **Reveals:** `fade-up` (30px translate) and `fade-in` triggered by `IntersectionObserver` on `[data-animate]` elements. Staggered with `100–800ms` delays.
- **Hover on cards:** border `white/5 → brand/30–40`, accent line grows from `12px` to full-width `brand/20`, background scanline opacity increases.
- **Press states:** buttons `scale(0.95–0.98)` + slight `translateY(-1px)` on hover.
- **No bounces. No spring. No scale-up pops.** The motion language is controlled, industrial, out-easing.

### Borders & radii
**All radii are zero.** Literally — `global.css` ships `border-radius: 0 !important` on `*::before, *::after`. The only exceptions in the entire product are the custom cursor dot and the tiny flag pips in the language switcher. Cards are rectangles. Buttons are rectangles. Inputs are rectangles.

Border colors:
- Default: `rgba(255,255,255,0.05–0.08)` — whisper-thin separators.
- Hover: the brand red washed to 30–40% — `color-mix(in srgb, var(--color-brand) 40%, transparent)`, never a hand-written rgba.
- Accent rule: `2px` solid `brand` on blockquotes, `1px` everywhere else.

### Shadows
Essentially absent. The one exception is the primary CTA glow on hover — the `--glow-brand` token, which derives its colour from `--color-brand` instead of repeating it. Depth is created by surface stepping, never by shadow.

### Cards
Flat rectangles:
```
background: var(--color-surface-2)   /* or --color-surface / --color-bg-deep */
border: 1px solid rgba(255,255,255,0.05)
padding: 2.5rem (p-10)
no radius, no shadow
```
Hover flips border to brand and grows an accent line along the bottom.

### Layout
- **Max content width:** `max-w-7xl` (80rem / 1280px), horizontally centered.
- **Side gutters:** `px-6` mobile → `px-10` tablet → `px-20` desktop.
- **Section vertical rhythm:** `py-20` to `py-24`, separated by `border-t border-white/5` (never a hard rule).
- **Grid:** 12-col via Tailwind, but layouts favor explicit flex columns. 3-up on desktop for principle/case grids.
- **Fixed elements:** site header (fixed, `z-50`, `backdrop-blur-xl`), custom cursor (fixed, `z-10000`, `mix-blend-mode: difference`), cookie banner, skip link.

### Transparency & blur
- Glass chrome only on the fixed header: `bg-black/80 backdrop-blur-xl`.
- Soft glass utility `.glass` / `.glass-strong` exists but used sparingly.
- Blur as "aura" on background orbs — never as a foreground element.

### Imagery
Client logos render on `bg-[#eaeaea]/10` panels at `h-24` to `h-32`, `object-contain`. The live site has no lifestyle or stock photography. All product screenshots are captured and placed as dark flat panels. Treat imagery as **annotated technical evidence**, not atmosphere.

### Focus & accessibility
- Focus ring: `outline: 2px solid var(--color-brand); outline-offset: 3px`.
- Skip link pinned to top-left, background brand red on focus.
- `prefers-reduced-motion` is honored — marquee stops, reveals collapse to instant.

### Cursor
The site replaces the OS cursor with a 20px hollow ring + 4px white dot at `mix-blend-mode: difference`, lerped at `0.2`. On interactive elements it scales to `3×` and the dot shrinks. This is a signature interaction — the only rounded thing in the entire product.

---

## Iconography

- **No icon font.** No Lucide, no Heroicons, no FontAwesome. Icons are bespoke inline SVGs — in the live codebase they live in `src/components/icons/` (Languages, Mail, MessageCircle, MessageSquare, Send, User) or inlined directly into components (X, arrows, WhatsApp mark, hamburger). That `src/` tree is the external Astro repo, not part of this package.
- **Stroke icons.** Pure strokes, `stroke-width: 2–4`, `stroke-linecap: round`, `stroke-linejoin: round`. `var(--color-brand)` for attention, `currentColor` otherwise.
- **Fill icons.** Only the WhatsApp glyph.
- **Decorative squares.** `w-1 h-1` / `w-1.5 h-1.5` / `w-2 h-2` solid squares in `brand/40` are used as bullet points, list markers, and pulse indicators. This is the closest AGLAYA gets to a decorative element.
- **Country flags** (SVG) used only in the language switcher, clipped to a round chip.
- **No emoji anywhere.** Zero. Don't add them.
- **No unicode symbol icons** (no `→` dingbats, no `✓`, no `⚡`). Arrows inside buttons are inline SVG strokes. The exception: a literal `→` character is used inside CTA labels like `"Request Proposal →"` as part of the text string — keep it there, don't replace with an SVG.

When you need an icon AGLAYA doesn't already have, draw a minimal line-stroke version in the same weight/style. Do not import Lucide or Heroicons — the whole point of the aesthetic is that nothing is store-bought.

---

## Product Identity

Model: **MONOLITHIC** — AGLAYA leads, the product describes. `aglaya.biz` is the master house, never a sub-brand; the products below are surfaces that consume from this repo. The single source of truth for the roster is [`products/products.json`](products/products.json), served live by the MCP (`list_products`, `get_product`, `get_accent`, `get_glyph`, `get_lockup`).

**Roster (7) and accents.** Six products plus the DESIGN SYSTEM house itself (`is_house`), each carrying exactly one accent:

| Product | Accent | Mark |
| ------- | ------ | ---- |
| KANBAN DESK | Cobalt — `--product-kanban-desk-accent` | three bars (columns) |
| CRM | Violet — `--product-crm-accent` | line + three nodes |
| OUTREACH | Teal — `--product-outreach-accent` | two chevrons |
| ConsentFlow | Carmín — `--product-consent-flow-accent` (+ green `--product-consent-flow-accent-2`) | Mónica Montúfar's seal, AGLAYA type, outlined — colour isotipo (set exception) |
| LEGAL REG TECH | Gold — `--product-legal-reg-tech-accent` | framed check (audit seal) |
| ORCHESTRATOR | Steel — `--product-orchestrator-accent` | hub + four satellites |
| DESIGN SYSTEM | Corporate green — `--product-design-system-accent` | 2×2 token grid — the house itself (`is_house`) |

**Two-level colour doctrine.** The 3-colour master palette (black / red / green) is rigid on the master brand. A **product surface** adds its accent as a first-class colour — allowed on CTAs, no proportion cap — per `get_nonnegotiables(scope="product")`. The accent never leaks onto the master; the master never adopts a product accent.

**Taxonomy.** Each product ships a **glyph** on a 96×96 grid in three variants — `white`, `accent` (accent on transparent), `fill` (accent square, mark knocked out in black) — and two **lockups**: `lockup` (horizontal) and `stacked`. Lockups reference Outfit / Space Mono by name; the repo ships those fonts.

**ConsentFlow.** Mónica Montúfar's concept for the `consent-ledger-wp` plugin — a green seal holding a "C" with a carmín check badge — rebuilt with AGLAYA type (wordmark in Inter, eyebrow in Space Mono) and delivered as **outlines**: zero font dependency, renders identically on any machine. It is the set's **exception**: instead of the three mono glyph variants it ships a single **colour isotipo**. The C is always white — the green seal encapsulates it and gives it its form, so it holds on any background; there is no light-surface variant and none is needed. Its CSS classes are namespaced per file (`cfg-`, `cfl-`, `cfs-`) so the assets stay correct when several are inlined into one page.

PULSE was removed from the set (telephone outbound, out of scope) — deleted, not archived, per the brand rule *eliminar > legacy*.

---

## Fonts

All three brand families are loaded from local files in `fonts/` — zero external font requests.

- **Outfit** (display) — variable font (`Outfit-Variable.ttf`, 100–900) plus 8 static weights (ExtraLight 200 → Black 900).
- **Inter** (body) — 18 OTF files covering 100 → 900 with italics (BETA files for the three lightest weights).
- **Space Mono** (labels) — Regular + Bold with italics.

Nothing is being substituted. The kit is fully offline-capable once these files ship alongside it.

---

## How to use this system

This design system is a **self-contained folder** you can drop anywhere. It has no dependencies beyond a browser.

### Browse the system
Open any file in `preview/` in a browser and you'll see the specimen card for that token (colors, type, spacing, components, brand). `ui_kits/website/index.html` is a full hi-fi recreation of the homepage built with the tokens — use it as the canonical reference for how everything composes.

### Use it in production code
```html
<!-- Drop-in stylesheet; loads fonts and exposes all tokens as CSS variables -->
<link rel="stylesheet" href="./colors_and_type.css">

<body style="background: var(--color-bg); color: var(--fg-1);">
  <h1 class="t-display-lg">Sovereign <span style="color: var(--color-brand);">systems.</span></h1>
</body>
```

All tokens are CSS custom properties (`--color-brand`, `--text-display-xl`, `--space-8`, `--ease-out`, etc.). Import `colors_and_type.css` and they're available globally.

### Use it with an AI coding tool (Claude Code, Cursor, Copilot)
Unzip the folder into your project. Any agent can read `SKILL.md` + `README.md` and immediately start generating on-brand code. Example prompt:

> "Using the design system in `./aglaya-design-system/`, build a landing page for our new ROI audit product."

The agent reads the tokens, copies assets, follows the voice rules, and ships pixel-consistent with the rest of the brand.

### Depend on it from another repo (package)
The tokens ship as a versioned package, `@aglaya/design-tokens`, pinned to a tag over `git+https` — the only shape that survives a foreign CI, which clones the consumer's repo and not this one.

```bash
npm install "git+https://github.com/ibaifernandez/aglaya-design-system.git#v1.1.0"
```

```css
@import "@aglaya/design-tokens/tokens.css";
```

The package ships the canonical `colors_and_type.css` itself — not an adapted copy — plus the fonts it loads and JSON/JS token forms derived at install time. One command tells a consumer how far behind it is:

```bash
npx aglaya-tokens-version
```

Semver policy, the name-collision rule (consumers rename; there is no alias map), and the mutation test that proves a consumer is depending rather than copying: [`docs/PACKAGE.md`](docs/PACKAGE.md).

### Query the brand live (MCP)
For projects that should read the brand **live** instead of copying it, this repo ships a sovereign MCP server in [`aglaya-ds-mcp/`](aglaya-ds-mcp/README.md). It exposes `get_token`, `list_tokens`, `get_voice_rules`, `check_voice`, `is_allowed_word`, `get_logo`, and `get_nonnegotiables` (master + `scope="product"`), plus **product identity** (`list_products`, `get_product`, `get_accent`, `get_glyph`, `get_lockup`, `get_product_voice`) and **component specs** (`list_components`, `get_component`) — each reading these canonical files live, so downstream surfaces (`aglaya.biz` included) consume the brand instead of duplicating it. The MCP is an optional, separable layer; the design-system folder stays runtime-free without it.

### Use it in Figma / other tools
- **Fonts:** install the `.otf` / `.ttf` files from `fonts/` into your OS font book.
- **Colors:** copy the hex values from `preview/colors-brand.html` and `colors-surface.html` into Figma Variables, Tailwind config, etc.
- **Logos:** drop the SVGs from `assets/` directly into Figma / Sketch / Illustrator.
- **Typography scale:** translate the `--text-*` tokens in `colors_and_type.css` into your tool's text styles.

### Extend it
If you build new components, drop them in `preview/components-*.html` and they become part of the system. The README's voice and visual rules are the contract — anything that follows them belongs.

---


