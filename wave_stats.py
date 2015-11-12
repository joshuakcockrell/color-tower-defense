from general_stats import *
from sprite_stats import *
from object_groups import *

class Wave():
    def __init__(self): # 30/10
        self.NEW_ENEMY = 30 # ammount of time between enemies
        self.new_enemy = self.NEW_ENEMY # so we can reset the time
        self.CURRENT_WAVE = 0
        self.current_wave = self.CURRENT_WAVE
        self.total_waves = 50 # max number of waves
        self.creating_wave = False # we are not creating a wave
        self.wave_done = True # the wave is over
        self.last_wave = False # we are not on our last wave
        self.wave_type = None # what kind of enemy is coming this wave
        self.LIFE_MULTIPLIER = 1
        self.life_multiplier = self.LIFE_MULTIPLIER
        self.life_multiplier_multiplier = .6 # higher is harder enemies

        self.map_enemies = None # holds enemies for which map we are currently on
        self.all_maps = [] # holds all map enemies
        n = 'basic' # normal sorry cause b is taken by boss
        s = 'slow'
        f = 'fast'
        b = 'boss'
        z = 'zombie'
        #bn = boss normal
        #bb = secret

                     #1 2 3 4 5 6 7 8 9 0
        self.map_1 = [n,n,n,s,n,s,n,s,f,n]
        
        self.map_2 = [n,n,s,f,n,n,f,f,s,b,
                      f,f,s,n,n,f,n,s,n,b]

        self.map_3 = [n,s,f,f,s,f,s,n,s,s,
                      s,s,f,s,f,s,f,f,n,b]

        self.map_4 = [n,n,s,s,f,n,b,n,f,b, # 1-10
                      n,f,s,n,f,s,n,n,f,b,
                      f,n,f,n,s,f,n,n,f,b]

        self.map_5 = [n,n,s,n,b,b,n,n,f,n, # 1-10
                      n,n,s,f,f,s,n,n,f,z,
                      n,f,s,n,s,s,f,n,f,z,
                      n,n,f,s,f,f,s,s,b,b]
        
        self.map_6 = [n,n,s,n,s,s,n,f,f,f,
                      s,f,s,b,b,n,s,f,b,b,
                      n,b,b,z,z,f,z,s,f,z,
                      b,f,f,s,n,b,z,f,s,b,
                      n,s,f,s,f,b,z,z,b,z]
        

        self.all_maps.extend([self.map_1] + [self.map_2] + [self.map_3] + [self.map_4] + [self.map_5] + [self.map_6])

    def start_new_map(self, map_number):
        self.map_enemies = self.all_maps[map_number]

    def start_new_wave(self):
        self.creating_wave = True
        self.wave_done = False
        self.wave_type = self.map_enemies[self.current_wave]
        self.current_wave += 1

        self.WAVE_AMMOUNT = enemy_stats(self.wave_type, 'wave_stats') # get stats using enemy_stats
        self.wave_ammount = self.WAVE_AMMOUNT # so we can reset the ammount
        
    def increase_difficulty(self):
        self.life_multiplier += (self.current_wave * self.life_multiplier_multiplier)

    def finish_wave(self):
        self.increase_difficulty() # make the next wave harder

        self.creating_wave = False # we are not creating a wave anymore
        self.wave_done = True # we can create more waves
        self.wave_ammount = wave.WAVE_AMMOUNT # reset number of enemies that are waiting to come
        
        if self.current_wave >= len(self.map_enemies): # if we finished the last wave
            self.wave_done = False # we cannot create any more waves
            self.last_wave = True
        

    def update(self, player): # runs every frame

        if self.last_wave: # if we are on the last wave
            if len(enemies) <= 0: # when all the enemies die
                player.game_won = True # YOU WIN!!! this needs to be
                
        else: # if there are more waves
            if wave.creating_wave == True: # when we want to create a new wave
                self.new_enemy -= 1 # counts down time between enemies
                if self.new_enemy <= 0: # when we need to create a new enemy
                    self.new_enemy = wave.NEW_ENEMY # resets timer for next enemy
                    self.wave_ammount -= 1 # counts down till no more enemies left in wave

                    if not self.wave_ammount < 0: # if there are more enemies left to come
                        return True # create an enemy

                    else: # if no more enemies are coming for this wave
                        self.finish_wave() # finish the wave

wave = Wave() # enemy wave stats
