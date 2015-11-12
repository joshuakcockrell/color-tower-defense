from general_stats import *
from wave_stats import *
from object_groups import *
from music import *
def reset(player):
    '''
    Function:
        Clears all the game elements and resets everything so
        we can start the game over
    '''
    player.money = player.MONEY # reset money
    player.life = player.LIFE # reset life
    player.game_over = False
    music.reset()

    wave.creating_wave = False # we are not creating a wave anymore
    wave.wave_done = True
    wave.last_wave = False
    wave.wave_ammount = None # reset number of enemies that are waiting to come
    wave.wave_type = None
    wave.map_enemies = None # holds enemies for which map we are currently on
    wave.current_wave = 0
    wave.life_multiplier = wave.LIFE_MULTIPLIER
        
    for o in all_objects:
        o.kill() # destroy every sprite thats in the all group

