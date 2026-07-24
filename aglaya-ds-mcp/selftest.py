"""End-to-end MCP self-test: spawn server.py over stdio as a real MCP client,
list tools, and call each one. Proves registration + transport, not just the
core functions. Run: ./.venv/bin/python selftest.py
"""

import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

HERE = Path(__file__).resolve().parent


def _payload(result):
    """Extract the structured/text content from a CallToolResult."""
    if getattr(result, "structuredContent", None):
        return result.structuredContent
    parts = []
    for c in result.content:
        parts.append(getattr(c, "text", str(c)))
    return "\n".join(parts)


async def main() -> int:
    params = StdioServerParameters(
        command=sys.executable, args=[str(HERE / "server.py")]
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            names = sorted(t.name for t in tools.tools)
            print("== TOOLS REGISTERED ==")
            print(names, "\n")

            expected = {
                "get_token", "list_tokens", "get_voice_rules", "check_voice",
                "is_allowed_word", "get_logo", "get_nonnegotiables",
                "list_products", "get_product", "get_accent", "get_glyph",
                "get_lockup", "get_product_voice",
                "list_components", "get_component",
            }
            missing = expected - set(names)
            if missing:
                print("!! MISSING TOOLS:", sorted(missing))
                return 1

            calls = [
                ("get_token", {"name": "color-brand"}),
                ("get_token", {"name": "--space-8"}),
                ("get_token", {"name": "product-legal-reg-tech-accent"}),
                ("list_tokens", {"category": "color"}),
                ("list_tokens", {"category": "product"}),
                ("get_voice_rules", {}),
                ("check_voice", {"text": "Our solutions transform your business!"}),
                ("is_allowed_word", {"term": "newsletter"}),
                ("is_allowed_word", {"term": "Sovereignty"}),
                ("get_logo", {"variant": "isotipo-rojo"}),
                ("get_logo", {"variant": "logotipo-white"}),
                ("get_nonnegotiables", {}),
                ("get_nonnegotiables", {"scope": "product"}),
                ("list_products", {}),
                ("get_product", {"id": "legal-reg-tech"}),
                ("get_accent", {"id": "orchestrator"}),
                ("get_glyph", {"id": "design-system", "variant": "accent"}),
                ("get_glyph", {"id": "kanban-desk", "variant": "fill"}),
                ("get_lockup", {"id": "consent-flow", "layout": "stacked"}),
                ("get_product_voice", {"id": "crm"}),
                ("list_components", {}),
                ("get_component", {"id": "button"}),
            ]
            for name, args in calls:
                res = await session.call_tool(name, args)
                out = _payload(res)
                print(f"== {name}({json.dumps(args)}) ==")
                print(
                    json.dumps(out, ensure_ascii=False, indent=2)
                    if isinstance(out, (dict, list))
                    else out
                )
                print()
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
