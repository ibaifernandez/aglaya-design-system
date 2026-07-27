// AGLAYA UI Kit — AntiClient exclusion principles block.

const EXCLUSIONS = [
  { title: 'INSUFFICIENT INVESTMENT MASS', body: "Our architecture is engineered for high-output environments. Without a proportional growth investment to justify the deployment, the data density remains insufficient for our systems to generate an efficient return." },
  { title: 'DATA STREAM VACUUM', body: 'Significant optimization requires volume. We do not deploy infrastructure in environments where the operational data stream is too thin to fuel our predictive models.' },
  { title: 'ARCHITECTURAL OVERKILL', body: "AGLAYA's systems are optimized for scale. If manual processes have not yet reached a critical bottleneck, the systemic leverage we provide will exceed your current operational requirements." },
  { title: 'COGNITIVE CONFIRMATION BIAS', body: 'We provide systemic truth, not confirmation bias. We are here to challenge your infrastructure, not to validate your comfort.' },
  { title: 'HUMAN LATENCY DEPENDENCY', body: 'We engineer for autonomous execution. If manual intervention is viewed as a virtue rather than a system failure, your operational culture is fundamentally incompatible with our infrastructure.' },
];

const ExclusionCard = ({ num, title, body }) => {
  const [hover, setHover] = React.useState(false);
  return (
    <div
      onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
      style={{
        display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 32,
        padding: 40, background: 'var(--surface-1)',
        border: `1px solid ${hover ? 'color-mix(in srgb, var(--brand) 40%, transparent)' : 'rgba(255,255,255,0.05)'}`,
        transition: 'border-color 0.3s var(--ease)',
      }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 16, maxWidth: 520 }}>
        <span style={{
          fontFamily: 'var(--font-mono)', fontSize: 9, color: 'var(--green)',
          letterSpacing: '0.5em', textTransform: 'uppercase', opacity: 0.55,
        }}>EXCLUSION_PRINCIPLE_{String(num).padStart(2,'0')}</span>
        <h3 style={{
          margin: 0, color: hover ? 'var(--brand)' : '#fff',
          fontFamily: 'var(--font-display)', fontWeight: 900,
          fontSize: 'clamp(1.4rem, 2vw, 1.9rem)',
          letterSpacing: '-0.01em', textTransform: 'uppercase',
          transition: 'color 0.3s var(--ease)',
        }}>{title}</h3>
        <p style={{
          margin: 0, color: 'rgba(255,255,255,0.55)', fontFamily: 'var(--font-body)',
          fontSize: 15, lineHeight: 1.55, maxWidth: 480,
        }}>{body}</p>
      </div>
      <div style={{
        width: 48, height: 48, flexShrink: 0, marginTop: 4,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        border: `1px solid ${hover ? 'var(--brand)' : 'rgba(255,255,255,0.1)'}`,
        transition: 'border-color 0.3s var(--ease)',
      }}>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
             style={{ stroke: 'var(--brand)' }}
             strokeWidth="4" strokeLinecap="round" strokeLinejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
      </div>
    </div>
  );
};

const AntiClient = () => {
  const left = EXCLUSIONS.slice(0,2);
  const right = EXCLUSIONS.slice(2);
  return (
    <section id="anti-client" style={{
      position: 'relative', padding: '96px 40px', background: '#000',
      borderTop: '1px solid rgba(255,255,255,0.05)',
      borderBottom: '1px solid rgba(255,255,255,0.05)',
      overflow: 'hidden',
    }}>
      {/* Huge BG text */}
      <div aria-hidden style={{
        position: 'absolute', inset: 0,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        opacity: 0.02, pointerEvents: 'none', userSelect: 'none',
      }}>
        <span style={{
          fontSize: '30vw', fontFamily: 'var(--font-display)', fontWeight: 900,
          letterSpacing: '-0.05em', lineHeight: 1, textTransform: 'uppercase',
          transform: 'rotate(-12deg)',
        }}>NOT_FOR_ALL</span>
      </div>

      <div style={{
        position: 'relative', maxWidth: 1280, margin: '0 auto',
        display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 64,
      }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
          <SectionHeader eyebrow="Access Control" line1="Non-Negotiable Parameters."/>
          <p style={{
            margin: 0, color: 'rgba(255,255,255,0.6)',
            fontFamily: 'var(--font-body)', fontSize: 16, lineHeight: 1.65,
            borderLeft: '2px solid color-mix(in srgb, var(--brand) 40%, transparent)', paddingLeft: 32, maxWidth: 480,
          }}>
            AGLAYA is an engineering firm, not a creative boutique. We optimize for Infrastructure Sovereignty, not corporate comfort. If you are looking for a partner to validate your current inefficiencies, find a traditional agency. If you need to build a sovereign engine, let's talk.
          </p>
          <div style={{
            display: 'flex', alignItems: 'center', gap: 16,
            color: 'var(--green)', fontFamily: 'var(--font-mono)',
            fontSize: 10, letterSpacing: '0.4em', textTransform: 'uppercase', opacity: 0.6,
          }}>
            <span>OPERATIONAL_INTEGRITY</span>
            <div style={{ width: 48, height: 1, background: 'color-mix(in srgb, var(--brand) 20%, transparent)' }}/>
          </div>
          {left.map((e,i) => <ExclusionCard key={i} num={i+1} {...e}/>)}
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
          {right.map((e,i) => <ExclusionCard key={i} num={i+3} {...e}/>)}
          <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
            <div style={{
              display: 'flex', alignItems: 'center', gap: 12,
              fontFamily: 'var(--font-mono)', fontSize: 10,
              color: 'rgba(255,255,255,0.2)', letterSpacing: '0.3em', textTransform: 'uppercase',
            }}>
              <span>INTEGRITY_CHECK: PASSED</span>
              {[...Array(4)].map((_,i) => (
                <span key={i} style={{
                  width: 8, height: 8, borderRadius: '50%',
                  background: 'color-mix(in srgb, var(--brand) 40%, transparent)',
                  animation: 'pulse 1.6s ease-in-out infinite',
                  animationDelay: `${i*0.2}s`,
                }}/>
              ))}
            </div>
          </div>
        </div>
      </div>
      <style>{`@keyframes pulse { 0%,100% { opacity: 0.4; } 50% { opacity: 1; } }`}</style>
    </section>
  );
};

window.AntiClient = AntiClient;
