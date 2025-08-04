import math
import os
import pygame

from towers.projectile import Projectile
from towers.tower import Tower

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Cannon(Tower):
    """
    Cannon tower class that represents a cannon tower in the game.
    It inherits from the Tower class and sets specific properties for the cannon tower.
    """

    tower_imgs = [
        pygame.transform.scale(
            pygame.image.load(os.path.join(base_path, "assets", "towers", f"cannon{i + 1}.png")).convert_alpha(),
            (150, 150)
        ) for i in range(4)
    ]
    toolbar_icon = pygame.transform.scale(
        pygame.image.load(os.path.join(base_path, "assets", "ui", "toolbar_cannon.png")).convert_alpha(),
        (160, 112)
    )
    toolbar_highlight = pygame.transform.scale(
        pygame.image.load(os.path.join(base_path, "assets", "ui", "toolbar_cannon_highlight.png")).convert_alpha(),
        (160, 112)
    )
    price = 300

    def __init__(self, x, y):
        super().__init__(x, y)
        self.tower_imgs = Cannon.tower_imgs
        self.range = 200
        self.price = Cannon.price
        self.damage = 2
        self.shoot_cooldown = 1500
        self.projectile_img = pygame.transform.scale(
            pygame.image.load(os.path.join(base_path, "assets", "towers", "cannon_projectile.png")).convert_alpha(),
            (32, 32)
        )

    def shoot(self, enemy):
        """
        Spawns a projectile toward the enemy from the cannon's turret tip.
        """
        dx = enemy.x - self.x
        dy = enemy.y - self.y
        angle = math.atan2(dy, dx)

        offset_x = math.cos(angle) * 70
        offset_y = math.sin(angle) * 70
        spawn_x = self.x + offset_x
        spawn_y = self.y + offset_y

        projectile = Projectile(spawn_x, spawn_y, enemy, damage=self.damage, image=self.projectile_img)
        self.projectiles.append(projectile)
