import {
  createLegalPageContent,
  LEGAL_CONTACT_EMAIL,
  type LegalPageContent,
} from "@/domain/legal";

export function getPrivacyContent(): LegalPageContent {
  return createLegalPageContent({
    title: "Política de privacidad",
    lastUpdated: "2026-11-26",
    contactEmail: LEGAL_CONTACT_EMAIL,
    intro:
      "Esta política describe cómo Deka trata la información en el piloto de reservas por Instagram. " +
      "Si necesitás solicitar la eliminación de datos, andá a la sección Eliminación de datos.",
    sections: [
      {
        id: "quienes-somos",
        heading: "Quiénes somos",
        body:
          "Deka es una plataforma piloto que ayuda a bares y cafés a gestionar consultas y reservas " +
          "mediante un agente conversacional en Instagram.",
      },
      {
        id: "datos",
        heading: "Qué datos intervienen",
        body:
          "En el flujo pueden aparecer mensajes de Instagram y datos que vos escribas para una reserva " +
          "(por ejemplo nombre, contacto, fecha, hora, cantidad de personas o espacio). " +
          "En esta fase piloto Deka no almacena de forma persistente esos datos personales en nuestros sistemas.",
      },
      {
        id: "finalidad",
        heading: "Para qué se usan",
        body:
          "Los usamos únicamente para responder consultas del menú u horarios y asistir el proceso de reserva " +
          "durante la conversación en curso.",
      },
      {
        id: "canal-meta",
        heading: "Canal Meta / Instagram",
        body:
          "Instagram (Meta) es el canal de mensajería: ellos procesan el transporte de los mensajes según sus " +
          "propias políticas. Deka recibe y responde a través de las APIs de Meta cuando están configuradas.",
      },
      {
        id: "conservacion",
        heading: "Conservación",
        body:
          "En este piloto no retenemos información personal identificable en Deka. " +
          "Si más adelante incorporamos persistencia (por ejemplo historial de reservas), actualizaremos esta política.",
      },
      {
        id: "derechos",
        heading: "Tus derechos",
        body:
          "Podés pedir información sobre el tratamiento, corrección o eliminación de datos relacionados con el piloto " +
          "escribiendo al contacto indicado más abajo.",
      },
      {
        id: "data-deletion",
        heading: "Eliminación de datos",
        body:
          `Para solicitar la eliminación de datos asociados a tu uso del piloto, escribí a ${LEGAL_CONTACT_EMAIL} ` +
          "indicando tu usuario de Instagram o el dato que querés borrar. Responderemos lo antes posible. " +
          "Como en esta fase no persistimos PII en Deka, la solicitud sirve sobre todo para confirmar que no " +
          "retenemos datos y para coordinar con el venue si hubiera registros fuera de Deka.",
      },
      {
        id: "contacto",
        heading: "Contacto",
        body: `Consultas de privacidad: ${LEGAL_CONTACT_EMAIL}.`,
      },
    ],
  });
}
