class Emitter():
    def __init__(self):
        self.opcode_str = ""
        self.stacks_instructions = []
        self.process_instructions = []

    def append_opcode(self, opc_str):
        """
        concatenate self.opcode_str and opc_str
        """
        self.opcode_str += opc_str

    def reset_opcode_str(self):
        self.opcode_str = ""

    def emit_stack_inst(self):
        """
        append opcode_str to stack_instructions
        """
        self.stacks_instructions.append(self.opcode_str)

    def emit_process_inst(self):
        """
        append opcode_str to process_instructions
        """

        self.process_instructions.append(self.opcode_str)

    def check_repeated_cards(self):
        """
        Returns True if there are repeated cards among the stacks
        """
        stack_opcodes_filt = list(filter(
            lambda s: len(s) > 1, self.stacks_instructions))

        cards_f = list(map(lambda s: s[1:-1], stack_opcodes_filt))

        return len(set(cards_f)) != len(cards_f)
