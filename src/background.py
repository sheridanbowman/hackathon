import pygame
import math
from pygame.locals import *

BG_WIDTH = 320

CAVE_BG_WIDTH = 256
CAVE_BG_HEIGHT = 256-32 # force overlap on jagged edge

def newCaveTileRow(screenWidth, screenHeight, depth):
    background_list = []

    totalCaveTilesX = math.ceil(screenWidth/CAVE_BG_WIDTH)+1
    totalCaveTilesY = math.ceil(screenHeight/CAVE_BG_HEIGHT)+1


    for repeatX in range(totalCaveTilesX):
        bgImage = BackgroundImage(filename="assets/cavebackground.png", 
                                    x_offset=CAVE_BG_WIDTH*repeatX, 
                                    y_offset=260+(depth*CAVE_BG_HEIGHT), screenWidth=screenWidth, 
                                    screenHeight=screenHeight, surface=False,
                                    tileNumX=totalCaveTilesX, tileNumY=totalCaveTilesY)
        background_list.append(bgImage)
    return background_list

def initSurfaceBackgroundTileGroup(screenWidth):
    background_list = []
    backgroundScale = 1.25
    backgroundWidth = 320 * backgroundScale
    backgroundRepeats = math.ceil(screenWidth/backgroundWidth)+1
    for filename in ["assets/FREE_Fantasy Forest/Sky.png", 
                    "assets/FREE_Fantasy Forest/Clouds.png",
                    "assets/FREE_Fantasy Forest/Rock Mountains.png",
                    "assets/FREE_Fantasy Forest/Grass Mountains.png"]:
        for repeat in range(backgroundRepeats):
            bgImage = BackgroundImage(filename=filename, x_offset=backgroundWidth*repeat, y_offset=-100, 
                                    imgWidth=backgroundWidth, screenWidth=screenWidth, surface=True)
            if filename.endswith("/Clouds.png"):
                bgImage.scrollingSpeed=14
            if filename.endswith("/Sky.png"):
                bgImage.scrollingSpeed=30
            background_list.append(bgImage)
    return background_list

class BackgroundImage(pygame.sprite.Sprite):
    def __init__(self, filename, x_offset, screenWidth, screenHeight=None, imgWidth=None, y_offset = 0, surface:bool=False, start_offset=0, tileNumX=0, tileNumY=0):
        super().__init__()
        self.surface = surface # Flag for if it's a surface BG object; surface objects dont loop downwards

        self.x_offset = x_offset
        self.y_offset = y_offset

        self.start_offset = start_offset
        
        if self.surface:
            self.image = pygame.transform.scale(pygame.image.load(filename), (imgWidth, imgWidth))
        else:
            self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()

        self.rect.x = x_offset
        self.rect.y = y_offset

        self.timer = 0

        self.imgWidth = imgWidth

        self.screenHeight = screenHeight
        self.screenWidth = screenWidth

        self.scrollingSpeed = False

        self.tileNumX = tileNumX
        self.tileNumY = tileNumY

    def update(self, globalYOffset):

        if self.surface:
            # Surface tiles logic
            self.rect.y = globalYOffset + self.y_offset

            # for scrolling clouds 
            if self.scrollingSpeed:
                self.timer +=1
                if self.timer > self.scrollingSpeed:
                    self.rect.x +=1
                    self.timer = 0

                    # Rollover
                    if self.rect.x > self.screenWidth:
                        self.rect.x = -self.imgWidth+1
        else:
            # Scroll the cave tiles s. offset
            self.rect.y = globalYOffset + self.y_offset  
