""" File: gui.py
This file contains the GUI for the chess application
"""
import pygame


class GUI:
    # Define Colors
    DARK_GRAY = (49, 46, 43)
    GREEN = (118, 150, 86)
    CREAM = (238, 238, 210)
    SQUARE_COLORS = (CREAM, GREEN)

    # Define Geometry
    WINDOW_WIDTH = 860
    MARGIN_PORTION = 0.2
    SQUARE_SIZE = int((WINDOW_WIDTH * (1 - MARGIN_PORTION) // 8) // 5 * 5)
    if SQUARE_SIZE > 100:
        SQUARE_SIZE = 100
    BOARD_SIZE = 8 * SQUARE_SIZE
    MARGIN_WIDTH = WINDOW_WIDTH - BOARD_SIZE

    # Define fonts
    LABEL_FONT = pygame.font.SysFont('bahnschrift', SQUARE_SIZE // 4)
    SCORE_FONT = pygame.font.SysFont('bahnschrift', 30)

    def __init__(self, game):
        self.dis = self.create_display()
        self.game_surface = self.create_game_surface()
        self.game = game
        self.set_sprites()

    def set_game(self, game):
        self.game = game

    def create_display(self):
        """ Creates the pygame display and sets the caption """
        dis = pygame.display.set_mode((self.WINDOW_WIDTH, self.BOARD_SIZE))
        pygame.display.set_caption('Chess')
        return dis

    def create_game_surface(self):
        """ Creates the game surface to be used for the in-game interface.  
        It contains the chess board, scoreboard and the options menu.
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
        x_location = self.SQUARE_SIZE * 5 / 6
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

    def update_display(self, pos):
        """ Updates the display by clearing the display to the blank board 
        surface.  Pieces are then drawn to the board including pieces held by 
        the user.
        pos: Tuple containing the x and y coordinates of the cursor
        """
        self.dis.blit(self.game_surface, (0, 0))

        # Draw pieces on board
        for i in range(8):
            for j in range(8):
                if self.game.board.board[i][j]:
                    self.dis.blit(self.game.board.board[i][j].sprite, 
                            (j * self.SQUARE_SIZE, i * self.SQUARE_SIZE))

        # Draw piece in hand
        if self.game.picked_piece:
            x, y = pos
            x -= self.SQUARE_SIZE // 2
            y -= self.SQUARE_SIZE // 2
            self.dis.blit(self.game.picked_piece.sprite, (x, y))

        pygame.display.update()

    def set_sprites(self):
        """ Sets the sprites for each piece on the board """
        for rank in self.game.board.board:
            for square in rank:
                if square:
                    filepath = f"res/img/{self.SQUARE_SIZE}/{square.filename}"
                    square.sprite = pygame.image.load(filepath)

    def pick_piece(self, pos):
        """ Pick up a pieces given the square coordinates """
        rank = pos[1] // self.SQUARE_SIZE
        file = pos[0] // self.SQUARE_SIZE
        if file < 8 and rank < 8:
            self.game.pick_piece((rank, file))

    def put_piece(self, pos):
        """ Place a piece at the given coordinates """
        rank = pos[1] // self.SQUARE_SIZE
        file = pos[0] // self.SQUARE_SIZE
        if file < 8 and rank < 8:
            self.game.put_piece((rank, file))