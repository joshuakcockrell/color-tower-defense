import os
import pygame
pygame.init()

def run():

    width = 750
    height = 600
    res = (width, height)
    screen = pygame.display.set_mode(res)
    clock = pygame.time.Clock()
    fps = 30


    class Credits_Screen(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            

            self.image1 = pygame.Surface((750, 600)) #Width Height
            self.image1.fill((0,0,0)) # fill the surface with RGB
            self.image = self.image1
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

    class Game_Over_Menu(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            #self.image1 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Game Complete Menu','Game Complete.png')).convert()
            self.image2 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Game Complete Menu','Game Complete Title.png')).convert()
            self.image2.set_colorkey(self.image2.get_at((0, 0)))
            self.image = self.image2
            self.rect = self.image.get_rect()
            self.rect.center = (width/2, height/2)
            # i was trying to set it up so that the gameover blinks. but couldnt gifure it out. :(


    class Continue(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image1 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Game Complete Menu','Main Menu Button.png')).convert()
            self.image2 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Game Complete Menu','Main Menu Button selected.png')).convert()
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.starting_alpha = 0
            self.alpha_speed = 2
            self.alpha = self.starting_alpha
            self.image.set_alpha(self.alpha) # cant see it
            
            self.time_till_appear = 240 # delay before we can click the button
            self.clickable = False # we cant click yet
            
        def update(self):
            if self.clickable == False:
                if self.time_till_appear > 0:
                    self.time_till_appear -= 1
                else: # we can now display the button
                    self.clickable = True
            elif self.clickable == True:
                if self.alpha < 255:
                    self.alpha += self.alpha_speed
                self.image = self.image1
                self.rect = self.image.get_rect()
                self.rect.center = (375, 509)

                mouse = pygame.mouse.get_pos()
                if self.rect.collidepoint(mouse):
                    self.image = self.image2
                self.image.set_alpha(self.alpha)
                
    gameover = Game_Over_Menu()
    continue_button = Continue()
    credits_screen = Credits_Screen()

    infoSprites = pygame.sprite.Group(credits_screen, gameover, continue_button)

    credits_screen_delay = 120
            
    running = True
    while running:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = pygame.mouse.get_pos()
                    if continue_button.clickable: # if we can click it yet
                        if continue_button.rect.collidepoint(click):
                            running = False

        
        infoSprites.update()
        infoSprites.draw(screen)

        pygame.display.flip()

        

if __name__ == '__main__':
    run()
    pygame.quit()
