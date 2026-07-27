// AGLAYA UI Kit — Hero section. Signature headline, eyebrow rule, two CTAs.

const Hero = () => (
  <section id="home" className="bg-scanlines" style={{
    position: 'relative', minHeight: '88vh',
    display: 'flex', flexDirection: 'column', justifyContent: 'center',
    padding: '120px 40px 80px', overflow: 'hidden',
  }}>
    {/* Aura */}
    <div style={{
      position: 'absolute', top: '50%', left: '25%',
      width: 500, height: 500,
      background: 'color-mix(in srgb, var(--brand) 8%, transparent)', filter: 'blur(120px)', borderRadius: '50%',
      transform: 'translateY(-50%)', pointerEvents: 'none',
    }}/>

    <div style={{
      position: 'relative', zIndex: 10, maxWidth: 1280, width: '100%', margin: '0 auto',
      display: 'flex', flexDirection: 'column', gap: 40,
    }}>
      <Eyebrow>We build systems that empower your business while you sleep</Eyebrow>

      <h1 style={{
        margin: 0, color: '#fff',
        fontFamily: 'var(--font-display)', fontWeight: 900,
        fontSize: 'clamp(3rem, 9vw, 9rem)', lineHeight: 0.94,
        letterSpacing: '-0.04em', textTransform: 'uppercase',
      }}>
        <span style={{ display: 'block' }}>The agency is dead.</span>
        <span style={{ display: 'block', color: 'var(--brand)' }}>Long live the system.</span>
      </h1>

      <div style={{ maxWidth: 560, display: 'flex', flexDirection: 'column', gap: 48 }}>
        <p style={{
          margin: 0, color: 'var(--muted)',
          fontFamily: 'var(--font-body)',
          fontSize: 'clamp(1.15rem, 1.5vw, 1.5rem)', lineHeight: 1.55,
        }}>
          Most teams don't need an agency. They need their own infrastructure.
          We build it. You own it. The system keeps running when we're not in the room.
        </p>

        <div style={{ display: 'flex', alignItems: 'center', gap: 32, flexWrap: 'wrap' }}>
          <PrimaryButton>Request Proposal →</PrimaryButton>
          <MonoLink>See the proof</MonoLink>
        </div>
      </div>
    </div>
  </section>
);

window.Hero = Hero;
