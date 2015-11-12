import os
import pygame
from general_stats import *
pygame.init()

def run(player):

    width = 750
    height = 600
    res = (width, height)
    screen = pygame.display.set_mode(res)
    clock = pygame.time.Clock()
    fps = 30

    open_maps = player.open_maps

    background = pygame.Surface(screen.get_size())

    class Select_Menu(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(os.path.join('Resources','Images','Menu Images','Map Select Menu','Select Map.png')).convert()
            self.rect = self.image.get_rect()
            self.rect.topleft = (0,0)

        def update(self):
            pass

    class Map0(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image1 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Map Select Menu','Map0.png')).convert()
            self.image2 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Map Select Menu','Map0(selected).png')).convert()
            self.map_number = 0
            self.open = open_maps[self.map_number]
            
        def update(self):
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (150, height/2.5)

            mouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse):
                self.image = self.image2

    class Map1(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image1 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Map Select Menu','Map1.png')).convert()
            self.image2 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Map Select Menu','Map1(selected).png')).convert()
            self.map_number = 1
            self.open = open_maps[self.map_number]
            
        def update(self):
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (width/2, height/2.5)

            mouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse):
                self.image = self.image2

    class Map2(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image1 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Map Select Menu','Map2.png')).convert()
            self.image2 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Map Select Menu','Map2(selected).png')).convert()
            self.map_number = 2
            self.open = open_maps[self.map_number]
            
        def update(self):
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (width - 150, height/2.5)

            mouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse):
                self.image = self.image2

    class Map3(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image1 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Map Select Menu','Map3.png')).convert()
            self.image2 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Map Select Menu','Map3(selected).png')).convert()
            self.map_number = 3
            self.open = open_maps[self.map_number]
            
        def update(self):
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (150, height - 150)

            mouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse):
                self.image = self.image2

    class Map4(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image1 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Map Select Menu','Map4.png')).convert()
            self.image2 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Map Select Menu','Map4(selected).png')).convert()
            self.map_number = 4
            self.open = open_maps[self.map_number]
            
        def update(self):
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (width/2, height - 150)

            mouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse):
                self.image = self.image2

    class Map5(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image1 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Map Select Menu','Map5.png')).convert()
            self.image2 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Map Select Menu','Map5(selected).png')).convert()
            self.map_number = 5
            self.open = open_maps[self.map_number]
            
        def update(self):
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (width - 150, height - 150)

            mouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse):
                self.image = self.image2
                
    def draw_cover(position):
        image = pygame.image.load(os.path.join('Resources','Images','Menu Images','Map Select Menu','Unknown Map.png')).convert()
        screen.blit(image, position)


    main = Select_Menu()
    map1 = Map0()
    map2 = Map1()
    map3 = Map2()
    map4 = Map3()
    map5 = Map4()
    map6 = Map5()
    infoSprites = pygame.sprite.Group(map1, map2, map3, map4, map5, map6)

    running = True
    pressed_quit = False
    map_number = None

    while running:

        clock.tick(fps)


        infoSprites.clear(screen, background)
        infoSprites.update()

        screen.blit(main.image, main.rect.topleft)
        
        for s in infoSprites:
            if not s.open: # if the map is closed
                draw_cover(s.rect.topleft) # draw a cover on top of it
            else:
                screen.blit(s.image, s.rect.topleft)
                
                
                

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pressed_quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pressed_quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN: # if we click down
                if event.button == 1: # if we left click
                    click = pygame.mouse.get_pos()
                    for s in infoSprites:
                        if s.rect.collidepoint(click):
                            if s.open:
                                map_number = s.map_number
                                running = False # end map selection menu
    return map_number, pressed_quit
