import os.path
import pygame
from enemies.enemy import Enemy

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Rolling(Enemy):
    """
    Black enemy class that represents an armored black cat enemy in the game.
    It inherits from the Enemy class and sets specific properties for the black cat enemy.
    """
    imgs = [
        pygame.transform.scale(
            pygame.image.load(os.path.join(base_path, "assets", "enemies","rolling", f"rolling{i + 1}.png")).convert_alpha(),
            (160, 132)
        ) for i in range(6)
    ]

    def __init__(self):
        super().__init__(animation_speed=5, movement_speed=5)
        self.imgs = Rolling.imgs