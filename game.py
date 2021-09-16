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

    def find_legal_moves(self):
        for rank in range(8):
            for file in range(8):
                if self.board.board[rank][file]:
                    self.board.board[rank][file].find_legal_moves((rank, file), self.board, self.move_log)

    def pick_piece(self, square):
        """ Pick up a pieces given the square coordinates 
        square: Tuple containing the rank and file indices
        """
        self.find_legal_moves()
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
            if  rank < 8 and file < 8 and (square in self.picked_piece.legal_moves):
                self.board.board[rank][file] = self.picked_piece
                self.picked_piece.has_not_moved = False
                self.picked_piece = None
                self.move_log.append((self.picked_from,square))
            else:
                self.board.board[self.picked_from[0]][self.picked_from[1]] = self.picked_piece
                self.picked_piece = None
