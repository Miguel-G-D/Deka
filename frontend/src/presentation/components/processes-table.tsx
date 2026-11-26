import type { ProcessRow } from "@/domain/process";
import { Badge } from "@/presentation/components/ui/badge";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/presentation/components/ui/card";

type ProcessesTableProps = {
  processes: ProcessRow[];
};

export function ProcessesTable({ processes }: ProcessesTableProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Processes</CardTitle>
        <p className="text-sm text-[var(--color-text-weak)]">
          Client conversations and reservation status
        </p>
      </CardHeader>
      <CardContent className="overflow-x-auto">
        <table className="w-full min-w-[48rem] border-collapse text-left text-sm">
          <thead>
            <tr className="border-b border-[var(--color-stroke-weak)] text-[var(--color-text-weak)]">
              <th className="px-[var(--space-3)] py-[var(--space-3)] font-medium">Process</th>
              <th className="px-[var(--space-3)] py-[var(--space-3)] font-medium">Client</th>
              <th className="px-[var(--space-3)] py-[var(--space-3)] font-medium">Status</th>
              <th className="px-[var(--space-3)] py-[var(--space-3)] font-medium">Party</th>
              <th className="px-[var(--space-3)] py-[var(--space-3)] font-medium">Space</th>
              <th className="px-[var(--space-3)] py-[var(--space-3)] font-medium">Received</th>
              <th className="px-[var(--space-3)] py-[var(--space-3)] font-medium">Human</th>
            </tr>
          </thead>
          <tbody>
            {processes.map((process) => (
              <tr
                key={process.processId}
                className="border-b border-[var(--color-stroke-weak)] text-[var(--color-text-strong)]"
              >
                <td className="px-[var(--space-3)] py-[var(--space-3)] font-mono text-xs">
                  {process.processId}
                </td>
                <td className="px-[var(--space-3)] py-[var(--space-3)]">
                  {process.clientName}
                </td>
                <td className="px-[var(--space-3)] py-[var(--space-3)]">
                  <Badge tone={process.status}>{process.status}</Badge>
                </td>
                <td className="px-[var(--space-3)] py-[var(--space-3)]">
                  {process.partySize}
                </td>
                <td className="px-[var(--space-3)] py-[var(--space-3)] capitalize">
                  {process.spaceType}
                </td>
                <td className="px-[var(--space-3)] py-[var(--space-3)]">
                  {new Date(process.receivedAt).toLocaleString()}
                </td>
                <td className="px-[var(--space-3)] py-[var(--space-3)]">
                  {process.needsHuman ? "Yes" : "No"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </CardContent>
    </Card>
  );
}
