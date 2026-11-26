import path from "path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

const srcDir = path.resolve(__dirname, "src");

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    include: ["tests/**/*.{test,spec}.{ts,tsx}"],
    coverage: {
      provider: "v8",
      reporter: ["text", "html"],
      all: false,
      include: [
        "src/domain/app-info.ts",
        "src/domain/legal.ts",
        "src/application/**/*.ts",
        "src/infrastructure/**/*.ts",
        "src/presentation/lib/**/*.ts",
        "src/presentation/components/kpi-cards.tsx",
        "src/presentation/components/processes-table.tsx",
        "src/presentation/components/ui/badge.tsx",
        "src/presentation/components/ui/card.tsx",
      ],
      exclude: ["src/**/index.ts", "src/app/**", "src/domain/process.ts"],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
  },
  resolve: {
    alias: {
      "@": srcDir,
    },
  },
});
