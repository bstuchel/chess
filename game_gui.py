""" File: game_gui.py
This file contains the GUI for the chess game
"""
import chess
from gui import GUI
import pygame


class GameGUI(GUI):
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
        self.board_flipped = False

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
        self.FILE_LABEL_Y = self.BOARD_SIZE - (self.SQUARE_SIZE // 3)
        self.RANK_LABEL_X = self.SQUARE_SIZE // 14

        # Results Menu
        self.RM_X = (3 * self.SQUARE_SIZE) // 2
        self.RM_Y = (9 * self.SQUARE_SIZE) // 4
        self.RM_WIDTH = 5 * self.SQUARE_SIZE
        self.RM_HEIGHT = (7 * self.SQUARE_SIZE) // 2
        self.WINNER_LABEL_Y = self.SQUARE_SIZE // 2
        self.TERM_LABEL_Y = 4 * self.SQUARE_SIZE // 3
        # New Game Button
        self.RM_NG_X = self.SQUARE_SIZE
        self.RM_NG_Y = 2 * self.SQUARE_SIZE
        self.RM_NG_WIDTH = 3 * self.SQUARE_SIZE
        self.RM_NG_HEIGHT = self.SQUARE_SIZE
        self.RM_NG_LABEL_Y = 5 * self.SQUARE_SIZE // 2
        self.RM_NG_X_ABS = self.RM_X + self.RM_NG_X
        self.RM_NG_Y_ABS = self.RM_Y + self.RM_NG_Y

        # Sidebar
        self.SB_WIDTH = self.WIDTH - self.BOARD_SIZE
        self.SB_MARGIN = self.SB_WIDTH//15 if self.SB_WIDTH//15 < 10 else 10
        self.SB_BTN_WIDTH = self.SB_WIDTH - 2 * self.SB_MARGIN
        self.SB_BTN_HEIGHT = self.BOARD_SIZE // 15
        # Score
        self.SB_SC_HEAD_FONT = self.SB_WIDTH//8 if self.SB_WIDTH//8 < 30 else 30
        self.SB_SC_LABEL_FONT = self.SB_WIDTH//10 if self.SB_WIDTH//10 < 22 else 22
        self.SB_SC_HEAD_Y = self.BOARD_SIZE // 3
        self.SB_SC_LABEL_Y = (self.SB_SC_HEAD_Y + self.SB_SC_HEAD_FONT + 
                              self.SB_MARGIN)
        self.SB_SC_LABEL_W_X = self.SB_WIDTH // 4
        self.SB_SC_LABEL_B_X = 3 * self.SB_WIDTH // 4
        self.SB_SC_SCORE_Y = (self.SB_SC_LABEL_Y + self.SB_SC_LABEL_FONT + 
                              self.SB_MARGIN)
        self.SB_SC_SCORE_W_X = self.SB_WIDTH // 4
        self.SB_SC_SCORE_B_X = 3 * self.SB_WIDTH // 4
        # Flip Board Button
        self.SB_FB_X = self.SB_MARGIN
        self.SB_FB_Y = self.SB_MARGIN
        self.SB_FB_X_ABS = self.BOARD_SIZE + self.SB_FB_X
        self.SB_FB_Y_ABS = self.SB_FB_Y
        # Undo Button
        self.SB_UD_WIDTH = self.SB_BTN_WIDTH // 2 - self.SB_MARGIN // 2
        self.SB_UD_X = self.SB_MARGIN
        self.SB_UD_Y = 2 * self.SB_MARGIN + self.SB_BTN_HEIGHT
        self.SB_UD_X_ABS = self.BOARD_SIZE + self.SB_UD_X
        self.SB_UD_Y_ABS = self.SB_UD_Y        
        # Redo Button
        self.SB_RD_WIDTH = self.SB_BTN_WIDTH // 2 - self.SB_MARGIN // 2
        self.SB_RD_X = 2 * self.SB_MARGIN + self.SB_UD_WIDTH
        self.SB_RD_Y = 2 * self.SB_MARGIN + self.SB_BTN_HEIGHT
        self.SB_RD_X_ABS = self.BOARD_SIZE + self.SB_RD_X
        self.SB_RD_Y_ABS = self.SB_RD_Y
        # Main Menu Button
        self.SB_MM_X = self.SB_MARGIN
        self.SB_MM_Y = self.BOARD_SIZE - 2*(self.SB_MARGIN+self.SB_BTN_HEIGHT)
        self.SB_MM_X_ABS = self.BOARD_SIZE + self.SB_MM_X
        self.SB_MM_Y_ABS = self.SB_MM_Y
        # New Game Button
        self.SB_NG_X = self.SB_MARGIN
        self.SB_NG_Y = self.BOARD_SIZE - self.SB_MARGIN - self.SB_BTN_HEIGHT
        self.SB_NG_X_ABS = self.BOARD_SIZE + self.SB_NG_X
        self.SB_NG_Y_ABS = self.SB_NG_Y

    def _define_fonts(self):
        """ Define the fonts used in the game GUI """
        self.LABEL_FONT = pygame.font.SysFont('bahnschrift', 
                                              self.SQUARE_SIZE // 4)
        self.RESULTS_FONT = pygame.font.SysFont('bahnschrift', 
                                              self.SQUARE_SIZE // 3)
        self.SB_FONT_BTN = pygame.font.SysFont('bahnschrift', 
                                              self.SB_BTN_HEIGHT // 2)
        self.SB_FONT_HEADING = pygame.font.SysFont('bahnschrift', 
                                              self.SB_SC_HEAD_FONT)
        self.SB_FONT_SCORE = pygame.font.SysFont('bahnschrift', 
                                              self.SB_SC_LABEL_FONT)

    def _get_sprites(self):
        """ Define the sprites for each chess piece 
        :return: The dictionary containing the sprites for each piece
        :rtype: dict{str: pygame.Surface} 
        """
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
        :return: The game surface
        :rtype: pygame.Surface
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
        """ Creates the promotion menu surface for the white pieces. 
        :return: The promotion menu for white
        :rtype: pygame.Surface
        """
        white_promo_surface = pygame.Surface((self.SQUARE_SIZE, 
                                             4*self.SQUARE_SIZE))
        white_promo_surface.fill(self.WHITE)
        white_promo_surface.blit(self.SPRITES['Q'], (0, 0))
        white_promo_surface.blit(self.SPRITES['N'], (0, self.SQUARE_SIZE))
        white_promo_surface.blit(self.SPRITES['R'], (0, 2 * self.SQUARE_SIZE))
        white_promo_surface.blit(self.SPRITES['B'], (0, 3 * self.SQUARE_SIZE))
        return white_promo_surface

    def _black_promo_menu(self):
        """ Creates the promotion menu surface for the black pieces. 
        :return: The promotion menu for black
        :rtype: pygame.Surface
        """
        black_promo_surface = pygame.Surface((self.SQUARE_SIZE, 
                                                4*self.SQUARE_SIZE))
        black_promo_surface.fill(self.WHITE)
        black_promo_surface.blit(self.SPRITES['b'], (0, 0))
        black_promo_surface.blit(self.SPRITES['r'], (0, self.SQUARE_SIZE))
        black_promo_surface.blit(self.SPRITES['n'], (0, 2 * self.SQUARE_SIZE))
        black_promo_surface.blit(self.SPRITES['q'], (0, 3 * self.SQUARE_SIZE))
        return black_promo_surface

    def _get_results_menu(self, btn_hover=False):
        """ Create and return the results menu surface 
        :param bool mm_hover: True if hovering over the button
        :return: The result menu surface
        :rtype: pygame.Surface
        """
        results_surface = pygame.Surface((self.RM_WIDTH, 
                                          self.RM_HEIGHT))
        results_surface.fill(self.DARK_GRAY)
        outcome = self.game.board.outcome()

        # Winner Label
        if outcome.winner:
            msg = "White Wins!"
        elif outcome.winner == None:
            msg = "Draw"
        else:
            msg = "Black Wins!"
        self.draw_label(self.RM_WIDTH // 2, self.WINNER_LABEL_Y, 
                        self.RESULTS_FONT, self.WHITE, msg, results_surface)

        # Temination Label
        self.draw_label(self.RM_WIDTH // 2, self.TERM_LABEL_Y, 
                        self.RESULTS_FONT, self.WHITE, 
                        outcome.termination.name.title(), results_surface)

        # New Game BTN
        self.draw_button(self.RM_NG_X, self.RM_NG_Y, self.RM_NG_WIDTH, 
                         self.RM_NG_HEIGHT, self.LIGHT_GREEN, self.GREEN, 
                         self.RESULTS_FONT, self.WHITE, "New Game", 
                         results_surface, btn_hover)

        return results_surface

    def _get_SB(self, fb_hover=False, ud_hover=False, rd_hover=False, 
                mm_hover=False, ng_hover=False):
        """ Creates and returns the sidebar surface 
        :param bool fb_hover: True if hovering over the flib board button
        :param bool ud_hover: True if hovering over the undo button
        :param bool rd_hover: True if hovering over the redo button
        :param bool mm_hover: True if hovering over the main menu button
        :param bool ng_hover: True if hovering over the new game button
        :return: The sidebar surface
        :rtype: pygame.Surface
        """
        SB_surf = pygame.Surface((self.SB_WIDTH, self.BOARD_SIZE))
        SB_surf.fill(self.DARK_GRAY)

        # Flip Board Button
        self.draw_button(self.SB_FB_X, self.SB_FB_Y, self.SB_BTN_WIDTH, 
                         self.SB_BTN_HEIGHT, self.LIGHT_GREEN, self.GREEN,
                         self.SB_FONT_BTN, self.WHITE, "Flip Board", SB_surf,
                         fb_hover)

        # Undo Button
        self.draw_button(self.SB_UD_X, self.SB_UD_Y, self.SB_UD_WIDTH, 
                         self.SB_BTN_HEIGHT, self.LIGHT_GREEN, self.GREEN,
                         self.SB_FONT_BTN, self.WHITE, "Undo", SB_surf,
                         ud_hover)

        # Redo Button
        self.draw_button(self.SB_RD_X, self.SB_RD_Y, self.SB_RD_WIDTH, 
                         self.SB_BTN_HEIGHT, self.LIGHT_GREEN, self.GREEN,
                         self.SB_FONT_BTN, self.WHITE, "Redo", SB_surf,
                         rd_hover)

        # Main Menu Button
        self.draw_button(self.SB_MM_X, self.SB_MM_Y, self.SB_BTN_WIDTH, 
                         self.SB_BTN_HEIGHT, self.LIGHT_GREEN, self.GREEN,
                         self.SB_FONT_BTN, self.WHITE, "Main Menu", SB_surf,
                         mm_hover)

        # New Game Button
        self.draw_button(self.SB_NG_X, self.SB_NG_Y, self.SB_BTN_WIDTH, 
                         self.SB_BTN_HEIGHT, self.LIGHT_GREEN, self.GREEN,
                         self.SB_FONT_BTN, self.WHITE, "New Game", SB_surf,
                         ng_hover)

        # Game Score
        self.draw_label(self.SB_WIDTH // 2, self.SB_SC_HEAD_Y, 
                        self.SB_FONT_HEADING, self.WHITE, "Captured Value", 
                        SB_surf)

        self.draw_label(self.SB_SC_LABEL_W_X, self.SB_SC_LABEL_Y, 
                        self.SB_FONT_SCORE, self.WHITE, "White", SB_surf)

        self.draw_label(self.SB_SC_LABEL_B_X, self.SB_SC_LABEL_Y, 
                        self.SB_FONT_SCORE, self.WHITE, "Black", SB_surf)

        self.draw_label(self.SB_SC_SCORE_W_X, self.SB_SC_SCORE_Y, 
                        self.SB_FONT_SCORE, self.WHITE, 
                        str(self.game.captured_value[1]), SB_surf)

        self.draw_label(self.SB_SC_SCORE_B_X, self.SB_SC_SCORE_Y, 
                        self.SB_FONT_SCORE, self.WHITE, 
                        str(self.game.captured_value[0]), SB_surf)

        return SB_surf

    def update_display(self, pos):
        """ Updates the display by clearing the display to the blank board 
        surface.  Pieces are then drawn to the board including pieces held by
        the user.
        :param tuple(int, int) pos: Tuple containing the x and y coordinates 
            of the cursor
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
                if self.board_flipped:
                    x = (7 - file) * self.SQUARE_SIZE
                    y = rank * self.SQUARE_SIZE
                self.dis.blit(self.SPRITES[char], (x, y))
                file += 1

        # Draw piece in hand
        if self.in_hand and in_hand_char:
                x, y = pos
                x -= self.SQUARE_SIZE // 2
                y -= self.SQUARE_SIZE // 2
                self.dis.blit(self.SPRITES[in_hand_char], (x, y))

        # Update sidebar
        x, y = pos
        if (x > self.SB_FB_X_ABS and 
            x < self.SB_FB_X_ABS + self.SB_BTN_WIDTH and 
            y > self.SB_FB_Y_ABS and 
            y < self.SB_FB_Y_ABS + self.SB_BTN_HEIGHT):
            self.dis.blit(self._get_SB(fb_hover=True), 
                          (self.BOARD_SIZE, 0))
        elif (x > self.SB_UD_X_ABS and 
            x < self.SB_UD_X_ABS + self.SB_UD_WIDTH and 
            y > self.SB_UD_Y_ABS and 
            y < self.SB_UD_Y_ABS + self.SB_BTN_HEIGHT):
            self.dis.blit(self._get_SB(ud_hover=True), 
                          (self.BOARD_SIZE, 0))
        elif (x > self.SB_RD_X_ABS and 
            x < self.SB_RD_X_ABS + self.SB_RD_WIDTH and 
            y > self.SB_RD_Y_ABS and 
            y < self.SB_RD_Y_ABS + self.SB_BTN_HEIGHT):
            self.dis.blit(self._get_SB(rd_hover=True), 
                          (self.BOARD_SIZE, 0))
        elif (x > self.SB_MM_X_ABS and 
            x < self.SB_MM_X_ABS + self.SB_BTN_WIDTH and 
            y > self.SB_MM_Y_ABS and 
            y < self.SB_MM_Y_ABS + self.SB_BTN_HEIGHT):
            self.dis.blit(self._get_SB(mm_hover=True), 
                          (self.BOARD_SIZE, 0))
        elif (x > self.SB_NG_X_ABS and 
            x < self.SB_NG_X_ABS + self.SB_BTN_WIDTH and 
            y > self.SB_NG_Y_ABS and 
            y < self.SB_NG_Y_ABS + self.SB_BTN_HEIGHT):
            self.dis.blit(self._get_SB(ng_hover=True), 
                          (self.BOARD_SIZE, 0))                        
        else:
            self.dis.blit(self._get_SB(), (self.BOARD_SIZE, 0))

        pygame.display.update()

    def click(self, pos):
        """ Called when the mouse is left clicked.  If clicked in the sidebar,
        button presses are checked.  If click on board, pick up a pieces at
        the square coordinates and put in hand
        :param tuple(int, int) pos: Tuple containing the x and y coordinates 
            of the cursor
        :return: 1 if new game button is clicked, 2 if the main menu button is 
            clicked and 0 otherwise
        :rtype: int
        """
        x, y = pos
        # Sidebar menu
        if x > self.BOARD_SIZE:
            # Flip Board
            if (self.SB_FB_X_ABS < x < self.SB_FB_X_ABS+self.SB_BTN_WIDTH and 
            self.SB_FB_Y_ABS < y < self.SB_FB_Y_ABS + self.SB_BTN_HEIGHT):
                self.board_flipped = not self.board_flipped
            # Undo Move
            elif (self.SB_UD_X_ABS < x < self.SB_UD_X_ABS+self.SB_UD_WIDTH and
            self.SB_UD_Y_ABS < y < self.SB_UD_Y_ABS + self.SB_BTN_HEIGHT):
                self.game.undo_move()
            # Redo Move
            elif (self.SB_RD_X_ABS < x < self.SB_RD_X_ABS+self.SB_RD_WIDTH and
            self.SB_RD_Y_ABS < y < self.SB_RD_Y_ABS + self.SB_BTN_HEIGHT):
                self.game.redo_move()
            # Main Menu
            elif (self.SB_MM_X_ABS < x < self.SB_MM_X_ABS+self.SB_BTN_WIDTH and
            self.SB_MM_Y_ABS < y < self.SB_MM_Y_ABS + self.SB_BTN_HEIGHT):
                return 2
            # New Game
            elif (self.SB_NG_X_ABS < x < self.SB_NG_X_ABS+self.SB_BTN_WIDTH and 
            self.SB_NG_Y_ABS < y < self.SB_NG_Y_ABS + self.SB_BTN_HEIGHT):
                return 1
        # Board move
        else:  
            if self.in_hand:
                self.in_hand == None
            else:
                file = pos[0] // self.SQUARE_SIZE
                rank = 7 - (pos[1] // self.SQUARE_SIZE)
                if -1 < file < 8 and -1 < rank < 8:
                    if self.board_flipped:
                        file = 7 - file
                        rank = 7 - rank
                    self.in_hand = (file, rank)
        return 0

    def put_piece(self, pos):
        """ Place a piece at the given coordinates 
        :param tuple(int, int) pos: Tuple containing the x and y coordinates 
            of the cursor
        """
        if self.in_hand == None:
            return
        file = pos[0] // self.SQUARE_SIZE
        rank = 7 - (pos[1] // self.SQUARE_SIZE)
        if -1 < file < 8 and -1 < rank < 8:
            if self.board_flipped:
                file = 7 - file
                rank = 7 - rank
            promo_piece = None
            if self.game.is_promotion(self.in_hand, (file, rank)):
                promo_piece = self._choose_promotion((file, rank))
            move = self.game.get_move(self.in_hand, (file, rank), promo_piece)
            self.game.user_move(move)
        self.in_hand = None

    def _choose_promotion(self, square):
        """ Displays the promotion menu and returns the users choice 
        :param tuple(int, int) square: The coordinates of the promotion square
            (both coordinates from 0-7 inlcusive)
        :return: The promotion piece or None if none are chosen
        :rtype: chess.Piece
        """
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
        """ Displays the results menu 
        :param tuple(int, int) pos: Tuple containing the x and y coordinates 
            of the cursor
        """
        x, y = pos
        if (self.RM_NG_X_ABS < x < self.RM_NG_X_ABS + self.RM_NG_WIDTH and 
            self.RM_NG_Y_ABS < y < self.RM_NG_Y_ABS + self.RM_NG_HEIGHT):
            result_menu = self._get_results_menu(btn_hover=True)
        else:
            result_menu = self._get_results_menu()
        self.dis.blit(result_menu, (self.RM_X, self.RM_Y))
        pygame.display.update()

    def menu_click(self, pos):
        """ Returns the value 1 if the button is clicked 
        :param tuple(int, int) pos: Tuple containing the x and y coordinates 
            of the cursor
        :return: The value 1 if the button is clicked otherwise 0
        :rtype: int
        """
        x, y = pos
        if (self.RM_NG_X_ABS < x < self.RM_NG_X_ABS + self.RM_NG_WIDTH and
            self.RM_NG_Y_ABS < y < self.RM_NG_Y_ABS + self.RM_NG_HEIGHT):
            return 1
        else:
            return 0
