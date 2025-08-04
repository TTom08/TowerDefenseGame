import pygame
import math

class Projectile:
    """
    Projectile class that represents a projectile fired by a tower towards an enemy.
    """
    def __init__(self, x, y, enemy, speed=400, damage=1, image=None):
        self.x = x
        self.y = y
        self.enemy = enemy
        self.speed = speed
        self.damage = damage
        self.image = image
        self.alive = True

        dx = enemy.x - x
        dy = enemy.y - y
        distance = math.hypot(dx, dy)
        if distance == 0:
            self.direction_x = 0
            self.direction_y = 0
        else:
            self.direction_x = dx / distance
            self.direction_y = dy / distance

    def update(self, dt):
        """
        Updates the projectile's position based on its speed and direction.
        :param dt: Time delta since the last update in milliseconds.
        """
        dt = dt / 1000.0
        if not self.enemy.alive:
            self.alive = False
            return

        dx = self.enemy.x - self.x
        dy = self.enemy.y - self.y
        distance = math.hypot(dx, dy)

        if distance != 0:
            self.direction_x = dx / distance
            self.direction_y = dy / distance

        self.x += self.direction_x * self.speed * dt
        self.y += self.direction_y * self.speed * dt

        if distance < self.speed * dt:
            self.enemy.take_damage(self.damage)
            self.alive = False

    def draw(self, window):
        rect = self.image.get_rect(center=(self.x, self.y))
        window.blit(self.image, rect)