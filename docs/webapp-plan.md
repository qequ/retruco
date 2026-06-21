# Retruco Playground — webapp plan

An interactive web playground for the TIMBA language: write a program in an
editor, run it, and step through execution watching cards move between the
stacks (`PILA`) and the hand (`MANO`).

**Decisions (locked):**
- **Engine:** port the VM to TypeScript, runs fully client-side.
- **Frontend:** React + Framer Motion.
- **v1 scope:** MVP stepper (editor + run + step/play/back/scrub + basic card
  animations + error display).

## A. Architecture at a glance
Everything runs in the browser; no backend.

```
Browser (static site)
  CodeMirror editor --source--> TS compiler --> {stackOps, processOps, srcMap}
                                     |
                                     v
                                 TS VM  --run once--> Trace (state[])
                                     |
        +----------------------------+----------------------------+
        v                                                         v
  Player controls (back/step/play/reset, timeline, speed)   Board renderer
        +------------------- currentStep ------------------> stacks + hand (Framer)
```

The compiler/VM mirror the existing Python pipeline (`lexer -> parser ->
emitter -> VM`), and the **Trace** is the single contract between engine and UI.

## B. The Trace contract (the linchpin)
Computed in one shot; the UI is a pure player over it. Cards carry **stable
IDs** assigned at stack-load, which is what makes animation almost free.

```ts
type Palo = 'O' | 'B' | 'E' | 'C';           // oro, basto, espada, copa
type Facing = 'up' | 'down';

interface Card { id: string; value: number; palo: Palo; }   // identity is fixed
interface CardState { facing: Facing; }                      // per-step, mutable

interface Step {
  index: number;
  pc: number;
  opcode: string;                 // e.g. "0INPUT", "7P0N"
  kind: 'take'|'deposit'|'invert'|'if'|'else'|'endif'|'while'|'endwhile';
  sourceLine: number | null;      // for editor highlight (from compiler srcMap)
  stacks: Record<string, string[]>;   // stackName -> cardIds, bottom->top
  hand: string | null;                // cardId or null
  facings: Record<string, Facing>;    // cardId -> facing at this step
  condition?: { text: string; result: boolean };  // for if/while steps
  error?: { code: number; name: string; message: string };
}

interface Trace {
  stackOrder: string[];               // declared stack names, for layout
  cards: Record<string, Card>;        // catalog
  steps: Step[];
  halted: 'ok' | 'error' | 'maxsteps';
}
```

Key design choices:
- **Full state per step** (programs are tiny, so no need for diffs). The
  renderer just draws `steps[current]`.
- **Step guard**: VM caps at e.g. 10k steps -> `halted: 'maxsteps'`. This turns
  an infinite loop (e.g. the old `MENOR O IGUAL` sort bug) into a friendly
  "possible infinite loop" banner instead of a hang.
- **Source map**: the emitter records `processOps[i].line` so the player can
  highlight the executing line. Worth adding to the Python emitter too.

## C. TS engine port (`web/src/engine/`)
- `lexer.ts`, `parser.ts`, `emitter.ts`, `vm.ts` — direct ports of `retruco/`.
- Errors become typed throwables, not `sys.exit`: `CompileError { line,
  message }` (surfaced in the editor) and runtime errors recorded into
  `Step.error` using the existing codes 1-5.
- `runToTrace(source): Trace` is the one public entry the UI calls.
- Card IDs assigned during stack-load (`<value><palo>` is already unique — the
  compiler's `check_repeated_cards` guarantees it).

## D. Frontend (`web/`)
- **Vite + React + TS**.
- **Editor**: CodeMirror 6 with a lightweight TIMBA mode (keyword highlighting
  from the token list; full grammar mode is a later nicety). Run button + error
  gutter.
- **Board**: a column per stack (`stackOrder`) + a "MANO" zone. Each card is a
  `<motion.div layoutId={card.id}>`.
- **Controls**: step-back, step-forward, play/pause, reset, a scrubbable
  timeline over `steps`, and a speed selector.
- **State**: a small store (Zustand or `useReducer`) holding `{trace, current,
  playing, speed}`.

## E. Animation strategy
Framer Motion's `layoutId` does the heavy lifting: when `current` changes, a
card whose position differs between steps **auto-animates** from old slot to new
slot — "fly from stack to hand" needs no manual coordinates. Layered on top:
- **Flip** (`INVIERTA`): animate `rotateY` when `facings[id]` changes; show a
  card-back for `down`.
- **Highlight**: pulse the source line + the card(s) that moved this step.
- **Errors**: red flash on the offending stack/hand + a message banner.
- Stepping backward is just decrementing `current` — animations run in reverse.

## F. Repo structure & tooling
Monorepo-lite; Python package untouched.

```
retruco/            # existing Python package (reference engine)
web/                # Vite app
  src/engine/       # TS port + vitest tests
  src/ui/           # editor, board, controls
  src/engine/__fixtures__/   # canonical traces exported from Python
package.json, vite.config.ts, ...
```

## G. Correctness: Python stays the source of truth
To stop the two engines from drifting:
1. Add a Python `export_trace(source) -> dict` emitting the **same** Trace JSON.
2. A script dumps traces for every `examples/*.timba` + the unit-test programs
   into `web/src/engine/__fixtures__/`.
3. **vitest** runs the TS engine on those same programs and asserts identical
   traces.
4. CI gains a `web` job: `npm ci && npm run build && npm test`. Divergence fails
   the build.

## H. Deployment
A `pages.yml` workflow builds `web/` and publishes to **GitHub Pages** on push
to `main`. Static, free. The playground URL goes in the README.

## I. Milestones (build order)
1. **Engine port + cross-check** — TS lexer/parser/emitter/vm, vitest against
   Python-exported fixtures. (De-risks everything; no UI yet.)
2. **Static board renderer** — render a single `Step` (stacks + hand), no
   animation.
3. **Player** — step/play/back/scrub wired to `trace.steps`; Framer `layoutId`.
4. **Editor + run** — CodeMirror, compile errors, line highlight, step-guard
   banner.
5. **Polish hooks** (post-MVP): flip animations, examples dropdown, shareable
   `?prog=` permalinks, speed control.
6. **Deploy** — Pages workflow + README link.

## J. Deferred decisions
- Full CodeMirror grammar/autocomplete vs simple keyword highlighting.
- Permalink encoding (URL param vs gist).
- Mobile/touch layout for the board.
- Whether to keep `gui_retruco.py` (Tkinter GUI) or retire it for the web
  playground.
