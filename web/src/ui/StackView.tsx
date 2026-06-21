import type { CardRepr } from "../engine/types";
import { CardView } from "./CardView";
import { cardId } from "./palos";

interface StackViewProps {
  name: string;
  cards: CardRepr[];
  /** ids of cards to highlight this step. */
  activeIds?: Set<string>;
}

export function StackView({ name, cards, activeIds }: StackViewProps) {
  // Cards are bottom -> top. Rendered in order and overlapped downward by CSS,
  // so the top-of-stack is the last child: lowest in the column, fully visible,
  // and painted on top (correct z-order without z-index juggling).
  return (
    <div className="stack">
      <div className="stack-label">{name}</div>
      <div className="stack-cards">
        {cards.length === 0 ? (
          <div className="slot-empty">vacía</div>
        ) : (
          cards.map((c) => (
            <CardView key={cardId(c)} card={c} active={activeIds?.has(cardId(c))} />
          ))
        )}
      </div>
    </div>
  );
}
