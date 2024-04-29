import pygame
from pygame.locals import *
from src.spritesheet import SpriteSheet

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

        self.xSpeed = 1

        self.xMoveDirection = random.randint(0,1)
        if self.xMoveDirection == 0:
            self.xMoveDirection = -1
        self.image = pygame.image.load('assets/player.png')
        self.chestType = random.randint(0,3)*2
        if monsterType == "heavyGhost":
            self.debugColor = (255, 0, 0)
            self.moveType = "walk"

                
            self.spriteSheet = SpriteSheet(image_path="assets/ghostSheetCombined.png",num_actions=2,frames_per_action=7, scale=0.75, animation_cooldown=200) 
            self.image=self.spriteSheet.currImage
            
        if monsterType == "lightGhost":
            self.debugColor = (192, 192, 192)
            self.moveType = "flyToTarget"
            self.xSpeed=0
    

            self.spriteSheet = SpriteSheet(image_path="assets/ghostSheetCombined2.png",num_actions=2,frames_per_action=7, scale=0.75, animation_cooldown=200) 
            self.image=self.spriteSheet.currImage
        
        if monsterType == "projectile":
            self.moveType = "flyToTarget"

        if monsterType == "treasureChest":
            self.spriteSheet = SpriteSheet(image_path="assets/Chests.png", xDim=48, yDim=32, num_actions=8,frames_per_action=5, scale=0.75, animation_cooldown=100) 
            self.spriteSheet.set_action(self.chestType)
            self.xSpeed=0

            self.image=self.spriteSheet.currImage
            
            self.debugColor = (255, 255, 0)

        if monsterType == "gem":
            scale =random.uniform(0.5, 0.75)
            offset = 32-(scale*32)
            self.spawnCoords = (self.spawnCoords[0] + random.randint(0,int(offset)), self.spawnCoords[1])
            self.debugColor = (255, 255, 255)
            self.spriteSheet = SpriteSheet(image_path="assets/Pixel purple gem.png",frames_per_action=7, scale=scale, pause=100) 
            self.image=self.spriteSheet.currImage
            self.xSpeed=0

        # TODO: if gem, draw gem, if ghost, draw ghost moving xMoveDirection, if chest ... etc


        
        self.rect = self.image.get_rect()
        self.rect.x = self.spawnCoords[0]
        self.rect.y = self.spawnCoords[1]

        self.max_speed = 3
        self.change_x = 0
        self.change_y = 0

        self.gravityMult = 0.01
        self.gravityAccel = 0  # Constant ramping acceleration due to gravity

        self.yOrigin = spawnCoords[1]



    def update(self, pressed_keys=None, globalOffset=0):
        if self.monsterType in ["heavyGhost", "gem", "treasureChest", "lightGhost"]:
            self.spriteSheet.updateSpriteSheet()
            if self.xMoveDirection == 1:
               self.image = pygame.transform.flip(self.spriteSheet.currImage, True, False)
            else:
                self.image = self.spriteSheet.currImage
        if self.moveType != "flyToTarget":
            self.gravityAccel = min(self.max_speed, self.gravityAccel + self.gravityMult)
            self.change_y +=self.gravityAccel

        if self.xMoveDirection:
            self.change_x = self.xSpeed * self.xMoveDirection
        self.rect.x += self.change_x
        self.yOrigin += self.change_y
        self.rect.y = self.yOrigin + globalOffset


        # if self.newOffset != globalOffset:
        #     self.newOffset = globalOffset
        #     self.rect.y += self.newOffset
        # print(self.rect.y, globalOffset)

        
        # collide list is a list of all of the sprites that the player is 
        # currently in contact with. If they are currently touching something,
        # the following code will check if the player is moving left or right
        # and make sure that the player doesn't move into the other sprite by setting
        # the player's position to the side of the other sprite

        # +++++++++++ Drawing++++++++++++++++++



        # ++++++++++ physics+++++++++++++++++
        if self.monsterType != "projectile":
            #check collision to player, do damage if mob, award points if loot, play relevant animations
            pass
        
        # Everything that's not a lightGhost collides with tiles
        if self.monsterType == "lightGhost": 
            # update fly target to player pos
            pass
        if self.monsterType in ["gem", "treasureChest", "heavyGhost"]:
            # if self.monsterType=="gem":
            #     print(len(self.walls))
            collide_list = pygame.sprite.spritecollide(self, self.walls, False)
            for wall in collide_list:
                if abs(wall.rect.left - self.rect.right) >5 and wall.rect.right - self.rect.left >5:
                    # Check for collision with the top side of the wall
                    if self.rect.bottom >= wall.rect.top and self.rect.top < wall.rect.top:
                        if self.change_y > 0.0:  # Moving upward
                            # print("botcollide")
                            self.rect.bottom = wall.rect.top
                            self.change_y = 0
                            self.gravityAccel = 0

                    # Check for collision with the bottom side of the wall
                    elif self.rect.top <= wall.rect.bottom and self.rect.bottom > wall.rect.bottom:
                        # print("sprite collides with bottom ", self.rect.top, wall.rect.bottom)
                        if self.change_y < 0.0:  # Moving upward
                            self.rect.top = wall.rect.bottom
                            self.change_y = 0
                            # print(self.rect.bottom , wall.rect.top)

            self.rect.x += self.change_x
            for wall in collide_list:
                # Check for collision with the right side of the wall
                if wall.rect.top < self.rect.bottom and wall.rect.bottom > self.rect.top:
                    if self.rect.left <= wall.rect.right and self.rect.right > wall.rect.right:
                        # print("sprite collides with right of block",self.rect.left, self.rect.right, wall.rect.left, wall.rect.right, self.change_x)
                        if self.change_x < 0:  # Moving left
                            self.rect.left = wall.rect.right
                            self.change_x = 0
                            self.xMoveDirection = self.xMoveDirection * -1

                        # if self.change_x < 0:  # Moving left
                            

                    # Check for collision with the left side of the wall
                    elif self.rect.right >= wall.rect.left and self.rect.left < wall.rect.left:
                        # print("sprite collides with left of block")
                        if self.change_x > 0:  # Moving left
                            self.rect.right = wall.rect.left
                            self.change_x = 0
                            self.xMoveDirection = self.xMoveDirection * -1
            

            # collide_list = pygame.sprite.spritecollide(self, self.walls, False)
            # for wall in collide_list:
            #     if self.rect.right >= wall.rect.left and self.rect.left <= wall.rect.left:
            #         # print(self.change_x)
            #         self.rect.right = wall.rect.left
            #         if self.moveType == "walking": #walkers change direction
            #             self.xMoveDirection = -1
            #         # print("Collision betwen sprite and the left side", self.change_x, self.rect.right, wall.rect.left)
            #     elif self.rect.left <= wall.rect.right and self.rect.right >= wall.rect.right:
            #         # print(self.change_x, self.rect.left, wall.rect.right)
            #         self.rect.left = wall.rect.right
            #         if self.moveType == "walking": #walkers change direction
            #             self.xMoveDirection = 1
            #             # print(self.change_x, self.rect.left, wall.rect.right)
            #         # print("Collision betwen sprite and the right side", self.change_x)
            #     elif self.rect.bottom >= wall.rect.top and self.rect.top <= wall.rect.top:
            #         # print("Collision betwen sprite and the top side")

            #         self.change_y = 0
            #         self.gravityAccel = 0
            #         self.rect.bottom = wall.rect.top
            #     # elif self.rect.top <= wall.rect.bottom and self.rect.bottom >= wall.rect.bottom:
            #     #     print("Collision betwen sprite and the bottom side")    
            # # if self.monsterType == "projectile":
            # #     # Also has enemy sprite collision
            # #     # spawn explosion at coord
            # #     # enemy_collide_list = pygame.sprite.spritecollide(self, self.enemies, False)
            # #     pass