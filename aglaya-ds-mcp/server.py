"""AGLAYA Design System — sovereign brand MCP server.

A SEPARATE query layer over the canonical design-system folder. It does NOT
own or copy any brand value: every tool reads the canonical files LIVE (see
`brand.py`) so downstream projects — aglaya.biz, the CRM panel, any Claude
session — can consult tokens, voice rules and logos without hand-copying them.

This is NOT graphify's generic `--mcp`; it is AGLAYA's own, dependency-light
(stdlib core + the MCP SDK only), stdio transport, drop-in for Claude Code /
Claude Desktop.

The design-system folder itself stays runtime-free and droppable; this
`aglaya-ds-mcp/` subfolder is an optional, separable consultation layer.

Register (user or project scope), e.g. Claude Code `.mcp.json`:
    {
      "mcpServers": {
        "aglaya-ds": {
          "command": "aglaya-ds-mcp/.venv/bin/python",
          "args": ["aglaya-ds-mcp/server.py"]
        }
      }
    }
"""

from __future__ import annotations

from typing import Optional

from mcp.server.fastmcp import FastMCP

import brand

mcp = FastMCP("aglaya-ds")


def _guard(fn, *args, **kwargs):
    """Run a core call, turning caller-facing BrandError into a clean dict."""
    try:
        return fn(*args, **kwargs)
    except brand.BrandError as e:
        return {"error": str(e)}


@mcp.tool()
def get_token(name: str) -> dict:
    """Return the live value of a single design token from colors_and_type.css.

    `name` accepts 'color-brand' or '--color-brand'.
    Example: get_token("color-brand") -> {"token": "--color-brand", "value": "#e8003d"}.
    """
    val = _guard(brand.get_token, name)
    if isinstance(val, dict):  # error
        return val
    return {"token": "--" + name.strip().lstrip("-"), "value": val}


@mcp.tool()
def list_tokens(category: Optional[str] = None) -> dict:
    """List design tokens, optionally by category.

    Categories: color, type, spacing, radius, motion, shadow, other.
    Omit `category` for all tokens.
    """
    return _guard(brand.list_tokens, category)


@mcp.tool()
def get_voice_rules() -> dict:
    """Return the brand voice rules read live from README.md: tone, pronouns
    (you/we), casing, protected vocabulary, and forbidden patterns."""
    return _guard(brand.get_voice_rules)


@mcp.tool()
def check_voice(text: str) -> dict:
    """Analyse `text` against the brand voice. Flags off-brand terms (with the
    AGLAYA-correct replacement, e.g. "solutions" -> "systems", "newsletter" ->
    "Dispatch"), forbidden phrases, exclamation marks, emoji, and rhetorical
    warmth questions. Returns {clean, findings}."""
    return _guard(brand.check_voice, text)


@mcp.tool()
def is_allowed_word(term: str) -> dict:
    """Is `term` on-brand? Protected vocabulary returns allowed=True; off-brand
    terms return allowed=False plus the correct AGLAYA term."""
    return _guard(brand.is_allowed_word, term)


@mcp.tool()
def get_logo(variant: str, fmt: str = "svg") -> dict:
    """Resolve a logo variant to its canonical file under assets/.

    variant: '<isotipo|logotipo>-<color>' — color accepts es/en aliases
    (rojo/red, blanco/white, negro/black, color). fmt: 'svg' (default) or 'png'.
    Example: get_logo("isotipo-rojo") -> path to assets/isotipo/svg/aglaya-isotipo-rojo.svg.
    """
    return _guard(brand.get_logo, variant, fmt)


@mcp.tool()
def get_nonnegotiables(scope: Optional[str] = None) -> dict:
    """The hard brand rules read live from SKILL.md.

    scope: 'master' (default) — the rigid marca-madre rules: AGLAYA uppercase,
    zero radius, 3 colors only, no emoji / Lucide / Heroicons, two-line headline
    with the second line in brand red, etc. 'product' — the product-surface
    rules: everything inherited from master EXCEPT color exclusivity; the
    product accent is first-class (allowed on CTAs, no proportion cap).
    """
    return _guard(brand.get_nonnegotiables, scope)


# ── Product identity (read live from products/products.json) ────────────────


@mcp.tool()
def list_products() -> dict:
    """List the AGLAYA product roster read live from products/products.json:
    id, name, accent (hex + token), functions, sacred flag. Includes the
    monolithic model + single-voice markers and any removed products."""
    return _guard(brand.list_products)


@mcp.tool()
def get_product(id: str) -> dict:
    """Full identity record for one product (accent, functions, glyph/lockup
    paths, exceptions). `id` accepts the slug ('kanban-desk') or display name."""
    return _guard(brand.get_product, id)


@mcp.tool()
def get_accent(id: str) -> dict:
    """A product's accent color: token, hex, oklch, cross-checked against the
    live CSS token. Two-level doctrine: the accent is first-class on that
    product's surface (CTA allowed, no proportion cap), never on the master."""
    return _guard(brand.get_accent, id)


@mcp.tool()
def get_glyph(id: str, variant: str = "accent") -> dict:
    """Resolve a product glyph SVG. variant: 'white' | 'accent' | 'fill'.
    Errors with the reason when a product ships no glyph (e.g. the sacred
    CONSENT FLOW ships none — it is never fabricated)."""
    return _guard(brand.get_glyph, id, variant)


@mcp.tool()
def get_lockup(id: str, layout: str = "lockup") -> dict:
    """Resolve a product lockup SVG. layout: 'lockup' (horizontal) | 'stacked'
    | product-specific ('lockup-outlined', 'lockup-ondark' for CONSENT FLOW)."""
    return _guard(brand.get_lockup, id, layout)


@mcp.tool()
def get_product_voice(id: str) -> dict:
    """A product's voice. Single-voice doctrine: returns the one AGLAYA voice
    for every product (per-product voice is intentional absence, not a gap)."""
    return _guard(brand.get_product_voice, id)


if __name__ == "__main__":
    mcp.run()  # stdio transport
