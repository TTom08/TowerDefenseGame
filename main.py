import pygame
import os

from mainmenu import MainMenu
from game import Game
from font import Font
from enemies.enemy import Enemy


def load_assets():
    """
    Load all necessary assets for the game.
    This function can be expanded to load more assets as needed.
    """
    pygame.mixer.quit()

    assets = {}
    # game.py assets
    assets['game_background'] = pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "other", "map.png")).convert(),
        (1280, 960)
    )
    assets['toolbar_bg'] = pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "ui", "toolbar.png")).convert(),
        (220, 960)
    )
    assets['start_button'] = pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "ui", "start_btn.png")).convert_alpha(),
        (198, 165)
    )
    assets['pause_button'] = pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "ui", "pause_btn.png")).convert_alpha(),
        (198, 165)
    )
    assets['placement_mask'] = pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "other", "placement_mask.png")).convert(),
        (1500, 960)
    )
    assets['statbar_bg'] = pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "ui", "statbar.png")).convert_alpha(),
        (900, 102)
    )
    assets['statbar_heart'] = pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "ui", "heart.png")).convert_alpha(),
        (50, 47.5)
    )
    assets['statbar_coin'] = pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "ui", "coin.png")).convert_alpha(),
        (26 + (13 * 0.35), 38 + (19 * 0.35))
    )
    assets['exit_menu_bg'] = pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "ui", "exit_menu.png")).convert_alpha(),
        (500, 150)
    )
    assets['exit_btn'] = pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "ui", "exit_btn.png")).convert_alpha(),
        (180, 72)
    )
    assets['continue_btn'] = pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "ui", "continue_btn.png")).convert_alpha(),
        (180, 72)
    )
    assets['my_font'] = Font("assets/ui/font.png")

    # mainmenu.py assets
    assets['menu_background'] = pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "ui", "mainmenu", "bg2.png")).convert(),
        (1500, 960)
    )
    assets['menu_ui_bg'] = pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "ui", "mainmenu", "mainmenu_ui_bg.png")).convert_alpha(),
        (1500, 480)
    )
    assets['menu_exit_btn'] = pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "ui", "mainmenu", "exitgame_btn.png")).convert_alpha(),
        (420, 90)
    )
    assets['menu_exit_btn_hover'] = pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "ui", "mainmenu", "exitgame_btn_hover.png")).convert_alpha(),
        (420, 90)
    )
    assets['play_btn'] = pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "ui", "mainmenu", "play_btn.png")).convert_alpha(),
        (420, 90)
    )
    assets['play_btn_hover'] = pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "ui", "mainmenu", "play_btn_hover.png")).convert_alpha(),
        (420, 90)
    )

    # enemy death particles
    assets['death_particles'] = [
        pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "enemies","death", f"death_particle{i + 1}.png")).convert_alpha(),
            (128, 128)
        ) for i in range(7)
    ]

    return assets


def main():
    pygame.init()

    window = pygame.display.set_mode((1500, 960))

    assets = load_assets()

    while True:
        menu = MainMenu(window, assets)
        enemy = Enemy(assets)
        menu.fade_in(window)
        menu_result = menu.run()

        if menu_result == "quit":
            break

        while True:
            game = Game(window, assets)
            game.fade_in(window)
            game_result = game.run()

            if game_result == "quit":
                break
            elif game_result == "restart":
                continue
            else:
                break

        if game_result == "quit":
            break


if __name__ == "__main__":
    main()
