import pygame
import os.path


class Tower:
    """
    Tower class that represents a tower in the game. It handles drawing the tower, its range, and detecting clicks on it.
    It also manages the tower's level and price.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.price = 0
        self.level = 0
        self.selected = False
        self.menu = None
        self.range = 100
        self.damage = 1
        self.shoot_cooldown = 1000
        self.time_since_last_shot = 0

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
        img = self.tower_imgs[self.level]
        rect = img.get_rect(center=(self.x, self.y))
        window.blit(img, rect)

        if self.selected:
            self.draw_range(window)

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
        img = self.tower_imgs[self.level]
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
        Simulates shooting at an enemy by reducing its health.
        This method should be called when the tower is ready to shoot.
        """
        enemy.take_damage(self.damage)

    def update(self, dt, enemies):
        """
        Updates the tower's state, including cooldown for shooting and checking for enemies in range.
        :param dt: The time delta since the last update.
        :param enemies: A list of enemy objects to check against the tower's range.
        """
        self.time_since_last_shot += dt
        if self.time_since_last_shot >= self.shoot_cooldown:
            target = self.find_target(enemies)
            if target:
                self.shoot(target)
                self.time_since_last_shot = 0
