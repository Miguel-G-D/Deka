"use client";

import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { ActivityPoint } from "@/domain/process";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/presentation/components/ui/card";

type ActivityChartProps = {
  series: ActivityPoint[];
};

export function ActivityChart({ series }: ActivityChartProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Process volume</CardTitle>
        <p className="text-sm text-[var(--color-text-weak)]">
          Conversations received by day
        </p>
      </CardHeader>
      <CardContent className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={series}>
            <CartesianGrid stroke="var(--color-stroke-weak)" vertical={false} />
            <XAxis
              dataKey="date"
              tick={{ fill: "var(--color-text-weak)", fontSize: 12 }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              allowDecimals={false}
              tick={{ fill: "var(--color-text-weak)", fontSize: 12 }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip />
            <Area
              type="monotone"
              dataKey="count"
              stroke="var(--color-brand)"
              fill="color-mix(in srgb, var(--color-brand) 35%, white)"
              strokeWidth={2}
            />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
