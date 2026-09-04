# AGLAYA · Website UI Kit

Hi-fi recreation of the **AGLAYA.biz** marketing home, built from this design system's canonical tokens and brand rules — the site consumes them, not the other way around.

`styles.css` **imports** `colors_and_type.css`; its own `:root` is a table of short aliases (`--brand: var(--color-brand)`, …) and holds no values. Every brand colour — the red, its dark and light steps, the corporate green, the surface ramp, the easing curve — resolves to a canonical token, and alpha variants are derived with `color-mix` instead of a hand-written rgba. `tools/guard_valores.py` fails CI if a brand value is written by hand anywhere in the repo, so this paragraph is checked, not promised.

**There is no longer a local ink scale, and that paragraph used to say there was.** The kit carried its own white-alpha ramp for hairline borders and secondary text — twenty distinct alpha values written by hand — and this file called it neutral chrome rather than brand, which is what made it look harmless.

It was not harmless. Twenty of those uses were **text that did not reach AA on black**, in the dark mode already in production; the worst, with nine uses, sat at 1.66:1. The composition that this system offers as «this is how it all goes together» was painting text nobody could read.

It is gone. Text now resolves to the three canonical registers (`--color-text`, `--color-muted`, `--color-faint`); hairlines and veils use `color-mix` over `--color-text` at the same alpha, so the ink follows the mode and the subtlety does not change. Nothing here holds a colour value any more.

`guard_valores.py` would **not** have caught any of it: pure white is exempt on purpose, or it would flag half the repo. That exemption is correct and stays — which is exactly why this paragraph has to be accurate instead of reassuring.

This file used to open by claiming every value came from the canon. It did not: the kit kept its own copy of the palette, and that copy had already drifted to a different light red and an off-ramp surface tone. A README that asserts consumption is worth exactly nothing — check the imports.

## Files
- `index.html` — composes the home view (Header → Hero → Problem → Systems → AntiClient → Footer)
- `styles.css` — design tokens + utility classes (scoped to the kit)
- `Primitives.jsx` — `PrimaryButton`, `GhostButton`, `MonoLink`, `Eyebrow`, `SectionHeader`
- `Header.jsx` — fixed glass header with nav, lang, WhatsApp, Contact
- `Hero.jsx` — signature two-line red-accent headline + CTAs
- `Problem.jsx` — card grid ("Agencies sell hours. / We sell sovereignty.")
- `SystemsGrid.jsx` — architecture principles + rotated industrial marquee
- `AntiClient.jsx` — exclusion-principle grid with pulse integrity check
- `Footer.jsx` — Dispatch signup + primary channel list + legal strip
- `assets/` — brand logo + favicon (copied from `/assets`)

## Composition rules the kit enforces

The **rules** live here. The **values** do not — they live in
`colors_and_type.css` and answer to `list_tokens()`. This file used to spell out
the canvas black, both surface steps, the brand red, the green and the easing
curve; the day any of them moves, a README that names them is quietly wrong
while claiming to be canonical.

- Zero border-radius anywhere (enforced globally in `styles.css`)
- Pure black canvas — card surfaces step up through the surface tokens, never a warm grey
- **Brand red only on:** logo accent, second-line headlines, primary CTAs, hover borders, focus outlines. Signal, never decoration
- **Corporate green only on:** mono eyebrows, codetags, "applied logic" labels. Never a fill, never a button
- One easing curve for every transition — no bounce, no spring
- Hover pattern: border steps from the faint rule to the brand wash + rule grows `w-12 → w-full`
- Primary CTA has an offset border-shadow that snaps home on hover

## Known gaps
- **The third architecture principle is named differently here than on the live site.** The site still carries the absolute-claim name this repo retired as a forbidden pattern; the kit carries `Integrity-First Architecture`, which says the same thing without promising a system cannot fail. Deliberate divergence, not drift: canon cannot ship a term it bans. The site is tracked to follow — this kit is the direction of travel, as always.
- `Services`, `Proof`, `ROI Audit`, and `Contact` pages are NOT built — the kit covers the home-page sections only. Open an issue if more are needed.
- Custom cursor is not reproduced (the live site swaps the OS cursor for a `mix-blend-mode: difference` ring). Intentional — it's distracting inside a component kit.
- Reveal `IntersectionObserver` is simplified to an autoplay CSS fade-up.
