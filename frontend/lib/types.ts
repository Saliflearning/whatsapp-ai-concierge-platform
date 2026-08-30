export type Route = "grounded" | "handoff";

export type DemoScenario = {
  id: string;
  prompt: string;
  route: Route;
  response: string;
  reason: string;
  evidence?: string;
};

export type ConversationSummary = {
  label: string;
  locale: string;
  status: "grounded" | "needs review" | "resolved";
  reason: string;
};

export type DemoMessageRequest = {
  event_id: string;
  customer_label: string;
  text: string;
  locale: "en" | "fr" | "es";
};

export type DemoMessageResult = {
  conversation_id: string;
  route: Route;
  response_text: string;
  reason_code: string;
  duplicate: boolean;
  handoff_id?: string;
  knowledge_source?: { id: string; label: string };
};
