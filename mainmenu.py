import os
import pygame

pygame.init()
pygame.mixer.quit()

class MainMenu:
    def __init__(self, window):
        self.window = window
        self.width, self.height = window.get_size()

        self.background = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "ui", "mainmenu", "bg.png")).convert(),
            (self.width, self.height)
        )

        self.menu_bg = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "ui", "mainmenu", "mainmenu_ui_bg.png")).convert_alpha(),
            (self.width, 480)
        )

        self.exit_btn = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "ui", "mainmenu", "exitgame_btn.png")).convert_alpha(),
            (420, 90)
        )
        self.exit_btn_rect = self.exit_btn.get_rect(topleft=(500, 580))
        self.exit_btn_hover = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "ui", "mainmenu", "exitgame_btn_hover.png")).convert_alpha(),
            (420, 90)
        )
        self.play_btn = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "ui", "mainmenu", "play_btn.png")).convert_alpha(),
            (420, 90)
        )
        self.play_btn_rect = self.play_btn.get_rect(topleft=(500, 450))
        self.play_btn_hover = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "ui", "mainmenu", "play_btn_hover.png")).convert_alpha(),
            (420, 90)
        )

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            mouse_pos = pygame.mouse.get_pos()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_btn_rect.collidepoint(mouse_pos):
                        self.fade_out(self.window)
                        return "game"
                    elif self.exit_btn_rect.collidepoint(mouse_pos):
                        self.fade_out(self.window)
                        return "quit"

            self.draw()
            pygame.display.flip()

    def draw(self):
        self.window.blit(self.background, (0, 0))
        self.window.blit(self.menu_bg, (0, self.height // 2 - 240))

        mouse_pos = pygame.mouse.get_pos()
        if self.exit_btn_rect.collidepoint(mouse_pos):
            self.window.blit(self.exit_btn_hover, (500, 580))
        else:
            self.window.blit(self.exit_btn, (500, 580))

        if self.play_btn_rect.collidepoint(mouse_pos):
            self.window.blit(self.play_btn_hover, (500, 450))
        else:
            self.window.blit(self.play_btn, (500, 450))


    def fade_out(self, window, speed=10):
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