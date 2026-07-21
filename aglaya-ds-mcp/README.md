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
| `list_tokens(category?)` | `colors_and_type.css` | all tokens, or one category — call it with no argument to see which categories exist |
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

## Response shapes

**These show the shape of each answer, never the answer.** A README that prints
`"value": "#e8003d"` is doing by hand exactly what this server exists to avoid —
and the day someone edits the CSS, this file says the old colour with the
confidence of a worked example. The whole point of the tool is that **only the
call knows the value**. Run them; the shapes below tell you what you'll get back.

```text
get_token("color-brand")
  -> {"token": "--color-brand", "value": <live from colors_and_type.css>}

list_tokens("motion")
  -> {"category": "motion", "count": <n>, "tokens": {<name>: <value>, ...}}

get_voice_rules()
  -> {"voice": <tone paragraph>,
      "protected_vocabulary": [{"term": <t>, "usage": <rule>}, ...],
      "forbidden_patterns": [<pattern>, ...]}                  # all live from README.md

check_voice(<text>)
  -> {"clean": <bool>, "findings": [
        {"type": "replace_term" | "forbidden_phrase" | "punctuation",
         "match": <offending fragment>, "suggestion": <on-brand fix>}, ...]}

is_allowed_word(<term>)
  -> {"allowed": <bool>, "correct_term": <replacement, if any>, "note": <why>}

get_logo(<variant>, <fmt?>)
  -> {"variant": <v>, "format": <fmt>, "relative_path": <path under assets/>,
      "exists": <bool>}

get_nonnegotiables()
  -> {"source": "SKILL.md", "rules": [<rule>, ...]}             # live from SKILL.md
```

> `check_voice` is a heuristic, not a parser. It matches surface patterns, so it
> can miss a violation or flag a clean phrase. Safety net, never final judge — if
> a finding looks wrong, read the rule it cites in `README.md` and decide there.
> No worked example of a known weakness lives here on purpose: the last one
> named a false positive that had been fixed for weeks, and a doc that teaches
> distrust of a working tool is worse than one that says nothing.

## Verify

```bash
./.venv/bin/python selftest.py       # spawns the server over stdio, calls every tool
./.venv/bin/python zerocopy_test.py  # edits a token mid-session, proves live read, restores
```

## Files

- `server.py` — FastMCP server, stdio transport. It declares the tools; this file
  does not count them.
- `brand.py` — sovereign, dependency-free core (all file reading + parsing)
- `selftest.py` — end-to-end MCP client test
- `zerocopy_test.py` — live-read proof
- `pyproject.toml` — declares the single dependency (`mcp`)
