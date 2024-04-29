import pygame
from monsters import Monster
from pygame.locals import *

class Projectile(Monster):
    def __init__(self, spawnCoords: tuple[int, int], walls: pygame.sprite.Group, direction: tuple[int, int]):
        super().__init__("projectile", walls, spawnCoords)
        self.moveType = "flyToTarget"
        self.direction = direction

    def update(self, pressed_keys):
        # Update projectile position based on direction
        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]

        # Check for collision with walls
        collide_list = pygame.sprite.spritecollide(self, self.walls, False)
        for wall in collide_list:
            # Adjust position if collision occurs
            if self.direction[0] > 0:  # Moving right
                self.rect.right = wall.rect.left
            elif self.direction[0] < 0:  # Moving left
                self.rect.left = wall.rect.right

            if self.direction[1] > 0:  # Moving down
                self.rect.bottom = wall.rect.top
            elif self.direction[1] < 0:  # Moving up
                self.rect.top = wall.rect.bottom