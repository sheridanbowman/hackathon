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
BLACK = (0, 0, 0)


class SpriteSheet:
    # def __init__(self, image_path, width, height, scale, color):
    #     self.sheet = pygame.image.load(image_path).convert_alpha()
    #     self.frame_width = width
    #     self.frame_height = height
    #     self.scale = scale
    #     self.color = color
    #     #For self.animation_steps, enter number of frames
    #     self.animation_steps = 5
    #     self.last_update = pygame.time.get_ticks()
    #     self.animation_cooldown = 100
    #     self.frame = 0
    #     self.animation_list = [
    #         self.get_image(i) for i in range(self.animation_steps)
    #     ]
    def __init__(self, image_path, frames_per_action, num_actions=1, paused=False, scale=1.0, pause=0, animation_cooldown=100, xDim=32, yDim=32, current_action=0):
        self.sheet = pygame.image.load(image_path).convert_alpha()
        self.num_actions = num_actions
        self.frames_per_action = frames_per_action
        self.actions = [[] for _ in range(num_actions)]

        # The 'row' or 'action' to begin on
        self.current_action = current_action

        # ticks to pause for
        self.animation_cooldown = animation_cooldown

        self.last_update = pygame.time.get_ticks()

        # Current frame
        self.frame = 0

        # if to have animation paused, to resume later (chest)
        self.paused = paused

        # pause between loops
        self.pause = pause
        self.pauseTimer = 0
        self.scale = scale
        # Fill self.actions with frames
        self.load_images(width=xDim, height=yDim, scale=scale)   

        self.currImage = self.actions[self.current_action][self.frame]

    

    def load_images(self, width, height, scale):
        for action in range(self.num_actions):
            for frame in range(self.frames_per_action):
                self.actions[action].append(self.get_image(frame, action, width, height, scale))


    def get_image(self, frame, row, width, height, scale):
        # image = pygame.Surface((self.frame_width, self.frame_height)).convert_alpha()
        # image.blit(self.sheet, (0, 0), (frame * self.frame_width, 0, self.frame_width, self.frame_height))
        # image = pygame.transform.scale(image, (self.frame_width * self.scale, self.frame_height * self.scale))
        # image.set_colorkey(self.color)
        # return image
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), ((frame * width), (row * height), width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(BLACK)
        return image

    def updateSpriteSheet(self):
        current_time = pygame.time.get_ticks()
        # print(self.frame, self.pauseTimer, self.pause)
        if self.frame == 0 and self.pause != 0 and self.pauseTimer < self.pause:
            # Increment the pause timer
            self.pauseTimer += 1
        else:
            if current_time - self.last_update >= self.animation_cooldown:
                self.frame += 1
                self.last_update = current_time
                if self.frame >= len(self.actions[self.current_action]):
                    self.frame = 0
            self.currImage = self.actions[self.current_action][self.frame]
            # Reset the pause timer if not in pause state
            self.pauseTimer = 0
        
        


    # Swap to action X
    def set_action(self, action_index):
        if action_index <= self.num_actions:
            self.current_action = action_index
            self.frame = 0
        else: 
            exit("Tried loading row", action_index, "out of", self.num_actions)
        

    # def draw(self, screen):
    #     # screen.blit(self.animation_list[self.frame], (x, y))
    #     screen.blit(self.actions[self.current_action][self.frame], (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))


# # Usage example:
# pygame.init()
# SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption('Sprite Animation')
# clock = pygame.time.Clock()

# #Insert png for sprite
# sprite_sheet = SpriteSheet('assets/ghostSheetCombined.png', 2, 8)

# running = True
# action_cycle = 0
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     sprite_sheet.update()

#     # Example: Cycle through actions
#     if pygame.time.get_ticks() % 2000 < 50:
#         action_cycle = (action_cycle + 1) % 4
#         sprite_sheet.set_action(action_cycle)

#     screen.fill(BLACK)
#     sprite_sheet.draw(screen)
#     pygame.display.flip()
#     clock.tick(60)

# # Insert sprite file, with each row, and their frames
# sprite_sheet_image_path = 'assets/Animated Chests/Chests.png'

# #Adjust the parameters as needed (x, y, size, dont touch those three zeros just leave them)
# sprite = SpriteSheet(sprite_sheet_image_path, 48, 32, 5, (0, 0, 0))

# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     screen.fill((30, 30, 30))  # Fill the screen with white to clear old frames
#     sprite.update_animation()
#     sprite.draw(screen, 100, 100)  # Draw the sprite at position (100, 100)
#     pygame.display.update()


pygame.quit()
