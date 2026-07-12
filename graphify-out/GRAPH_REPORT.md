# Graph Report - aglaya-design-system  (2026-07-12)

## Corpus Check
- 10 files · ~11,072 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 95 nodes · 82 edges · 17 communities (10 shown, 7 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 11 edges (avg confidence: 0.68)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `aa238659`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Component Specimens
- Design System Guide
- Logo Variants
- Footer Component
- Systems Display
- Color Palette System
- Exclusions Section
- Problems Section
- Layout & Spacing
- White Mark
- Black Mark
- Red Mark
- Content Fundamentals
- How to use this system

## God Nodes (most connected - your core abstractions)
1. `Design Tokens CSS` - 21 edges
2. `Visual Foundations` - 13 edges
3. `AGLAYA Design System` - 8 edges
4. `Content Fundamentals` - 7 edges
5. `How to use this system` - 6 edges
6. `Website UI Kit Index` - 4 edges
7. `Logo Variants Specimen` - 3 edges
8. `AGLAYA Logotype – White` - 2 edges
9. `Sources` - 1 edges
10. `Index` - 1 edges

## Surprising Connections (you probably didn't know these)
- `Primary Logo Specimen` --displays--> `AGLAYA Logotype – White`  [INFERRED]
  preview/brand-logo-primary.html → assets/logotipo/svg/aglaya-logotipo-blanco.svg
- `Logo Variants Specimen` --displays--> `AGLAYA Logotype – White`  [INFERRED]
  preview/brand-logo-variants.html → assets/logotipo/svg/aglaya-logotipo-blanco.svg
- `Logo Variants Specimen` --displays--> `AGLAYA Logotype – Black`  [INFERRED]
  preview/brand-logo-variants.html → assets/logotipo/svg/aglaya-logotipo-negro.svg
- `Logo Variants Specimen` --displays--> `AGLAYA Logotype – Brand Red`  [INFERRED]
  preview/brand-logo-variants.html → assets/logotipo/svg/aglaya-logotipo-color.svg
- `Favicon Specimen Cards` --references--> `Design Tokens CSS`  [EXTRACTED]
  preview/brand-favicon.html → colors_and_type.css

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Design System Preview and Documentation Suite** — readme, preview_brand_favicon_html, preview_brand_iconography_html, preview_colors_brand_html, preview_components_badges_html, preview_components_buttons_html, preview_components_card_html, preview_spacing_borders_html [EXTRACTED 0.95]

## Communities (17 total, 7 thin omitted)

### Community 0 - "Component Specimens"
Cohesion: 0.10
Nodes (21): Design Tokens CSS, Favicon Specimen Cards, Iconography Specimen, Brand Colors Specimen, Semantic Colors Specimen, Surface Colors Specimen, Badges Component Specimen, Buttons Component Specimen (+13 more)

### Community 1 - "Design System Guide"
Cohesion: 0.50
Nodes (4): Website Kit Favicon, Website Kit Logo White, Website UI Kit Index, Website UI Kit Documentation

### Community 3 - "Logo Variants"
Cohesion: 0.40
Nodes (5): AGLAYA Logotype – White, AGLAYA Logotype – Brand Red, AGLAYA Logotype – Black, Primary Logo Specimen, Logo Variants Specimen

### Community 6 - "Color Palette System"
Cohesion: 0.15
Nodes (13): Animation, Backgrounds, Borders & radii, Cards, Cursor, Focus & accessibility, Imagery, Layout (+5 more)

### Community 9 - "Layout & Spacing"
Cohesion: 0.29
Nodes (6): AGLAYA Design System, Fonts, Iconography, Index, Sources, AGLAYA Design Skill Definition

### Community 15 - "Content Fundamentals"
Cohesion: 0.29
Nodes (7): Casing, Content Fundamentals, Forbidden patterns, Pronouns, Sample copy, Signature terms, Voice

### Community 16 - "How to use this system"
Cohesion: 0.33
Nodes (6): Browse the system, Extend it, How to use this system, Use it in Figma / other tools, Use it in production code, Use it with an AI coding tool (Claude Code, Cursor, Copilot)

## Knowledge Gaps
- **61 isolated node(s):** `Sources`, `Index`, `Voice`, `Pronouns`, `Casing` (+56 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AGLAYA Design System` connect `Layout & Spacing` to `How to use this system`, `Color Palette System`, `Content Fundamentals`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Why does `Visual Foundations` connect `Color Palette System` to `Layout & Spacing`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Why does `Design Tokens CSS` connect `Component Specimens` to `Design System Guide`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **What connects `Sources`, `Index`, `Voice` to the rest of the system?**
  _61 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Component Specimens` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._