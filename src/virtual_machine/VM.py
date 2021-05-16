from cards import Position


class VirtualMachine():

    def __init__(self, opcodes, stacks_list):
        """
        Opcodes: a list of strings that contains opcodes to be executed by 
        virtual machine
        stack_sets: a list of strings that contains opcodes to set up stacks
        """
        self.opcodes = opcodes
        self.stacks_list = stacks_list
        self.pc = 0  # starting the program at the beginning of the opcodes list
        self.stacks = []  # will contain the stacks of cards
