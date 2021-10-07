import sys
from optparse import OptionParser
from typing import DefaultDict
from gui_retruco import Retruco

from lexer import *
from emitter import *
from parser import *
from virtual_machine.vm import VirtualMachine


parser = OptionParser(usage="usage: %prog [options] [file]")
parser.add_option("-g", "--gui", action="store_true", default=False, dest="use_gui",
                  help="abre el editor de Retruco")
parser.add_option("-d", "--debug", action="store_true", default=False, dest="debug",
                  help="muestra los opcodes generados por el compilador y los estados de las pilas después de ejecutar cada instrucción")

(options, args) = parser.parse_args()


# main program

if options.use_gui:
    rt = Retruco()
    rt.mainloop()

else:
    if len(args) != 1:
        parser.print_help()
        sys.exit(1)

    FILE_POS = 1
    if options.debug:
        FILE_POS += 1

    with open(sys.argv[FILE_POS], 'r') as inputFile:
        input = inputFile.read()

    lexer = Lexer(input)
    emitter = Emitter()

    parser = Parser(lexer, emitter)
    parser.program()  # Start the parser.

    if emitter.check_repeated_cards():
        print("Error - Se encontraron cartas repetidas en las pilas")
        sys.exit(1)

    if options.debug:
        print("stacks instructions")
        print(emitter.stacks_instructions)

        print("----------")
        print("process instructions")
        print(emitter.process_instructions)
        print("----------")

    vm = VirtualMachine(emitter.process_instructions,
                        emitter.stacks_instructions, options.debug)

    vm.run()

    print("Estado final")
    vm.show_machine_status(parser.names_declared)
