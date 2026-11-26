import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";
import { afterAll, afterEach, beforeAll, describe, expect, it } from "vitest";

import { getDashboardData } from "@/application/get-dashboard-data";
import {
  fetchClients,
  fetchDashboardSummary,
  fetchProcesses,
} from "@/infrastructure/dashboard-api";

const summaryPayload = {
  total_processes: 2,
  interested_count: 1,
  reserved_count: 0,
  confirmed_count: 1,
  needs_human_count: 1,
  total_party_size: 6,
  activity_series: [{ date: "2026-11-20", count: 2 }],
};

const processPayload = [
  {
    process_id: "proc-1",
    client_id: "cli-1",
    client_name: "Ana Pérez",
    status: "interested",
    party_size: 2,
    space_type: "table",
    received_at: "2026-11-20T10:00:00+00:00",
    needs_human: true,
  },
];

const clientPayload = [
  { id: "cli-1", name: "Ana Pérez", phone: "+5491100000001" },
];

const server = setupServer(
  http.get("http://127.0.0.1:8000/api/dashboard/summary", () =>
    HttpResponse.json(summaryPayload),
  ),
  http.get("http://127.0.0.1:8000/api/processes", () =>
    HttpResponse.json(processPayload),
  ),
  http.get("http://127.0.0.1:8000/api/clients", () =>
    HttpResponse.json(clientPayload),
  ),
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("dashboard API", () => {
  it("maps summary dto to domain", async () => {
    const summary = await fetchDashboardSummary();
    expect(summary.totalProcesses).toBe(2);
    expect(summary.activitySeries[0]?.count).toBe(2);
  });

  it("maps process rows", async () => {
    const rows = await fetchProcesses();
    expect(rows[0]?.clientName).toBe("Ana Pérez");
    expect(rows[0]?.needsHuman).toBe(true);
  });

  it("maps clients", async () => {
    const clients = await fetchClients();
    expect(clients[0]?.id).toBe("cli-1");
  });

  it("loads dashboard data via use case", async () => {
    const data = await getDashboardData();
    expect(data.summary.confirmedCount).toBe(1);
    expect(data.processes).toHaveLength(1);
  });

  it("throws when the API responds with an error", async () => {
    server.use(
      http.get("http://127.0.0.1:8000/api/dashboard/summary", () =>
        HttpResponse.json({ detail: "boom" }, { status: 500 }),
      ),
    );
    await expect(fetchDashboardSummary()).rejects.toThrow("Request failed: 500");
  });
});

