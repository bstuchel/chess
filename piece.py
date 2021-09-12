""" File: piece.py
This file contains the Piece class and subclasses for each piece type
"""

import pygame


class Piece():
    def __init__(self, isWhite):
        self.isWhite = isWhite
        self.is_captured = False
        self.has_not_moved = True
        self.legal_moves = []
        self.sprite = None


class Pawn(Piece):
    def __init__(self, isWhite):
        super().__init__(isWhite)
        self.filename = f"{'w' if isWhite else 'b'}p.png"
        self.value = 1


class Knight(Piece):
    def __init__(self, isWhite):
        super().__init__(isWhite)
        self.filename = f"{'w' if isWhite else 'b'}n.png"
        self.value = 3


class Bishop(Piece):
    def __init__(self, isWhite):
        super().__init__(isWhite)
        self.filename = f"{'w' if isWhite else 'b'}b.png"
        self.value = 3


class Rook(Piece):
    def __init__(self, isWhite):
        super().__init__(isWhite)
        self.filename = f"{'w' if isWhite else 'b'}r.png"
        self.value = 5


class Queen(Piece):
    def __init__(self, isWhite):
        super().__init__(isWhite)
        self.filename = f"{'w' if isWhite else 'b'}q.png"
        self.value = 9


class King(Piece):
    def __init__(self, isWhite):
        super().__init__(isWhite)
        self.filename = f"{'w' if isWhite else 'b'}k.png"
