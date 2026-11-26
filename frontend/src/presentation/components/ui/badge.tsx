import type { HTMLAttributes } from "react";

import { cn } from "@/presentation/lib/utils";

const statusStyles: Record<string, string> = {
  interested:
    "bg-[color-mix(in_srgb,var(--color-brand)_18%,white)] text-[var(--color-text-strong)]",
  reserved:
    "bg-[color-mix(in_srgb,var(--color-brand)_28%,white)] text-[var(--color-text-strong)]",
  confirmed:
    "bg-[color-mix(in_srgb,var(--color-brand)_40%,white)] text-[var(--color-text-strong)]",
  default:
    "bg-[var(--color-stroke-weak)] text-[var(--color-text-weak)]",
};

export function Badge({
  className,
  tone = "default",
  ...props
}: HTMLAttributes<HTMLSpanElement> & { tone?: keyof typeof statusStyles }) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-[var(--radius-sm)] px-[var(--space-2)] py-[var(--space-1)] text-xs font-medium capitalize",
        statusStyles[tone] ?? statusStyles.default,
        className,
      )}
      {...props}
    />
  );
}
