import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { Badge } from "@/presentation/components/ui/badge";
import { HomeView } from "@/presentation/views/home-view";

describe("HomeView", () => {
  it("renders brand name and tagline", () => {
    render(<HomeView />);
    expect(screen.getByRole("heading", { name: "Deka" })).toBeTruthy();
    expect(screen.getByText(/bars and cafés/i)).toBeTruthy();
  });
});

describe("Badge", () => {
  it("falls back to default tone", () => {
    render(<Badge>fallback</Badge>);
    expect(screen.getByText("fallback")).toBeTruthy();
  });
});
