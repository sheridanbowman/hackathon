class staticTile:
    def __init__(self, enemySpawn=False, 
                 default: bool = False, treasure: bool = False, 
                 gem: bool = False, empty:bool = False, grass:bool = False, 
                 coords:tuple[int, int] = (0,0)):
        self.enemySpawn = enemySpawn
        self.default = default
        self.treasure = treasure
        self.gem = gem
        self.empty = empty
        self.grass = grass
        self.coords = coords
    
        self.debugColor = (0,0,0)

        if enemySpawn == "Ghost":
            self.debugColor = (192, 192, 192)
        if enemySpawn == "Default":
            self.debugColor = (255, 0, 0)
        if default:
            self.debugColor = (139, 69, 19)
        if treasure:
            self.debugColor = (255, 255, 0)
        if gem:
            self.debugColor = (255, 0, 255)
        if empty:
            self.debugColor = False
        if grass:
            self.debugColor =  (0, 255, 0)
        
            
        