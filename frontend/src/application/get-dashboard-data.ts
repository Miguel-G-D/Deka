import type { DashboardSummary, ProcessRow } from "@/domain/process";
import {
  fetchDashboardSummary,
  fetchProcesses,
} from "@/infrastructure/dashboard-api";

export type DashboardData = {
  summary: DashboardSummary;
  processes: ProcessRow[];
};

export async function getDashboardData(): Promise<DashboardData> {
  const [summary, processes] = await Promise.all([
    fetchDashboardSummary(),
    fetchProcesses(),
  ]);
  return { summary, processes };
}
