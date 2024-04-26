import pygame
import spritesheet

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheet')

sprite_sheet_ghost = pygame.image.load('ghost-Sheet.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_ghost)

BG = (50, 50, 50)
#adds transparency to img
BLACK = (0, 0, 0)

#make animation list
animation_list = []
animation_steps = 4
last_update = pygame.time.get_ticks()
animation_cooldown = 100
frame = 0

for x in range(animation_steps):
    animation_list.append(sprite_sheet.get_image(x, 32, 32, 2, BLACK))

#Game Loop
run = True
while run:
    
    #to update background
    screen.fill(BG)

    #to update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list):
            frame = 0

    #show frame image
    screen.blit(animation_list[frame], (x * 72, 0))

    # screen.blit(frame_0, (0,0))
    # screen.blit(frame_1, (50,0))

    #Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
