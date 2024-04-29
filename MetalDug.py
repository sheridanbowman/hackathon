import pygame
import math
import sys
from src.playerHealth import PlayerHealth
from src.monsters import Monster
from src.background import BackgroundImage, newCaveTileRow, initSurfaceBackgroundTileGroup
from src.staticTile import staticTile
from src.tileChunks import setChunkDims, createProceduralChunk, createCustomChunk
from src.score import ScoreCounter
from src.tank import Tank
from pygame.locals import *

# Constants for display. Make sure dims are divisible by tile px size!
# WIDTH = 800/1.5
# HEIGHT = 1000/1.5
WIDTH = 800 
HEIGHT = 1000
TILE_PX_SIZE = 32

clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.Font("assets/m5x7/m5x7.ttf", 36)

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])

        self.image.fill((50, 50, 255))
        self.rect = self.image.get_rect()

        self.rect.y = y
        self.rect.x = x

# Pass global info into tileChunks, set internal global vars in tilechunks.py
CHUNK_HEIGHT, CHUNK_WIDTH = setChunkDims(WIDTH, HEIGHT, TILE_PX_SIZE)

screen = pygame.display.set_mode([800, 1000])
pygame.display.set_caption('METAL DUG')

def retryState(countdown):
    # Get the text surface
    text_surface = font.render("CONTINUE?", True, (255, 255, 255))
    text_rect = text_surface.get_rect()

    text_rect.center = screen.get_rect().center

    screen.blit(text_surface, text_rect)

    # Check if countdown is provided and less than or equal to 0
    if countdown <= 0:
        pygame.quit()
        sys.exit()

    countdown_surface = font.render(str(countdown), True, (255, 255, 255))
    countdown_rect = countdown_surface.get_rect()
    countdown_rect.midtop = (text_rect.centerx, text_rect.bottom + 10)
    screen.blit(countdown_surface, countdown_rect)

    # "Retry" prompt
    retry_text = ">INSERT COIN?<"
    retry_surface = font.render(retry_text, True, (255, 255, 255))
    retry_rect = retry_surface.get_rect()
    retry_rect.midtop = (text_rect.centerx, countdown_rect.bottom + 10)
    screen.blit(retry_surface, retry_rect)

    pygame.display.flip()

    # Return the rectangle coordinates of the "RETRY" text
    return retry_rect
    


# # Groups to update
# tile_list = pygame.sprite.Group()
# all_sprite_list = pygame.sprite.Group()
# wall_list = pygame.sprite.Group()

# # Initialize score counter
# score = ScoreCounter(xPos=0,yPos=0,initialScore=0)

# # Load first chunk
# firstChunk = createCustomChunk()
# chunkList = []
# chunkList.append(firstChunk)

# # add tiles to be updated
# for tile in firstChunk.getTiles():
#     if not (tile.backgroundEmpty or tile.empty):
#         tile_list.add(tile)

# # Add monsters to spawn
# for monster in firstChunk.enemySpawns:
#     monster.walls = wall_list
#     all_sprite_list.add(monster)

# # Demo of procedural level at depth X>0 
# # depth = 1
# # testChunk = createProceduralChunk(depth) 

# # chunkBG = pygame.image.load("assets/FREE_Fantasy Forest/Sky.png")
# # stretched_image = pygame.transform.scale(chunkBG, (300, 300))


# # Add the surface background image, start the cave background images 
# background_list = pygame.sprite.Group()
# background_list.add(initSurfaceBackgroundTileGroup(screenWidth=WIDTH))
# caveTileCount = 0
# for _ in range(math.ceil(HEIGHT/224)+1):
#     background_list.add(newCaveTileRow(screenWidth=WIDTH, screenHeight=HEIGHT, depth=caveTileCount))
#     caveTileCount +=1

# # sprite.Group() lets you use the collide function as detailed above.
# # It also allows you to call the update() function for all the sprites
# # at once

# playerTank = Tank(50, 50, WIDTH, HEIGHT)
# all_sprite_list.add(playerTank)

# # Demo camera init, offsets all items Y values based on playerTank pos 
# camera_x, camera_y = 0, 0
# camLowerBound = HEIGHT // 2
# globalOffset = 0


# demowalls = [Wall(0, 300, 3000, 20), Wall(0, 900, 3000, 20), Wall(WIDTH-50, 0, 20, 3000), Wall(30, 0, 20, 3000)]
# wall_list.add(demowalls)
# all_sprite_list.add(demowalls)

# health = PlayerHealth(HEIGHT)

# all_sprite_list.add(health)

# playerTank.walls = wall_list


