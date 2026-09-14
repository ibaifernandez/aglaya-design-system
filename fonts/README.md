# fonts/ — tipografías de terceros, redistribuidas bajo OFL 1.1

Estas tres familias **no son de AGLAYA**. Se redistribuyen dentro de este repo
y dentro del paquete `@aglaya/design-tokens` bajo la **SIL Open Font License
1.1**, que exige que la licencia y el aviso de copyright viajen con los
archivos. Por eso están aquí y no en un enlace.

La licencia del repo ([`../LICENSE`](../LICENSE)) **no las cubre y no las
puede cubrir**: son de sus autores y mantienen sus propios términos.

| Familia | Uso en la marca | Copyright, según el propio binario | Licencia |
| --- | --- | --- | --- |
| **Inter** | body | Copyright 2017-2019 The Inter project authors | [`LICENSE-Inter.txt`](LICENSE-Inter.txt) |
| **Outfit** | display | Copyright 2021 The Outfit Project Authors | [`LICENSE-Outfit.txt`](LICENSE-Outfit.txt) |
| **Space Mono** | labels, eyebrows | Copyright 2016 The Space Mono Project Authors | [`LICENSE-SpaceMono.txt`](LICENSE-SpaceMono.txt) |

La columna del copyright no está tecleada de memoria: sale de la tabla `name`
de los propios archivos (id 0), que es lo que declara cada binario que se
entrega. Los archivos de licencia son copia **verbatim** de la que publica cada
proyecto, sin una línea añadida — modificar un texto de licencia sería
exactamente lo que no se puede hacer.

Inter trae una variante conocida en el cuerpo del OFL (`PERMISSION AND
CONDITIONS` donde SIL escribe `PERMISSION & CONDITIONS`); el resto del texto es
idéntico al canónico de SIL en las tres.

## La regla

**Ninguna familia entra en `fonts/` sin su licencia al lado.** No es una
costumbre: [`../tools/guard_paquete.py`](../tools/guard_paquete.py) empareja
cada archivo de fuente con un `LICENSE-<Familia>.txt` en este directorio y
falla si alguno se queda sin pareja. Añadir una cuarta familia sin su licencia
pone el CI rojo antes de que el paquete llegue a nadie.

Es la avería que ya ocurrió una vez: el repo se hizo público y el paquete
redistribuyó las tres familias sin su archivo de licencia. Un guardián es más
barato que acordarse.

## Qué NO hace este directorio

- No se renombra ninguna familia. El OFL protege los nombres reservados, y
  renombrar una fuente para «adaptarla» es la forma más rápida de incumplirlo.
- No se venden las fuentes por separado. El OFL lo prohíbe; aquí van dentro de
  un sistema de diseño, que es exactamente el uso previsto.
- No se sirven desde una CDN. Son locales a propósito: cero peticiones
  externas, y el paquete funciona sin red.
