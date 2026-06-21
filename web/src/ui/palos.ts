import type { Palo } from "../engine/cards";

export interface PaloInfo {
  name: string;
  color: string;
  symbol: string;
}

// Spanish suits mapped to a readable color + pip. (Not the French suits, but
// distinct and legible cross-platform.)
export const PALOS: Record<Palo, PaloInfo> = {
  O: { name: "Oro", color: "#c79a1e", symbol: "●" },
  C: { name: "Copa", color: "#b03a3a", symbol: "♥" },
  E: { name: "Espada", color: "#27408b", symbol: "♠" },
  B: { name: "Basto", color: "#2e7d4f", symbol: "♣" },
};

/** Stable per-card id: value+palo is unique within a program. */
export function cardId(card: { v: number; p: string }): string {
  return `${card.v}${card.p}`;
}
