import type { TraceStep } from "../engine/types";
import { cardId } from "./palos";

/** Map each card id to a location key (stack name, "@hand", or facing change). */
function locations(step: TraceStep): Map<string, string> {
  const loc = new Map<string, string>();
  for (const [name, cards] of Object.entries(step.stacks)) {
    for (const c of cards) loc.set(cardId(c), `${name}:${c.f}`);
  }
  if (step.hand) loc.set(cardId(step.hand), `@hand:${step.hand.f}`);
  return loc;
}

/** Card ids whose location or facing changed between two steps. */
export function movedCardIds(prev: TraceStep | null, cur: TraceStep): Set<string> {
  const moved = new Set<string>();
  if (!prev) return moved;
  const before = locations(prev);
  const after = locations(cur);
  for (const [id, where] of after) {
    if (before.get(id) !== where) moved.add(id);
  }
  return moved;
}
