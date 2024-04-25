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
from staticTile import staticTile

# How many tiles per chunk, in X Y axis
TILES_PER_CHUNK_WIDTH = 40
TILES_PER_CHUNK_HEIGHT = 50

TILE_PX_SIZE = 20

CAVE_BG = "example.png"
SURFACE_BG ="example2.png"




# Initialize a random tileChunk
# Produces X% of each tile type, determined by Depth, and shuffles into 2D array for chunk
def createProceduralChunk(depth:int):
    # TODO safety check to ensure whatever rates dont surpass total number of tiles per chunk at extreme depths
    totalTiles = TILES_PER_CHUNK_WIDTH * TILES_PER_CHUNK_HEIGHT
    chunk = tileChunk(depth, CAVE_BG)
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

    # print(len(unsortedTiles))
    remainingTiles = totalTiles - (treasureCavernRate + defaultEnemyCavernRate + ghostEnemySpawnRate)
    # print(remainingTiles, totalTiles, treasureCavernRate, defaultEnemyCavernRate, ghostEnemySpawnRate)
    
    # Gems default to 33% remainder, scales by depth 10 becomes 100% remainder
    gemTiles = int((0.33 * remainingTiles) + (depth * 0.066))
    for _ in range(gemTiles):
        unsortedTiles.append(staticTile(gem=True))

    defaultTiles = remainingTiles - gemTiles
    for _ in range(int(defaultTiles)):
        unsortedTiles.append(staticTile(default=True))

    # Randomize and stack into 2d
    # additionally, assigns X/Y positions to each tile
    random.shuffle(unsortedTiles)
    
    randomTileArray = []
    y_pos = 0
    for i in range(0, totalTiles, TILES_PER_CHUNK_WIDTH):
        row = []
        x_pos = 0
        for tile in unsortedTiles[i:i+TILES_PER_CHUNK_WIDTH]:
            tile.coords = (x_pos, y_pos)
            row.append(tile)
            x_pos += TILE_PX_SIZE
        randomTileArray.append(row)
        y_pos += TILE_PX_SIZE

    
    chunk.tilesArray = randomTileArray
    return chunk

# Initialize custom chunk
# Defaults to 'beginning chunk' if not fed a custom 2d array
def createCustomChunk(customArray=False):
    chunk = createProceduralChunk(0)
    chunk.backgroundImage = SURFACE_BG
    if customArray:
        chunk.tilesArray = customArray
    else:
        # Fill the first 1/4 with empty space, then a row of grass
        startSpace = int(TILES_PER_CHUNK_HEIGHT*0.25)
        yPos = 0
        for rowIndex in range(startSpace+1):
            row = []
            xPos = 0
            for _ in range(TILES_PER_CHUNK_WIDTH):
                if rowIndex == startSpace:
                    localTile = staticTile(grass=True, coords=(xPos, yPos))
                else:
                    localTile = staticTile(empty=True, coords=(xPos, yPos))
                row.append(localTile)
                xPos+=TILE_PX_SIZE
            yPos+=TILE_PX_SIZE
            chunk.tilesArray[rowIndex] = row
            # chunk.tilesArray[x] = [staticTile(grass=True) for _ in range(TILES_PER_CHUNK_WIDTH)]

            
        # chunk.tilesArray[startSpace] = [staticTile(grass=True) for _ in range(TILES_PER_CHUNK_WIDTH)]

    return chunk

# Chunk class
class tileChunk:
    # depth: determines RNG for treasure, monster spawn frequency, tile color variance
    # background: Path of image to load behind tiles
    # tilesArray: initialized array to hold tile assignments
    def __init__(self, depth: int, backgroundImage: str):
        self.depth = depth
        self.backgroundImage = backgroundImage
        self.tilesArray = None

    
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

