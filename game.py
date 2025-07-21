import os.path
import pygame

from enemies.tabby import Tabby

class Game:
    def __init__(self):
        self.width = 1280
        self.height = 960
        self.window = pygame.display.set_mode((self.width, self.height))

        self.enemies = [Tabby()]
        self.towers = []
        self.lives = 10
        self.money = 200
        self.background = pygame.transform.scale(
            pygame.image.load(os.path.join("assets","other", "map.png")),
            (self.width, self.height)
        )
        # self.clicks = []   used for mapping enemy path

    def run(self):
        run = True
        clock = pygame.time.Clock()
        
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # self.clicks.append(pos)      also used for mapping enemy path
                    # print(self.clicks)
                    pass
                    
            self.draw()

        pygame.quit()

    def draw(self):
        self.window.blit(self.background, (0,0))
        # for p in self.clicks:
            # pygame.draw.circle(self.window, (255,0,0), (p[0], p[1]), 5, 0)      used for mapping enemy path
        pygame.display.update()

tower_game = Game()
tower_game.run()