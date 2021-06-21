# TIMBA2000 specs

the TIMBA2000 is a virtual machine that handles stacks of spanish cards.
The machine has a Harvard architecture(the instructions and the data are in separate memory spaces), and uses a program counter(pc) to move between instructions, like a classic machine. It uses a stack of opcode addresses to handle while loops.

## Usage of the virtual Machine

To instance the virtual machine you need to pass it two lists; a lists of operations opcodes and a list of stack opcodes

## Opcodes of the virtual machine

Previous considerations; 
1. when refering to the palo of a card we refer that is one of four posible values: Oro, Espada, Copa and Basto.
2. A card can be faced Up or faced Down.

### Stack Opcodes
    Used to setup the stacks at the beginning of the virtual machine, the stacks are not setup again, and they can't be created nor destroyed during the execution of the operations opcodes


    _S_ - CREATE an empty stack S
    where S >= 0.


    _SPVL_ - ADD the card with the value numeric V and the palo P in the position in the position  to the stack S
    if the stack doesn't exist it will create it.

    where V ∈ {"1","2","3","4","5","6","7", "10", "11", "12"}
          P ∈ {"O", "E", "B", "C"}
          S >= 0
          L ∈ {"U", "D"}
    
    Note: 
   1. it can be created an stack S and later add instrucitions of the form SPVL but not the other way, otherwise it will crash the machine.
   2. There are no repeated cards. The machine actually can handle any value for a card but we're following the spanish cards standard pattern.

### Operations Opcodes
    Main operations with the cards and stacks.


    0S - TAKE the card at the top of the stack S.
    where  S is a valid stack created before execution.

    1S - DEPOSIT the card that the machine is holding into the stack S.
    where S is a valid stack created before execution

    2 - INVERT the card that the machine is holding.

    3{LOGICCOND} - IF  instruction
    The machine evaluates LOGICCOND. If true the program counter increments by 1, otherwise it will jump to the closest ELSE  instruction that correspond to it.(see ELSE  INSTRUCTION)
    If the machine evaluates LOGICCOND to true and reaches the closest ELSE  instruction that correspond to it, it will jump to the ENDIF  instruction(see ENDIF  instruction)
    For an explanation to LOGICCOND see Logic condition section

    4 - ELSE  instruction. Bounded to the last opcodes

    5 - ENDIF  instruction. Bounded to the two last opcodes

    _Note_: Whenever there is a IF instruction it MUST be an ELSE and ENDIF instructions at some point after it that matches with it, otherwise the machine crashes.

    7{LOGICCOND} - WHILE instruction
    Before evaluate LOGICCOND the machine checks If the opcode address is at the top of the stack, if not it will append it to the while addresses stack and serch its corresponding ENDWHILE instruction(see ENDWHILE instruction) and add it to the endwhile instruction addreses stack.
    Then the machine evaluates LOGICCOND. If true increment the program counter by 1.
    If LOGICCOND evaluates to False it sets the program counter to its ENDWHILE address.  


    8 - ENDWHILE instruction
    pops the WHILE and ENDWHILE stack addreses. Increments the pc by 1.

    _Note_: Whenever there is a WHILE instruction it MUST be an ENDWHILE instructions at some point after it that matches with it, otherwise the machine crashes.

### Logic Conditions
WIP

### Error codes
WIP