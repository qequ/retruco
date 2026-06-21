import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { runToTrace } from "../engine/trace";
import { EXAMPLES } from "../examples";
import { Board } from "./Board";

describe("Board renders a trace step", () => {
  const ex = EXAMPLES.find((e) => e.name === "split_by_palo")!;
  const trace = runToTrace(ex.source);

  it("renders stacks, hand zone and cards without crashing", () => {
    const last = trace.steps[trace.steps.length - 1];
    const html = renderToStaticMarkup(<Board stackOrder={trace.stackOrder} step={last} />);
    expect(html).toContain("MAZO");
    expect(html).toContain("MONEDAS");
    expect(html).toContain("RESTO");
    expect(html).toContain("MANO");
    // Final state sorts the two oros (1 and 3) into MONEDAS.
    expect(html).toContain("de Oro");
  });

  it("shows the empty-slot placeholder when a stack is empty", () => {
    const first = trace.steps[0];
    const html = renderToStaticMarkup(<Board stackOrder={trace.stackOrder} step={first} />);
    expect(html).toContain("vacía");
  });
});
