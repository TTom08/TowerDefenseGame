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
