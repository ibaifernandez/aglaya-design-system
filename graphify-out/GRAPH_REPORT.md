# Graph Report - aglaya-design-system  (2026-07-24)

## Corpus Check
- 24 files · ~25,626 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 256 nodes · 278 edges · 53 communities (16 shown, 37 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 12 edges (avg confidence: 0.69)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cd1f736a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Brand Voice Rules
- Sovereign Brand Server
- Design System Assets
- Token Management API
- MCP Server Testing
- Logo Specimen Cards
- Footer Component
- Systems Showcase
- Brand Exclusions
- Website Kit
- Problem Showcase
- White Mark Variant
- Black Mark Variant
- Red Mark Variant
- MCP Server Package
- Favicon Specimens
- Iconography
- Brand Colors
- Semantic Colors
- Surface Colors
- Badges
- Buttons
- Card
- Comparison Grid
- Input Fields
- Borders and Spacing
- Radii and Shadows
- Spacing Scale
- Body Typography
- Display Typography
- Signature Headline
- Inter Font Weights
- Monospace Typography
- Outfit Font Weights
- Space Mono Weights
- CONTRACT — Estilo de marca AGLAYA
- Visual Foundations
- guard_huella.py
- test_guard_huella.sh
- Spec — Sistema de Identidad de Producto AGLAYA
- AGLAYA.biz Website
- Logos and Favicons
- _read
- Font Files
- Inter Typeface (Body)
- Outfit Typeface (Display)
- Design System Specimen Cards
- Space Mono Typeface (Monospace Labels)
- Website UI Kit (Hi-fi Recreation)
- AGLAYA Design System — Sovereign Brand MCP

## God Nodes (most connected - your core abstractions)
1. `_guard()` - 17 edges
2. `BrandError` - 14 edges
3. `Visual Foundations` - 13 edges
4. `Spec — Sistema de Identidad de Producto AGLAYA` - 11 edges
5. `_read()` - 10 edges
6. `AGLAYA Design System` - 9 edges
7. `_signature_terms()` - 9 edges
8. `_product()` - 9 edges
9. `get_voice_rules()` - 8 edges
10. `Content Fundamentals` - 7 edges

## Surprising Connections (you probably didn't know these)
- `Primary Logo Specimen` --displays--> `AGLAYA Logotype – White`  [INFERRED]
  preview/brand-logo-primary.html → assets/logotipo/svg/aglaya-logotipo-blanco.svg
- `Logo Variants Specimen` --displays--> `AGLAYA Logotype – White`  [INFERRED]
  preview/brand-logo-variants.html → assets/logotipo/svg/aglaya-logotipo-blanco.svg
- `Logo Variants Specimen` --displays--> `AGLAYA Logotype – Brand Red`  [INFERRED]
  preview/brand-logo-variants.html → assets/logotipo/svg/aglaya-logotipo-color.svg
- `Logo Variants Specimen` --displays--> `AGLAYA Logotype – Black`  [INFERRED]
  preview/brand-logo-variants.html → assets/logotipo/svg/aglaya-logotipo-negro.svg
- `Website UI Kit Index` --references--> `Website Kit Logo White`  [INFERRED]
  ui_kits/website/index.html → ui_kits/website/assets/logo-white.svg

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Typography System (Display, Body, Mono)** — outfit_font, inter_font, space_mono_font [EXTRACTED 1.00]
- **MCP Server Implementation (Query Layer)** — aglaya_ds_mcp_server, aglaya_ds_mcp_brand, aglaya_ds_mcp_readme [EXTRACTED 1.00]

## Communities (53 total, 37 thin omitted)

### Community 0 - "Brand Voice Rules"
Cohesion: 0.09
Nodes (35): _all_tokens(), _available_logos(), BrandError, _category_of(), _components_manifest(), get_accent(), get_component(), get_glyph() (+27 more)

### Community 1 - "Sovereign Brand Server"
Cohesion: 0.09
Nodes (33): check_voice(), get_accent(), get_component(), get_glyph(), get_lockup(), get_logo(), get_nonnegotiables(), get_product() (+25 more)

### Community 2 - "Design System Assets"
Cohesion: 0.40
Nodes (4): AGLAYA · Website UI Kit, Composition rules the kit enforces, Files, Known gaps

### Community 3 - "Token Management API"
Cohesion: 0.12
Nodes (14): AGLAYA · Flota — el capitán, CLAUDE.md — aglaya-design-system, Esta sección no lleva estado, Orden de lectura, Qué es este repo, Reglas duras, CONTRACT - AGLAYA Design System, Interfaces (dos formas de consumir) (+6 more)

### Community 4 - "MCP Server Testing"
Cohesion: 0.20
Nodes (9): main(), _payload(), End-to-end MCP self-test: spawn server.py over stdio as a real MCP client, list, Extract the structured/text content from a CallToolResult., main(), ZERO-COPY proof: within ONE live MCP session, edit the canonical CSS and show ge, _val(), aglaya-ds-mcp/.venv/bin/python (+1 more)

### Community 6 - "Logo Specimen Cards"
Cohesion: 0.40
Nodes (5): AGLAYA Logotype – White, AGLAYA Logotype – Brand Red, AGLAYA Logotype – Black, Primary Logo Specimen, Logo Variants Specimen

### Community 10 - "Website Kit"
Cohesion: 0.67
Nodes (3): Website Kit Favicon, Website Kit Logo White, Website UI Kit Index

### Community 38 - "CONTRACT — Estilo de marca AGLAYA"
Cohesion: 0.10
Nodes (20): AGLAYA Design System, Browse the system, Casing, Content Fundamentals, Extend it, Fonts, Forbidden patterns, How to use this system (+12 more)

### Community 39 - "Visual Foundations"
Cohesion: 0.15
Nodes (13): Animation, Backgrounds, Borders & radii, Cards, Cursor, Focus & accessibility, Imagery, Layout (+5 more)

### Community 40 - "guard_huella.py"
Cohesion: 0.47
Nodes (5): Path, enmascarar(), main(), Tapa los fragmentos entrecomillados conservando offsets y saltos., recortar_seccion()

### Community 42 - "Spec — Sistema de Identidad de Producto AGLAYA"
Cohesion: 0.17
Nodes (11): 10. Riesgos / vigilancias, 1. Problema, 2. Decisiones (brainstorming), 3. Roster final (6 productos), 4. Doctrina de dos niveles (no-negociables), 5. Forma sistematizada (dentro del repo), 6. Superficie MCP nueva (espejo de `brand.py`, lectura en vivo), 7. Iteraciones limpias (esta sesión, sin colapsar objetivos) (+3 more)

### Community 45 - "_read"
Cohesion: 0.15
Nodes (20): _bullets(), check_voice(), _forbidden_phrases(), get_nonnegotiables(), get_voice_rules(), is_allowed_word(), Return the body of a markdown section (### heading) up to the next     heading o, Parse a two-column markdown table into (col1, col2) rows, skipping     the heade (+12 more)

### Community 53 - "AGLAYA Design System — Sovereign Brand MCP"
Cohesion: 0.22
Nodes (7): AGLAYA Design System — Sovereign Brand MCP, Files, Register, Response shapes, Setup (one-time bootstrap), Tools, Verify

## Knowledge Gaps
- **93 isolated node(s):** `Sources`, `Index`, `Voice`, `Pronouns`, `Casing` (+88 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AGLAYA Design System` connect `CONTRACT — Estilo de marca AGLAYA` to `AGLAYA Design System — Sovereign Brand MCP`, `Visual Foundations`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Why does `Visual Foundations` connect `Visual Foundations` to `CONTRACT — Estilo de marca AGLAYA`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Why does `_read()` connect `_read` to `Brand Voice Rules`, `guard_huella.py`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **What connects `Sources`, `Index`, `Voice` to the rest of the system?**
  _93 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Brand Voice Rules` be split into smaller, more focused modules?**
  _Cohesion score 0.09206349206349207 - nodes in this community are weakly interconnected._
- **Should `Sovereign Brand Server` be split into smaller, more focused modules?**
  _Cohesion score 0.0855614973262032 - nodes in this community are weakly interconnected._
- **Should `Token Management API` be split into smaller, more focused modules?**
  _Cohesion score 0.11764705882352941 - nodes in this community are weakly interconnected._