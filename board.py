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
        for color in [Color.WHITE, Color.BLACK]:
            rank = 0 if color == Color.BLACK else 7
            self.board[rank][0] = Rook(color)
            self.board[rank][1] = Knight(color)
            self.board[rank][2] = Bishop(color)
            self.board[rank][3] = Queen(color)
            self.board[rank][4] = King(color)
            self.board[rank][5] = Bishop(color)
            self.board[rank][6] = Knight(color)
            self.board[rank][7] = Rook(color)
        for i in range(8):
            self.board[1][i] = Pawn(Color.BLACK)
        for i in range(8):
            self.board[6][i] = Pawn(Color.WHITE)
