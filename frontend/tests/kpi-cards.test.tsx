import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { KpiCards } from "@/presentation/components/kpi-cards";
import { ProcessesTable } from "@/presentation/components/processes-table";

describe("dashboard presentation", () => {
  it("renders KPI values", () => {
    render(
      <KpiCards
        summary={{
          totalProcesses: 10,
          interestedCount: 3,
          reservedCount: 3,
          confirmedCount: 4,
          needsHumanCount: 2,
          totalPartySize: 40,
          activitySeries: [],
        }}
      />,
    );
    expect(screen.getByText("Total processes")).toBeTruthy();
    expect(screen.getByText("10")).toBeTruthy();
    expect(screen.getByText("Needs human")).toBeTruthy();
  });

  it("renders process rows", () => {
    render(
      <ProcessesTable
        processes={[
          {
            processId: "proc-1",
            clientId: "cli-1",
            clientName: "Ana Pérez",
            status: "interested",
            partySize: 2,
            spaceType: "table",
            receivedAt: "2026-11-20T10:00:00+00:00",
            needsHuman: true,
          },
          {
            processId: "proc-2",
            clientId: "cli-2",
            clientName: "Bruno Díaz",
            status: "confirmed",
            partySize: 4,
            spaceType: "terrace",
            receivedAt: "2026-11-21T10:00:00+00:00",
            needsHuman: false,
          },
        ]}
      />,
    );
    expect(screen.getByText("Ana Pérez")).toBeTruthy();
    expect(screen.getByText("proc-1")).toBeTruthy();
    expect(screen.getByText("Yes")).toBeTruthy();
    expect(screen.getByText("No")).toBeTruthy();
  });
});

