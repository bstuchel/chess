""" File: main.py
This is the main file for the chess application.  It contains the mainloop 
and control flow for the application.
"""
from game import Game
import pygame
pygame.init()

from game import Game
from gui import GUI


def main():
    game = Game()
    gui = GUI(game)
    gui.update_display((0, 0))

    # Mainloop
    while True:
        for event in pygame.event.get():
            # End application if window is closed
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    gui.pick_piece(event.pos)

            if event.type == pygame.MOUSEMOTION:
                pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    gui.put_piece(event.pos)

        gui.update_display(pos)


if __name__ == "__main__":
    main()
