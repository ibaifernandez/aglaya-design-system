#!/usr/bin/env node
/**
 * Deriva las formas JS/JSON de los tokens desde `colors_and_type.css`.
 *
 * Por qué esto NO se versiona. El CSS canónico es la única casa de un valor de
 * marca en este repo — `tools/guard_valores.py` falla si un valor aparece
 * escrito a mano en cualquier otro archivo versionado. Un `tokens.json`
 * commiteado sería exactamente esa segunda casa: envejece en silencio, y el día
 * que el rojo se mueva sigue sirviendo el rojo viejo con cara de canon. Así que
 * `dist/` se genera en cada instalación (npm corre `prepare` también cuando la
 * dependencia viene de git) y está en `.gitignore`. Un clon limpio no trae ni
 * un valor duplicado: los fabrica leyendo el CSS.
 *
 * El nombre del token NO se traduce. La clave es `--color-brand`, no
 * `colorBrand`. Un segundo vocabulario es un segundo sitio donde discrepar, y
 * la deriva que este paquete existe para cerrar empezó justo así: el mismo
 * nombre significando cosas distintas en dos repos.
 *
 * Sin dependencias: Node y nada más, igual que el resto de la nave.
 *
 * Uso:  node scripts/build-tokens.mjs
 */

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const RAIZ = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const CSS = resolve(RAIZ, "colors_and_type.css");
const DIST = resolve(RAIZ, "dist");

// Mismo recorte que usan el MCP (`brand.py:_all_tokens`) y el guardián de
// valores. Si los tres no coinciden, el paquete puede publicar un token que el
// MCP no sirve — y nadie se entera hasta que un consumidor lo pide.
const ROOT = /:root\s*\{(.*?)\}/s;
const DECL = /--([a-zA-Z0-9-]+)\s*:\s*([^;]+);/g;

function leerTokens() {
  const css = readFileSync(CSS, "utf8");
  const bloque = ROOT.exec(css);
  if (!bloque) {
    throw new Error(`no encontré el bloque :root en ${CSS}`);
  }
  const tokens = {};
  for (const [, nombre, valor] of bloque[1].matchAll(DECL)) {
    tokens[`--${nombre}`] = valor.trim();
  }
  if (Object.keys(tokens).length === 0) {
    // Un build vacío es peor que un build roto: publica un paquete que
    // resuelve a nada y el consumidor pinta transparente sin ver un error.
    throw new Error(`el bloque :root de ${CSS} no declaró ni un token`);
  }
  return tokens;
}

function version() {
  return JSON.parse(readFileSync(resolve(RAIZ, "package.json"), "utf8")).version;
}

const tokens = leerTokens();
const v = version();

mkdirSync(DIST, { recursive: true });

writeFileSync(
  resolve(DIST, "tokens.json"),
  JSON.stringify({ source: "colors_and_type.css", version: v, tokens }, null, 2) + "\n",
);

writeFileSync(
  resolve(DIST, "tokens.js"),
  [
    "// GENERADO por scripts/build-tokens.mjs desde colors_and_type.css.",
    "// No lo edites: se reescribe en cada instalación y no se versiona.",
    `export const version = ${JSON.stringify(v)};`,
    `export const tokens = ${JSON.stringify(tokens, null, 2)};`,
    "export default tokens;",
    "",
  ].join("\n"),
);

writeFileSync(
  resolve(DIST, "tokens.d.ts"),
  [
    "// GENERADO por scripts/build-tokens.mjs. No lo edites.",
    "export declare const version: string;",
    "export declare const tokens: Record<string, string>;",
    "export default tokens;",
    "",
  ].join("\n"),
);

console.log(
  `build-tokens: ${Object.keys(tokens).length} token(s) desde colors_and_type.css -> dist/ (v${v})`,
);
