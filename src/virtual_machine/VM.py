from cards import Card, Position


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
        self.whilestack = []  # will keep an address stack to return
        self.endwhilequeue = []  # address stack to jump when while ends
        self.stacks = []  # will contain the stacks of cards
        self.hand = None  # the card that UCP holds in it hand
        # if any problem occurs during instructions execution this flag
        # contains the problem type
        # 0 == EXECUTION_OK
        # 1 == FULL_HAND_ERROR
        # 2 == EMPTY_STACK_ERROR
        # 3 == EMPTY_HAND_ERROR
        self.error_code = 0

    def load_stacks(self):
        """
        Precondition: there are no repeated cards - the compiler must
        handle that error.
        Decodes the stack opcodes and creates the stacks and the cards
        they belong.
        Instruction form; SVP
        S: index of stack they belong, if there is no stack with that index
        it will be created.
        V: value of the card; {1,..., 7, 10, ..., 12}
        P: Palos of the game {O(ro), B(asto), E(spada), C(opa)}
        all the cards are face up when inserted.
        """

        for ins in self.stacks_opcodes:
            # decode the instruction
            sp = int(ins[0])
            v = int(ins[1])
            p = ins[2]
            try:
                self.stacks[sp].append(Card(v, p))
            except IndexError:
                self.stacks.insert(sp, [])
                self.stacks[sp].append(Card(v, p))

    def take_card(self):
        # OPCODE FORM: 0S where S is stack number
        opcode = self.opcodes[self.pc]

        if self.hand != None:
            # I'm already holdoing a card in hand
            self.error_code = 1
            return

        if len(self.stacks[int(opcode[0])]) == 0:
            self.error_code = 2
            return

        self.hand = self.stacks[int(opcode[1])].pop()

    def deposit_hand_card(self):
        # OPCODE FORM: 1S where S is stack number
        opcode = self.opcodes[self.pc]

        if self.hand == None:
            self.error_code = 3
            return

        self.stacks[int(opcode[1])].append(self.hand)
        self.hand = None

    def invert_hand_card(self):
        # OPCODE == 2
        if self.hand == None:
            self.error_code = 3
            return
        self.hand.swap_position()

    def execute_instruction(self):
        print(self.opcodes[self.pc][0])
        inst_type = self.opcodes[self.pc][0]

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
            if self.error_code == 1:
                print("ERRROR CODE 1 - FULL_HAND_ERROR")
            elif self.error_code == 2:
                print("ERRROR CODE 2 - EMPTY_STACK_ERROR")
            elif self.error_code == 3:
                print("ERROR CODE 3 - EMPTY_HAND_ERROR")
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
