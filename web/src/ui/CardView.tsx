import type { CardRepr } from "../engine/types";
import { PALOS } from "./palos";

interface CardViewProps {
  card: CardRepr;
  /** Highlight the card (e.g. it moved or is being inspected this step). */
  active?: boolean;
}

export function CardView({ card, active }: CardViewProps) {
  if (card.f === "down") {
    return <div className={`card card-down${active ? " card-active" : ""}`} aria-label="carta boca abajo" />;
  }

  const palo = PALOS[card.p];
  return (
    <div
      className={`card${active ? " card-active" : ""}`}
      style={{ color: palo.color }}
      aria-label={`${card.v} de ${palo.name}`}
      title={`${card.v} de ${palo.name}`}
    >
      <span className="card-corner card-corner-tl">
        {card.v}
        <br />
        {palo.symbol}
      </span>
      <span className="card-pip">{palo.symbol}</span>
      <span className="card-corner card-corner-br">
        {card.v}
        <br />
        {palo.symbol}
      </span>
    </div>
  );
}
