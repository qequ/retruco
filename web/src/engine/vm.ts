import { Card, Position } from "./cards";

function compare(a: number, op: string, b: number): boolean {
  switch (op) {
    case "=":
    case "==":
      return a === b;
    case "!=":
      return a !== b;
    case "<":
      return a < b;
    case ">":
      return a > b;
    case "<=":
      return a <= b;
    case ">=":
      return a >= b;
    default:
      return false;
  }
}

function isNumeric(s: string): boolean {
  return s.length > 0 && /^[0-9]+$/.test(s);
}

/**
 * Error codes (mirrors the Python VM):
 *   0 OK, 1 FULL_HAND, 2 EMPTY_STACK, 3 EMPTY_HAND,
 *   4 LOGIC_CONDITION, 5 FACE_DOWN_CARD_LOGIC.
 */
export class VirtualMachine {
  opcodes: string[];
  stacksOpcodes: string[];
  pc = 0;
  private whilestack: number[] = [];
  private endwhilestack: number[] = [];
  private ifflags: boolean[] = [];
  private elsestack: number[] = [];
  private endifstack: number[] = [];
  stacks: Card[][] = [];
  hand: Card | null = null;
  errorCode = 0;
  lastOpcodeAddress = 0;

  constructor(opcodes: string[], stacksOpcodes: string[]) {
    this.opcodes = opcodes;
    this.stacksOpcodes = stacksOpcodes;
  }

  private top(stack: Card[]): Card {
    return stack[stack.length - 1];
  }

  decodeLogicalCondition(cond: string): boolean {
    if (cond[0] === "P") {
      const idx = parseInt(cond.slice(1, -1), 10);
      let res = this.stacks[idx].length === 0;
      if (cond[cond.length - 1] === "N") res = !res;
      return res;
    } else if (cond[0] === "C") {
      if (this.hand === null) {
        this.errorCode = 3;
        return false;
      }

      const changing = cond.slice(2);
      const c0 = changing[0];
      let res: boolean;

      if (c0 === "F") {
        res = this.hand.position === Position.FACE_DOWN;
      } else if (["E", "B", "C", "O"].includes(c0)) {
        res = this.hand.type === c0;
      } else if (c0 === "P") {
        const stackNum = parseInt(changing.slice(1), 10);
        if (this.stacks[stackNum].length === 0) {
          this.errorCode = 2;
          return false;
        }
        if (this.top(this.stacks[stackNum]).position === Position.FACE_DOWN) {
          this.errorCode = 5;
          return false;
        }
        res = this.hand.type === this.top(this.stacks[stackNum]).type;
      } else if (["!", "=", "<", ">"].includes(c0)) {
        let op: string;
        let offset: number;
        if (changing[1] === "=") {
          op = changing.slice(0, 2);
          offset = 2;
        } else {
          op = changing[0];
          offset = 1;
        }
        const operand = changing.slice(offset);
        if (operand[0] === "P") {
          const stackNum = parseInt(changing.slice(offset + 1), 10);
          if (this.stacks[stackNum].length === 0) {
            this.errorCode = 2;
            return false;
          }
          if (this.top(this.stacks[stackNum]).position === Position.FACE_DOWN) {
            this.errorCode = 5;
            return false;
          }
          res = compare(this.hand.value, op, this.top(this.stacks[stackNum]).value);
        } else if (isNumeric(operand)) {
          res = compare(this.hand.value, op, parseInt(operand, 10));
        } else {
          this.errorCode = 4;
          return false;
        }
      } else {
        this.errorCode = 4;
        return false;
      }

      if (cond[1] === "N") res = !res;

      if (this.hand.position === Position.FACE_DOWN && c0 !== "F") {
        this.errorCode = 5;
        return false;
      }
      return res;
    } else {
      this.errorCode = 4;
      return false;
    }
  }

  eval_condition(cond: string): boolean {
    // & (and) has less precedence than | (or). Evaluate every proposition first
    // (side effects on errorCode), then combine.
    const logic = cond
      .split("|")
      .map((orPart) => orPart.split("&").map((x) => this.decodeLogicalCondition(x)));
    return logic.some((conj) => conj.every((b) => b));
  }

