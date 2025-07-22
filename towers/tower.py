import pygame

class Tower:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.price = 0
        self.level = 0
        self.selected = False
        self.menu = None
        self.range = 100

    def draw(self, window):
        img = self.tower_imgs[self.level]
        rect = img.get_rect(center=(self.x, self.y))
        window.blit(img, rect)

        if self.selected:
            self.draw_range(window)

    def draw_range(self, window):
        pygame.draw.circle(window, (0, 255, 0), (self.x, self.y), self.range, 2)

    def click(self, x, y):
        img = self.tower_imgs[self.level]
        rect = img.get_rect(center=(self.x, self.y))
        return rect.collidepoint(x, y)
