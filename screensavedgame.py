import os
import pygame
import pickle
from player import *
#from general_stats import *
pygame.init()

def run():

    width = 750
    height = 600
    res = (width, height)
    screen = pygame.display.set_mode(res)
    clock = pygame.time.Clock()
    fps = 30

    background = pygame.Surface(screen.get_size())

    class Load_Game(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(os.path.join('Resources','Images','Menu Images','Load Game Menu','Load Game Background.png')).convert()
            self.rect = self.image.get_rect()
            self.rect.topleft = (0,0)
            
        def update(self):
            pass

    class Saved_Game0(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image1 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Load Game Menu','Save File 1.png')).convert()
            self.image2 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Load Game Menu','Save File 1 (selected).png')).convert()
            self.saved_game_number = 0

        def is_clicked(self):
            if not test_if_open(self.saved_game_number): # if the save file exists
                player_data = Player()
                create_file(self.saved_game_number, player_data)
            return load_game(self.saved_game_number)

        def delete_file(self): # creates a new save file ontop of the previous one
            player_data = Player()
            create_file(self.saved_game_number, player_data)
            
                                
        def update(self):
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (150, height/2.5)

            mouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse):
                self.image = self.image2

    class Saved_Game1(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image1 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Load Game Menu','Save File 2.png')).convert()
            self.image2 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Load Game Menu','Save File 2 (selected).png')).convert()
            self.saved_game_number = 1

        def is_clicked(self):
            if not test_if_open(self.saved_game_number): # if the save file exists
                player_data = Player()
                create_file(self.saved_game_number, player_data)
            return load_game(self.saved_game_number)

        def delete_file(self): # creates a new save file ontop of the previous one
            player_data = Player()
            create_file(self.saved_game_number, player_data)
            
        def update(self):
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (375, height/2.5)

            mouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse):
                self.image = self.image2

    class Saved_Game2(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image1 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Load Game Menu','Save File 3.png')).convert()
            self.image2 = pygame.image.load(os.path.join('Resources','Images','Menu Images','Load Game Menu','Save File 3 (selected).png')).convert()
            self.saved_game_number = 2

        def is_clicked(self):
            if not test_if_open(self.saved_game_number): # if the save file doesnt exist
                player_data = Player()
                create_file(self.saved_game_number, player_data)
                return load_game(self.saved_game_number)
            return load_game(self.saved_game_number)

        def delete_file(self): # creates a new save file ontop of the previous one
            player_data = Player()
            create_file(self.saved_game_number, player_data)
            
        def update(self):
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (600, height/2.5)

            mouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse):
                self.image = self.image2

    class Black_Cover(pygame.sprite.Sprite):
    #covers the background so menus can appear on top of it

        def __init__(self):
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.image = pygame.Surface((750,600))
            self.image.fill ((0,0,0))
            self.rect = self.image.get_rect()
            self.rect.topleft = (0,0)
            self.starting_alpha = 255
            self.image.set_alpha(self.starting_alpha)

        def cover_on(self):
            self.image.set_alpha(150)

        def cover_off(self):
            self.image.set_alpha(self.starting_alpha)

    class Difficulty_Choice(pygame.sprite.Sprite):
        # the text that is all like "what difficulty do you want to choose!$@&^"

        def __init__(self):
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.image1 = pygame.Surface((450, 100))

            self.text = 'difficulty'
            self.font = pygame.font.Font(os.path.join('Resources','Fonts','m04.ttf'), 42)
            self.text_surface = self.font.render(self.text, 1, (255, 255, 255))
            self.image1.blit(self.text_surface, (10,10))

            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (375, 200)
            

    class Easy_Button(pygame.sprite.Sprite):
        # lol :]
        # funny name
        # if you get what im saying :)
        def __init__(self):
            pygame.sprite.Sprite.__init__(self, self.groups)

            self.image1 = pygame.Surface((260, 100))
            self.image1_front = pygame.Surface((256, 96))
            self.image1_front.fill((0,0,0))
            self.image1.fill((255,255,255))
            self.image1.blit(self.image1_front, (2,2))
            self.image2 = pygame.Surface((260, 100)) 
            self.image2_front = pygame.Surface((256, 96))
            self.image2_front.fill((24, 196, 40)) # fill the surface with RGB
            self.image2.fill((255,255,255))
            self.image2.blit(self.image2_front, (2,2))

            self.text = 'easy'
            
            self.font = pygame.font.Font(os.path.join('Resources','Fonts','m04.ttf'), 42)
            self.text_surface1 = self.font.render(self.text, 1, (255, 255, 255))
            self.image1.blit(self.text_surface1, (46,29))
            self.image2.blit(self.text_surface1, (46,29))

            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (200,400)

            self.difficulty = 'easy'

        def update(self):            
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (200, 400)

            mouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse):
                self.image = self.image2


            

    class Hard_Button(pygame.sprite.Sprite):
        # this name is not as funny :[
        def __init__(self):
            pygame.sprite.Sprite.__init__(self, self.groups)

            self.image1 = pygame.Surface((260, 100))
            self.image1_front = pygame.Surface((256, 96))
            self.image1_front.fill((0,0,0))
            self.image1.fill((255,255,255))
            self.image1.blit(self.image1_front, (2,2))
            self.image2 = pygame.Surface((260, 100)) 
            self.image2_front = pygame.Surface((256, 96))
            self.image2_front.fill((196, 24, 24)) # fill the surface with RGB
            self.image2.fill((255,255,255))
            self.image2.blit(self.image2_front, (2,2)) 

            self.text = 'hard'
            
            self.font = pygame.font.Font(os.path.join('Resources','Fonts','m04.ttf'), 42)
            self.text_surface1 = self.font.render(self.text, 1, (255, 255, 255))
            self.image1.blit(self.text_surface1, (46,29))
            self.image2.blit(self.text_surface1, (46,29))

            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (550,400)

            self.difficulty = 'hard'

        def update(self):            
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (550,400)

            mouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse):
                self.image = self.image2
            
            

    class Info_Button(pygame.sprite.Sprite):
        # a button that allows you to delete any save file
        # color 179 r 24 g 196 b

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

            self.image1 = pygame.Surface((600, 200)) #Width Height
            self.image2 = pygame.Surface((600, 200)) #Width Height
            self.image2_front = pygame.Surface((256, 96)) #Width Height
            self.image1.fill((0,0,0))
            self.image2_front.fill((179, 24, 196)) # fill the surface with RGB
            self.image2.fill((255,255,255))
            self.image2.blit(self.image2_front, (2,2))
            

            self.text1 = 'delete'
            self.text2 = 'file'
            
            self.font = pygame.font.Font(os.path.join('Resources','Fonts','m04.ttf'), 42)
            self.text_surface1 = self.font.render(self.text1, 1, (255, 255, 255))
            self.text_surface2 = self.font.render(self.text2, 1, (255, 255, 255))
            self.image1.blit(self.text_surface1, (4,4))
            self.image1.blit(self.text_surface2, (4,54))
            self.image2.blit(self.text_surface1, (4,4))
            self.image2.blit(self.text_surface2, (4,54))

            self.image = self.image1
            self.rect = self.image.get_rect()

            self.delete_mode = False # we are not deleting any files yet
            '''
            self.image1 = pygame.image.load('Resources/Images/Menu Images/Map Select Menu/Map3.png').convert()
            self.image2 = pygame.image.load('Resources/Images/Menu Images/Map Select Menu/Map3(selected).png').convert()
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (150, height - 150)
            '''
            
        def is_clicked(self):
            '''
            changes the text so that people
            can cancel the delete
            '''

            if self.delete_mode == False:
                
                self.text1 = 'cancel'
                self.delete_mode = True # we are deleting stuff

                # creating the new image text

                self.image1 = pygame.Surface((600, 200)) #Width Height
                self.image2 = pygame.Surface((600, 200)) #Width Height
                self.image2_front = pygame.Surface((256, 96)) #Width Height
                self.image1.fill((0,0,0))
                self.image2_front.fill((179, 24, 196)) # fill the surface with RGB
                self.image2.fill((255,255,255))
                self.image2.blit(self.image2_front, (2,2))

                
                self.font = pygame.font.Font(os.path.join('Resources','Fonts','m04.ttf'), 42)
                self.text_surface1 = self.font.render(self.text1, 1, (255, 255, 255))

                self.image1.blit(self.text_surface1, (4,29))
                self.image2.blit(self.text_surface1, (4,29))

                self.image = self.image1
                self.rect = self.image.get_rect()

            elif self.delete_mode == True:
                
                self.text1 = 'delete'
                self.text2 = 'file'
                self.delete_mode = False # we are not deleting stuff

                self.image1 = pygame.Surface((600, 200)) #Width Height
                self.image2 = pygame.Surface((600, 200)) #Width Height
                self.image2_front = pygame.Surface((256, 96)) #Width Height
                self.image1.fill((0,0,0))
                self.image2_front.fill((179, 24, 196)) # fill the surface with RGB
                self.image2.fill((255,255,255))
                self.image2.blit(self.image2_front, (2,2))

                self.font = pygame.font.Font(os.path.join('Resources','Fonts','m04.ttf'), 42)
                self.text_surface1 = self.font.render(self.text1, 1, (255, 255, 255))
                self.text_surface2 = self.font.render(self.text2, 1, (255, 255, 255))

                self.image1.blit(self.text_surface1, (4,4))
                self.image1.blit(self.text_surface2, (4,54))
                self.image2.blit(self.text_surface1, (4,4))
                self.image2.blit(self.text_surface2, (4,54))

                self.image = self.image1
                self.rect = self.image.get_rect()

            return self.delete_mode
        
        def display_save_file_info(self, open_maps, difficulty):

            if difficulty != None: # if the difficulty has been set already

                # get which map is currently open
                current_map = 0
                for m in open_maps:
                    if m == False:
                        break
                    else:
                        current_map += 1
                    
                self.text1 = 'level-' + str(current_map)
                self.text2 = 'skill-' + str(difficulty)
                file_name = 'Map' + str((current_map - 1)) + '.png'
                self.map_image = pygame.image.load(os.path.join('Resources','Images','Menu Images','Map Select Menu',file_name)).convert()

                # creating the new image text

                self.image1 = pygame.Surface((600, 200)) #Width Height
                self.image2 = pygame.Surface((600, 200)) #Width Height
                self.image1_front = pygame.Surface((596, 196)) #Width Height
                self.image2_front = pygame.Surface((596, 196)) #Width Height
                self.image1.fill((0,0,0))
                #self.image1_front.fill((179, 24, 196)) # fill the surface with RGB
                self.image1_front.fill((0,0,0)) # fill the surface with RGB
                self.image2_front.fill((179, 24, 196)) # fill the surface with RGB
                self.image2.fill((255,255,255))
                self.image2.blit(self.image2_front, (2,2))
                self.image1.fill((255,255,255))
                self.image1.blit(self.image1_front, (2,2))

                
                self.font = pygame.font.Font(os.path.join('Resources','Fonts','m04.ttf'), 30)
                self.text_surface1 = self.font.render(self.text1, 1, (255, 255, 255))
                self.text_surface2 = self.font.render(self.text2, 1, (255, 255, 255))

                self.image1.blit(self.text_surface1, (4,29))
                self.image1.blit(self.text_surface2, (4,79))
                self.image1.blit(self.map_image, (425, 25))
                self.image2.blit(self.text_surface1, (4,29))
                self.image2.blit(self.text_surface2, (4,79))

                self.image = self.image1
                self.rect = self.image.get_rect()

            if difficulty == None:
                    
                self.text1 = 'New File'

                # creating the new image text

                self.image1 = pygame.Surface((600, 200)) #Width Height
                self.image2 = pygame.Surface((600, 200)) #Width Height
                self.image1_front = pygame.Surface((596, 196)) #Width Height
                self.image2_front = pygame.Surface((596, 196)) #Width Height
                self.image1.fill((0,0,0))
                #self.image1_front.fill((179, 24, 196)) # fill the surface with RGB
                self.image1_front.fill((0,0,0)) # fill the surface with RGB
                self.image2_front.fill((179, 24, 196)) # fill the surface with RGB
                self.image2.fill((255,255,255))
                self.image2.blit(self.image2_front, (2,2))
                self.image1.fill((255,255,255))
                self.image1.blit(self.image1_front, (2,2))

                
                self.font = pygame.font.Font(os.path.join('Resources','Fonts','m04.ttf'), 42)
                self.text_surface1 = self.font.render(self.text1, 1, (255, 255, 255))

                self.image1.blit(self.text_surface1, (150,79))
                self.image2.blit(self.text_surface1, (150,79))

                self.image = self.image1
                self.rect = self.image.get_rect()

                

        def set_to_default(self):

            if self.delete_mode == True:
                
                self.text1 = 'cancel'

                # creating the new image text

                self.image1 = pygame.Surface((600, 200)) #Width Height
                self.image2 = pygame.Surface((600, 200)) #Width Height
                self.image1_front = pygame.Surface((596, 196)) #Width Height
                self.image2_front = pygame.Surface((596, 196)) #Width Height
                self.image1.fill((0,0,0))
                #self.image1_front.fill((179, 24, 196)) # fill the surface with RGB
                self.image1_front.fill((0,0,0)) # fill the surface with RGB
                self.image2_front.fill((179, 24, 196)) # fill the surface with RGB
                self.image2.fill((255,255,255))
                self.image2.blit(self.image2_front, (2,2))
                self.image1.fill((255,255,255))
                self.image1.blit(self.image1_front, (2,2))

                
                self.font = pygame.font.Font(os.path.join('Resources','Fonts','m04.ttf'), 42)
                self.text_surface1 = self.font.render(self.text1, 1, (255, 255, 255))

                self.image1.blit(self.text_surface1, (174,79))
                self.image2.blit(self.text_surface1, (174,79))

                self.image = self.image1
                self.rect = self.image.get_rect()

            elif self.delete_mode == False:
                
                self.text1 = 'delete'
                self.text2 = 'file'

                self.image1 = pygame.Surface((600, 200)) #Width Height
                self.image2 = pygame.Surface((600, 200)) #Width Height
                self.image1_front = pygame.Surface((596, 196)) #Width Height
                self.image2_front = pygame.Surface((596, 196)) #Width Height
                self.image1.fill((0,0,0))
                #self.image1_front.fill((179, 24, 196)) # fill the surface with RGB
                self.image1_front.fill((0,0,0)) # fill the surface with RGB
                self.image2_front.fill((179, 24, 196)) # fill the surface with RGB
                self.image2.fill((255,255,255))
                self.image2.blit(self.image2_front, (2,2))
                self.image1.fill((255,255,255))
                self.image1.blit(self.image1_front, (2,2))

                self.font = pygame.font.Font(os.path.join('Resources','Fonts','m04.ttf'), 42)
                self.text_surface1 = self.font.render(self.text1, 1, (255, 255, 255))
                self.text_surface2 = self.font.render(self.text2, 1, (255, 255, 255))

                self.image1.blit(self.text_surface1, (174,52))
                self.image1.blit(self.text_surface2, (174,104))
                self.image2.blit(self.text_surface1, (174,52))
                self.image2.blit(self.text_surface2, (174,104))

                self.image = self.image1
                self.rect = self.image.get_rect()
            return self.delete_mode
            
        def update(self):            
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.center = (375, 475)

            mouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse):
                self.image = self.image2

    def select_difficulty_options():
        # creates all of the buttons and text that we need
        Black_Cover()
        Difficulty_Choice()
        Easy_Button()
        Hard_Button()
        

    def test_if_open(file_number):
        '''
        return True if the save file exists
        '''
        return os.path.isfile(((os.path.join('Resources','Save Data','save file') + str(file_number))))

    def load_game(file_number):
        save_file = open((os.path.join('Resources','Save Data','save file') + str(file_number)), 'r')
        player = pickle.load(save_file)
        save_file.close()
        return player

    def get_file_info(file_number):
        try:
            save_file = open((os.path.join('Resources','Save Data','save file') + str(file_number)), 'r')
        #if the file doesn't exist, create one, then load it.
        except IOError:
            player_data = Player()
            create_file(file_number, player_data)
            save_file = open((os.path.join('Resources','Save Data','save file') + str(file_number)), 'r')
            
        player = pickle.load(save_file)
        save_file.close()
        return player.open_maps, player.difficulty

    def create_file(file_number, player_data):
        save_file = open((os.path.join('Resources','Save Data','save file') + str(file_number)), 'w')
        pickle.dump(player_data,save_file)
        save_file.close()

    main = Load_Game()
    file0 = Saved_Game0()
    file1 = Saved_Game1()
    file2 = Saved_Game2()
    infoSprites = pygame.sprite.Group(file0, file1, file2)

    difficulty_buttons_graphics = pygame.sprite.Group()
    difficulty_buttons = pygame.sprite.Group()

    Black_Cover.groups = difficulty_buttons_graphics
    Difficulty_Choice.groups = difficulty_buttons_graphics
    Easy_Button.groups = difficulty_buttons
    Hard_Button.groups = difficulty_buttons

    info_button = Info_Button()
    deleting_file_mode = False
    save_file_number = None
    player = None

    running = True
    pressed_quit = False
    selecting_difficulty = False

    while running:
        clock.tick(fps)

        screen.blit(main.image, main.rect.topleft)

        if not selecting_difficulty:
            infoSprites.update()
            info_button.update()
        screen.blit(info_button.image, info_button.rect.topleft)  
        
        infoSprites.draw(screen)
        
        difficulty_buttons_graphics.draw(screen)
        difficulty_buttons.draw(screen)
        difficulty_buttons.update()
                
                

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

                    if not selecting_difficulty:
                        for s in infoSprites:
                            if s.rect.collidepoint(click): # if we click on a save file
                                if deleting_file_mode == True: #clicking to delete a save file
                                    s.delete_file()
                                    deleting_file_mode = info_button.is_clicked() # changes the text and sees if we are deleting stuff

                                else:
                                    player = s.is_clicked()
                                    save_file_number = s.saved_game_number
                                    #if player.difficulty == None: # if were making a new file
                                        #info_button.select_difficulty()
                                    if player.difficulty in ['easy', 'hard']:
                                        running = False
                                    else: # if it is a new game
                                        select_difficulty_options()
                                        selecting_difficulty = True
                                    
                        if info_button.rect.collidepoint(click):
                            deleting_file_mode = info_button.is_clicked() # changes the text and sees if we are deleting stuff

                    else: # if we are picking the difficulty of a new save file
                        pass
                        # S O DO STUFF

                        for b in difficulty_buttons:
                            if b.rect.collidepoint(click):
                                player.difficulty = b.difficulty
                                create_file(save_file_number, player)

                                
                                running = False

                                
                                
                                
                        




                        
            mouse = pygame.mouse.get_pos()
            mouse_over_button = False # the mouse is not over a button
            if not selecting_difficulty:
                for i in infoSprites: # if we go over one of the three save files
                    if i.rect.collidepoint(mouse):
                        mouse_over_button = True
                        save_file_open_maps, save_file_difficulty = get_file_info(i.saved_game_number)
                        info_button.display_save_file_info(save_file_open_maps, save_file_difficulty)
                        
                if mouse_over_button == False: # if we didnt mouseover any of the save file buttons
                    deleting_file_mode = info_button.set_to_default()
                
    return player, save_file_number, pressed_quit
                            
if __name__ == "__main__":
    save_file_stats = run()
    print save_file_stats
    pygame.quit()
