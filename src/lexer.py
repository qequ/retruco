from enum import Enum
from os import sys


class Lexer:
    def __init__(self, input):
        # Source code to lex as a string. Append a newline to simplify lexing/parsing the last token/statement.
        self.source = input + '\n'
        self.cur_char = ''   # Current character in the string.
        self.cur_pos = -1    # Current position in the string.
        self.next_char()

    # Process the next character.
    def next_char(self):
        self.cur_pos += 1
        if self.cur_pos >= len(self.source):
            self.cur_char = '\0'  # EOF
        else:
            self.cur_char = self.source[self.cur_pos]

    # Return the lookahead character.
    def peek(self):
        if self.cur_pos + 1 >= len(self.source):
            return '\0'
        return self.source[self.cur_pos+1]

    # Invalid token found, print error message and exit.
    def abort(self, message):
        sys.exit("Lexing error. " + message)

    # Skip whitespace except newlines, which we will use to indicate the end of a statement.
    def skipWhitespace(self):
        while self.cur_char == ' ' or self.cur_char == '\t' or self.cur_char == '\r':
            self.next_char()

    # Skip comments in the code.
    def skipComment(self):
        if self.cur_char == '#':
            while self.cur_char != '\n':
                self.next_char()

    # Return the next token.
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None

        # Check the first character of this token to see if we can decide what it is.
        # If it is a multiple character operator (e.g., !=), number, identifier, or keyword then we will process the rest.

        if self.cur_char == "-":
            token = Token(self.cur_char, TokenType.DASH)
        
        elif self.cur_char == ",":
            token = Token(self.cur_char, TokenType.COMMA)
        
        elif self.cur_char == ";":
            token = Token(self.cur_char, TokenType.SEMICOLON)

        elif self.cur_char.isdigit():
            # Leading character is a digit, so this must be a number.
            # Get all consecutive digits and decimal if there is one.
            startPos = self.cur_pos
            while self.peek().isdigit():
                self.next_char()


            # Get the substring.
            tokText = self.source[startPos: self.cur_pos + 1]
            token = Token(tokText, TokenType.NUMBER)
        elif self.cur_char.isalpha():
            # Leading character is a letter, so this must be an identifier or a keyword.
            # Get all consecutive alpha numeric characters.
            startPos = self.cur_pos
            while self.peek().isalnum():
                self.next_char()

            # Check if the token is in the list of keywords.
            # Get the substring.
            tokText = self.source[startPos: self.cur_pos + 1]
            keyword = Token.checkIfKeyword(tokText)
            if keyword == None:  # Identifier
                token = Token(tokText, TokenType.IDENT)
            else:   # Keyword
                token = Token(tokText, keyword)
        elif self.cur_char == '\n':
            token = Token(self.cur_char, TokenType.NEWLINE)
        elif self.cur_char == '\0':
            token = Token('', TokenType.EOF)
        else:
            # Unknown token!
            self.abort("Unknown token: " + self.cur_char)

        self.next_char()
        return token


# Token contains the original text and the type of token.
class Token:
    def __init__(self, tokenText, tokenKind):
        # The token's actual text. Used for identifiers, strings, and numbers.
        self.text = tokenText
        # The TokenType that this token is classified as.
        self.kind = tokenKind

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # Relies on all keyword enum values being 1XX.
            if kind.name == tokenText and kind.value >= 2:
                return kind
        return None


class TokenType(Enum):
    SEMICOLON = -5
    COMMA = -4
    DASH = -3
    EOF = -2
    NEWLINE = -1  # SEPARATOR OF INSTRUCTIONS
    NUMBER = 0
    IDENT = 1  # IDENTIFIER OF STACKS

    # KEYWORDS
    ABAJO = 2
    BASTOS = 3
    BOCA = 4
    CARTA = 5
    CARTAS = 6
    CON = 7
    COPAS = 8
    DE = 9
    DEL = 10
    DEFINICION = 11
    DEPOSITE = 12
    DEPOSITELA = 13
    DISTINTO = 14
    EJECUTE = 15
    EN = 16
    ES = 17
    ESPADAS = 18
    ESTA = 19
    IGUAL = 20
    INVIERTA = 21
    INVIERTALA = 22
    LA = 23
    LAS = 24
    MAS = 25
    MAYOR = 26
    VACIA = 27
    MENOR = 28
    MIENTRAS = 29
    NADA = 30
    NO = 31
    O = 32
    OROS = 33
    PILA = 34
    PROGRAMA = 35
    QUE = 36
    REPITA = 37
    SI = 38
    SIGUIENTES = 39
    SINO = 40
    TOME = 41
    TOPE = 42
    UCP = 43
    UNA = 44
    VALOR = 45
    Y = 46
    TIENE = 47
    ARRIBA = 48
