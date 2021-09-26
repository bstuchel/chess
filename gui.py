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
    MENU_FONT = pygame.font.SysFont('bahnschrift', SQUARE_SIZE // 3)

    # Define sprites
    SPRITES = {}
    for piece_char in "pnbrqk":
        filepath_black = f"res/img/{SQUARE_SIZE}/b{piece_char}.png"
        filepath_white = f"res/img/{SQUARE_SIZE}/w{piece_char}.png"
        SPRITES[piece_char] = pygame.image.load(filepath_black)
        SPRITES[piece_char.upper()] = pygame.image.load(filepath_white)

    def __init__(self):
        self.dis = self._create_display()
        self.game_surface = self._create_game_surface()
        self.white_promo_surf = self._white_promo_menu()
        self.black_promo_surf = self._black_promo_menu()
        self.game = None
        self.in_hand = None

    def set_game(self, game):
        self.game = game

    def _create_display(self):
        """ Creates the pygame display and sets the caption """
        dis = pygame.display.set_mode((self.WINDOW_WIDTH, self.BOARD_SIZE))
        pygame.display.set_caption('Chess')
        return dis

    def _create_game_surface(self):
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

    def _white_promo_menu(self):
        """ Creates the promotion menu surface for the white pieces. """
        white_promo_surface = pygame.Surface((self.SQUARE_SIZE, 
                                             4*self.SQUARE_SIZE))
        white_promo_surface.fill(self.WHITE)
        white_promo_surface.blit(self.SPRITES['Q'], (0, 0))
        white_promo_surface.blit(self.SPRITES['N'], (0, self.SQUARE_SIZE))
        white_promo_surface.blit(self.SPRITES['R'], (0, 2 * self.SQUARE_SIZE))
        white_promo_surface.blit(self.SPRITES['B'], (0, 3 * self.SQUARE_SIZE))
        return white_promo_surface

    def _black_promo_menu(self):
        """ Creates the promotion menu surface for the black pieces. """
        black_promo_surface = pygame.Surface((self.SQUARE_SIZE, 
                                                4*self.SQUARE_SIZE))
        black_promo_surface.fill(self.WHITE)
        black_promo_surface.blit(self.SPRITES['b'], (0, 0))
        black_promo_surface.blit(self.SPRITES['r'], (0, self.SQUARE_SIZE))
        black_promo_surface.blit(self.SPRITES['n'], (0, 2 * self.SQUARE_SIZE))
        black_promo_surface.blit(self.SPRITES['q'], (0, 3 * self.SQUARE_SIZE))
        return black_promo_surface

    def _get_game_over_menu(self):
        game_over_surface = pygame.Surface((5 * self.SQUARE_SIZE, 
                                            (7 * self.SQUARE_SIZE) // 2))
        game_over_surface.fill(self.DARK_GRAY)
        # pygame.draw.rect(game_over_surface, self.GREEN,
        #                  (self.SQUARE_SIZE // 2, self.SQUARE_SIZE // 2, 
        #                   2 * self.SQUARE_SIZE, self.SQUARE_SIZE))

        outcome = self.game.board.outcome()
        if outcome.winner:
            label = "White Wins!"
        elif outcome.winner == None:
            label = "Draw"
        else:
            label = "Black Wins!"
        termination_label = self.MENU_FONT.render(label, True, self.WHITE)
        width = termination_label.get_width()
        height = termination_label.get_height()
        game_over_surface.blit(termination_label, 
                               [5 * self.SQUARE_SIZE // 2 - width // 2, 
                                self.SQUARE_SIZE // 2 - height // 2])

        termination = outcome.termination.name.title()
        termination_label = self.MENU_FONT.render(termination, True, self.WHITE)
        width = termination_label.get_width()
        height = termination_label.get_height()
        game_over_surface.blit(termination_label, 
                               [5 * self.SQUARE_SIZE // 2 - width // 2, 
                                4 * self.SQUARE_SIZE // 3 - height // 2])

        pygame.draw.rect(game_over_surface, self.GREEN,
                         (self.SQUARE_SIZE, 2 * self.SQUARE_SIZE,
                          3 * self.SQUARE_SIZE, self.SQUARE_SIZE))
        new_game_label = self.MENU_FONT.render("New Game", True, self.WHITE)
        width = new_game_label.get_width()
        height = new_game_label.get_height()
        game_over_surface.blit(new_game_label, 
                               [5 * self.SQUARE_SIZE // 2 - width // 2, 
                                5 * self.SQUARE_SIZE // 2 - height // 2])
        return game_over_surface

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
            promo_piece = None
            if self.game.is_promotion(self.in_hand, (file, rank)):
                promo_piece = self._choose_promotion((file, rank))
            self.game.move(self.in_hand, (file, rank), promo_piece)
        self.in_hand = None

    def _choose_promotion(self, square):
        # Display menu
        file, rank = square
        if rank == 7:
            self.dis.blit(self.white_promo_surf, (file * self.SQUARE_SIZE, 0))
        else:
            self.dis.blit(self.black_promo_surf, (file * self.SQUARE_SIZE, 4 * self.SQUARE_SIZE))
        pygame.display.update()
        # Get response
        while True:
            pygame.time.delay(50)
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                x, y = event.pos
                click_file = x // self.SQUARE_SIZE
                click_rank = 7 - (y // self.SQUARE_SIZE)
                rank_diff = abs(click_rank - rank)
                if click_file == file and rank_diff < 4:
                    if rank_diff == 3: return chess.BISHOP
                    elif rank_diff == 2: return chess.ROOK
                    elif rank_diff == 1: return chess.KNIGHT
                    else: return chess.QUEEN                
                return None

    def display_menu(self):
        self.dis.blit(self._get_game_over_menu(), ((5 * self.SQUARE_SIZE) // 2, 
                                            (9 * self.SQUARE_SIZE) // 4))
        pygame.display.update()
