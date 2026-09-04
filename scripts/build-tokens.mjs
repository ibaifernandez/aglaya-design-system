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

// Los modos de color viven en el mismo CSS, cada uno bajo su selector, y
// redefinen los MISMOS nombres de token. Aquí solo se declara dónde mirar: los
// valores se leen del CSS como todo lo demás, ni uno se teclea en este script.
// Esa es la línea que separa este repo de una copia vendorizada, y es lo que
// prueba tools/test_mutacion.sh.
const MODOS = {
  light: /\[data-theme="light"\]\s*\{(.*?)\n\}/s,
};

// Los comentarios se quitan ANTES de parsear. El bloque del modo claro lleva
// dentro las cifras de contraste que justifican cada alfa, y sin esto una línea
// de comentario podría colarse como token — un valor de marca inventado por un
// comentario es exactamente la clase de mentira que este paquete existe para
// impedir. Comprobado que sobre `:root` no cambia nada: los mismos 87.
const sinComentarios = (s) => s.replace(/\/\*[\s\S]*?\*\//g, "");

function declaraciones(bloque, etiqueta) {
  const tokens = {};
  for (const [, nombre, valor] of sinComentarios(bloque).matchAll(DECL)) {
    tokens[`--${nombre}`] = valor.trim();
  }
  if (Object.keys(tokens).length === 0) {
    // Un build vacío es peor que un build roto: publica un paquete que
    // resuelve a nada y el consumidor pinta transparente sin ver un error.
    throw new Error(`el bloque ${etiqueta} de ${CSS} no declaró ni un token`);
  }
  return tokens;
}

function leerTokens() {
  const css = readFileSync(CSS, "utf8");
  const bloque = ROOT.exec(css);
  if (!bloque) {
    throw new Error(`no encontré el bloque :root en ${CSS}`);
  }
  return declaraciones(bloque[1], ":root");
}

function leerModos(base) {
  const css = readFileSync(CSS, "utf8");
  const modos = {};
  for (const [nombre, patron] of Object.entries(MODOS)) {
    const bloque = patron.exec(css);
    if (!bloque) {
      // Silencio no: un modo declarado aquí y ausente del CSS saldría del build
      // como si no existiera, y el consumidor lo pediría y recibiría undefined.
      throw new Error(`no encontré el bloque del modo '${nombre}' en ${CSS}`);
    }
    const tokens = declaraciones(bloque[1], `modo '${nombre}'`);
    // Un modo REDEFINE; no inventa. Un nombre que no exista en :root sería un
    // token que solo vive en un modo — media marca, y nadie se enteraría.
    const huerfanos = Object.keys(tokens).filter((t) => !(t in base));
    if (huerfanos.length) {
      throw new Error(
        `el modo '${nombre}' declara tokens que no existen en :root: ${huerfanos.join(", ")}`,
      );
    }
    modos[nombre] = tokens;
  }
  return modos;
}

function version() {
  return JSON.parse(readFileSync(resolve(RAIZ, "package.json"), "utf8")).version;
}

const tokens = leerTokens();
const modes = leerModos(tokens);
const v = version();

mkdirSync(DIST, { recursive: true });

// `tokens` NO cambia de forma ni de contenido: sigue siendo el mapa plano con
// los valores del modo por defecto, que son los de siempre. Quien lo lea hoy no
// nota absolutamente nada, y por eso esto es MENOR y no MAYOR — docs/PACKAGE.md
// declara mayor cambiar de forma una vía de exports, menor añadir.
//
// El modo claro viaja en `modes`, una clave hermana. El nombre es interfaz en
// cuanto se publique, así que se elige una vez y se razona: `tokens` es la base
// y el defecto; `modes.<nombre>` lleva SOLO lo que ese modo redefine. Un modo
// nuevo mañana entra dentro sin cambiar la forma — con una clave `light` suelta
// habría que añadir otra hermana cada vez, y renombrar cuesta a cada consumidor.
//
// Para tener un modo completo se compone: { ...tokens, ...modes.light }.
writeFileSync(
  resolve(DIST, "tokens.json"),
  JSON.stringify({ source: "colors_and_type.css", version: v, tokens, modes }, null, 2) + "\n",
);

writeFileSync(
  resolve(DIST, "tokens.js"),
  [
    "// GENERADO por scripts/build-tokens.mjs desde colors_and_type.css.",
    "// No lo edites: se reescribe en cada instalación y no se versiona.",
    `export const version = ${JSON.stringify(v)};`,
    `export const tokens = ${JSON.stringify(tokens, null, 2)};`,
    "// Solo lo que cada modo REDEFINE. Modo completo: { ...tokens, ...modes.light }.",
    `export const modes = ${JSON.stringify(modes, null, 2)};`,
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
    "export declare const modes: Record<string, Record<string, string>>;",
    "export default tokens;",
    "",
  ].join("\n"),
);

const resumen = Object.entries(modes)
  .map(([n, t]) => `${n}: ${Object.keys(t).length}`)
  .join(", ");
console.log(
  `build-tokens: ${Object.keys(tokens).length} token(s) desde colors_and_type.css ` +
    `-> dist/ (v${v}) · modos [${resumen}]`,
);
