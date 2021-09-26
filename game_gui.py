""" File: gui.py
This file contains the GUI for the chess application
"""
import chess
import pygame


class GameGUI:
    # Define Colors
    DARK_GRAY = (49, 46, 43)
    GREEN = (118, 150, 86)
    LIGHT_GREEN = (168, 200, 136)
    CREAM = (238, 238, 210)
    WHITE = (255, 255, 255)
    LIGHT_GRAY = (241, 241, 241)
    SQUARE_COLORS = (CREAM, GREEN)

    # Define Geometry
    BOARD_PORTION = 0.8

    def __init__(self, dis, game):
        dis.fill(self.DARK_GRAY)
        self.dis = dis
        self._define_geometry()
        self._define_fonts()
        self.SPRITES = self._get_sprites()
        self.game_surface = self._create_game_surface()
        self.white_promo_surf = self._white_promo_menu()
        self.black_promo_surf = self._black_promo_menu()
        self.game = game
        self.in_hand = None

    def _define_geometry(self):
        """ Define geometry used in the game GUI """
        # Window Data
        self.WIDTH, self.HEIGHT = self.dis.get_size()

        # Board Data
        self.TRIAL_W = int((self.WIDTH * self.BOARD_PORTION // 8) // 5 * 5)
        self.TRIAL_H = int((self.HEIGHT // 8) // 5 * 5)
        self.SQUARE_SIZE = self.TRIAL_H 
        if self.TRIAL_W < self.TRIAL_H: self.SQUARE_SIZE = self.TRIAL_W
        if self.SQUARE_SIZE > 100: self.SQUARE_SIZE = 100
        self.BOARD_SIZE = 8 * self.SQUARE_SIZE
        self.MARGIN_WIDTH = self.WIDTH - self.BOARD_SIZE
        self.FILE_LABEL_Y = self.BOARD_SIZE - (self.SQUARE_SIZE // 3)
        self.RANK_LABEL_X = self.SQUARE_SIZE // 14

        # Results Menu
        self.RESULT_MENU_X = (3 * self.SQUARE_SIZE) // 2
        self.RESULT_MENU_Y = (9 * self.SQUARE_SIZE) // 4
        self.RESULT_MENU_WIDTH = 5 * self.SQUARE_SIZE
        self.RESULT_MENU_HEIGHT = (7 * self.SQUARE_SIZE) // 2
        self.WINNER_LABEL_Y = self.SQUARE_SIZE // 2
        self.TERM_LABEL_Y = 4 * self.SQUARE_SIZE // 3
        self.BUTTON_X = self.SQUARE_SIZE
        self.BUTTON_Y = 2 * self.SQUARE_SIZE
        self.BUTTON_WIDTH = 3 * self.SQUARE_SIZE
        self.BUTTON_HEIGHT = self.SQUARE_SIZE
        self.BUTTON_LABEL_Y = 5 * self.SQUARE_SIZE // 2
        self.BUTTON_X_ABS = self.RESULT_MENU_X + self.BUTTON_X
        self.BUTTON_Y_ABS = self.RESULT_MENU_Y + self.BUTTON_Y

    def _define_fonts(self):
        """ Define the fonts used in the game GUI """
        self.LABEL_FONT = pygame.font.SysFont('bahnschrift', 
                                              self.SQUARE_SIZE // 4)
        self.SCORE_FONT = pygame.font.SysFont('bahnschrift', 30)
        self.RESULTS_FONT = pygame.font.SysFont('bahnschrift', 
                                              self.SQUARE_SIZE // 3)

    def _get_sprites(self):
        """ Define the sprites for each chess piece """
        SPRITES = {}
        for piece_char in "pnbrqk":
            filepath_black = f"res/img/{self.SQUARE_SIZE}/b{piece_char}.png"
            filepath_white = f"res/img/{self.SQUARE_SIZE}/w{piece_char}.png"
            SPRITES[piece_char] = pygame.image.load(filepath_black)
            SPRITES[piece_char.upper()] = pygame.image.load(filepath_white)
        return SPRITES

    def _create_game_surface(self):
        """ Creates the game surface to be used for the in-game interface.  
        It contains the chess board, scoreboard and the options menu.
        """
        # Chess Board
        game_surface = pygame.Surface((self.WIDTH, self.BOARD_SIZE))
        game_surface.fill(self.DARK_GRAY)
        for x in range(0, 8):
            for y in range(0, 8):
                pygame.draw.rect(game_surface, self.SQUARE_COLORS[(x+y) % 2],
                                (x * self.SQUARE_SIZE, y * self.SQUARE_SIZE, 
                                 self.SQUARE_SIZE, self.SQUARE_SIZE))
        # File labels (a-h)
        file_location_x = self.SQUARE_SIZE * 5 / 6
        labels = 'abcdefgh'
        for i in range(len(labels)):
            label = self.LABEL_FONT.render(labels[i], True, 
                                           self.SQUARE_COLORS[i % 2])
            game_surface.blit(label, [file_location_x, self.FILE_LABEL_Y])
            file_location_x += self.SQUARE_SIZE
        # Rank labels (1-8)
        y_location = 7 * self.SQUARE_SIZE  # Starts labeling at the bottom
        for i in range(8):
            label = self.LABEL_FONT.render(str(i + 1), True, 
                                           self.SQUARE_COLORS[i % 2])
            game_surface.blit(label, [self.RANK_LABEL_X, y_location])
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

    def _get_results_menu(self, button_hover=False):
        """ Create and return the results menu surface """
        results_surface = pygame.Surface((self.RESULT_MENU_WIDTH, 
                                          self.RESULT_MENU_HEIGHT))
        results_surface.fill(self.DARK_GRAY)
        outcome = self.game.board.outcome()

        # Winner Label
        if outcome.winner:
            label = "White Wins!"
        elif outcome.winner == None:
            label = "Draw"
        else:
            label = "Black Wins!"
        winner_label = self.RESULTS_FONT.render(label, True, self.WHITE)
        width = winner_label.get_width()
        height = winner_label.get_height()
        results_surface.blit(winner_label, 
                               [self.RESULT_MENU_WIDTH // 2 - width // 2, 
                                self.WINNER_LABEL_Y - height // 2])

        # Temination Label
        termination = outcome.termination.name.title()
        term_label = self.RESULTS_FONT.render(termination, True, self.WHITE)
        width = term_label.get_width()
        height = term_label.get_height()
        results_surface.blit(term_label, 
                               [self.RESULT_MENU_WIDTH // 2 - width // 2, 
                                self.TERM_LABEL_Y - height // 2])

        # New Game Button
        color = self.LIGHT_GREEN if button_hover else self.GREEN
        pygame.draw.rect(results_surface, color,
                         (self.BUTTON_X, self.BUTTON_Y,
                          self.BUTTON_WIDTH, self.BUTTON_HEIGHT))
        new_game_label = self.RESULTS_FONT.render("New Game", True, self.WHITE)
        width = new_game_label.get_width()
        height = new_game_label.get_height()
        results_surface.blit(new_game_label, 
                               [self.RESULT_MENU_WIDTH // 2 - width // 2, 
                                self.BUTTON_LABEL_Y - height // 2])
        return results_surface

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
        if self.in_hand:
            self.in_hand == None
        else:
            file = pos[0] // self.SQUARE_SIZE
            rank = 7 - (pos[1] // self.SQUARE_SIZE)
            if file > -1 and file < 8 and rank > -1 and rank < 8:
                self.in_hand = (file, rank)

    def put_piece(self, pos):
        """ Place a piece at the given coordinates 
        pos: Tuple containing the x and y coordinates of the cursor
        """
        if self.in_hand == None:
            return
        file = pos[0] // self.SQUARE_SIZE
        rank = 7 - (pos[1] // self.SQUARE_SIZE)
        if file > -1 and file < 8 and rank > -1 and rank < 8:
            promo_piece = None
            if self.game.is_promotion(self.in_hand, (file, rank)):
                promo_piece = self._choose_promotion((file, rank))
            self.game.move(self.in_hand, (file, rank), promo_piece)
        self.in_hand = None

    def _choose_promotion(self, square):
        """ Displays the promotion menu and returns the users choice """
        # Display menu
        file, rank = square
        if rank == 7:
            self.dis.blit(self.white_promo_surf, (file * self.SQUARE_SIZE, 0))
        else:
            self.dis.blit(self.black_promo_surf, (file * self.SQUARE_SIZE, 
                                                  4 * self.SQUARE_SIZE))
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

    def display_menu(self, pos):
        """ Displays the results menu """
        x, y = pos
        if (x > self.BUTTON_X_ABS and 
            x < self.BUTTON_X_ABS + self.BUTTON_WIDTH and 
            y > self.BUTTON_Y_ABS and 
            y < self.BUTTON_Y_ABS + self.BUTTON_HEIGHT):
            self.dis.blit(self._get_results_menu(button_hover=True), 
                          (self.RESULT_MENU_X, self.RESULT_MENU_Y))
        else:
            self.dis.blit(self._get_results_menu(), (self.RESULT_MENU_X, 
                                                     self.RESULT_MENU_Y))
        pygame.display.update()

    def menu_click(self, pos):
        """ Returns the value 1 if the button is clicked """
        x, y = pos
        if (x > self.BUTTON_X_ABS and 
            x < self.BUTTON_X_ABS + self.BUTTON_WIDTH and 
            y > self.BUTTON_Y_ABS and 
            y < self.BUTTON_Y_ABS + self.BUTTON_HEIGHT):
            return 1
