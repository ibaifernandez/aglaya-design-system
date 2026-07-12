# AGLAYA Design System — Sovereign Brand MCP

A small, **AGLAYA-owned** MCP server that lets any project consult the brand
**live** — tokens, voice rules, protected vocabulary, logos — instead of
hand-copying values. It is the query layer over the canonical design-system
folder; the folder stays the single source of truth.

- **Sovereign.** Own code. The stdlib-only core (`brand.py`) has **zero**
  third-party dependencies and **zero** hardcoded brand values. The MCP SDK is
  the only external package, and only the transport (`server.py`) touches it.
  This is **not** graphify's generic `--mcp`.
- **Zero-copy, single source.** Every tool **reads the canonical files live**
  on each call. Change `colors_and_type.css` / `README.md` / `SKILL.md` /
  `assets/` and the answers change with no code edit. (Proven by
  `zerocopy_test.py`.)
- **Separate layer.** The design-system folder remains runtime-free and
  droppable. This `aglaya-ds-mcp/` subfolder is optional and separable — drop
  the design system without it and nothing breaks.

## Tools

| Tool | Reads | Returns |
| ---- | ----- | ------- |
| `get_token(name)` | `colors_and_type.css` | value of one token (`color-brand` or `--color-brand`) |
| `list_tokens(category?)` | `colors_and_type.css` | all tokens, or one category: `color·type·spacing·radius·motion·shadow·other` |
| `get_voice_rules()` | `README.md` | tone, pronouns, casing, protected vocabulary, forbidden patterns |
| `check_voice(text)` | `README.md` | off-brand findings + AGLAYA-correct replacement |
| `is_allowed_word(term)` | `README.md` | allowed? + correct term if off-brand |
| `get_logo(variant, fmt?)` | `assets/` | canonical file path for a logo variant |
| `get_nonnegotiables()` | `SKILL.md` | the hard brand rules |

## Setup (one-time bootstrap)

The venv is gitignored — recreate it after cloning:

```bash
cd aglaya-ds-mcp
python3 -m venv .venv
./.venv/bin/python -m pip install -e .      # installs the MCP SDK
```

## Register

**Claude Code** — `.mcp.json` at the repo root (already provided):

```json
{
  "mcpServers": {
    "aglaya-ds": {
      "command": "aglaya-ds-mcp/.venv/bin/python",
      "args": ["aglaya-ds-mcp/server.py"]
    }
  }
}
```

**Claude Desktop** — `claude_desktop_config.json`, using absolute paths:

```json
{
  "mcpServers": {
    "aglaya-ds": {
      "command": "/ABS/PATH/aglaya-design-system/aglaya-ds-mcp/.venv/bin/python",
      "args": ["/ABS/PATH/aglaya-design-system/aglaya-ds-mcp/server.py"]
    }
  }
}
```

Then the tools are callable from any session: `get_token`, `check_voice`, etc.

## Examples (real output)

```text
get_token("color-brand")
  -> {"token": "--color-brand", "value": "#e8003d"}

list_tokens("motion")
  -> {"category": "motion", "count": 6,
      "tokens": {"--ease-out": "cubic-bezier(0.16, 1, 0.3, 1)", ...}}

get_voice_rules()
  -> {"voice": "Terse, imperative, technical. ...",
      "protected_vocabulary": [{"term": "Dispatch", "usage": "The newsletter. Never \"newsletter\"."}, ...],
      "forbidden_patterns": ["\"Solutions\" (say systems)", ...]}

check_voice("Our solutions transform your business!")
  -> {"clean": false, "findings": [
        {"type": "replace_term",     "match": "solutions",              "suggestion": "use \"Systems\""},
        {"type": "forbidden_phrase", "match": "Transform your business", "suggestion": "remove / rewrite ..."},
        {"type": "punctuation",      "match": "!",                       "suggestion": "state it flat ..."}]}

is_allowed_word("newsletter")
  -> {"allowed": false, "correct_term": "Dispatch", "note": "off-brand — use \"Dispatch\""}

get_logo("isotipo-rojo")
  -> {"variant": "isotipo-rojo", "format": "svg",
      "relative_path": "assets/isotipo/svg/aglaya-isotipo-rojo.svg", "exists": true}

get_nonnegotiables()
  -> {"source": "SKILL.md", "rules": ["`AGLAYA` always UPPERCASE.", "Zero border-radius. ...", ...]}
```

## Verify

```bash
./.venv/bin/python selftest.py       # spawns the server over stdio, calls every tool
./.venv/bin/python zerocopy_test.py  # edits a token mid-session, proves live read, restores
```

## Files

- `server.py` — FastMCP server, stdio transport (the 7 tools)
- `brand.py` — sovereign, dependency-free core (all file reading + parsing)
- `selftest.py` — end-to-end MCP client test
- `zerocopy_test.py` — live-read proof
- `pyproject.toml` — declares the single dependency (`mcp`)
