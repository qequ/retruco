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
