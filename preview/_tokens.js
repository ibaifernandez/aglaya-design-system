/* Rellena EN VIVO los valores que un specimen muestra al lector.
 *
 * Un specimen que enseña el hex tecleado a mano miente el día que el token se
 * mueva — y es justo la página que alguien abre para saber cuál es el rojo.
 * Aquí el valor sale de `colors_and_type.css` en el momento de pintar, igual
 * que lo saca el MCP: la página no puede desviarse de la fuente porque no
 * guarda ninguna copia.
 *
 * Uso:  <span data-token="--color-brand"></span>
 *       <span data-token="--color-brand" data-case="upper"></span>
 *
 * Sin dependencias y sin red: script clásico, mismo ethos que el resto del kit.
 */
(function () {
  function pintar() {
    var raiz = getComputedStyle(document.documentElement);
    var nodos = document.querySelectorAll('[data-token]');
    for (var i = 0; i < nodos.length; i++) {
      var el = nodos[i];
      var valor = raiz.getPropertyValue(el.getAttribute('data-token')).trim();
      if (!valor) {
        // Un token que no existe tiene que verse, no desaparecer: un hueco en
        // blanco se lee como «no hay color» en vez de como «el token está mal».
        el.textContent = '?? ' + el.getAttribute('data-token');
        el.style.opacity = '0.6';
        continue;
      }
      el.textContent = el.getAttribute('data-case') === 'upper'
        ? valor.toUpperCase()
        : valor;
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', pintar);
  } else {
    pintar();
  }
})();
