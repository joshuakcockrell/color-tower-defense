import pygame
from load_sliced_sprites import *

##### Explosions #####

class Explosion(pygame.sprite.Sprite):

    

    def __init__(self, position):
        
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.explosion_images = load_sliced_sprites(50, 50, os.path.join('Resources','Images','Animations','explosiontileset.png'))
        for image in self.explosion_images:
                image.set_colorkey(image.get_at((0, 0))) # issues here suppost to make transparent
        self.frame = 0 # starting image
        self.image = self.explosion_images[self.frame] # use frame to get correct image
        self.rect = self.image.get_rect()
        self.NEW_IMAGE = 3 # time between images
        self.new_image = self.NEW_IMAGE # so we can reset the timer
        self.rect.center = position # center = position that was recieved when we called this 


    def update(self, player):
        self.new_image -= 1 # count down till next image is used
        if self.new_image <= 0: # when we need to change the image
            self.frame += 1 # switch to next image
            self.new_image = self.NEW_IMAGE # reset image timer
            
        if self.frame >= (len(self.explosion_images) - 1): # when we run out of images
            self.kill() # die you wasteful explosion
        self.image = self.explosion_images[self.frame] # pick the image based on what frame we are on
