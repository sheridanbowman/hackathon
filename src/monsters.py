import pygame
from pygame.locals import *

import random

# Class for 'monster' type objects that can be spawned; and have collision options: includes gems and chests

# monsterType: type of monster, ["heavyGhost", "treasureChest", "lightGhost", "gem"]
# affectedByGravity: whether it's affected by gravity
# spawnCoords: where the monster spawns
validMonsters = ["heavyGhost", "treasureChest", "lightGhost", "gem", "projectile"]
moveTypes = ["flyToTarget", "walk", "seek", "static"]

class Monster(pygame.sprite.Sprite):
    def __init__(self, monsterType:str, walls=None, spawnCoords:tuple[int, int] = (0,0), targetCoords:tuple[int, int] = (0,0)):
        super(Monster, self).__init__()
        
        if monsterType in validMonsters:
            self.monsterType = monsterType
        else:
            exit("Trying to assign a monster type that doesnt exist!", monsterType, validMonsters)
        
        self.affectedByGravity = None 
        if self.monsterType in ["heavyGhost", "treasureChest", "gem"]:
            self.affectedByGravity = True
        if self.monsterType in ["projectile", "lightGhost"]:
            self.affectedByGravity = False
        
        self.spawnCoords = spawnCoords
        self.walls = walls

        self.debugColor = None # for debugging tile spawn locations

        self.moveType = "static"
        self.targetCoords = targetCoords #target for fly behavior, seek behavior

        self.xSpeed = 2
        self.xMoveDirection = False # init as false, randomized if walk type

        if monsterType == "heavyGhost":
            self.debugColor = (255, 0, 0)
            self.moveType = "walk"
            self.xMoveDirection = random.randint(0,1)
            if self.xMoveDirection == 0:
                self.xMoveDirection = -1
            
        if monsterType == "lightGhost":
            self.debugColor = (192, 192, 192)
            self.moveType = "flyToTarget"
        
        if monsterType == "projectile":
            self.moveType = "flyToTarget"

        if monsterType == "treasureChest":
            self.debugColor = (255, 255, 0)

        if monsterType == "gem":
            self.debugColor = (255, 255, 255)

        # TODO: if gem, draw gem, if ghost, draw ghost moving xMoveDirection, if chest ... etc
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

        if self.xMoveDirection:
            self.change_x = self.xSpeed * self.xMoveDirection
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        
        # collide list is a list of all of the sprites that the player is 
        # currently in contact with. If they are currently touching something,
        # the following code will check if the player is moving left or right
        # and make sure that the player doesn't move into the other sprite by setting
        # the player's position to the side of the other sprite

        if self.monsterType != "projectile":
            #check collision to player, do damage if mob, award points if loot, play relevant animations
            pass

        # Everything that's not a lightGhost collides with tiles
        if self.monsterType == "lightGhost": 
            # update fly target to player pos
            pass
        else: # Has wall collision
            collide_list = pygame.sprite.spritecollide(self, self.walls, False)
            for wall in collide_list:
                if self.rect.right >= wall.rect.left and self.rect.left <= wall.rect.left:
                    # print(self.change_x)
                    self.rect.right = wall.rect.left
                    if self.moveType == "walking": #walkers change direction
                        self.xMoveDirection = -1
                    # print("Collision betwen sprite and the left side", self.change_x, self.rect.right, wall.rect.left)
                elif self.rect.left <= wall.rect.right and self.rect.right >= wall.rect.right:
                    # print(self.change_x, self.rect.left, wall.rect.right)
                    self.rect.left = wall.rect.right
                    if self.moveType == "walking": #walkers change direction
                        self.xMoveDirection = 1
                        # print(self.change_x, self.rect.left, wall.rect.right)
                    # print("Collision betwen sprite and the right side", self.change_x)
                elif self.rect.bottom >= wall.rect.top and self.rect.top <= wall.rect.top:
                    # print("Collision betwen sprite and the top side")

                    self.change_y = 0
                    self.gravityAccel = 0
                    self.rect.bottom = wall.rect.top
                # elif self.rect.top <= wall.rect.bottom and self.rect.bottom >= wall.rect.bottom:
                #     print("Collision betwen sprite and the bottom side")    
            # if self.monsterType == "projectile":
            #     # Also has enemy sprite collision
            #     # spawn explosion at coord
            #     # enemy_collide_list = pygame.sprite.spritecollide(self, self.enemies, False)
            #     pass