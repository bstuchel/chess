""" File: game.py
This file contains the Game class which controls the logic for the game
"""
import chess


class Game:
    def __init__(self):
        self.board = chess.Board()
