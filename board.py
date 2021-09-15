""" File: board.py
This file contains the board class that holds pieces and their locations
"""
from piece import Color, Pawn, Knight, Bishop, Rook, Queen, King


class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.set_board()

    def set_board(self):
        """ Sets the board by creating pieces and placing them in their 
        starting squares 
        """
        self.board[0][0] = Rook(Color.BLACK)
        self.board[0][1] = Knight(Color.BLACK)
        self.board[0][2] = Bishop(Color.BLACK)
        self.board[0][3] = Queen(Color.BLACK)
        self.board[0][4] = King(Color.BLACK)
        self.board[0][5] = Bishop(Color.BLACK)
        self.board[0][6] = Knight(Color.BLACK)
        self.board[0][7] = Rook(Color.BLACK)
        self.board[7][0] = Rook(Color.WHITE)
        self.board[7][1] = Knight(Color.WHITE)
        self.board[7][2] = Bishop(Color.WHITE)
        self.board[7][3] = Queen(Color.WHITE)
        self.board[7][4] = King(Color.WHITE)
        self.board[7][5] = Bishop(Color.WHITE)
        self.board[7][6] = Knight(Color.WHITE)
        self.board[7][7] = Rook(Color.WHITE)
        for i in range(8):
            self.board[1][i] = Pawn(Color.BLACK)
        for i in range(8):
            self.board[6][i] = Pawn(Color.WHITE)
