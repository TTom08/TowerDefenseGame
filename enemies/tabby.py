import os.path

import pygame

class Tabby:
    imgs = [pygame.image.load(os.path.join("assets", "enemies", f"tabby{i+1}.png")) for i in range(2)]