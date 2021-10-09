""" File: ai_game.py
This file contains the AIGame class which adds methods for makeing computer 
moves for singleplayer chess games
"""
import chess
from game import Game
import random

class AIGame(Game):
    def __init__(self):
        super().__init__()

    def user_move(self, move):
        """ Make the move if it is legal, if move works, make AI move
        :param chess.Move move: The move to attempt
        """
        if self.move(move): 
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
        if depth == 0 or self.is_game_over():
            return self.captured_value[1] - self.captured_value[0], None

        if is_white:
            max_eval = -1000
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
            min_eval = 1000
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
