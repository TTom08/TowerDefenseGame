import os
import pygame

from towers.tower import Tower

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Crossbow(Tower):
    """
    Crossbow tower class that represents a crossbow tower in the game.
    """
    tower_animations = [
        [
            pygame.transform.scale(
                pygame.image.load(
                    os.path.join(base_path, "assets", "towers", f"crossbow{i + 1}.png")).convert_alpha(),
                (160, 160)
            ) for i in range(7)
        ],
        [
            pygame.transform.scale(
                pygame.image.load(
                    os.path.join(base_path, "assets", "towers", f"crossbow_upg{i + 1}.png")).convert_alpha(),
                (160, 160)
            ) for i in range(7)
        ]
    ]

    toolbar_icon = pygame.transform.scale(
        pygame.image.load(os.path.join(base_path, "assets", "ui", "toolbar_crossbow.png")).convert_alpha(),
        (160, 112)
    )
    toolbar_highlight = pygame.transform.scale(
        pygame.image.load(os.path.join(base_path, "assets", "ui", "toolbar_crossbow_highlight.png")).convert_alpha(),
        (160, 112)
    )
    price = 150

    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 150
        self.price = Crossbow.price
        self.projectile_img = pygame.transform.scale(
            pygame.image.load(os.path.join(base_path, "assets", "towers", "crossbow_projectile.png")).convert_alpha(),
            (48, 48)
        )
        self.tower_imgs = Crossbow.tower_animations

    def draw(self, window):
        """
        Override draw to handle multi-level animations
        """
        if self.shooting and self.tower_shooting_frame < len(self.tower_imgs[self.level - 1]):
            img = self.tower_imgs[self.level - 1][self.tower_shooting_frame]
        else:
            img = self.tower_imgs[self.level - 1][0]

        rotated_img = pygame.transform.rotate(img, -self.last_rotation_angle)
        rect = rotated_img.get_rect(center=(self.x, self.y))
        window.blit(rotated_img, rect)

        if self.selected:
            self.draw_range(window)

        for proj in self.projectiles:
            proj.draw(window)

    def upgrade(self):
        if self.level < 2:
            super().upgrade()