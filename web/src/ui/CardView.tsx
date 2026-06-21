import type { CardRepr } from "../engine/types";
import { cardBackSrc, cardImageSrc, PALOS } from "./palos";

interface CardViewProps {
  card: CardRepr;
  /** Highlight the card (e.g. it moved or is being inspected this step). */
  active?: boolean;
}

export function CardView({ card, active }: CardViewProps) {
  const className = `card${active ? " card-active" : ""}`;

  if (card.f === "down") {
    return (
      <img className={className} src={cardBackSrc()} alt="carta boca abajo" draggable={false} />
    );
  }

  const label = `${card.v} de ${PALOS[card.p].name}`;
  return (
    <img
      className={className}
      src={cardImageSrc(card)}
      alt={label}
      title={label}
      draggable={false}
    />
  );
}
