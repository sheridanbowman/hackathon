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

    def change_speed(self, x_diff, y_diff):
        self.change_x = x_diff
        self.change_y = y_diff
    
    def update(self, pressed_keys):
        # Player position
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
