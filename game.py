import os.path
import pygame

from enemies.tabby import Tabby


class Game:
    def __init__(self):
        self.game_width = 1280
        self.toolbar_width = 220
        self.width = self.game_width + self.toolbar_width
        self.height = 960
        self.window = pygame.display.set_mode((self.width, self.height))

        self.enemies = [Tabby()]
        self.towers = []
        self.lives = 10
        self.money = 200
        self.tool_images = []

        self.background = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "other", "map.png")),
            (self.game_width, self.height)
        )

        self.toolbar_bg = pygame.Surface((self.toolbar_width, self.height))
        self.toolbar_bg = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "ui", "toolbar.png")),
            (self.toolbar_width, self.height)
        )

        self.crossbow_img = pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "ui", "toolbar_crossbow.png")),
                (160, 112)
            )
        self.crossbow_highlight = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "ui", "toolbar_crossbow_highlight.png")),
            (160, 112)
        )

        self.crossbow_pos = (self.game_width + 30, 40)
        self.crossbow_rect = pygame.Rect(
            self.crossbow_pos[0],
            self.crossbow_pos[1],
            160, 112
        )
        self.crossbow_selected = False

    def run(self):
        run = True
        clock = pygame.time.Clock()

        while run:
            mouse_pos = pygame.mouse.get_pos()
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.crossbow_rect.collidepoint(mouse_pos):
                        self.crossbow_selected = not self.crossbow_selected

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
        self.window.blit(self.background, (0, 0))

        self.window.blit(self.toolbar_bg, (self.game_width, 0))

        # Displaying enemies
        for e in self.enemies:
            e.draw(self.window)

        self.window.blit(self.crossbow_img, self.crossbow_pos)

            # Highlight selected tool
        if self.crossbow_selected:
            self.window.blit(self.crossbow_highlight, self.crossbow_pos)

        # Display path points
        # for point in self.enemies[0].path:
        #    pygame.draw.circle(self.window, (255, 0, 0), point, 5)
        pygame.display.update()


tower_game = Game()
tower_game.run()
