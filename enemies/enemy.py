import pygame
import math

class Enemy:
    imgs = []

    def __init__(self, animation_speed=10, movement_speed=3):
        self.animation_speed = animation_speed
        self.movement_speed = movement_speed
        self.animation_count = 0
        self.health = 1
        self.path = [(1053, 16), (1056, 61), (1055, 116), (1066, 183), (1050, 254), (1007, 283), (893, 275), (798, 276), (643, 271), (489, 277), (334, 275), (229, 282), (180, 280), (147, 307), (155, 350), (173, 400), (181, 456), (193, 543), (203, 612), (213, 693), (220, 749), (263, 770), (347, 775), (429, 780), (524, 783), (616, 792), (705, 795), (751, 777), (763, 712), (772, 617), (786, 555), (850, 538), (970, 541), (1050, 545), (1105, 551), (1111, 618), (1104, 695), (1114, 754), (1153, 775), (1210, 786), (1257, 787)]
        self.x, self.y = self.path[0]
        self.width = 174
        self.height = 132

        self.img = None
        self.vel = 3
        self.path_pos = 0
        self.move_count = 0
        self.move_distance = 0
        self.dis = 0

    def draw(self, window):
        self.img = self.imgs[self.animation_count // self.animation_speed]
        self.animation_count += 1
        if self.animation_count >= len(self.imgs) * self.animation_speed:
            self.animation_count = 0

        img_rect = self.img.get_rect()
        # Centering image
        window.blit(self.img, (self.x - img_rect.width // 2, self.y - img_rect.height // 2 - 45))
        self.move()

    def collide(self, X, Y):
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def move(self):
        if self.path_pos + 1 >= len(self.path):
            return False

        x1, y1 = self.path[self.path_pos]
        x2, y2 = self.path[self.path_pos + 1]

        dir_x = x2 - x1
        dir_y = y2 - y1

        # Distance between path points
        distance = math.hypot(dir_x, dir_y)
        if distance == 0:
            return True

        dir_x /= distance
        dir_y /= distance

        self.x += dir_x * self.movement_speed
        self.y += dir_y * self.movement_speed

        # If the enemy has reached the next path point
        if (dir_x > 0 and self.x >= x2) or (dir_x < 0 and self.x <= x2):
            if (dir_y > 0 and self.y >= y2) or (dir_y < 0 and self.y <= y2):
                self.x = x2
                self.y = y2
                self.path_pos += 1

        return True

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            return True