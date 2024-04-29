
import random
import pygame
from pygame.locals import *
class ScoreCounter(pygame.sprite.Sprite):
    def __init__(self, xPos:int, yPos:int, initialScore:int=0):
        self.collision=False
        
        self.score = initialScore # Literal Score Total
        self.delayedScore = initialScore # Delayed Score Display
        self.x=xPos
        self.y=yPos

        # Delay for incrementing
        self.delay = 1
        
        #internal timer to increment on
        self.timer = 0

    def update(self, yOffset):
        # If the score needs to be incremented, increment on timer
        if self.score > self.delayedScore:
            if self.timer > self.delay:
                self.timer = 0
                self.delayedScore += max(1, int((self.score - self.delayedScore)/5))
            else:
                self.timer +=1


        # self.x = self.x
        # self.y = self.y + yOffset

    def addScore(self, newScore):
        self.score += newScore

    # def getShake(self):
    #     difference = self.score - self.delayedScore
    #     xShake = random.randint((-difference//5), difference//5)
    #     yShake = random.randint((-difference//5), difference//5)
    #     return xShake, yShake
