""" File: piece.py
This file contains the Piece class and subclasses for each piece type
"""
from enum import Enum


class Color(Enum):
    BLACK = 0
    WHITE = 1

    def get_color_tag(self):
        return 'b' if self.value == 0 else 'w'


class Piece:
    def __init__(self, color):
        self.color = color
        self.is_captured = False
        self.has_not_moved = True
        self.legal_moves = []
        self.sprite = None


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.filename = f"{color.get_color_tag()}p.png"
        self.value = 1

    def find_legal_moves(self, square, board, move_log):
        self.legal_moves.clear()
        rank, file = square
        sign = 1 if self.color == Color.BLACK else -1

        # Move 2 squares if on starting square
        if (rank + 2*sign < 8 and rank + 2*sign > -1 and 
            self.has_not_moved and 
            not board.board[rank + sign][file] and 
            not board.board[rank + 2*sign][file]):
            self.legal_moves.append((rank + 2*sign, file)) 

        # Move 1 square forward
        if (rank + sign < 8 and rank + sign > -1 and 
            not board.board[rank + sign][file]):
            self.legal_moves.append((rank + sign, file)) 

        # Capture king side
        if (rank + sign < 8 and rank + sign > -1 and file + 1 < 8 and 
            board.board[rank + sign][file + 1] and 
            board.board[rank + sign][file + 1].color != self.color):
            self.legal_moves.append((rank + sign, file + 1)) 

        # Capture queen side
        if (rank + sign < 8 and rank + sign > -1 and file - 1 > -1 and 
            board.board[rank + sign][file - 1] and 
            board.board[rank + sign][file - 1].color != self.color):
            self.legal_moves.append((rank + sign, file - 1)) 

        # En passant
        if move_log:
            start_square, end_square = move_log[-1]
            if (isinstance(board.board[end_square[0]][end_square[1]], Pawn) and 
                board.board[end_square[0]][end_square[1]].color != self.color and 
                end_square[0] == rank and 
                abs(end_square[0] - start_square[0]) == 2):
                self.legal_moves.append((rank + sign, end_square[1]))


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.filename = f"{color.get_color_tag()}n.png"
        self.value = 3

    def find_legal_moves(self, square, board, move_log):
        self.legal_moves.clear()
        rank, file = square
        for delta_rank in [-2, -1, 1, 2]:
            for delta_file in [-2, -1, 1, 2]:
                if abs(delta_file) + abs(delta_rank) != 3:
                    continue
                new_rank = rank + delta_rank
                new_file = file + delta_file
                if ((new_rank > -1 and new_rank < 8 and 
                    new_file > -1 and new_file < 8) and 
                    not (board.board[new_rank][new_file] and
                    board.board[new_rank][new_file].color == self.color)):
                    self.legal_moves.append((new_rank, new_file))


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.filename = f"{color.get_color_tag()}b.png"
        self.value = 3

    def find_legal_moves(self, square, board, move_log):
        self.legal_moves.clear()
        for delta_rank, delta_file in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            rank, file = square
            while True:
                rank += delta_rank
                file += delta_file
                if rank < 0 or rank > 7 or file < 0 or file > 7:
                    break
                if board.board[rank][file]: 
                    if board.board[rank][file].color != self.color:
                        self.legal_moves.append((rank, file))
                    break
                self.legal_moves.append((rank, file))


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.filename = f"{color.get_color_tag()}r.png"
        self.value = 5

    def find_legal_moves(self, square, board, move_log):
        self.legal_moves.clear()
        for delta_rank, delta_file in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            rank, file = square
            while True:
                rank += delta_rank
                file += delta_file
                if rank < 0 or rank > 7 or file < 0 or file > 7:
                    break
                if board.board[rank][file]: 
                    if board.board[rank][file].color != self.color:
                        self.legal_moves.append((rank, file))
                    break
                self.legal_moves.append((rank, file))


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.filename = f"{color.get_color_tag()}q.png"
        self.value = 9

    def find_legal_moves(self, square, board, move_log):
        self.legal_moves.clear()
        for delta_rank in range(-1, 2):
            for delta_file in range(-1, 2):
                if delta_rank == 0 and delta_file == 0:
                    continue
                rank, file = square
                while True:
                    rank += delta_rank
                    file += delta_file
                    if rank < 0 or rank > 7 or file < 0 or file > 7:
                        break
                    if board.board[rank][file]: 
                        if board.board[rank][file].color != self.color:
                            self.legal_moves.append((rank, file))
                        break
                    self.legal_moves.append((rank, file))


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.filename = f"{color.get_color_tag()}k.png"

    def find_legal_moves(self, square, board, move_log):
        self.legal_moves.clear()
        rank, file = square
        for delta_rank in range(-1, 2):
            for delta_file in range(-1, 2):
                if delta_rank == 0 and delta_file == 0:
                    continue
                new_rank = rank + delta_rank
                new_file = file + delta_file
                if (new_rank < 0 or new_rank > 7 or 
                    new_file < 0 or new_file > 7):
                    continue
                if board.board[new_rank][new_file]: 
                    if board.board[new_rank][new_file].color != self.color:
                        self.legal_moves.append((new_rank, new_file))
                    continue
                self.legal_moves.append((new_rank, new_file))

        # Check castling
        if self.has_not_moved:
            # Check king side
            if not board.board[rank][5] and not board.board[rank][6]:
                if board.board[rank][7] and board.board[rank][7].has_not_moved:
                    self.legal_moves.append((rank, 6))
            # Check queen side
            if (not board.board[rank][1] and not board.board[rank][2] and 
                not board.board[rank][3]):
                if board.board[rank][0] and board.board[rank][0].has_not_moved:
                    self.legal_moves.append((rank, 2))