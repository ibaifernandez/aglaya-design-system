// AGLAYA UI Kit — Systems grid + industrial marquee.

const SYSTEMS = [
  { name: 'Systemic Alchemy', tagline: 'Transforming operational chaos into autonomous digital assets.',
    cases: ['Autonomous opportunity validation','Operational truth visualization','Automated consensus protocols'] },
  { name: 'Inevitable Logical Flow', tagline: 'Systems that execute the precise action based on user behavior.',
    cases: ['Purchase intent synchronization','Reactive authority deployment','Progressive credibility assets'] },
  { name: 'Zero-Leak Architecture', tagline: 'Infrastructure where data integrity and performance are non-negotiable.',
    cases: ['Performance capture interfaces','Digital asset shielding','Real-time data consistency'] },
  { name: 'Algorithmic Sovereignty', tagline: 'Autonomous intelligence integrated into the core of business execution.',
    cases: ['Corporate memory deployment','Critical intelligence extraction','Cognitive load distribution'] },
  { name: 'Zero-Filter Diagnostics', tagline: 'Eliminating operational lies to find the shortest path to profitability.',
    cases: ['Market authority mapping','Operational leak deconstruction','Command and control structuring'] },
];

const SystemCard = ({ s, i }) => {
  const [hover, setHover] = React.useState(false);
  return (
    <article
      onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
      style={{
        position: 'relative', overflow: 'hidden', minHeight: '100%',
        display: 'flex', flexDirection: 'column',
        padding: 40,
        background: 'var(--surface-2)',
        border: `1px solid ${hover ? 'rgba(232,0,61,0.3)' : 'rgba(255,255,255,0.05)'}`,
        transition: 'border-color 0.5s var(--ease)',
      }}>
      <span style={{
        fontFamily: 'var(--font-mono)', fontSize: 10, color: 'var(--brand)',
        letterSpacing: '0.5em', textTransform: 'uppercase', marginBottom: 16,
      }}>ARCHITECTURE_PRINCIPLE_00{i+1}</span>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        <h3 style={{
          margin: 0, color: hover ? 'var(--brand)' : '#fff',
          fontFamily: 'var(--font-display)', fontWeight: 900,
          fontSize: 'clamp(1.6rem, 2.2vw, 2.2rem)',
          letterSpacing: '-0.025em', textTransform: 'uppercase',
          transition: 'color 0.3s var(--ease)',
        }}>{s.name}</h3>
        <p style={{
          margin: 0, color: 'var(--muted)', fontFamily: 'var(--font-body)',
          fontSize: 17, fontStyle: 'italic', lineHeight: 1.3,
        }}>{s.tagline}</p>
      </div>
      <div style={{
        marginTop: 16, height: 1,
        width: hover ? '100%' : 48,
        background: hover ? 'rgba(232,0,61,0.2)' : 'rgba(255,255,255,0.1)',
        transition: 'all 0.7s var(--ease)',
      }}/>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 14, marginTop: 20 }}>
        <span style={{
          fontFamily: 'var(--font-mono)', fontSize: 9, color: 'var(--green)',
          letterSpacing: '0.5em', textTransform: 'uppercase',
        }}>APPLIED_LOGIC:</span>
        <ul style={{ margin: 0, padding: 0, listStyle: 'none', display: 'flex', flexDirection: 'column', gap: 10 }}>
          {s.cases.map(c => (
            <li key={c} style={{
              display: 'flex', alignItems: 'center', gap: 10,
              color: 'var(--muted)', fontFamily: 'var(--font-mono)',
              fontSize: 11, letterSpacing: '0.08em', textTransform: 'uppercase',
            }}>
              <span style={{ width: 6, height: 6, background: 'rgba(232,0,61,0.4)', flexShrink: 0 }}/>
              {c}
            </li>
          ))}
        </ul>
      </div>
    </article>
  );
};

const MarqueeWords = () => (
  <div style={{ display: 'flex', alignItems: 'center', gap: 80, flexShrink: 0 }}>
    {['Systemic Alchemy','/','Inevitable Logical Flow','/','Zero-Leak Architecture','/','Algorithmic Sovereignty','/','Zero-Filter Diagnostics','/'].map((w,i) => (
      <span key={i} style={{
        fontFamily: 'var(--font-display)', fontWeight: 900, fontSize: 40,
        textTransform: 'uppercase', letterSpacing: '-0.03em',
        color: w === '/' ? 'var(--brand)' : 'rgba(255,255,255,0.2)',
      }}>{w}</span>
    ))}
  </div>
);

const SystemsGrid = () => (
  <section id="systems" style={{
    position: 'relative', padding: '80px 40px 0', background: '#000',
    borderTop: '1px solid rgba(255,255,255,0.05)', overflow: 'hidden',
  }}>
    <div style={{ maxWidth: 1280, margin: '0 auto' }}>
      <div style={{ marginBottom: 48 }}>
        <SectionHeader
          eyebrow="Engineering principles guiding our system design"
          line1="Our Architecture"/>
      </div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 24 }}>
        {SYSTEMS.map((s,i) => (
          <div key={s.name} style={{ flex: '1 1 30%', minWidth: 300 }}>
            <SystemCard s={s} i={i}/>
          </div>
        ))}
      </div>
    </div>

    <div style={{
      marginTop: 96, transform: 'rotate(-1deg) translateY(40px)',
      borderTop: '1px solid rgba(255,255,255,0.05)',
      borderBottom: '1px solid rgba(255,255,255,0.05)',
      background: 'var(--surface-1)', padding: '32px 0', overflow: 'hidden',
    }}>
      <div className="marquee-track" style={{
        display: 'flex', gap: 80, whiteSpace: 'nowrap', width: 'max-content',
      }}>
        {[...Array(6)].map((_,i) => <MarqueeWords key={i}/>)}
      </div>
    </div>
  </section>
);

window.SystemsGrid = SystemsGrid;
