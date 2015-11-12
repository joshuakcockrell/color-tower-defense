from general_stats import *
def snap_to_grid(position):
    '''
    recieves a position and changes it so that the position is
    centered to the nearest tile
    '''
    x = position[0] # get value
    x //= tile # break down into ammount of tiles two division signs rounds to the nearest integer
    x *= tile # multiply tiles into pixels again
    x += (tile/2) # add value to reach the center of the tile
    
    y = position[1]
    y //= tile
    y *= tile
    y += (tile/2)


    return (x,y)

def tile_position(position): # this function is not used
    '''
    changes a position from pixels to tiles
    '''
    x = position[0] # get value
    x //= tile # break down into ammount of tiles two division signs rounds to the nearest integer

    y = position[1]
    y //= tile
