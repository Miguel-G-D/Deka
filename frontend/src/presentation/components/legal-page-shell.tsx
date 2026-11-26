import Link from "next/link";
import type { ReactNode } from "react";

type LegalPageShellProps = {
  title: string;
  lastUpdated: string;
  children: ReactNode;
};

export function LegalPageShell({
  title,
  lastUpdated,
  children,
}: LegalPageShellProps) {
  return (
    <main
      style={{
        padding: "var(--space-10)",
        maxWidth: "40rem",
        margin: "0 auto",
      }}
    >
      <header style={{ marginBottom: "var(--space-6)" }}>
        <p
          style={{
            color: "var(--color-text-strong)",
            fontWeight: 600,
            fontSize: "1.25rem",
            margin: 0,
            marginBottom: "var(--space-4)",
          }}
        >
          <Link
            href="/"
            style={{ color: "inherit", textDecoration: "none" }}
          >
            Deka
          </Link>
        </p>
        <nav
          style={{
            display: "flex",
            gap: "var(--space-4)",
            marginBottom: "var(--space-6)",
            fontSize: "0.875rem",
          }}
        >
          <Link
            href="/privacy"
            style={{ color: "var(--color-text-strong)" }}
          >
            Privacidad
          </Link>
          <Link href="/terms" style={{ color: "var(--color-text-strong)" }}>
            Condiciones
          </Link>
        </nav>
        <h1
          style={{
            color: "var(--color-text-strong)",
            margin: 0,
            marginBottom: "var(--space-2)",
            fontSize: "1.5rem",
            fontWeight: 600,
          }}
        >
          {title}
        </h1>
        <p
          style={{
            color: "var(--color-text-weak)",
            margin: 0,
            fontSize: "0.875rem",
          }}
        >
          Última actualización: {lastUpdated}
        </p>
      </header>
      {children}
      <footer
        style={{
          marginTop: "var(--space-8)",
          paddingTop: "var(--space-4)",
          borderTop: "var(--border) solid var(--color-stroke-weak)",
          fontSize: "0.875rem",
          color: "var(--color-text-weak)",
          display: "flex",
          gap: "var(--space-4)",
        }}
      >
        <Link href="/privacy" style={{ color: "var(--color-text-strong)" }}>
          Privacidad
        </Link>
        <Link href="/terms" style={{ color: "var(--color-text-strong)" }}>
          Condiciones
        </Link>
      </footer>
    </main>
  );
}
