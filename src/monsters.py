import pygame
from pygame.locals import *
from src.spritesheet import SpriteSheet
from src.playerHealth import PlayerHealth
from src.tank import Tank
from src.score import ScoreCounter

import math
import random


pygame.mixer.init()
explosionSound = pygame.mixer.Sound('assets/laser gun.wav')
coinSound =pygame.mixer.Sound('assets/Pickup Coin.wav')
explosion =pygame.mixer.Sound('assets/explosion_echo_29.wav')
damage = pygame.mixer.Sound('assets/damage.wav')
# upgrade =pygame.mixer.Sound('assets/upgrade.wav')

# Class for 'monster' type objects that can be spawned; and have collision options: includes gems and chests

# monsterType: type of monster, ["heavyGhost", "treasureChest", "lightGhost", "gem"]
# spawnCoords: where the monster spawns
validMonsters = ["heavyGhost", "treasureChest", "lightGhost", "gem", "projectile", "explosion"]
moveTypes = ["flyToTarget", "walk", "seek", "static"]

def move_towards_target(x1, y1, x2, y2, speed):

    angle = math.atan2(y2 - y1, x2 - x1)

    speed_x = math.cos(angle) * speed
    speed_y = math.sin(angle) * speed

    return speed_x, speed_y

def casualty(rect1, rect2, radius):
    center1 = rect1.center
    center2 = rect2.center
    distance = math.sqrt((center2[0] - center1[0])**2 + (center2[1] - center1[1])**2)
    # print(distance, radius)
    if distance < radius:
        return True
    return False

THRESHOLD = 10

