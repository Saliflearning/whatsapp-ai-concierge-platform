import type { DemoMessageRequest, DemoMessageResult } from "./types";

export async function submitSyntheticMessage(
  payload: DemoMessageRequest,
): Promise<DemoMessageResult> {
  const baseUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
  const business = process.env.NEXT_PUBLIC_DEMO_BUSINESS;
  const token = process.env.NEXT_PUBLIC_DEMO_TOKEN;
  if (!business || !token) {
    throw new Error("Synthetic API demo configuration is unavailable.");
  }
  const response = await fetch(`${baseUrl}/api/demo/messages`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-demo-business": business,
      "x-demo-token": token,
    },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error(`Synthetic API request failed (${response.status}).`);
  }
  return response.json() as Promise<DemoMessageResult>;
}
