import pygame
from pygame.locals import *


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Tank, self).__init__()

        self.image = pygame.image.load('assets/player.png')
        self.rect = self.image.get_rect()

        # Allows for initialization of the player onto a selected location
        self.rect.x = x
        self.rect.y = y

        self.change_x = 0
        self.change_y = 0

        self.walls = None

        self.acceleration = 0.05
        self.deceleration = 0.15
        self.max_speed = 3
        self.change_x = 0
        self.change_y = 0
        self.gravityMult = 0.01
        self.gravityAccel = 0  # Constant ramping acceleration due to gravity

        # internal counter for keeping track of jump speed, resets on collision
        self.jumpDuration = 0

        # Limit for how long to apply Jump Speed Displacement
        self.jumpLimit = 20
        self.jumpSpeed = 3
            
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

        if pressed_keys[K_a]:
            self.change_speed(-self.acceleration, 0)
            not_moving = False
        elif self.change_x < 0:
            self.change_x += self.deceleration

        if pressed_keys[K_d]:
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
        

        self.gravityAccel = min(self.max_speed, self.gravityAccel + self.gravityMult)
        self.change_y +=self.gravityAccel

        self.rect.x += self.change_x
        self.rect.y += max(-9, min(9, self.change_y))
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
        for wall in collide_list:

            if self.rect.right >= wall.rect.left and self.rect.left <= wall.rect.left:
                self.rect.right = wall.rect.left
                # print("Collision betwen sprite and the left side")
            elif self.rect.left <= wall.rect.right and self.rect.right >= wall.rect.right:
                self.rect.left = wall.rect.right
                # print("Collision betwen sprite and the right side")
            elif self.rect.bottom >= wall.rect.top and self.rect.top <= wall.rect.top:
                # print("Collision betwen sprite and the top side")
                if self.change_y > 0:

                    # Reset jump
                    self.jumpDuration = 0

                    self.change_y = 0
                    self.gravityAccel = 0
                    self.rect.bottom = wall.rect.top
                else:
                    self.rect.top = wall.rect.bottom
            # elif self.rect.top <= wall.rect.bottom and self.rect.bottom >= wall.rect.bottom:
                # print("Collision betwen sprite and the bottom side")
            # print(self.rect.bottom, wall.rect.top, self.rect.bottom>wall.rect.top)
            # Collision below?
            
