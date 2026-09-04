// AGLAYA UI Kit — Fixed site header. Glass chrome, nav links, WhatsApp, contact CTA.

const Header = () => {
  return (
    <header style={{
      position: 'sticky', top: 0, left: 0, width: '100%', zIndex: 50,
      background: 'rgba(0,0,0,0.8)', backdropFilter: 'blur(24px)',
      borderBottom: '1px solid color-mix(in srgb, var(--color-text) 5%, transparent)',
    }}>
      <div style={{
        maxWidth: 1280, margin: '0 auto', height: 80,
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '0 40px', gap: 32,
      }}>
        {/* Logo lockup */}
        <a href="#home" aria-label="AGLAYA Home"
          style={{ display: 'flex', flexDirection: 'column', gap: 3, flexShrink: 0 }}>
          <img src="./assets/logo-white.svg" alt="" style={{ height: 24, width: 'auto' }}/>
          <span style={{
            fontFamily: 'var(--font-mono)', fontSize: 7, color: 'var(--color-text)',
            letterSpacing: '0.2em', textTransform: 'uppercase', textAlign: 'center',
          }}>The Uncomfortable AI·gency</span>
        </a>

        {/* Nav */}
        <nav style={{ display: 'flex', alignItems: 'center', gap: 32 }}>
          {['Systems','Proof','Economics','Services','ROI Audit'].map(label => (
            <a key={label} href={`#${label.toLowerCase().replace(/ /g,'-')}`}
              onMouseEnter={e => e.currentTarget.style.color = 'var(--brand)'}
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
        <div style={{ display: 'flex', alignItems: 'center', gap: 20 }}>
          {/* Lang switcher */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, opacity: 0.7 }}>
            <span title="ES" style={{ fontFamily: 'var(--font-mono)', fontSize: 10, letterSpacing: '0.2em' }}>ES</span>
            <span style={{ color: 'var(--color-faint)' }}>/</span>
            <span title="PT" style={{ fontFamily: 'var(--font-mono)', fontSize: 10, letterSpacing: '0.2em' }}>PT</span>
          </div>

          {/* WhatsApp pill */}
          <a href="#whatsapp" aria-label="WhatsApp"
            style={{
              display: 'inline-flex', alignItems: 'center', gap: 8,
              background: 'var(--brand)', color: '#ffffff' /* tinta sobre relleno rojo: blanca (tramo 3) */,
              padding: '8px 16px 8px 12px', borderRadius: 999,
              fontFamily: 'var(--font-display)', fontWeight: 900,
              fontSize: 11, letterSpacing: '0.2em', textTransform: 'uppercase',
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
              fontSize: 12, letterSpacing: '0.2em', textTransform: 'uppercase',
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
