import pyxel
from editor import Editor


class App():
    def __init__(self):
        pyxel.init(256, 256, caption="Retruco", fullscreen=True)
        #self.program = ""
        self.ed = Editor()

        pyxel.run(self.update, self.draw)
        # after this no code will be executed

    def update(self):

        self.ed.add_char()

    def draw(self):
        pyxel.cls(0)

        pyxel.rect(0, 0, 256, 256, 3)

        pyxel.text(0, 0, self.ed.program, 10)


App()
