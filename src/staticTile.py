import pygame
from pygame.locals import *
import random

class staticTile(pygame.sprite.Sprite):
    def __init__(self, enemySpawn=False, 
                 default: bool = False, treasure: bool = False, 
                 gem: bool = False, empty:bool = False, grass:bool = False, 
                 backgroundEmpty: bool = False,
                 boundary:bool=False, coords:tuple[int, int] = (0,0)):
        super().__init__()
        self.enemySpawn = enemySpawn
        self.default = default
        self.treasure = treasure
        self.gem = gem
        self.empty = empty
        self.backgroundEmpty = backgroundEmpty
        self.grass = grass
        self.coords = coords
        self.boundary = boundary
    
        self.debugColor = None
        self.collision = False
        self.image = pygame.Surface((36, 36), pygame.SRCALPHA)

        spriteSheet = pygame.image.load('assets/dirtTilesOverdraw.png').convert_alpha()
        self.sprites = []
        for col in range(5):
            self.sprites.append(spriteSheet.subsurface((col * 36, 0, 36, 36)))

        if enemySpawn == "lightGhost":
            self.debugColor = (192, 192, 192)
            self.image = self.sprites[random.randint(1,2)]
        if enemySpawn == "heavyGhost":
            self.debugColor = (255, 0, 0)
        if default:
            self.collision = True
            self.debugColor = (139, 69, 19)
            self.image = self.sprites[random.randint(1,2)]
        if treasure:
            self.debugColor = (255, 255, 0)
        if gem:
            self.collision = True
            self.debugColor = (255, 0, 255)
            self.image = self.sprites[random.randint(3,4)]
        if empty:
            self.debugColor = (0, 0, 0, 0)
        if grass:
            self.collision = True
            self.debugColor = (0, 255, 0)
            self.image = self.sprites[0]
        if boundary:
            self.collision = True
            self.debugColor = (0, 0, 0, 0)
        if backgroundEmpty:
            self.debugColor = False

        

        # self.image = pygame.Surface((36, 36))
        self.rect = self.image.get_rect()
        # self.image.fill(self.debugColor)

        # Create a smaller rect centered within the larger rect
        small_rect = pygame.Rect((0, 0), (32, 32))
        small_rect.center = self.rect.center
        self.rect = small_rect

            
        # self.rect.topleft = self.coords
        # self.rect = self.image.get_rect()
        # self.rect.x, self.rect.y = self.coords
        # print(self.rect.topleft, self.coords, self.grass, self.empty)

    # Handles logic for destroying a tile
    # Returns points to add, 'monster' type to spawn, and coordinates to spawn it
    def destroyTile(self):
        # print(self.debugColor)
        monsterSpawn = False
        points = 0
        if self.gem:  
            monsterSpawn = "gem"

        if not (self.empty or self.backgroundEmpty or self.boundary):
            points = 10
            self.empty = True
            self.grass = False
            self.default = False
            self.gem = False
            self.image=None
            super().kill()
        return monsterSpawn, points
            
    def update(self, yOffset):
        # print(self.rect.x, self.rect.y)
        self.rect.x = self.coords[0]
        self.rect.y = self.coords[1] + yOffset
        


        
        
        
            
        