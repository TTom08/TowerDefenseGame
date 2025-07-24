import os
import pygame

from towers.tower import Tower

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Cannon(Tower):
    """
    Cannon tower class that represents a cannon tower in the game.
    It inherits from the Tower class and sets specific properties for the cannon tower.
    """

    tower_imgs = [
        pygame.transform.scale(
            pygame.image.load(os.path.join(base_path, "assets", "towers", "cannon.png")).convert_alpha(),
            (150, 150)
        )
    ]
    toolbar_icon = pygame.transform.scale(
        pygame.image.load(os.path.join(base_path, "assets", "ui", "toolbar_cannon.png")).convert_alpha(),
        (160, 112)
    )
    toolbar_highlight = pygame.transform.scale(
        pygame.image.load(os.path.join(base_path, "assets", "ui", "toolbar_cannon_highlight.png")).convert_alpha(),
        (160, 112)
    )

    def __init__(self, x, y):
        super().__init__(x, y)
        self.tower_imgs = Cannon.tower_imgs
        self.range = 200
        self.price = 200