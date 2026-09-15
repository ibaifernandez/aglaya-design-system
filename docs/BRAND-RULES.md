# AGLAYA — Brand rules

> **This file is canon.** It holds AGLAYA's non-negotiables and its voice rules,
> and the `aglaya-ds` MCP server reads them from here, **live, on every call**
> (`get_nonnegotiables`, `get_voice_rules`, `check_voice`, `is_allowed_word`).
>
> **It is written mostly in Spanish on purpose.** AGLAYA writes in Spanish, the
> voice rules quote Spanish phrases verbatim, and `check_voice` matches those
> phrases literally — translating them would stop it catching Spanish copy.
>
> **The headings are an interface, not a title.** The server looks each section
> up by its exact heading text. Rename one and the whole fleet silently receives
> that rule empty. The self-test (`aglaya-ds-mcp/selftest.py`) catches it: run it.
>
> **Do not paraphrase these rules anywhere else.** Ask the MCP. A copied rule is a
> rule that expires without warning.

---

## Non-negotiables

Reglas de la **marca madre AGLAYA** (aglaya.biz, materiales de agencia, redes). Rígidas: se aplican a toda superficie AGLAYA, salvo donde una superficie de **producto** declare una excepción explícita en `## Non-negotiables — producto`.

- `AGLAYA` always UPPERCASE.
- Zero border-radius. Every corner is square.
- Black canvas (`--color-bg`), red accent (`--color-brand`), green monospace (`--color-corporate-green`). Nothing else. Ask `get_token` for the values — a rule that carries its own hex stops being true the day the hex moves.
- No emoji. No Lucide. No Heroicons. No gradients-as-decoration. No rounded corners except the custom cursor.
- Copy is terse and imperative. No "we believe", no "we're passionate about", no exclamation marks, no rhetorical questions.
- Display type is Outfit Black, UPPERCASE, tight tracking. Body is Inter. Mono is Space Mono with extreme `letter-spacing: var(--tracking-widest)` to `var(--tracking-ultra)`.
- Signature headline move: line 1 white, line 2 `color: var(--color-brand)`.
- **En modo claro un acento no es tinta.** Es relleno, filete, punto o marca. Los acentos se eligieron para brillar sobre negro; sobre los fondos claros no llegan al suelo de texto. Cuando el acento es relleno, lo que tiene que pasar el umbral es el texto que va encima, no el acento.
- **`--color-brand` no es tinta de TEXTO CORRIDO en ningún modo.** Como tinta, en claro es `--color-brand-dark` y en oscuro `--color-brand-light`. Pregunta los valores a `get_token`.
- **El titular de firma es la excepción, y no es una excepción arbitraria:** «línea 1 blanca, línea 2 en `--color-brand`» sigue vigente porque es **display**, y el suelo del texto grande es más bajo que el del corrido. Medido en los dos modos y sobre los cinco fondos de cada uno: el rojo va de 4,06 a 4,67, por encima de ese suelo en todos. **La regla de arriba y el movimiento de firma no se contradicen: hablan de tamaños distintos.**
- **Sobre relleno `--color-brand`, la tinta es blanca.** La negra no llega: da el mismo contraste que el rojo sobre negro, y ése no alcanza el suelo de texto.
- **En modo claro el eyebrow lleva el verde como marca, no como letra:** filete `--color-corporate-green` delante, texto en `--fg-eyebrow`, que en ese modo es el gris del canon. En oscuro sigue siendo letra verde con filete rojo. El verde no tiene pareja oscura en la paleta —a diferencia del rojo— y conservarlo como tinta habría costado un color de marca nuevo y permanente.
- **Corrección, no reescritura:** estas dos reglas decían antes que el rojo solo fallaba como tinta **en modo claro**, y que en negro «pasaba raspando». Era falso, y el motivo importa más que el dato: el contraste del rojo sobre negro se venía citando como `4,50` —el umbral exacto— y es el **redondeo a dos decimales** de un valor que queda por debajo. Un número que se redondea justo al límite hay que mirarlo sin redondear.

## Non-negotiables — producto

Una **superficie de producto** (KANBAN DESK, CRM, OUTREACH, ConsentFlow, LEGAL REG TECH, ORCHESTRATOR, y la propia DESIGN SYSTEM — ver `products/products.json`) hereda TODOS los no-negociables de la marca madre, con una única excepción: su color de acento es de primera clase.

