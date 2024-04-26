import pygame
import math
from src.staticTile import staticTile
from src.tileChunks import setChunkDims, createProceduralChunk, createCustomChunk
from src.tank import Tank
from pygame.locals import *

# Constants for display. Make sure dims are divisible by tile px size!
WIDTH = 800
HEIGHT = 1000
TILE_PX_SIZE = 32

# Pass global info into tileChunks, set internal global vars in tilechunks.py
CHUNK_HEIGHT, CHUNK_WIDTH = setChunkDims(WIDTH, HEIGHT, TILE_PX_SIZE)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('My Game')

# Demo of start level
chunkList = []
chunkList.append(createCustomChunk())

# Demo of procedural level at depth X>0 
# depth = 1
# testChunk = createProceduralChunk(depth) 

chunkBG = pygame.image.load(chunkList[0].backgroundImage)
stretched_image = pygame.transform.scale(chunkBG, (WIDTH, 300))

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])

        self.image.fill((50, 50, 255))
        self.rect = self.image.get_rect()

        self.rect.y = y
        self.rect.x = x


clock = pygame.time.Clock()

all_sprite_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()

# sprite.Group() lets you use the collide function as detailed above.
# It also allows you to call the update() function for all the sprites
# at once

playerTank = Tank(50, 50)
all_sprite_list.add(playerTank)

# Demo camera init, offsets all items Y values based on playerTank pos 
camera_x, camera_y = 0, 0
camLowerBound = HEIGHT // 2
globalOffset = 0

# Load the turret image
turret_image = pygame.image.load("assets/player.png")
turret_image = pygame.transform.scale(turret_image, (75, 50))
turret_rect = turret_image.get_rect()


wall1 = Wall(100, 0, 10, 200)
wall_list.add(wall1)
all_sprite_list.add(wall1)
playerTank.walls = wall_list

player_width = 50
player_height = 50

running = True
while running == True:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.fill((255, 255, 255))

    # Check if deep enough to load new chunk
    # Compares against # of prev chunks loaded, 33% of latest
    depth = len(chunkList)
    if (playerTank.rect.y - globalOffset) > ((depth-1) + 0.33)*CHUNK_HEIGHT*TILE_PX_SIZE:
        chunkList.append(createProceduralChunk(depth=depth))
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
    
    pressed_keys = pygame.key.get_pressed()

    all_sprite_list.update(pressed_keys)
    playerTank.update(pressed_keys)

    # Update camera offset to follow the playerTank
    camera_y = max(0, (playerTank.rect.y ) - ((camLowerBound) + globalOffset))
    if camera_y > 0:
        offset = playerTank.rect.y - camLowerBound
        playerTank.rect.y = camLowerBound
        globalOffset -= offset

    # Testing BG 
    screen.blit(stretched_image, (0, 0-camera_y))

    # draw all tiles in all chunks 
    #TODO: only draw tiles in (n-1, n, n+1) chunks
    #have to either keep collisions for all tiles forever
    #or kill enemies off screen; or they'll drop to top of current chunk
    #and clip through 
    for chunk in chunkList:
        for tileInstance in chunk.getTiles():
            color = tileInstance.debugColor
            if color:
                pygame.draw.rect(screen, color, (tileInstance.coords[0], tileInstance.coords[1]-camera_y, TILE_PX_SIZE, TILE_PX_SIZE))

    all_sprite_list.draw(screen)

    # Turret logic
    # Calculate the angle between the turret and the mouse
    angle = math.degrees(math.atan2(mouse_y - playerTank.rect.y, mouse_x - (playerTank.rect.x+16)))

    # Rotate the turret image
    rotated_turret = pygame.transform.rotate(turret_image, -angle)
    rotated_rect = rotated_turret.get_rect(center=((playerTank.rect.x+16), playerTank.rect.y))
    screen.blit(rotated_turret, rotated_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()