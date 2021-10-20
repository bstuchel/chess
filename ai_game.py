""" File: ai_game.py
This file contains the AIGame class which adds methods for makeing computer 
moves for singleplayer chess games
"""
import chess
from game import Game
import mysql.connector
import random

class AIGame(Game):
    def __init__(self):
        super().__init__()
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="briansql",
            database="chess_openings"
        )
        self.cursor = self.db.cursor(buffered=True)

    def user_move(self, move):
        """ Make the move if it is legal, if move works, make AI move
        :param chess.Move move: The move to attempt
        """
        if self.move(move): 
            if self.is_game_over():
                return
            if self.board.fullmove_number < 10:
                ai_move = self.get_opening_move()
            else:
                _, ai_move = self.minimax(4, -1000, 1000, self.board.turn==chess.WHITE)
            self.move(ai_move)

    def random_move(self):
        """ Get and return a random legal mvoe """
        count = self.board.legal_moves.count()
        if count == 0:
            return
        move_idx = random.choice(range(count))
        idx = 0
        for move in self.board.legal_moves:
            if move_idx == idx:
                return move
            idx += 1

    def minimax(self, depth, alpha, beta, is_white):
        """ Recursively find and return the best move for the turn color 
        given position and depth using minimax with alpha beta pruning.  The 
        evaluation is just the value of white captured pieces minus the value 
        of black captured pieces.
        :param int depth: Depth to searth moves to
        :param int alpha: Min value for alpha pruning
        :param int beta: Max value for beta pruning
        :param bool is_white: True when it's white's turn to move
        :return: Maximum evaluation and the best move to make
        :rtype: Tuple(int, chess.Move)
        """
        if depth == 0:
            return self.captured_value[1] - self.captured_value[0], None
        elif self.is_game_over():
            if is_white: return -1000, None
            else: return 1000, None

        if is_white:
            max_eval = -10000
            max_move = None
            for move in self.board.legal_moves:
                self.move(move)
                cur_eval, _ = self.minimax(depth - 1, alpha, beta, False)
                self.undo_move()
                if cur_eval > max_eval:
                    max_eval = cur_eval
                    max_move = move
                    alpha = cur_eval
                if beta <= alpha:
                    break
            return max_eval, max_move

        else:
            min_eval = 10000
            min_move = None
            for move in self.board.legal_moves:
                self.move(move)
                cur_eval, _ = self.minimax(depth - 1, alpha, beta, True)
                self.undo_move()
                if cur_eval < min_eval:
                    min_eval = cur_eval
                    min_move = move
                    beta = cur_eval
                if beta <= alpha:
                    break
            return min_eval, min_move

    def get_opening_move(self):
        """ Get the most played move for a given position from the opening 
        database 
        """
        selection_call = f"SELECT name, COUNT(name) AS `value_occurrence` \
                           FROM chess_openings.moves \
                           WHERE fen = '{self.board.board_fen()}' \
                           GROUP BY name \
                           ORDER BY `value_occurrence` DESC \
                           LIMIT 1;"
        self.cursor.execute(selection_call)
        selection = self.cursor.fetchall()
        if selection:
            move_uci = selection[0][0]
            return chess.Move.from_uci(move_uci)
        else:
            _, ai_move = self.minimax(4, -1000, 1000, self.board.turn==chess.WHITE)
            return ai_move
