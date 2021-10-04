""" File: ai_game.py
This file contains the AIGame class which adds methods for makeing computer 
moves for singleplayer chess games
"""
from game import Game
import random

class AIGame(Game):
    def __init__(self):
        super().__init__()

    def user_move(self, move):
        """ Make the move if it is legal 
        :param chess.Move move: The move to attempt
        """
        success = self.move(move)
        if success: self.ai_move()

    def ai_move(self):
        # Go through moves with each move having fixed chance of being chosen
        count = self.board.legal_moves.count()
        for move in self.board.legal_moves:
            choice = random.random()
            if choice < 1 / count:
                self.move(move)
                return

        # If nothing is chosen, make the first legal move
        for move in self.board.legal_moves:
            self.move(move)
            return
