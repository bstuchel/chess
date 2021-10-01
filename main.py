""" File: main.py
This is the main file for the chess application.  It contains the mainloop 
and control flow for the application.

To Do:
    - Add AI for singleplayer games
    - Add a game clock
    - Add a display of previous moves
"""
import pygame
pygame.init()

from enum import Enum
from game import Game
from game_gui import GameGUI
from menu_gui import MenuGUI


# Window Geometry
WINDOW_WIDTH = 860
WINDOW_HEIGHT = 680


class GameState(Enum):
    """ Type used to control the gamestate """
    QUIT = -1
    GAME = 0
    MENU = 1


def main():
    """ Set up and control the flow of the application """
    dis = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Chess')
    game_state = GameState.MENU
    while True:
        if game_state == GameState.GAME:
            game_state = play(dis)

        if game_state == GameState.MENU:
            game_state = menu(dis)

        if game_state == GameState.QUIT:
            pygame.quit()
            return


def play(dis):
    """ Sets up and runs the chess game """
    game = Game()
    gui = GameGUI(dis, game)
    pos = (0, 0)
    gui.update_display(pos)
    need_update = False

    # Game Loop
    while True:
        if not gui.in_hand:
            pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                result = gui.click(event.pos)
                if result == 1: return GameState.GAME
                if result == 2: return GameState.MENU
                need_update = True

            if event.type == pygame.MOUSEMOTION:
                pos = event.pos
                need_update = True

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                gui.put_piece(event.pos)
                need_update = True

        if need_update:
            gui.update_display(pos)
            need_update = False
            if game.is_game_over():
                break

    # Results Menu
    gui.display_menu((0, 0))
    while True:
        pygame.time.delay(15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
        
            if event.type == pygame.MOUSEMOTION:
                gui.display_menu(event.pos)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                choice = gui.menu_click(event.pos)
                if choice == 1:
                    return GameState.GAME


def menu(dis):
    """ Sets up and shows the menu for the application """
    gui = MenuGUI(dis)
    pos = (0, 0)
    gui.update_display(pos)

    # Menu Loop
    while True:
        pygame.time.delay(15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT

            if event.type == pygame.MOUSEMOTION:
                gui.update_display(event.pos)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                choice = gui.click(event.pos)
                if choice == 1:
                    return GameState.GAME


if __name__ == "__main__":
    main()
