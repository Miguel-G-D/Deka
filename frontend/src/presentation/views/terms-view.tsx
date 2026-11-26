import { getTermsContent } from "@/application/get-terms-content";
import { LegalPageShell } from "@/presentation/components/legal-page-shell";

export function TermsView() {
  const content = getTermsContent();

  return (
    <LegalPageShell title={content.title} lastUpdated={content.lastUpdated}>
      <p
        style={{
          color: "var(--color-text-weak)",
          marginTop: 0,
          marginBottom: "var(--space-6)",
          lineHeight: 1.6,
        }}
      >
        {content.intro}
      </p>
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-6)" }}>
        {content.sections.map((section) => (
          <section key={section.id} id={section.id}>
            <h2
              style={{
                color: "var(--color-text-strong)",
                fontSize: "1.125rem",
                fontWeight: 600,
                margin: 0,
                marginBottom: "var(--space-2)",
              }}
            >
              {section.heading}
            </h2>
            <p
              style={{
                color: "var(--color-text-weak)",
                margin: 0,
                lineHeight: 1.6,
              }}
            >
              {section.body}
            </p>
          </section>
        ))}
      </div>
    </LegalPageShell>
  );
}
