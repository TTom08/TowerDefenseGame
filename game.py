import os.path

import pygame

class Game:
    def __init__(self):
        self.width = 960
        self.height = 720
        self.win = pygame.display.set_mode((self.width, self.height))

        self.enemies = []
        self.towers = []
        self.lives = 10
        self.money = 200
        self.background = pygame.image.load(os.path.join("towers", "map.png"))

    def run(self):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

        pygame.quit()

    def draw(self):
        self.win.blit(self.background, (0,0))
        pygame.display.update()