from cards import *


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
        self.endwhilestack = []  # address stack to jump when while ends
        self.whileflag = False
        self.stacks = []  # will contain the stacks of cards
        self.hand = None  # the card that UCP holds in it hand

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
