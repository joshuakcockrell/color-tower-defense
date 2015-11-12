import pygame, os

def load_sliced_sprites(w, h, filename):
    '''
    Function:
        Takes one big image and cuts it into smaller
        pieces to be used for animation
    Specs :
        Master can be any height.
        Sprites frames width must be the same width
        Master width must be len(frames)*frame.width
    '''
    images = [] # create empty images list
    master_image = pygame.image.load(os.path.join('', filename)).convert_alpha() # load image to be cut

    master_width, master_height = master_image.get_size() # get full image sixe
    for i in xrange(int(master_width/w)): # cut the image up
        images.append(master_image.subsurface((i*w,0,w,h))) # add images to list
    return images # sent the images list
