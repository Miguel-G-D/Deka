const navItems = [
  { label: "Dashboard", active: true },
  { label: "Processes", active: false },
  { label: "Clients", active: false },
  { label: "Spaces", active: false },
];

export function AppSidebar() {
  return (
    <aside className="flex w-64 shrink-0 flex-col border-r border-[var(--color-stroke-weak)] bg-[color-mix(in_srgb,var(--color-brand)_8%,white)] p-[var(--space-5)]">
      <div className="mb-[var(--space-6)]">
        <p className="text-xl font-semibold text-[var(--color-text-strong)]">Deka</p>
        <p className="text-sm text-[var(--color-text-weak)]">Café pilot</p>
      </div>
      <nav className="flex flex-1 flex-col gap-[var(--space-2)]">
        {navItems.map((item) => (
          <span
            key={item.label}
            className={
              item.active
                ? "rounded-[var(--radius-md)] bg-[var(--color-brand)] px-[var(--space-3)] py-[var(--space-2)] text-sm font-medium text-white"
                : "rounded-[var(--radius-md)] px-[var(--space-3)] py-[var(--space-2)] text-sm text-[var(--color-text-weak)]"
            }
          >
            {item.label}
          </span>
        ))}
      </nav>
      <div className="mt-auto border-t border-[var(--color-stroke-weak)] pt-[var(--space-4)] text-sm text-[var(--color-text-weak)]">
        Operator view
      </div>
    </aside>
  );
}
