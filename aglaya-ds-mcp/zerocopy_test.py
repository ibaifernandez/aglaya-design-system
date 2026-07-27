"""ZERO-COPY proof: within ONE live MCP session, edit the canonical CSS and show
get_token returns the new value with NO server restart and NO code change — then
restore the file byte-for-byte. Run: ./.venv/bin/python zerocopy_test.py
"""

import asyncio
import re
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

HERE = Path(__file__).resolve().parent
CSS = HERE.parent / "colors_and_type.css"
SENTINEL = "#1234ff"


def _val(res):
    import json

    sc = getattr(res, "structuredContent", None)
    if not sc:
        sc = json.loads(res.content[0].text)
    return sc.get("value", sc)


async def main() -> int:
    original = CSS.read_text(encoding="utf-8")
    assert "--color-brand:" in original
    params = StdioServerParameters(command=sys.executable, args=[str(HERE / "server.py")])
    ok = False
    try:
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                before = _val(await session.call_tool("get_token", {"name": "color-brand"}))
                print("1. before edit        get_token(color-brand) ->", before)

                # Mutate the canonical file mid-session (no restart). The old
                # value comes from the call above, never typed here: a proof
                # that hardcodes the red breaks the day the red moves, and it
                # would be the last place anyone looks.
                edited, hits = re.subn(
                    r"(--color-brand\s*:\s*)[^;]+;",
                    lambda m: m.group(1) + SENTINEL + ";",
                    original,
                    count=1,
                )
                assert hits == 1, "no --color-brand declaration to mutate"
                CSS.write_text(edited, encoding="utf-8")
                print(f"2. edited CSS on disk (--color-brand -> {SENTINEL})")

                after = _val(await session.call_tool("get_token", {"name": "color-brand"}))
                print("3. after edit (SAME session) get_token(color-brand) ->", after)

                # Live-read means: the answer tracked the file, and it was not
                # already the sentinel by accident.
                ok = before != SENTINEL and after == SENTINEL
    finally:
        CSS.write_text(original, encoding="utf-8")
        vuelto = CSS.read_text(encoding="utf-8") == original
        print("4. restored file byte-for-byte ->", vuelto)
        if not vuelto:
            print("   !! el CSS canónico NO quedó como estaba — revísalo antes de nada")
            ok = False

    print("\nZERO-COPY PROOF:", "PASS ✓" if ok else "FAIL ✗")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
