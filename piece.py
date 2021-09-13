""" File: piece.py
This file contains the Piece class and subclasses for each piece type
"""


class Piece:
    def __init__(self, color):
        self.color = color
        self.is_captured = False
        self.has_not_moved = True
        self.legal_moves = []
        self.sprite = None


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.filename = f"{color}p.png"
        self.value = 1


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.filename = f"{color}n.png"
        self.value = 3


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.filename = f"{color}b.png"
        self.value = 3


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.filename = f"{color}r.png"
        self.value = 5


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.filename = f"{color}q.png"
        self.value = 9


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.filename = f"{color}k.png"
