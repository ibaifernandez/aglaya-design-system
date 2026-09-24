# Fase C — Cumplimiento legal

Auditoría `aglaya-design-system-2026-09-24-mariana` · commit auditado `17d95cc` · modo `report`.

## Cuadro de evidencias — Fase C

| Confianza    | Nº | % de la fase |
|--------------|----|--------------|
| PROVEN       | 3  | 75 %         |
| UNVERIFIABLE | 1  | 25 %         |
| **Total**    | **4** | 100 %     |

Fuente de la evidencia: code-read 2 · tool-external 1 (`gh api`) · manual-verification 0.

Salud: 75 % PROVEN, por encima del 60 %.

## Qué aplica y qué no

**Protección de datos (RGPD, Ley 21.719, LGPD, CCPA): no aplica.** Este repo no trata datos personales de nadie:
- no hay formularios que envíen nada;
- el del kit es una simulación: `setTimeout` y ningún envío (`ui_kits/website/Footer.jsx:8-13`);
- no hay cookies, almacenamiento ni analítica (grep vacío, fase A);
- el MCP responde por stdio a la sesión local y no guarda nada.

Por eso no aplican la política de privacidad, el registro de DPA, los endpoints de borrado y exportación, las bases legales, las TOM, la brecha en 72 h, la DPIA, el banner, la retención ni las transferencias (RGPD arts. 5–35 y capítulo V; Ley 21.719 art. 14 ter y capítulo V).

**Sí aplica la propiedad intelectual.** El repo es público (`evidencia/github-ajustes.txt`) y redistribuye material de terceros:
- tres familias tipográficas;
- tres librerías JavaScript;
- el concepto de marca de una persona ajena.

Además declara derechos sobre todo lo demás (`LICENSE`).

El rubric de severidad legal está escrito para protección de datos. Para derechos de autor y marcas se usa su misma escala: MEDIA para un hueco documental o de cumplimiento con arreglo trivial, y BAJA para lo que es mejora o necesita revisión legal para confirmarse.

## Tabla de hallazgos

| ID | Confianza | Dim | Hallazgo | Evidencia | Norma | Severidad | Esfuerzo |
|----|-----------|-----|----------|-----------|-------|-----------|----------|
| C-01 | PROVEN | licencias | Se redistribuyen React, ReactDOM y Babel (MIT) sin su licencia, bajo una `LICENSE` de «todos los derechos reservados» | `LICENSE:9-18`, cabeceras de `ui_kits/website/vendor/react.production.min.js:1-9` y `ui_kits/website/vendor/react-dom.production.min.js:1-9` | Licencia MIT (condición de aviso) | MEDIA | 0,5 h |
| C-02 | UNVERIFIABLE · NV_CREDENTIALS | marcas | ConsentFlow es un concepto de otra persona y `LICENSE` lo reclama como marca propia, sin constancia de cesión | `README.md:177`, `:186`, `products/products.json:72`, `:84`, `LICENSE:67-70` | Derecho de marca y de autor | — | — |
| C-03 | PROVEN | derechos de autor | Seis identidades figuran hechas por una IA y `LICENSE` reclama copyright sobre ellas | `products/products.json:15`, `:34`, `:53`, `:90`, `:110`, `:130`, `LICENSE:12-14` | Autoría humana (p. ej. LPI española, art. 5.1) | BAJA | revisión legal |
| C-04 | PROVEN | licencias | `LICENSE` dice «no se concede ningún permiso», pero publicar en GitHub ya concede ver y bifurcar | `LICENSE:27-34`, `evidencia/github-ajustes.txt` (`allow_forking: true`) | Términos de servicio de GitHub, sección D.5 | BAJA | 0,25 h |

**Recuento:** CRÍTICA 0 · ALTA 0 · MEDIA 1 · BAJA 2 · UNVERIFIABLE 1.

---

## Detalle

### C-01 · Código MIT redistribuido sin su licencia, y reclamado como propio

- **Qué pasa.** `ui_kits/website/vendor/` lleva React, ReactDOM y Babel standalone, las tres con licencia MIT.
  - Las cabeceras de React remiten a «the LICENSE file in the root directory of this source tree» (`ui_kits/website/vendor/react.production.min.js:1-9`, `ui_kits/website/vendor/react-dom.production.min.js:1-9`). En este repo, ese fichero es la licencia de AGLAYA.
  - Babel solo lleva avisos sueltos dentro del minificado.
  - En el repo no hay ningún texto de la licencia MIT.
