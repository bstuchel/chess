""" File: main.py
This is the main file for the chess application.  It contains the mainloop 
and control flow for the application.
"""
from gui import GUI
import pygame


def main():
    pygame.init()

    gui = GUI()
    pygame.display.update()

    # Mainloop
    while True:
        for event in pygame.event.get():
            # End application if window is closed
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        gui.update_display()


if __name__ == "__main__":
    main()
