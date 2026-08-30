import { DemoConsole } from "@/components/demo-console";
import { MetricCard } from "@/components/metric-card";
import { conversations } from "@/lib/demo-data";

const engineering = [
  ["01", "Trust boundary", "HMAC verification and tenant-scoped operator access reject unauthenticated and cross-tenant requests."],
  ["02", "Grounding policy", "The assistant answers only when approved same-tenant evidence matches. Otherwise, it hands off."],
  ["03", "Atomic evidence", "Messages, reason codes, sources, handoffs, and audit events commit in one transaction."],
  ["04", "Provider seam", "A local fake transport proves the workflow without paid APIs, credentials, or network calls."],
];

export default function Home() {
  return (
    <main>
      <nav className="nav shell" aria-label="Primary navigation">
        <a className="brand" href="#top"><span>WA</span> Concierge <i>Reference</i></a>
        <div><a href="#architecture">Architecture</a><a href="/demo">Demo</a><a href="#evidence">Evidence</a></div>
        <a className="repo-link" href="https://github.com/Saliflearning/whatsapp-ai-concierge-platform">View repository ↗</a>
      </nav>

      <header className="hero shell" id="top">
        <div className="hero-copy">
          <p className="eyebrow"><span /> Production-minded AI systems</p>
          <h1>Conversations that know when to <em>stop.</em></h1>
          <p className="lede">A privacy-safe reference platform for grounded, multilingual messaging workflows—with tenant isolation, explainable decisions, and human escalation built in.</p>
          <div className="hero-actions"><a className="primary" href="/demo">Explore the decision trace</a><a href="#architecture">Read the architecture</a></div>
          <div className="chips"><span>FastAPI</span><span>Next.js</span><span>SQLite</span><span>HMAC</span><span>Python 3.12</span></div>
        </div>
        <div className="system-card" aria-label="System flow">
          <div className="system-head"><span><i /> SYSTEM ONLINE</span><code>SYNTHETIC_MODE</code></div>
          <div className="flow-node start"><small>01 · INBOUND</small><b>Signed message</b><span>HMAC verified</span></div>
          <div className="connector" />
          <div className="flow-node"><small>02 · DECISION</small><b>Policy + grounding</b><span>Tenant-scoped evidence</span></div>
          <div className="branch"><div className="branch-line" /><div className="flow-node success"><small>MATCH</small><b>Grounded answer</b><span>Cited source</span></div><div className="flow-node caution"><small>NO MATCH</small><b>Human handoff</b><span>Reason recorded</span></div></div>
          <div className="system-foot"><span>NO PII</span><span>NO PAID APIs</span><span>FULL AUDIT</span></div>
        </div>
      </header>

      <section className="metrics shell" id="evidence">
        <MetricCard value="2" label="Isolated tenants" note="Cross-tenant access hidden" />
        <MetricCard value="3" label="Supported locales" note="English · French · Spanish" />
        <MetricCard value="100%" label="Audited decisions" note="Reason + evidence trace" />
        <MetricCard value="0" label="External services" note="Runs locally from clone" />
      </section>

      <section className="architecture shell" id="architecture">
        <div className="section-intro"><p className="eyebrow">Engineering decisions</p><h2>Safety is an architecture choice.</h2><p>Every boundary is visible, testable, and designed to fail closed.</p></div>
        <div className="engineering-grid">{engineering.map(([number, title, copy]) => <article key={number}><span>{number}</span><h3>{title}</h3><p>{copy}</p></article>)}</div>
      </section>

      <div className="demo-wrap" id="demo"><div className="shell"><DemoConsole /></div></div>

      <section className="operations shell">
        <div className="section-intro"><p className="eyebrow">Operator workspace</p><h2>Review without losing context.</h2><p>Synthetic conversations expose the operational state a human needs—not hidden chain-of-thought.</p></div>
        <div className="table-card"><div className="table-head"><strong>Conversation queue</strong><span>3 synthetic records</span></div>{conversations.map((item) => <div className="table-row" key={item.label}><b>{item.label}</b><span>{item.locale}</span><span className={`queue-${item.status.replace(" ", "-")}`}>{item.status}</span><span>{item.reason}</span></div>)}</div>
      </section>

      <footer><div className="shell"><div><b>Built as a clean-room engineering reference.</b><p>All businesses, people, messages, and credentials are synthetic.</p></div><div><span>MIT licensed</span><span>Reproducible locally</span><span>Security documented</span></div></div></footer>
    </main>
  );
}
