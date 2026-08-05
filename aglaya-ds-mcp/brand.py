"""AGLAYA brand core — sovereign, dependency-free readers over the canonical files.

This module is the SOVEREIGN CORE of the brand MCP. It has ZERO third-party
dependencies (stdlib only) and holds ZERO hardcoded brand values: every token,
rule, vocabulary term and logo path is read LIVE from the canonical files in the
design-system folder each time it is requested. Change `colors_and_type.css`,
`README.md`, `SKILL.md` or `assets/` and the answers change with no code edit.

Canonical files (resolved relative to the repo root = this file's grandparent):
  - colors_and_type.css : design tokens (the single source of truth)
  - README.md           : voice rules, protected vocabulary, forbidden patterns
  - SKILL.md            : the hard non-negotiables
  - assets/             : canonical logo SVG/PNG

The MCP server (`server.py`) is a thin transport layer over these functions.
Keeping the core here means it is testable and reusable without the MCP SDK.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

# Repo root = the design-system folder that CONTAINS this mcp subfolder.
# aglaya-ds-mcp/brand.py -> parent (aglaya-ds-mcp) -> parent (repo root).
REPO_ROOT = Path(__file__).resolve().parent.parent

CSS_FILE = REPO_ROOT / "colors_and_type.css"
README_FILE = REPO_ROOT / "README.md"
SKILL_FILE = REPO_ROOT / "SKILL.md"
ASSETS_DIR = REPO_ROOT / "assets"
PRODUCTS_FILE = REPO_ROOT / "products" / "products.json"
COMPONENTS_FILE = REPO_ROOT / "components" / "components.json"


class BrandError(Exception):
    """Raised for caller-facing problems (unknown token, missing file, etc.)."""


def _read(path: Path) -> str:
    if not path.exists():
        raise BrandError(f"canonical file missing: {path.relative_to(REPO_ROOT)}")
    return path.read_text(encoding="utf-8")


# ────────────────────────────────────────────────────────────────────────────
# TOKENS  (read live from colors_and_type.css :root {})
# ────────────────────────────────────────────────────────────────────────────

_TOKEN_RE = re.compile(r"--([a-zA-Z0-9-]+)\s*:\s*([^;]+);")

# category -> ordered prefixes that classify a token by its name
_CATEGORIES: dict[str, tuple[str, ...]] = {
    "color": ("color-", "fg-"),
    "type": ("font-", "text-", "tracking-"),
    "spacing": ("space-", "layout-", "bp-"),
    "radius": ("radius-",),
    "motion": ("ease-", "dur-"),
    "shadow": ("shadow-", "glow-", "aura-"),
    "product": ("product-",),
}


def _all_tokens() -> dict[str, str]:
    """Parse every custom property inside the first :root { … } block."""
    css = _read(CSS_FILE)
    root = re.search(r":root\s*\{(.*?)\}", css, re.DOTALL)
    scope = root.group(1) if root else css
    out: dict[str, str] = {}
    for name, value in _TOKEN_RE.findall(scope):
        out[name] = re.sub(r"\s+", " ", value).strip()
    return out


def _category_of(name: str) -> str:
    for cat, prefixes in _CATEGORIES.items():
        if name.startswith(prefixes):
            return cat
    return "other"


def get_token(name: str) -> str:
    """Return the value of a single token. Accepts 'color-brand' or '--color-brand'."""
    key = name.strip().lstrip("-")
    tokens = _all_tokens()
    if key not in tokens:
        # helpful nudge: suggest near matches
        near = [n for n in tokens if key in n or n in key][:5]
        hint = f" Did you mean: {', '.join('--' + n for n in near)}?" if near else ""
        raise BrandError(f"unknown token '--{key}'.{hint}")
    return tokens[key]


def list_tokens(category: Optional[str] = None) -> dict:
    """List tokens, optionally filtered by category.

    Returns {"category": <str|"all">, "count": n, "tokens": {name: value}}.
    Categories: color, type, spacing, radius, motion, shadow, other.
    """
    tokens = _all_tokens()
    if category:
        cat = category.strip().lower()
        valid = set(_CATEGORIES) | {"other"}
        if cat not in valid:
            raise BrandError(
                f"unknown category '{category}'. Valid: {', '.join(sorted(valid))}."
            )
        tokens = {n: v for n, v in tokens.items() if _category_of(n) == cat}
    else:
        cat = "all"
    return {
        "category": cat,
        "count": len(tokens),
        "tokens": {f"--{n}": v for n, v in tokens.items()},
    }


# ────────────────────────────────────────────────────────────────────────────
# VOICE  (read live from README.md)
# ────────────────────────────────────────────────────────────────────────────


def _section(md: str, heading: str) -> str:
    """Return the body of a markdown section (### heading) up to the next
    heading of the same-or-higher level or a horizontal rule."""
    pat = re.compile(
        r"^#{2,4}\s+" + re.escape(heading) + r"\s*$(.*?)(?=^#{1,4}\s|\n---\s*$|\Z)",
        re.DOTALL | re.MULTILINE,
    )
    m = pat.search(md)
    return m.group(1).strip() if m else ""


def _bullets(block: str) -> list[str]:
    out = []
    for line in block.splitlines():
        s = line.strip()
        if s.startswith(("- ", "* ")):
            out.append(s[2:].strip())
    return out


def _table_rows(block: str) -> list[tuple[str, str]]:
    """Parse a two-column markdown table into (col1, col2) rows, skipping
    the header and separator lines."""
    rows = []
    for line in block.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 2:
            continue
        if set(cells[0]) <= {"-", " "} or cells[0].lower() in ("term", "source"):
            continue  # separator / header
        rows.append((cells[0], cells[1]))
    return rows


def _strip_md(s: str) -> str:
    return re.sub(r"[*`_]", "", s).strip()


def _signature_terms() -> list[dict]:
    """Protected vocabulary from README '### Signature terms', with the
    forbidden words each term REPLACES parsed live from its usage cell."""
    md = _read(README_FILE)
    block = _section(md, "Signature terms")
    terms = []
    for term_cell, usage_cell in _table_rows(block):
        # canonical term = first bolded/plain head, before any "(" or "/"
        head = _strip_md(term_cell).split("(")[0].split("/")[0].strip()
        # words this term replaces: any quoted synonym that appears in a cell
        # carrying a negative trigger (not / never / in place of). Scans BOTH
        # the term cell ('Systems (not "solutions", not "tools")') and the
        # usage cell ('in place of "lead", "metric", "input"').
        replaces = []
        for cell in (term_cell, usage_cell):
            if re.search(r"\b(?:not|never|in place of)\b", cell, re.IGNORECASE):
                replaces += re.findall(r'"([^"]+)"', cell)
        terms.append(
            {
                "term": head,
                "usage": _strip_md(usage_cell),
                "replaces": [r.lower() for r in replaces],
            }
        )
    return terms


def _forbidden_phrases() -> list[str]:
    """Quoted forbidden phrases from README '### Forbidden patterns'."""
    md = _read(README_FILE)
    block = _section(md, "Forbidden patterns")
    phrases = []
    for bullet in _bullets(block):
        for q in re.findall(r'"([^"]+)"', bullet):
            cleaned = q.strip().strip("…").strip()
            if cleaned:
                phrases.append(cleaned)
    return phrases


def get_voice_rules() -> dict:
    """Structured voice rules read live from README '## Content Fundamentals'."""
    md = _read(README_FILE)
    sig = _signature_terms()
    return {
        "voice": _strip_md(_section(md, "Voice")),
        # Full section, not just its bullets: the rule is stated in the lead
        # line ("Assertiveness is not a tone. It is what you can back."), and
        # _bullets would drop exactly that.
        "evidence": _strip_md(_section(md, "Evidence")),
        "pronouns": _bullets(_section(md, "Pronouns")),
        "casing": _bullets(_section(md, "Casing")),
        "protected_vocabulary": [
            {"term": t["term"], "usage": t["usage"]} for t in sig
        ],
        "forbidden_patterns": _bullets(_section(md, "Forbidden patterns")),
    }


# words/phrases that are always wrong, mapped to the AGLAYA-correct term.
# Built LIVE from the signature-terms table (never hardcoded here).
def _replacement_map() -> dict[str, str]:
    mapping: dict[str, str] = {}
    for t in _signature_terms():
        for word in t["replaces"]:
            mapping[word] = t["term"]
    return mapping


# emoji / forbidden pictographic-symbol ranges. Deliberately EXCLUDES U+2192
# (→) — AGLAYA keeps the literal arrow in CTA labels ("Request Proposal →").
_EMOJI_RE = re.compile(
    "[" "\U0001f000-\U0001faff" "\U00002600-\U000026ff" "\U00002700-\U000027bf" "]"
)


def check_voice(text: str) -> dict:
    """Analyse `text` against the live brand voice rules. Returns findings with
    the AGLAYA-correct replacement where one exists."""
    findings = []
    low = text.lower()

    # 1) replacement terms (word-boundary, from signature table)
    for wrong, right in _replacement_map().items():
        if re.search(r"\b" + re.escape(wrong) + r"\b", low):
            findings.append(
                {
                    "type": "replace_term",
                    "match": wrong,
                    "message": f'"{wrong}" is off-brand',
                    "suggestion": f'use "{right}"',
                }
            )

    # 2) forbidden phrases (word-boundary match, from forbidden-patterns list).
    # \b…\b avoids substring false positives (e.g. "solutions" inside
    # "resolutions", "partners" inside "partnerships").
    for phrase in _forbidden_phrases():
        pl = phrase.lower()
        if (
            pl
            and re.search(r"\b" + re.escape(pl) + r"\b", low)
            and not any(f["match"] == pl for f in findings)
        ):
            findings.append(
                {
                    "type": "forbidden_phrase",
                    "match": phrase,
                    "message": f'"{phrase}" is a forbidden pattern',
                    "suggestion": "remove / rewrite in terse, imperative voice",
                }
            )

    # 3) exclamation marks
    if "!" in text:
        findings.append(
            {
                "type": "punctuation",
                "match": "!",
                "message": "exclamation marks are forbidden",
                "suggestion": "state it flat — AGLAYA never exclaims",
            }
        )

    # 4) emoji / pictographic symbols
    for sym in dict.fromkeys(_EMOJI_RE.findall(text)):
        findings.append(
            {
                "type": "emoji",
                "match": sym,
                "message": "emoji / decorative symbols are forbidden",
                "suggestion": "delete it — zero emoji in AGLAYA copy",
            }
        )

    # 5) rhetorical warmth question (advisory — AGLAYA avoids sales-warmth ?s)
    if "?" in text:
        findings.append(
            {
                "type": "rhetorical_question",
                "match": "?",
                "message": "possible rhetorical / warmth question",
                "suggestion": "advisory — AGLAYA avoids rhetorical questions for warmth",
                "advisory": True,
            }
        )

    return {
        "text": text,
        "clean": not [f for f in findings if not f.get("advisory")],
        "findings": findings,
    }


def is_allowed_word(term: str) -> dict:
    """Is `term` allowed? Protected terms -> allowed; off-brand terms -> the
    correct replacement."""
    t = term.strip()
    tl = t.lower()
    for sig in _signature_terms():
        if sig["term"].lower() == tl:
            return {
                "term": t,
                "allowed": True,
                "protected": True,
                "note": f"protected brand term — {sig['usage']}",
            }
    repl = _replacement_map()
    if tl in repl:
        return {
            "term": t,
            "allowed": False,
            "protected": False,
            "correct_term": repl[tl],
            "note": f'off-brand — use "{repl[tl]}"',
        }
    # A retired term is not neutral. Without this, `is_allowed_word` claimed a
    # word was "not forbidden" while `check_voice` flagged the same word — two
    # tools, two answers, and the cheaper one blessing what the other bans.
    for phrase in _forbidden_phrases():
        if phrase.lower() == tl:
            return {
                "term": t,
                "allowed": False,
                "protected": False,
                "note": "forbidden pattern — README '### Forbidden patterns' "
                        "says what to write instead",
            }
    return {
        "term": t,
        "allowed": True,
        "protected": False,
        "note": "not a protected or forbidden term — neutral",
    }


# ────────────────────────────────────────────────────────────────────────────
# LOGOS  (read live from assets/)
# ────────────────────────────────────────────────────────────────────────────

_LOGO_KINDS = ("isotipo", "logotipo")
# color aliases -> the filename token actually used on disk, per kind
_COLOR_ALIASES = {
    "white": "blanco",
    "blanco": "blanco",
    "black": "negro",
    "negro": "negro",
    "red": "rojo",
    "rojo": "rojo",
    "color": "color",
}


def _available_logos() -> list[str]:
    out = []
    for kind in _LOGO_KINDS:
        svg = ASSETS_DIR / kind / "svg"
        if svg.is_dir():
            for f in sorted(svg.glob(f"aglaya-{kind}-*.svg")):
                out.append(f.stem.replace(f"aglaya-{kind}-", f"{kind}-"))
    return out


def get_logo(variant: str, fmt: str = "svg") -> dict:
    """Resolve a logo variant to its canonical file.

    variant: '<kind>-<color>' e.g. 'isotipo-rojo', 'logotipo-blanco',
             'logotipo-color'. Kind: isotipo|logotipo. Color accepts
             es/en aliases (rojo/red, blanco/white, negro/black, color).
    fmt: 'svg' (default, canonical) or 'png'.
    """
    parts = variant.strip().lower().replace("_", "-").split("-", 1)
    if len(parts) != 2 or parts[0] not in _LOGO_KINDS:
        raise BrandError(
            f"variant must be '<isotipo|logotipo>-<color>'. Available: "
            f"{', '.join(_available_logos())}"
        )
    kind, color_raw = parts
    color = _COLOR_ALIASES.get(color_raw)
    if color is None:
        raise BrandError(
            f"unknown color '{color_raw}'. Use one of: "
            f"{', '.join(sorted(set(_COLOR_ALIASES)))}"
        )
    fmt = fmt.strip().lower()
    if fmt not in ("svg", "png"):
        raise BrandError("fmt must be 'svg' or 'png'")
    path = ASSETS_DIR / kind / fmt / f"aglaya-{kind}-{color}.{fmt}"
    if not path.exists():
        raise BrandError(
            f"no {fmt} for '{kind}-{color}'. Available: {', '.join(_available_logos())}"
        )
    return {
        "variant": f"{kind}-{color}",
        "format": fmt,
        "path": str(path),
        "relative_path": str(path.relative_to(REPO_ROOT)),
        "exists": True,
    }


# ────────────────────────────────────────────────────────────────────────────
# PRODUCTS  (read live from products/products.json — the roster's single truth)
# ────────────────────────────────────────────────────────────────────────────


def _manifest() -> dict:
    """Parse products/products.json live."""
    raw = _read(PRODUCTS_FILE)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise BrandError(f"products.json is not valid JSON: {e}")


def _product(pid: str) -> dict:
    """Resolve a product by id (slug) or display name, case-insensitive."""
    key = pid.strip().lower()
    products = _manifest().get("products", [])
    for p in products:
        if p.get("id") == key or p.get("name", "").lower() == key:
            return p
    known = ", ".join(p.get("id", "?") for p in products)
    raise BrandError(f"unknown product '{pid}'. Known: {known}")


def list_products() -> dict:
    """Roster summary read live from the manifest."""
    m = _manifest()
    prods = [
        {
            "id": p["id"],
            "name": p["name"],
            "sacred": p.get("sacred", False),
            "accent": p["accent"]["hex"],
            "accent_token": p["accent"]["token"],
            "functions": p.get("functions", []),
        }
        for p in m.get("products", [])
    ]
    return {
        "model": m.get("model"),
        "voice": m.get("voice"),
        "count": len(prods),
        "products": prods,
        "removed": [r.get("id") for r in m.get("removed", [])],
    }


def get_product(pid: str) -> dict:
    """Full manifest record for one product."""
    return _product(pid)


def get_accent(pid: str) -> dict:
    """A product's accent: manifest values cross-checked against the live CSS
    token (so the answer can never silently drift from colors_and_type.css)."""
    p = _product(pid)
    a = p["accent"]
    out = {
        "product": p["id"],
        "token": a["token"],
        "hex": a["hex"],
        "oklch": a.get("oklch"),
        "name": a.get("name"),
    }
    if "secondary" in a:
        out["secondary"] = a["secondary"]
    try:
        out["css_value"] = get_token(a["token"])
    except BrandError:
        out["css_value"] = None
        out["warning"] = f"{a['token']} not found in colors_and_type.css"
    return out


def get_glyph(pid: str, variant: Optional[str] = None) -> dict:
    """Resolve a product glyph SVG path. Variant keys are manifest-driven and
    vary by product: most use 'white'|'accent'|'fill'; CONSENT FLOW is the
    set's exception with a colour isotipo ('color'|'light'). Omit `variant`
    for the default ('accent' if present, else the first available key)."""
    p = _product(pid)
    glyphs = {k: val for k, val in (p.get("glyphs") or {}).items() if val}
    if not glyphs:
        reason = p.get("glyphs_absent_reason", "product ships no glyph")
        raise BrandError(f"'{p['id']}' ships no glyph — {reason}")
    if variant is None:
        v = "accent" if "accent" in glyphs else next(iter(glyphs))
    else:
        v = variant.strip().lower()
    if v not in glyphs:
        raise BrandError(
            f"'{p['id']}' has no '{v}' glyph. Available: {', '.join(glyphs)}"
        )
    path = glyphs[v]
    full = REPO_ROOT / path
    return {
        "product": p["id"],
        "variant": v,
        "path": str(full),
        "relative_path": path,
        "exists": full.exists(),
    }


def get_lockup(pid: str, layout: str = "lockup") -> dict:
    """Resolve a product lockup SVG path. layout: 'lockup' (horizontal),
    'stacked', or any product-specific key (e.g. CONSENT FLOW's
    'lockup-outlined', 'lockup-ondark')."""
    p = _product(pid)
    lay = layout.strip().lower()
    lockups = p.get("lockups") or {}
    if not lockups.get(lay):
        avail = ", ".join(k for k, v in lockups.items() if v)
        raise BrandError(f"'{p['id']}' has no '{lay}' lockup. Available: {avail}")
    path = lockups[lay]
    full = REPO_ROOT / path
    return {
        "product": p["id"],
        "layout": lay,
        "path": str(full),
        "relative_path": path,
        "exists": full.exists(),
    }


def get_product_voice(pid: str) -> dict:
    """A product's voice. Single-voice doctrine: every product speaks the one
    AGLAYA voice — this validates the id and returns the shared voice rules,
    making explicit that per-product voice is intentional absence, not a gap."""
    p = _product(pid)
    return {
        "product": p["id"],
        "voice_model": "single",
        "note": (
            "Todos los productos hablan con la voz única AGLAYA — "
            "no hay voz por producto (intencional, no un hueco)."
        ),
        "voice": get_voice_rules(),
    }


# ────────────────────────────────────────────────────────────────────────────
# COMPONENTS  (read live from components/components.json)
# ────────────────────────────────────────────────────────────────────────────


def _components_manifest() -> dict:
    raw = _read(COMPONENTS_FILE)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise BrandError(f"components.json is not valid JSON: {e}")


def list_components() -> dict:
    """Component roster (button, card, input, badge…) with their variants,
    read live from components/components.json."""
    comps = _components_manifest().get("components", [])
    return {
        "count": len(comps),
        "components": [
            {
                "id": c["id"],
                "name": c["name"],
                "variants": [v["name"] for v in c.get("variants", [])],
            }
            for c in comps
        ],
    }


def get_component(cid: str) -> dict:
    """Full spec for one component: token refs, per-variant/structural values,
    states and rules. `cid` accepts the id ('button') or display name."""
    key = cid.strip().lower()
    comps = _components_manifest().get("components", [])
    for c in comps:
        if c.get("id") == key or c.get("name", "").lower() == key:
            return c
    known = ", ".join(c.get("id", "?") for c in comps)
    raise BrandError(f"unknown component '{cid}'. Known: {known}")


# ────────────────────────────────────────────────────────────────────────────
# NON-NEGOTIABLES  (read live from SKILL.md)
# ────────────────────────────────────────────────────────────────────────────


# scope -> the exact SKILL.md heading it maps to. Kept HERE (not in the caller)
# so the em-dash heading string lives in one place and callers pass a plain word.
_NONNEG_HEADINGS = {
    "master": "Non-negotiables",
    "product": "Non-negotiables — producto",
}
_NONNEG_SCOPE_ALIASES = {
    "master": "master", "madre": "master", "casa": "master", "house": "master",
    "product": "product", "producto": "product",
}


def get_nonnegotiables(scope: Optional[str] = None) -> dict:
    """The hard brand rules, read live from SKILL.md.

    scope: 'master' (default) -> the rigid marca-madre rules from
    '## Non-negotiables'. 'product' -> the product-surface rules from
    '## Non-negotiables — producto' (accent is first-class: CTA allowed, no
    proportion cap; everything else inherited from master).
    """
    key = (scope or "master").strip().lower()
    resolved = _NONNEG_SCOPE_ALIASES.get(key)
    if resolved is None:
        raise BrandError(
            f"unknown scope '{scope}'. Use 'master' (default) or 'product'."
        )
    md = _read(SKILL_FILE)
    block = _section(md, _NONNEG_HEADINGS[resolved])
    return {"source": "SKILL.md", "scope": resolved, "rules": _bullets(block)}
