import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { getPrivacyContent } from "@/application/get-privacy-content";
import { getTermsContent } from "@/application/get-terms-content";
import { LEGAL_CONTACT_EMAIL } from "@/domain/legal";
import { PrivacyView } from "@/presentation/views/privacy-view";
import { TermsView } from "@/presentation/views/terms-view";

describe("getPrivacyContent", () => {
  it("returns Spanish privacy copy with contact and data-deletion", () => {
    const content = getPrivacyContent();
    expect(content.title).toMatch(/privacidad/i);
    expect(content.contactEmail).toBe(LEGAL_CONTACT_EMAIL);
    expect(content.contactEmail).toBe("miguelgiradu@gmail.com");
    const deletion = content.sections.find((s) => s.id === "data-deletion");
    expect(deletion).toBeDefined();
    expect(deletion?.body).toContain(LEGAL_CONTACT_EMAIL);
    expect(
      content.sections.some((s) =>
        s.body.toLowerCase().includes("no almacena"),
      ),
    ).toBe(true);
  });
});

describe("getTermsContent", () => {
  it("returns Spanish terms with contact email", () => {
    const content = getTermsContent();
    expect(content.title).toMatch(/condiciones/i);
    expect(content.contactEmail).toBe("miguelgiradu@gmail.com");
    expect(
      content.sections.some((s) => s.body.includes(LEGAL_CONTACT_EMAIL)),
    ).toBe(true);
  });
});

describe("PrivacyView", () => {
  it("renders title, deletion anchor, and contact", () => {
    render(<PrivacyView />);
    expect(
      screen.getByRole("heading", { name: /política de privacidad/i }),
    ).toBeTruthy();
    expect(
      screen.getByRole("heading", { name: /eliminación de datos/i }),
    ).toBeTruthy();
    expect(document.getElementById("data-deletion")).toBeTruthy();
    expect(screen.getAllByText(/miguelgiradu@gmail.com/).length).toBeGreaterThan(
      0,
    );
  });
});

describe("TermsView", () => {
  it("renders terms heading", () => {
    render(<TermsView />);
    expect(
      screen.getByRole("heading", { name: /condiciones del servicio/i }),
    ).toBeTruthy();
  });
});
