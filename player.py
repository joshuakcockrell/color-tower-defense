class Player(): # all the info for the player
    def __init__(self): # 300
        self.MONEY = 100 # player's money default 100
        self.money = self.MONEY # so we can reset the money
        self.LIFE = 10 # player's life
        self.life = self.LIFE # so we can reset the life when the game is over
        self.map = None # the map that we are playing on
        self.game_over = False
        self.game_won = False
        self.quiting = False
        o = True # open map
        c = False # closed map
        self.open_maps = [o,c,c,c,c,c]
        #self.open_maps = [o,o,o,o,o,o]
        self.difficulty = None # it has not been set yet

    def open_new_map(self):
        self.open_maps[self.map + 1] = True
