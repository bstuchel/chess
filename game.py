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
        rank, file = square
        if self.board.board[rank][file]:
            self.picked_piece = self.board.board[rank][file]
            self.board.board[rank][file] = None
            self.picked_from = square

    def put_piece(self, square):
        rank, file = square
        if self.picked_piece and self.board.board[rank][file] == None:
            self.board.board[rank][file] = self.picked_piece
            self.picked_piece = None
            self.move_log.append(f'{self.picked_from}->{square}')