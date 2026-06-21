import type { TraceStep } from "../engine/types";
import { CardView } from "./CardView";
import { cardId } from "./palos";
import { StackView } from "./StackView";

interface BoardProps {
  stackOrder: string[];
  step: TraceStep;
  /** ids of cards that moved on the transition into this step. */
  activeIds?: Set<string>;
}

export function Board({ stackOrder, step, activeIds }: BoardProps) {
  return (
    <div className="board">
      <div className="stacks-row">
        {stackOrder.map((name) => (
          <StackView
            key={name}
            name={name}
            cards={step.stacks[name] ?? []}
            activeIds={activeIds}
          />
        ))}
      </div>

      <div className="hand-zone">
        <div className="stack-label">MANO</div>
        <div className="hand-slot">
          {step.hand ? (
            <CardView card={step.hand} active={activeIds?.has(cardId(step.hand))} />
          ) : (
            <div className="slot-empty">vacía</div>
          )}
        </div>
      </div>
    </div>
  );
}
