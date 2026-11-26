import { getDashboardData } from "@/application/get-dashboard-data";
import { ActivityChart } from "@/presentation/components/activity-chart";
import { AppSidebar } from "@/presentation/components/app-sidebar";
import { KpiCards } from "@/presentation/components/kpi-cards";
import { ProcessesTable } from "@/presentation/components/processes-table";

export async function DashboardView() {
  const { summary, processes } = await getDashboardData();

  return (
    <div className="flex min-h-screen bg-[var(--color-bg)]">
      <AppSidebar />
      <main className="flex-1 space-y-[var(--space-6)] p-[var(--space-6)]">
        <header>
          <h1 className="text-2xl font-semibold text-[var(--color-text-strong)]">
            Dashboard
          </h1>
          <p className="text-sm text-[var(--color-text-weak)]">
            Reservation processes for the café pilot
          </p>
        </header>
        <KpiCards summary={summary} />
        <ActivityChart series={summary.activitySeries} />
        <ProcessesTable processes={processes} />
      </main>
    </div>
  );
}
