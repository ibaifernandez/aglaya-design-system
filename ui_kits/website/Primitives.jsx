// AGLAYA UI Kit — shared primitives
// Buttons, eyebrows, codetags, section headers. No radii, ever.

const BrandArrow = ({ size = 14, stroke = 'currentColor' }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none"
       stroke={stroke} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
    <path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>
  </svg>
);

// Primary CTA — filled brand red with offset shadow-border
const PrimaryButton = ({ children, href = '#', onClick }) => {
  const Tag = href ? 'a' : 'button';
  return (
    <Tag href={href} onClick={onClick}
      style={{
        position: 'relative', display: 'inline-flex', alignItems: 'center', gap: 8,
        background: 'var(--brand)', color: '#fff',
        padding: '20px 22px',
        fontFamily: 'var(--font-display)', fontWeight: 900, fontSize: 16,
        letterSpacing: '0.2em', textTransform: 'uppercase',
        transition: 'transform 0.3s var(--ease), background 0.3s var(--ease)',
      }}
      onMouseEnter={e => { e.currentTarget.style.transform = 'scale(1.02)';
        e.currentTarget.querySelector('.s').style.transform = 'translate(0,0)'; }}
      onMouseLeave={e => { e.currentTarget.style.transform = 'none';
        e.currentTarget.querySelector('.s').style.transform = 'translate(4px,4px)'; }}>
      {children}
      <span className="s" style={{
        position: 'absolute', inset: 0,
        border: '1px solid rgba(255,255,255,0.2)',
        transform: 'translate(4px,4px)', zIndex: -1,
        transition: 'transform 0.3s var(--ease)',
      }}/>
    </Tag>
  );
};

// Ghost CTA — white-on-white
const GhostButton = ({ children, href = '#' }) => (
  <a href={href}
    style={{
      display: 'inline-flex', alignItems: 'center', gap: 8,
      background: 'rgba(255,255,255,0.1)', color: '#fff',
      border: '1px solid rgba(255,255,255,0.2)',
      padding: '10px 20px',
      fontFamily: 'var(--font-display)', fontWeight: 900, fontSize: 12,
      letterSpacing: '0.2em', textTransform: 'uppercase',
      transition: 'background 0.3s var(--ease)',
    }}
    onMouseEnter={e => e.currentTarget.style.background = 'rgba(255,255,255,0.2)'}
    onMouseLeave={e => e.currentTarget.style.background = 'rgba(255,255,255,0.1)'}>
    {children}
    <BrandArrow size={12} />
  </a>
);

// Monospace link w/ growing rule — "See the proof →"
const MonoLink = ({ children, href = '#' }) => {
  const [hover, setHover] = React.useState(false);
  return (
    <a href={href}
      onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
      style={{
        display: 'inline-flex', alignItems: 'center', gap: 14,
        fontFamily: 'var(--font-mono)', fontSize: 12,
        letterSpacing: '0.3em', textTransform: 'uppercase',
        color: hover ? '#fff' : 'var(--muted)',
        transition: 'color 0.3s var(--ease)',
      }}>
      {children}
      <span style={{
        height: 1, width: hover ? 64 : 40,
        background: hover ? 'var(--brand)' : 'rgba(255,255,255,0.2)',
        transition: 'all 0.3s var(--ease)',
      }}/>
    </a>
  );
};

// Eyebrow — green monospace with brand-red rule
const Eyebrow = ({ children }) => (
  <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
    <div style={{ width: 32, height: 1, background: 'var(--brand)' }}/>
    <span style={{
      color: 'var(--green)', fontFamily: 'var(--font-mono)',
      fontSize: 12, fontWeight: 900,
      letterSpacing: '0.5em', textTransform: 'uppercase',
    }}>{children}</span>
  </div>
);

// Section title — line 1 white / line 2 brand-red
const SectionHeader = ({ eyebrow, line1, line2, maxWidth = 860 }) => (
  <header style={{ display: 'flex', flexDirection: 'column', gap: 28 }}>
    {eyebrow && <Eyebrow>{eyebrow}</Eyebrow>}
    <h2 style={{
      margin: 0, maxWidth,
      fontFamily: 'var(--font-display)', fontWeight: 900,
      fontSize: 'clamp(2.2rem, 5vw, 4.5rem)', lineHeight: 0.96,
      letterSpacing: '-0.03em', textTransform: 'uppercase',
    }}>
      <span style={{ display: 'block' }}>{line1}</span>
      {line2 && <span style={{ display: 'block', color: 'var(--brand)' }}>{line2}</span>}
    </h2>
  </header>
);

Object.assign(window, { PrimaryButton, GhostButton, MonoLink, Eyebrow, SectionHeader, BrandArrow });
