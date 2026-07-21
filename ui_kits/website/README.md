# AGLAYA · Website UI Kit

Hi-fi recreation of the **AGLAYA.biz** marketing home, built from this design system's canonical tokens and brand rules. Every color, token, spacing value, and copy string comes from `colors_and_type.css` + the voice/visual rules in the root `README.md` — the site consumes these tokens, not the other way around.

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
- `Services`, `Proof`, `ROI Audit`, and `Contact` pages are NOT built — the kit covers the home-page sections only. Open an issue if more are needed.
- Custom cursor is not reproduced (the live site swaps the OS cursor for a `mix-blend-mode: difference` ring). Intentional — it's distracting inside a component kit.
- Reveal `IntersectionObserver` is simplified to an autoplay CSS fade-up.
