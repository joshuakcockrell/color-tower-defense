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

    background = pygame.Surface(screen.get_size())

    class Game_Over_Menu(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image1 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Map Complete Menu','Map Complete.png')).convert()
            # i was trying to set it up so that the gameover blinks. but couldnt gifure it out. :(
            
        def update(self):
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (width/2, height/2)

    class Continue(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image1 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Map Complete Menu','continue.png')).convert()
            self.image2 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Map Complete Menu','continue selected.png')).convert()
            
        def update(self):
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (375, 509)

            mouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse):
                self.image = self.image2
            
    running = True
    while running:
        clock.tick(fps)

        gameover = Game_Over_Menu()
        back = Continue()

        infoSprites = pygame.sprite.Group(gameover, back)

        infoSprites.clear(screen, background)
        infoSprites.update()
        infoSprites.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = pygame.mouse.get_pos()
                    if back.rect.collidepoint(click):
                        running = False

if __name__ == '__main__':
    run()
    pygame.quit()
