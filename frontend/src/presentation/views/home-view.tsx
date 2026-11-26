import { getHomeContent } from "@/application/get-home-content";

export function HomeView() {
  const content = getHomeContent();

  return (
    <main
      style={{
        padding: "var(--space-10)",
        maxWidth: "40rem",
      }}
    >
      <h1
        style={{
          color: "var(--color-text-strong)",
          marginBottom: "var(--space-2)",
        }}
      >
        {content.name}
      </h1>
      <p style={{ color: "var(--color-text-weak)", margin: 0 }}>
        {content.tagline}
      </p>
    </main>
  );
}
