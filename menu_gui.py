""" File: menu_gui.py
This file contains the GUI for the chess menu
"""
from gui import GUI
import pygame


class MenuGUI(GUI):
    # Define Colors
    DARK_GRAY = (49, 46, 43)
    GREEN = (118, 150, 86)
    LIGHT_GREEN = (168, 200, 136)
    WHITE = (255, 255, 255)

    def __init__(self, dis):
        dis.fill(self.DARK_GRAY)
        self.dis = dis
        self._define_geometry()
        self._define_fonts()

    def _define_geometry(self):
        """ Define geometry used in the menu GUI """
        # Window Data
        self.WIDTH, self.HEIGHT = self.dis.get_size()

        # Menu Data
        self.HEADING_Y = self.HEIGHT // 4
        self.BUTTON_HEIGHT = self.HEIGHT // 10
        self.BUTTON_WIDTH = 3 * self.BUTTON_HEIGHT
        self.BUTTON_X = self.WIDTH // 2 - self.BUTTON_WIDTH // 2
        self.BUTTON_Y = self.HEIGHT // 2 - self.BUTTON_HEIGHT // 2

    def _define_fonts(self):
        """ Define the fonts used in the menu GUI """
        self.HEADING_FONT = pygame.font.SysFont('bahnschrift', 
                                                self.HEIGHT // 20)
        self.LABEL_FONT = pygame.font.SysFont('bahnschrift', 
                                              self.HEIGHT // 25)

    def update_display(self, pos):
        """ Updates the display by clearing the display to the blank board 
        surface.  Pieces are then drawn to the board including pieces held by 
        the user.
        :param tuple(int, int) pos: Tuple containing the x and y coordinates 
            of the cursor
        """
        self.dis.fill(self.DARK_GRAY)

        # Write Heading
        self.draw_label(self.WIDTH // 2, self.HEADING_Y, self.HEADING_FONT, 
                        self.WHITE, "Welcome to Chess!", self.dis)

        # Draw Button
        x, y = pos
        hover = (self.BUTTON_X < x < self.BUTTON_X + self.BUTTON_WIDTH and 
                 self.BUTTON_Y < y < self.BUTTON_Y + self.BUTTON_HEIGHT)

        self.draw_button(self.BUTTON_X, self.BUTTON_Y, self.BUTTON_WIDTH, 
                         self.BUTTON_HEIGHT, self.LIGHT_GREEN, self.GREEN, 
                         self.LABEL_FONT, self.WHITE, "New Game", self.dis, 
                         hover)

        pygame.display.update()

    def click(self, pos):
        """ Returns the value 1 if the button is clicked 
        :param tuple(int, int) pos: Tuple containing the x and y coordinates 
            of the cursor
        :return: The value 1 if the button is clicked otherwise 0
        :rtype: int
        """
        x, y = pos
        if (self.BUTTON_X < x < self.BUTTON_X + self.BUTTON_WIDTH and 
            self.BUTTON_Y < y < self.BUTTON_Y + self.BUTTON_HEIGHT):
            return 1
        else:
            return 0
