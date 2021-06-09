from .cards import Card, Position


class VirtualMachine():

    def __init__(self, opcodes, stacks_opcodes):
        """
        Opcodes: a list of strings that contains opcodes to be executed by 
        virtual machine
        stacks_opcodes: a list of strings that contains opcodes to set up stacks
        """
        self.opcodes = opcodes
        self.stacks_opcodes = stacks_opcodes
        self.pc = 0  # starting the program at the beginning of the opcodes list
        # while opcode helper structures
        self.whilestack = []  # will keep an address stack to return
        self.endwhilestack = []  # address stack to jump when while ends
        # if opcode helper structures
        self.ifflags = []
        self.elsestack = []
        self.endifstack = []
        self.stacks = []  # will contain the stacks of cards
        self.hand = None  # the card that UCP holds in it hand
        # if any problem occurs during instructions execution this flag
        # contains the problem type
        # 0 == EXECUTION_OK
        # 1 == FULL_HAND_ERROR
        # 2 == EMPTY_STACK_ERROR
        # 3 == EMPTY_HAND_ERROR
        # 4 == LOGIC CONDITION ERROR
        # 5 == FACE_DOWN_CARD_LOGIC_ERROR
        self.error_code = 0
        self.last_opcode_address = 0  # useful to show the error in code

    def decode_logical_condition(self, logic_cond):
        log_dec = ""

        if logic_cond[0] == "P":
            # The frontend must ensure that logic_cond[1:-1] stack exists
            # logic_cond == Px1...xn{E, N}
            log_dec = "len(self.stacks[" + logic_cond[1:-1] + "]) == 0"

            if logic_cond[-1] == "N":
                log_dec = "not " + log_dec

        elif logic_cond[0] == "C":
            if self.hand == None:
                # none card has been taken
                self.error_code = 3
                return False

            # possible logic encondings
            # C{E, N}{F, E, B, C, O, Px1...xn}
            # C{E, N}{!=, =, <, >, <=, >=}{[1,2,...7, 10,...12], Px1...xn}
            changing_part = logic_cond[2:]
            if changing_part[0] == "F":
                log_dec = "self.hand.position == Position.FACE_DOWN"
            elif changing_part[0] in ["E", "B", "C", "O"]:
                log_dec = "self.hand.type == '{}'".format(changing_part[0])

            elif changing_part[0] == "P":
                stack_num = int(changing_part[1:])

                if len(self.stacks[stack_num]) == 0:
                    self.error_code = 2
                    return False

                log_dec = "self.hand.type == self.stacks[{}][-1].type".format(
                    stack_num)

            elif changing_part[0] in ["!", "=", "<", ">"]:
                if changing_part[1] == "=":
                    logical_comp = changing_part[:2]
                    offset = 2
                else:
                    logical_comp = changing_part[0]
                    offset = 1

                if changing_part[offset:][0] == "P":
                    # check if the value of the card is equal to the
                    # value of the card at the top of the stack Px1...xn
                    stack_num = int(changing_part[offset+1:])
                    if len(self.stacks[stack_num]) == 0:
                        self.error_code = 2
                        return False

                    log_dec = "self.hand.value {} self.stacks[{}][-1].value".format(
                        logical_comp, stack_num)

                elif changing_part[offset:].isnumeric():
                    # check if the value of the card is equal to a given
                    # number
                    log_dec = "self.hand.value {} {}".format(
                        logical_comp, changing_part[offset:])

                else:
                    self.error_code = 4
                    return False

            else:
                # error decoding logical instruction
                self.error_code = 4
                return False

            if logic_cond[1] == "N":
                log_dec = "not " + log_dec

            if self.hand.position == Position.FACE_DOWN and changing_part[0] != "F":
                self.error_code = 5
                return False
        else:
            self.error_code = 4
            return False

        return eval(log_dec)

    def eval_condition(self, cond):
        """
        method to determine boolean value of an encoded compound proposition.
        cond(ition) is a compound string of encoded propositions.
        &(and) has less precedence than |(or)
        """
        propositions = list(map(lambda s: s.split("&"), cond.split("|")))

        logic = list(map(lambda l: list(
            map(lambda x: self.decode_logical_condition(x), l)), propositions))

        res = []
        for b in logic:
            res.append(all(b))

        return any(res)

    def while_decode(self):
        # OPCODE FORM: 7{COMPOUND ENCODED PROPOSITION}
        if len(self.whilestack) == 0 or self.whilestack[-1] != self.pc:
            # it's a new while loop
            # search for the its endwhile instruction and add it to the
            # endwhile stack
            nested_level = 1
            address = self.pc
            # as a precondition every while opcode has an endwhile opcode
            while nested_level != 0:
                address += 1

                if self.opcodes[address][0] == "7":
                    # nested while
                    nested_level += 1

                elif self.opcodes[address][0] == "8":
                    # found an endwhile
                    if nested_level == 1:
                        # its the endwhile corresponding to the while
                        self.endwhilestack.append(address)
                    nested_level -= 1

            self.whilestack.append(self.pc)

        # the precondition in this part of the code is that
        # the top of both stacks(while and endwhile) has the
        # current while and endwhile addresses
        eval_bool = self.eval_condition((self.opcodes[self.pc])[1:])
        if self.error_code != 0:
            return

        if eval_bool:
            # enter the while loop
            self.pc += 1
        else:
            # jump to the end_while address + 1 opcode
            self.pc = self.endwhilestack.pop() + 1
            self.whilestack.pop()

    def endwhile_decode(self):
        # branching to the while again
        self.pc = self.whilestack[-1]

    def if_decode(self):

        nested_level = 1
        address = self.pc

        while nested_level != 0:
            # looking for the if's else and endif opcodes' addresses
            address += 1

            if self.opcodes[address][0] == "3":
                # nested if
                nested_level += 1

            elif self.opcodes[address][0] == "4" and nested_level == 1:
                # the else of the if
                self.elsestack.append(address)

            elif self.opcodes[address][0] == "5":
                if nested_level == 1:
                    self.endifstack.append(address)
                nested_level -= 1

        # at the top of the stacks its the else and endwhile addresses of this
        # if opcode
        eval_bool = self.eval_condition((self.opcodes[self.pc])[1:])

        if eval_bool:
            self.pc += 1
            self.ifflags.append(True)
        else:
            self.pc = self.elsestack[-1]
            self.ifflags.append(False)

    def else_decode(self):
        if self.ifflags[-1]:
            self.pc = self.endifstack[-1]
        else:
            self.pc += 1

    def endif_decode(self):
        self.ifflags.pop()
        self.elsestack.pop()
        self.pc += 1

    def load_stacks(self):
        """
        Precondition: there are no repeated cards - the compiler must
        handle that error.
        Decodes the stack opcodes and creates the stacks and the cards
        they belong.
        An empty stack instructios should be before of a SPV instruction
        of the same stack
        Instruction form; SPVL || S(if the stack is empty)
        S: index of stack they belong, if there is no stack with that index
        it will be created.
        V: value of the card; {1,..., 7, 10, ..., 12}
        P: Palos of the game {O(ro), B(asto), E(spada), C(opa)}
        all the cards are face up when inserted.
        L: Determines the Face position of the card: U(p) or D(own)
        """

        for ins in self.stacks_opcodes:
            # decode the instruction
            if ins.isnumeric():
                # its an empty stack
                self.stacks.insert(int(ins), [])
            else:
                palo_index = 0
                for i in range(len(ins)):
                    if ins[i] in ["O", "E", "C", "B"]:
                        palo_index = i
                        break

                sp = int(ins[:palo_index])
                v = int(ins[palo_index + 1: -1])
                p = ins[palo_index]
                if ins[-1] == "D":
                    l = Position.FACE_DOWN
                else:
                    l = Position.FACE_UP
                try:
                    self.stacks[sp].append(Card(v, p, l))
                except IndexError:
                    self.stacks.insert(sp, [])
                    self.stacks[sp].append(Card(v, p, l))

    def take_card(self):
        # OPCODE FORM: 0S where S is stack number
        opcode = self.opcodes[self.pc]

        if self.hand != None:
            # I'm already holdoing a card in hand
            self.error_code = 1
            return

        if len(self.stacks[int(opcode[1:])]) == 0:
            self.error_code = 2
            return

        self.hand = self.stacks[int(opcode[1])].pop()

    def deposit_hand_card(self):
        # OPCODE FORM: 1S where S is stack number
        opcode = self.opcodes[self.pc]

        if self.hand == None:
            self.error_code = 3
            return

        self.stacks[int(opcode[1:])].append(self.hand)
        self.hand = None

    def invert_hand_card(self):
        # OPCODE == 2
        if self.hand == None:
            self.error_code = 3
            return
        self.hand.swap_position()

    def execute_instruction(self):
        inst_type = self.opcodes[self.pc][0]
        self.last_opcode_address = self.pc
        # decoding instructions
        if inst_type == "0":
            self.take_card()
            self.pc += 1
        elif inst_type == "1":
            self.deposit_hand_card()
            self.pc += 1
        elif inst_type == "2":
            self.invert_hand_card()
            self.pc += 1
        elif inst_type == "3":
            self.if_decode()
        elif inst_type == "4":
            self.else_decode()
        elif inst_type == "5":
            self.endif_decode()
        elif inst_type == "7":
            self.while_decode()
        elif inst_type == "8":
            self.endwhile_decode()

    def run(self):
        """
        Main loop of the virtual machine
        """
        self.load_stacks()
        while self.pc != len(self.opcodes):
            # fetch - decode - execute
            self.execute_instruction()
            # checking for errors
            if self.error_code != 0:
                break

        if self.error_code != 0:
            # showing error
            print("Error in instruction {} - Address: {}",
                  format(self.opcodes[self.last_opcode_address], self.last_opcode_address))
            if self.error_code == 1:
                print("ERROR CODE 1 - FULL_HAND_ERROR")
            elif self.error_code == 2:
                print("ERROR CODE 2 - EMPTY_STACK_ERROR")
            elif self.error_code == 3:
                print("ERROR CODE 3 - EMPTY_HAND_ERROR")
            elif self.error_code == 4:
                print("ERROR CODE 4 - LOGIC CONDITION ERROR")
            elif self.error_code == 5:
                print("ERROR CODE 5 - FACE_DOWN_CARD_LOGIC_ERROR")

            print("EXECUTION INTERRUPTED")

    def show_machine_status(self):
        """
        prints the stacks and hand cards
        """
        count = 0
        for s in self.stacks:
            print("STACK: {}".format(count))
            for c in s:
                c.print_card()
            count += 1

        print("HAND")
        if self.hand != None:
            self.hand.print_card()
        else:
            print("MANO VACIA")
