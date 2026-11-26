import type { Metadata } from "next";

import { TermsView } from "@/presentation/views/terms-view";

export const metadata: Metadata = {
  title: "Condiciones del servicio | Deka",
  description:
    "Condiciones del servicio del piloto Deka para consultas y reservas por Instagram.",
};

export default function TermsPage() {
  return <TermsView />;
}
