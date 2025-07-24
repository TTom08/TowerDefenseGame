import pygame


def clip(surf, x, y, x_size, y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x, y, x_size, y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()  # Return a copy of the clipped surface


class Font:
    def __init__(self, path):
        self.spacing = 1
        self.character_order = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        font_img = pygame.image.load(path).convert_alpha()
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            char = font_img.get_at((x, 0))
            if char[0] == 127:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                self.characters[self.character_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1

    def render(self, surf, text, loc):
        x_offset = 0
        for char in text:
            surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
            x_offset += self.characters[char].get_width() + self.spacing