- Hereda todos los no-negociables de la marca madre **excepto la exclusividad de color** («Nothing else»).
- El **acento del producto** (definido en `products/products.json` y como token en `colors_and_type.css`) es color de primera clase: **libre en CTA, sin tope de proporción**.
- El rojo madre (`--color-brand`) no se reemplaza: coexiste con el acento en la superficie del producto. El acento identifica al producto; el rojo sigue siendo el rojo de la marca.
- Todo lo demás sigue vigente sin cambios: radius 0, sin emoji / Lucide / Heroicons, tipografía (Outfit Black / Inter / Space Mono), headline de dos líneas, voz seca e imperativa.
- La marca madre NO adopta acentos de producto: fuera de una superficie de producto, siguen los 3 colores y nada más.
- **En modo claro el acento de producto tampoco es tinta**, y eso no le quita ser de primera clase: sigue libre en CTA y sin tope de proporción **como relleno, filete, punto o marca**. Lo que cambia es que el texto no se pinta con él. Ninguno de los acentos de producto llega al suelo de texto sobre los fondos claros — se eligieron para brillar sobre negro.

---

## Content Fundamentals

> Los títulos de esta sección están en inglés a propósito y **no se traducen**:
> `aglaya-ds-mcp/brand.py` los busca por texto exacto (`_section`) para servir el
> canon por el MCP. El título es interfaz; el contenido es el canon. Traducir un
> título dejaría a la flota entera sin esa regla, en silencio.

### Voice

Breve, conciso, accionable, declarativo, técnico y preciso.

A AGLAYA le importa más **decir correctamente qué ocurre** que caer bien a los receptores de su comunicación.

«La Agencia Incómoda» del sobrenombre de AGLAYA es literal: **AGLAYA no suaviza malas noticias ni adorna conclusiones.** Tampoco utiliza cautelas rituales para evitar pronunciarse o suavizar el choque cuando la evidencia sí invita a hacerlo.

Dicha incomodidad, no obstante, no consiste en ser agresivo. Consiste en **mantener el criterio incluso cuando agradar resulta lo más fácil e incluso comercialmente inteligente**.

### Evidence

> **Ser asertivo no es un tono. Es lo que se puede respaldar.**

La evidencia determina hasta dónde puede llegar la voz.

- Lo que AGLAYA prohíbe es **decirle al cliente lo que quiere oír**, no elogiarle. El elogio merecido se dice. Lo que nunca ocurre es que el cliente dicte el diagnóstico. Metáfora odontológica: «*Si hay que sacar el premolar 44, se saca el premolar 44; no se empasta el incisivo 41 porque es lo que ha pedido el paciente*».
- **Directo no es duro.** Es sin adornos, no ser duro con pura gratuidad.
- **Afirmar más de lo que respalda la evidencia no es convicción, es fanfarronería.** Es el mismo fallo que vender algo como invencible, apuntando en la dirección contraria.
- Cuando la evidencia permite una conclusión clara, se dice con claridad. Cuando no la permite, **la incertidumbre también se dice con claridad**.
- Una inferencia es una inferencia y se presenta como tal. La ausencia de un problema concreto no implica que «todo está bien». Un dato desconocido no se rellena con diarrea verbal.

> **AGLAYA sostiene la conclusión más clara que la evidencia le permite sostener: ni palabras de más para impresionar, ni de menos para agradar (o viceversa).**

### Shape

- Frases preferentemente cortas.
- Una idea principal por párrafo.
- Voz activa siempre que sea natural.
- El punto tiene preferencia sobre la subordinación innecesaria.
- Se empieza por la conclusión, el dato o el problema; no por calentamiento social.
- Se explica lo necesario para entender y decidir. **No se demuestra inteligencia mediante longitud.**
- Una orden se formula como orden cuando realmente existe una acción que ejecutar. El resto se afirma de forma declarativa.

### Pronouns

- **«Tú»** para dirigirse directamente al fundador, operador o responsable que debe comprender o decidir algo: *«Tú lo posees.»*
- **«Nosotros»** únicamente para acciones que realmente ejecuta AGLAYA: *«Lo construimos.»*
- Evitar fórmulas impersonales cuando oculten quién hace qué.
- Nunca usar como relleno: "Nuestro equipo…"; "Creemos que…"; "Nos apasiona…"; "Estamos encantados de…"; "Esperamos poder…".

### Casing

