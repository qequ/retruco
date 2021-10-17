import pyxel

keyboard_dict = {
    pyxel.KEY_0: "0",
    pyxel.KEY_1: "1",
    pyxel.KEY_2: "2",
    pyxel.KEY_3: "3",
    pyxel.KEY_4: "4",
    pyxel.KEY_5: "5",
    pyxel.KEY_6: "6",
    pyxel.KEY_7: "7",
    pyxel.KEY_8: "8",
    pyxel.KEY_9: "9",
    pyxel.KEY_PERIOD: ";",
    pyxel.KEY_MINUS: "-",
    pyxel.KEY_COMMA: ",",
    pyxel.KEY_SPACE: " ",
    pyxel.KEY_A: "A",
    pyxel.KEY_B: "B",
    pyxel.KEY_C: "C",
    pyxel.KEY_D: "D",
    pyxel.KEY_E: "E",
    pyxel.KEY_F: "F",
    pyxel.KEY_G: "G",
    pyxel.KEY_H: "H",
    pyxel.KEY_I: "I",
    pyxel.KEY_J: "J",
    pyxel.KEY_K: "K",
    pyxel.KEY_L: "L",
    pyxel.KEY_M: "M",
    pyxel.KEY_N: "N",
    pyxel.KEY_O: "O",
    pyxel.KEY_P: "P",
    pyxel.KEY_Q: "Q",
    pyxel.KEY_R: "R",
    pyxel.KEY_S: "S",
    pyxel.KEY_T: "T",
    pyxel.KEY_U: "U",
    pyxel.KEY_V: "V",
    pyxel.KEY_W: "W",
    pyxel.KEY_X: "X",
    pyxel.KEY_Y: "Y",
    pyxel.KEY_Z: "Z",
    pyxel.KEY_BACKSPACE: "",
    pyxel.KEY_ENTER: "\n",
    pyxel.KEY_TAB: "    "

}


class Editor():
    def __init__(self) -> None:
        # MAX LEN OF A ROW: 64
        self.program = ""
        # coords of the pointer to show the actual
        self.pointer_x = 0
        self.pointer_y = 0

    def add_char(self):
        for b in keyboard_dict.keys():
            if pyxel.btnp(b):
                if b == pyxel.KEY_BACKSPACE:
                    # delete last char
                    self.program = self.program[:-1]

                elif b == pyxel.KEY_TAB:
                    print("key tab")
                    # add four or less spaces
                    if 64 - self.last_return_char_distance() >= 4:
                        self.program += " " * 4
                    else:
                        self.program += " " * (64 - self.last_return_char_distance())

                elif self.last_return_char_distance() == 64 and b != pyxel.KEY_ENTER:
                    # add a jump line char and then the char
                    self.program += '\n{}'.format(keyboard_dict[b])
                else:
                    self.program += keyboard_dict[b]
                print(len(self.program))
                break

    def last_return_char_distance(self):
        rev_program = self.program[::-1]
        distance = 0

        for c in rev_program:
            if c == '\n':
                return distance
            distance += 1
        # if there is none then it's take in count the start of the string
        return distance
