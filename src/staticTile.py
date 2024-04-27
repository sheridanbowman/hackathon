import pygame
from pygame.locals import *

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

        if enemySpawn == "lightGhost":
            self.debugColor = (192, 192, 192)
        if enemySpawn == "heavyGhost":
            self.debugColor = (255, 0, 0)
        if default:
            self.collision = True
            self.debugColor = (139, 69, 19)
        if treasure:
            self.debugColor = (255, 255, 0)
        if gem:
            self.collision = True
            self.debugColor = (255, 0, 255)
        if empty:
            self.debugColor = (0, 0, 0)
        if grass:
            self.collision = True
            self.debugColor = (0, 255, 0)
        if boundary:
            self.collision = True
            self.debugColor = (0, 0, 0)
        if backgroundEmpty:
            self.debugColor = False

        self.image = pygame.Surface((32, 32))
        self.image.fill(self.debugColor)
        self.rect = self.image.get_rect()
        # self.rect.topleft = self.coords
        # self.rect = self.image.get_rect()
        # self.rect.x, self.rect.y = self.coords
        # print(self.rect.topleft, self.coords, self.grass, self.empty)

    # Handles logic for destroying a tile
    # Returns points to add, 'monster' type to spawn, and coordinates to spawn it
    def destroyTile(self):
        monsterSpawn = False
        points = 10
        spawnCoords = False
        if self.gem:  
            monsterSpawn = "gem"
            spawnCoords = self.coords
        if not (self.empty or self.backgroundEmpty or self.boundary):
            self.empty = True
            self.grass = False
            self.default = False
            self.gem = False
            self.image.fill((0,0,0)) # <---- TODO: replace with sprite
        return monsterSpawn, points, self.coords
            
    def update(self, yOffset):
        # print(self.rect.x, self.rect.y)
        self.rect.x = self.coords[0]
        self.rect.y = self.coords[1] + yOffset
        


        
        
        
            
        