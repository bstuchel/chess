""" File: piece.py
This file contains the Piece class and subclasses for each piece type
"""
from enum import Enum


class Color(Enum):
    BLACK = 0
    WHITE = 1

    def get_color_tag(self):
        """ return the character tag used to denote the color """
        return self.name[0].lower()


class Piece:
    def __init__(self, color):
        self.color = color
        self.is_captured = False
        self.has_not_moved = True
        self.sprite = None


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.filename = f"{color.get_color_tag()}p.png"
        self.value = 1

    def get_legal_moves(self, square, board, move_log):
        """ Find and return the list of legal moves for a pawn given the 
        location, board and move log 
        
        Arguments:
        square (tuple(int, int)): Coordinates of square on the chess board
        board (list(list)): 8x8 2D list of the board containing piece objects
        move_log (list(tuple(squre, square))): List of moves, where each 
            move is a tuple that contains the starting and ending squares

        Return:
        legal_moves (list(square)): A list of the squares that the piece can 
            move to
        """
        legal_moves = []
        rank, file = square
        sign = 1 if self.color == Color.BLACK else -1

        # Move 2 squares if on starting square
        if (rank + 2*sign < 8 and rank + 2*sign > -1 and 
            self.has_not_moved and 
            not board[rank + sign][file] and 
            not board[rank + 2*sign][file]):
            legal_moves.append((rank + 2*sign, file)) 

        # Move 1 square forward
        if (rank + sign < 8 and rank + sign > -1 and 
            not board[rank + sign][file]):
            legal_moves.append((rank + sign, file)) 

        # Capture king side
        if (rank + sign < 8 and rank + sign > -1 and file < 7 and 
            board[rank + sign][file + 1] and 
            board[rank + sign][file + 1].color != self.color):
            legal_moves.append((rank + sign, file + 1)) 

        # Capture queen side
        if (rank + sign < 8 and rank + sign > -1 and file > 0 and 
            board[rank + sign][file - 1] and 
            board[rank + sign][file - 1].color != self.color):
            legal_moves.append((rank + sign, file - 1)) 

        # En passant
        if move_log:
            start_square, end_square = move_log[-1]
            if (isinstance(board[end_square[0]][end_square[1]], Pawn) and 
                board[end_square[0]][end_square[1]].color != self.color and 
                end_square[0] == rank and 
                abs(end_square[0] - start_square[0]) == 2):
                legal_moves.append((rank + sign, end_square[1]))

        return legal_moves


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.filename = f"{color.get_color_tag()}n.png"
        self.value = 3

    def get_legal_moves(self, square, board, move_log):
        """ Find and return the list of legal moves for a knight given the 
        location, board and move log 
        
        Arguments:
        square (tuple(int, int)): Coordinates of square on the chess board
        board (list(list)): 8x8 2D list of the board containing piece objects
        move_log (list(tuple(squre, square))): List of moves, where each 
            move is a tuple that contains the starting and ending squares

        Return:
        legal_moves (list(square)): A list of the squares that the piece can 
            move to
        """
        legal_moves = []
        rank, file = square
        for delta_rank in [-2, -1, 1, 2]:
            for delta_file in [-2, -1, 1, 2]:
                if abs(delta_file) + abs(delta_rank) != 3:
                    continue
                new_rank = rank + delta_rank
                new_file = file + delta_file
                if ((new_rank > -1 and new_rank < 8 and 
                    new_file > -1 and new_file < 8) and 
                    not (board[new_rank][new_file] and
                    board[new_rank][new_file].color == self.color)):
                    legal_moves.append((new_rank, new_file))
        return legal_moves


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.filename = f"{color.get_color_tag()}b.png"
        self.value = 3

    def get_legal_moves(self, square, board, move_log):
        """ Find and return the list of legal moves for a bishop given the 
        location, board and move log 
        
        Arguments:
        square (tuple(int, int)): Coordinates of square on the chess board
        board (list(list)): 8x8 2D list of the board containing piece objects
        move_log (list(tuple(squre, square))): List of moves, where each 
            move is a tuple that contains the starting and ending squares

        Return:
        legal_moves (list(square)): A list of the squares that the piece can 
            move to
        """
        legal_moves = []
        for delta_rank, delta_file in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            rank, file = square
            while True:
                rank += delta_rank
                file += delta_file
                if rank < 0 or rank > 7 or file < 0 or file > 7:
                    break
                if board[rank][file]: 
                    if board[rank][file].color != self.color:
                        legal_moves.append((rank, file))
                    break
                legal_moves.append((rank, file))
        return legal_moves


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.filename = f"{color.get_color_tag()}r.png"
        self.value = 5

    def get_legal_moves(self, square, board, move_log):
        """ Find and return the list of legal moves for a rook given the 
        location, board and move log 
        
        Arguments:
        square (tuple(int, int)): Coordinates of square on the chess board
        board (list(list)): 8x8 2D list of the board containing piece objects
        move_log (list(tuple(squre, square))): List of moves, where each 
            move is a tuple that contains the starting and ending squares

        Return:
        legal_moves (list(square)): A list of the squares that the piece can 
            move to
        """
        legal_moves = []
        for delta_rank, delta_file in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            rank, file = square
            while True:
                rank += delta_rank
                file += delta_file
                if rank < 0 or rank > 7 or file < 0 or file > 7:
                    break
                if board[rank][file]: 
                    if board[rank][file].color != self.color:
                        legal_moves.append((rank, file))
                    break
                legal_moves.append((rank, file))
        return legal_moves


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.filename = f"{color.get_color_tag()}q.png"
        self.value = 9

    def get_legal_moves(self, square, board, move_log):
        """ Find and return the list of legal moves for a queen given the 
        location, board and move log 
        
        Arguments:
        square (tuple(int, int)): Coordinates of square on the chess board
        board (list(list)): 8x8 2D list of the board containing piece objects
        move_log (list(tuple(squre, square))): List of moves, where each 
            move is a tuple that contains the starting and ending squares

        Return:
        legal_moves (list(square)): A list of the squares that the piece can 
            move to
        """
        legal_moves = []
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
                    if board[rank][file]: 
                        if board[rank][file].color != self.color:
                            legal_moves.append((rank, file))
                        break
                    legal_moves.append((rank, file))
        return legal_moves


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.filename = f"{color.get_color_tag()}k.png"

    def get_legal_moves(self, square, board, move_log):
        """ Find and return the list of legal moves for a king given the 
        location, board and move log 
        
        Arguments:
        square (tuple(int, int)): Coordinates of square on the chess board
        board (list(list)): 8x8 2D list of the board containing piece objects
        move_log (list(tuple(squre, square))): List of moves, where each 
            move is a tuple that contains the starting and ending squares

        Return:
        legal_moves (list(square)): A list of the squares that the piece can 
            move to
        """
        legal_moves = []
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
                if board[new_rank][new_file]: 
                    if board[new_rank][new_file].color != self.color:
                        legal_moves.append((new_rank, new_file))
                    continue
                legal_moves.append((new_rank, new_file))

        # Check castling
        if self.has_not_moved:
            # Check king side
            if not board[rank][5] and not board[rank][6]:
                if board[rank][7] and board[rank][7].has_not_moved:
                    legal_moves.append((rank, 6))
            # Check queen side
            if (not board[rank][1] and not board[rank][2] and 
                not board[rank][3]):
                if board[rank][0] and board[rank][0].has_not_moved:
                    legal_moves.append((rank, 2))
        return legal_moves

    def is_in_check(self, square, board):
        # Check for pawns
        rank, file = square
        sign = 1 if self.color == Color.BLACK else -1

        if (rank + sign < 8 and rank + sign > -1 and file < 7 and 
            board[rank + sign][file + 1] and 
            board[rank + sign][file + 1].color != self.color and
            isinstance(board[rank + sign][file + 1], Pawn)):
            return True

        if (rank + sign < 8 and rank + sign > -1 and file > 0 and 
            board[rank + sign][file - 1] and 
            board[rank + sign][file - 1].color != self.color and
            isinstance(board[rank + sign][file - 1], Pawn)):
            return True
        
        # Check for knights
        for delta_rank in [-2, -1, 1, 2]:
            for delta_file in [-2, -1, 1, 2]:
                if abs(delta_file) + abs(delta_rank) != 3:
                    continue
                new_rank = rank + delta_rank
                new_file = file + delta_file
                if ((new_rank > -1 and new_rank < 8 and 
                    new_file > -1 and new_file < 8) and 
                    board[new_rank][new_file] and
                    board[new_rank][new_file].color != self.color and
                    isinstance(board[new_rank][new_file], Knight)):
                    return True

        # Check for bishops and queens
        for delta_rank, delta_file in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            rank, file = square
            while True:
                rank += delta_rank
                file += delta_file
                if rank < 0 or rank > 7 or file < 0 or file > 7:
                    break
                if board[rank][file]: 
                    if (board[rank][file].color != self.color and 
                        isinstance(board[rank][file], (Bishop, Queen))):
                        return True
                    break

        # Check for rooks and queens
        for delta_rank, delta_file in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            rank, file = square
            while True:
                rank += delta_rank
                file += delta_file
                if rank < 0 or rank > 7 or file < 0 or file > 7:
                    break
                if board[rank][file]: 
                    if (board[rank][file].color != self.color and 
                        isinstance(board[rank][file], (Rook, Queen))):
                        return True
                    break

        # Check for kings
        for delta_rank in range(-1, 2):
            for delta_file in range(-1, 2):
                if delta_rank == 0 and delta_file == 0:
                    continue
                new_rank = rank + delta_rank
                new_file = file + delta_file
                if (new_rank > -1 and new_rank < 8 and 
                    new_file > -1 and new_file < 8 and 
                    board[new_rank][new_file] and 
                    board[rank][file].color != self.color and 
                    isinstance(board[rank][file], King)):
                    return True

        return False