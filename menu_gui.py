""" File: gui.py
This file contains the GUI for the chess application
"""
import pygame


class MenuGUI:
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
        self.BUTTON_WIDTH = self.WIDTH // 4
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
        pos: Tuple containing the x and y coordinates of the cursor
        """
        self.dis.fill(self.DARK_GRAY)

        # Write Heading
        header_label = self.HEADING_FONT.render("Welcome to Chess!", True, 
                                                self.WHITE)
        width = header_label.get_width()
        height = header_label.get_height()
        self.dis.blit(header_label, [self.WIDTH // 2 - width // 2, 
                                      self.HEADING_Y - height // 2])

        # Draw Button
        x, y = pos
        if (x > self.BUTTON_X and 
            x < self.BUTTON_X + self.BUTTON_WIDTH and 
            y > self.BUTTON_Y and 
            y < self.BUTTON_Y + self.BUTTON_HEIGHT):
            pygame.draw.rect(self.dis, self.LIGHT_GREEN,
                             (self.BUTTON_X, self.BUTTON_Y,
                              self.BUTTON_WIDTH, self.BUTTON_HEIGHT))
        else:
            pygame.draw.rect(self.dis, self.GREEN,
                             (self.BUTTON_X, self.BUTTON_Y,
                              self.BUTTON_WIDTH, self.BUTTON_HEIGHT))
        header_label = self.LABEL_FONT.render("New Game", True, self.WHITE)
        width = header_label.get_width()
        height = header_label.get_height()
        self.dis.blit(header_label, [self.WIDTH // 2 - width // 2, 
                                      self.HEIGHT // 2 - height // 2])

        pygame.display.update()

    def click(self, pos):
        """ Returns the value 1 if the button is clicked 
        pos: Tuple containing the x and y coordinates of the cursor
        """
        x, y = pos
        if (x > self.BUTTON_X and 
            x < self.BUTTON_X + self.BUTTON_WIDTH and 
            y > self.BUTTON_Y and 
            y < self.BUTTON_Y + self.BUTTON_HEIGHT):
            return 1
