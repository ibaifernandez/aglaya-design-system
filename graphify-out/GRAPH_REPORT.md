# Graph Report - .  (2026-07-12)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 141 nodes · 162 edges · 38 communities (10 shown, 28 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.71)
- Token cost: 36,564 input · 2,206 output

## Graph Freshness
- Built from commit: `7aae0f98`
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

## God Nodes (most connected - your core abstractions)
1. `_signature_terms()` - 9 edges
2. `_guard()` - 9 edges
3. `Design Tokens (CSS Custom Properties)` - 9 edges
4. `_read()` - 8 edges
5. `BrandError` - 7 edges
6. `get_voice_rules()` - 7 edges
7. `_section()` - 6 edges
8. `_forbidden_phrases()` - 6 edges
9. `_all_tokens()` - 5 edges
10. `list_tokens()` - 5 edges

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
- **Canonical Brand Source (Sovereign Package)** — readme, skill, colors_and_type, assets, fonts, preview [EXTRACTED 1.00]
- **MCP Server Implementation (Query Layer)** — aglaya_ds_mcp_server, aglaya_ds_mcp_brand, aglaya_ds_mcp_readme [EXTRACTED 1.00]
- **Design System Preview and Documentation Suite** — readme, preview_brand_favicon_html, preview_brand_iconography_html, preview_colors_brand_html, preview_components_badges_html, preview_components_buttons_html, preview_components_card_html, preview_spacing_borders_html [EXTRACTED 0.95]

## Communities (38 total, 28 thin omitted)

### Community 0 - "Brand Voice Rules"
Cohesion: 0.17
Nodes (22): _bullets(), check_voice(), _forbidden_phrases(), get_nonnegotiables(), get_voice_rules(), is_allowed_word(), AGLAYA brand core — sovereign, dependency-free readers over the canonical files., Return the body of a markdown section (### heading) up to the next     heading o (+14 more)

### Community 1 - "Sovereign Brand Server"
Cohesion: 0.16
Nodes (17): check_voice(), get_logo(), get_nonnegotiables(), get_token(), get_voice_rules(), _guard(), is_allowed_word(), list_tokens() (+9 more)

### Community 2 - "Design System Assets"
Cohesion: 0.33
Nodes (11): AGLAYA.biz Website, MCP Server Documentation, Logos and Favicons, Design Tokens (CSS Custom Properties), Font Files, Inter Typeface (Body), Outfit Typeface (Display), Design System Specimen Cards (+3 more)

### Community 3 - "Token Management API"
Cohesion: 0.17
Nodes (13): _all_tokens(), _available_logos(), BrandError, _category_of(), get_logo(), get_token(), list_tokens(), Raised for caller-facing problems (unknown token, missing file, etc.). (+5 more)

### Community 4 - "MCP Server Testing"
Cohesion: 0.20
Nodes (9): main(), _payload(), End-to-end MCP self-test: spawn server.py over stdio as a real MCP client, list, Extract the structured/text content from a CallToolResult., main(), ZERO-COPY proof: within ONE live MCP session, edit the canonical CSS and show ge, _val(), aglaya-ds-mcp/.venv/bin/python (+1 more)

### Community 6 - "Logo Specimen Cards"
Cohesion: 0.40
Nodes (5): AGLAYA Logotype – White, AGLAYA Logotype – Brand Red, AGLAYA Logotype – Black, Primary Logo Specimen, Logo Variants Specimen

### Community 10 - "Website Kit"
Cohesion: 0.50
Nodes (4): Website Kit Favicon, Website Kit Logo White, Website UI Kit Index, Website UI Kit Documentation

## Knowledge Gaps
- **35 isolated node(s):** `EXCLUSIONS`, `FOOTER_LINKS`, `PROBLEMS`, `SYSTEMS`, `aglaya-ds-mcp/.venv/bin/python` (+30 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **28 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BrandError` connect `Token Management API` to `Brand Voice Rules`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Why does `Design Tokens (CSS Custom Properties)` connect `Design System Assets` to `Brand Voice Rules`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **What connects `EXCLUSIONS`, `FOOTER_LINKS`, `PROBLEMS` to the rest of the system?**
  _35 weakly-connected nodes found - possible documentation gaps or missing edges._