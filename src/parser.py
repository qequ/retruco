import sys
from lexer import *


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        # names declared in declarations part of the program
        self.names_declared = []
        # names listed in process part of the program
        self.names_listed = set()

        self.cur_token = None
        self.peek_token = None
        self.next_token()
        self.next_token()

        self.code_line = 1

    def check_token(self, kind):
        """
        Return true if the current token matches to the kind given.

        """
        return kind == self.cur_token.kind

    def check_peek(self, kind):
        """
        Return true if the next token matches to the kind given.

        """
        return kind == self.peek_token.kind

    def match(self, kind):
        """
        Try to match current token. If not, error. Advances the current token.

        """
        if not self.check_token(kind):
            self.abort("Expected " + kind.name +
                       ", got " + self.cur_token.kind.name)
        self.next_token()

    def match_phrase(self, kind_list):
        """
        Match an entire phrase of tokens

        """
        for k in kind_list:
            self.match(k)

    def next_token(self):
        """
        Advances the current token.

        """
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.getToken()
        # No need to worry about passing the EOF, lexer handles that.

    def abort(self, message):
        sys.exit("Error. " + message + " - Linea {}".format(self.code_line))

    def skip_whitespace_tokens(self):
        while self.check_token(TokenType.NEWLINE):
            self.next_token()
            self.code_line += 1


    # programa ::=  <declaraciones> nl <proceso>
    def program(self):
        print("PROGRAM")

        # Since some newlines are required in our grammar, need to skip the excess.
        self.skip_whitespace_tokens()

        self.declarations()
        self.match(TokenType.SEMICOLON)
        self.process()

        for stack_names in self.names_listed:
            if not stack_names in self.names_declared:
                self.abort(
                    "Declarada una pila que no existe: {}".format(stack_names))

    # <declaraciones> := UCP EJECUTE CON LAS SIGUIENTES CARTAS nl <lista de pilas>

    def declarations(self):
        print("declaraciones")
        self.skip_whitespace_tokens()

        self.match_phrase([TokenType.UCP,
                           TokenType.EJECUTE,
                           TokenType.CON,
                           TokenType.LAS,
                           TokenType.SIGUIENTES,
                           TokenType.CARTAS,
                           TokenType.NEWLINE])

        while not self.check_token(TokenType.SEMICOLON):
            self.stacks_list()

    # <lista de pilas> := <descripcion de pila> | <descripcion de pila> , nl* <lista de pilas>
    def stacks_list(self):
        print("lista de stacks")
        self.stack_description()

        while self.check_token(TokenType.COMMA):
            self.next_token()

            # allow newlines to improve code legibility
            self.skip_whitespace_tokens()

            self.stack_description()

    # <descripcion de pila> := <pila> <nombre> <contenido>
    def stack_description(self):
        print("descripcion de stack")
        self.stack()
        self.name()
        self.content()

    # <pila> := LA PILA | PILA
    def stack(self):
        print("stack")
        if self.check_token(TokenType.LA):
            self.match_phrase([TokenType.LA, TokenType.PILA])

        elif self.check_token(TokenType.PILA):
            self.next_token()
        else:
            self.abort(
                "Se esperaba LA PILA O PILA, en cambio se encuentra {}".format(self.cur_token.text))

    # <nombre> := str alfanumérico que no comienza con número ni contiene símbolos especiales, palabras reservadas
    def name(self):
        print("name")
        if self.check_token(TokenType.IDENT):
            # it's the name of a new stack
            if self.cur_token.text in self.names_declared:
                self.abort("Nombre de Pila {} ya declarado anteriormente".format(
                    self.cur_token.text))
            elif len(self.cur_token.text) == 0 or self.cur_token.text[0].isdigit():
                self.abort("Nombre de Pila {} Incorrecto - no puede comenzar con numero".format(
                    self.cur_token.text))
            for tok in TokenType:
                if tok.value >= 2 and self.cur_token.text == tok.name:
                    self.abort(
                        "Nombre de Pila {} Incorrecto - palabra reservada".format(self.cur_token.text))
            self.names_declared.append(self.cur_token.text)
            self.next_token()
        else:
            self.abort("Esperado Nombre de Pila")

    # <contenido> := NO TIENE CARTAS | TIENE <lista de cartas>
    def content(self):
        print("content")
        if self.check_token(TokenType.NO):
            self.match_phrase(
                [TokenType.NO, TokenType.TIENE, TokenType.CARTAS])
        elif self.check_token(TokenType.TIENE):
            self.next_token()
            self.cards_list()

        else:
            self.abort(
                "Se esperaba NO o TIENE pero se encuentra {}".format(self.cur_token.text))

    # <lista de cartas> := <descripcion de carta> | <descripcion de carta> - nl* <lista de cartas>
    def cards_list(self):
        print("card list")
        self.card_description()

        while self.check_token(TokenType.DASH):
            self.next_token()


            self.skip_whitespace_tokens()

            self.card_description()

    # <descripcion de carta> := <numero> DE <palos> <posicion>
    def card_description(self):
        print("card description")
        self.number()
        self.match(TokenType.DE)
        self.palos()
        self.position()

    # <numero> := 1 | 2 | 3 | 4 | 5 | 6 | 7 | 10 | 11 | 12
    def number(self):
        print("number")
        if self.check_token(TokenType.NUMBER):
            valid_nums = [i for i in range(1, 8)] + [i for i in range(10, 13)]
            if not int(self.cur_token.text) in valid_nums:
                self.abort("Tiene que ser un numero entre 1 y 7 o 10 y 12")

            self.next_token()
        else:
            self.abort(
                "Se esperaba un numero, en cambio hay {}".format(self.cur_token.text))

    # <palos> := OROS | BASTOS | ESPADAS | COPAS
    def palos(self):
        print("palos")
        if self.check_token(TokenType.OROS) or \
                self.check_token(TokenType.BASTOS) or \
                self.check_token(TokenType.ESPADAS) or self.check_token(TokenType.COPAS):

            self.next_token()
        else:
            self.abort(
                "Se esperaba un palo de carta, en cambio se tiene {}".format(self.cur_token.text))

    # <posicion> := BOCA ARRIBA | BOCA ABAJO
    def position(self):
        print("position")
        self.match(TokenType.BOCA)

        if self.check_token(TokenType.ARRIBA):

            self.next_token()
        elif self.check_token(TokenType.ABAJO):

            self.next_token()
        else:
            self.abort(
                "Se esperaba ARRIBA o ABAJO, en cambio se tiene {}".format(self.cur_token.text))

    def process(self):
        print(self.names_declared)
