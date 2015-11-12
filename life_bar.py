import pygame
from general_stats import *


class Life_Bar(pygame.sprite.Sprite):
    '''draws a life bar over the sprites head
    '''

    def __init__(self, starting_life, life, position, height, width):
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.bar_height = 4
        self.bar_width = 16
        self.health_percent = starting_life / life
        
        self.image = pygame.Surface((self.bar_width, self.bar_height))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.host_height = height
        self.host_width = width
        
        self.rect.center = (position[0] - (width / 4)), (position[1] - height)
        self.starting_life = starting_life
        
    def is_dead(self):
        self.kill()
        
    def update(self, starting_life, life, position):
        self.health_percent = starting_life / life
        
        self.image.fill((255,0,0)) # fill with red
        self.image.fill((0,255,0), # green
                    (0,0,(self.bar_width / self.health_percent), self.bar_height)) # size of green

        self.rect.center = position[0], (position[1] - self.host_height)

        
'''       
def draw_life_bar(starting_health, health, position, height, width):
     draws a life bar over the sprites head 

    health_bar_x = position[0] - (width / 4)
    health_bar_y = position[1] - height# - 6
    
    health_percent = (starting_health / health)
    
    bar_image.fill((255,0,0)) # fill the bar with red
    bar_image.fill((0,255,0), # green
                    (0,0,(bar_width / health_percent), bar_height)) # size of green

    screen.blit(bar_image,(health_bar_x, health_bar_y))
    '''
