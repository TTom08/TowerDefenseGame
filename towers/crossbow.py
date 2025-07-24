import os

import pygame
from towers.tower import Tower

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Crossbow(Tower):
    """
    Crossbow tower class that represents a crossbow tower in the game.
    It inherits from the Tower class and sets specific properties for the crossbow tower.
    """
    tower_imgs = [
        pygame.transform.scale(
            pygame.image.load(os.path.join(base_path, "assets", "towers", "crossbow1.png")).convert_alpha(),
            (160, 160)
        )
    ]
    toolbar_icon = pygame.transform.scale(
        pygame.image.load(os.path.join(base_path, "assets", "ui", "toolbar_crossbow.png")).convert_alpha(),
        (160, 112)
    )
    toolbar_highlight = pygame.transform.scale(
        pygame.image.load(os.path.join(base_path, "assets", "ui", "toolbar_crossbow_highlight.png")).convert_alpha(),
        (160, 112)
    )

    def __init__(self, x, y):
        super().__init__(x, y)
        self.tower_imgs = Crossbow.tower_imgs
        self.range = 150
        self.price = 150
