import type { Emitter } from "./emitter";
import { KEYWORD_NAMES, Lexer, Token, TokenType } from "./lexer";

export class CompileError extends Error {
  line: number;
  constructor(message: string, line: number) {
    super(`${message} - Linea ${line}`);
    this.line = line;
  }
}

export class Parser {
  private lexer: Lexer;
  private emitter: Emitter;
  namesDeclared: string[] = [];
  private curToken!: Token;
  private peekToken!: Token;
  private codeLine = 1;

  constructor(lexer: Lexer, emitter: Emitter) {
    this.lexer = lexer;
    this.emitter = emitter;
    this.nextToken();
    this.nextToken();
  }

  private checkToken(kind: TokenType): boolean {
    return kind === this.curToken.kind;
  }

  private checkTokenList(kinds: TokenType[]): boolean {
    return kinds.some((k) => k === this.curToken.kind);
  }

  private checkPeek(kind: TokenType): boolean {
    return kind === this.peekToken.kind;
  }

  private match(kind: TokenType): void {
    if (!this.checkToken(kind)) {
      this.abort(`Se esperaba ${TokenType[kind]}, se encuentra ${TokenType[this.curToken.kind]}`);
    }
    this.nextToken();
  }

  private matchPhrase(kinds: TokenType[]): void {
    for (const k of kinds) this.match(k);
  }

  private nextToken(): void {
    this.curToken = this.peekToken;
    this.peekToken = this.lexer.getToken();
  }

  private abort(message: string): never {
    throw new CompileError("Error. " + message, this.codeLine);
  }

  private skipWhitespaceTokens(): void {
    while (this.checkToken(TokenType.NEWLINE)) {
      this.nextToken();
      this.codeLine += 1;
    }
  }

  // programa ::= <declaraciones> ; nl* <proceso>
  program(): void {
    this.skipWhitespaceTokens();
    this.declarations();
    this.match(TokenType.SEMICOLON);
    this.skipWhitespaceTokens();
    this.process();
  }

  private declarations(): void {
    this.skipWhitespaceTokens();
    this.matchPhrase([
      TokenType.UCP,
      TokenType.EJECUTE,
      TokenType.CON,
      TokenType.LAS,
      TokenType.SIGUIENTES,
      TokenType.CARTAS,
      TokenType.NEWLINE,
    ]);
    this.codeLine += 1;
    while (!this.checkToken(TokenType.SEMICOLON)) {
      this.stacksList();
    }
  }

  private stacksList(): void {
    this.stackDescription();
    while (this.checkToken(TokenType.COMMA)) {
      this.nextToken();
      this.skipWhitespaceTokens();
      this.stackDescription();
    }
  }

  private stackDescription(): void {
    this.stack();
    this.name();
    this.content();
  }

  private stack(): void {
    if (this.checkToken(TokenType.LA)) {
      this.matchPhrase([TokenType.LA, TokenType.PILA]);
    } else if (this.checkToken(TokenType.PILA)) {
      this.nextToken();
    } else {
      this.abort(`Se esperaba LA PILA O PILA, en cambio se encuentra ${this.curToken.text}`);
    }
  }

  private name(calledByProcess = false): void {
    if (this.checkToken(TokenType.IDENT)) {
      if (calledByProcess) {
        if (this.namesDeclared.includes(this.curToken.text)) {
          this.emitter.appendOpcode(String(this.namesDeclared.indexOf(this.curToken.text)));
          this.nextToken();
        } else {
          this.abort(`Nombre de Pila ${this.curToken.text} no declarado`);
        }
      } else {
        if (this.namesDeclared.includes(this.curToken.text)) {
          this.abort(`Nombre de Pila ${this.curToken.text} ya declarado anteriormente`);
        } else if (this.curToken.text.length === 0 || isDigit(this.curToken.text[0])) {
          this.abort(
            `Nombre de Pila ${this.curToken.text} Incorrecto - no puede comenzar con numero`,
          );
        }
        if (KEYWORD_NAMES.has(this.curToken.text)) {
          this.abort(`Nombre de Pila ${this.curToken.text} Incorrecto - palabra reservada`);
        }
        this.namesDeclared.push(this.curToken.text);
        this.nextToken();
      }
    } else {
      this.abort(`Esperado Nombre de Pila, en cambio se encuentra ${this.curToken.text}`);
    }
  }

  private content(): void {
    if (this.checkToken(TokenType.NO)) {
      this.matchPhrase([TokenType.NO, TokenType.TIENE, TokenType.CARTAS]);
      this.emitter.appendOpcode(String(this.namesDeclared.length - 1));
      this.emitter.emitStackInst();
      this.emitter.resetOpcodeStr();
    } else if (this.checkToken(TokenType.TIENE)) {
      this.nextToken();
      this.cardsList();
    } else {
      this.abort(`Se esperaba NO o TIENE pero se encuentra ${this.curToken.text}`);
    }
  }

