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

    def run(self):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

        pygame.quit()