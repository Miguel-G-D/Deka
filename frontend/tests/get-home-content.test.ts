import { describe, expect, it } from "vitest";

import { getHomeContent } from "@/application/get-home-content";
import { createAppInfo } from "@/domain/app-info";
import { getApiBaseUrl } from "@/infrastructure/api-client";
import { cn } from "@/presentation/lib/utils";

describe("domain", () => {
  it("creates app info", () => {
    const info = createAppInfo("Deka", "tag");
    expect(info.name).toBe("Deka");
    expect(info.tagline).toBe("tag");
  });
});

describe("application", () => {
  it("returns home content", () => {
    const content = getHomeContent();
    expect(content.name).toBe("Deka");
    expect(content.tagline).toContain("bars");
  });
});

describe("infrastructure", () => {
  it("defaults api base url", () => {
    expect(getApiBaseUrl()).toContain("8000");
  });
});

describe("presentation utils", () => {
  it("merges class names", () => {
    expect(cn("px-2", "px-4")).toBe("px-4");
  });
});
