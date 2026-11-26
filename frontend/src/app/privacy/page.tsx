import type { Metadata } from "next";

import { PrivacyView } from "@/presentation/views/privacy-view";

export const metadata: Metadata = {
  title: "Política de privacidad | Deka",
  description:
    "Política de privacidad del piloto Deka: reservas y consultas por Instagram.",
};

export default function PrivacyPage() {
  return <PrivacyView />;
}
