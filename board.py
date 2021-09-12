""" File: board.py
This file contains the board class that controls the logic for the chess game
"""
from piece import Pawn, Knight, Bishop, Rook, Queen, King


class Board():
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.score = {"white": 0, "black": 0}
        self.move_log = []
        self.set_board()

    def set_board(self):
        """ Sets the board by creating pieces and placing them in their 
        starting squares 
        """
        self.board[0][0] = Rook(False)
        self.board[0][1] = Knight(False)
        self.board[0][2] = Bishop(False)
        self.board[0][3] = Queen(False)
        self.board[0][4] = King(False)
        self.board[0][5] = Bishop(False)
        self.board[0][6] = Knight(False)
        self.board[0][7] = Rook(False)
        self.board[7][0] = Rook(True)
        self.board[7][1] = Knight(True)
        self.board[7][2] = Bishop(True)
        self.board[7][3] = Queen(True)
        self.board[7][4] = King(True)
        self.board[7][5] = Bishop(True)
        self.board[7][6] = Knight(True)
        self.board[7][7] = Rook(True)
        for i in range(8):
            self.board[1][i] = Pawn(False)
        for i in range(8):
            self.board[6][i] = Pawn(True)
