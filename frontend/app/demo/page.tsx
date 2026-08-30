import { DemoConsole } from "@/components/demo-console";
import Link from "next/link";

export default function DemoPage() {
  return (
    <main className="standalone-demo">
      <nav className="nav shell" aria-label="Demo navigation">
        <Link className="brand" href="/"><span>WA</span> Concierge <i>Reference</i></Link>
        <Link className="repo-link" href="/">← Project overview</Link>
      </nav>
      <div className="shell standalone-demo-content">
        <DemoConsole />
        <p className="demo-disclaimer">
          This interaction is deterministic and uses fictional records. Connect the typed local API
          client to exercise the equivalent persisted workflow.
        </p>
      </div>
    </main>
  );
}
