import argparse
import sys

from .compiler.emitter import Emitter
from .compiler.lexer import Lexer
from .compiler.parser import Parser
from .virtual_machine.vm import VirtualMachine


def build_arg_parser():
    parser = argparse.ArgumentParser(
        prog="retruco",
        description="Un interprete para el lenguaje de programacion TIMBA.",
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="archivo fuente TIMBA a ejecutar",
    )
    parser.add_argument(
        "-g",
        "--gui",
        action="store_true",
        dest="use_gui",
        help="abre el editor de Retruco",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        dest="debug",
        help="muestra los opcodes generados por el compilador y los estados "
        "de las pilas despues de ejecutar cada instruccion",
    )
    return parser


def run_file(path, debug=False):
    with open(path) as input_file:
        source = input_file.read()

    lexer = Lexer(source)
    emitter = Emitter()

    parser = Parser(lexer, emitter)
    parser.program()  # Start the parser.

    if emitter.check_repeated_cards():
        print("Error - Se encontraron cartas repetidas en las pilas")
        sys.exit(1)

    if debug:
        print("stacks instructions")
        print(emitter.stacks_instructions)
        print("----------")
        print("process instructions")
        print(emitter.process_instructions)
        print("----------")

    vm = VirtualMachine(
        emitter.process_instructions, emitter.stacks_instructions, debug
    )
    vm.run()

    print("Estado final")
    vm.show_machine_status(parser.names_declared)


def main(argv=None):
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    if args.use_gui:
        from .gui_retruco import Retruco

        rt = Retruco()
        rt.mainloop()
        return

    if not args.file:
        parser.print_help()
        sys.exit(1)

    run_file(args.file, args.debug)


if __name__ == "__main__":
    main()
