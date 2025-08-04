import pygame
import math


class Enemy:
    """
    Enemy class that represents a generic enemy in the game.
    It handles enemy movement along a predefined path, enemy health, drawing the enemy on the screen,
    and detecting collisions with projectiles.
    """
    imgs = []

    def __init__(self, assets, animation_speed=10, movement_speed=3):
        self.animation_speed = animation_speed
        self.movement_speed = movement_speed
        self.animation_count = 0
        self.health = 1
        self.value = 10
        self.alive = True
        self.path = [(1056, 16), (1055, 61), (1054, 116), (1053, 183), (1050, 254), (1007, 283), (893, 275), (798, 276),
                     (643, 271), (489, 277), (334, 275), (229, 282), (180, 280), (147, 307), (155, 350), (173, 400),
                     (181, 456), (193, 543), (203, 612), (213, 693), (220, 749), (263, 770), (347, 775), (429, 780),
                     (524, 783), (616, 792), (705, 795), (751, 777), (763, 712), (772, 617), (786, 555), (850, 538),
                     (970, 541), (1050, 545), (1105, 551), (1111, 618), (1113, 695), (1114, 754), (1153, 775),
                     (1210, 786), (1257, 787)]
        self.x, self.y = self.path[0]
        self.width = 174
        self.height = 132

        self.img = None
        self.vel = 3
        self.path_pos = 0
        self.move_count = 0
        self.move_distance = 0
        self.dis = 0
        self.y_offset = -45

        self.flip_right = False
        self.should_flip = False
        self.should_rotate = False

        self.death_particles = assets['death_particles']
        self.death_frame_duration = 3
        self.death_frame = 0
        self.death_timer = 0
        self.death_effect_playing = False
        self.finished = False

    def draw(self, window):
        """
        Draws the enemy on the given window.
        It updates the enemy's image based on the current animation frame and moves the enemy along its path by calling
        the move() method.
        Rolling and Boss enemies transform according to the path and direction of movement.
        :param window: The Pygame window where the enemy will be drawn.
        """
        # If the enemy is not alive, it plays the death effect.
        if not self.alive:
            self.play_death_particles(window)
            return

        self.img = self.imgs[self.animation_count // self.animation_speed]
        self.animation_count += 1
        if self.animation_count >= len(self.imgs) * self.animation_speed:
            self.animation_count = 0

        transformed_img = self.img
        if self.should_flip and self.flip_right:
            transformed_img = pygame.transform.flip(self.img, True, False)

        if self.should_rotate:
            x1, y1 = self.path[self.path_pos]
            x2, y2 = self.path[self.path_pos + 1]

            dx = x2 - x1
            dy = y2 - y1

            angle = math.degrees(math.atan2(-dy, dx))
            # The image is facing down so 90 degrees rotate
            angle += 90

            transformed_img = pygame.transform.rotate(self.img, angle)

            # Center the rotated image
            rect = transformed_img.get_rect(center=(self.x, self.y + self.y_offset))
            window.blit(transformed_img, rect.topleft)

        img_rect = transformed_img.get_rect()
        window.blit(transformed_img, (self.x - img_rect.width // 2, self.y - img_rect.height // 2 + self.y_offset))

        self.move()

    def collide(self, X, Y):
        """
        Checks if the enemy collides with the given coordinates (X, Y).
        :param X: The x-coordinate to check for collision.
        :param Y: The y-coordinate to check for collision.
        """
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def move(self):
        """
        Moves the enemy along its predefined path.
        """
        if self.path_pos + 1 >= len(self.path):
            return False

        x1, y1 = self.path[self.path_pos]
        x2, y2 = self.path[self.path_pos + 1]

        dir_x = x2 - x1
        dir_y = y2 - y1

        # If the enemy should flip based on direction
        if self.should_flip:
            if dir_x > 0:
                self.flip_right = True
            elif dir_x < 0:
                self.flip_right = False

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

    def take_damage(self, damage):
        """
        Reduces the enemy's health by the specified damage amount.
        If the health drops to zero or below, the enemy is marked as not alive.
        :param damage: The amount of damage to apply to the enemy's health.
        """
        self.health -= damage
        if self.health <= 0:
            self.alive = False

            self.death_frame = 0
            self.death_timer = 0
            self.finished = False

    def play_death_particles(self, window):
        """
        Plays the death particles animation.
        Each particle image is displayed for death_frame_duration frames before moving to the next.
        """
        if self.death_frame < len(self.death_particles):
            particle_img = self.death_particles[self.death_frame]

            particle_rect = particle_img.get_rect(center=(self.x, self.y + self.y_offset))
            window.blit(particle_img, particle_rect.topleft)

            self.death_timer += 1
            if self.death_timer >= self.death_frame_duration:
                self.death_timer = 0
                self.death_frame += 1
        else:
            self.finished = True
