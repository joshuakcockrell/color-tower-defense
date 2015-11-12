import os
import pygame
pygame.init()

def run():

    width = 750
    height = 600
    res = (width, height)
    screen = pygame.display.set_mode(res)
    cover = pygame.Surface(screen.get_size())
    cover.fill((0,0,0))
    cover_alpha = 255
    alpha_speed = 4

    clock = pygame.time.Clock()
    fps = 30
    TIMER = (3 * fps) # runs for three seconds 
    timer = TIMER


    class Mad_Cloud_Games_Logo(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(os.path.join('Resources','Images','Menu Images','Mad Cloud Games Menu','Logo with Words.png')).convert()
            self.rect = self.image.get_rect()
            self.rect.center = (width/2, height/2)

    logo = Mad_Cloud_Games_Logo()
    infoSprites = pygame.sprite.Group(logo)
    
    not_quitting = True
    running = True

    while running:
        clock.tick(30)

        
        
        timer -= 1
        if timer >= 0:
            cover_alpha -= alpha_speed # make the cover more transparent
            
        elif timer <= 0: # more covered
            cover_alpha += alpha_speed
            if cover_alpha >= 255:
                timer = TIMER
                running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                not_quitting = False
                        

        screen.fill((255,255,255))
        infoSprites.update()
        infoSprites.draw(screen)
        
        cover.set_alpha(cover_alpha)
        screen.blit(cover,(0,0))

        pygame.display.flip()
    return not_quitting

if __name__ == '__main__':
    print run()
    pygame.quit()
