export type LegalSection = {
  id: string;
  heading: string;
  body: string;
};

export type LegalPageContent = {
  title: string;
  lastUpdated: string;
  contactEmail: string;
  intro: string;
  sections: LegalSection[];
};

export const LEGAL_CONTACT_EMAIL = "miguelgiradu@gmail.com";

export function createLegalPageContent(
  content: LegalPageContent,
): LegalPageContent {
  return content;
}
