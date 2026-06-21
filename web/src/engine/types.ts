import type { Palo } from "./cards";

export type Facing = "up" | "down";
export type Halted = "ok" | "error" | "maxsteps";

/** A card as serialized in a trace snapshot. Value+palo uniquely identify it. */
export interface CardRepr {
  v: number;
  p: Palo;
  f: Facing;
}

export interface TraceStep {
  index: number;
  pc: number | null;
  opcode: string | null;
  stacks: Record<string, CardRepr[]>;
  hand: CardRepr | null;
}

export interface TraceError {
  code: number;
  name: string;
}

export interface Trace {
  stackOrder: string[];
  steps: TraceStep[];
  halted: Halted;
  error: TraceError | null;
}
