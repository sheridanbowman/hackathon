import pygame
from pygame.locals import *



debugMode = False

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, screenWidth, screenHeight):
        super(Tank, self).__init__()

        # Main body Sprite
        self.spriteSheet = pygame.image.load('assets/demoTankBaseGreen.png').convert_alpha()
        self.sprites =  [[None for _ in range(2)] for _ in range(2)]
        for row in range(2):
            for col in range(2):
                spritex = col * 36
                spritey = row * 32
                self.sprites[row][col] = self.spriteSheet.subsurface((spritex, spritey, 36, 32))

        self.image = self.sprites[0][0]

        self.rect = self.image.get_rect()
        # Create a smaller rect centered within the larger rect
        small_rect = pygame.Rect((0, 0), (30, 30))
        small_rect.center = self.rect.center
        self.rect = small_rect
        #smaller rect to easier navigate single tile holes
        

        # Tank Head 
        self.head_bg = pygame.image.load("assets/tankHeadBackground.png").convert_alpha()
        self.head_mask = pygame.image.load("assets/tankHeadMask.png").convert_alpha()

        self.mask_surface = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA) #mask the whole screen
        self.mask_surface.blit(self.head_mask, (0, 0)) # let a little bit through


        # Turret images
        self.turret_image = pygame.image.load("assets/turretRight.png")
        self.turret_rect= self.turret_image.get_rect()

        # Allows for initialization of the player onto a selected location
        self.rect.x = x
        self.rect.y = y

        self.change_x = 0
        self.change_y = 0

        self.walls = None

        self.direction = 1 # Changed by keypress, determines which side tanks rendered facing

        self.acceleration = 0.03
        self.deceleration = 0.05
        self.max_speed = 2
        self.change_x = 0
        self.change_y = 0
        self.gravityMult = 0.01
        self.gravityAccel = 0  # Constant ramping acceleration due to gravity

        # internal counter for keeping track of jump speed, resets on collision
        self.jumpDuration = 0

        # Limit for how long to apply Jump Speed Displacement
        self.jumpLimit = 15
        self.jumpSpeed = 2
            
        # TODO: increase jump height as multiple of current speed
        # TODO: global jump cooldown


    def change_speed(self, x_diff, y_diff):
        # only update called dimension
        if x_diff != 0:
            if abs(self.change_x + x_diff) < self.max_speed:
                self.change_x += x_diff
        # if abs(self.change_y + y_diff) < self.max_speed:
        if y_diff != 0:
            self.change_y = y_diff

    def update(self, pressed_keys):
        # Player position
        not_moving = True
        
        if not debugMode:
            if pressed_keys[K_w]:
                if self.jumpDuration < self.jumpLimit:
                    self.jumpDuration += 1
                    
                    # Dont accel up using function, instant impulse up
                    # self.change_speed(0, -self.acceleration*6)
                    self.change_y = -self.jumpSpeed
            else:
                # Prevent 'double jumping'
                if self.change_y < 0:
                    self.jumpDuration = self.jumpLimit
                    self.change_y += self.acceleration
        else:
            if pressed_keys[K_s]:
                self.rect.y += self.jumpSpeed   
            if pressed_keys[K_w]:
                self.rect.y -= self.jumpSpeed 


        if pressed_keys[K_a]:
            self.direction = 1
            self.change_speed(-self.acceleration, 0)
            not_moving = False
        elif self.change_x < 0:
            self.change_x += self.deceleration

        if pressed_keys[K_d]:
            self.direction = 0
            self.change_speed(self.acceleration, 0)
            not_moving = False
        elif self.change_x > 0:
            self.change_x -= self.deceleration

        
        # if not_moving:
        #     # Decelerate if no key is pressed
        #     if self.change_x > 0:
        #         self.change_x -= self.deceleration
        #     elif self.change_x < 0:
        #         self.change_x += self.deceleration
        #     # if self.change_y > 0:
        #     #     self.change_y -= self.acceleration
        #     if self.change_y < 0:
        #         self.change_y += self.acceleration
        
        if not debugMode:
            self.gravityAccel = min(self.max_speed, self.gravityAccel + self.gravityMult)
            self.change_y +=self.gravityAccel


        # self.rect.x += self.change_x
        # self.rect.y += max(-9, min(9, self.change_y))

        # self.rect.y +=1
        # print(self.jumpDuration)
        

        collide_list = pygame.sprite.spritecollide(self, self.walls, False)
        # collide list is a list of all of the sprites that the player is 
        # currently in contact with. If they are currently touching something,
        # the following code will check if the player is moving left or right
        # and make sure that the player doesn't move into the other sprite by setting
        # the player's position to the side of the other sprite
        # for wall in collide_list:
        #     if self.change_x > 0:
        #         self.rect.right = wall.rect.left
        #     else:
        #         self.rect.left = wall.rect.right
        
        # does the same as above, but with up and down
        # collide_list = pygame.sprite.spritecollide(self, self.walls, False)
        # if not debugMode:
        #     for wall in collide_list:
        #         if self.rect.bottom >= wall.rect.top and self.rect.top >= wall.rect.top:
        #             # print("Collision betwen sprite and the top side")
        #             # if self.change_y > 0:
        #             # Reset jump
        #             self.jumpDuration = 0

        #             self.change_y = 0
        #             self.gravityAccel = 0
        #             self.rect.bottom = wall.rect.top
        #         elif self.rect.right >= wall.rect.left and self.rect.left <= wall.rect.left:
        #             self.rect.right = wall.rect.left
        #             self.change_x = 0
        #             print("Collision betwen sprite and the left side")
        #         elif self.rect.left <= wall.rect.right and self.rect.right >= wall.rect.right:
        #             self.rect.left = wall.rect.right
        #             self.change_x = 0
        #             print("Collision betwen sprite and the right side")
        #         elif self.rect.top <= wall.rect.bottom and self.rect.bottom >= wall.rect.bottom:
        #             # print("Collision betwen sprite and the bottom side")
        #             self.rect.top = wall.rect.bottom
        #             self.change_y = 0
            
        #     # print(self.rect.bottom, wall.rect.top, self.rect.bottom>wall.rect.top)
        #     # Collision below?

        # self.rect.x += self.change_x
        # self.rect.y += max(-9, min(9, self.change_y))
        # if not debugMode:
        #     for wall in collide_list:
        #         # Check for collision with the top side of the wall
        #         if self.rect.bottom >= wall.rect.top and self.rect.top < wall.rect.top:
        #             if self.change_y > 0.0:  # Moving upward
        #                 print("botcollide")
        #                 self.rect.bottom = wall.rect.top
        #             # Reset jump
        #             self.jumpDuration = 0
        #             self.change_y = 0
        #             self.gravityAccel = 0

        #          # Check for collision with the bottom side of the wall
        #         elif self.rect.top <= wall.rect.bottom and self.rect.bottom > wall.rect.bottom:
        #             print("sprite collides with bottom ", self.rect.top, wall.rect.bottom)
        #             if self.change_y < 0.0:  # Moving upward
        #                 self.rect.top = wall.rect.bottom
        #                 self.change_y = 0
        #                 print(self.rect.bottom , wall.rect.top)



        #         # Check for collision with the right side of the wall
        #         elif self.rect.left <= wall.rect.right and self.rect.right > wall.rect.right:
        #             print("sprite collides with right of block", 
        #                   self.rect.left, self.rect.right, wall.rect.left, wall.rect.right, self.change_x)
        #             if self.change_x < 0:  # Moving left
        #                 self.rect.left = wall.rect.right
        #                 self.change_x = (self.change_x*-1)//2

        #             # if self.change_x < 0:  # Moving left
                        

        #         # Check for collision with the left side of the wall
        #         elif self.rect.right >= wall.rect.left and self.rect.left < wall.rect.left:
        #             print("sprite collides with left of block")
        #             if self.change_x > 0:  # Moving left
        #                 self.rect.right = wall.rect.left
        #                 self.change_x = (self.change_x*-1)//2

        
        self.rect.y += max(-9, min(9, self.change_y))
        if not debugMode:
            for wall in collide_list:
                if abs(wall.rect.left - self.rect.right) >5 and wall.rect.right - self.rect.left >5:
                    # Check for collision with the top side of the wall
                    if self.rect.bottom >= wall.rect.top and self.rect.top < wall.rect.top:
                        if self.change_y > 0.0:  # Moving upward
                            # print("botcollide")
                            self.rect.bottom = wall.rect.top
                        # Reset jump
                        self.jumpDuration = 0
                        self.change_y = 0
                        self.gravityAccel = 0

                    # Check for collision with the bottom side of the wall
                    elif self.rect.top <= wall.rect.bottom and self.rect.bottom > wall.rect.bottom:
                        # print("sprite collides with bottom ", self.rect.top, wall.rect.bottom)
                        if self.change_y < 0.0:  # Moving upward
                            self.rect.top = wall.rect.bottom
                            self.change_y = 0
                            print(self.rect.bottom , wall.rect.top)

            self.rect.x += self.change_x
            for wall in collide_list:
                # Check for collision with the right side of the wall
                if wall.rect.top < self.rect.bottom and wall.rect.bottom > self.rect.top:
                    if self.rect.left <= wall.rect.right and self.rect.right > wall.rect.right:
                        # print("sprite collides with right of block",self.rect.left, self.rect.right, wall.rect.left, wall.rect.right, self.change_x)
                        if self.change_x < 0:  # Moving left
                            self.rect.left = wall.rect.right
                            self.change_x = 0

                        # if self.change_x < 0:  # Moving left
                            

                    # Check for collision with the left side of the wall
                    elif self.rect.right >= wall.rect.left and self.rect.left < wall.rect.left:
                        # print("sprite collides with left of block")
                        if self.change_x > 0:  # Moving left
                            self.rect.right = wall.rect.left
                            self.change_x = 0


            
            # print(self.rect.bottom, wall.rect.top, self.rect.bottom>wall.rect.top)
            # Collision below?
        
        

        # movepanels = self.rightpanels
        # mainpanel = movepanels[1]

        # if self.direction == 1: 
        #     movepanels = self.leftpanels
        # # render alt move frame on odd pixel counts
        # if self.rect.x % 2 == 0:
        #     mainpanel = movepanels[0]
        # if self.direction == 1:
        self.image = self.sprites[self.direction][self.rect.x % 2 == 0]
        # draw main panel
            
