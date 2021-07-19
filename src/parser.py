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

    def check_token_list(self, kind_list):
        """
        Return true if the current token matches one of the kind given.
        """

        for k in kind_list:
            if k == self.cur_token.kind:
                return True

        return False

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
            self.abort("Se esperaba " + kind.name +
                       ", se encuentra " + self.cur_token.kind.name)
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

    # programa ::=   <declaraciones> ; nl* <proceso>
    def program(self):
        print("PROGRAM")

        # Since some newlines are required in our grammar, need to skip the excess.
        self.skip_whitespace_tokens()

        self.declarations()
        self.match(TokenType.SEMICOLON)
        self.skip_whitespace_tokens()
        self.process()

        for stack_names in self.names_listed:
            if not stack_names in self.names_declared:
                self.abort(
                    "Declarada una pila que no existe: {}".format(stack_names))

    # <declaraciones> := UCP EJECUTE CON LAS SIGUIENTES CARTAS nl <lista de pilas>

    def declarations(self):
        self.skip_whitespace_tokens()

        self.match_phrase([TokenType.UCP,
                           TokenType.EJECUTE,
                           TokenType.CON,
                           TokenType.LAS,
                           TokenType.SIGUIENTES,
                           TokenType.CARTAS,
                           TokenType.NEWLINE])
        # the previous counting the previous NEWLINE token
        self.code_line += 1

        while not self.check_token(TokenType.SEMICOLON):
            self.stacks_list()

    # <lista de pilas> := <descripcion de pila> | <descripcion de pila> , nl* <lista de pilas>
    def stacks_list(self):
        self.stack_description()

        while self.check_token(TokenType.COMMA):
            self.next_token()

            # allow newlines to improve code legibility
            self.skip_whitespace_tokens()

            self.stack_description()

    # <descripcion de pila> := <pila> <nombre> <contenido>
    def stack_description(self):
        self.stack()
        self.name()
        self.content()

    # <pila> := LA PILA | PILA
    def stack(self):
        if self.check_token(TokenType.LA):
            self.match_phrase([TokenType.LA, TokenType.PILA])

        elif self.check_token(TokenType.PILA):
            self.next_token()
        else:
            self.abort(
                "Se esperaba LA PILA O PILA, en cambio se encuentra {}".format(self.cur_token.text))

    # <nombre> := str alfanumérico que no comienza con número ni contiene símbolos especiales, palabras reservadas
    def name(self, called_by_process=False):
        print("name")
        if self.check_token(TokenType.IDENT):

            if called_by_process:
                if self.cur_token.text in self.names_declared:
                    # emitter placeholder
                    self.next_token()
                else:
                    self.abort("Nombre de Pila {} no declarado".format(
                        self.cur_token.text))

            else:
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
            self.abort("Esperado Nombre de Pila, en cambio se encuentra {}".format(
                self.cur_token.text))

    # <contenido> := NO TIENE CARTAS | TIENE <lista de cartas>
    def content(self):
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
        self.card_description()

        while self.check_token(TokenType.DASH):
            self.next_token()

            self.skip_whitespace_tokens()

            self.card_description()

    # <descripcion de carta> := <numero> DE <palos> <posicion>
    def card_description(self):
        self.number()
        self.match(TokenType.DE)
        self.palos()
        self.position()

    # <numero> := 1 | 2 | 3 | 4 | 5 | 6 | 7 | 10 | 11 | 12
    def number(self, used_by_process=False):
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
    def palos(self, used_for_process=False):
        print("palos")
        if self.check_token(TokenType.OROS
                            ) or \
                self.check_token(TokenType.BASTOS) or \
                self.check_token(TokenType.ESPADAS) or self.check_token(TokenType.COPAS):

            self.next_token()
        else:
            self.abort(
                "Se esperaba un palo de carta, en cambio se tiene {}".format(self.cur_token.text))

    # <posicion> := BOCA ARRIBA | BOCA ABAJO
    def position(self):
        self.match(TokenType.BOCA)

        if self.check_token(TokenType.ARRIBA):

            self.next_token()
        elif self.check_token(TokenType.ABAJO):

            self.next_token()
        else:
            self.abort(
                "Se esperaba ARRIBA o ABAJO, en cambio se tiene {}".format(self.cur_token.text))

    def process(self):
        print("PROCESS")
        self.match_phrase([TokenType.DEFINICION, TokenType.DE,
                          TokenType.PROGRAMA, TokenType.NEWLINE])
        self.code_line += 1

        self.statements(TokenType.EOF)

    # <sentencias> := <sentencia> | <sentencia> nl+ <sentencias>

    def statements(self, delimiter_kind):
        delim_list = []
        delim_list.append(TokenType.EOF)
        delim_list.append(delimiter_kind)

        while not self.check_token_list(delim_list):
            self.statement()

    def statement(self):
        # check which of the possible instruction is

        if self.check_token(TokenType.TOME):
            self.take()

        elif self.check_token(TokenType.DEPOSITE) or self.check_token(TokenType.DEPOSITELA):
            self.deposit()

        elif self.check_token(TokenType.INVIERTA) or self.check_token(TokenType.INVIERTALA):
            self.invert()

        elif self.check_token(TokenType.SI):
            self.selection()

        elif self.check_token(TokenType.MIENTRAS):
            self.iteration()

        else:
            self.abort("Se esperaba una operacion: TOME, DEPOSITE, INVIERTA, SI, MIENTRAS. En cambio, se encuentra: {}".format(
                self.cur_token.kind))

        self.nl()

    # <tomar> DE <pila> <nombre>

    def take(self):
        print("tomar")
        self.match(TokenType.TOME)
        if self.check_token(TokenType.UNA):
            self.next_token()
            if self.check_token(TokenType.CARTA):
                self.next_token()

        self.match(TokenType.DE)
        self.stack()
        self.name(True)

    # <depositar> EN <pila> <nombre>
    def deposit(self):
        print("depositar")
        if self.check_token(TokenType.DEPOSITE):
            self.match_phrase(
                [TokenType.DEPOSITE, TokenType.LA, TokenType.CARTA])
        else:
            self.match(TokenType.DEPOSITELA)
        self.match(TokenType.EN)
        self.stack()
        self.name(True)

    # <invertir>
    def invert(self):
        print("invertir")
        if self.check_token(TokenType.INVIERTA):
            self.match_phrase(
                [TokenType.INVIERTA, TokenType.LA, TokenType.CARTA])
        else:
            self.match(TokenType.INVIERTALA)

        # emit

    # <de seleccion> := SI <condicion> nl+ <sentencias> SINO nl+ <sentencias> NADA MAS |
    #                   SI <condicion> nl+ <sentencias> SINO nl+ NADA MAS

    def selection(self):
        print("selection")
        self.match(TokenType.SI)
        self.condition()
        self.nl()
        self.statements(TokenType.SINO)
        self.match(TokenType.SINO)
        self.nl()
        if self.check_token(TokenType.NADA):
            self.match_phrase([TokenType.NADA, TokenType.MAS])
        else:
            self.statements(TokenType.NADA)
            self.match_phrase([TokenType.NADA, TokenType.MAS])

    def condition(self):
        print("condicion")
        self.simple_condition()

        while self.check_token(TokenType.Y) or self.check_token(TokenType.O):
            self.next_token()
            self.simple_condition()

    # <condicion simple> := <condicion de pila vacia> | <condiciones de carta>
    def simple_condition(self):
        print("condicion simple")
        if self.check_token(TokenType.CARTA) or self.check_peek(TokenType.CARTA):
            self.card_conditions()
        elif self.check_token(TokenType.PILA) or self.check_peek(TokenType.PILA):
            self.empty_stack_condition()
        else:
            self.abort("Se esperaba LA PILA, PILA, LA CARTA, CARTA. En cambio, se encuentra {}".format(
                self.cur_token.text))

    # <condicion de pila vacia> := <pila> <nombre> ESTA VACIA | <pila> <nombre> NO ESTA VACIA
    def empty_stack_condition(self):
        print("condicion pila vacia")
        self.stack()
        self.name(True)

        if self.check_token(TokenType.NO):
            self.match_phrase([TokenType.NO, TokenType.ESTA, TokenType.VACIA])
            # emit
        elif self.check_token(TokenType.ESTA):
            self.match_phrase([TokenType.ESTA, TokenType.VACIA])
            # emit
        else:
            self.abort("Se esperaba NO ESTA, ESTA. En cambio, se encuentra {}".format(
                self.cur_token.text))

    # <condicion de carta> := <estado> | <caracteristica>
    # <estado> := <carta> ESTA BOCA ABAJO | <carta> NO ESTA BOCA ABAJO
    # <caracteristica> := <carta> <es o no es> <de palos> | <carta> <es o no es> <valor> | <carta> ES DE <relac> PALO QUE TOPE DE <pila> <nombre>

    def card_conditions(self):
        print("condiciones de carta")
        self.card()

        if (self.check_token(TokenType.NO) and self.check_peek(TokenType.ESTA)) or self.check_token(TokenType.ESTA):
            self.state()
        elif self.check_token(TokenType.ES) and self.check_peek(TokenType.DE):
            self.relation_palo_stack()
        elif self.check_token(TokenType.NO) and self.check_peek(TokenType.ES) or self.check_token(TokenType.ES):
            self.is_it()

            # check if its_of_palos
            if (self.check_token(TokenType.DEL) and self.check_peek(TokenType.PALO)) or self.check_token(TokenType.OROS) \
                    or self.check_token(TokenType.BASTOS) or self.check_token(TokenType.ESPADAS) or self.check_token(TokenType.COPAS):
                self.of_palos()
            else:
                self.value()

        else:
            self.abort("Condicion de Carta mal formada")

    # <valor> := DE <rela> VALOR QUE TOPE DE <pila> <nombre> | DE VALOR <relacion> <numero> | <relacion> <numero>
    def value(self):
        print("valor")
        if self.check_token(TokenType.DE):
            self.next_token()
            # DE <rela> VALOR QUE TOPE DE <pila> <nombre> | DE VALOR <relacion> <numero>
            if self.check_token(TokenType.VALOR):
                # DE VALOR <relacion> <numero>
                self.next_token()
                self.relation()
                self.number(True)
            else:
                # DE <rela> VALOR QUE TOPE DE <pila> <nombre>
                self.rela()
                self.match_phrase(
                    [TokenType.VALOR, TokenType.QUE, TokenType.TOPE, TokenType.DE, TokenType.PILA])
                self.name(True)
        else:
            self.relation()
            self.number(True)

    # <rela> := IGUAL | DISTINTO | MAYOR | MENOR | MAYOR O IGUAL | MENOR O IGUAL

    def rela(self):
        if self.check_token(TokenType.IGUAL):
            self.next_token()

        elif self.check_token(TokenType.DISTINTO):
            self.next_token()

        elif self.check_token(TokenType.MAYOR):
            if self.check_peek(TokenType.O):
                self.match_phrase(
                    [TokenType.MAYOR, TokenType.O, TokenType.IGUAL])
            else:
                self.next_token()

        elif self.check_token(TokenType.MENOR):
            if self.check_peek(TokenType.O):
                self.match_phrase(
                    [TokenType.MENOR, TokenType.O, TokenType.IGUAL])
            else:
                self.next_token()

        else:
            self.abort("Se esperaba una relacion; IGUAL, DISTINTO, MAYOR, MENOR... En cambio, se encuentra {}".format(
                self.cur_token.text))

    # <relacion> := IGUAL A | DISTINTO DE | MAYOR QUE | MENOR QUE | MAYOR O IGUAL A | MENOR O IGUAL A

    def relation(self):
        if self.check_token(TokenType.IGUAL):
            self.match_phrase([TokenType.IGUAL, TokenType.A])

        elif self.check_token(TokenType.DISTINTO):
            self.match_phrase([TokenType.DISTINTO, TokenType.DE])

        elif self.check_token(TokenType.MAYOR):
            if self.check_peek(TokenType.O):
                self.match_phrase(
                    [TokenType.MAYOR, TokenType.O, TokenType.IGUAL, TokenType.A])
            else:
                self.match_phrase([TokenType.MAYOR, TokenType.QUE])

        elif self.check_token(TokenType.MENOR):
            if self.check_peek(TokenType.O):
                self.match_phrase(
                    [TokenType.MENOR, TokenType.O, TokenType.IGUAL, TokenType.A])
            else:
                self.match_phrase([TokenType.MENOR, TokenType.QUE])
        else:
            self.abort("Se esperaba una relacion; IGUAL, DISTINTO, MAYOR, MENOR... En cambio, se encuentra {}".format(
                self.cur_token.text))

    # <de palos> := DEL PALO <palos> | <palos>

    def of_palos(self):
        if self.check_token(TokenType.DEL):
            self.match_phrase([TokenType.DEL, TokenType.PALO])

        self.palos()

    # <carta> ESTA BOCA ABAJO | <carta> NO ESTA BOCA ABAJO
    def state(self):
        print("estado")
        if self.check_token(TokenType.NO):
            self.match_phrase([TokenType.NO, TokenType.ESTA,
                              TokenType.BOCA, TokenType.ABAJO])

        elif self.check_token(TokenType.ESTA):
            self.match_phrase(
                [TokenType.ESTA, TokenType.BOCA, TokenType.ABAJO])

        else:
            self.abort("Esperado NO ESTA... O ESTA... En cambio, se encuentra {}".format(
                self.cur_token))

    # <carta> ES DE <relac> PALO QUE TOPE DE <pila> <nombre>
    def relation_palo_stack(self):
        self.match_phrase([TokenType.ES, TokenType.DE])

        if self.check_token(TokenType.IGUAL):
            self.next_token()
        elif self.check_token(TokenType.DISTINTO):
            self.next_token()
        else:
            self.abort("Esperado IGUAL o DISTINTO. En cambio, se encuentra {}".format(
                self.cur_token.text))

        self.match_phrase([TokenType.PALO, TokenType.QUE,
                          TokenType.TOPE, TokenType.DE])
        self.stack()
        self.name(True)

    # <es o no es> := ES | NO ES
    def is_it(self):
        if self.check_token(TokenType.ES):
            self.next_token()
        elif self.check_token(TokenType.NO):
            self.match_phrase([TokenType.NO, TokenType.ES])
        else:
            self.abort("Esperado ES o NO ES. En cambio, se encuentra {}".format(
                self.cur_token.text))

    def card(self):
        if self.check_token(TokenType.LA):
            self.match_phrase([TokenType.LA, TokenType.CARTA])

        elif self.check_token(TokenType.CARTA):
            self.next_token()
        else:
            self.abort(
                "Se esperaba LA CARTA O CARTA, en cambio se encuentra {}".format(self.cur_token.text))

    # nl+ ::= '\n'+

    def nl(self):
        print("NEWLINE")
        # Require at least one newline.
        self.match(TokenType.NEWLINE)
        self.code_line += 1
        # But we will allow extra newlines too, of course.
        self.skip_whitespace_tokens()
