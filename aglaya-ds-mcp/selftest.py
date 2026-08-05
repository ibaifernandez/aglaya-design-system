"""End-to-end MCP self-test: spawn server.py over stdio as a real MCP client,
list the tools, call every one, and CHECK each answer.

Why the checking matters, since this file used to skip it: a failing tool does
NOT raise. `session.call_tool` comes back with `isError=False` and a perfectly
ordinary payload of `{"error": "..."}`, because the server turns BrandError into
a clean dict on purpose. The old version printed that and exited 0. It could
only catch two things — a tool missing from the registry, and the transport
falling over — so every tool in the set could have been answering garbage and
this test would still have said PASS.

So each call declares what it expects:

  "ok"     the tool must answer without an error payload
  "falla"  the tool must REPORT an error (unknown token, unknown product…)

The second half is not decoration. A test that only asserts «nothing errored»
is passed trivially by a server that never errors, and the tools whose whole
job is to reject a bad id would be the ones left unprotected.

Run: ./.venv/bin/python selftest.py     ·     Exit: 0 all good · 1 failures.
"""

import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

HERE = Path(__file__).resolve().parent

ESPERADAS = {
    "get_token", "list_tokens", "get_voice_rules", "check_voice",
    "is_allowed_word", "get_logo", "get_nonnegotiables",
    "list_products", "get_product", "get_accent", "get_glyph",
    "get_lockup", "get_product_voice",
    "list_components", "get_component",
}

# (tool, args, veredicto)  ·  veredicto: "ok" responde · "falla" debe rechazar
LLAMADAS = [
    ("get_token", {"name": "color-brand"}, "ok"),
    ("get_token", {"name": "--space-8"}, "ok"),
    ("get_token", {"name": "product-legal-reg-tech-accent"}, "ok"),
    ("get_token", {"name": "no-existe-este-token"}, "falla"),
    ("list_tokens", {"category": "color"}, "ok"),
    ("list_tokens", {"category": "product"}, "ok"),
    ("list_tokens", {}, "ok"),
    ("list_tokens", {"category": "categoria-inventada"}, "falla"),
    ("get_voice_rules", {}, "ok"),
    ("check_voice", {"text": "Our solutions transform your business!"}, "ok"),
    ("is_allowed_word", {"term": "newsletter"}, "ok"),
    ("is_allowed_word", {"term": "Sovereignty"}, "ok"),
    ("get_logo", {"variant": "isotipo-rojo"}, "ok"),
    ("get_logo", {"variant": "logotipo-white"}, "ok"),
    ("get_logo", {"variant": "isotipo-fucsia"}, "falla"),
    ("get_logo", {"variant": "mascota-rojo"}, "falla"),
    ("get_nonnegotiables", {}, "ok"),
    ("get_nonnegotiables", {"scope": "product"}, "ok"),
    ("get_nonnegotiables", {"scope": "ni-madre-ni-producto"}, "falla"),
    ("list_products", {}, "ok"),
    ("get_product", {"id": "legal-reg-tech"}, "ok"),
    ("get_product", {"id": "nave-que-no-existe"}, "falla"),
    ("get_accent", {"id": "orchestrator"}, "ok"),
    ("get_glyph", {"id": "design-system", "variant": "accent"}, "ok"),
    ("get_glyph", {"id": "kanban-desk", "variant": "fill"}, "ok"),
    ("get_glyph", {"id": "kanban-desk", "variant": "variante-inventada"}, "falla"),
    ("get_lockup", {"id": "consent-flow", "layout": "stacked"}, "ok"),
    ("get_lockup", {"id": "crm", "layout": "diagonal"}, "falla"),
    ("get_product_voice", {"id": "crm"}, "ok"),
    ("list_components", {}, "ok"),
    ("get_component", {"id": "button"}, "ok"),
    ("get_component", {"id": "carousel"}, "falla"),
]


def _payload(result):
    """Extract the structured/text content from a CallToolResult."""
    if getattr(result, "structuredContent", None):
        return result.structuredContent
    partes = [getattr(c, "text", str(c)) for c in result.content]
    crudo = "\n".join(partes)
    try:
        return json.loads(crudo)
    except (json.JSONDecodeError, TypeError):
        return crudo


def _es_error(payload) -> bool:
    """¿Este payload es un rechazo? `_guard` en server.py devuelve {"error": …};
    FastMCP puede envolverlo en {"result": {...}}. Se miran las dos formas."""
    if isinstance(payload, dict):
        if "error" in payload:
            return True
        interior = payload.get("result")
        if isinstance(interior, dict) and "error" in interior:
            return True
        return False
    return isinstance(payload, str) and '"error"' in payload


