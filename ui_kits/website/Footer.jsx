// AGLAYA UI Kit — Footer with Dispatch signup and primary links.

const DispatchForm = () => {
  const [email, setEmail] = React.useState('');
  const [focus, setFocus] = React.useState(false);
  const [state, setState] = React.useState('idle'); // idle | syncing | synced

  const submit = (e) => {
    e.preventDefault();
    if (!email) return;
    setState('syncing');
    setTimeout(() => setState('synced'), 1200);
  };

  return (
    <form onSubmit={submit} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
      <label style={{
        fontFamily: 'var(--font-mono)', fontSize: 9,
        letterSpacing: '0.4em', color: 'var(--green)', textTransform: 'uppercase',
      }}>CORPORATE_EMAIL</label>
      <div style={{ display: 'flex', gap: 12 }}>
        <input
          type="email" value={email} onChange={e => setEmail(e.target.value)}
          onFocus={() => setFocus(true)} onBlur={() => setFocus(false)}
          placeholder="operator@company.com"
          style={{
            flex: 1, padding: '16px 18px',
            background: focus ? 'color-mix(in srgb, var(--brand) 3%, transparent)' : 'rgba(255,255,255,0.03)',
            border: `1px solid ${focus ? 'color-mix(in srgb, var(--brand) 50%, transparent)' : 'rgba(255,255,255,0.25)'}`,
            color: '#fff', fontFamily: 'var(--font-body)', fontSize: 15,
            outline: 'none', transition: 'all 0.3s var(--ease)',
          }}/>
        <PrimaryButton onClick={submit}>
          {state === 'syncing' ? 'SYNCING...' : state === 'synced' ? 'SYNCED' : 'Subscribe →'}
        </PrimaryButton>
      </div>
      <p style={{
        margin: 0, color: 'rgba(255,255,255,0.35)',
        fontFamily: 'var(--font-mono)', fontSize: 10,
        letterSpacing: '0.2em', textTransform: 'uppercase',
      }}>
        {state === 'synced' ? 'DATA_SYNCHRONIZED. DISPATCH_NODE_ACTIVE.' : 'Zero filler. Weekly signal, not noise.'}
      </p>
    </form>
  );
};

const FOOTER_LINKS = [
  { label: 'ROI Audit', desc: 'Zero-filter diagnostic of your operational leaks.' },
  { label: 'Services', desc: 'Sovereign systems, engineered to your stack.' },
  { label: 'Contact', desc: 'Open a direct channel with the founding engineers.' },
];

const FooterLinkRow = ({ label, desc }) => (
  <a href="#"
    style={{
      display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start',
      gap: 20, padding: '20px 0',
      borderTop: '1px solid rgba(255,255,255,0.08)',
    }}
    onMouseEnter={e => { e.currentTarget.querySelector('.lab').style.color = 'var(--brand-light)';
      e.currentTarget.querySelector('.go').style.color = 'var(--brand-light)'; }}
    onMouseLeave={e => { e.currentTarget.querySelector('.lab').style.color = '#fff';
      e.currentTarget.querySelector('.go').style.color = 'rgba(255,255,255,0.26)'; }}>
    <div style={{ display: 'flex', flexDirection: 'column', gap: 8, minWidth: 0 }}>
      <span className="lab" style={{
        color: '#fff', fontFamily: 'var(--font-display)', fontWeight: 900,
        fontSize: 18, letterSpacing: '0.04em', textTransform: 'uppercase',
        transition: 'color 0.3s var(--ease)',
      }}>{label}</span>
      <span style={{
        color: 'rgba(255,255,255,0.46)',
        fontFamily: 'var(--font-body)', fontSize: 14, lineHeight: 1.5,
      }}>{desc}</span>
    </div>
    <span className="go" style={{
      flexShrink: 0, marginTop: 4,
      fontFamily: 'var(--font-mono)', fontSize: 12,
      letterSpacing: '0.28em', textTransform: 'uppercase',
      color: 'rgba(255,255,255,0.26)', transition: 'color 0.3s var(--ease)',
    }}>[GO]</span>
  </a>
);

