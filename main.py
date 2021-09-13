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
    pos = (0, 0)
    gui.update_display(pos)
    need_update = False

    # Mainloop
    while True:
        if not game.picked_piece:
            pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    gui.pick_piece(event.pos)
                    need_update = True

            if event.type == pygame.MOUSEMOTION:
                pos = event.pos
                need_update = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    gui.put_piece(event.pos)
                    need_update = True

        if need_update:
            gui.update_display(pos)
            need_update = False


if __name__ == "__main__":
    main()
