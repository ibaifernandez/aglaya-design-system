# Graph Report - aglaya-design-system  (2026-07-21)

## Corpus Check
- 21 files · ~16,744 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 166 nodes · 186 edges · 42 communities (13 shown, 29 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.71)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4aa51460`
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
- AGLAYA · Website UI Kit
- guard_huella.py
- test_guard_huella.sh

## God Nodes (most connected - your core abstractions)
1. `_signature_terms()` - 9 edges
2. `_guard()` - 9 edges
3. `Design Tokens (CSS Custom Properties)` - 9 edges
4. `_read()` - 8 edges
5. `BrandError` - 7 edges
6. `get_voice_rules()` - 7 edges
7. `_section()` - 6 edges
8. `_forbidden_phrases()` - 6 edges
9. `CONTRACT — Estilo de marca AGLAYA` - 6 edges
10. `CLAUDE.md — aglaya-design-system` - 5 edges

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

## Communities (42 total, 29 thin omitted)

### Community 0 - "Brand Voice Rules"
Cohesion: 0.10
Nodes (35): _all_tokens(), _available_logos(), BrandError, _bullets(), _category_of(), check_voice(), _forbidden_phrases(), get_logo() (+27 more)

### Community 1 - "Sovereign Brand Server"
Cohesion: 0.16
Nodes (17): check_voice(), get_logo(), get_nonnegotiables(), get_token(), get_voice_rules(), _guard(), is_allowed_word(), list_tokens() (+9 more)

### Community 2 - "Design System Assets"
Cohesion: 0.33
Nodes (11): AGLAYA.biz Website, MCP Server Documentation, Logos and Favicons, Design Tokens (CSS Custom Properties), Font Files, Inter Typeface (Body), Outfit Typeface (Display), Design System Specimen Cards (+3 more)

### Community 3 - "Token Management API"
Cohesion: 0.29
Nodes (6): AGLAYA · Flota — el capitán, CLAUDE.md — aglaya-design-system, Esta sección no lleva estado, Orden de lectura, Qué es este repo, Reglas duras

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
Cohesion: 0.29
Nodes (6): CONTRACT — Estilo de marca AGLAYA, Interfaces (dos formas de consumir), No-negociables, Quién consume, Quién NO (exclusión dura), Qué rige

### Community 39 - "AGLAYA · Website UI Kit"
Cohesion: 0.50
Nodes (4): AGLAYA · Website UI Kit, Composition rules the kit enforces, Files, Known gaps

### Community 40 - "guard_huella.py"
Cohesion: 0.60
Nodes (4): enmascarar(), main(), Tapa los fragmentos entrecomillados conservando offsets y saltos., recortar_seccion()

## Knowledge Gaps
- **46 isolated node(s):** `Qué es este repo`, `Orden de lectura`, `Reglas duras`, `Esta sección no lleva estado`, `Qué rige` (+41 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AGLAYA · Website UI Kit` connect `AGLAYA · Website UI Kit` to `Design System Assets`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `Design Tokens (CSS Custom Properties)` connect `Design System Assets` to `Brand Voice Rules`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **What connects `Qué es este repo`, `Orden de lectura`, `Reglas duras` to the rest of the system?**
  _46 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Brand Voice Rules` be split into smaller, more focused modules?**
  _Cohesion score 0.10158730158730159 - nodes in this community are weakly interconnected._