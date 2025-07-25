import os.path
import pygame

pygame.init()
pygame.mixer.quit()

window = pygame.display.set_mode((1500, 960))

from enemies.tabby import Tabby
from enemies.black import Black
from towers.crossbow import Crossbow
from towers.cannon import Cannon
from font import Font


###
# This is a simple tower defense game where you can place towers to defend against waves of enemies.
###

class Game:
    """
    This is the main game class that handles the game loop, events, and rendering.
    """

    def __init__(self):
        self.game_width = 1280
        self.toolbar_width = 220
        self.width = self.game_width + self.toolbar_width
        self.height = 960
        self.window = pygame.display.set_mode((self.width, self.height))

        self.lives = 10
        self.money = 200
        self.round = 0
        self.selected_tool = None
        self.towers = []
        self.round_active = False

        self.enemies = []

        self.available_towers = [
            {
                'class': Crossbow,
                'icon': Crossbow.toolbar_icon,
                'highlight': Crossbow.toolbar_highlight,
                'pos': (self.game_width + 30, 33)
            },
            {
                'class': Cannon,
                'icon': Cannon.toolbar_icon,
                'highlight': Cannon.toolbar_highlight,
                'pos': (self.game_width + 30, 160)
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
        # Pause button
        self.pause_button = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "ui", "pause_btn.png")).convert_alpha(),
            (198, 165)
        )

        # Placement mask
        self.placement_mask = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "other", "placement_mask.png")).convert(),
            (self.game_width, self.height)
        )
        self.mask_pixels = pygame.PixelArray(self.placement_mask)

        # Statbar - lives and money
        self.statbar_bg = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "ui", "statbar.png")).convert_alpha(),
            (900, 102)
        )
        self.statbar_heart = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "ui", "heart.png")).convert_alpha(),
            (50, 47.5)
        )
        self.statbar_coin = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "ui", "coin.png")).convert_alpha(),
            (26 + (13 * 0.35), 38 + (19 * 0.35))
        )

        # Exit menu and its buttons
        self.exit_menu_active = False
        self.exit_menu_bg = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "ui", "exit_menu.png")).convert_alpha(),
            (500, 150)
        )
        self.exit_btn = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "ui", "exit_btn.png")).convert_alpha(),
            (180, 72)
        )
        self.exit_btn_rect = self.exit_btn.get_rect(topleft=(self.game_width // 2 - 195, self.height // 2 - 33))
        self.continue_btn = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "ui", "continue_btn.png")).convert_alpha(),
            (180, 72)
        )
        self.continue_btn_rect = self.continue_btn.get_rect(topleft=(self.game_width // 2 + 20, self.height // 2 - 33))

        self.my_font = Font("assets/ui/font.png")

        for t in self.available_towers:
            t['rect'] = pygame.Rect(t['pos'][0], t['pos'][1], 160, 112)

        self.start_button_rect = self.start_button.get_rect(topleft=(1292, 784))

    def run(self):
        """
        Initializes the game and sets up the necessary variables and assets.
        This method is called when the game is started.
        """
        running = True
        clock = pygame.time.Clock()

        while running:
            mouse_pos = pygame.mouse.get_pos()
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for t in self.available_towers:
                        if t['rect'].collidepoint(mouse_pos):
                            self.selected_tool = t['class'] if self.selected_tool != t['class'] else None
                            break

                    if self.start_button_rect.collidepoint(mouse_pos):
                        if self.selected_tool:
                            print("Please place a tower before starting the game!")
                        else:
                            if not self.round_active:
                                # Start the round
                                self.enemies.append(Tabby())
                                self.enemies.append(Black())
                                self.round += 1
                                self.round_active = True
                            else:
                                # Pause the round
                                self.round_active = False
                    else:
                        # Place tower on map if the area is buildable
                        if self.selected_tool and mouse_pos[0] < self.game_width:
                            if (self.money - self.selected_tool.price if self.selected_tool else 0) >= 0:
                                if self.is_buildable(mouse_pos[0], mouse_pos[1]) and not self.is_overlapping(
                                        mouse_pos[0], mouse_pos[1]):
                                    self.towers.append(self.selected_tool(mouse_pos[0], mouse_pos[1]))
                                    self.money -= self.selected_tool.price
                                    self.selected_tool = None
                                else:
                                    print("Invalid build location!")
                            else:
                                print("Not enough money to place this tower!")

                    if self.exit_menu_active:
                        if self.exit_btn_rect.collidepoint(mouse_pos):
                            running = False
                        elif self.continue_btn_rect.collidepoint(mouse_pos):
                            self.exit_menu_active = False

                # Show exit menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.exit_menu_active = not self.exit_menu_active

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
        """
            Checks if the given coordinates (x, y) are buildable for placing a tower.
            :param x: The x-coordinate to check.
            :param y: The y-coordinate to check.
            """
        if 0 <= x < self.game_width and 0 <= y < self.height:
            color = self.placement_mask.get_at((x, y))
            return color[:3] == (255, 255, 255)  # White means its buildable
        return False

    def is_overlapping(self, x, y):
        """
        Checks if the given coordinates (x, y) overlap with any existing tower.
        :param x: The x-coordinate to check.
        :param y: The y-coordinate to check.
        """
        for tower in self.towers:
            if tower.click(x, y):
                return True
        return False

    def draw(self):
        """
        Displays the game window and draws all the game elements such as towers, enemies, and UI.
        """
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
                if self.is_buildable(mouse_x, mouse_y) and not self.is_overlapping(mouse_x, mouse_y):
                    preview_img.set_alpha(128)
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

        # Display start and pause buttons
        button_img = self.pause_button if self.round_active else self.start_button
        self.window.blit(button_img, (1292, 784))

        # Display lives and money on statbar
        self.window.blit(self.statbar_bg, (5, 5))
        self.window.blit(self.statbar_heart, (55, 30))
        self.window.blit(self.statbar_coin, (300, 22))
        # Test rendering numbers
        self.my_font.render(self.window, str(self.lives), (120, 35), scale=3)
        self.my_font.render(self.window, str(self.money), (350, 27), scale=2.5)
        # Display rounds number
        self.my_font.render(self.window, "ROUND", (580, 24), scale=3)
        self.my_font.render(self.window, str(self.round), (770, 24), scale=3)

        # Display exit menu if active
        if self.exit_menu_active:
            self.window.blit(self.exit_menu_bg, (self.game_width // 2 - 250, self.height // 2 - 75))
            self.window.blit(self.exit_btn, (self.game_width // 2 - 195, self.height // 2 - 33))
            self.window.blit(self.continue_btn, (self.game_width // 2 + 20, self.height // 2 - 33))
            self.my_font.render(self.window, "EXIT", (self.game_width // 2 - 145, self.height // 2 - 10), scale=2)
            self.my_font.render(self.window, "CONTINUE", (self.game_width // 2 + 45, self.height // 2 - 7), scale=1.5)

        pygame.display.update()


tower_game = Game()
tower_game.run()
