import { type Card, Position } from "./cards";
import { Emitter } from "./emitter";
import { Lexer } from "./lexer";
import { Parser } from "./parser";
import type { CardRepr, Halted, Trace, TraceStep } from "./types";
import { VirtualMachine } from "./vm";

export const MAX_STEPS = 10000;

const ERROR_NAMES: Record<number, string> = {
  1: "FULL_HAND_ERROR",
  2: "EMPTY_STACK_ERROR",
  3: "EMPTY_HAND_ERROR",
  4: "LOGIC_CONDITION_ERROR",
  5: "FACE_DOWN_CARD_LOGIC_ERROR",
};

function cardRepr(card: Card): CardRepr {
  return {
    v: card.value,
    p: card.type as CardRepr["p"],
    f: card.position === Position.FACE_DOWN ? "down" : "up",
  };
}

function snapshotStacks(vm: VirtualMachine, names: string[]): Record<string, CardRepr[]> {
  const out: Record<string, CardRepr[]> = {};
  vm.stacks.forEach((stack, i) => {
    const name = i < names.length ? names[i] : String(i);
    out[name] = stack.map(cardRepr);
  });
  return out;
}

function snapshot(
  vm: VirtualMachine,
  names: string[],
  index: number,
  pc: number | null,
  opcode: string | null,
): TraceStep {
  return {
    index,
    pc,
    opcode,
    stacks: snapshotStacks(vm, names),
    hand: vm.hand !== null ? cardRepr(vm.hand) : null,
  };
}

/** Compile and run `source`, returning the full execution trace. */
export function runToTrace(source: string, maxSteps: number = MAX_STEPS): Trace {
  const lexer = new Lexer(source);
  const emitter = new Emitter();
  const parser = new Parser(lexer, emitter);
  parser.program();
  const names = [...parser.namesDeclared];

  const vm = new VirtualMachine(emitter.processInstructions, emitter.stacksInstructions);
  vm.loadStacks();

  const steps: TraceStep[] = [snapshot(vm, names, 0, null, null)];
  let halted: Halted = "ok";

  while (vm.pc !== vm.opcodes.length) {
    if (steps.length - 1 >= maxSteps) {
      halted = "maxsteps";
      break;
    }
    const pcBefore = vm.pc;
    const opcode = vm.opcodes[pcBefore];
    vm.executeInstruction();
    steps.push(snapshot(vm, names, steps.length, pcBefore, opcode));
    if (vm.errorCode !== 0) {
      halted = "error";
      break;
    }
  }

  const error =
    vm.errorCode !== 0 ? { code: vm.errorCode, name: ERROR_NAMES[vm.errorCode] } : null;

  return { stackOrder: names, steps, halted, error };
}
