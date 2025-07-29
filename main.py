import pygame

from mainmenu import MainMenu
from game import Game


def main():
    pygame.init()

    window = pygame.display.set_mode((1500, 960))

    while True:
        menu = MainMenu(window)
        game = Game(window)

        menu_result = menu.run()
        if menu_result == "quit":
            break

        game_result = game.run()
        if game_result == "quit":
            break

        del game

if __name__ == "__main__":
    main()