async def main() -> int:
    params = StdioServerParameters(
        command=sys.executable, args=[str(HERE / "server.py")]
    )
    fallos = []
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            nombres = sorted(t.name for t in tools.tools)
            print("== TOOLS REGISTERED ==")
            print(nombres, "\n")

            faltan = ESPERADAS - set(nombres)
            if faltan:
                print("!! MISSING TOOLS:", sorted(faltan))
                return 1
            sobran = set(nombres) - ESPERADAS
            if sobran:
                # Sin esto, una tool nueva entra a la flota sin que nadie la
                # haya llamado nunca — y el verde de este archivo la avalaría.
                print("!! tools sin probar (añádelas a LLAMADAS):", sorted(sobran), "\n")
                fallos.append(f"tools sin cobertura: {sorted(sobran)}")

            for nombre, args, veredicto in LLAMADAS:
                res = await session.call_tool(nombre, args)
                out = _payload(res)
                erroneo = bool(getattr(res, "isError", False)) or _es_error(out)
                etiqueta = f"{nombre}({json.dumps(args, ensure_ascii=False)})"

                if veredicto == "ok" and erroneo:
                    fallos.append(f"{etiqueta} debía responder y devolvió error")
                    marca = "FALLO"
                elif veredicto == "falla" and not erroneo:
                    fallos.append(f"{etiqueta} debía rechazar y respondió como si nada")
                    marca = "FALLO"
                else:
                    marca = "ok" if veredicto == "ok" else "rechaza"

                print(f"== [{marca}] {etiqueta} ==")
                print(
                    json.dumps(out, ensure_ascii=False, indent=2)
                    if isinstance(out, (dict, list))
                    else out
                )
                print()

            # El vocabulario protegido vive en DOS tablas del README, una por
            # idioma, y su ENCABEZADO es el único anclaje. Renómbralo, o
            # cámbiale la raya larga por un guion, y el castellano desaparece
            # del MCP sin que nada se ponga rojo: get_voice_rules responde
            # igual de contenta con media tabla, así que el veredicto ok/falla
            # de arriba no lo caza. Se comprueba el CONTENIDO.
            reglas = _payload(await session.call_tool("get_voice_rules", {}))
            vocab = reglas.get("protected_vocabulary", []) if isinstance(reglas, dict) else []
            idiomas = {t.get("lang") for t in vocab if isinstance(t, dict)}
            for esperado in ("en", "es"):
                if esperado not in idiomas:
                    fallos.append(
                        f"get_voice_rules no sirve vocabulario '{esperado}' — "
                        "¿se renombró su tabla en el README?"
                    )

            # Y que la tabla se parsee no basta: sus vetos tienen que morder.
            veto = _payload(await session.call_tool("is_allowed_word", {"term": "soluciones"}))
            if not isinstance(veto, dict) or veto.get("allowed") is not False:
                fallos.append("is_allowed_word('soluciones') debía vetarse y no lo hace")

            # Una fila puede declarar VARIAS formas del mismo término
            # ("Sovereignty / Sovereign", "soberanía / soberano"), y la tool
            # registraba solo la primera: preguntar por la segunda devolvía
            # "neutral" sobre una palabra protegida. Se comprueban TODAS las
            # formas de TODAS las filas, en los dos idiomas.
            #
            # Las formas se leen de lo que sirve el propio servidor, no de una
            # lista tecleada aquí: una lista a mano se queda corta el día que
            # alguien añada un par al README, y este archivo daría verde.
            formas = 0
            for entrada in vocab:
                if not isinstance(entrada, dict):
                    continue
                for forma in entrada.get("forms", []):
                    res_f = _payload(
                        await session.call_tool("is_allowed_word", {"term": forma})
                    )
                    if not isinstance(res_f, dict) or not res_f.get("protected"):
                        fallos.append(
                            f"is_allowed_word({forma!r}) debía ser término protegido "
                            f"y no lo es — ¿se registró solo la primera forma del par?"
                        )
                    formas += 1
            if not formas:
                fallos.append("ninguna forma de término protegido llegó a comprobarse")

            print(
                f"== [contenido] vocabulario servido en: {sorted(i for i in idiomas if i)}"
                f" · {formas} forma(s) consultable(s) ==\n"
            )

    print("─" * 60)
    if fallos:
        print(f"SELFTEST: {len(fallos)} fallo(s)")
        for f in fallos:
            print("  ·", f)
        return 1
    print(f"SELFTEST: {len(LLAMADAS)} llamadas, todas con el veredicto esperado ✓")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
