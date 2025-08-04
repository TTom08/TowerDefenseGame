import os.path
import pygame
from enemies.enemy import Enemy

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Boss(Enemy):
    """
    Tabby enemy class that represents a tabby cat enemy in the game.
    It inherits from the Enemy class and sets specific properties for the tabby enemy.
    """
    imgs = [
        pygame.transform.scale(
            pygame.image.load(os.path.join(base_path, "assets", "enemies", f"boss{i + 1}.png")).convert_alpha(),
            (162, 234)
        ) for i in range(2)
    ]

    def __init__(self, assets):
        super().__init__(assets, animation_speed=10, movement_speed=3)
        self.imgs = Boss.imgs
        self.y_offset = 10
        self.health = 10
        self.should_rotate = True
        self.value = 50
