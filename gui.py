""" File: gui.py
This file contains the GUI for the chess application
"""

import pygame
pygame.init()


class GUI():
    # Define Colors
    TAN = (250, 224, 185)
    GRAY = (160, 160, 160)
    BROWN = (112, 90, 62)
    WHITE = (255, 255, 255)
    DARK_GRAY = (49, 46, 43)
    GREEN = (118, 150, 86)
    CREAM = (238, 238, 210)
    SQUARE_COLORS = (CREAM, GREEN)

    # Define Geometry
    WINDOW_WIDTH = 832
    MARGIN_PORTION = 0.2
    SQUARE_SIZE = int(WINDOW_WIDTH * (1 - MARGIN_PORTION) // 8)
    BOARD_SIZE = 8 * SQUARE_SIZE
    MARGIN_WIDTH = WINDOW_WIDTH - BOARD_SIZE

    # Define fonts
    LABEL_FONT = pygame.font.SysFont('bahnschrift', SQUARE_SIZE // 4)
    SCORE_FONT = pygame.font.SysFont('bahnschrift', 30)

    def __init__(self):
        self.dis = self.create_display()
        self.game_surface = self.create_game_surface()

    def create_display(self):
        dis = pygame.display.set_mode((self.WINDOW_WIDTH, self.BOARD_SIZE))
        dis.fill(self.DARK_GRAY)
        pygame.display.set_caption('Chess')
        return dis

    def create_game_surface(self):
        """ This function creates the game surface to be used for the in-game 
        interface.  It contains both the chess board, scoreboard and the 
        options menu.
        """
        # Chess Board
        game_surface = pygame.Surface((self.WINDOW_WIDTH, self.BOARD_SIZE))
        game_surface.fill(self.DARK_GRAY)
        for x in range(0, 8):
            for y in range(0, 8):
                pygame.draw.rect(game_surface, self.SQUARE_COLORS[(x+y) % 2],
                                (x * self.SQUARE_SIZE, y * self.SQUARE_SIZE, 
                                 self.SQUARE_SIZE, self.SQUARE_SIZE))

        # File labels (a-h)
        x_location = self.SQUARE_SIZE * 3 / 4
        y_location = self.BOARD_SIZE - (self.SQUARE_SIZE / 3)
        labels = 'abcdefgh'
        for i in range(len(labels)):
            label = self.LABEL_FONT.render(labels[i], True, 
                                           self.SQUARE_COLORS[i % 2])
            game_surface.blit(label, [x_location, y_location])
            x_location += self.SQUARE_SIZE

        # Rank labels (1-8)
        x_location = self.SQUARE_SIZE // 14
        y_location = 7 * self.SQUARE_SIZE  # Starts labeling at the bottom
        for i in range(8):
            label = self.LABEL_FONT.render(str(i + 1), True, 
                                           self.SQUARE_COLORS[i % 2])
            game_surface.blit(label, [x_location, y_location])
            y_location -= self.SQUARE_SIZE
        return game_surface

    def update_display(self):
        """ This funcetion updated the display by writing the game_surface 
        over it. 
        """
        self.dis.blit(self.game_surface, (0, 0))
        pygame.display.update()
    