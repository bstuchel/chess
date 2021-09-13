""" File: game.py
This file contains the Game class which controls the logic for the game
"""
from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.score = {'w': 0, 'b': 0}
        self.move_log = []
        self.picked_piece = None
        self.picked_from = None

    def pick_piece(self, square):
        """ Pick up a pieces given the square coordinates 
        square: Tuple containing the rank and file indices
        """
        rank, file = square
        if rank < 8 and file < 8 and self.board.board[rank][file]:
            self.picked_piece = self.board.board[rank][file]
            self.board.board[rank][file] = None
            self.picked_from = square

    def put_piece(self, square):
        """ Place a piece at the given coordinates 
        square: Tuple containing the rank and file indices
        """
        rank, file = square
        if self.picked_piece:
            if  rank < 8 and file < 8:
                self.board.board[rank][file] = self.picked_piece
                self.picked_piece = None
                self.move_log.append(f'{self.picked_from}->{square}')
            else:
                self.board.board[self.picked_from[0]][self.picked_from[1]] = self.picked_piece
                self.picked_piece = None