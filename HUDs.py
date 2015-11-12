import pygame, EnemySprites
from general_stats import *
from wave_stats import *
from sprite_stats import *
from object_groups import *
##### module that stores info on all the buttons and on screen text #####
width = 750
height = 600

class Fading_Cover(pygame.sprite.Sprite):
    # for fade in and out of games

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((width, height))
        self.image.fill ((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        self.starting_alpha = 255
        self.alpha_value = self.starting_alpha
        self.image.set_alpha(self.starting_alpha)
        self.alpha_speed = 2

    def faded_in(self):
        self.image.set_alpha(self.alpha_value)
        self.alpha_value -= self.alpha_speed
        if self.alpha_value <= 0:
            return True

    def faded_out(self):
        self.image.set_alpha(self.alpha_value)
        self.alpha_value += self.alpha_speed
        if self.alpha_value >= 255:
            return True

class Info_Bar(pygame.sprite.Sprite): # box at bottom of screen that displays useful info
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.size = (580,80)

        self.image = pygame.Surface(self.size) #Width Height
        self.image.fill((0, 0, 0)) # fill the surface with RGB
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (10, 590)
        self.alpha_value = 0
        self.fade_out_speed = 6
        self.time_till_fade_out = 0
        self.font = pygame.font.Font(os.path.join('Resources','Fonts','Microsoft Sans Serif.ttf'), 14)
        self.font_color = (0,0,0)

        self.last_temp_info_type = None #stores the most recent info type that was temporarily displayed on the info button
        self.displaying = False # we are not displaying anything
    def display_info(self, info, info_type, delayed_fade_out):
        
        self.alpha_value = 180
        if delayed_fade_out == True:
            self.time_till_fade_out = 60
        else:
            self.time_till_fade_out = 0
        
        '''
        self.rect = self.image.get_rect()
        self.rect.topleft = (610, ((slot * 55) + 265))# where the button is displayed

        ##### text displayed on the info button #####
        self.font = pygame.font.Font('Resources/Fonts/Microsoft Sans Serif.ttf', 14)
        
        '''
        if self.displaying_message == False: # if nothing is already displaying, then we can display something new
            if info_type == 'upgrade info':
                if self.last_temp_info_type != info: # if we have not made the temporary stats yet
                    self.temp_info_stats = turret_stats(info, 'info_stats')

                    self.temp_image = pygame.Surface(self.size) #Width Height
                    self.temp_image.fill((255, 255, 255)) # fill the surface with RGB

                    self.temp_turret_range = self.temp_info_stats[3]
                    self.temp_turret_range_text = 'Range: %s' % ((self.temp_turret_range/tile))
                    self.temp_turret_range_surface = self.font.render(self.temp_turret_range_text, 1, self.font_color)
                    self.temp_image.blit(self.temp_turret_range_surface, (1,1))
                    
                    self.temp_turret_attack_rate = self.temp_info_stats[4]
                    self.temp_calculated_rate = round((fps/(self.temp_turret_attack_rate/fps))/fps, 1) # formula to get attack rate
                    self.temp_turret_attack_rate_text = 'Rate: %s/second' % (self.temp_calculated_rate)
                    self.temp_turret_attack_rate_surface = self.font.render(self.temp_turret_attack_rate_text, 1, self.font_color)
                    self.temp_image.blit(self.temp_turret_attack_rate_surface, (1,16))

                    self.temp_turret_attack_damage = self.temp_info_stats[5]
                    self.temp_turret_damage_text = 'Damage: %s' % (self.temp_turret_attack_damage)
                    self.temp_turret_damage_surface = self.font.render(self.temp_turret_damage_text, 1, self.font_color)
                    self.temp_image.blit(self.temp_turret_damage_surface, (1,31))

                    self.temp_turret_description_text = self.temp_info_stats[0]
                    self.temp_turret_description_surface = self.font.render(self.temp_turret_description_text, 1, self.font_color)
                    self.temp_image.blit(self.temp_turret_description_surface, (1,46))

                    self.last_temp_info_type = info
                    self.image = self.temp_image

                else:#if we already made the temporary info for this button
                    self.image = self.temp_image

            elif info_type == 'message':
                self.displaying_message = True
                self.temp_image = pygame.Surface(self.size) #Width Height
                self.temp_image.fill((255, 255, 255)) # fill the surface with RGB

                self.temp_message_text = info
                self.temp_message_surface = self.font.render(self.temp_message_text, 1, self.font_color)
                self.temp_image.blit(self.temp_message_surface, (((self.size[0] - self.temp_message_surface.get_width())/2),40))
                self.last_temp_info_type = info
                self.image = self.temp_image
            

    def fade_out(self):
        if self.time_till_fade_out <= 0:
            self.displaying_message = False
            if self.alpha_value >= 0:
                self.alpha_value -= self.fade_out_speed
        else:
            self.time_till_fade_out -= 1

    def update(self, player):
        self.image.set_alpha(self.alpha_value)

class Side_Bar(pygame.sprite.Sprite): # Bar which most HUD are displayed on

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((150, 600)) #Width Height
        self.image.fill((0, 0, 0)) # fill the surface with RGB 
        self.rect = self.image.get_rect()
        self.rect.topleft = (600, 0)
    def draw(self):
        screen.blit(self.image,self.rect.topleft)

class Direction_Arrow(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.images = [] # holds all the images for different rotations
        image0 = pygame.image.load(os.path.join('Resources','Images','Menu Images','In Game Menu','arrow.png')).convert()
        image90 = pygame.transform.rotate(image0, 90)
        image180 = pygame.transform.rotate(image0, 180)
        image270 = pygame.transform.rotate(image0, 270)
        self.images.extend([image0] + [image90] + [image180] + [image270])
        self.image_direction = None
        self.map_positions = []
        map0_pos = [(325,50), 270] # holds rect.center, and direction to point
        map1_pos = [(50,225), 0]
        map2_pos = [(50,425), 0]
        map3_pos = [(50,225), 0]
        map4_pos = [(225,50), 270]
        map5_pos = [(50,125), 0]
        self.map_positions.extend([map0_pos] + [map1_pos] + [map2_pos] +
                                  [map3_pos] + [map4_pos] + [map5_pos])
        self.position_info = None
        self.alpha_value = 0 # starts at 0
        self.max_alpha = 255
        self.min_alpha = 0
        self.alpha_speed = 5
        self.adding_more_alpha = False
        self.vanishing = False

    def start_new_map(self, player):
        position_info = self.map_positions[player.map]
        self.image_direction = position_info[1]
        self.image = self.images[self.image_direction / 90]
        self.image.set_colorkey(self.image.get_at((0, 0))) # transparent
        self.rect = self.image.get_rect()
        self.rect.center = position_info[0]


    def vanish(self):
        self.vanishing = True
                
    def update(self, player):
        if self.vanishing == False:
            if self.adding_more_alpha == True:
                self.alpha_value += self.alpha_speed
                if self.alpha_value >= self.max_alpha:
                    self.adding_more_alpha = False
            else:
                self.alpha_value -= self.alpha_speed
                if self.alpha_value <= self.min_alpha:
                    self.adding_more_alpha = True

        else:
            if self.alpha_value >= self.min_alpha:
                self.alpha_value -= self.alpha_speed
            

        self.image.set_alpha(self.alpha_value)




class Sound_Toggle(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.font = pygame.font.Font(os.path.join('Resources','Fonts','Microsoft Sans Serif.ttf'), 14)
        self.sound_setting = 'ON/OFF'
        self.text = 'SOUND ' + self.sound_setting
        self.image1 = self.font.render(self.text, 1, (255, 255, 255))
        self.image2 = self.font.render(self.text, 1, (255, 25, 25))
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.center = (675, 540)
        self.sound_on = True

    def change_setting(self, music_on):
        '''
        music_on is true or false
        '''
        
        if music_on == True:
            self.sound_on = True 
            self.sound_setting = 'ON'
        elif music_on == False:
            self.sound_on = False
            self.sound_setting = 'OFF'
        self.text = 'SOUND ' + self.sound_setting
        self.image1 = self.font.render(self.text, 1, (255, 255, 255))
        self.image2 = self.font.render(self.text, 1, (255, 25, 25))
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.center = (675, 540)
        
                
    def update(self, player):
        self.image = self.image1
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            self.image = self.image2
            self.rect = self.image.get_rect()
            self.rect.center = (675, 540)


class Pause(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.font = pygame.font.Font(os.path.join('Resources','Fonts','Microsoft Sans Serif.ttf'), 14)
        self.text = 'PAUSE GAME'
        self.image1 = self.font.render(self.text, 1, (255, 255, 255))
        self.image2 = self.font.render(self.text, 1, (255, 25, 25))
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.center = (675, height - 40)
                
    def update(self, player):
        self.image = self.image1
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            self.image = self.image2
            self.rect = self.image.get_rect()
            self.rect.center = (675, height - 40)

#class Music_toggle

class Main_Menu(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.font = pygame.font.Font(os.path.join('Resources','Fonts','Microsoft Sans Serif.ttf'), 14)
        self.text = 'MAIN MENU'
        self.image1 = self.font.render(self.text, 1, (255, 255, 255))
        self.image2 = self.font.render(self.text, 1, (255, 25, 25))
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.center = (675, height - 15)
                
    def update(self, player):
        self.image = self.image1
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            self.image = self.image2
            self.rect = self.image.get_rect()
            self.rect.center = (675, height - 15)

class Next_Wave(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.font = pygame.font.Font(os.path.join('Resources','Fonts','Microsoft Sans Serif.ttf'), 14)
        self.text = 'NEXT WAVE'
        self.image1 = self.font.render(self.text, 1, (255, 255, 255))
        self.image2 = self.font.render(self.text, 1, (255, 25, 25))
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.center = (675, 35)
                
    def update(self, player):
        self.image = self.image1
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            self.image = self.image2
            self.rect = self.image.get_rect()
            self.rect.center = (675, 35)

class Life(pygame.sprite.Sprite):

    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.font = pygame.font.Font(os.path.join('Resources','Fonts','Microsoft Sans Serif.ttf'), 14)
        self.life = player.life
        self.text = 'LIFE: %s' % (self.life)
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (675, 15)
        
    def update(self, player):
        self.life = player.life
        self.text = 'LIFE: %s' % (self.life)
        self.image = self.font.render(self.text, 1, (255, 255, 255))

class Money(pygame.sprite.Sprite):

    def __init__(self, player_money):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.font = pygame.font.Font(os.path.join('Resources','Fonts','Microsoft Sans Serif.ttf'), 14)
        self.money = player_money
        self.text = 'MONEY: %s' % (self.money)
        self.image = self.font.render(self.text, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (675, 110)

    def update(self, player):
        self.money = player.money
        self.text = 'MONEY: %s' % (self.money)
        self.image = self.font.render(self.text, 1, (255, 255, 255))


class Wave_Info(pygame.sprite.Sprite): # displays number of enemies on screen

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.font = pygame.font.Font(os.path.join('Resources','Fonts','Microsoft Sans Serif.ttf'), 14)
        self.wave = wave.current_wave

        self.image = pygame.Surface((130, 50)) #Width Height
        self.image.fill((0, 100, 100)) # fill the surface with RGB 
        self.rect = self.image.get_rect()
        self.rect.center = (675, 75) #675 180

        self.wave = wave.current_wave
        self.ammount_text = 'WAVE:%s' % (self.wave) + '/%s' % (len(wave.map_enemies))
        self.ammount_surface = self.font.render(self.ammount_text, 1, (255,255,255))
        self.image.blit(self.ammount_surface, (1,1))
        
        self.wave_kind_text = '%s' % (wave.wave_type)
        self.wave_kind_surface = self.font.render(self.wave_kind_text, 1, (255,255,255))
        self.image.blit(self.wave_kind_surface, (1,16))

        self.wave_enemy_life_base = enemy_stats(wave.wave_type, 'life') # get enemy base health
        self.wave_enemy_life_text = 'Life:%s' % (self.wave_enemy_life_base * wave.life_multiplier) # calculate enemy health
        self.wave_enemy_life_surface = self.font.render(self.wave_enemy_life_text, 1, (255,255,255))
        self.image.blit(self.wave_enemy_life_surface, (1,31))

class Build_Turret_Button(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        ##### turret stats #####
        self.turret_type = 'Basic' # turret stats found in Values module

        self.image1 = pygame.Surface((130, 50)) #Width Height
        self.image1.fill((0, 175, 0)) # fill the surface with RGB
        self.image2 = pygame.Surface((130, 50)) #Width Height
        self.image2.fill((0, 255, 0)) # fill the surface with RGB
        self.image = self.image1
        self.rect = self.image1.get_rect()
        self.rect.center = (675, 150)# X, Y(5, 60)



        self.font = pygame.font.Font(os.path.join('Resources','Fonts','Microsoft Sans Serif.ttf'), 14)
        self.turret_stats = turret_stats(self.turret_type, 'info_stats')
        
        self.picture = self.turret_stats[1]

        self.turret_type_text = '%s' % (self.turret_type)
        self.turret_type_surface = self.font.render(self.turret_type_text, 1, (0, 0, 0))
        self.image1.blit(self.turret_type_surface, (50,1))
        self.image2.blit(self.turret_type_surface, (50,1))

        self.build_cost = self.turret_stats[2]
        self.build_cost_text = 'Cost: %s' % (self.build_cost)
        self.build_cost_surface = self.font.render(self.build_cost_text, 1, (0, 0, 0))
        self.image1.blit(self.build_cost_surface, (50,16))
        self.image2.blit(self.build_cost_surface, (50,16))

        self.hotkey = 'B'
        self.hotkey_text = 'Hotkey[%s]' % (self.hotkey)
        self.hotkey_surface = self.font.render(self.hotkey_text, 1, (0, 0, 0))
        self.image1.blit(self.hotkey_surface, (50,31))
        self.image2.blit(self.hotkey_surface, (50,31))

        
        '''
        self.turret_range = self.turret_stats[3]
        self.turret_range_text = 'Range: %s' % ((self.turret_range/tile))
        self.turret_range_surface = self.font.render(self.turret_range_text, 1, (0,0,0))
        self.image2.blit(self.turret_range_surface, (1,1))
        
        self.turret_attack_rate = self.turret_stats[4]
        self.calculated_rate = round((fps/(self.turret_attack_rate/fps))/fps, 1) # formula to get attack rate
        self.turret_attack_rate_text = 'Rate: %s/second' % (self.calculated_rate)
        self.turret_attack_rate_surface = self.font.render(self.turret_attack_rate_text, 1, (0,0,0))
        self.image2.blit(self.turret_attack_rate_surface, (1,16))

        self.turret_attack_damage = self.turret_stats[5]
        self.turret_damage_text = 'Damage: %s' % (self.turret_attack_damage)
        self.turret_damage_surface = self.font.render(self.turret_damage_text, 1, (0,0,0))
        self.image2.blit(self.turret_damage_surface, (1,31))
        '''
        
        self.image1.blit(self.picture, (((self.image.get_height() - self.picture.get_height()) / 2),#   x  place the turret picture at (x,y)
                                            ((self.image.get_height() - self.picture.get_height()) / 2))) # y # place the turret picture at (x,y)
        self.image2.blit(self.picture, (((self.image.get_height() - self.picture.get_height()) / 2),#   x  place the turret picture at (x,y)
                                            ((self.image.get_height() - self.picture.get_height()) / 2))) # y # place the turret picture at (x,y)


    def update(self, player):

        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            self.image = self.image2
        else:
            self.image = self.image1

class In_Game_Menu(pygame.sprite.Sprite): # create a box that menu buttons can be posted ontop of
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((140, 280)) # how big the menu is X,Y
        self.image.fill((100, 255, 100)) # fill the surface with RGB
        self.image.set_alpha(175) # make the image see through 255 is most visible
        self.rect = self.image.get_rect()
        self.rect.topleft = (605, 210)


class Button(pygame.sprite.Sprite): # in game menu buttons

    def __init__(self, slot, button_type, button_info): # ((140, 275)) X Y total
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.button_type = button_type # used when we click on a button
        self.button_info = button_info
        self.slot = slot
        self.button_y_start = 215

        if button_type == 'info': # display tower info
            self.image1 = pygame.Surface((130, 50)) #Width Height
            self.image1.fill((255, 150, 0)) # fill the surface with RGB
            self.image2 = pygame.Surface((130, 50)) #Width Height
            self.image2.fill((0, 150, 255)) # fill the surface with RGB
            self.image = self.image1
            self.rect = self.image.get_rect()
            self.rect.topleft = (610, ((slot * 55) + self.button_y_start))# where the button is displayed

            ##### text displayed on the info button #####
            self.font = pygame.font.Font(os.path.join('Resources','Fonts','Microsoft Sans Serif.ttf'), 14)
            self.info_stats = turret_stats(button_info, 'info_stats')
            
            self.turret_range = self.info_stats[3]
            self.turret_range_text = 'Range: %s' % ((self.turret_range/tile))
            self.turret_range_surface = self.font.render(self.turret_range_text, 1, (0,0,0))
            self.image1.blit(self.turret_range_surface, (1,1))
            
            self.turret_attack_rate = self.info_stats[4]
            self.calculated_rate = round((fps/(self.turret_attack_rate/fps))/fps, 1) # formula to get attack rate
            self.turret_attack_rate_text = 'Rate: %s/second' % (self.calculated_rate)
            self.turret_attack_rate_surface = self.font.render(self.turret_attack_rate_text, 1, (0,0,0))
            self.image1.blit(self.turret_attack_rate_surface, (1,16))

            self.turret_attack_damage = self.info_stats[5]
            self.turret_damage_text = 'Damage: %s' % (self.turret_attack_damage)
            self.turret_damage_surface = self.font.render(self.turret_damage_text, 1, (0,0,0))
            self.image1.blit(self.turret_damage_surface, (1,31))

            self.last_temp_info_type = None #stores the most recent info type that was temporarily displayed on the info button
            
        if button_type == 'upgrade': # make a upgrader button
            
            self.turret_type = button_info
            self.upgrade_cost = turret_stats(self.turret_type, 'cost')
            self.image1 = pygame.Surface((130, 50)) #Width Height
            self.image1.fill((0, 0, 175)) # fill the surface with RGB 
            self.image2 = pygame.Surface((130, 50)) #Width Height
            self.image2.fill((0, 0, 255)) # fill the surface with RGB
            self.image = self.image1
            
            self.rect = self.image.get_rect()
            self.rect.topleft = (610, ((slot * 55) + self.button_y_start))# X, Y(5, 60)

            self.font = pygame.font.Font(os.path.join('Resources','Fonts','Microsoft Sans Serif.ttf'), 14)
            self.upgrade_stats = turret_stats(self.turret_type, 'info_stats')
            self.picture = self.upgrade_stats[1]

            self.upgrade_type = self.turret_type
            self.upgrade_type_text = '%s' % (self.upgrade_type)
            self.upgrade_type_surface = self.font.render(self.upgrade_type_text, 1, (255, 255, 255))
            self.image1.blit(self.upgrade_type_surface, (50,1))
            self.image2.blit(self.upgrade_type_surface, (50,1))

            self.upgrade_cost = self.upgrade_stats[2]
            self.upgrade_cost_text = 'Cost: %s' % (self.upgrade_cost)
            self.upgrade_cost_surface = self.font.render(self.upgrade_cost_text, 1, (255, 255, 255))
            self.image1.blit(self.upgrade_cost_surface, (50,16))
            self.image2.blit(self.upgrade_cost_surface, (50,16))

            self.hotkey = self.slot
            self.hotkey_text = 'Hotkey[%s]' % (self.hotkey)
            self.hotkey_surface = self.font.render(self.hotkey_text, 1, (255, 255, 255))
            self.image1.blit(self.hotkey_surface, (50,31))
            self.image2.blit(self.hotkey_surface, (50,31))
            ''' used to display upgrade info
            self.turret_range = self.upgrade_stats[2]
            self.turret_range_text = 'Range: %s' % ((self.turret_range/tile))
            self.turret_range_surface = self.font.render(self.turret_range_text, 1, (255, 255, 255))
            self.image2.blit(self.turret_range_surface, (1,1))
            
            self.turret_attack_rate = self.upgrade_stats[3]
            self.calculated_rate = round((fps/(self.turret_attack_rate/fps))/fps, 1) # formula to get attack rate
            self.turret_attack_rate_text = 'Rate: %s/second' % (self.calculated_rate)
            self.turret_attack_rate_surface = self.font.render(self.turret_attack_rate_text, 1, (255, 255, 255))
            self.image2.blit(self.turret_attack_rate_surface, (1,16))

            self.turret_attack_damage = self.upgrade_stats[4]
            self.turret_damage_text = 'Damage: %s' % (self.turret_attack_damage)
            self.turret_damage_surface = self.font.render(self.turret_damage_text, 1, (255, 255, 255))
            self.image2.blit(self.turret_damage_surface, (1,31))

            '''
            

            self.image1.blit(self.picture, (((self.image.get_height() - self.picture.get_height()) / 2),#   x  place the turret picture at (x,y)
                                            ((self.image.get_height() - self.picture.get_height()) / 2))) # y

            self.image2.blit(self.picture, (((self.image.get_height() - self.picture.get_height()) / 2),#   x  place the turret picture at (x,y)
                                            ((self.image.get_height() - self.picture.get_height()) / 2))) # y


        if button_type == 'sell': # display tower sell options
            self.turret_type = button_info
            self.width = 130
            self.height = 50
            
            self.image1 = pygame.Surface((self.width, self.height)) #Width Height
            self.image1.fill((175, 0, 0)) # fill the surface with RGB
            self.image2 = pygame.Surface((self.width, self.height)) #Width Height
            self.image2.fill((255, 0, 0)) # fill the surface with RGB
            self.image = self.image1
            
            self.rect = self.image.get_rect()
            self.rect.topleft = (610, ((slot * 55) + self.button_y_start))# X, Y(5, 70

            self.font = pygame.font.Font(os.path.join('Resources','Fonts','Microsoft Sans Serif.ttf'), 14)
            
            self.sell_text = 'Sell Tower'
            self.sell_surface = self.font.render(self.sell_text, 1, (255, 255, 255))
            self.image1.blit(self.sell_surface, (((self.width - self.sell_surface.get_width())/2),1))
            self.image2.blit(self.sell_surface, (((self.width - self.sell_surface.get_width())/2),1))

            self.refund_ammount = turret_stats(self.turret_type, 'cost')
            self.refund_text = 'Refund: %s' % (self.refund_ammount * 1) #.75
            self.refund_surface = self.font.render(self.refund_text, 1, (255, 255, 255))
            self.image1.blit(self.refund_surface, (((self.width - self.refund_surface.get_width())/2),16))
            self.image2.blit(self.refund_surface, (((self.width - self.refund_surface.get_width())/2),16))

            self.hotkey = 'S'
            self.hotkey_text = 'Hotkey[%s]' % (self.hotkey)
            self.hotkey_surface = self.font.render(self.hotkey_text, 1, (255, 255, 255))
            self.image1.blit(self.hotkey_surface, (((self.width - self.hotkey_surface.get_width())/2),31))
            self.image2.blit(self.hotkey_surface, (((self.width - self.hotkey_surface.get_width())/2),31))

        if button_type == 'placement info':
            self.turret_type = button_info
            self.width = 130
            self.height = 50
            self.image1 = pygame.Surface((self.width, self.height)) #Width Height
            self.image1.fill((175, 0, 0)) # fill the surface with RGB
            self.image2 = pygame.Surface((self.width, self.height)) #Width Height
            self.image2.fill((175, 0, 0)) # fill the surface with RGB
            self.image = self.image1

            self.rect = self.image.get_rect()
            self.rect.topleft = (610, ((slot * 55) + self.button_y_start))# X, Y(5, 70
            self.font = pygame.font.Font(os.path.join('Resources','Fonts','Microsoft Sans Serif.ttf'), 14)
            self.info_text1 = 'Click anywhere off'
            self.info_text2 = 'the path to place'
            self.info_text3 = 'the tower'
            
            self.info_surface1 = self.font.render(self.info_text1, 1, (255, 255, 255))
            self.info_surface2 = self.font.render(self.info_text2,1, (255, 255, 255))
            self.info_surface3 = self.font.render(self.info_text3, 1, (255, 255, 255))

            self.image1.blit(self.info_surface1, (((self.width - self.info_surface1.get_width())/2),1))
            self.image1.blit(self.info_surface2, (((self.width - self.info_surface2.get_width())/2),16))
            self.image1.blit(self.info_surface3, (((self.width - self.info_surface3.get_width())/2),31))
            self.image2.blit(self.info_surface1, (((self.width - self.info_surface1.get_width())/2),1))
            self.image2.blit(self.info_surface2, (((self.width - self.info_surface2.get_width())/2),16))
            self.image2.blit(self.info_surface3, (((self.width - self.info_surface3.get_width())/2),31))


        if button_type == 'cancel placement':
            self.turret_type = button_info
            self.width = 130
            self.height = 50
            
            self.image1 = pygame.Surface((self.width, self.height)) #Width Height
            self.image1.fill((175, 0, 0)) # fill the surface with RGB
            self.image2 = pygame.Surface((self.width, self.height)) #Width Height
            self.image2.fill((255, 0, 0)) # fill the surface with RGB
            self.image = self.image1

            self.rect = self.image.get_rect()
            self.rect.topleft = (610, ((slot * 55) + self.button_y_start))# X, Y(5, 70
            
            self.font = pygame.font.Font(os.path.join('Resources','Fonts','Microsoft Sans Serif.ttf'), 14)
            self.info_text1 = 'Cancel'
            self.info_text2 = 'tower placement'
            self.info_surface1 = self.font.render(self.info_text1, 1, (255, 255, 255))
            self.info_surface2 = self.font.render(self.info_text2, 1, (255, 255, 255))

            self.hotkey = 'Space/Right Click'
            self.hotkey_text = '[%s]' % (self.hotkey)
            self.hotkey_surface = self.font.render(self.hotkey_text, 1, (255, 255, 255))

            self.image1.blit(self.hotkey_surface, (((self.width - self.hotkey_surface.get_width())/2),31))
            self.image2.blit(self.hotkey_surface, (((self.width - self.hotkey_surface.get_width())/2),31))
            
            self.image1.blit(self.info_surface1, (((self.width - self.info_surface1.get_width())/2),1))
            self.image1.blit(self.info_surface2, (((self.width - self.info_surface2.get_width())/2),15))
            self.image2.blit(self.info_surface1, (((self.width - self.info_surface1.get_width())/2),1))
            self.image2.blit(self.info_surface2, (((self.width - self.info_surface2.get_width())/2),15))




            
    def update_info(self, button_info):
        
        if self.button_type == 'info':
            '''
            self.rect = self.image.get_rect()
            self.rect.topleft = (610, ((slot * 55) + 265))# where the button is displayed

            ##### text displayed on the info button #####
            self.font = pygame.font.Font('Resources/Fonts/Microsoft Sans Serif.ttf', 14)

            '''
            if self.last_temp_info_type != button_info: # if we have not made the temporary stats yet
                self.temp_info_stats = turret_stats(button_info, 'info_stats')

                self.temp_image1 = pygame.Surface((130, 50)) #Width Height
                self.temp_image1.fill((255, 150, 0)) # fill the surface with RGB

                self.temp_turret_range = self.temp_info_stats[3]
                self.temp_turret_range_text = 'Range: %s' % ((self.temp_turret_range/tile))
                self.temp_turret_range_surface = self.font.render(self.temp_turret_range_text, 1, (0,0,0))
                self.temp_image1.blit(self.temp_turret_range_surface, (1,1))
                
                self.temp_turret_attack_rate = self.temp_info_stats[4]
                self.temp_calculated_rate = round((fps/(self.temp_turret_attack_rate/fps))/fps, 1) # formula to get attack rate
                self.temp_turret_attack_rate_text = 'Rate: %s/second' % (self.temp_calculated_rate)
                self.temp_turret_attack_rate_surface = self.font.render(self.temp_turret_attack_rate_text, 1, (0,0,0))
                self.temp_image1.blit(self.temp_turret_attack_rate_surface, (1,16))

                self.temp_turret_attack_damage = self.temp_info_stats[5]
                self.temp_turret_damage_text = 'Damage: %s' % (self.temp_turret_attack_damage)
                self.temp_turret_damage_surface = self.font.render(self.temp_turret_damage_text, 1, (0,0,0))
                self.temp_image1.blit(self.temp_turret_damage_surface, (1,31))

                self.last_temp_info_type = button_info
                self.image = self.temp_image1

            else:#if we already made the temporary info for this button
                self.image = self.temp_image1

    def reset_info(self):
        '''
        when we move the mouse off of a button
        this is called to change the info button
        to display the info of the selected turret
        instead of the info of the button that
        the users mouse is over
        '''
        
        if self.button_type == 'info':
            self.image = self.image1

            

    def update(self, player):

        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            if self.button_type != 'info': # info buttons dont change image
                self.image = self.image2

                
        else:
            if self.button_type != 'info': # doesnt change
                self.image = self.image1
            
            
def info_menu(menu_type, turret_type):

    if menu_type == 'turret': # menu for turrets

        # this stores the info for the info, upgrade trees, and sell buttons
        # duper super usefull!

        if turret_type == 'Basic': # five slots create the menu
            Button(0, 'info', turret_type) # send which slot, what kind of button, what the button needs to display
            Button(1, 'upgrade', 'Army')
            Button(2, 'upgrade', 'Nature')
            Button(3, 'upgrade', 'Science')
            Button(4, 'sell', turret_type)

        if turret_type == 'Army': # five slots create the menu
            Button(0, 'info', turret_type) # send which slot, what kind of button, what the button needs to display
            Button(1, 'upgrade', 'Machine')
            Button(2, 'upgrade', 'Splash')
            Button(3, 'upgrade', 'Homing')
            Button(4, 'sell', turret_type)

        if turret_type == 'Machine': # five slots create the menu
            Button(0, 'info', turret_type) # send which slot, what kind of button, what the button needs to display
            Button(1, 'upgrade', 'Rambo')
            Button(4, 'sell', turret_type)

        if turret_type == 'Rambo':
            Button(0, 'info', turret_type)
            Button(4, 'sell', turret_type)

        if turret_type == 'Splash': # five slots create the menu
            Button(0, 'info', turret_type) # send which slot, what kind of button, what the button needs to display
            Button(1, 'upgrade', 'Bomb')
            Button(4, 'sell', turret_type)

        if turret_type == 'Bomb':
            Button(0, 'info', turret_type)
            Button(4, 'sell', turret_type)

        if turret_type == 'Homing': # five slots create the menu
            Button(0, 'info', turret_type) # send which slot, what kind of button, what the button needs to display
            Button(1, 'upgrade', 'Homing V2')
            Button(4, 'sell', turret_type)

        if turret_type == 'Homing V2': # five slots create the menu
            Button(0, 'info', turret_type) # send which slot, what kind of button, what the button needs to display
            Button(4, 'sell', turret_type)

        if turret_type == 'Planet': # five slots create the menu
            Button(0, 'info', turret_type) # send which slot, what kind of button, what the button needs to display
            Button(1, 'upgrade', 'Galaxy')
            Button(4, 'sell', turret_type)

        if turret_type == 'Galaxy': # five slots create the menu
            Button(0, 'info', turret_type) # send which slot, what kind of button, what the button needs to display
            Button(4, 'sell', turret_type)

        if turret_type == 'Nature': # five slots create the menu
            Button(0, 'info', turret_type) # send which slot, what kind of button, what the button needs to display
            Button(1, 'upgrade', 'Fly')
            Button(2, 'upgrade', 'Fire')
            Button(3, 'upgrade', 'Planet')
            Button(4, 'sell', turret_type)

        if turret_type == 'Fly': # five slots create the menu
            Button(0, 'info', turret_type) # send which slot, what kind of button, what the button needs to display
            Button(1, 'upgrade', 'Bee')
            Button(4, 'sell', turret_type)

        if turret_type == 'Bee': # five slots create the menu
            Button(0, 'info', turret_type) # send which slot, what kind of button, what the button needs to display
            Button(4, 'sell', turret_type)

        if turret_type == 'Fire':
            Button(0, 'info', turret_type)
            Button(1, 'upgrade', 'Volcano')
            Button(4, 'sell', turret_type)
                
        if turret_type == 'Volcano':
            Button(0, 'info', turret_type)
            Button(4, 'sell', turret_type)

        if turret_type == 'Science':
            Button(0, 'info', turret_type)
            Button(1, 'upgrade', 'Slow')
            Button(2, 'upgrade', 'DEW')
            Button(3, 'upgrade', 'Pulse Beam')
            Button(4, 'sell', turret_type)

        if turret_type == 'Slow':
            Button(0, 'info', turret_type)
            Button(1, 'upgrade', 'Freeze')
            Button(4, 'sell', turret_type)

        if turret_type == 'DEW':
            Button(0, 'info', turret_type)
            Button(1, 'upgrade', 'Hydro DEW')
            Button(4, 'sell', turret_type)

        if turret_type == 'Hydro DEW':
            Button(0, 'info', turret_type)
            Button(4, 'sell', turret_type)

        if turret_type == 'Pulse Beam':
            Button(0, 'info', turret_type)
            Button(1, 'upgrade', 'Robot')
            Button(4, 'sell', turret_type)

        if turret_type == 'Robot':
            Button(0, 'info', turret_type)
            Button(4, 'sell', turret_type)

    elif menu_type == 'turret placement':
        if turret_type == 'Basic':
            Button(0, 'placement info', turret_type)
            Button(4, 'cancel placement', turret_type)

def clear_info_menu():
    
    for b in buttons:
        b.kill()
    
        
