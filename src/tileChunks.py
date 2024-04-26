# Chunk Logic for procedural gen / ‘custom’ level (Sheridan) 
# 	Background for 1 default level, ‘default dirt’ darker for everything below that
# 	Chunk logic 2d array of “tile” objects

# 	Semi random assignment of different ‘objects’ : controlled by depth
# 		Deeper gives you more monsters, more treasure 

# 	Option for taking preauthored ‘custom’ level array (starting level default first chunk)

# 	Initialize random after that

# 	when/where enemies spawn
# 		Default monsters in cavities
import random
import math
from src.staticTile import staticTile

# TODO: backgrounds per chunk
# TODO: ensure monster / treasure rng assignment never occurs on consecutive rows to prevent double caverns
# TODO: createCustomChunk gets Depth offset to Y values if custom array is used
# TODO: populate self.enemySpawns with enemy objects 
# TODO: enemy spawns also part of treasure chest cavities
# TODO: createProceduralChunk: safety check to ensure whatever rates dont surpass total number of tiles per chunk at extreme depths

# How many tiles to draw outside of chunk as border
EXTRA_TILES_BOUNDARY_BUFFER = 1

CAVE_BG = "assets/placeholderCaveBG.png"
SURFACE_BG ="assets/placeholderSurfaceBG.png"

# Determines chunk dimensions based on input Display resolution, pixel dimensions
# sets global vars once, for remaining functions to reference
tilesPerChunkWidth = None
tilesPerChunkHeight = None
tilesSize = None
def setChunkDims(displayWidth:int, displayHeight:int, tileSize:int):
    global tilesPerChunkWidth
    global tilesPerChunkHeight
    global tilesSize
    tilesPerChunkWidth = math.ceil(displayWidth / tileSize)
    tilesPerChunkHeight = math.ceil(displayHeight / tileSize)
    tilesSize = tileSize

# Initializes a random tileChunk
# Produces X% of each tile type, determined by Depth, and shuffles into 2D array for chunk
# addCavernsLater: Flag to skip 'adding caverns', if it's expected to be handled in Custom array after more adds 
def createProceduralChunk(depth:int=0, addCavernsLater=False):
    totalTiles = tilesPerChunkWidth * tilesPerChunkHeight
    newChunk = tileChunk(depth, CAVE_BG)
    unsortedTiles = []
        
    ghostEnemySpawnRate = depth*3.0
    for _ in range(int(ghostEnemySpawnRate)):
        unsortedTiles.append(staticTile(enemySpawn="Ghost"))

    # flags creation of a small cavern, with just an enemy
    defaultEnemyCavernRate = (1+depth)*3.0 
    for _ in range(int(defaultEnemyCavernRate)):
        unsortedTiles.append(staticTile(enemySpawn="Default"))

    # flags creation of a small cavern, with an enemy + treasure
    treasureCavernRate = (1+depth)*3.0
    for _ in range(int(treasureCavernRate)):
        unsortedTiles.append(staticTile(treasure=True))

    remainingTiles = totalTiles - (treasureCavernRate + defaultEnemyCavernRate + ghostEnemySpawnRate)
    
    # Gems default to 33% remainder, scales by depth 10 becomes 100% remainder
    gemTiles = int((0.33 * remainingTiles) + (depth * 0.066))
    for _ in range(gemTiles):
        unsortedTiles.append(staticTile(gem=True))

    defaultTiles = remainingTiles - gemTiles
    for _ in range(int(defaultTiles)):
        unsortedTiles.append(staticTile(default=True))

    # All tiles initialized; Randomize and stack into 2d, assign X/Y coords
    random.shuffle(unsortedTiles)
    randomTileArray = []

    # Current position starts at bottom of last chunk
    yPos = depth * tilesPerChunkHeight * tilesSize
    for i in range(0, totalTiles, tilesPerChunkWidth):
        row = []
        
        # Add buffer tile(s) w. negative offset to start
        for x in range(EXTRA_TILES_BOUNDARY_BUFFER):
            bufferXPos = (x+1) * tilesSize * -1
            row.append(staticTile(boundary=True, coords=(bufferXPos, yPos)))

        # Add main tiles
        xPos = 0
        for tile in unsortedTiles[i:i+tilesPerChunkWidth]:
            tile.coords = (xPos, yPos)
            row.append(tile)
            xPos += tilesSize

        # Add buffer tile(s) w. normal offset to end
        for x in range(EXTRA_TILES_BOUNDARY_BUFFER):
            row.append(staticTile(boundary=True, coords=(xPos, yPos)))
            xPos += tilesSize
        
        randomTileArray.append(row)
        yPos += tilesSize

    # Tilearray is complete and randomized
    if addCavernsLater:
        newChunk.tilesArray = randomTileArray
    else:
        newChunk.tilesArray = addCaverns(randomTileArray)
    return newChunk