- **Qué exige la MIT.** Incluir el aviso de copyright y el de permiso en todas las copias.
- **Qué dice la licencia de AGLAYA.** Cubre «everything in this repository EXCEPT the font software under `fonts/`», incluido «the UI kit under `ui_kits/`» (`LICENSE:9-18`). Es decir, reclama todos los derechos también sobre código de Meta y de los autores de Babel.
- **Contraste con lo que ya se hace bien.** El repo cuida esto al milímetro con las fuentes: tiene una licencia por familia y un guardián que las empareja (`tools/guard_paquete.py`). El kit no está en el paquete npm (no figura en `files` de `package.json`), pero el repo público ya es una redistribución.
- **Severidad.** MEDIA: incumplimiento de una licencia de terceros con arreglo trivial.
- **Arreglo.**
  - Poner junto a los minificados el texto de la licencia MIT de React y el de Babel, un fichero por proyecto.
  - Exceptuar `ui_kits/website/vendor/` en la sección 1 de `LICENSE`, igual que `fonts/`.
  - Si se quiere que no vuelva a pasar, extender a `vendor/` el emparejamiento de `guard_paquete`.

### C-02 · ConsentFlow: concepto ajeno reclamado como marca · UNVERIFIABLE (NV_CREDENTIALS)

- **Qué dice el repo.**
  - La identidad de ConsentFlow es «Mónica Montúfar's concept» (`README.md:177`, `:186`).
  - El manifiesto le atribuye la autoría del concepto (`products/products.json:72`, `:84`).
  - El CSS marca sus colores como suyos y «sacred» (`colors_and_type.css:63-64`).
  - `LICENSE` reclama como marcas del titular «the product names and their glyphs and lockups» (`LICENSE:67-70`), sin excepción para ConsentFlow.
- **Qué no consta.** En el repo no hay ninguna cesión, licencia ni acuerdo con la autora.
- **Por qué no es PROVEN.** Puede existir fuera del repo. Desde aquí no se puede comprobar.
- **Acción externa.** Confirmar que existe un acuerdo escrito con la autora que cubra el uso y el registro de la marca, y citarlo en `products/products.json` o en `LICENSE`. Si no existe, pactarlo o excluir ConsentFlow de la sección 4 de `LICENSE`.

### C-03 · Identidades hechas por una IA bajo reclamación de copyright

- **Qué pasa.** Seis productos figuran con `"author": "Claude (Claude Design)"` (`products/products.json:15`, `:34`, `:53`, `:90`, `:110`, `:130`). `LICENSE` reclama copyright sobre «the product glyphs and lockups» (`LICENSE:12-14`).
- **Por qué importa.** En varias jurisdicciones el derecho de autor exige que el autor sea una persona física. La Ley de Propiedad Intelectual española dice en su art. 5.1 que autor es «la persona natural», y la guía de la US Copyright Office de 2023 excluye el material generado por IA sin aportación humana. La protección que no depende de la autoría es la de **marca** (sección 4 de `LICENSE`).
- **Severidad.** BAJA. Los hechos son PROVEN; el alcance jurídico necesita revisión de un abogado.
- **Arreglo.** Documentar la aportación humana (selección, edición, dirección) donde la hubo, y apoyarse en la marca.

### C-04 · «Ningún permiso», en un repo público y bifurcable

- **Qué pasa.** `LICENSE:27-34` dice que no se concede permiso alguno para usar, copiar ni distribuir. Pero el repo es público y permite forks (`allow_forking: true`, `evidencia/github-ajustes.txt`). La sección D.5 de los términos de servicio de GitHub concede a sus usuarios ver el contenido público y bifurcarlo dentro de GitHub.
- **Por qué importa.** La frase no es falsa fuera de GitHub, pero se queda corta. La propia `LICENSE` ya explica por qué el repo es público (`LICENSE:36-40`). Falta reconocer esa licencia mínima, para que el texto no prometa más de lo que puede.
- **Severidad.** BAJA.
- **Arreglo.** Una frase en la sección 2 que reconozca la licencia de la sección D.5 de GitHub. O desactivar los forks, si se prefiere.

---

## Verificaciones en positivo

- **Las fuentes cumplen el OFL 1.1.**
  - Cada familia viaja con su licencia sin tocar (`fonts/LICENSE-Inter.txt`, `fonts/LICENSE-Outfit.txt`, `fonts/LICENSE-SpaceMono.txt`).
  - `LICENSE` las excluye de su cobertura (`LICENSE:46-61`).
  - Los nombres de las familias no se han cambiado (`fonts/README.md:48-49`).
  - Un guardián empareja cada fichero con su licencia (`tools/guard_paquete.py`).
- **La atribución de las fuentes sale de los propios binarios** y el motivo está documentado (`fonts/README.md:17-28`).
- **Los derechos que se reclaman empiezan cerrados, y retirar una licencia ya publicada se declara MAYOR** (`LICENSE:87-92`, `docs/PACKAGE.md:92`): cambiar las reglas a un consumidor exige avisarle con una versión mayor.
