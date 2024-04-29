import pygame
from pygame.locals import *
from src.monsters import Monster



class Projectile(Monster):
    def __init__(self, spawnCoords: tuple[int, int], walls: pygame.sprite.Group, direction: tuple[int, int], angle: float):
        super().__init__("projectile", walls, spawnCoords)
        self.moveType = "flyToTarget"
        self.direction = direction
        self.image = pygame.Surface((10, 10))  # Placeholder surface, adjust size as needed
        self.image.fill((255, 255, 255))  # Placeholder color, adjust as needed
        self.rect = self.image.get_rect(center=spawnCoords)
        self.angle = angle

    def update(self, pressed_keys):
        # Update projectile position based on direction

        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]

        super().update(pressed_keys)