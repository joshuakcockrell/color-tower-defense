import os
import pygame.mixer

class music():
    def __init__(self):
        pygame.mixer.init()
        self.menu_music = pygame.mixer.Sound(os.path.join('Resources','Music','menu.wav')) # load the menu music
        self.game_music = pygame.mixer.Sound(os.path.join('Resources','Music','game.wav'))
        self.end_music = pygame.mixer.Sound(os.path.join('Resources','Music','end.wav'))

        self.thunder = pygame.mixer.Sound(os.path.join('Resources','Music','Thunder.wav'))
        self.explosion = pygame.mixer.Sound(os.path.join('Resources','Music','Soundeffects','','Chip_Perc_9.wav'))
        self.basic_shot = pygame.mixer.Sound(os.path.join('Resources','Music','Soundeffects','Percs','Chip_Perc_9.wav'))
        #self.die = pygame.mixer.Sound(os.path.join('Resources','Music','Soundeffects','Percs','Chip_Perc_8.wav'))
                                                            


        self.channel_menu = pygame.mixer.Channel(0)
        self.channel_game = pygame.mixer.Channel(1)
        self.channel_end = pygame.mixer.Channel(2)
        self.channel_fx = pygame.mixer.Channel(3)
        self.channel_thunder = pygame.mixer.Channel(4)

        #shot channels    
        self.channel_basic = pygame.mixer.Channel(5)

        self.channel_die = pygame.mixer.Channel(6)
        self.channels = []
        self.channels.extend([self.channel_menu] + [self.channel_game] +
                             [self.channel_end] + [self.channel_fx] +
                             [self.channel_thunder] + [self.channel_basic] +
                             [self.channel_die])

        
        
        self.music_on = True
        self.sound_on = True

    def play(self, channel, sound, loop):
        if self.music_on: # so the user can turn it off
            if loop == True:
                channel.play(sound,-1)
            else:
                channel.play(sound)
        
    def stop(self, channel):
        channel.stop()

    def pause(self, channel):
        channel.pause()

    def unpause(self, channel):
        channel.unpause()

    def reset(self):
        return
        
        pygame.mixer.quit()

        pygame.mixer.init()
        
    
music = music()