const Footer = () => (
  <footer style={{
    position: 'relative', overflow: 'hidden',
    borderTop: '1px solid rgba(255,255,255,0.08)',
    background: 'var(--color-bg-deep)', padding: '80px 40px 40px',
  }}>
    <div className="bg-grid" style={{
      position: 'absolute', inset: 0, opacity: 0.15, pointerEvents: 'none',
    }}/>
    <div style={{
      position: 'relative', maxWidth: 1280, margin: '0 auto',
      display: 'flex', flexDirection: 'column', gap: 64,
    }}>
      <div style={{
        display: 'grid', gridTemplateColumns: '1.55fr 0.9fr', gap: 64, alignItems: 'flex-start',
      }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 32 }}>
          <img src="./assets/logo-white.svg" alt="AGLAYA" style={{ height: 24, width: 'auto' }}/>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <span style={{
              fontFamily: 'var(--font-mono)', fontSize: 10,
              letterSpacing: '0.42em', textTransform: 'uppercase', color: 'var(--green)',
            }}>DISPATCH_NODE</span>
            <h2 style={{
              margin: 0, color: '#fff', maxWidth: 640,
              fontFamily: 'var(--font-display)', fontWeight: 900,
              fontSize: 'clamp(2rem, 3.5vw, 3rem)',
              letterSpacing: '-0.02em', textTransform: 'uppercase', lineHeight: 0.94,
            }}>Weekly signal for operators who ship.</h2>
            <p style={{
              margin: 0, color: 'rgba(255,255,255,0.62)', maxWidth: 520,
              fontFamily: 'var(--font-body)', fontSize: 16, lineHeight: 1.6,
            }}>
              Architecture notes, automation protocols, and operational truths from the field.
              No filler. No platform dependency theatre.
            </p>
          </div>
          <div style={{
            maxWidth: 560,
            border: '1px solid rgba(255,255,255,0.1)', background: 'rgba(255,255,255,0.025)',
            padding: 28,
          }}>
            <DispatchForm/>
          </div>
        </div>

        <div style={{
          border: '1px solid rgba(255,255,255,0.1)', background: 'rgba(255,255,255,0.02)', padding: 28,
        }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginBottom: 16 }}>
            <span style={{
              fontFamily: 'var(--font-mono)', fontSize: 10,
              letterSpacing: '0.38em', textTransform: 'uppercase', color: 'rgba(255,255,255,0.35)',
            }}>PRIMARY_CHANNELS</span>
            <p style={{
              margin: 0, color: 'rgba(255,255,255,0.52)', maxWidth: 320,
              fontFamily: 'var(--font-body)', fontSize: 13, lineHeight: 1.6,
            }}>Three direct routes into the system. Pick the one that matches your current bottleneck.</p>
          </div>
          <div>{FOOTER_LINKS.map(l => <FooterLinkRow key={l.label} {...l}/>)}</div>
        </div>
      </div>

      <div style={{
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        borderTop: '1px solid rgba(255,255,255,0.08)', paddingTop: 24, gap: 24, flexWrap: 'wrap',
      }}>
        <span style={{
          fontFamily: 'var(--font-mono)', fontSize: 10,
          color: 'rgba(255,255,255,0.34)', letterSpacing: '0.24em', textTransform: 'uppercase',
        }}>Sovereign systems. Zero platform dependency theatre.</span>
        <div style={{ display: 'flex', alignItems: 'center', gap: 24, flexWrap: 'wrap' }}>
          <a href="#" style={{ color: 'rgba(255,255,255,0.42)', fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: 11, letterSpacing: '0.18em', textTransform: 'uppercase' }}>Privacy</a>
          <a href="#" style={{ color: 'rgba(255,255,255,0.42)', fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: 11, letterSpacing: '0.18em', textTransform: 'uppercase' }}>Cookies</a>
          <span style={{ color: 'rgba(255,255,255,0.22)', fontFamily: 'var(--font-mono)', fontSize: 10, letterSpacing: '0.2em', textTransform: 'uppercase' }}>© {new Date().getFullYear()} AGLAYA</span>
        </div>
      </div>
    </div>
  </footer>
);

window.Footer = Footer;
window.DispatchForm = DispatchForm;
