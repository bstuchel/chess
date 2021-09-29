""" File: game.py
This file contains the Game class which controls the logic for the game
"""
import chess


class Game:
    def __init__(self):
        self.board = chess.Board()
        self.captured_value = [0, 0]

    def move(self, from_coord, to_coord, promotion=None):
        """ Creates a move object and pushed the move if it is legal """
        from_square = chess.square(from_coord[0], from_coord[1])
        to_square = chess.square(to_coord[0], to_coord[1])
        move = chess.Move(from_square, to_square, promotion)
        if move in self.board.legal_moves:
            if self.board.is_capture(move):
                captured_piece = self.board.piece_at(to_square)
                if not captured_piece: # En passant
                    captured_piece = chess.Piece(chess.PAWN, not self.board.turn)
                self.capture(captured_piece)
            self.board.push(move)

    def capture(self, piece):
        color = 0 if piece.color == chess.WHITE else 1
        if piece.piece_type == chess.QUEEN: val = 9
        elif piece.piece_type == chess.ROOK: val = 5
        elif piece.piece_type == chess.BISHOP: val = 3
        elif piece.piece_type == chess.KNIGHT: val = 3
        elif piece.piece_type == chess.PAWN: val = 1
        self.captured_value[color] += val

    def is_promotion(self, from_coord, to_coord):
        """ Returns whether or not the piece can be promted """
        from_square = chess.square(from_coord[0], from_coord[1])
        piece = self.board.piece_at(from_square)
        if not piece:
            return False
        promo_rank = 7 if piece.color == chess.WHITE else 0
        return piece.piece_type == chess.PAWN and to_coord[1] == promo_rank

    def is_game_over(self):
        """ Returns whether the game is over """
        return bool(self.board.outcome())
