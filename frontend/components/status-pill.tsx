import type { Route } from "@/lib/types";

export function StatusPill({ route }: { route: Route }) {
  return <span className={`status status-${route}`}>{route === "grounded" ? "Grounded" : "Human handoff"}</span>;
}