  private cardsList(): void {
    this.cardDescription();
    while (this.checkToken(TokenType.DASH)) {
      this.nextToken();
      this.skipWhitespaceTokens();
      this.cardDescription();
    }
  }

  private cardDescription(): void {
    this.emitter.appendOpcode(String(this.namesDeclared.length - 1));
    this.number();
    this.match(TokenType.DE);
    this.palos();
    this.position();
  }

  private number(): void {
    if (this.checkToken(TokenType.NUMBER)) {
      const validNums = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12];
      if (!validNums.includes(parseInt(this.curToken.text, 10))) {
        this.abort("Tiene que ser un numero entre 1 y 7 o 10 y 12");
      }
      this.emitter.appendOpcode(this.curToken.text);
      this.nextToken();
    } else {
      this.abort(`Se esperaba un numero, en cambio hay ${this.curToken.text}`);
    }
  }

  private palos(usedForProcess = false): void {
    if (
      this.checkToken(TokenType.OROS) ||
      this.checkToken(TokenType.BASTOS) ||
      this.checkToken(TokenType.ESPADAS) ||
      this.checkToken(TokenType.COPAS)
    ) {
      if (usedForProcess) {
        this.emitter.appendOpcode(this.curToken.text[0]);
      } else {
        const s = this.emitter.opcodeStr;
        let num: string;
        if (s.length === 3) {
          num = s[s.length - 2] + s[s.length - 1];
        } else {
          num = s[s.length - 1];
        }
        this.emitter.opcodeStr = s[0];
        this.emitter.appendOpcode(this.curToken.text[0]);
        this.emitter.appendOpcode(num);
      }
      this.nextToken();
    } else {
      this.abort(`Se esperaba un palo de carta, en cambio se tiene ${this.curToken.text}`);
    }
  }

  private position(): void {
    this.match(TokenType.BOCA);
    if (this.checkToken(TokenType.ARRIBA)) {
      this.emitter.appendOpcode("U");
      this.nextToken();
    } else if (this.checkToken(TokenType.ABAJO)) {
      this.emitter.appendOpcode("D");
      this.nextToken();
    } else {
      this.abort(`Se esperaba ARRIBA o ABAJO, en cambio se tiene ${this.curToken.text}`);
    }
    this.emitter.emitStackInst();
    this.emitter.resetOpcodeStr();
  }

  private process(): void {
    this.matchPhrase([
      TokenType.DEFINICION,
      TokenType.DE,
      TokenType.PROGRAMA,
      TokenType.NEWLINE,
    ]);
    this.codeLine += 1;
    this.statements(TokenType.EOF);
  }

  private statements(delimiter: TokenType): void {
    const delims = [TokenType.EOF, delimiter];
    while (!this.checkTokenList(delims)) {
      this.statement();
    }
  }

  private statement(): void {
    this.emitter.resetOpcodeStr();
    if (this.checkToken(TokenType.TOME)) {
      this.take();
    } else if (this.checkToken(TokenType.DEPOSITE) || this.checkToken(TokenType.DEPOSITELA)) {
      this.deposit();
    } else if (this.checkToken(TokenType.INVIERTA) || this.checkToken(TokenType.INVIERTALA)) {
      this.invert();
    } else if (this.checkToken(TokenType.SI)) {
      this.selection();
    } else if (this.checkToken(TokenType.MIENTRAS)) {
      this.iteration();
    } else {
      this.abort(
        `Se esperaba una operacion: TOME, DEPOSITE, INVIERTA, SI, MIENTRAS. En cambio, se encuentra: ${TokenType[this.curToken.kind]}`,
      );
    }
    this.nl();
    this.emitter.emitProcessInst();
  }

  private iteration(): void {
    this.match(TokenType.MIENTRAS);
    this.emitter.appendOpcode("7");
    this.condition();
    this.emitter.emitProcessInst();
    this.nl();
    this.statements(TokenType.REPITA);
    this.match(TokenType.REPITA);
    this.emitter.resetOpcodeStr();
    this.emitter.appendOpcode("8");
  }

  private take(): void {
    this.match(TokenType.TOME);
    if (this.checkToken(TokenType.UNA)) {
      this.nextToken();
      if (this.checkToken(TokenType.CARTA)) {
        this.nextToken();
      }
    }
    this.match(TokenType.DE);
    this.stack();
    this.emitter.appendOpcode("0");
    this.name(true);
  }

  private deposit(): void {
    if (this.checkToken(TokenType.DEPOSITE)) {
      this.matchPhrase([TokenType.DEPOSITE, TokenType.LA, TokenType.CARTA]);
    } else {
      this.match(TokenType.DEPOSITELA);
    }
    this.match(TokenType.EN);
    this.emitter.appendOpcode("1");
    this.stack();
    this.name(true);
  }

  private invert(): void {
    if (this.checkToken(TokenType.INVIERTA)) {
      this.matchPhrase([TokenType.INVIERTA, TokenType.LA, TokenType.CARTA]);
    } else {
      this.match(TokenType.INVIERTALA);
    }
    this.emitter.appendOpcode("2");
  }

  private selection(): void {
    this.match(TokenType.SI);
    this.emitter.appendOpcode("3");
    this.condition();
    this.emitter.emitProcessInst();
    this.nl();
    this.statements(TokenType.SINO);
    this.match(TokenType.SINO);
    this.emitter.resetOpcodeStr();
    this.emitter.appendOpcode("4");
    this.emitter.emitProcessInst();
    this.emitter.resetOpcodeStr();
    this.nl();
    if (this.checkToken(TokenType.NADA)) {
      this.matchPhrase([TokenType.NADA, TokenType.MAS]);
    } else {
      this.statements(TokenType.NADA);
      this.matchPhrase([TokenType.NADA, TokenType.MAS]);
    }
    this.emitter.resetOpcodeStr();
    this.emitter.appendOpcode("5");
  }

  private condition(): void {
    this.simpleCondition();
    while (this.checkToken(TokenType.Y) || this.checkToken(TokenType.O)) {
      if (this.checkToken(TokenType.Y)) {
        this.emitter.appendOpcode("&");
      } else {
        this.emitter.appendOpcode("|");
      }
      this.nextToken();
      this.simpleCondition();
    }
  }

  private simpleCondition(): void {
    if (this.checkToken(TokenType.CARTA) || this.checkPeek(TokenType.CARTA)) {
      this.cardConditions();
    } else if (this.checkToken(TokenType.PILA) || this.checkPeek(TokenType.PILA)) {
      this.emptyStackCondition();
    } else {
      this.abort(
        `Se esperaba LA PILA, PILA, LA CARTA, CARTA. En cambio, se encuentra ${this.curToken.text}`,
      );
    }
  }

  private emptyStackCondition(): void {
    this.stack();
    this.emitter.appendOpcode("P");
    this.name(true);
    if (this.checkToken(TokenType.NO)) {
      this.matchPhrase([TokenType.NO, TokenType.ESTA, TokenType.VACIA]);
      this.emitter.appendOpcode("N");
    } else if (this.checkToken(TokenType.ESTA)) {
      this.matchPhrase([TokenType.ESTA, TokenType.VACIA]);
      this.emitter.appendOpcode("E");
    } else {
      this.abort(`Se esperaba NO ESTA, ESTA. En cambio, se encuentra ${this.curToken.text}`);
    }
  }

  private cardConditions(): void {
    this.card();
    this.emitter.appendOpcode("C");
    if (
      (this.checkToken(TokenType.NO) && this.checkPeek(TokenType.ESTA)) ||
      this.checkToken(TokenType.ESTA)
    ) {
      this.state();
    } else if (
      (this.checkToken(TokenType.NO) && this.checkPeek(TokenType.ES)) ||
      this.checkToken(TokenType.ES)
    ) {
      this.isIt();
      if (
        (this.checkToken(TokenType.DEL) && this.checkPeek(TokenType.PALO)) ||
        this.checkToken(TokenType.OROS) ||
        this.checkToken(TokenType.BASTOS) ||
        this.checkToken(TokenType.ESPADAS) ||
        this.checkToken(TokenType.COPAS)
      ) {
        this.ofPalos();
      } else if (this.checkToken(TokenType.DE) && this.checkPeek(TokenType.PALO)) {
        this.relationPaloStack();
      } else {
        this.value();
      }
    } else {
      this.abort("Condicion de Carta mal formada");
    }
  }

  private value(): void {
    if (this.checkToken(TokenType.DE)) {
      this.nextToken();
      if (this.checkToken(TokenType.VALOR)) {
        this.nextToken();
        this.relation();
        this.number();
      } else {
        this.rela();
        this.matchPhrase([
          TokenType.VALOR,
          TokenType.QUE,
          TokenType.TOPE,
          TokenType.DE,
          TokenType.PILA,
        ]);
        this.emitter.appendOpcode("P");
        this.name(true);
      }
    } else {
      this.relation();
      this.number();
    }
  }

  private rela(): void {
    if (this.checkToken(TokenType.IGUAL)) {
      this.emitter.appendOpcode("=");
      this.nextToken();
    } else if (this.checkToken(TokenType.DISTINTO)) {
      this.emitter.appendOpcode("!=");
      this.nextToken();
    } else if (this.checkToken(TokenType.MAYOR)) {
      if (this.checkPeek(TokenType.O)) {
        this.matchPhrase([TokenType.MAYOR, TokenType.O, TokenType.IGUAL]);
        this.emitter.appendOpcode(">=");
      } else {
        this.emitter.appendOpcode(">");
        this.nextToken();
      }
    } else if (this.checkToken(TokenType.MENOR)) {
      if (this.checkPeek(TokenType.O)) {
        this.matchPhrase([TokenType.MENOR, TokenType.O, TokenType.IGUAL]);
        this.emitter.appendOpcode("<=");
      } else {
        this.emitter.appendOpcode("<");
        this.nextToken();
      }
    } else {
      this.abort(
        `Se esperaba una relacion; IGUAL, DISTINTO, MAYOR, MENOR... En cambio, se encuentra ${this.curToken.text}`,
      );
    }
  }

  private relation(): void {
    if (this.checkToken(TokenType.IGUAL)) {
      this.matchPhrase([TokenType.IGUAL, TokenType.A]);
      this.emitter.appendOpcode("=");
    } else if (this.checkToken(TokenType.DISTINTO)) {
      this.matchPhrase([TokenType.DISTINTO, TokenType.DE]);
      this.emitter.appendOpcode("!=");
    } else if (this.checkToken(TokenType.MAYOR)) {
      if (this.checkPeek(TokenType.O)) {
        this.matchPhrase([TokenType.MAYOR, TokenType.O, TokenType.IGUAL, TokenType.A]);
        this.emitter.appendOpcode(">=");
      } else {
        this.matchPhrase([TokenType.MAYOR, TokenType.QUE]);
        this.emitter.appendOpcode(">");
      }
    } else if (this.checkToken(TokenType.MENOR)) {
      if (this.checkPeek(TokenType.O)) {
        this.matchPhrase([TokenType.MENOR, TokenType.O, TokenType.IGUAL, TokenType.A]);
        this.emitter.appendOpcode("<=");
      } else {
        this.matchPhrase([TokenType.MENOR, TokenType.QUE]);
        this.emitter.appendOpcode("<");
      }
    } else {
      this.abort(
        `Se esperaba una relacion; IGUAL, DISTINTO, MAYOR, MENOR... En cambio, se encuentra ${this.curToken.text}`,
      );
    }
  }

  private ofPalos(): void {
    if (this.checkToken(TokenType.DEL)) {
      this.matchPhrase([TokenType.DEL, TokenType.PALO]);
    }
    this.palos(true);
  }

  private state(): void {
    if (this.checkToken(TokenType.NO)) {
      this.matchPhrase([TokenType.NO, TokenType.ESTA, TokenType.BOCA, TokenType.ABAJO]);
      this.emitter.appendOpcode("N");
    } else if (this.checkToken(TokenType.ESTA)) {
      this.matchPhrase([TokenType.ESTA, TokenType.BOCA, TokenType.ABAJO]);
      this.emitter.appendOpcode("E");
    } else {
      this.abort(`Esperado NO ESTA... O ESTA... En cambio, se encuentra ${this.curToken.text}`);
    }
    this.emitter.appendOpcode("F");
  }

  private relationPaloStack(): void {
    this.matchPhrase([
      TokenType.DE,
      TokenType.PALO,
      TokenType.IGUAL,
      TokenType.QUE,
      TokenType.TOPE,
      TokenType.DE,
    ]);
    this.stack();
    this.emitter.appendOpcode("P");
    this.name(true);
  }

  private isIt(): void {
    if (this.checkToken(TokenType.ES)) {
      this.nextToken();
      this.emitter.appendOpcode("E");
    } else if (this.checkToken(TokenType.NO)) {
      this.matchPhrase([TokenType.NO, TokenType.ES]);
      this.emitter.appendOpcode("N");
    } else {
      this.abort(`Esperado ES o NO ES. En cambio, se encuentra ${this.curToken.text}`);
    }
  }

  private card(): void {
    if (this.checkToken(TokenType.LA)) {
      this.matchPhrase([TokenType.LA, TokenType.CARTA]);
    } else if (this.checkToken(TokenType.CARTA)) {
      this.nextToken();
    } else {
      this.abort(`Se esperaba LA CARTA O CARTA, en cambio se encuentra ${this.curToken.text}`);
    }
  }

  private nl(): void {
    this.match(TokenType.NEWLINE);
    this.codeLine += 1;
    this.skipWhitespaceTokens();
  }
}

function isDigit(c: string): boolean {
  return c >= "0" && c <= "9";
}
