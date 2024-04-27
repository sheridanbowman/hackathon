import pygame
import spritesheet

# pygame.init()

# SCREEN_WIDTH = 500
# SCREEN_HEIGHT = 500

# #(Rename caption with respect to character)
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption('Spritemovement(Ghost)')


# #(Name the variable with respect to sprite character, insert appropriate png)
# sprite_sheet_ghost = pygame.image.load('assets/ghost-Sheet.png').convert_alpha()
# # sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_ghost)
# sprite_sheet = pygame.image.load(sprite_sheet_ghost).convert_alpha()

# BG = (50, 50, 50)
# #adds transparency to img
# BLACK = (0, 0, 0)

# #make animation list
# # animation_list = []
# # animation_steps = 4
# # last_update = pygame.time.get_ticks()
# # animation_cooldown = 100
# # frame = 0

# # for x in range(animation_steps):
# #     animation_list.append(sprite_sheet.get_image(x, 32, 32, 2, BLACK))
# ghost_spritesheet = spritesheet.SpriteSheet(sprite_sheet, 32, 32, 2, (0, 0, 0))  # Adjust frame size and scale as needed

# #Game Loop
# run = True
# while run:
    
#     #to update background
#     screen.fill(BG)

#     sprite_sheet.update_animation()
#     sprite_sheet.draw(screen, 72, 0)  # Adjust position as needed

#     #to update animation
#     # current_time = pygame.time.get_ticks()
#     # if current_time - last_update >= animation_cooldown:
#     #     frame += 1
#     #     last_update = current_time
#     #     if frame >= len(animation_list):
#     #         frame = 0

#     #show frame image
#     # screen.blit(animationlist[frame], (x * 72, 0))

#     # screen.blit(frame_0, (0,0))
#     # screen.blit(frame_1, (50,0))

#     #Event handler
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False

#     pygame.display.update()

# pygame.quit()
# Initialize Pygame
pygame.init()

# Screen configuration
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sprite Movement (Ghost)')

# Load the spritesheet image
sprite_sheet_image = 'assets/ghost-Sheet.png'  # Ensure this path is correct
ghost_sprite_sheet = pygame.image.load(sprite_sheet_image).convert_alpha()

# Create a SpriteSheet object for the Ghost character
ghost_spritesheet = spritesheet.SpriteSheet(ghost_sprite_sheet, 32, 32, 2, (0, 0, 0))  # Adjust frame size and scale as needed

# Background color
BG = (50, 50, 50)

# Game Loop
run = True
while run:
    # Update background
    screen.fill(BG)

    # Update animation and draw the current frame
    ghost_spritesheet.update_animation()
    ghost_spritesheet.draw(screen, 32, 0)  # Adjust position as needed

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
