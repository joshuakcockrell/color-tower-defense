import os
import pygame
pygame.init()

def run():

    width = 750
    height = 600
    res = (width, height)
    screen = pygame.display.set_mode(res)
    clock = pygame.time.Clock()
    fps = 50

    background = pygame.Surface(screen.get_size())

    class Name(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image1 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Main Menu','Color Tower Defense copy2.png')).convert()
            self.image = self.image1
            self.image.set_colorkey((0,255,255)) # transparent blue color
            self.rect = self.image.get_rect()
            self.rect.center = (width/2, height/2)
            
        def update(self):
            pass

    class Color(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(os.path.join('Resources','Images','Menu Images','Main Menu','Color copy.png')).convert()
            self.image2 = self.image
            self.image3 = self.image
            self.rect = self.image.get_rect()
            self.rect2 = self.image2.get_rect()
            self.rect3 = self.image3.get_rect()
            self.rect.topleft = (0,0)
            self.rect2.topleft = (690,0)
            self.rect3.topleft = (-690,0)
            self.speed = 2
            
        def update(self):
            self.rect.centerx += self.speed
            self.rect2.centerx += self.speed
            self.rect3.centerx += self.speed
            
            if self.rect.left >= screen.get_width():
                self.reset(self.rect)
            if self.rect2.left >= screen.get_width():
                self.reset(self.rect2)
            if self.rect3.left >= screen.get_width():
                self.reset(self.rect3)

        def draw(self):
            screen.blit(self.image, self.rect)
            screen.blit(self.image2, self.rect2)
            screen.blit(self.image3, self.rect3)
            
        
        def reset(self, rect):
            
            rect.left = -1320
        

    class Play_Game(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image1 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Main Menu','Play.png')).convert()
            self.image2 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Main Menu','Play Red.png')).convert()
            self.image1.set_colorkey(self.image1.get_at((11, 11))) # transparent
            self.image2.set_colorkey(self.image2.get_at((11, 11))) # transparent

        def update(self):
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (195, 509)

            mouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse):
                self.image = self.image2

                
    class Exit_Game(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image1 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Main Menu','Quit.png')).convert()
            self.image2 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Main Menu','Quit Red.png')).convert()
            self.image1.set_colorkey(self.image1.get_at((0, 0))) # transparent
            self.image2.set_colorkey(self.image2.get_at((0, 0))) # transparent

        def update(self):
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (555, 509)

            mouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse):
                self.image = self.image2

    class Credits_Button(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

            self.text = 'credits'
            self.font = pygame.font.Font(os.path.join('Resources','Fonts','m04.ttf'), 42)
            self.image1 = self.font.render(self.text, 1, (255, 255, 255))
            self.image2 = self.font.render(self.text, 1, (255, 0, 0))
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.topright = (750,0)

        def update(self):
            self.image = self.image1
            mouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse):
                self.image = self.image2
    '''
    class Cover(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            
            self.image = pygame.Surface((750, 600)) #Width Height
            self.image.fill((0,0,0)) # fill the surface with RGB
            self.rect = self.image.get_rect()
            self.rect.topleft = (0,0)# where the button is displayed
            self.starting_alpha_value = 0
            self.alpha_value = self.starting_alpha_value
            self.alpha_speed = 7
            self.max_alpha_value = 180
            self.image.set_alpha(self.alpha_value)
            self.fading_in = False
            self.fading_out = False

        def update(self):
            if self.fading_in:
                if self.alpha_value < self.max_alpha_value:
                    self.alpha_value += self.alpha_speed

            if self.fading_out:
                if self.alpha_value > 0:
                    self.alpha_value -= self.alpha_speed
                    
            self.image.set_alpha(self.alpha_value)

        def display_on(self):
            self.fading_in = True
            self.fading_out = False

        def display_off(self):
            self.fading_in = False
            self.fading_out = True
    '''


    class Credits_Screen(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            

            self.image1 = pygame.Surface((750, 600)) #Width Height
            self.image1.fill((0,0,0)) # fill the surface with RGB
            self.image = self.image1
            #self.image.set_colorkey((0,0,0)) # transparent
            self.rect = self.image.get_rect()
            self.rect.topleft = (0,0)# where the button is displayed
            self.font = pygame.font.Font(os.path.join('Resources','Fonts','Microsoft Sans Serif.ttf'), 14)
            
            self.text1 = 'Josh Cockrell - Technical Director, Systems Architect, Design, Gameplay, Audio, Art'
            self.text2 = 'Tyler Christensen - Music, Art'
            self.text3 = 'Tess Bybee - Art'
            self.text4 = 'Chris Breinholt - Critical decision choices concerning white colored robots. (Among other things)'
            self.text5 = 'Special Thanks - Dr0id, HydroKirby, EmCeeMayor, nClam, Eli Benderski, exarcun'
            self.text6 = '                            themissinglint, lolrus, Ryan Brown'

            self.text_surface1 = self.font.render(self.text1, 1, (255,255,255))
            self.text_surface2 = self.font.render(self.text2, 1, (255,255,255))
            self.text_surface3 = self.font.render(self.text3, 1, (255,255,255))
            self.text_surface4 = self.font.render(self.text4, 1, (255,255,255))
            self.text_surface5 = self.font.render(self.text5, 1, (255,255,255))
            self.text_surface6 = self.font.render(self.text6, 1, (255,255,255))

            self.image.blit(self.text_surface1, (40,260))
            self.image.blit(self.text_surface2, (40,280))
            self.image.blit(self.text_surface3, (40,300))
            self.image.blit(self.text_surface4, (40,320))
            self.image.blit(self.text_surface5, (40,340))
            self.image.blit(self.text_surface6, (40,360))
            
            self.image.set_alpha(0)


        def display_on(self):
            self.image.set_alpha(255)

        def display_off(self):
            self.image.set_alpha(0)
            



    play = Play_Game()
    color = Color()
    exit = Exit_Game()
    name = Name()
    credits_button = Credits_Button()
    credits_screen = Credits_Screen()
    
    infoSprites = pygame.sprite.LayeredUpdates(name, play, exit, credits_button, credits_screen)

    running = True
    not_quitting = True
    viewing_credits = False
    while running:
        clock.tick(fps)

        infoSprites.update()

        color.update()
        color.draw()
        infoSprites.draw(screen)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                not_quitting = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = pygame.mouse.get_pos()
                    if viewing_credits:
                        viewing_credits = False
                        credits_screen.display_off()
                        
                    if play.rect.collidepoint(click):
                        running = False
                        
                    elif exit.rect.collidepoint(click):
                        running = False
                        not_quitting = False
                        
                    elif credits_button.rect.collidepoint(click):
                        viewing_credits = True
                        credits_screen.display_on()

    return not_quitting

if __name__ == '__main__':
    print run()
    pygame.quit()