def loadGame():
    gameOver = False
    screen = pygame.display.set_mode([800, 1000])
    pygame.display.set_caption('METAL DUG')

    tile_list = pygame.sprite.Group()
    all_sprite_list = pygame.sprite.Group()
    global wall_list
    wall_list = pygame.sprite.Group()
    score = ScoreCounter(xPos=0,yPos=0,initialScore=0)
    # Load first chunk
    firstChunk = createCustomChunk()
    chunkList = []
    chunkList.append(firstChunk)
    # add tiles to be updated
    for tile in firstChunk.getTiles():
        if not (tile.backgroundEmpty or tile.empty):
            tile_list.add(tile)
            # wall_list.add(tile)
            # all_sprite_list.add(tile)

    # Add monsters to spawn
    for monster in firstChunk.enemySpawns:
        # monster.walls = wall_list
        monster.walls=tile_list
        all_sprite_list.add(monster)
    # Add the surface background image, start the cave background images 
    background_list = pygame.sprite.Group()
    background_list.add(initSurfaceBackgroundTileGroup(screenWidth=WIDTH))
    caveTileCount = 0
    for _ in range(math.ceil(HEIGHT/224)+1):
        background_list.add(newCaveTileRow(screenWidth=WIDTH, screenHeight=HEIGHT, depth=caveTileCount))
        caveTileCount +=1

    playerTank = Tank(50, 50, WIDTH, HEIGHT)
    all_sprite_list.add(playerTank)

    # Demo camera init, offsets all items Y values based on playerTank pos 
    camera_x, camera_y = 0, 0
    camLowerBound = HEIGHT // 2
    globalOffset = 0

    # demowalls = [Wall(0, 300, 3000, 20), Wall(0, 900, 3000, 20), Wall(WIDTH-50, 0, 20, 3000), Wall(30, 0, 20, 3000)]
    # wall_list.add(demowalls)
    # all_sprite_list.add(demowalls)

    health = PlayerHealth(HEIGHT)

    all_sprite_list.add(health)

    # playerTank.walls = wall_list
    playerTank.walls = tile_list

    countdown=10
    print(len(wall_list))
    return countdown, gameOver, playerTank, screen, tile_list, all_sprite_list, wall_list, background_list, chunkList, caveTileCount, health, score, camera_x, camera_y, camLowerBound, globalOffset


#load game 
countdown, gameOver, playerTank, screen, tile_list, all_sprite_list, wall_list, background_list, chunkList, caveTileCount, health, score, camera_x, camera_y, camLowerBound, globalOffset = loadGame()

timer = 0
running = True
retryRect = None

