import {
  createLegalPageContent,
  LEGAL_CONTACT_EMAIL,
  type LegalPageContent,
} from "@/domain/legal";

export function getTermsContent(): LegalPageContent {
  return createLegalPageContent({
    title: "Condiciones del servicio",
    lastUpdated: "2026-11-26",
    contactEmail: LEGAL_CONTACT_EMAIL,
    intro:
      "Estas condiciones aplican al uso del piloto de Deka para consultas y asistencia de reservas " +
      "a través de Instagram.",
    sections: [
      {
        id: "servicio",
        heading: "Descripción del servicio",
        body:
          "Deka ofrece un agente conversacional en fase piloto que responde preguntas (menú, horarios, " +
          "disponibilidad) y orienta el proceso de reserva para bares y cafés participantes.",
      },
      {
        id: "uso-aceptable",
        heading: "Uso aceptable",
        body:
          "Debés usar el servicio de forma lícita y respetuosa. No está permitido abusar del canal " +
          "(spam, acoso, intentos de vulnerar sistemas o suplantar identidades).",
      },
      {
        id: "venue",
        heading: "Relación con el venue",
        body:
          "La confirmación final de una reserva y las condiciones del local corresponden al bar o café. " +
          "Deka asiste la conversación; el venue es responsable de la prestación del servicio gastronómico.",
      },
      {
        id: "limitacion",
        heading: "Limitación de responsabilidad",
        body:
          "El piloto se ofrece «tal cual». Deka no garantiza disponibilidad continua ni la exactitud absoluta " +
          "de respuestas generadas automáticamente. En la medida permitida por la ley, no somos responsables " +
          "por daños indirectos derivados del uso del agente.",
      },
      {
        id: "contacto",
        heading: "Contacto",
        body: `Consultas sobre estas condiciones: ${LEGAL_CONTACT_EMAIL}.`,
      },
    ],
  });
}
