import pygame

from mainmenu import MainMenu
from game import Game


def main():
    pygame.init()

    window = pygame.display.set_mode((1500, 960))

    while True:
        menu = MainMenu(window)
        menu.fade_in(window)
        menu_result = menu.run()


        if menu_result == "quit":
            break

        game = Game(window)
        game.fade_in(window)
        game_result = game.run()


        if game_result == "quit":
            break

        del game


if __name__ == "__main__":
    main()
