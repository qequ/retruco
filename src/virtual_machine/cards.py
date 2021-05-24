from enum import Enum


class Position(Enum):
    FACE_UP = 1
    FACE_DOWN = 2


class Card():

    def __init__(self, value, type_card, position=Position.FACE_UP):
        """
        type: O(ro), B(asto), C(opa), E(spada)
        Value: 1, 2, 3, ..., 12
        position: face up / face down 
        """
        self.type = type_card
        self.value = value
        self.position = position

    def swap_position(self):
        if self.position == Position.FACE_DOWN:
            self.position = Position.FACE_UP
        else:
            self.position = Position.FACE_DOWN
