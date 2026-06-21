import { useMemo, useState } from "react";
import "./App.css";
import { runToTrace } from "./engine/trace";
import { EXAMPLES } from "./examples";
import { Board } from "./ui/Board";
import { movedCardIds } from "./ui/diff";

function App() {
  const [exampleName, setExampleName] = useState(EXAMPLES[0].name);
  const [current, setCurrent] = useState(0);

  const example = EXAMPLES.find((e) => e.name === exampleName) ?? EXAMPLES[0];
  const trace = useMemo(() => runToTrace(example.source), [example.source]);

  const lastIndex = trace.steps.length - 1;
  const idx = Math.min(current, lastIndex);
  const step = trace.steps[idx];
  const prevStep = idx > 0 ? trace.steps[idx - 1] : null;
  const moved = useMemo(() => movedCardIds(prevStep, step), [prevStep, step]);

  function selectExample(name: string) {
    setExampleName(name);
    setCurrent(0);
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Retruco Playground</h1>
        <select value={exampleName} onChange={(e) => selectExample(e.target.value)}>
          {EXAMPLES.map((e) => (
            <option key={e.name} value={e.name}>
              {e.label}
            </option>
          ))}
        </select>
      </header>

      <Board stackOrder={trace.stackOrder} step={step} activeIds={moved} />

      <div className="controls">
        <button onClick={() => setCurrent(0)} disabled={idx === 0} title="Inicio">
          ⏮
        </button>
        <button
          onClick={() => setCurrent((i) => Math.max(0, i - 1))}
          disabled={idx === 0}
          title="Anterior"
        >
          ◀
        </button>
        <input
          type="range"
          min={0}
          max={lastIndex}
          value={idx}
          onChange={(e) => setCurrent(Number(e.target.value))}
        />
        <button
          onClick={() => setCurrent((i) => Math.min(lastIndex, i + 1))}
          disabled={idx === lastIndex}
          title="Siguiente"
        >
          ▶
        </button>
        <span className="step-readout">
          paso {idx} / {lastIndex}
        </span>
      </div>

      <div className="status">
        <span>
          opcode: <code>{step.opcode ?? "(inicio)"}</code>
        </span>
        {idx === lastIndex && (
          <span className={`halt halt-${trace.halted}`}>
            {trace.halted === "ok" && "✓ terminó correctamente"}
            {trace.halted === "error" && `✗ error ${trace.error?.code}: ${trace.error?.name}`}
            {trace.halted === "maxsteps" && "⏱ posible bucle infinito (límite de pasos)"}
          </span>
        )}
      </div>

      <footer className="credits">
        Cartas:{" "}
        <a
          href="https://commons.wikimedia.org/wiki/File:Baraja_espa%C3%B1ola_completa.png"
          target="_blank"
          rel="noreferrer"
        >
          Baraja Española
        </a>{" "}
        por Basquetteur (Wikimedia Commons),{" "}
        <a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank" rel="noreferrer">
          CC BY-SA 3.0
        </a>
        .
      </footer>
    </div>
  );
}

export default App;
