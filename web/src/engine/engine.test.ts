import { describe, expect, it } from "vitest";
import { runToTrace } from "./trace";
import type { Trace } from "./types";

// Load every fixture exported by the Python reference engine
// (tools/export_traces.py). Each fixture embeds the source program plus the
// canonical trace, so the TS engine must reproduce it byte-for-byte.
type Fixture = Trace & { source: string };
const fixtures = import.meta.glob<Fixture>("./__fixtures__/*.json", {
  eager: true,
  import: "default",
});

const cases = Object.entries(fixtures).map(([path, fixture]) => {
  const name = path.split("/").pop()!.replace(/\.json$/, "");
  return { name, fixture };
});

describe("TS engine matches Python reference traces", () => {
  it("loaded fixtures", () => {
    expect(cases.length).toBeGreaterThan(0);
  });

  for (const { name, fixture } of cases) {
    it(`reproduces trace for ${name}`, () => {
      const { source, ...expected } = fixture;
      const actual = runToTrace(source);
      expect(actual).toEqual(expected);
    });
  }
});
