import type { DashboardSummary } from "@/domain/process";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/presentation/components/ui/card";

type KpiCardsProps = {
  summary: DashboardSummary;
};

export function KpiCards({ summary }: KpiCardsProps) {
  const items = [
    {
      title: "Total processes",
      value: String(summary.totalProcesses),
      hint: "Active reservation conversations",
    },
    {
      title: "Confirmed",
      value: String(summary.confirmedCount),
      hint: "Ready for the venue",
    },
    {
      title: "Needs human",
      value: String(summary.needsHumanCount),
      hint: "Escalations waiting",
    },
    {
      title: "Party seats",
      value: String(summary.totalPartySize),
      hint: "Guests across all processes",
    },
  ];

  return (
    <div className="grid gap-[var(--space-4)] md:grid-cols-2 xl:grid-cols-4">
      {items.map((item) => (
        <Card key={item.title}>
          <CardHeader>
            <CardTitle>{item.title}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-semibold text-[var(--color-text-strong)]">
              {item.value}
            </p>
            <p className="mt-[var(--space-2)] text-sm text-[var(--color-text-weak)]">
              {item.hint}
            </p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
