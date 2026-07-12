---
name: aglaya-design
description: Use this skill to generate well-branded interfaces and assets for AGLAYA, either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the `README.md` file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## File map

- `README.md` — full brand guide (content voice, visual foundations, iconography, forbidden patterns, sample copy)
- `colors_and_type.css` — all tokens as CSS custom properties + ready-to-use `t-*` semantic classes
- `assets/` — logos (white / black / color) + favicons (SVG + PNG)
- `preview/` — 19 design-system specimen cards (colors, type, spacing, components, brand)
- `ui_kits/website/` — hi-fi React recreation of the marketing site. Start here for any web work.

## Non-negotiables

- `AGLAYA` always UPPERCASE.
- Zero border-radius. Every corner is square.
- Black canvas (`#000`), red accent (`#e8003d`), green monospace (`#9fc243`). Nothing else.
- No emoji. No Lucide. No Heroicons. No gradients-as-decoration. No rounded corners except the custom cursor.
- Copy is terse and imperative. No "we believe", no "we're passionate about", no exclamation marks, no rhetorical questions.
- Display type is Outfit Black, UPPERCASE, tight tracking. Body is Inter. Mono is Space Mono with extreme `letter-spacing: 0.3em–0.5em`.
- Signature headline move: line 1 white, line 2 `color: var(--color-brand)`.
