import pygame
import math

class Enemy:
    imgs = []

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_count = 0
        self.health = 1
        self.path = [(1053, 16), (1056, 61), (1055, 116), (1066, 183), (1050, 254), (1007, 283), (893, 275), (798, 276), (643, 271), (489, 277), (334, 275), (229, 282), (180, 280), (147, 307), (155, 350), (173, 400), (181, 456), (193, 543), (203, 612), (213, 693), (220, 749), (263, 770), (347, 775), (429, 780), (524, 783), (616, 792), (705, 795), (751, 777), (763, 712), (772, 617), (786, 555), (850, 538), (970, 541), (1050, 545), (1105, 551), (1111, 618), (1104, 695), (1114, 754), (1153, 775), (1210, 786), (1257, 787)]
        self.img = None
        self.vel = 3
        self.path_pos = 0
        self.move_count = 0
        self.move_distance = 0

    def draw(self, win):
        self.animation_count += 1
        self.img = self.imgs[self.animation_count]

        if self.animation_count >= len(self.imgs):
            self.animation_count = 0

        win.blit(self.img, (self.x, self.y))
        self.move()

    def collide(self, X, Y):
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def move(self, change):
        x1,y1 = self.path[self.path_pos]
        if self.path_pos + 1 >=  len(self.path):
            x2, y2 = (1240,800)
        else:
            x2, y2 = self.path[self.path_pos + 1]

        move_distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        self.move_count += 1
        dirn = (x2 - x1, y2 - y1)

        move_x, move_y = (self.x + dirn[0] * self.move_count, self.y + dirn[1] * self.move_count)
        self.dis += math.sqrt((move_x - x1) ** 2 + (move_y - y1) ** 2)

        if self.dis >= move_distance:
            self.dis = 0
            self.move_count = 0
            self.path_pos += 1

        self.x = move_x
        self.y = move_y


    def hit(self):
        self.health == 1
        if self.health <= 0:
            return True