""" File: game.py
This file contains the Game class which controls the logic for the game
"""
from piece import Color, Pawn, Knight, Bishop, Rook, Queen, King


class Game:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.black_king_square = None
        self.white_king_square = None
        self.set_board()
        self.score = {Color.WHITE: 0, Color.BLACK: 0}
        self.move_log = []
        self.turn = Color.WHITE
        self.picked_piece = None
        self.picked_from = None
        self.picked_piece_moves = None

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
        self.black_king_square = (0, 4)
        self.white_king_square = (7, 4)

    def pick_piece(self, square):
        """ Pick up a pieces given the square coordinates 
        square: Tuple containing the rank and file indices
        """
        rank, file = square
        if rank < 8 and file < 8 and self.board[rank][file]:
            self.picked_piece = self.board[rank][file]
            self.board[rank][file] = None
            self.picked_piece_moves = self.picked_piece.get_legal_moves(
                (rank, file), self.board, self.move_log)
            self.picked_from = square

    def put_piece(self, square):
        """ Place a piece at the given coordinates 
        square: Tuple containing the rank and file indices
        """
        rank, file = square
        if self.picked_piece:
            if  rank < 8 and file < 8 and (square in self.picked_piece_moves):
                self.board[rank][file] = self.picked_piece
                self.picked_piece.has_not_moved = False
                self.move_log.append((self.picked_from,square))
                if isinstance(self.picked_piece, King):
                    if self.picked_piece.color == Color.WHITE:
                        self.white_king_square = square
                    else:
                        self.black_king_square = square
                self.look_for_checks()
            else:
                rank_start = self.picked_from[0]
                file_start = self.picked_from[1]
                self.board[rank_start][file_start] = self.picked_piece
            self.picked_piece = None

    def look_for_checks(self):
        """ Checks both kings to see if they are in check """
        for rank, file in (self.white_king_square, 
                           self.black_king_square):
            if self.board[rank][file].is_attacked(
                (rank, file), self.board):
                print(f'{self.board[rank][file].color} King is in check')
