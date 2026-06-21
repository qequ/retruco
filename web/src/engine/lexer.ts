export enum TokenType {
  SEMICOLON = -5,
  COMMA = -4,
  DASH = -3,
  EOF = -2,
  NEWLINE = -1, // SEPARATOR OF INSTRUCTIONS
  NUMBER = 0,
  IDENT = 1, // IDENTIFIER OF STACKS

  // KEYWORDS (value >= 2)
  ABAJO = 2,
  BASTOS = 3,
  BOCA = 4,
  CARTA = 5,
  CARTAS = 6,
  CON = 7,
  COPAS = 8,
  DE = 9,
  DEL = 10,
  DEFINICION = 11,
  DEPOSITE = 12,
  DEPOSITELA = 13,
  DISTINTO = 14,
  EJECUTE = 15,
  EN = 16,
  ES = 17,
  ESPADAS = 18,
  ESTA = 19,
  IGUAL = 20,
  INVIERTA = 21,
  INVIERTALA = 22,
  LA = 23,
  LAS = 24,
  MAS = 25,
  MAYOR = 26,
  VACIA = 27,
  MENOR = 28,
  MIENTRAS = 29,
  NADA = 30,
  NO = 31,
  O = 32,
  OROS = 33,
  PILA = 34,
  PROGRAMA = 35,
  QUE = 36,
  REPITA = 37,
  SI = 38,
  SIGUIENTES = 39,
  SINO = 40,
  TOME = 41,
  TOPE = 42,
  UCP = 43,
  UNA = 44,
  VALOR = 45,
  Y = 46,
  TIENE = 47,
  ARRIBA = 48,
  PALO = 49,
  A = 50,
}

// Names of all keyword tokens (value >= 2), used for keyword lookup and the
// parser's reserved-word check.
export const KEYWORD_NAMES: ReadonlySet<string> = new Set(
  Object.keys(TokenType).filter(
    (k) => Number.isNaN(Number(k)) && (TokenType[k as keyof typeof TokenType] as number) >= 2,
  ),
);

const KEYWORDS: Record<string, TokenType> = {};
for (const name of KEYWORD_NAMES) {
  KEYWORDS[name] = TokenType[name as keyof typeof TokenType] as unknown as TokenType;
}

export class LexError extends Error {}

export class Token {
  text: string;
  kind: TokenType;

  constructor(text: string, kind: TokenType) {
    this.text = text;
    this.kind = kind;
  }

  static checkIfKeyword(text: string): TokenType | null {
    return text in KEYWORDS ? KEYWORDS[text] : null;
  }
}

const EOF = "\0";

function isDigit(c: string): boolean {
  return c >= "0" && c <= "9";
}

function isAlpha(c: string): boolean {
  return /[A-Za-z]/.test(c);
}

function isAlnum(c: string): boolean {
  return /[A-Za-z0-9]/.test(c);
}

export class Lexer {
  private source: string;
  private curChar = "";
  private curPos = -1;

  constructor(input: string) {
    // Append a newline to simplify lexing the final token/statement.
    this.source = input + "\n";
    this.nextChar();
  }

  private nextChar(): void {
    this.curPos += 1;
    this.curChar = this.curPos >= this.source.length ? EOF : this.source[this.curPos];
  }

  private peek(): string {
    if (this.curPos + 1 >= this.source.length) return EOF;
    return this.source[this.curPos + 1];
  }

  private abort(message: string): never {
    throw new LexError("Lexing error. " + message);
  }

  private skipWhitespace(): void {
    while (this.curChar === " " || this.curChar === "\t" || this.curChar === "\r") {
      this.nextChar();
    }
  }

  private skipComment(): void {
    if (this.curChar === "#") {
      // Cast avoids TS pinning the literal type from the `=== "#"` narrowing
      // above; nextChar() mutates curChar but TS can't see that.
      while ((this.curChar as string) !== "\n") this.nextChar();
    }
  }

  getToken(): Token {
    this.skipWhitespace();
    this.skipComment();
    let token: Token;

    if (this.curChar === "-") {
      token = new Token(this.curChar, TokenType.DASH);
    } else if (this.curChar === ",") {
      token = new Token(this.curChar, TokenType.COMMA);
    } else if (this.curChar === ";") {
      token = new Token(this.curChar, TokenType.SEMICOLON);
    } else if (isDigit(this.curChar)) {
      const startPos = this.curPos;
      while (isDigit(this.peek())) this.nextChar();
      const text = this.source.slice(startPos, this.curPos + 1);
      token = new Token(text, TokenType.NUMBER);
    } else if (isAlpha(this.curChar)) {
      const startPos = this.curPos;
      while (isAlnum(this.peek())) this.nextChar();
      const text = this.source.slice(startPos, this.curPos + 1);
      const keyword = Token.checkIfKeyword(text);
      token = keyword === null ? new Token(text, TokenType.IDENT) : new Token(text, keyword);
    } else if (this.curChar === "\n") {
      token = new Token(this.curChar, TokenType.NEWLINE);
    } else if (this.curChar === EOF) {
      token = new Token("", TokenType.EOF);
    } else {
      this.abort("Unknown token: " + this.curChar);
    }

    this.nextChar();
    return token;
  }
}
