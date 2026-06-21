"""Structured execution traces for TIMBA programs.

`run_to_trace` compiles and runs a program, capturing a full state snapshot
after every instruction. The result is the canonical trace consumed by the web
playground's TypeScript engine cross-check (see web/src/engine) and is a clean,
JSON-serializable view of execution.
"""

from .compiler.emitter import Emitter
from .compiler.lexer import Lexer
from .compiler.parser import Parser
from .virtual_machine.cards import Position
from .virtual_machine.vm import VirtualMachine

MAX_STEPS = 10000

ERROR_NAMES = {
    1: "FULL_HAND_ERROR",
    2: "EMPTY_STACK_ERROR",
    3: "EMPTY_HAND_ERROR",
    4: "LOGIC_CONDITION_ERROR",
    5: "FACE_DOWN_CARD_LOGIC_ERROR",
}


def _card(card):
    return {
        "v": card.value,
        "p": card.type,
        "f": "down" if card.position == Position.FACE_DOWN else "up",
    }


def _snapshot_stacks(vm, names):
    out = {}
    for i, stack in enumerate(vm.stacks):
        name = names[i] if i < len(names) else str(i)
        out[name] = [_card(c) for c in stack]
    return out


def _snapshot(vm, names, index, pc, opcode):
    return {
        "index": index,
        "pc": pc,
        "opcode": opcode,
        "stacks": _snapshot_stacks(vm, names),
        "hand": _card(vm.hand) if vm.hand is not None else None,
    }


def run_to_trace(source, max_steps=MAX_STEPS):
    """Compile and run `source`, returning a JSON-serializable trace dict."""
    lexer = Lexer(source)
    emitter = Emitter()
    parser = Parser(lexer, emitter)
    parser.program()
    names = list(parser.names_declared)

    vm = VirtualMachine(emitter.process_instructions, emitter.stacks_instructions)
    vm.load_stacks()

    # Step 0 is the initial board, before any instruction executes.
    steps = [_snapshot(vm, names, 0, None, None)]
    halted = "ok"

    while vm.pc != len(vm.opcodes):
        if len(steps) - 1 >= max_steps:
            halted = "maxsteps"
            break
        pc_before = vm.pc
        opcode = vm.opcodes[pc_before]
        vm.execute_instruction()
        steps.append(_snapshot(vm, names, len(steps), pc_before, opcode))
        if vm.error_code != 0:
            halted = "error"
            break

    error = None
    if vm.error_code != 0:
        error = {"code": vm.error_code, "name": ERROR_NAMES.get(vm.error_code)}

    return {
        "stackOrder": names,
        "steps": steps,
        "halted": halted,
        "error": error,
    }
