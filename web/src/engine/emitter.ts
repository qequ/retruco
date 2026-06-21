export class Emitter {
  opcodeStr = "";
  stacksInstructions: string[] = [];
  processInstructions: string[] = [];

  appendOpcode(s: string): void {
    this.opcodeStr += s;
  }

  resetOpcodeStr(): void {
    this.opcodeStr = "";
  }

  emitStackInst(): void {
    this.stacksInstructions.push(this.opcodeStr);
  }

  emitProcessInst(): void {
    this.processInstructions.push(this.opcodeStr);
  }

  checkRepeatedCards(): boolean {
    const filtered = this.stacksInstructions.filter((s) => s.length > 1);
    const cards = filtered.map((s) => s.slice(1, -1));
    return new Set(cards).size !== cards.length;
  }
}
