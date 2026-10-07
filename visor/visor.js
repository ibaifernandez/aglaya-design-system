/* El visor, por dentro. Todo lo que pinta viene de /api/*, que a su vez viene
 * de aglaya-ds-mcp/brand.py — el mismo lector que usa el MCP. Aquí no hay ni
 * un valor de marca escrito: si una sección no tiene datos, se queda vacía y
 * lo dice, en vez de rellenarse con algo plausible.
 *
 * El contraste SÍ se calcula aquí, y a propósito en un solo sitio: con los
 * valores que el canon acaba de servir. Dos calculadoras del mismo número son
 * dos números que algún día discrepan.
 */

const SUELO = 4.5;   // el suelo de texto; el canon lo declara como suelo, no veredicto

const pedir = (ruta) => fetch(ruta, { cache: "no-store" }).then((r) => r.json());

// ── color ───────────────────────────────────────────────────────────────────
const canal = (v) => {
  v /= 255;
  return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
};
const luminancia = ([r, g, b]) => 0.2126 * canal(r) + 0.7152 * canal(g) + 0.0722 * canal(b);
const contraste = (f, b) => {
  const [a, c] = [luminancia(f), luminancia(b)];
  const [hi, lo] = a > c ? [a, c] : [c, a];
  return (hi + 0.05) / (lo + 0.05);
};

/* Resuelve un valor del canon a [r,g,b,alfa], siguiendo var() dentro del mismo
 * mapa de tokens. Devuelve null si no es un color — y entonces no se inventa
 * nada: la fila se enseña sin muestra. */
function aRGB(valor, tokens, visto = []) {
  if (!valor) return null;
  const v = String(valor).trim();
  const ref = v.match(/^var\((--[\w-]+)\)$/);
  if (ref) {
    if (visto.includes(ref[1]) || !(ref[1] in tokens)) return null;
    return aRGB(tokens[ref[1]], tokens, [...visto, ref[1]]);
  }
  const hex = v.match(/^#([0-9a-f]{3}|[0-9a-f]{6})$/i);
  if (hex) {
    const h = hex[1].length === 3 ? [...hex[1]].map((c) => c + c).join("") : hex[1];
    return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16), 1];
  }
  const rgb = v.match(/^rgba?\(([^)]+)\)$/i);
  if (rgb) {
    const p = rgb[1].split(",").map((x) => parseFloat(x));
    if (p.length >= 3) return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1];
  }
  const mix = v.match(/^color-mix\(in srgb,\s*(.+?)\s+([\d.]+)%,\s*transparent\)$/i);
  if (mix) {
    const base = aRGB(mix[1], tokens, visto);
    if (base) return [base[0], base[1], base[2], base[3] * (parseFloat(mix[2]) / 100)];
  }
  return null;
}

const componer = (c, fondo) =>
  [0, 1, 2].map((i) => Math.round(c[i] * c[3] + fondo[i] * (1 - c[3]))).concat(1);