- **`AGLAYA`** siempre en mayúsculas.
- Titulares y antetítulos de display: **MAYÚSCULAS**.
- Cuerpo de texto: frase normal.
- Etiquetas monoespaciadas: **MAYÚSCULAS**, con espaciado amplio.
- Las mayúsculas son estructura visual, no una forma de gritar.

### Signature terms
Used consistently across the site; treat these as protected brand vocabulary:

**Regla de precisión** (canon, 24-ago-2026): no se fuerza el vocabulario de marca
cuando hacerlo hace del significado de algo uno más difícil de comprender o
digerir. Un *lead* puede llamarse lead cuando esa sea la entidad comercial
exacta. Una métrica puede llamarse métrica. Un proceso puede llamarse proceso si
no constituye realmente un protocolo. **La marca sirve a la verdad. La verdad no
se deforma para servir a la marca.**

Por eso `Signal` y `Protocol` ya no vetan esas palabras: abajo son preferencias,
no prohibiciones. Lo que sigue vetado es lo que el canon prohíbe expresamente.

| Term | Usage |
| --- | --- |
| **Sovereignty** / **Sovereign** | The thing AGLAYA sells. |
| **Systems** (not "solutions", not "tools") | The thing AGLAYA ships. Preferred over the vetoed words when what is being described really is a system. |
| **Architecture** / **Infrastructure** | What the system is made of. |
| **Operational truth** | What the audit surfaces. |
| **Signal** | Data that matters. Preferred over lead, metric or input — but per the precision rule, a lead may be called a lead when that is the exact commercial entity. |
| **Protocol** | Preferred over process or steps when the thing really is a protocol. A process that is not a protocol may be called a process. |
| **Zero-filter** | Qualifier on diagnostics: findings arrive unsoftened. It claims something about how AGLAYA reports — which AGLAYA controls — never about how a system behaves. That is why it survives the retirement of absolute promises and "Zero-leak" does not. |
| **Dispatch** | The newsletter. Never "newsletter". |

### Signature terms — castellano

El mismo vocabulario para el copy en castellano. **Un nombre se queda, una idea
se traduce:** una cabecera no es un concepto. Cada fila lleva su original inglés
entre paréntesis para que el par se vea; los vetos son las palabras que un
redactor español teclea sin pensar.

Dos filas van sin veto a propósito. En inglés `control` y `process` se pueden
vetar; en castellano «control de acceso» y «proceso de compra» son frases
inocentes y corrientes, y un guardián que grita de más lo desactiva el primero
que lo sufra — entonces no protege nada. Quedan sin veto hasta que el corrector
sepa vetar frases en vez de palabras sueltas.

| Término | Uso |
| --- | --- |
| **Autonomía / Autónomo** (Sovereignty) | Lo que AGLAYA vende. **La asimetría con la tabla inglesa es deliberada, no una errata**: en español «soberanía» parece aludir a política más que ninguna otra cosa. Cuando alguien puede hacer algo por su cuenta no es «soberano», es «autónomo». `Sovereignty` se queda en inglés; aquí no. Quien lo «arregle» estará deshaciendo una decisión de marca. |
| **sistemas** (Systems) | Lo que AGLAYA entrega. Nunca "soluciones", nunca "solución", nunca "herramientas", nunca "herramienta". |
| **arquitectura / infraestructura** (Architecture / Infrastructure) | De qué está hecho el sistema. |
| **verdad operativa** (Operational truth) | Lo que la auditoría saca a la superficie. |
| **señal** (Signal) | El dato que importa. Preferido frente a lead o métrica — pero por la regla de precisión, un lead puede llamarse lead cuando esa sea la entidad comercial exacta, y una métrica puede llamarse métrica. |
| **protocolo** (Protocol) | Preferido cuando la cosa es de verdad un protocolo. Un proceso que no lo sea puede llamarse proceso. |
| **sin filtros** (Zero-filter) | Calificador sobre cómo AGLAYA informa: los hallazgos llegan sin suavizar. Afirma algo que AGLAYA controla —su propio reporte—, nunca cómo se comporta un sistema. Por eso sobrevive al retiro de las promesas absolutas y "Zero-leak" no. El rótulo Zero-Filter Diagnostics no se traduce: es un nombre, no una idea. |
| **Dispatch** | El boletín. No se traduce, y ese es justo el motivo: traducirlo lo convierte en la palabra vetada. Nunca "boletín", nunca "boletines". |

