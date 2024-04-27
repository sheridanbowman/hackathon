import pygame
import math
from src.background import BackgroundImage, initBackgroundTileGroup
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
firstChunk = createCustomChunk()
chunkList = []
chunkList.append(firstChunk)

# Demo of procedural level at depth X>0 
# depth = 1
# testChunk = createProceduralChunk(depth) 

# chunkBG = pygame.image.load("assets/FREE_Fantasy Forest/Sky.png")
# stretched_image = pygame.transform.scale(chunkBG, (300, 300))


class Collisions:
    @staticmethod
    def check_collision(sprite,group):
        #checks collision between sprites
        collisions = pygame.sprite.spritecollide(sprite,group, False)
        return collisions
    @staticmethod
    def check_wall_collision(sprite, wall_group):
        #checks collision between sprite and walls.
        collisions = pygame.sprite.spritecollide(sprite, wall_group, False)
        for wall in collisions:
            if pygame.sprite.collide_rect(sprite, wall):
                if sprite.rect.bottom > wall.rect.top and sprite.rect.top < wall.rect.bottom:
                    if sprite.rect.right > wall.rect.left and sprite.rect.left < wall.rect.right:
                        # Collision will be handled.
                        sprite.handle_collision(wall)

    @staticmethod
    def check_projectile_collision(projectile, target_group):
        #checks collision between projectiles and targets
        collisions = pygame.sprite.spritecollide(projectile, target_group, False)
        for target in collisions:
            if pygame.sprite.collide_rect(projectile, target):
                # Collision are handled
                projectile.handle_collision(target)

class Projectile(pygame.sprite.Sprite):
    def handle_collision(self, collided_sprite):
        # method to handle collisions with another sprite (tiles or enemy)
        pass


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])

        self.image.fill((50, 50, 255))
        self.rect = self.image.get_rect()

        self.rect.y = y
        self.rect.x = x

clock = pygame.time.Clock()

background_list = initBackgroundTileGroup(screenWidth=WIDTH)

tile_list = pygame.sprite.Group()
for tile in firstChunk.getTiles():
    if not tile.backgroundEmpty:
        tile_list.add(tile)

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


wall1 = Wall(0, 300, 3000, 20)
wall_list.add(wall1)
all_sprite_list.add(wall1)

for monster in firstChunk.enemySpawns:
    monster.walls = wall_list
    all_sprite_list.add(monster)

# wall2 = Wall(HEIGHT-40, 200, 3000, 20)
# wall_list.add(wall2)
# all_sprite_list.add(wall2)
playerTank.walls = wall_list

player_width = 50
player_height = 50

running = True
while running == True:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.fill((255, 255, 255))

    background_list.update(globalOffset-100)
    background_list.draw(screen)

    tile_list.update(globalOffset)
    tile_list.draw(screen)

    # Check if deep enough to load new chunk
    # Compares against # of prev chunks loaded, 33% of latest
    depth = len(chunkList)
    if (playerTank.rect.y - globalOffset) > ((depth-1) + 0.33)*CHUNK_HEIGHT*TILE_PX_SIZE:
        newChunk = createProceduralChunk(depth=depth)
        chunkList.append(newChunk)
        tile_list.add(newChunk.getTiles())

        for monster in newChunk.enemySpawns:
            monster.walls = wall_list
            all_sprite_list.add(monster)
        
    m1Click = False
    m2Click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click is inside the sprite's rect
            m1Click = True

    
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
    # screen.blit(stretched_image, (0, 0-camera_y))

    # draw all tiles in all chunks 
    #TODO: only draw tiles in (n-1, n, n+1) chunks
    #have to either keep collisions for all tiles forever
    #or kill enemies off screen; or they'll drop to top of current chunk
    #and clip through 
    for chunk in chunkList:
        for tileInstance in chunk.getTiles():
            # Camera bounds
            if (tileInstance.coords[1]-camera_y > 0-TILE_PX_SIZE) and (tileInstance.coords[1]-camera_y < HEIGHT+TILE_PX_SIZE):
                color = tileInstance.debugColor
                if tileInstance.rect.collidepoint((mouse_x, mouse_y))and m1Click:
                    tileInstance.destroyTile()
                # if color:
                    # pygame.draw.rect(screen, color, (tileInstance.coords[0], tileInstance.coords[1]-camera_y, TILE_PX_SIZE, TILE_PX_SIZE))
        # Debug: draw monster spawns
        # for monsterInstance in chunk.enemySpawns:
        #     # print(monsterInstance.debugColor, monsterInstance.spawnCoords, monsterInstance.monsterType)
        #     pygame.draw.rect(screen, monsterInstance.debugColor, (monsterInstance.spawnCoords[0], monsterInstance.spawnCoords[1]-camera_y, TILE_PX_SIZE-3, TILE_PX_SIZE-3))
    
    for projectile in projectile_list:
        #need to add projectile list
        Collisions.check_projectile_collision(projectile, wall_list)
        Collisions.check_projectile_collision(projectile, enemy_list)
        #need to add enemy list
    
    
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