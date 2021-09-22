""" File: gui.py
This file contains the GUI for the chess application
"""
import chess
import pygame


class GUI:
    # Define Colors
    DARK_GRAY = (49, 46, 43)
    GREEN = (118, 150, 86)
    CREAM = (238, 238, 210)
    WHITE = (255, 255, 255)
    LIGHT_GRAY = (241, 241, 241)
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

    # Define sprites
    SPRITES = {}
    for piece_char in "pnbrqk":
        filepath_black = f"res/img/{SQUARE_SIZE}/b{piece_char}.png"
        filepath_white = f"res/img/{SQUARE_SIZE}/w{piece_char}.png"
        SPRITES[piece_char] = pygame.image.load(filepath_black)
        SPRITES[piece_char.upper()] = pygame.image.load(filepath_white)

    def __init__(self, game):
        self.dis = self.create_display()
        self.game_surface = self.create_game_surface()
        self.white_promo_surf = self.white_promo_menu()
        self.black_promo_surf = self.black_promo_menu()
        self.game = game
        self.in_hand = None

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

    def white_promo_menu(self):
        """ Creates the promotion menu surface for the white pieces. """
        white_promo_surface = pygame.Surface((self.SQUARE_SIZE, 
                                             4*self.SQUARE_SIZE))
        white_promo_surface.fill(self.WHITE)
        white_promo_surface.blit(self.SPRITES['Q'], (0, 0))
        white_promo_surface.blit(self.SPRITES['N'], (0, self.SQUARE_SIZE))
        white_promo_surface.blit(self.SPRITES['R'], (0, 2 * self.SQUARE_SIZE))
        white_promo_surface.blit(self.SPRITES['B'], (0, 3 * self.SQUARE_SIZE))
        return white_promo_surface
        
    def black_promo_menu(self):
        """ Creates the promotion menu surface for the black pieces. """
        black_promo_surface = pygame.Surface((self.SQUARE_SIZE, 
                                                4*self.SQUARE_SIZE))
        black_promo_surface.fill(self.WHITE)
        black_promo_surface.blit(self.SPRITES['b'], (0, 0))
        black_promo_surface.blit(self.SPRITES['r'], (0, self.SQUARE_SIZE))
        black_promo_surface.blit(self.SPRITES['n'], (0, 2 * self.SQUARE_SIZE))
        black_promo_surface.blit(self.SPRITES['q'], (0, 3 * self.SQUARE_SIZE))
        return black_promo_surface

    def update_display(self, pos):
        """ Updates the display by clearing the display to the blank board 
        surface.  Pieces are then drawn to the board including pieces held by 
        the user.
        pos: Tuple containing the x and y coordinates of the cursor
        """
        self.dis.blit(self.game_surface, (0, 0))
        # Draw pieces on board
        rank = 7
        file = 0
        in_hand_char = None
        for char in self.game.board.board_fen():
            if char == '/':
                file = 0
                rank -= 1
            elif char.isnumeric():
                file += int(char)
            elif self.in_hand == (file, rank):
                in_hand_char = char
                file += 1
            else:
                x = file * self.SQUARE_SIZE
                y = (7 - rank) * self.SQUARE_SIZE
                self.dis.blit(self.SPRITES[char], (x, y))
                file += 1

        # Draw piece in hand
        if self.in_hand and in_hand_char:
                x, y = pos
                x -= self.SQUARE_SIZE // 2
                y -= self.SQUARE_SIZE // 2
                self.dis.blit(self.SPRITES[in_hand_char], (x, y))

        pygame.display.update()

    def pick_piece(self, pos):
        """ Pick up a pieces given the square coordinates
        pos: Tuple containing the x and y coordinates of the cursor
        """
        file = pos[0] // self.SQUARE_SIZE
        rank = 7 - (pos[1] // self.SQUARE_SIZE)
        self.in_hand = (file, rank)

    def put_piece(self, pos):
        """ Place a piece at the given coordinates 
        pos: Tuple containing the x and y coordinates of the cursor
        """
        file = pos[0] // self.SQUARE_SIZE
        rank = 7 - (pos[1] // self.SQUARE_SIZE)
        if file > -1 and file < 8 and rank > -1 and rank < 8:
            if self.game.is_promotion(self.in_hand, (file, rank)):
                # self.game.move(self.in_hand, (file, rank), chess.QUEEN)
                self.choose_promotion((file, rank))
            else:
                self.game.move(self.in_hand, (file, rank))
        self.in_hand = None

    def choose_promotion(self, square):
        file, rank = square
        if rank == 7:
            self.dis.blit(self.white_promo_surf, (file * self.SQUARE_SIZE, 0))
        else:
            self.dis.blit(self.black_promo_surf, (file * self.SQUARE_SIZE, 4 * self.SQUARE_SIZE))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return