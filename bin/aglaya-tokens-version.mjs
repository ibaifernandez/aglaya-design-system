#!/usr/bin/env node
/**
 * Imprime cuántas versiones por detrás va el consumidor.
 *
 * Esta es la ventaja entera de depender en vez de copiar, y no llega sola:
 * copiar tampoco duele el primer día — duele siete semanas después, cuando
 * `--color-surface-2` ya significa dos cosas distintas y nadie sabe desde
 * cuándo. Un consumidor que copia no tiene forma de preguntar «¿voy atrasado?».
 * Uno que depende, sí, y esto es esa forma: un comando, desde su repo, sin
 * clonar el nuestro.
 *
 *   npx aglaya-tokens-version            → humano
 *   npx aglaya-tokens-version --json     → para un paso de CI
 *   npx aglaya-tokens-version --strict   → sale 1 si va por detrás (gate de CI)
 *
 * Salidas: 0 al día (o atrasado sin --strict) · 1 atrasado con --strict
 *          · 2 no se pudo comprobar (sin git, sin red, sin tags).
 *
 * El 2 importa: «no pude mirar» NUNCA se imprime como «estás al día». Ese es
 * el verde vacío que desactiva una comprobación el primer día que falla la red.
 */

import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const PKG = resolve(AQUI, "..", "package.json");

const args = new Set(process.argv.slice(2));
const JSON_OUT = args.has("--json");
const STRICT = args.has("--strict");

function salir(codigo, humano, datos) {
  if (JSON_OUT) console.log(JSON.stringify(datos, null, 2));
  else console.log(humano);
  process.exit(codigo);
}

function fallo(mensaje, datos = {}) {
  salir(2, `aglaya-tokens-version: no se pudo comprobar — ${mensaje}`, {
    ok: false,
    error: mensaje,
    ...datos,
  });
}

// ── semver, lo justo ────────────────────────────────────────────────────────
// Solo se comparan versiones de release. Un tag con pre-release (`v2.0.0-rc.1`)
// se ignora a propósito: publicar un candidato no deja atrasado a nadie.
const SEMVER = /^v?(\d+)\.(\d+)\.(\d+)$/;

const parse = (s) => {
  const m = SEMVER.exec(s.trim());
  return m ? [Number(m[1]), Number(m[2]), Number(m[3])] : null;
};
const cmp = (a, b) => a[0] - b[0] || a[1] - b[1] || a[2] - b[2];
const fmt = (v) => v.join(".");

// ── de dónde salen los datos ────────────────────────────────────────────────
let pkg;
try {
  pkg = JSON.parse(readFileSync(PKG, "utf8"));
} catch (e) {
  fallo(`no pude leer ${PKG}: ${e.message}`);
}

const instalada = parse(pkg.version ?? "");
if (!instalada) fallo(`la versión instalada no es semver: ${pkg.version}`);

const bruta = pkg.repository?.url ?? "";
// `git+https://host/x.git` -> `https://host/x.git`. Un `git@host:x.git` (SSH)
// no se traduce: si el paquete se publicó con URL SSH, el consumidor no puede
// consultarla sin llaves, y eso es un fallo del publicador, no del consumidor.
const remoto = bruta.replace(/^git\+/, "");
if (!/^https:\/\//.test(remoto)) {
  fallo(`repository.url no es https y un CI ajeno no podrá consultarla: ${bruta || "(vacía)"}`);
}

let salida;
try {
  salida = execFileSync("git", ["ls-remote", "--tags", "--refs", remoto], {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
    timeout: 20_000,
    env: { ...process.env, GIT_TERMINAL_PROMPT: "0" },
  });
} catch (e) {
  fallo(`git ls-remote falló sobre ${remoto} (${e.code ?? e.message})`, { remote: remoto });
}

const publicadas = salida
  .split("\n")
  .map((l) => l.split("refs/tags/")[1])
  .filter(Boolean)
  .map(parse)
  .filter(Boolean)
  .sort(cmp);

if (publicadas.length === 0) {
  fallo(`el remoto no publica ningún tag de versión: ${remoto}`, { remote: remoto });
}

const ultima = publicadas[publicadas.length - 1];
const detras = publicadas.filter((v) => cmp(v, instalada) > 0);

// Un mayor por delante no es «vas dos versiones tarde»: es «te van a romper
// nombres de token». Se dice aparte porque la acción es distinta — leer el
// contrato antes de subir, no subir y ver qué pasa.
const mayorPorDelante = detras.some((v) => v[0] > instalada[0]);

const datos = {
  ok: true,
  package: pkg.name,
  installed: fmt(instalada),
  latest: fmt(ultima),
  behind: detras.length,
  behindVersions: detras.map(fmt),
  majorAhead: mayorPorDelante,
  remote: remoto,
};

if (detras.length === 0) {
  const adelantada = cmp(instalada, ultima) > 0;
  salir(
    0,
    adelantada
      ? `${pkg.name} ${fmt(instalada)} — por delante del último tag publicado (${fmt(ultima)}). Estás sobre una rama sin taggear.`
      : `${pkg.name} ${fmt(instalada)} — al día (último publicado: ${fmt(ultima)}).`,
    { ...datos, ahead: adelantada },
  );
}

const lineas = [
  `${pkg.name} ${fmt(instalada)} — ${detras.length} versión(es) por detrás.`,
  `  último publicado: ${fmt(ultima)}`,
  `  te faltan:        ${detras.map(fmt).join(", ")}`,
];
if (mayorPorDelante) {
  lineas.push(
    "  AVISO: hay un MAYOR por delante — algún token cambió de nombre o desapareció.",
    "         Lee docs/PACKAGE.md del repo antes de subir; el build puede romperse.",
  );
}
salir(STRICT ? 1 : 0, lineas.join("\n"), datos);
