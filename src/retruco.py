import sys
from optparse import OptionParser
from retruco_gui import Retruco

from lexer import *
from emitter import *
from parser import *
from virtual_machine.vm import VirtualMachine


parser = OptionParser(usage="usage: %prog [options] [file]")
parser.add_option("-g", "--gui", action="store_true", default=False, dest="use_gui",
                  help="abre el editor de Retruco")


(options, args) = parser.parse_args()


# main program

if options.use_gui:
    rt = Retruco()
    rt.mainloop()

else:
    if len(args) != 1:
        parser.print_help()
        sys.exit(1)

    with open(sys.argv[1], 'r') as inputFile:
        input = inputFile.read()

    lexer = Lexer(input)
    emitter = Emitter()

    parser = Parser(lexer, emitter)
    parser.program()  # Start the parser.
    print("Parsing completed.")
    print(emitter.stacks_instructions)
    print(emitter.process_instructions)

    vm = VirtualMachine(emitter.process_instructions,
                        emitter.stacks_instructions)

    vm.run()

    print("Estado final")
    vm.show_machine_status(parser.names_declared)