# go back over rows and subtract caverns for treasure / monsters. Add monster flag for treasure room
def addCaverns(tileArray):
    for row in tileArray:
        index = 0
        tileIndiciesToCut = []
        for localTile in row:
            if localTile.treasure==True or localTile.enemySpawn == "Default":
                numSpaces = random.randint(3, 7)
                offsetRoot = random.randint(0, (numSpaces-1))
                for x in range(numSpaces):
                    tileIndiciesToCut.append((index-offsetRoot)+x)
            index +=1

        # Empty tiles determined, swap out of row if its not a boundary tile
        for index in tileIndiciesToCut:
            if (index >= 0) and (index < len(row)): # Safety for slim chance of oob index
                lastTile = row[index]
                if lastTile.boundary == False:
                    row[index] = staticTile(empty=True, coords=lastTile.coords)
    return tileArray

# Initialize custom chunk
# Defaults to 'beginning chunk' if not fed a custom 2d array
def createCustomChunk(depth:int=0, customArray=False):
    chunk = createProceduralChunk(0, addCavernsLater=True)
    chunk.backgroundImage = SURFACE_BG
    if customArray:
        exit("TODO: customArray gets Depth offset to Y values if used")
        chunk.tilesArray = customArray
    else:
        # Fill the first 1/4 with empty space, then a row of grass
        startSpace = int(tilesPerChunkHeight*0.25)
        yPos = depth * tilesPerChunkHeight * tilesSize
        for rowIndex in range(startSpace+1):
            row = chunk.tilesArray[rowIndex]
            xPos = 0
            # Offset rows by buffer to preserve boundary
            for itemIndex in range(EXTRA_TILES_BOUNDARY_BUFFER, len(row)-1):
                if rowIndex == startSpace:
                    localTile = staticTile(grass=True, coords=(xPos, yPos))
                else:
                    localTile = staticTile(empty=True, coords=(xPos, yPos))
                row[itemIndex] = localTile
                xPos+= tilesSize
            yPos+= tilesSize
            chunk.tilesArray[rowIndex] = row

        # Add a cap of Boundary boxes above player, same coords as first row, but offset
        capRow = []
        for tileReference in chunk.tilesArray[0]:
            capRow.append(staticTile(boundary=True, coords=(tileReference.coords[0], tileReference.coords[1]-tilesSize)))
        chunk.tilesArray.append(capRow)

        # If no cavern within first 3 rows, force treasure room on row 3
        soonCavern = False
        for index in range(startSpace+1, startSpace+4):
            for localTile in chunk.tilesArray[index]:
                if localTile.treasure or localTile.enemySpawn=="Default":
                    soonCavern = True
                    print("found cavern", index)
                    break
            if soonCavern:
                break

        if not soonCavern:
            print("no cavern found, adding cavern", startSpace+3, tilesPerChunkWidth//2)
            lastTile = chunk.tilesArray[startSpace+3][tilesPerChunkWidth//2]
            chunk.tilesArray[startSpace+3][tilesPerChunkWidth//2] = staticTile(treasure=True, coords=lastTile.coords)

    chunk.tilesArray = addCaverns(chunk.tilesArray)

    return chunk

# Chunk class
class tileChunk:
    # depth: determines RNG for treasure, monster spawn frequency, tile color variance
    # background: Path of image to load behind tiles
    # tilesArray: initialized array to hold tile assignments
    # enemySpawns: list of enemy spawns to initialize on chunk load
    def __init__(self, depth: int, backgroundImage: str):
        self.depth = depth
        self.backgroundImage = backgroundImage
        self.tilesArray = None
        self.enemySpawns = None
        self.tilesPerChunkHeight = tilesPerChunkHeight
    
    # Returns a FLATTENED list of tiles by default, or the internal 2D array, if needed for w.e reason
    def getTiles(self, returnFlattened=True) -> list:
        if returnFlattened:
            flattenedList = []
            for row in self.tilesArray:
                for item in row:
                    flattenedList.append(item)
            # print(len(flattenedList))
            return flattenedList
        else:
            return self.tilesArray