while running == True:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # mouse_x = mouse_x / 1.5
    # mouse_y = mouse_y / 1.5
    screen.fill((255, 255, 255))

    background_list.update(globalOffset)
    background_list.draw(screen)

    tile_list.update(globalOffset)
    tile_list.draw(screen)

    # DEEBUG: uncomment to see background in front of tiles
    # background_list.update(globalOffset)
    # background_list.draw(screen)

    # Check if deep enough to load new chunk
    # Compares against # of prev chunks loaded, 33% of latest
    depth = len(chunkList)
    if (playerTank.rect.y - globalOffset) > ((depth-1) + 0.33)*CHUNK_HEIGHT*TILE_PX_SIZE:
        newChunk = createProceduralChunk(depth=depth)
        chunkList.append(newChunk)
        for tile in newChunk.getTiles():
            if not (tile.backgroundEmpty or tile.empty):
                tile_list.add(tile)
                # wall_list.add(tile)

        for monster in newChunk.enemySpawns:
            monster.walls = tile_list
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
            if event.button == 1:  # Left mouse button (m1) click
                # Check if the mouse click is inside the sprite's rect
                m1Click = True
            if event.button == 3:  # Right mouse button (m2) click
                m2Click = True
                health.update_health(health.health-1)
            


    pressed_keys = pygame.key.get_pressed()
    
    if not gameOver:
        all_sprite_list.update(pressed_keys=pressed_keys, globalOffset=globalOffset)
        playerTank.update(pressed_keys)

    # Update camera offset to follow the playerTank
    camera_y = max(0, (playerTank.rect.y ) - ((camLowerBound) + globalOffset))
    if camera_y > 0:
        offset = playerTank.rect.y - camLowerBound
        playerTank.rect.y = camLowerBound
        globalOffset -= offset

    if globalOffset < (((caveTileCount-1) * -224)+500):
        background_list.add(newCaveTileRow(screenWidth=WIDTH, screenHeight=HEIGHT, depth=caveTileCount))
        caveTileCount+=1
    # Testing BG 
    # screen.blit(stretched_image, (0, 0-camera_y))

    # draw all tiles in all chunks 
    #TODO: only draw tiles in (n-1, n, n+1) chunks
    #have to either keep collisions for all tiles forever
    #or kill enemies off screen; or they'll drop to top of current chunk
    #and clip through 
    
    monsterSpawn = False
    for chunk in chunkList:
        for tileInstance in chunk.getTiles():
            # Camera bounds
            if (tileInstance.coords[1]-camera_y > 0-TILE_PX_SIZE) and (tileInstance.coords[1]-camera_y < HEIGHT+TILE_PX_SIZE):
                color = tileInstance.debugColor
                if tileInstance.rect.collidepoint((mouse_x, mouse_y)) and m1Click:
                    monsterSpawn, points = tileInstance.destroyTile()
                    score.addScore(points)
                    if monsterSpawn:
                        print(len(tile_list))
                        newGem = Monster(monsterType="lightGhost", spawnCoords=(tileInstance.coords[0],tileInstance.coords[1]), walls=tile_list)
                        newGem.update()
                        all_sprite_list.add(newGem)
                        # Spawn monster
                # if color:
                    # pygame.draw.rect(screen, color, (tileInstance.coords[0], tileInstance.coords[1]-camera_y, TILE_PX_SIZE, TILE_PX_SIZE))
        # Debug: draw monster spawns
        # for monsterInstance in chunk.enemySpawns:
        #     # print(monsterInstance.debugColor, monsterInstance.spawnCoords, monsterInstance.monsterType)
        #     pygame.draw.rect(screen, monsterInstance.debugColor, (monsterInstance.spawnCoords[0], monsterInstance.spawnCoords[1]-camera_y, TILE_PX_SIZE-3, TILE_PX_SIZE-3))
    
    # for projectile in projectile_list:
    #     #need to add projectile list
    #     Collisions.check_projectile_collision(projectile, wall_list)
    #     Collisions.check_projectile_collision(projectile, enemy_list)
    #     #need to add enemy list
    
    
    all_sprite_list.draw(screen)


    # ======================= Screen Score =======================
    score.update(globalOffset)
    # xShake, yShake = score.getShake()
    xShake, yShake = 0, 0
    scoreText = font.render(str(score.delayedScore), True, (255,255,255))
    scoreText_rect = scoreText.get_rect(topright=(WIDTH - 10+xShake, (10+yShake)))

    # Draw scoreText on screen
    screen.blit(scoreText, scoreText_rect)


    # ======================= GAME OVER screen =======================
    # flag to stop updating sprites etc
    if health.health == 0:
        gameOver = True

    # Render game over text, reload game if player clicks to 'insert coin'  
    if gameOver:        
        timer +=1
        retryRect = retryState(countdown)

        if retryRect is not None:
            if retryRect.collidepoint((mouse_x, mouse_y)) and m1Click:
                countdown, gameOver, playerTank, screen, tile_list, all_sprite_list, wall_list, background_list, chunkList, caveTileCount, health, score, camera_x, camera_y, camLowerBound, globalOffset = loadGame()

        if timer > 100:
            # Decrease the countdown
            countdown -= 1
            timer=0

        continue


    # ======================= Turret Logic =======================
    # Calculate the angle between the turret and the mouse (int offsets for center)
    angle = math.degrees(math.atan2(mouse_y - playerTank.rect.y-18, mouse_x - (playerTank.rect.x+16)))

    # Rotate the turret image
    rotated_turret = pygame.transform.rotate(playerTank.turret_image, -angle)
    rotated_rect = rotated_turret.get_rect(center=((playerTank.rect.x+16), playerTank.rect.y+18))
    screen.blit(rotated_turret, rotated_rect)

    # ======================= Tank Head 'Logic' =======================
    # Rotate the literal BG sprite for tank head
    tankHeadBg = pygame.transform.rotate(playerTank.head_bg, -angle)
    masked_sprite_image = tankHeadBg.copy()

    # Rescale the mask to the new dims of tank head bg (Sprite will rotate internally and persistantly point to a bounding rect set of coords)
    resized_mask = pygame.transform.scale(playerTank.head_mask, (masked_sprite_image.get_width(), masked_sprite_image.get_height()))
    
    # Draw the mask onto the sprite BG 
    masked_sprite_image.set_colorkey((0, 0, 0))
    masked_sprite_image.blit(resized_mask, (0,0), special_flags=pygame.BLEND_RGBA_MULT)

    # Draw the whole thing
    screen.blit(masked_sprite_image, rotated_rect)


    # ======================= Screen Resize =======================
    # Resize image for zoom in, reset width highet to /1.5, draw screen to real diims
    # scaled_surface = pygame.transform.scale(screen, (800 * 1.5, 1000 * 1.5))
    # screen.blit(scaled_surface, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()