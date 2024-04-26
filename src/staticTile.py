import pygame
from pygame.locals import *

class staticTile:
    def __init__(self, enemySpawn=False, 
                 default: bool = False, treasure: bool = False, 
                 gem: bool = False, empty:bool = False, grass:bool = False, 
                 boundary:bool=False, coords:tuple[int, int] = (0,0)):
        super().__init__()
        self.enemySpawn = enemySpawn
        self.default = default
        self.treasure = treasure
        self.gem = gem
        self.empty = empty
        self.grass = grass
        self.coords = coords
        self.boundary = boundary
    
        self.debugColor = None

        if enemySpawn == "Ghost":
            self.debugColor = (192, 192, 192)
        if enemySpawn == "Default":
            self.debugColor = (255, 0, 0)
        if default:
            self.debugColor = (139, 69, 19)
        if treasure:
            self.debugColor = (255, 255, 0)
        if gem:
            self.debugColor = (255, 0, 255)
        if empty:
            self.debugColor = False
        if grass:
            self.debugColor = (0, 255, 0)
        if boundary:
            self.debugColor = (0, 0, 0)
        
        
            
        