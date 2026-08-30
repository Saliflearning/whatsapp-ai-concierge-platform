import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { DemoConsole } from "@/components/demo-console";

describe("DemoConsole", () => {
  it("shows grounded evidence", () => {
    render(<DemoConsole />);
    expect(screen.getByText(/Synthetic service hours · approved tenant source/)).toBeInTheDocument();
    expect(screen.getByText("Grounded")).toBeInTheDocument();
  });

  it("shows and resolves a human handoff", () => {
    render(<DemoConsole />);
    fireEvent.click(screen.getByRole("button", { name: "Policy boundary" }));
    expect(screen.getByText("Human handoff")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Resolve synthetic handoff" }));
    expect(screen.getByRole("status")).toHaveTextContent("immutable audit event appended");
  });
});
