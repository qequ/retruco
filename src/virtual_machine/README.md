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
A LOGICCOND is a string encoding of variable length that serves to check logic conditions about a card that is kept in the Hand register or about the stacks. This string is always appended to an IF or WHILE opcode.


_Types of logic conditions_
   1. Conditions about stacks


       a LOGICCOND about a stack of cards is mainly to check if the stack is empty or not. The encoding is of the form **Px1...xn{E, N}** where x1...xn is the number of the stack, that exists,  and N serves as the negative of the proposition, otherwise use E.
       
       
       e.g. _P0E_: This is a logic proposition that means "The stack 0 is empty"
       
         _P1N_: This means "The stack 1 is not empty"

   2. Conditions about Hand register
        
        
        a LOGICCOND about the card that you have in the Hand register covers more logic conditions, which are summarized in the following two patterns and will be broken down later
        
        **C{E, N}{F, E, B, C, O, Px1...xn}**
        **C{E, N}{!=, =, <, >, <=, >=}{[1,2,...7, 10,...12], Px1...xn}**
       
       
       As the previous condition about the stack, the {E, N} part of the encoding serves to negate(or let with that truth value) the statement.
       
       
       * **C{E, N}F**: The card is, or not, in the Face Down Position
       * **C{E, N}{E, B, C, O}**: The card is, or not, of the Palo **E**spada, **B**asto, **C**opa, **O**ro
       * **C{E, N}PX1...XN**: The card has, or not, the same Palo as the the card at the top of the stack **x1...xn**
       * **C{E, N}{!=, =, <, >, <=, >=}[1,2,...7, 10,...12]**: The value of the card is compared using one of the classic comparison operators with a given number of the possible subset of spanish cards allowed numbers(no 8 or 9)
       * **C{E, N}{!=, =, <, >, <=, >=}Px1...xn**: The same statement as the previous but instead of comparing the value of the card with a given number it's compared with the value of the card at the top of the stack **x1....xn**
       

All of the LOGICCOND listed before can be combined using **&**(AND) and **|**(OR).

e.g. P0E&CE=P0 decodes to the statement "The stack 0 is not empty and the card in the hand register has the same value that the card at the top of the stack 0"


### Error codes
After the execution of every instruction the vm variable `error_code` if an error happened. The possible errors are listed below.
* 0 - EXECUTION OK: No problem ocurred after the opcode execution.
* 1 == FULL_HAND_ERROR: Mainly used when you try to take a card from a stack and you already have a card in the Hand register
* 2 == EMPTY_STACK_ERROR: Used when you try to execute an instruction or decode a logical condition using an empty stack. e.g take a card from an empty stack or compare the Hand register card with an empty stack
* 3 == EMPTY_HAND_ERROR: Similar to the previous error but with the Hand register empty.
* 4 == LOGIC CONDITION ERROR: Used when decoding a malformed LOGICCOND.
* 5 == FACE_DOWN_CARD_LOGIC_ERROR: Used mainly in logic decoding. When one of the cards used in LOGICCOND is in a face down position (and it's not the **C{E, N}F**  proposition) the abstraction can't be broken, i.e. the vm can't know the palo and/or the value of the card. e.g. the vm is decoding CE!=P0 but the card at the top of the stack 0 is face down, i.e. can't compare with the card at the Hand register
