// AGLAYA UI Kit — Problem grid. 6 cards, codetag eyebrow, growing hover rule.

const PROBLEMS = [
  { title: 'The Rental Trap', body: "Stop building your empire on rented soil. When you hire a traditional agency, you're merely financing their portfolio. The moment the contract ends, they walk away with your accounts, your automations, and your hard-earned knowledge." },
  { title: 'Training Your Executioner', body: 'SaaS is not a tool; it\u2019s a parasite feeding on your business logic. Every "winning pattern" you upload to a shared cloud is an unpaid consulting session for the algorithm.' },
  { title: 'Digital Serfdom', body: "If you don\u2019t own the code, you don\u2019t own the company. Relying on shared servers is like broadcasting your secret recipe over a public radio frequency." },
  { title: 'The AGLAYA Fortress', body: "We don\u2019t create dependency; we build fortresses. We hand you the keys to your own infrastructure so that when we leave the room, the machine keeps humming." },
  { title: 'The Data Donor Myth', body: "Every subscription you pay is a micro-bet against your own long-term relevance. You\u2019re trading proprietary intelligence for a shiny interface." },
  { title: 'The Cost of Sovereignty', body: "Ownership is uncomfortable because it demands responsibility, but the alternative is digital obsolescence. Stop renting your future." },
];

const ProblemCard = ({ i, title, body }) => {
  const [hover, setHover] = React.useState(false);
  return (
    <article
      onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
      style={{
        position: 'relative', overflow: 'hidden',
        display: 'flex', flexDirection: 'column',
        padding: 32,
        background: 'var(--surface-2)',
        border: `1px solid ${hover ? 'rgba(232,0,61,0.4)' : 'rgba(255,255,255,0.05)'}`,
        transition: 'border-color 0.5s var(--ease)',
      }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 24 }}>
        <span style={{
          fontFamily: 'var(--font-mono)', fontSize: 9, color: 'var(--green)',
          textTransform: 'uppercase', letterSpacing: '0.4em', opacity: 0.7,
        }}>LOGIC_NODE_{String(i+1).padStart(3,'0')}</span>
        <span style={{
          width: 4, height: 4,
          background: hover ? 'var(--brand)' : 'rgba(232,0,61,0.4)',
          transition: 'background 0.3s var(--ease)',
        }}/>
      </div>
      <h3 style={{
        margin: '0 0 16px', color: hover ? 'var(--brand)' : '#fff',
        fontFamily: 'var(--font-display)', fontWeight: 900,
        fontSize: 24, letterSpacing: '-0.02em', textTransform: 'uppercase',
        transition: 'color 0.3s var(--ease)',
      }}>{title}</h3>
      <p style={{
        margin: 0, color: hover ? 'rgba(255,255,255,0.7)' : 'rgba(255,255,255,0.4)',
        fontFamily: 'var(--font-body)', fontSize: 14, lineHeight: 1.6,
        transition: 'color 0.5s var(--ease)',
      }}>{body}</p>
      <div style={{
        marginTop: 32, height: 1,
        width: hover ? '100%' : 32,
        background: hover ? 'rgba(232,0,61,0.2)' : 'rgba(255,255,255,0.1)',
        transition: 'all 0.7s var(--ease)',
      }}/>
    </article>
  );
};

const Problem = () => (
  <section id="problem" style={{
    padding: '80px 40px', borderTop: '1px solid rgba(255,255,255,0.05)',
    background: '#000',
  }}>
    <div style={{ maxWidth: 1280, margin: '0 auto', display: 'flex', flexDirection: 'column', gap: 48 }}>
      <SectionHeader
        eyebrow="Not your typical agency"
        line1="Agencies sell hours."
        line2="We sell sovereignty."/>
      <div style={{
        display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 24,
      }}>
        {PROBLEMS.map((p, i) => <ProblemCard key={i} i={i} {...p}/>)}
      </div>
      <div style={{
        display: 'flex', justifyContent: 'flex-end', alignItems: 'center', gap: 24,
        marginTop: 40, opacity: 0.5,
      }}>
        <span style={{
          fontFamily: 'var(--font-mono)', fontSize: 10, color: '#fff',
          letterSpacing: '0.5em', textTransform: 'uppercase',
        }}>REF_ID: 001_SOVEREIGNTY_LOGIC</span>
        <div style={{ display: 'flex', gap: 4 }}>
          {[...Array(5)].map((_,i) => <div key={i} style={{ width: 6, height: 6, background: 'var(--green)' }}/>)}
        </div>
      </div>
    </div>
  </section>
);

window.Problem = Problem;
