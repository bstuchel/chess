""" File: ai_game.py
This file contains the AIGame class which adds methods for makeing computer 
moves for singleplayer chess games
"""
from game import Game


class AIGame(Game):
    def __init__(self):
        super().__init__()
