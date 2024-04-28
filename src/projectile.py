import pygame
import math
from monsters import Monster
from pygame.locals import *

class Projectile(Monster):
    def __init__(self, spawnCoords: tuple[int, int], targetCoords: tuple[int, int], walls=None):
        super().__init__("projectile", walls, spawnCoords, targetCoords)
        self.speed = 5  # Adjust speed as needed
        self.distance_traveled = 0
        self.max_distance = 300  # Maximum distance the projectile can travel

    def update(self, pressed_keys):
        # Update position based on speed and direction
        self.rect.x += self.speed * math.cos(math.radians(self.angle))
        self.rect.y += self.speed * math.sin(math.radians(self.angle))

        # Update distance traveled
        self.distance_traveled += self.speed

        # Check if the projectile has reached maximum distance
        if self.distance_traveled >= self.max_distance:
            self.kill()

        # Check for collisions with walls
        collide_list = pygame.sprite.spritecollide(self, self.walls, False)
        if collide_list:
            self.kill()

        # Check for collisions with other sprites
        self.handle_collision(None, None)  # Passing None as arguments for projectile_sprite_group and explosion_animation_group