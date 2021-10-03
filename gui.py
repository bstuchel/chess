""" File: gui.py
This file contains the GUI class which contains methods used for the a
pplications GUI.
"""
import pygame


class GUI:
    def draw_button(self, x, y, w, h, ac, ic, font, fc, msg, surf, active):
        """ Draw a button given the following parameters
        
        :param int x: The x-coordinate of the top-left corner of the button
        :param int y: The y-coordinate of the top-left corner of the button
        :param int w: The width of the button
        :param int h: The height of the button
        :param pygame.Color or int or tuple (int, int, int [int]) ac: The 
            active color of the button
        :param pygame.Color or int or tuple (int, int, int [int]) ic: The 
            inactive color of the button
        :param pygame.font.Font font: The font of the button label
        :param pygame.Color or int or tuple (int, int, int [int]) fc: The 
            color of the button label
        :param str msg: The text for the button label
        :param pygame.Surface surf: The surface that the button is drawn on
        :param bool active: True when the button is active
        """
        color = ac if active else ic
        pygame.draw.rect(surf, color, (x, y, w, h))
        self.draw_label(x + w // 2, y + h // 2, font, fc, msg, surf)

    @staticmethod
    def draw_label(x, y, font, fc, msg, surf):
        """ Draw a label the following parameters
        
        :param int x: The x-coordinate of the middle-center of the label
        :param int y: The y-coordinate of the middle-center of the label
        :param pygame.font.Font font: The font of the label
        :param pygame.Color or int or tuple (int, int, int [int]) fc: The 
            color of the label
        :param str msg: The text for the label
        :param pygame.Surface surf: The surface that the button is drawn on
        """
        label = font.render(msg, True, fc)
        width = label.get_width()
        height = label.get_height()
        surf.blit(label, [x - width // 2, y - height // 2])
