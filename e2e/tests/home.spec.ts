import { expect, test } from "@playwright/test";

test("dashboard shows seeded process and client", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Dashboard" })).toBeVisible();
  await expect(page.getByText("Deka").first()).toBeVisible();
  await expect(page.getByText("Ana Pérez").first()).toBeVisible();
  await expect(page.getByText("proc-1").first()).toBeVisible();
  await expect(page.getByText("Total processes")).toBeVisible();
});
