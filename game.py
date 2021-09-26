""" File: game.py
This file contains the Game class which controls the logic for the game
"""
import chess


class Game:
    def __init__(self):
        self.board = chess.Board()

    def move(self, from_coord, to_coord, promotion=None):
        from_square = chess.square(from_coord[0], from_coord[1])
        to_square = chess.square(to_coord[0], to_coord[1])
        move = chess.Move(from_square=from_square, to_square=to_square, 
                          promotion=promotion)
        if move in self.board.legal_moves:
            self.board.push(move)

    def is_promotion(self, from_coord, to_coord):
        from_square = chess.square(from_coord[0], from_coord[1])
        piece = self.board.piece_at(from_square)
        if not piece:
            return False
        promo_rank = 7 if piece.color == chess.WHITE else 0
        return piece.piece_type == chess.PAWN and to_coord[1] == promo_rank

    def is_game_over(self):
        return bool(self.board.outcome())
