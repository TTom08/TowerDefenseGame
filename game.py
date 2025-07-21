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
                    pass

            # Iterate through enemies - to list
            to_delete = []
            for e in self.enemies:
                if e.path_pos >= len(e.path) - 1:
                    to_delete.append(e)
            # Delete enemy once its off screen
            for d in to_delete:
                self.enemies.remove(d)
                    
            self.draw()

        pygame.quit()

    def draw(self):
        self.window.blit(self.background, (0,0))

        # Displaying enemies
        for e in self.enemies:
            e.draw(self.window)

        # Display path points
        #for point in self.enemies[0].path:
        #    pygame.draw.circle(self.window, (255, 0, 0), point, 5)
        pygame.display.update()

tower_game = Game()
tower_game.run()