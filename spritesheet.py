import pygame

# class SpriteSheet():
#         def __init__(self, image, width, height, scale, color):
#             # self.sheet = image
#             # self.animation_list = []
#             # self.animation_steps = 4
#             # self.last_update = pygame.time.get_ticks()
#             # self.animation_cooldown = 100
#             # self.frame = 0
#             self.sheet = pygame.image.load('assets/ghost-Sheet.png').convert_alpha()
#             self.frame_width = width
#             self.frame_height = height
#             self.scale = scale
#             self.color = color
#             self.animation_steps = 4
#             self.last_update = pygame.time.get_ticks()
#             self.animation_cooldown = 100
#             self.frame = 0
#             self.animation_list = [
#                 self.get_image(i) for i in range(self.animation_steps)
#             ]

#         def get_image(self, frame, width, height, scale, color):
#             image = pygame.Surface((width, height)).convert_alpha()
#             image.blit(self.sheet, (0,0), ((frame * width), 0, width, height))
#             image = pygame.transform.scale(image, (width * scale, height * scale))
#             image.set_colorkey(color)

#             return image 
        
#         def update_animation(self):
#                 current_time = pygame.time.get_ticks()
#                 if current_time - self.last_update >= self.animation_cooldown:
#                     self.frame += 1
#                     self.last_update = current_time
#                     if self.frame >= len(self.animation_list):
#                         self.frame = 0

class SpriteSheet:
    def __init__(self, image_path, width, height, scale, color):
        self.sheet = pygame.image.load(image_path).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.scale = scale
        self.color = color
        self.animation_steps = 4
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.frame = 0
        self.animation_list = [
            self.get_image(i) for i in range(self.animation_steps)
        ]

    def get_image(self, frame):
        image = pygame.Surface((self.frame_width, self.frame_height)).convert_alpha()
        image.blit(self.sheet, (0, 0), (frame * self.frame_width, 0, self.frame_width, self.frame_height))
        image = pygame.transform.scale(image, (self.frame_width * self.scale, self.frame_height * self.scale))
        image.set_colorkey(self.color)
        return image

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = current_time
            if self.frame >= len(self.animation_list):
                self.frame = 0

    def draw(self, screen, x, y):
        screen.blit(self.animation_list[self.frame], (x, y))

# Usage example:
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sprite Animation')

# Create a SpriteSheet object
sprite_sheet_image_path = 'assets/ghost-Sheet.png'
sprite = SpriteSheet(sprite_sheet_image_path, 32, 32, 3, (0, 0, 0))  # Adjust these parameters as needed

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))  # Fill the screen with white to clear old frames
    sprite.update_animation()
    sprite.draw(screen, 100, 100)  # Draw the sprite at position (100, 100)
    pygame.display.update()


pygame.quit()
