import os.path
import pygame
from enemies.enemy import Enemy

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Tabby(Enemy):
    """
    Tabby enemy class that represents a tabby cat enemy in the game.
    It inherits from the Enemy class and sets specific properties for the tabby enemy.
    """
    imgs = [
        pygame.transform.scale(
            pygame.image.load(os.path.join(base_path, "assets", "enemies", f"tabby{i + 1}.png")).convert_alpha(),
            (174, 132)
        ) for i in range(2)
    ]

    def __init__(self):
        super().__init__(animation_speed=10, movement_speed=3)
        self.imgs = Tabby.imgs
