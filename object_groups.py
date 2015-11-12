import pygame

##### Create object groups #####
huds = pygame.sprite.RenderUpdates()
fading_covers = pygame.sprite.GroupSingle()
enemies = pygame.sprite.LayeredUpdates()
turrets = pygame.sprite.Group()
shots = pygame.sprite.Group()
explosions = pygame.sprite.Group()
turretplacers = pygame.sprite.GroupSingle()
turret_range = pygame.sprite.GroupSingle()
buttons = pygame.sprite.LayeredUpdates()
wave_info_group = pygame.sprite.GroupSingle()
life_bars = pygame.sprite.Group()

map_draw = pygame.sprite.GroupSingle() # holds the map
all_update = pygame.sprite.Group()  #used for updating everything at the same time
all_draw = pygame.sprite.RenderUpdates() # used for drawing everything at the same time
all_objects = pygame.sprite.Group() # used for reseting the game
