import os.path
import pygame

pygame.init()
pygame.mixer.quit()

window = pygame.display.set_mode((1500, 960))

from enemies.tabby import Tabby
from enemies.black import Black
from towers.crossbow import Crossbow

class Game:
    def __init__(self):
        self.game_width = 1280
        self.toolbar_width = 220
        self.width = self.game_width + self.toolbar_width
        self.height = 960
        self.window = pygame.display.set_mode((self.width, self.height))

        self.lives = 10
        self.money = 200
        self.selected_tool = None
        self.towers = []

        self.enemies = [Tabby(), Black()]

        self.available_towers = [
            {
                'class': Crossbow,
                'icon': Crossbow.toolbar_icon,
                'highlight': Crossbow.toolbar_highlight,
                'pos': (self.game_width + 30, 33)
            }
        ]

        # Game background
        self.background = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "other", "map.png")).convert(),
            (self.game_width, self.height)
        )

        # Toolbar background
        self.toolbar_bg = pygame.Surface((self.toolbar_width, self.height))
        self.toolbar_bg = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "ui", "toolbar.png")).convert(),
            (self.toolbar_width, self.height)
        )

        # Start button
        self.start_button = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "ui", "start_btn.png")).convert_alpha(),
            (198, 165)
        )

        # Placement mask
        self.placement_mask = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "other", "placement_mask.png")).convert(),
            (self.game_width, self.height)
        )
        self.mask_pixels = pygame.PixelArray(self.placement_mask)

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
                        # Place tower on map if the area is buildable
                        if self.selected_tool and mouse_pos[0] < self.game_width:
                            if self.is_buildable(mouse_pos[0], mouse_pos[1]):
                                self.towers.append(self.selected_tool(mouse_pos[0], mouse_pos[1]))
                                self.selected_tool = None
                            else:
                                print("Invalid build location!")

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

    def is_buildable(self, x, y):
        if 0 <= x < self.game_width and 0 <= y < self.height:
            color = self.placement_mask.get_at((x, y))
            return color[:3] == (255, 255, 255)  # White means its buildable
        return False

    def draw(self):
        self.window.blit(self.background, (0, 0))

        self.window.blit(self.toolbar_bg, (self.game_width, 0))



        for tower in self.towers:
            tower.draw(self.window)

        for e in self.enemies:
            e.draw(self.window)

        for t in self.available_towers:
            self.window.blit(t['icon'], t['pos'])
            if self.selected_tool == t['class']:
                self.window.blit(t['highlight'], t['pos'])

        # Draw preview image of the tower whle hovering over the game area
        if self.selected_tool:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x < self.game_width:
                preview_tower = self.selected_tool(mouse_x, mouse_y)
                preview_img = preview_tower.tower_imgs[preview_tower.level].copy()
                if self.is_buildable(mouse_x, mouse_y):
                    preview_img.set_alpha(128)  # semi-transparent green
                else:
                    preview_img.fill((255, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)
                    preview_tower.tower_range_circle.fill((220, 35, 35, 144), special_flags=pygame.BLEND_RGBA_MULT)
                rect = preview_img.get_rect(center=(mouse_x, mouse_y))
                self.window.blit(preview_img, rect)

                # Properly scaled tower range circle
                scaled_circle = pygame.transform.scale(
                    preview_tower.tower_range_circle, (2 * preview_tower.range, 2 * preview_tower.range)
                )
                # Display range while hovering the preview tower
                self.window.blit(
                    scaled_circle, (mouse_x - preview_tower.range, mouse_y - preview_tower.range)
                )

        # Display path points
        # for point in self.enemies[0].path:
        #    pygame.draw.circle(self.window, (255, 0, 0), point, 5)

        self.window.blit(self.start_button, (1292, 784))

        pygame.display.update()


tower_game = Game()
tower_game.run()
