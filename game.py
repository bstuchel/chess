""" File: game.py
This file contains the Game class which controls the logic for the game
"""
import chess
from collections import deque


class Game:
    def __init__(self):
        self.board = chess.Board()
        self.captured_value = [0, 0]
        self.undone_moves = deque()

    def reset(self):
        """ Resets the game board and variables """
        self.board.reset()
        self.captured_value = [0, 0]
        self.undone_moves.clear()

    def get_move(self, from_coord, to_coord, promotion=None):
        """ Creates a move object whether or not it's legal 
        :param tuple(int, int) from_coord: The coordinate of the piece's 
            starting location (both coords must be 0-7 inclusive)        
        :param tuple(int, int) to_coord: The coordinate of the piece's ending
            location (both coords must be 0-7 inclusive)
        :param chess.Piece or None promotion: Piece to promote to
        :return: The chess move given starting and ending coords
        :rtype: chess.Move
        """
        from_square = chess.square(from_coord[0], from_coord[1])
        to_square = chess.square(to_coord[0], to_coord[1])
        return chess.Move(from_square, to_square, promotion)

    def user_move(self, move):
        self.move(move)

    def move(self, move):
        """ Make the move if it is legal 
        :param chess.Move move: The move to attempt
        :return: True if the move is legal
        :rtype: bool
        """
        if move not in self.board.legal_moves:
            return False

        self.capture(move)
        self.board.push(move)
        self.undone_moves.clear()
        return True

    def capture(self, move):
        """ If the move is a capture, add the captured piece's value to the 
        game score 
        :param chess.Move move: The move to be checked for captures
        """
        if self.board.is_capture(move):
            color = 0 if self.board.turn == chess.BLACK else 1
            captured_piece = self.board.piece_at(move.to_square)
            if captured_piece:
                if captured_piece.piece_type == chess.QUEEN: val = 9
                elif captured_piece.piece_type == chess.ROOK: val = 5
                elif captured_piece.piece_type == chess.BISHOP: val = 3
                elif captured_piece.piece_type == chess.KNIGHT: val = 3
                else: val = 1
            else: # En passant
                val = 1
            self.captured_value[color] += val

    def uncapture(self, move):
        """ If the move is a capture, subtract the captured piece's value 
        from the game score 
        :param chess.Move move: The move to be checked for captures
        """
        if self.board.is_capture(move):
            color = 0 if self.board.turn == chess.BLACK else 1
            captured_piece = self.board.piece_at(move.to_square)
            if captured_piece:
                if captured_piece.piece_type == chess.KING: val = 100
                elif captured_piece.piece_type == chess.QUEEN: val = 9
                elif captured_piece.piece_type == chess.ROOK: val = 5
                elif captured_piece.piece_type == chess.BISHOP: val = 3
                elif captured_piece.piece_type == chess.KNIGHT: val = 3
                else: val = 1
            else: # En passant
                val = 1
            self.captured_value[color] -= val

    def undo_move(self):
        """ Undoes the last move made and adds it to the undone moves
        stack 
        """
        if self.board.ply() != 0:
            move = self.board.pop()
            self.undone_moves.append(move)
            self.uncapture(move)

    def redo_move(self):
        """ Redoes the last move that was undone """
        if self.undone_moves:
            move = self.undone_moves.pop()
            self.capture(move)
            self.board.push(move)

    def is_promotion(self, from_coord, to_coord):
        """ Returns whether or not the piece can be promted 
        :param tuple(int, int) from_coord: The coordinate of the piece's 
            starting location (both coords must be 0-7 inclusive)        
        :param tuple(int, int) to_coord: The coordinate of the piece's ending
            location (both coords must be 0-7 inclusive)
        :return: The True if the move promotes a pawn
        :rtype: bool
        """
        from_square = chess.square(from_coord[0], from_coord[1])
        piece = self.board.piece_at(from_square)
        if not piece:
            return False
        promo_rank = 7 if piece.color == chess.WHITE else 0
        return piece.piece_type == chess.PAWN and to_coord[1] == promo_rank

    def is_game_over(self):
        """ Returns whether the game is over 
        :return: The True if the game is over
        :rtype: bool
        """
        return bool(self.board.outcome())
