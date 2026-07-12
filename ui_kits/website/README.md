# AGLAYA · Website UI Kit

Hi-fi recreation of the **AGLAYA.biz** marketing site. Sourced directly from the live Astro codebase (`src/components/`) — every color, token, spacing value, and copy string matches production.

## Files
- `index.html` — composes the home view (Header → Hero → Problem → Systems → AntiClient → Footer)
- `styles.css` — design tokens + utility classes (scoped to the kit)
- `Primitives.jsx` — `PrimaryButton`, `GhostButton`, `MonoLink`, `Eyebrow`, `SectionHeader`
- `Header.jsx` — fixed glass header with nav, lang, WhatsApp, Contact
- `Hero.jsx` — signature two-line red-accent headline + CTAs
- `Problem.jsx` — 6-card grid ("Agencies sell hours. / We sell sovereignty.")
- `SystemsGrid.jsx` — 5 architecture principles + rotated industrial marquee
- `AntiClient.jsx` — exclusion-principle grid with pulse integrity check
- `Footer.jsx` — Dispatch signup + primary channel list + legal strip
- `assets/` — brand logo + favicon (copied from `/assets`)

## Composition rules the kit enforces
- Zero border-radius anywhere (enforced globally in `styles.css`)
- Pure `#000` canvas — card surfaces step up to `#050505 / #0c0c0c`
- Brand red `#e8003d` used only on: logo accent, second-line headlines, primary CTAs, hover borders, focus outlines
- Corporate green `#9fc243` used only for mono eyebrows, codetags, "applied logic" labels
- All transitions use `cubic-bezier(0.16, 1, 0.3, 1)`
- Hover pattern: border `white/5 → brand/30–40` + rule grows `w-12 → w-full`
- Primary CTA has an offset `translate(4,4)` border-shadow that snaps home on hover

## Known gaps
- `Services`, `Proof`, `ROI Audit`, and `Contact` pages are NOT built — the kit covers the home-page sections only. Open an issue if more are needed.
- Custom cursor is not reproduced (the live site swaps the OS cursor for a `mix-blend-mode: difference` ring). Intentional — it's distracting inside a component kit.
- Reveal `IntersectionObserver` is simplified to an autoplay CSS fade-up.
