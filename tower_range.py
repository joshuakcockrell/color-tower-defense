import pygame
from snap_to_grid import *

##### Range circle #####
class Tower_Range(pygame.sprite.Sprite):
    def __init__(self, location, tower_range):

        pygame.sprite.Sprite.__init__(self, self.groups)
        self.range = tower_range  
        self.image = pygame.Surface((self.range*2, self.range*2)) # create a box surface
        self.image.fill((255, 255, 255)) # fill the image with RGB
        self.image.set_colorkey(self.image.get_at((0, 0))) # make the white transparent
        self.rect = self.image.get_rect()
        self.rect.center = location # draw it at the location
        pygame.draw.circle(self.image, (0, 200, 0), ((int(self.range),int(self.range))), int(self.range), 2) # draw the circle inside the box

    def move(self, position):
        grid_position = snap_to_grid(position)
        self.rect.center = grid_position