  private whileDecode(): void {
    if (this.whilestack.length === 0 || this.whilestack[this.whilestack.length - 1] !== this.pc) {
      let nestedLevel = 1;
      let address = this.pc;
      while (nestedLevel !== 0) {
        address += 1;
        if (this.opcodes[address][0] === "7") {
          nestedLevel += 1;
        } else if (this.opcodes[address][0] === "8") {
          if (nestedLevel === 1) this.endwhilestack.push(address);
          nestedLevel -= 1;
        }
      }
      this.whilestack.push(this.pc);
    }

    const evalBool = this.eval_condition(this.opcodes[this.pc].slice(1));
    if (this.errorCode !== 0) return;

    if (evalBool) {
      this.pc += 1;
    } else {
      this.pc = (this.endwhilestack.pop() as number) + 1;
      this.whilestack.pop();
    }
  }

  private endwhileDecode(): void {
    this.pc = this.whilestack[this.whilestack.length - 1];
  }

  private ifDecode(): void {
    let nestedLevel = 1;
    let address = this.pc;
    while (nestedLevel !== 0) {
      address += 1;
      if (this.opcodes[address][0] === "3") {
        nestedLevel += 1;
      } else if (this.opcodes[address][0] === "4" && nestedLevel === 1) {
        this.elsestack.push(address);
      } else if (this.opcodes[address][0] === "5") {
        if (nestedLevel === 1) this.endifstack.push(address);
        nestedLevel -= 1;
      }
    }

    const evalBool = this.eval_condition(this.opcodes[this.pc].slice(1));
    if (evalBool) {
      this.pc += 1;
      this.ifflags.push(true);
    } else {
      this.pc = this.elsestack[this.elsestack.length - 1];
      this.ifflags.push(false);
    }
  }

  private elseDecode(): void {
    if (this.ifflags[this.ifflags.length - 1]) {
      this.pc = this.endifstack[this.endifstack.length - 1];
    } else {
      this.pc += 1;
    }
  }

  private endifDecode(): void {
    this.ifflags.pop();
    this.elsestack.pop();
    this.pc += 1;
  }

  loadStacks(): void {
    for (const ins of this.stacksOpcodes) {
      if (isNumeric(ins)) {
        this.stacks.splice(parseInt(ins, 10), 0, []);
      } else {
        let paloIndex = 0;
        for (let i = 0; i < ins.length; i++) {
          if (["O", "E", "C", "B"].includes(ins[i])) {
            paloIndex = i;
            break;
          }
        }
        const sp = parseInt(ins.slice(0, paloIndex), 10);
        const v = parseInt(ins.slice(paloIndex + 1, -1), 10);
        const p = ins[paloIndex];
        const pos = ins[ins.length - 1] === "D" ? Position.FACE_DOWN : Position.FACE_UP;
        if (this.stacks[sp] === undefined) {
          this.stacks.splice(sp, 0, []);
        }
        this.stacks[sp].push(new Card(v, p, pos));
      }
    }
  }

  private takeCard(): void {
    const opcode = this.opcodes[this.pc];
    if (this.hand !== null) {
      this.errorCode = 1;
      return;
    }
    if (this.stacks[parseInt(opcode.slice(1), 10)].length === 0) {
      this.errorCode = 2;
      return;
    }
    this.hand = this.stacks[parseInt(opcode[1], 10)].pop() as Card;
  }

  private depositHandCard(): void {
    const opcode = this.opcodes[this.pc];
    if (this.hand === null) {
      this.errorCode = 3;
      return;
    }
    this.stacks[parseInt(opcode.slice(1), 10)].push(this.hand);
    this.hand = null;
  }

  private invertHandCard(): void {
    if (this.hand === null) {
      this.errorCode = 3;
      return;
    }
    this.hand.swapPosition();
  }

  executeInstruction(): void {
    const instType = this.opcodes[this.pc][0];
    this.lastOpcodeAddress = this.pc;
    if (instType === "0") {
      this.takeCard();
      this.pc += 1;
    } else if (instType === "1") {
      this.depositHandCard();
      this.pc += 1;
    } else if (instType === "2") {
      this.invertHandCard();
      this.pc += 1;
    } else if (instType === "3") {
      this.ifDecode();
    } else if (instType === "4") {
      this.elseDecode();
    } else if (instType === "5") {
      this.endifDecode();
    } else if (instType === "7") {
      this.whileDecode();
    } else if (instType === "8") {
      this.endwhileDecode();
    }
  }
}
