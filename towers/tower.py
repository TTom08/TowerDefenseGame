import pygame
import os.path

class Tower:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.price = 0
        self.level = 0
        self.selected = False
        self.menu = None
        self.range = 100

        self.tower_range_circle = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "towers", "range_circle_64.png")),
            (self.range, self.range)
        )

    def draw(self, window):
        img = self.tower_imgs[self.level]
        rect = img.get_rect(center=(self.x, self.y))
        window.blit(img, rect)

        if self.selected:
            self.draw_range(window)

    # Draws the range circle around the tower once its placed down
    def draw_range(self, window):
        if self.tower_range_circle:
            # used for centering
            window.blit(
                self.tower_range_circle,
                (self.x - self.tower_range_circle.get_width() // 2,
                 self.y - self.tower_range_circle.get_height() // 2)
            )



    def click(self, x, y):
        img = self.tower_imgs[self.level]
        rect = img.get_rect(center=(self.x, self.y))
        return rect.collidepoint(x, y)
