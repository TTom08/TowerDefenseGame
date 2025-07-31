import os.path
import pygame
from enemies.enemy import Enemy

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Black(Enemy):
    """
    Black enemy class that represents an armored black cat enemy in the game.
    It inherits from the Enemy class and sets specific properties for the black cat enemy.
    """
    imgs = [
        pygame.transform.scale(
            pygame.image.load(os.path.join(base_path, "assets", "enemies", f"armored{i + 1}.png")).convert_alpha(),
            (174, 132)
        ) for i in range(2)
    ]

    def __init__(self):
        super().__init__(animation_speed=15, movement_speed=2)
        self.imgs = Black.imgs
        self.y_offset = -45