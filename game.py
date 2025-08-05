import math

import pygame
import random

pygame.init()
pygame.mixer.quit()

window = pygame.display.set_mode((1500, 960))

from enemies.tabby import Tabby
from enemies.black import Black
from enemies.rolling import Rolling
from enemies.boss import Boss
from towers.crossbow import Crossbow
from towers.cannon import Cannon


###
# This is a simple tower defense game where you can place towers to defend against waves of enemies.
###

class Game:
    """
    This is the main game class that handles the game loop, events, and rendering.
    """

    def __init__(self, window, assets):
        self.window = window
        self.game_width = 1280
        self.toolbar_width = 220
        self.width, self.height = window.get_size()

        self.lives = 10
        self.money = 200
        self.round = 0
        self.selected_tool = None
        self.towers = []
        self.round_active = False

        self.enemies = []
        self.upcoming_enemies = []
        self.spawn_delay = 2000
        self.spawn_delay_cap = 500
        self.last_spawn_time = 0

        self.round_start_delay = 2000
        self.round_start_time = 0
        self.auto_start = False
        self.waiting_for_start = False
        self.game_over = False
        self.boss_round = False

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
        self.selected_tower = None

        self.assets = assets

        # Game background
        self.game_background = assets['game_background']

        # Toolbar background
        self.toolbar_bg = pygame.Surface((self.toolbar_width, self.height))
        self.toolbar_bg = assets['toolbar_bg']

        # Start button
        self.start_button = assets['start_button']
        # Pause button
        self.pause_button = assets['pause_button']

        # Placement mask
        self.placement_mask = assets['placement_mask']
        # PixelArray for the placement mask to check buildable areas
        self.mask_pixels = pygame.PixelArray(self.placement_mask)

        # Statbar - lives and money
        self.statbar_bg = assets['statbar_bg']
        self.statbar_heart = assets['statbar_heart']
        self.statbar_coin = assets['statbar_coin']

        # Exit menu and its buttons
        self.exit_menu_active = False
        self.exit_menu_scale = 0.0
        self.exit_menu_target_scale = 0.0
        self.exit_menu_bg = assets['exit_menu_bg']
        self.exit_btn = assets['exit_btn']
        self.exit_btn_rect = self.exit_btn.get_rect(topleft=(self.game_width // 2 - 195, self.height // 2 - 33))
        self.continue_btn = assets['continue_btn']
        self.continue_btn_rect = self.continue_btn.get_rect(topleft=(self.game_width // 2 + 20, self.height // 2 - 33))

        # Custom font
        self.my_font = assets['my_font']
        self.messages = []

        for t in self.available_towers:
            t['rect'] = pygame.Rect(t['pos'][0], t['pos'][1], 160, 112)

        self.start_button_rect = self.start_button.get_rect(topleft=(1292, 784))

        self.enemy_types = [
            {'class': Tabby, 'min-wave': 1},
            {'class': Black, 'min-wave': 3},
            {'class': Rolling, 'min-wave': 5}
        ]
        self.enemy_type_boss = Boss

    def run(self):
        """
        Initializes the game and sets up the necessary variables and assets.
        This method is called when the game is started.
        """
        running = True
        clock = pygame.time.Clock()

        self.draw()
        pygame.display.flip()

        while running:
            mouse_pos = pygame.mouse.get_pos()
            dt = clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Checks if a tool is selected
                    for t in self.available_towers:
                        if t['rect'].collidepoint(mouse_pos):
                            self.selected_tool = t['class'] if self.selected_tool != t['class'] else None
                            break

                    # Check if a tower was clicked with left click and selects it or deselects it
                    if event.button == 1 and self.selected_tool is None:
                        for tower in self.towers:
                            if tower.click(mouse_pos[0], mouse_pos[1]):
                                self.selected_tower = tower if self.selected_tower != tower else None
                                break
                        else:
                            self.selected_tower = None

                    # Upgrade tower with right click
                    if event.button == 3 and self.selected_tower:
                        upgrade_cost = 200
                        if self.selected_tower.level < 2:
                            if self.money >= upgrade_cost:
                                self.money -= upgrade_cost
                                self.selected_tower.upgrade()
                            else:
                                self.show_message("NOT ENOUGH MONEY!", (mouse_pos[0] + 15, mouse_pos[1] - 3), duration=20)
                        else:
                            self.show_message("UPGRADED!", (mouse_pos[0] + 15, mouse_pos[1] - 3), duration=20)

                    # Starting the game - start button logic
                    if self.start_button_rect.collidepoint(mouse_pos):
                        if self.selected_tool:
                            self.show_message("TOOL IS SELECTED!", (mouse_pos[0] - 350, mouse_pos[1] - 3), duration=20)
                        else:
                            if not self.round_active and not self.waiting_for_start:
                                if self.auto_start:
                                    # Auto start enabled
                                    self.waiting_for_start = True
                                    self.round_start_time = pygame.time.get_ticks()
                                else:
                                    # Manual start
                                    self.round += 1
                                    self.upcoming_enemies = self.generate_wave(self.round)
                                    self.last_spawn_time = pygame.time.get_ticks()
                                    self.round_active = True

                            # Switching between auto start mode
                            self.auto_start = not self.auto_start
                    else:
                        # Place tower on map if the area is buildable
                        if self.selected_tool and mouse_pos[0] < self.game_width:
                            if self.is_buildable(mouse_pos[0], mouse_pos[1]) and not self.is_overlapping(mouse_pos[0],
                                                                                                         mouse_pos[1]):
                                if (self.money - self.selected_tool.price if self.selected_tool else 0) >= 0:
                                    self.towers.append(self.selected_tool(mouse_pos[0], mouse_pos[1]))
                                    self.money -= self.selected_tool.price
                                    self.selected_tool = None
                                else:
                                    self.show_message("NOT ENOUGH MONEY!", (mouse_pos[0] + 15, mouse_pos[1] - 3),
                                                      duration=20)
                            else:
                                self.show_message("INVALID BUILD LOCATION!", (mouse_pos[0] + 15, mouse_pos[1] - 3),
                                                  duration=20)

                    # Handles exit menu interactions
                    if self.exit_menu_scale > 0.95:
                        if self.exit_btn_rect.collidepoint(mouse_pos):
                            self.fade_out(window)
                            return "menu"
                        elif self.continue_btn_rect.collidepoint(mouse_pos):
                            self.exit_menu_active = False
                            self.exit_menu_target_scale = 0.0

                # Show exit menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.exit_menu_active = not self.exit_menu_active
                        self.exit_menu_target_scale = 1.0 if self.exit_menu_active else 0.0

                # Sell the selected tower
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        if self.selected_tower:
                            self.money += self.selected_tower.sell_price
                            self.towers.remove(self.selected_tower)
                            self.selected_tower = None

                # Restart the game if game over
                if self.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    return "restart"
                # Exit to main menu if game over
                elif self.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.fade_out(self.window)
                    return "menu"

            # Iterate through enemies - to list
            to_delete = []
            for e in self.enemies:
                if e.path_pos >= len(e.path) - 1:
                    to_delete.append(e)

            for tower in self.towers:
                tower.update(dt, self.enemies)

            # Remove dead enemies
            dead_enemies = [e for e in self.enemies if not e.alive and e.finished]
            for enemy in dead_enemies:
                self.enemies.remove(enemy)
                self.money += enemy.value

            # Delete enemy once its off screen
            for d in to_delete:
                self.enemies.remove(d)
                if not self.game_over:
                    if isinstance(d, Tabby):
                        self.lives -= 1
                    elif isinstance(d, Black):
                        self.lives -= 2
                    elif isinstance(d, Rolling):
                        self.lives -= 3
                    elif isinstance(d, Boss):
                        self.lives -= 5

            if self.lives < 0:
                self.lives = 0

            if self.lives <= 0 and not self.game_over:
                self.game_over = True
                self.auto_start = False

            # If auto start is enabled, automatically start the next round delayed
            if self.waiting_for_start:
                if pygame.time.get_ticks() - self.round_start_time >= self.round_start_delay:
                    self.round += 1
                    self.upcoming_enemies = self.generate_wave(self.round)
                    self.last_spawn_time = pygame.time.get_ticks()
                    self.round_active = True
                    self.waiting_for_start = False

            # Adding delay between enemy spawns
            if self.round_active and self.upcoming_enemies:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_spawn_time >= self.spawn_delay:
                    enemy = self.upcoming_enemies.pop(0)
                    self.enemies.append(enemy)
                    self.last_spawn_time = current_time

            # If the round is over (no more enemies), end it and prepare next if auto_start is ON
            if self.round_active and not self.upcoming_enemies and not self.enemies:
                self.round_active = False
                if self.auto_start:
                    self.waiting_for_start = True
                    self.round_start_time = pygame.time.get_ticks()
                    while self.spawn_delay == self.spawn_delay_cap:
                        self.spawn_delay -= 50

            if self.exit_menu_active:
                self.selected_tool = None

            self.draw()
            pygame.display.flip()

        return "menu"

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

    def generate_wave(self, wave_num):
        """
        Generates a wave of enemies based on the current wave number.
        :param wave_num: The current wave number.
        :return: A list of enemy instances for the current wave.
        """
        wave_enemies = []
        num_enemies = 5 + wave_num * 2
        boss_num_enemies = 1 + math.floor(wave_num * 0.25)

        self.boss_round = (wave_num % 10 == 0)

        if self.boss_round:
            for _ in range(boss_num_enemies):
                wave_enemies.append(self.enemy_type_boss(self.assets))
        else:
            available_enemies = [e['class'] for e in self.enemy_types if wave_num >= e['min-wave']]
            if not available_enemies:
                available_enemies = [self.enemy_types[0]['class']]
            for _ in range(num_enemies):
                enemy_class = random.choice(available_enemies)
                wave_enemies.append(enemy_class(self.assets))

        return wave_enemies

    def draw(self):
        """
        Displays the game window and draws all the game elements such as towers, enemies, and UI.
        """
        self.window.blit(self.game_background, (0, 0))

        for tower in self.towers:
            tower.draw(self.window)

        for e in self.enemies:
            e.draw(self.window)

        self.window.blit(self.toolbar_bg, (self.game_width, 0))

        for t in self.available_towers:
            self.window.blit(t['icon'], t['pos'])
            if self.selected_tool == t['class']:
                self.window.blit(t['highlight'], t['pos'])

        # Draw preview image of the tower whle hovering over the game area
        if self.selected_tool:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x < self.game_width:
                preview_tower = self.selected_tool(mouse_x, mouse_y)
                preview_img = preview_tower.tower_imgs[0][0].copy()
                if self.is_buildable(mouse_x, mouse_y) and not self.is_overlapping(mouse_x, mouse_y):
                    preview_img.set_alpha(128)
                else:
                    overlay = pygame.Surface(preview_img.get_size(), pygame.SRCALPHA)
                    overlay.fill((255, 0, 0, 128))
                    preview_img.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
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
        button_img = self.pause_button if self.auto_start else self.start_button
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

        self.draw_exit_menu()

        for msg in self.messages[:]:
            if msg['duration'] > 0:
                self.my_font.render(self.window, msg['text'], msg['pos'], scale=2, alpha=msg['alpha'])
                msg['duration'] -= 1
            else:
                msg['alpha'] -= msg['fade_speed']
                if msg['alpha'] <= 0:
                    self.messages.remove(msg)
                    continue
                self.my_font.render(self.window, msg['text'], msg['pos'], scale=2, alpha=msg['alpha'])

        # If the game is over, display the game over screen
        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((50, 50, 50, 180))
            self.window.blit(overlay, (0, 0))

            self.my_font.render(self.window, "GAME OVER", (self.game_width // 2 - 150, self.height // 2 - 50), scale=4)
            self.my_font.render(self.window, "PRESS R TO RESTART", (self.game_width // 2 - 140, self.height // 2 + 20),
                                scale=2)
            self.my_font.render(self.window, "PRESS ESC TO EXIT TO MAIN MENU",
                                (self.game_width // 2 - 110, self.height // 2 + 200), scale=1)

        # Draw range circle around the selected tower
        if self.selected_tower:
            scaled_range_circle = pygame.transform.scale(
                self.selected_tower.tower_range_circle,
                (self.selected_tower.range * 2, self.selected_tower.range * 2)  # Double the range for diameter
            )
            self.window.blit(scaled_range_circle,
                             (self.selected_tower.x - self.selected_tower.range,
                              self.selected_tower.y - self.selected_tower.range))

        if self.selected_tower is not None:
            self.my_font.render(self.window, "PRESS RIGHT MOUSE BUTTON TO UPGRADE", (75, 880), scale=3)
            self.my_font.render(self.window, "PRESS X TO SELL", (550, 930), scale=1.5)

    def draw_exit_menu(self):
        """
        Draws the exit menu with buttons to exit or continue the game.
        """
        # Display exit menu with transition
        scale_speed = 0.3
        if self.exit_menu_scale < self.exit_menu_target_scale:
            self.exit_menu_scale += (self.exit_menu_target_scale - self.exit_menu_scale) * scale_speed
        elif self.exit_menu_scale > self.exit_menu_target_scale:
            self.exit_menu_scale -= (self.exit_menu_scale - self.exit_menu_target_scale) * scale_speed

        if self.exit_menu_scale > 0 and not self.game_over:
            scale = self.exit_menu_scale
            base_x = self.game_width // 2
            base_y = self.height // 2

            # exit menu
            scaled_bg = pygame.transform.smoothscale(self.exit_menu_bg, (int(500 * scale), int(150 * scale)))
            bg_rect = scaled_bg.get_rect(center=(base_x, base_y))
            self.window.blit(scaled_bg, bg_rect.topleft)

            # exit button
            scaled_exit_btn = pygame.transform.smoothscale(self.exit_btn, (int(175 * scale), int(66 * scale)))
            exit_rect = scaled_exit_btn.get_rect(center=(base_x - 110 * scale, base_y))
            self.window.blit(scaled_exit_btn, exit_rect.topleft)

            # continue button
            scaled_continue_btn = pygame.transform.smoothscale(self.continue_btn, (int(175 * scale), int(66 * scale)))
            cont_rect = scaled_continue_btn.get_rect(center=(base_x + 110 * scale, base_y))
            self.window.blit(scaled_continue_btn, cont_rect.topleft)

            # exit and continue button texts
            self.my_font.render(self.window, "EXIT", (base_x - 145 * scale, base_y - 10 * scale), scale=scale * 2)
            self.my_font.render(self.window, "CONTINUE", (base_x + 50 * scale, base_y - 10), scale=scale * 1.5)

    def show_message(self, text, pos, duration=60, fade_speed=8):
        """
        Displays a message on the screen for a specified duration.
        :param text: The message to display.
        :param pos: (x, y) position on screen.
        :param duration: How long to show the message (in frames).
        """
        self.messages.append({
            'text': text,
            'pos': pos,
            'alpha': 255,
            'duration': duration,
            'fade_speed': fade_speed
        })

    def fade_out(self, window, speed=10):
        """
        Fades out the game window to black.
        :param window: The Pygame window to fade out.
        :param speed: The speed of the fade effect (default is 10).
        """
        fade = pygame.Surface(window.get_size()).convert_alpha()
        fade.fill((0, 0, 0, 0))
        clock = pygame.time.Clock()

        alpha = 0
        while alpha < 255:
            self.draw()
            alpha = min(255, alpha + speed)
            fade.fill((0, 0, 0, alpha))
            window.blit(fade, (0, 0))
            pygame.display.flip()
            clock.tick(60)

    def fade_in(self, window, speed=5):
        """
        Fades in the game window to black.
        :param window: The Pygame window to fade in.
        :param speed: The speed of the fade effect (default is 5).
        """
        fade = pygame.Surface(window.get_size()).convert_alpha()
        fade.fill((0, 0, 0, 255))
        clock = pygame.time.Clock()

        alpha = 255
        while alpha > 0:
            self.draw()
            alpha = max(0, alpha - speed)
            fade.fill((0, 0, 0, alpha))
            window.blit(fade, (0, 0))
            pygame.display.flip()
            clock.tick(60)
