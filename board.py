""" File: board.py
This file contains the board class that holds pieces and their locations
"""
from piece import Pawn, Knight, Bishop, Rook, Queen, King


class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.set_board()

    def set_board(self):
        """ Sets the board by creating pieces and placing them in their 
        starting squares 
        """
        self.board[0][0] = Rook('b')
        self.board[0][1] = Knight('b')
        self.board[0][2] = Bishop('b')
        self.board[0][3] = Queen('b')
        self.board[0][4] = King('b')
        self.board[0][5] = Bishop('b')
        self.board[0][6] = Knight('b')
        self.board[0][7] = Rook('b')
        self.board[7][0] = Rook('w')
        self.board[7][1] = Knight('w')
        self.board[7][2] = Bishop('w')
        self.board[7][3] = Queen('w')
        self.board[7][4] = King('w')
        self.board[7][5] = Bishop('w')
        self.board[7][6] = Knight('w')
        self.board[7][7] = Rook('w')
        for i in range(8):
            self.board[1][i] = Pawn('b')
        for i in range(8):
            self.board[6][i] = Pawn('w')