class Monster(pygame.sprite.Sprite):
    def __init__(self, monsterType:str, walls=None, spawnCoords:tuple[int, int] = (0,0), targetCoords:tuple[int, int] = (0,0), 
                 allSprites=None,scoreHandle = None, playerHandle = None, health_Handle=None, explosionRadius= 60):
        super(Monster, self).__init__()
        
        if monsterType in validMonsters:
            self.monsterType = monsterType
        else:
            exit("Trying to assign a monster type that doesnt exist!", monsterType, validMonsters)

        self.collision = True
        self.scoreHandle = scoreHandle
        self.playerHandle = playerHandle
        self.spawnCoords = spawnCoords
        self.allSprites=allSprites
        self.walls = walls
        self.explosionRadius=explosionRadius

        self.health_Handle = health_Handle

        self.debugColor = None # for debugging tile spawn locations

        self.moveType = "static"
        self.targetCoords = targetCoords #target for fly behavior, seek behavior

        self.xSpeed = 1

        self.xMoveDirection = random.randint(0,1)
        if self.xMoveDirection == 0:
            self.xMoveDirection = -1
        self.image = pygame.image.load('assets/player.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.spawnCoords[0]
        self.rect.y = self.spawnCoords[1]

        self.chestType = random.randint(0,3)*2
        if monsterType == "heavyGhost":
            self.debugColor = (255, 0, 0)
            self.moveType = "walk"
            self.xSpeed=2
            self.ySpeed=0
                
            self.spriteSheet = SpriteSheet(image_path="assets/ghostSheetCombined.png",num_actions=2,frames_per_action=7, scale=0.75, animation_cooldown=200) 
            self.image=self.spriteSheet.currImage
            
        if monsterType == "lightGhost":
            self.debugColor = (192, 192, 192)
            self.moveType = "flyToTarget"
            self.xSpeed=2
            self.ySpeed=2
    
            self.spriteSheet = SpriteSheet(image_path="assets/ghostSheetCombined2.png",num_actions=2,frames_per_action=7, scale=0.75, animation_cooldown=200) 
            self.image=self.spriteSheet.currImage
        
        if monsterType == "projectile":
            self.moveType = "flyToTarget"
            self.image = pygame.image.load('assets/omniProjectile.png')
            self.collision = False
            self.xSpeed=0#unused
            self.ySpeed=0#unuesed
            self.speed_x, self.speed_y = move_towards_target(self.rect.x, self.rect.y, self.targetCoords[0], self.targetCoords[1], 15)

        if monsterType == "treasureChest":
            self.spriteSheet = SpriteSheet(image_path="assets/Chests.png", xDim=48, yDim=32, num_actions=8,frames_per_action=5, scale=0.75, animation_cooldown=100) 
            self.spriteSheet.set_action(self.chestType)
            self.xSpeed=0
            self.ySpeed=0
            self.collision = False

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
            self.ySpeed=0
            self.collision = False

        if monsterType == "explosion":
            self.spriteSheet = SpriteSheet(image_path="assets/Retro Impact Effect Pack 1 A.png", xDim=64, yDim=64, num_actions=24, frames_per_action=7, scale=2.0, animation_cooldown=20) 
            self.spriteSheet.set_action(5)
            self.xSpeed=0
            self.ySpeed=0
            self.collision = False

            self.image=self.spriteSheet.currImage

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
        if self.monsterType in ["heavyGhost", "gem", "treasureChest", "lightGhost", "explosion"]:
            self.spriteSheet.updateSpriteSheet()
            if self.xMoveDirection == 1:
               self.image = pygame.transform.flip(self.spriteSheet.currImage, True, False)
            else:
                self.image = self.spriteSheet.currImage
            if self.monsterType=="explosion" and self.spriteSheet.frame==6:
                super().kill()
        
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

        # +++++++++collision++++++++++++++++++++
        if self.monsterType in ["lightGhost", "heavyGhost", "gem", "treasureChest"]:
            # print(self.monsterType, self, self.playerHandle)
            if pygame.sprite.collide_rect(self, self.playerHandle):
                if self.monsterType == "gem":
                    coinSound.play()
                    self.scoreHandle.addScore(100)
                if self.monsterType == "treasureChest":
                    coinSound.play()
                    choice = random.randint(0,1)
                    if choice == 1:
                        self.scoreHandle.addScore(400)
                    if choice == 0:
                        self.health_Handle.update_health(self.health_Handle.health+1)
                if self.monsterType in ["lightGhost", "heavyGhost"]:
                    damage.play()
                    self.health_Handle.update_health(self.health_Handle.health-1)

                super().kill()

        #Check projectile against mobs

        # ++++++++++ physics+++++++++++++++++
        if self.monsterType in ["projectile", "lightGhost"]:
            if self.monsterType == "lightGhost":
                
                self.targetCoords = (self.playerHandle.rect.x,  self.playerHandle.rect.y)
                #update speed real time
                self.speed_x, self.speed_y = move_towards_target(self.rect.x, self.rect.y, self.targetCoords[0], self.targetCoords[1], 2)
                if self.speed_x>=0:
                    self.speed_x = min(2,self.speed_x)
                else:
                    self.speed_x = max(-2,self.speed_x)

                if self.speed_y>=0:
                    self.speed_y = min(2,self.speed_y)
                else:
                    self.speed_y = max(-2, self.speed_y)
                self.rect.x += self.speed_x
                self.yOrigin += self.speed_y
                self.rect.y = self.yOrigin + globalOffset
                # print(self.rect.x, self.rect.y, self.speed_x, self.speed_y)
           
           
            # if self.rect.x < self.targetCoords[0]:
            #     self.rect.x += self.xSpeed
            # else:
            #     self.rect.x -= self.xSpeed
            # if self.rect.y < self.targetCoords[1]:
            #     self.rect.y += self.ySpeed
            # else:
            #     self.rect.y -= self.ySpeed
            else:
                self.rect.y += self.speed_y
                self.rect.x += self.speed_x

                # self.yOrigin += self.speed_y
                # self.rect.y = self.yOrigin + globalOffset
                # print(self.rect.y, self.yOrigin, globalOffset)

                
            if self.monsterType == "projectile": #projectile check
                tile_collide_list = pygame.sprite.spritecollide(self, self.walls, False)
                sprite_collide_list = pygame.sprite.spritecollide(self, self.allSprites, False)

                collisionPoint=False
                for collidedTile in tile_collide_list:
                    collisionPoint = (collidedTile.rect.x, collidedTile.rect.y)
                    
                for collidedSprite in sprite_collide_list:
                    if collidedSprite.collision==True:
                        collisionPoint = (collidedSprite.rect.x, collidedSprite.rect.y)

            
                #Got pt of collision, now determine casualties
                if collisionPoint:
                    # print(collisionPoint, len(tile_collide_list), len(sprite_collide_list))
                    explosion.play()
                    newGem = Monster(monsterType="explosion", spawnCoords=(collisionPoint[0],collisionPoint[1]-globalOffset), walls=self.walls, 
                        allSprites=self.allSprites,scoreHandle=self.scoreHandle, health_Handle=self.health_Handle, playerHandle=self.playerHandle)
                    self.allSprites.add(newGem)
                    for localTile in self.walls:
                        if casualty(localTile.rect, self.rect, self.explosionRadius):
                            if localTile.gem:
                                newGem = Monster(monsterType="gem", spawnCoords=(localTile.rect.x,localTile.rect.y-globalOffset), walls=self.walls, 
                        allSprites=self.allSprites,scoreHandle=self.scoreHandle, health_Handle=self.health_Handle, playerHandle=self.playerHandle)
                                self.allSprites.add(newGem)
                            localTile.destroyTile()
                    for localSprite in self.allSprites:
                        if localSprite.collision==True and casualty(localSprite.rect, self.rect, self.explosionRadius):
                            localSprite.kill()
                    #kill self after all 
                    super().kill()
            
        
        # Everything that's not a lightGhost collides with tiles
        if self.monsterType == "explosion": 
            self.rect.y=self.yOrigin+globalOffset
            return

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