// ── pintar ──────────────────────────────────────────────────────────────────
const el = (sel) => document.querySelector(sel);
const esc = (t) => String(t).replace(/[<>&]/g, (c) => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;" }[c]));
const conCodigo = (t) => esc(t).replace(/`([^`]+)`/g, "<code>$1</code>")
                               .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");

function pintarNormas(d) {
  const lista = (r) => (r && (r.rules || r.items || r)) || [];
  for (const [id, datos] of [["#nn-madre", d.no_negociables_madre], ["#nn-producto", d.no_negociables_producto]]) {
    const reglas = lista(datos);
    el(id).innerHTML = reglas.length
      ? reglas.map((x) => `<li>${conCodigo(typeof x === "string" ? x : JSON.stringify(x))}</li>`).join("")
      : "<li>el canon no devolvió ninguna regla para este ámbito</li>";
  }
  el("#procedencia").textContent =
    `normas y valores leídos de ${d.no_negociables_madre?.source || "docs/BRAND-RULES.md"} ` +
    `y de colors_and_type.css, a través de aglaya-ds-mcp/brand.py, en esta misma recarga.`;
}

/* Rótulos en castellano de los bloques que devuelve `get_voice_rules`. Las
 * claves de la API están en inglés y en minúscula, y hasta hoy se enseñaban
 * crudas: «voice», «evidence», «protected_vocabulary», con el contenido en
 * castellano debajo. Esto NO traduce contenido —el contenido es del canon— ni
 * decide nada: solo pone nombre al cajón. Una clave que no esté aquí se enseña
 * tal cual y se nota, en vez de desaparecer. */
const ROTULO = {
  voice: "Voz",
  evidence: "Evidencia",
  shape: "Forma",
  pronouns: "Pronombres",
  casing: "Mayúsculas",
  protected_vocabulary: "Vocabulario protegido",
  forbidden_patterns: "Frases vetadas",
  final_check: "Comprobación final",

  // Y los campos de las fichas de componente y de los acentos de producto, que
  // también se enseñaban con su clave inglesa. Mismo criterio: esto nombra el
  // cajón, no toca el contenido. Lo que no esté aquí sale con su clave y se ve.
  id: "Identificador",
  name: "Nombre",
  use: "Para qué",
  specimen: "Muestra",
  tokens: "Tokens que usa",
  variants: "Variantes",
  spec: "Especificación",
  states: "Estados",
  rules: "Reglas",
  signature: "Rasgo de firma",
  label_convention: "Convención de rótulo",
  background: "Fondo",
  color: "Color",
  border: "Borde",
  padding: "Relleno",
  radius: "Radio",
  font: "Tipografía",
  title: "Título",
  body: "Cuerpo",
  label: "Etiqueta",
  rule: "Filete",
  dot: "Punto",
  adornment: "Adorno",
  hover: "Al pasar el ratón",
  focus: "Al enfocar",
  textarea: "Área de texto",
  index_eyebrow: "Antetítulo de índice",
  "letter-spacing": "Espaciado entre letras",
  "text-transform": "Caja del texto",
  product: "Producto",
  token: "Token",
  hex: "Hexadecimal",
  oklch: "OKLCH",
  css_value: "Valor CSS",
  secondary: "Secundario",

  // Del vocabulario protegido. `button`, `card` y compañía NO entran aquí: no
  // son claves de la API, son el nombre del componente — dato, no rótulo.
  term: "Término",
  forms: "Formas",
  lang: "Idioma",
  usage: "Uso",
};

function pintarVoz(voz) {
  const cuerpo = el("#voz-cuerpo");
  cuerpo.innerHTML = "";
  for (const [clave, valor] of Object.entries(voz || {})) {
    const caja = document.createElement("div");
    caja.className = "ficha";
    caja.innerHTML =
      `<h3 class="rotulo">${esc(ROTULO[clave] || clave)}</h3>` + comoTexto(valor);
    cuerpo.appendChild(caja);
  }
}

/* Pinta cualquier cosa que devuelva el canon como lo que es —lista, ficha de
 * campos o prosa— y NUNCA como bloque de código. Un `pre` no parte líneas: por
 * eso cada tarjeta traía su barra horizontal. */
function comoTexto(valor) {
  if (valor === null || valor === undefined) return "";
  if (Array.isArray(valor)) {
    return `<ul class="reglas">${valor.map((x) => `<li>${comoTexto(x)}</li>`).join("")}</ul>`;
  }
  if (typeof valor === "object") {
    return `<dl>${Object.entries(valor).map(([k, v]) =>
      `<div class="campo"><dt>${esc(ROTULO[k] || k)}</dt><dd>${comoTexto(v)}</dd></div>`).join("")}</dl>`;
  }
  return conCodigo(String(valor));
}

function filaColor(nombre, claro, oscuro) {
  const muestra = (modo) =>
    `<span class="muestra" style="background: var(${nombre})" data-modo-muestra="${modo}"></span>`;
  return `<tr>
    <td><code>${esc(nombre)}</code></td>
    <td><code>${esc(oscuro)}</code></td>
    <td><code>${esc(claro)}</code></td>
    <td>${muestra("ambos")}</td>
  </tr>`;
}

function pintarValores(d) {
  const oscuro = d.oscuro.tokens, claro = d.claro.tokens;
  const nombres = Object.keys(oscuro);

  const esColor = (n) => aRGB(oscuro[n], oscuro) !== null;
  const colores = nombres.filter(esColor);
  el("#tabla-color").innerHTML =
    `<tr><th>token</th><th>oscuro</th><th>claro</th><th>muestra</th></tr>` +
    colores.map((n) => filaColor(n, claro[n], oscuro[n])).join("") +
    parejasDeTinta(oscuro, claro);

  const fuentes = nombres.filter((n) => n.startsWith("--font-"));
  el("#tipos").innerHTML = fuentes.map((n) => `
    <div class="tipo">
      <div class="nombre">${esc(n)} · <code>${esc(oscuro[n])}</code></div>
      <div style="font-family: var(${n}); font-size: 28px;">AGLAYA 0123 — el zorro marrón salta</div>
    </div>`).join("");

  const resto = nombres.filter((n) => !esColor(n) && !n.startsWith("--font-"));
  el("#tabla-resto").innerHTML =
    `<tr><th>token</th><th>oscuro</th><th>claro</th></tr>` +
    resto.map((n) => `<tr><td><code>${esc(n)}</code></td><td><code>${esc(oscuro[n])}</code></td><td><code>${esc(claro[n])}</code></td></tr>`).join("");
}

/* Las parejas que de verdad importan: tinta sobre fondo, en los dos modos, con
 * su número. Salen de los tokens semánticos del propio canon, no de una lista
 * escrita aquí.
 *
 * Y se emparejan como manda el canon, no todas contra todas. Las tintas
 * `--fg-on-*` son para RELLENOS —`--fg-on-brand` sobre el rojo de marca,
 * `--fg-on-accent` sobre el acento de un producto—, así que cruzarlas con las
 * superficies fabrica ocho parejas que nadie va a pintar nunca y las enseña en
 * rojo. Medido antes de corregirlo: ese cruce daba 1.03 para la tinta blanca
 * sobre fondo claro y 1.00 para la negra sobre fondo oscuro. Un visor que
 * enseña un fallo inventado es peor que uno que no mide: hace dudar del canon
 * que está bien. */
function parejasDeTinta(oscuro, claro) {
  const tintas = Object.keys(oscuro)
    .filter((n) => n.startsWith("--fg-") && !n.startsWith("--fg-on-"));
  const fondos = ["--color-bg", "--color-surface", "--color-surface-2", "--color-surface-3"]
    .filter((n) => n in oscuro);
  let html = `<tr><th>tinta sobre fondo</th><th>oscuro</th><th>claro</th><th></th></tr>`;

  const medir = (tok, t, f) => {
    const fondo = aRGB(tok[f], tok);
    let tinta = aRGB(tok[t], tok);
    if (!fondo || !tinta) return null;
    if (tinta[3] < 1) tinta = componer(tinta, fondo);
    const r = contraste(tinta, fondo);
    return { txt: r.toFixed(2), bajo: r < SUELO };
  };

  const fila = (etiqueta, o, c) => {
    if (!o && !c) return "";
    const celda = (x) => x ? `<td class="ratio ${x.bajo ? "bajo" : ""}">${x.txt}</td>` : "<td>—</td>";
    const aviso = (o && o.bajo) || (c && c.bajo) ? `por debajo del suelo (${SUELO})` : "";
    return `<tr><td>${etiqueta}</td>${celda(o)}${celda(c)}<td>${aviso}</td></tr>`;
  };

  for (const t of tintas) {
    for (const f of fondos) {
      html += fila(`<code>${esc(t)}</code> sobre <code>${esc(f)}</code>`,
                   medir(oscuro, t, f), medir(claro, t, f));
    }
  }

  // Tinta sobre RELLENO: cada `--fg-on-*` contra los rellenos que el canon le
  // asigna. El relleno es el mismo color en los dos modos, así que la columna
  // «claro» repite el número a propósito: eso es lo que dice el canon.
  const rellenos = [["--fg-on-brand", "--color-brand"]];
  for (const n of Object.keys(oscuro)) {
    if (/^--product-.*accent(-\d+)?$/.test(n)) {
      const tinta = n === "--product-consent-flow-accent" ? "--fg-on-brand" : "--fg-on-accent";
      rellenos.push([tinta, n]);
    }
  }
  for (const [t, f] of rellenos) {
    if (!(t in oscuro) || !(f in oscuro)) continue;
    html += fila(`<code>${esc(t)}</code> sobre relleno <code>${esc(f)}</code>`,
                 medir(oscuro, t, f), medir(claro, t, f));
  }
  return html;
}

function pintarFichas(comp, prod) {
  const fichas = comp.fichas || [];
  el("#componentes").innerHTML = fichas.length
    ? fichas.map((f) => {
        const { id, ...resto } = f;
        return `<div class="ficha"><h3 class="rotulo">${esc(id || "")}</h3>${comoTexto(resto)}</div>`;
      }).join("")
    : "<p class='aviso'>el canon no devolvió fichas</p>";

  const acentos = prod.acentos || [];
  el("#acentos").innerHTML =
    `<tr><th>producto</th><th>token</th><th>valor</th><th>muestra</th></tr>` +
    acentos.map((a) => `<tr>
      <td>${esc(a.product || a.id || "")}</td>
      <td><code>${esc(a.token || "")}</code></td>
      <td><code>${esc(a.hex || a.value || "")}</code></td>
      <td><span class="muestra" style="background: var(${esc(a.token || "--color-bg")})"></span></td>
    </tr>`).join("");
}

// ── modo y pestañas ─────────────────────────────────────────────────────────
function modo(nuevo) {
  document.documentElement.dataset.theme = nuevo;
  document.querySelector("[data-modo]").textContent = nuevo === "light" ? "claro" : "oscuro";
}

el("#modo").addEventListener("click", () =>
  modo(document.documentElement.dataset.theme === "light" ? "dark" : "light"));

document.querySelectorAll("[data-ir]").forEach((b) =>
  b.addEventListener("click", () => {
    document.querySelectorAll("[data-ir]").forEach((x) => x.classList.toggle("activa", x === b));
    document.querySelectorAll("main section").forEach((s) =>
      (s.hidden = s.id !== b.dataset.ir));
  }));

// ── arranque ────────────────────────────────────────────────────────────────
modo("dark");
Promise.all([pedir("/api/normas"), pedir("/api/valores"), pedir("/api/componentes"), pedir("/api/productos")])
  .then(([normas, valores, comp, prod]) => {
    pintarNormas(normas);
    pintarVoz(normas.voz);
    pintarValores(valores);
    pintarFichas(comp, prod);
  })
  .catch((e) => {
    document.querySelector("main").innerHTML =
      `<p class="aviso">el canon no se pudo leer: ${esc(e.message)}. ` +
      `No se enseña nada en su lugar: una página que rellena huecos es la copia que esto evita.</p>`;
  });