### Forbidden patterns

Las frases van **entre comillas dobles rectas** porque `brand.py` (`_forbidden_phrases`)
solo persigue lo entrecomillado así. Una prohibición escrita sin comillas se lee
aquí y **no la persigue `check_voice`**: se vería como regla y no lo sería.

- "We believe…" / "We're passionate about…" / "Our mission is…" / "Creemos que…" / "Nos apasiona…" / "Nuestra misión es…"
- "Estamos encantados…" / "Esperamos poder…"
- "Solutions" / "Soluciones" cuando solo sustituye vagamente a sistemas
- "Synergy" / "Sinergias"
- "partner with you" / "trusted partner" / "Journey" / "Transform your business" / "Transforma tu negocio" — se veta **la frase, no la palabra**: un socio real puede llamarse partner, y por la regla de precisión la marca no prevalece sobre el término exacto. Lo que se persigue es el cliché, no el sustantivo.
- "Innovador" / "Innovative" / "Revolucionario" / "Revolutionary" / "World-class" / "Best-in-class", o equivalentes sin prueba
- Exclamation marks — signos de exclamación en copy de producto
- Emoji in product copy (the codebase contains zero emoji)
- Rhetorical questions used for sales warmth — preguntas retóricas utilizadas únicamente para fabricar cercanía comercial
- Superlativos sin evidencia
- Agresividad utilizada como sustituto de criterio
- "Zero-leak", y cualquier promesa absoluta de que un sistema no fallará. **El software gotea —y el software con IA dentro gotea más—.** AGLAYA no promete invulnerabilidad, ausencia total de errores ni comportamiento perfecto cuando no puede demostrarlo. En lugar de una promesa absoluta se nombra la propiedad concreta que sí puede acreditarse: datos almacenados localmente; cero solicitudes externas; fuentes servidas localmente; dependencias versionadas; revisión humana obligatoria; evidencia trazable; comportamiento observado bajo unas condiciones determinadas. Cuanto más específica sea la afirmación, menos necesita parecer impresionante.

### Final check

Antes de publicar cualquier texto de AGLAYA, debe poder responderse «sí» a estas preguntas:

1. **¿Es verdad?**
2. **¿Podemos demostrar hasta dónde es verdad?**
3. **¿Está dicho con la mayor claridad posible?**
4. **¿Hemos añadido dureza, grandilocuencia o jerga que no aporta información?**
5. **¿Un lector entiende qué ocurre, por qué importa y qué debe hacer después?**

Si la evidencia y la frase entran en conflicto, **se rebaja la frase. Nunca se estira la evidencia.**

### What this voice does not cover

These rules govern **tone and brand vocabulary**. They do not govern commercial or
legal argument, and `check_voice` does not look at it: a text can come back clean
here and still be unpublishable.

The language rules that carry legal risk — how compliance may be claimed, whether a
fine may be used as a selling argument, the exact wording a consent checkbox is
allowed to use — are not brand rules and do not live in this repo. They live in the
captain's commercial material (repo `aglaya-orchestrator`) and are asked for through
the `aglaya-atlas` MCP, `verdad_comercial`.

They are **named here, never copied**. A legal rule copied into this repo would go
stale the day the contract moves, and nobody would find out — while it kept reading
like canon. Passing the brand corrector is not permission to publish.

### Sample copy

> **Hero.** _"The agency is dead. Long live the system."_
> _"Most teams don't need an agency. They need their own infrastructure. We build it. You own it. The system keeps running when we're not in the room."_

> **Problem card.** _"Stop building your empire on rented soil. When you hire a traditional agency, you are merely financing their portfolio."_

> **Anti-Client.** _"If you are looking for a partner to validate your current inefficiencies, find a traditional agency. If you need to build a sovereign engine, let's talk."_

> **Form state.** `SYNCING...` → `SYNCED` / `DATA_SYNCHRONIZED` / `ERROR_DURING_TRANSMISSION. REATTEMPT_REQUIRED.`

> **Footer.** _"Sovereign systems. Zero platform dependency theatre."_

Monospace labels behave as terminal output — `REF_ID:`, `LOGIC_NODE_001`, `EXCLUSION_PRINCIPLE_01`, `PLATFORM_FEES: 0.00`, `SYSTEM_INTEGRITY_OK`. Use them as structural chrome, not decoration.
