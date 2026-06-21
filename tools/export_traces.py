#!/usr/bin/env python3
"""Export canonical execution traces as JSON fixtures for the web engine.

Runs every program in examples/ (plus a few inline edge cases) through the
Python reference engine and writes one JSON file per program into
web/src/engine/__fixtures__/. The TypeScript engine's vitest suite loads these
and asserts it produces identical traces, keeping the two engines in lockstep.

Usage:
    py tools/export_traces.py
"""

import json
import pathlib

from retruco.trace import run_to_trace

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"
OUT_DIR = ROOT / "web" / "src" / "engine" / "__fixtures__"

# Small inline programs that exercise error paths the examples don't.
INLINE = {
    "err_empty_stack": (
        "UCP EJECUTE CON LAS SIGUIENTES CARTAS\n"
        "LA PILA MAZO NO TIENE CARTAS;\n\n"
        "DEFINICION DE PROGRAMA\n"
        "TOME UNA CARTA DE LA PILA MAZO\n"
    ),
    "err_empty_hand": (
        "UCP EJECUTE CON LAS SIGUIENTES CARTAS\n"
        "LA PILA MAZO TIENE 1 DE OROS BOCA ARRIBA,\n"
        "LA PILA DESTINO NO TIENE CARTAS;\n\n"
        "DEFINICION DE PROGRAMA\n"
        "DEPOSITE LA CARTA EN PILA DESTINO\n"
    ),
}


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = []

    programs = {path.stem: path.read_text(encoding="utf-8")
                for path in sorted(EXAMPLES.glob("*.timba"))}
    programs.update(INLINE)

    for name, source in programs.items():
        trace = run_to_trace(source)
        # Embed the source so the TS cross-check is self-contained.
        fixture = {"source": source, **trace}
        out = OUT_DIR / f"{name}.json"
        out.write_text(json.dumps(fixture, indent=2) + "\n", encoding="utf-8")
        written.append((name, len(trace["steps"]), trace["halted"]))

    print(f"Wrote {len(written)} fixtures to {OUT_DIR.relative_to(ROOT)}:")
    for name, steps, halted in written:
        print(f"  - {name}: {steps} steps, halted={halted}")


if __name__ == "__main__":
    main()
