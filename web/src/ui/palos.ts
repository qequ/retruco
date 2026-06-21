import type { Palo } from "../engine/cards";

export interface PaloInfo {
  /** Singular display name, used for accessible labels. */
  name: string;
}

// Spanish-deck suits (naipes españoles). Card faces are real images
// (see cardImageSrc); this map is just for labels.
export const PALOS: Record<Palo, PaloInfo> = {
  O: { name: "Oro" },
  C: { name: "Copa" },
  E: { name: "Espada" },
  B: { name: "Basto" },
};

/** Stable per-card id: value+palo is unique within a program. */
export function cardId(card: { v: number; p: string }): string {
  return `${card.v}${card.p}`;
}

const PALO_SLUG: Record<Palo, string> = {
  O: "oros",
  C: "copas",
  E: "espadas",
  B: "bastos",
};

/** Public URL of a card face image (baraja española). */
export function cardImageSrc(card: { v: number; p: Palo }): string {
  const v = String(card.v).padStart(2, "0");
  return `${import.meta.env.BASE_URL}cards/${v}-${PALO_SLUG[card.p]}.png`;
}

/** Public URL of the card-back image. */
export function cardBackSrc(): string {
  return `${import.meta.env.BASE_URL}cards/reverso.png`;
}
