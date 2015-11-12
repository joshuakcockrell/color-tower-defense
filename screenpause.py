import os
import pygame
pygame.init()

def run():

    width = 750
    height = 600
    res = (width, height)
    screen = pygame.display.set_mode(res)
    clock = pygame.time.Clock()
    fps = 40

    background = pygame.Surface(screen.get_size())

    class Paused(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image1 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Pause Menu','Game Paused copy.png')).convert()

        def update(self):
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (width/2, height/2)

    class Play_Game(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image1 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Pause Menu','resume.png')).convert()
            self.image2 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Pause Menu','resume selected.png')).convert()

        def update(self):
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (366, 509)

            mouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse):
                self.image = self.image2
                
    running = True
    not_quitting = True
    while running:
        clock.tick(fps)

        paused = Paused()
        play = Play_Game()

        infoSprites = pygame.sprite.Group(paused, play)
        
        infoSprites.clear(screen, background)
        infoSprites.update()
        infoSprites.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                not_quitting = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = pygame.mouse.get_pos()
                    if play.rect.collidepoint(click):
                        running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_p]:
                    running = False
                    not_quitting = True

    return not_quitting

if __name__ == '__main__':
    print run()
    pygame.quit()
