import os.path
import pygame
from enemies.enemy import Enemy

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Tabby(Enemy):
    imgs = [
        pygame.transform.scale(
            pygame.image.load(os.path.join(base_path, "assets", "enemies", f"tabby{i + 1}.png")),
            (174, 132)
        )
        for i in range(2)
    ]

    def __init__(self):
        super().__init__(animation_speed=10)
        self.imgs = Tabby.imgs
