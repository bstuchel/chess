""" File: main.py
This is the main file for the chess application.  It contains the mainloop 
and control flow for the application.
"""
from game import Game
import pygame
pygame.init()

from enum import Enum
from game import Game
from gui import GUI


class GameState(Enum):
    # Type used to control the gamestate
    QUIT = -1
    GAME = 0
    MENU = 1


def main():
    pygame.init()
    gui = GUI()
    game_state = GameState.GAME
    while True:
        if game_state == GameState.GAME:
            game_state = play(gui)

        if game_state == GameState.MENU:
            game_state = menu(gui)

        if game_state == GameState.QUIT:
            pygame.quit()
            return


def play(gui):
    game = Game()
    gui.set_game(game)
    pos = (0, 0)
    gui.update_display(pos)
    need_update = False

    # Mainloop
    while True:
        if not gui.in_hand:
            pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT

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
            if game.is_game_over():
                return GameState.MENU

    
def menu(gui):
    pos = (0, 0)
    gui.update_display(pos)

    # Display the end game menu
    gui.display_menu()

    # Mainloop
    while True:
        pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    gui.menu_click(pos)


if __name__ == "__main__":
    main()
