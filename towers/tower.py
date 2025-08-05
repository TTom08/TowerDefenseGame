import math

import pygame
import os.path

from towers.projectile import Projectile


class Tower:
    """
    Tower class that represents a tower in the game. It handles drawing the tower, its range, and detecting clicks on it.
    It also manages the tower's level and price.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.price = 0
        self.level = 1
        self.selected = False
        self.menu = None
        self.range = 100
        self.damage = 1
        self.shoot_cooldown = 1050
        self.time_since_last_shot = 0

        self.tower_imgs = []
        self.shooting = False
        self.tower_shooting_frame = 0
        self.animation_cd = 150
        self.animation_timer = 0

        self.projectile_img = None
        self.projectiles = []
        self.current_target = None
        self.last_rotation_angle = 0

        self.tower_range_circle = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "towers", "range_circle_64.png")).convert_alpha(),
            (self.range, self.range)
        )
        self.tower_range_circle.set_alpha(144)

    def draw(self, window):
        """
        Draws the tower on the given window.
        If the tower is selected it also draws the range circle around it.
        :param window: The Pygame window where the tower will be drawn.
        """
        current_level_frames = self.tower_imgs[self.level - 1]

        # Get the current frame
        if self.shooting and self.tower_shooting_frame < len(current_level_frames):
            current_frame = current_level_frames[self.tower_shooting_frame]
        else:
            current_frame = current_level_frames[0]

        # Rotate the image based on the last rotation angle
        rotated_img = pygame.transform.rotate(current_frame, -self.last_rotation_angle)

        rect = rotated_img.get_rect(center=(self.x, self.y))
        window.blit(rotated_img, rect)

        if self.selected:
            self.draw_range(window)

        for proj in self.projectiles:
            proj.draw(window)

    def draw_range(self, window):
        """
        Draws the range circle around the tower once its placed down.
        :param window: The Pygame window where the range circle will be drawn.
        """
        if self.tower_range_circle:
            # used for centering
            window.blit(
                self.tower_range_circle,
                (self.x - self.tower_range_circle.get_width() // 2,
                 self.y - self.tower_range_circle.get_height() // 2)
            )

    def click(self, x, y):
        """
        Detects if the tower was clicked on by checking if the given coordinates (x, y) collide with the tower's rectangle.
        :param x: The x-coordinate of the click.
        :param y: The y-coordinate of the click.
        """
        current_level_frames = self.tower_imgs[self.level - 1]
        img = current_level_frames[0]

        rect = img.get_rect(center=(self.x, self.y))
        return rect.collidepoint(x, y)

    def is_enemy_in_range(self, enemy):
        """
        Checks if the given enemy is within the tower's range.
        :param enemy: The enemy object to check against the tower's range.
        :return: True if the enemy is within range, False otherwise.
        """
        distance = ((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2) ** 0.5
        return distance <= self.range

    def find_target(self, enemies):
        """
        Finds the first enemy within the tower's range.
        :param enemies: A list of enemy objects to check against the tower's range.
        :return: The first enemy within range, or None if no enemy is found.
        """
        for enemy in enemies:
            if self.is_enemy_in_range(enemy):
                return enemy
        return None

    def shoot(self, enemy):
        """
        Spawns a projectile toward the enemy.
        """
        projectile = Projectile(self.x, self.y, enemy, damage=self.damage, image=self.projectile_img)
        self.projectiles.append(projectile)

    def update(self, dt, enemies):
        """
        Updates the tower's state, including cooldown for shooting and checking for enemies in range.
        :param dt: The time delta since the last update.
        :param enemies: A list of enemy objects to check against the tower's range.
        """
        self.time_since_last_shot += dt
        self.animation_timer += dt

        for proj in self.projectiles[:]:
            proj.update(dt)
            if not proj.alive:
                self.projectiles.remove(proj)

        if self.shooting:
            if self.animation_timer >= self.animation_cd:
                self.tower_shooting_frame += 1
                self.animation_timer = 0
                if self.tower_shooting_frame >= len(self.tower_imgs[self.level - 1]):
                    self.tower_shooting_frame = 0
                    self.shooting = False

        if self.time_since_last_shot >= self.shoot_cooldown and not self.shooting:
            target = self.find_target(enemies)
            if target:
                self.current_target = target
                self.rotation_angle = self.get_angle_to_enemy(target)
                self.last_rotation_angle = self.rotation_angle
                self.shooting = True
                self.tower_shooting_frame = 0
                self.animation_timer = 0
                self.shoot(target)
                self.time_since_last_shot = 0
            else:
                self.current_target = None
                self.shooting = False

    def get_angle_to_enemy(self, enemy):
        """
        Calculates the angle from the tower to the enemy in degrees.
        :param enemy: The enemy object to calculate the angle to.
        :return: The angle in degrees from the tower to the enemy.
        """
        dx = enemy.x - self.x
        dy = enemy.y - self.y

        angle_deg = math.degrees(math.atan2(dy, dx))

        # Smooth transition across the 180°/-180° boundary
        if angle_deg < -90:
            angle_deg += 360

        return (angle_deg - 90) % 360

    def update_range_circle(self):
        """
        Updates the range circle image based on the current range of the tower.
        """
        self.tower_range_circle = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "towers", "range_circle_64.png")).convert_alpha(),
            (self.range, self.range)
        )
        self.tower_range_circle.set_alpha(144)

    def upgrade(self):
        """
        Upgrades the tower to the next level, increasing its range and decreasing its shooting cooldown.
        """
        if self.level < 2 and len(self.tower_imgs) > self.level:
            self.level += 1
            self.range += 100
            self.animation_cd = 100  # 100ms × 7 = 700ms total animation
            self.shoot_cooldown = self.animation_cd * len(self.tower_imgs[self.level - 1])
            self.update_range_circle()
