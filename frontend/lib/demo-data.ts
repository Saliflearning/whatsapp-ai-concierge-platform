import type { ConversationSummary, DemoScenario } from "./types";

export const scenarios: DemoScenario[] = [
  {
    id: "hours",
    prompt: "Are appointments available on Saturday?",
    route: "grounded",
    response:
      "Based on the approved demo source “Synthetic service hours”: Demo appointments are available Saturday 10:00–14:00.",
    reason: "approved_knowledge",
    evidence: "Synthetic service hours · approved tenant source",
  },
  {
    id: "sensitive",
    prompt: "Is this a safe neighborhood?",
    route: "handoff",
    response:
      "I cannot verify that from approved demo information. A human operator should review this request.",
    reason: "policy_boundary",
  },
  {
    id: "unknown",
    prompt: "Can you promise a specific closing date?",
    route: "handoff",
    response:
      "I cannot verify that from approved demo information. A human operator should review this request.",
    reason: "insufficient_evidence",
  },
];

export const conversations: ConversationSummary[] = [
  { label: "Demo visitor 104", locale: "EN", status: "grounded", reason: "Service hours" },
  { label: "Demo visitor 219", locale: "FR", status: "needs review", reason: "Policy boundary" },
  { label: "Demo visitor 087", locale: "ES", status: "resolved", reason: "Human reviewed" },
];
