import pygame
import math
from pygame.locals import *

BG_WIDTH = 320

def initBackgroundTileGroup(screenWidth):
    background_list = pygame.sprite.Group()
    backgroundScale = 1.25
    backgroundWidth = 320 * backgroundScale
    backgroundRepeats = math.ceil(screenWidth/backgroundWidth)+1
    for filename in ["assets/FREE_Fantasy Forest/Sky.png", 
                    "assets/FREE_Fantasy Forest/Clouds.png",
                    "assets/FREE_Fantasy Forest/Rock Mountains.png",
                    "assets/FREE_Fantasy Forest/Grass Mountains.png"]:
        for repeat in range(backgroundRepeats):
            bgImage = BackgroundImage(filename=filename, x_offset=backgroundWidth*repeat, 
                                    imgWidth=backgroundWidth, screenWidth=screenWidth)
            if filename.endswith("/Clouds.png"):
                bgImage.scrollingSpeed=14
            if filename.endswith("/Sky.png"):
                bgImage.scrollingSpeed=30
            background_list.add(bgImage)
    return background_list

class BackgroundImage(pygame.sprite.Sprite):
    def __init__(self, filename, x_offset, imgWidth, screenWidth):
        super().__init__()

        self.x_offset = x_offset

        self.image = pygame.transform.scale(pygame.image.load(filename), (imgWidth, imgWidth))
        self.rect = self.image.get_rect()
        self.rect.x = x_offset
        self.timer = 0
        self.rect.y = 0

        self.imgWidth = imgWidth
        self.screenWidth = screenWidth

        self.scrollingSpeed = False

        # for x in self.xrepeats:
        #     for layer in self.layers:
        #         self.images[x] = pygame.image.load(layer)
        #         self.rect = self.image.get_rect()
        #         self.rect.x = self.x + x*BG_WIDTH
        #         self.rect.y = self.y

    def update(self,yOffset):
        self.rect.y = yOffset-10
        if self.scrollingSpeed:
            self.timer +=1
            if self.timer > self.scrollingSpeed:
                self.rect.x +=1
                self.timer = 0

                # Rollover
                if self.rect.x > self.screenWidth:
                    self.rect.x = -self.imgWidth+1
        