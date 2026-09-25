// AGLAYA UI Kit — Fixed site header. Glass chrome, nav links, WhatsApp, contact CTA.

const Header = () => {
  return (
    <header style={{
      position: 'sticky', top: 0, left: 0, width: '100%', zIndex: 50,
      background: 'rgba(0,0,0,0.8)', backdropFilter: 'blur(24px)',
      borderBottom: '1px solid color-mix(in srgb, var(--color-text) 5%, transparent)',
    }}>
      <div style={{
        maxWidth: 1280, margin: '0 auto',
        // `minHeight` y no `height`: con altura fija, lo que envuelve se sale de
        // la barra en vez de agrandarla. Laterales por token: 40 px fijos dejan
        // 295 de contenido en una pantalla de 375.
        minHeight: 80, padding: 'var(--space-4) var(--space-6)',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        flexWrap: 'wrap', gap: 'var(--space-4)',
      }}>
        {/* Logo lockup */}
        <a href="#home" aria-label="AGLAYA Home"
          style={{ display: 'flex', flexDirection: 'column', gap: 3, flexShrink: 0 }}>
          <img src="./assets/logo-white.svg" alt="" style={{ height: 24, width: 'auto' }}/>
          <span style={{
            fontFamily: 'var(--font-mono)', fontSize: 7, color: 'var(--color-text)',
            letterSpacing: 'var(--tracking-wider)', textTransform: 'uppercase', textAlign: 'center',
          }}>The Uncomfortable AI·gency</span>
        </a>

        {/* Nav */}
        {/* `flexWrap` y un hueco menor: medido en la página, a 375 px este nav medía
            709 px y arrastraba scroll horizontal a todo el documento. No hay punto
            de corte porque no hace falta: envuelve cuando no cabe. */}
        <nav style={{ display: 'flex', alignItems: 'center', gap: 20, flexWrap: 'wrap' }}>
          {['Systems','Proof','Economics','Services','ROI Audit'].map(label => (
            <a key={label} href={`#${label.toLowerCase().replace(/ /g,'-')}`}
              /* --brand como tinta da 4.4985 sobre negro y el canon lo prohíbe;
                 --brand-ink es el alias del kit para --fg-brand, que da 6.55. */
              onMouseEnter={e => e.currentTarget.style.color = 'var(--brand-ink)'}
              onMouseLeave={e => e.currentTarget.style.color = 'var(--muted)'}
              style={{
                color: 'var(--muted)', fontFamily: 'var(--font-display)',
                fontWeight: 700, fontSize: 13,
                letterSpacing: '0.18em', textTransform: 'uppercase',
                transition: 'color 0.3s var(--ease)',
              }}>{label}</a>
          ))}
        </nav>

        {/* Actions */}
        {/* También envuelve: medido, este grupo se salía 11 px a 375. */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 20, flexWrap: 'wrap' }}>
          {/* Lang switcher */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, opacity: 0.7 }}>
            <span title="ES" style={{ fontFamily: 'var(--font-mono)', fontSize: 10, letterSpacing: 'var(--tracking-wider)' }}>ES</span>
            {/* Separador: decoración, no contenido. Con `--color-faint` bajo el
                0.7 del grupo daba 2.73 sobre negro. Se oculta a lectores de
                pantalla en vez de subirle el color, porque leer «ES barra PT»
                no aporta nada. */}
            <span aria-hidden="true" style={{ color: 'var(--color-faint)' }}>/</span>
            <span title="PT" style={{ fontFamily: 'var(--font-mono)', fontSize: 10, letterSpacing: 'var(--tracking-wider)' }}>PT</span>
          </div>

          {/* WhatsApp pill */}
          <a href="#whatsapp" aria-label="WhatsApp"
            style={{
              display: 'inline-flex', alignItems: 'center', gap: 8,
              background: 'var(--brand)', color: '#ffffff' /* tinta sobre relleno rojo: blanca (tramo 3) */,
              padding: '8px 16px 8px 12px', borderRadius: 999,
              fontFamily: 'var(--font-display)', fontWeight: 900,
              fontSize: 11, letterSpacing: 'var(--tracking-wider)', textTransform: 'uppercase',
            }}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M.057 24l1.687-6.163a11.87 11.87 0 0 1-1.587-5.946C.16 5.335 5.495 0 12.05 0a11.82 11.82 0 0 1 8.413 3.488 11.82 11.82 0 0 1 3.48 8.414c-.003 6.557-5.338 11.892-11.893 11.892a11.9 11.9 0 0 1-5.688-1.448L.057 24zM6.6 20.2c1.68.99 3.27 1.58 5.38 1.58 5.45 0 9.88-4.43 9.89-9.88 0-5.46-4.42-9.89-9.88-9.89C6.54 2.01 2.11 6.45 2.1 11.9c0 2.23.65 3.89 1.75 5.64l-1 3.65 3.74-.98z"/></svg>
            WhatsApp
          </a>

          {/* Contact */}
          <a href="#contact"
            style={{
              display: 'inline-flex', alignItems: 'center', gap: 8,
              background: 'color-mix(in srgb, var(--color-text) 10%, transparent)', border: '1px solid color-mix(in srgb, var(--color-text) 20%, transparent)',
              color: 'var(--color-text)', padding: '10px 20px',
              fontFamily: 'var(--font-display)', fontWeight: 900,
              fontSize: 12, letterSpacing: 'var(--tracking-wider)', textTransform: 'uppercase',
            }}>
            Contact
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </a>
        </div>
      </div>
    </header>
  );
};

window.Header = Header;
