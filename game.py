import os.path
import pygame

from enemies.tabby import Tabby
from towers.crossbow import Crossbow


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
        self.selected_tool = None

        # Game background
        self.background = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "other", "map.png")),
            (self.game_width, self.height)
        )

        # Toolbar background
        self.toolbar_bg = pygame.Surface((self.toolbar_width, self.height))
        self.toolbar_bg = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "ui", "toolbar.png")),
            (self.toolbar_width, self.height)
        )

        self.available_towers = [
            {
                'class': Crossbow,
                'icon': Crossbow.toolbar_icon,
                'highlight': Crossbow.toolbar_highlight,
                'pos': (self.game_width + 30, 33)
            }
        ]

        for t in self.available_towers:
            t['rect'] = pygame.Rect(t['pos'][0], t['pos'][1], 160, 112)

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
                    for t in self.available_towers:
                        if t['rect'].collidepoint(mouse_pos):
                            self.selected_tool = t['class'] if self.selected_tool != t['class'] else None
                            break
                    else:
                        # Place tower on map if selected
                        if self.selected_tool and mouse_pos[0] < self.game_width:
                            self.towers.append(self.selected_tool(mouse_pos[0], mouse_pos[1]))
                            self.selected_tool = None

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

        for e in self.enemies:
            e.draw(self.window)

        for t in self.available_towers:
            self.window.blit(t['icon'], t['pos'])
            if self.selected_tool == t['class']:
                self.window.blit(t['highlight'], t['pos'])

        if self.selected_tool:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            print(self.selected_tool)
            if mouse_x < self.game_width:
                # Hovering tower image
                preview_tower = self.selected_tool(mouse_x, mouse_y)

                # Range circle around the tower
                pygame.draw.circle(self.window, (0, 255, 0), (mouse_x, mouse_y), preview_tower.range, 1)

                # Transparent preview image of the tower
                preview_img = preview_tower.tower_imgs[preview_tower.level].copy()
                preview_img.set_alpha(128)
                rect = preview_img.get_rect(center=(mouse_x, mouse_y))
                self.window.blit(preview_img, rect)

        for tower in self.towers:
            tower.draw(self.window)

        # Display path points
        # for point in self.enemies[0].path:
        #    pygame.draw.circle(self.window, (255, 0, 0), point, 5)
        pygame.display.update()

tower_game = Game()
tower_game.run()
