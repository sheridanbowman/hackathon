import pygame
from src.staticTile import staticTile
from src.tileChunks import setChunkDims, createProceduralChunk, createCustomChunk
from pygame.locals import *

# Constants for display. Make sure dims are divisible by tile px size!
WIDTH = 800
HEIGHT = 1000
TILE_PX_SIZE = 32

# Pass global info into tileChunks, to determine chunk size
setChunkDims(WIDTH, HEIGHT, TILE_PX_SIZE)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('My Game')

# Demo of start level
testChunk = createCustomChunk()

# Demo of procedural level at depth X>0 
# depth = 1
# testChunk = createProceduralChunk(depth) 

chunkBG = pygame.image.load(testChunk.backgroundImage)
stretched_image = pygame.transform.scale(chunkBG, (WIDTH, 300))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()

        self.image = pygame.image.load('assets/player.png')
        self.rect = self.image.get_rect()

        # Allows for initialization of the player onto a selected location
        self.rect.x = x
        self.rect.y = y

        self.change_x = 0
        self.change_y = 0

        self.walls = None

    def change_speed(self, x_diff, y_diff):
        self.change_x = x_diff
        self.change_y = y_diff
    
    def update(self, pressed_keys):
        not_moving = True
        if pressed_keys[K_w]:
            self.change_speed(0, -3)
            not_moving = False
        if pressed_keys[K_a]:
            self.change_speed(-3, 0)
            not_moving = False
        if pressed_keys[K_s]:
            self.change_speed(0, 3)
            not_moving = False
        if pressed_keys[K_d]:
            self.change_speed(3, 0)
            not_moving = False
        if not_moving:
            self.change_speed(0,0)

        self.rect.x += self.change_x
        collide_list = pygame.sprite.spritecollide(self, self.walls, False)

        # collide list is a list of all of the sprites that the player is 
        # currently in contact with. If they are currently touching something,
        # the following code will check if the player is moving left or right
        # and make sure that the player doesn't move into the other sprite by setting
        # the player's position to the side of the other sprite
        for wall in collide_list:
            if self.change_x > 0:
                self.rect.right = wall.rect.left
            else:
                self.rect.left = wall.rect.right

        # does the same as above, but with up and down
        self.rect.y += self.change_y
        collide_list = pygame.sprite.spritecollide(self, self.walls, False)
        for wall in collide_list:
            if self.change_y > 0:
                self.rect.bottom = wall.rect.top
            else:
                self.rect.top = wall.rect.bottom


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

player = Player(50, 50)
all_sprite_list.add(player)

# Demo camera init, offsets all items Y values based on player pos 
camera_x, camera_y = 0, 0
#todo, doesnt actually keep player in center of screen .... 

wall1 = Wall(100, 0, 10, 200)
wall_list.add(wall1)
all_sprite_list.add(wall1)

player.walls = wall_list

running = True
while running == True:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
    
    pressed_keys = pygame.key.get_pressed()

    all_sprite_list.update(pressed_keys)
    player.update(pressed_keys)

    # Update camera offset to follow the player
    camera_x = player.rect.x - WIDTH // 2
    camera_y = max(0, player.rect.y - HEIGHT // 2)

    player.rect.y -= camera_y
    
    # Testing BG 
    screen.blit(stretched_image, (0-camera_x, 0-camera_y))

    # Testing chunk
    for tileInstance in testChunk.getTiles():
        color = tileInstance.debugColor
        if color:
            pygame.draw.rect(screen, color, (tileInstance.coords[0]-camera_x, tileInstance.coords[1], TILE_PX_SIZE, TILE_PX_SIZE))

    
    all_sprite_list.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()