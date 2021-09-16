""" File: game.py
This file contains the Game class which controls the logic for the game
"""
from board import Board
from piece import Color, King


class Game:
    def __init__(self):
        self.board = Board()
        self.score = {Color.WHITE: 0, Color.BLACK: 0}
        self.move_log = []
        self.picked_piece = None
        self.picked_from = None
        self.picked_piece_moves = None

    def pick_piece(self, square):
        """ Pick up a pieces given the square coordinates 
        square: Tuple containing the rank and file indices
        """
        rank, file = square
        if rank < 8 and file < 8 and self.board.board[rank][file]:
            self.picked_piece = self.board.board[rank][file]
            self.board.board[rank][file] = None
            self.picked_piece_moves = self.picked_piece.get_legal_moves(
                (rank, file), self.board.board, self.move_log)
            self.picked_from = square

    def put_piece(self, square):
        """ Place a piece at the given coordinates 
        square: Tuple containing the rank and file indices
        """
        rank, file = square
        if self.picked_piece:
            if  rank < 8 and file < 8 and (square in self.picked_piece_moves):
                self.board.board[rank][file] = self.picked_piece
                self.picked_piece.has_not_moved = False
                self.move_log.append((self.picked_from,square))
                if isinstance(self.picked_piece, King):
                    if self.picked_piece.color == Color.WHITE:
                        self.board.white_king_square = square
                    else:
                        self.board.black_king_square = square
                self.look_for_checks()
            else:
                rank_start = self.picked_from[0]
                file_start = self.picked_from[1]
                self.board.board[rank_start][file_start] = self.picked_piece
            self.picked_piece = None

    def look_for_checks(self):
        for rank, file in (self.board.white_king_square, 
                           self.board.black_king_square):
            if self.board.board[rank][file].is_in_check(
                (rank, file), self.board.board):
                print(f'{self.board.board[rank][file].color} King is in check')
