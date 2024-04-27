import pygame
from pygame.locals import *

import random

# Class for 'monster' type objects that can be spawned; and have collision options: includes gems and chests

# monsterType: type of monster, ["heavyGhost", "treasureChest", "lightGhost", "gem"]
# affectedByGravity: whether it's affected by gravity
# spawnCoords: where the monster spawns
validMonsters = ["heavyGhost", "treasureChest", "lightGhost", "gem"]

class monster(pygame.sprite.Sprite):
    def __init__(self, monsterType:str, spawnCoords:tuple[int, int] = (0,0)):
        super(monster, self).__init__()
        self.monsterType = monsterType
        if monsterType not in validMonsters:
            exit("Trying to assign a monster type that doesnt exist!", monsterType, validMonsters)
        self.affectedByGravity = False 
        if self.monsterType in ["heavyGhost", "treasureChest", "gem"]:
            self.affectedByGravity = True
        
        self.spawnCoords = spawnCoords
        self.walls = None
        self.debugColor = None

        self.xSpeed = 2
        self.initialDirection = False

        if monsterType == "heavyGhost":
            self.initialDirection = random.randint(0,1)
            if self.initialDirection == 0:
                self.initialDirection = -1
            
            self.debugColor = (255, 0, 0)
        if monsterType == "lightGhost":
            self.debugColor = (192, 192, 192)
        if monsterType == "treasureChest":
            self.debugColor = (255, 255, 0)
        if monsterType == "gem":
            self.debugColor = (255, 255, 255)

        self.image = pygame.image.load('assets/player.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.spawnCoords[0]
        self.rect.y = self.spawnCoords[1]



        self.max_speed = 3
        self.change_x = 0
        self.change_y = 0

        self.gravityMult = 0.01
        self.gravityAccel = 0  # Constant ramping acceleration due to gravity



    def update(self, pressed_keys):
        self.gravityAccel = min(self.max_speed, self.gravityAccel + self.gravityMult)
        self.change_y +=self.gravityAccel

        if self.initialDirection:
            self.change_x = self.xSpeed * self.initialDirection
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        collide_list = pygame.sprite.spritecollide(self, self.walls, False)
        # collide list is a list of all of the sprites that the player is 
        # currently in contact with. If they are currently touching something,
        # the following code will check if the player is moving left or right
        # and make sure that the player doesn't move into the other sprite by setting
        # the player's position to the side of the other sprite

        for wall in collide_list:
            if self.rect.right >= wall.rect.left and self.rect.left <= wall.rect.left:
                print(self.change_x)
                self.rect.right = wall.rect.left-1
                if self.initialDirection:
                    self.change_x = self.change_x * -1
                print("Collision betwen sprite and the left side", self.change_x)
            elif self.rect.left <= wall.rect.right and self.rect.right >= wall.rect.right:
                print(self.change_x)
                self.rect.left = wall.rect.right+1
                if self.initialDirection:
                    self.change_x = self.change_x * -1
                print("Collision betwen sprite and the right side", self.change_x)
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
            #     print("Collision betwen sprite and the bottom side")

            # if self.rect.bottom>wall.rect.top:
            #     if self.change_y > 0:
            #         self.change_y = 0
            #         self.gravityAccel = 0
            #         self.rect.bottom = wall.rect.top
            #     else:
            #         self.rect.top = wall.rect.bottom
            # if wall.rect.right > self.rect.left or self.rect.right < wall.rect.left:
            #     # print("side collide")
            #     # Flip direction on collision with 'wall' thats on same plane
            #     if self.initialDirection:
            #         self.change_x = self.change_x * -1
            #     if self.change_x > 0:
            #         self.rect.right = wall.rect.left
            #     else:
            #         self.rect.left = wall.rect.right


            
        