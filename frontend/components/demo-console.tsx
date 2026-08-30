"use client";

import { useState } from "react";

import { scenarios } from "@/lib/demo-data";
import type { DemoScenario } from "@/lib/types";

import { StatusPill } from "./status-pill";

export function DemoConsole() {
  const [active, setActive] = useState<DemoScenario>(scenarios[0]);
  const [resolved, setResolved] = useState(false);

  function selectScenario(scenario: DemoScenario) {
    setActive(scenario);
    setResolved(false);
  }

  return (
    <section className="console" aria-labelledby="console-title">
      <div className="console-head">
        <div>
          <p className="eyebrow">Interactive policy trace</p>
          <h2 id="console-title">See the decision, evidence, and audit trail</h2>
        </div>
        <span className="live"><i /> Local synthetic mode</span>
      </div>
      <div className="scenario-tabs" role="group" aria-label="Synthetic scenarios">
        {scenarios.map((scenario) => (
          <button
            className={active.id === scenario.id ? "active" : ""}
            key={scenario.id}
            onClick={() => selectScenario(scenario)}
          >
            {scenario.id === "hours" ? "Grounded answer" : scenario.id === "sensitive" ? "Policy boundary" : "Unknown claim"}
          </button>
        ))}
      </div>
      <div className="trace-grid">
        <div className="phone" aria-label="Synthetic message preview">
          <div className="phone-bar"><span>Northstar Demo</span><small>Synthetic tenant</small></div>
          <div className="chat">
            <p className="bubble inbound">{active.prompt}</p>
            <p className="bubble outbound">{active.response}</p>
          </div>
        </div>
        <div className="decision-panel">
          <div className="decision-top">
            <StatusPill route={resolved ? "grounded" : active.route} />
            <code>{resolved ? "operator_resolved" : active.reason}</code>
          </div>
          <div className="trace-row"><span>01</span><div><b>Tenant boundary</b><p>Request authenticated and scoped to Northstar Demo.</p></div></div>
          <div className="trace-row"><span>02</span><div><b>Policy decision</b><p>{active.route === "grounded" ? "Approved evidence matched." : "Automation stopped safely."}</p></div></div>
          <div className="trace-row"><span>03</span><div><b>Audit event</b><p>Reason code and source reference recorded atomically.</p></div></div>
          {active.evidence ? <div className="evidence"><small>Evidence</small><strong>{active.evidence}</strong></div> : null}
          {active.route === "handoff" && !resolved ? (
            <button className="resolve" onClick={() => setResolved(true)}>Resolve synthetic handoff</button>
          ) : null}
          {resolved ? <p className="resolved-note" role="status">Handoff resolved · immutable audit event appended</p> : null}
        </div>
      </div>
    </section>
  );
}
