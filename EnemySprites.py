import pygame, random
from general_stats import *
from sprite_stats import *
from wave_stats import *
from map_directions import *
from life_bar import *
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, player):

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.enemy_stats = enemy_stats(enemy_type, 'all_stats')

        self.images = self.enemy_stats[0]
        self.base_life = self.enemy_stats[1]
        self.orginal_speed = self.enemy_stats[2]
        self.speed = self.orginal_speed
        self.reward = self.enemy_stats[3]

        self.frame = 0 # starting image
        self.ANIMATION_TIMER = 10
        self.animation_timer = self.ANIMATION_TIMER
        self.animated_image = len(self.images) > 1 # find if the image needs to be animated True/False
        
        self.image_right = self.images[self.frame]
        self.image_up = pygame.transform.rotate(self.image_right, 90)
        self.image_left = pygame.transform.rotate(self.image_right, 180)
        self.image_down = pygame.transform.rotate(self.image_right, 270)

        self.starting_life = (self.base_life * wave.life_multiplier) # used when drawing the life bar
        self.life = self.starting_life
        
        self.image = self.image_right
        self.rect = self.image.get_rect() # get size of the image so we can use self.rect.center

        # make this more readible
        ##### movement #####
        self.directions = map_directions[player.map] # directions to move gets values from map_directions list based on which map you are on
        self.distances = map_distances[player.map] # how many tiles to move gets values from map_distances list based on which map you are on
        self.start = map_start[player.map] # spawn location gets values from map_start list based on which map you are on
        self.current_movement = 0 # to track which move is next
        self.direction = self.directions[self.current_movement] # gets direction from self.directions list
        self.distance = (self.distances[self.current_movement] * tile) # amount of tiles we want to move from the distances list
        self.trueX = ((self.start[0] * tile) - (tile / 2)) # calculates starting location in (x,y) using the self.start list
        self.trueY = ((self.start[1] * tile) - (tile / 2))
        self.prevX = self.trueX
        self.prevY = self.trueY
        self.rect.center = (self.trueX, self.trueY)
        self.total_distance_traveled = 0
        self.distance_traveledX = 0
        self.distance_traveledY = 0

        ##### create life bar to display health #####
        self.life_bar = Life_Bar(self.starting_life, self.life, self.rect.center, self.image.get_height(), self.image.get_width())
        self.is_alive = True
        self.is_being_slowed = False
        self.slowed_timer = None
        
    
    def reach_end(self, player):
        self.kill() # kill it!
        player.life -= 1 # hurt player (because letting a enemy get through is bad)
        self.is_alive = False
        self.life_bar.is_dead()
    def is_dead(self, player):
        self.kill()
        self.life_bar.is_dead()
        self.is_alive = False
        #player.money += (self.reward * wave.life_multipler)
        player.money += int(self.starting_life / 4) #2.5

    def get_hit(self, damage_of_hit, player):
        self.life -= damage_of_hit
        if self.life <= 0:
            self.is_dead(player)

    def get_slowed(self, slowing_percentage, slow_duration, player):
        if self.is_being_slowed == False: # if its not being slowed
            self.is_being_slowed = True
            self.speed *= slowing_percentage
            self.time_until_not_slowed = slow_duration
        else:
            self.time_until_not_slowed = slow_duration

    def update_slowed_state(self):
        # counts down until the enemy is not being slowed anymore
        if self.is_being_slowed:
            self.time_until_not_slowed -= 1
            if self.time_until_not_slowed <= 0:
                self.is_being_slowed = False # were not being slowed anymore
                self.speed = self.orginal_speed
        
    def update(self, player):
            
        ##### Directions for movement #####
        
        if self.direction == "d": # if direction is down
            self.x_velocity= 0
            self.y_velocity= 1
            if not self.animated_image:
                self.image = self.image_down # sets the picture to the down image
        if self.direction == "u": # up
            self.x_velocity= 0
            self.y_velocity= -1
            if not self.animated_image:
                self.image = self.image_up
        if self.direction == "l": # left
            self.x_velocity= -1
            self.y_velocity= 0
            if not self.animated_image:
                self.image = self.image_left
        if self.direction == "r": # right
            self.x_velocity= 1
            self.y_velocity= 0
            if not self.animated_image:
                self.image = self.image_right
            
        if self.direction == "ul": # if direction is down
            self.x_velocity= -.707
            self.y_velocity= -.707
            if not self.animated_image:
                self.image = self.image_down # sets the picture to the down image
        if self.direction == "ur": # up
            self.x_velocity= .707
            self.y_velocity= -.707
            if not self.animated_image:
                self.image = self.image_up
        if self.direction == "dl": # left
            self.x_velocity= -.707
            self.y_velocity= .707
            if not self.animated_image:
                self.image = self.image_left
        if self.direction == "dr": # right
            self.x_velocity= .707
            self.y_velocity= .707
            if not self.animated_image:
                self.image = self.image_right

        if self.animated_image: # if there is animation
            self.animation_timer -= 1
            if self.animation_timer <= 0:
                self.animation_timer = self.ANIMATION_TIMER
                if self.frame >= (len(self.images) - 1):
                    self.frame = 0
                else:
                    self.frame += 1
                self.image = self.images[self.frame]

            
        ##### picking next direction to move #####
        '''
        grid = snap_to_grid(self.rect.center)
        print grid
        if (    (grid[0] - self.trueX) * (grid[0] - self.prevX) < 0 or
                (grid[1] - self.trueY) * (grid[1] - self.prevY) < 0):
        '''
        self.distance -= self.speed
        if self.distance <= 0:
            self.current_movement += 1 # next movement
        
            if self.current_movement >= len(self.directions): # when we are out of directions to move
                self.reach_end(player)
                
            else: # when there are more directions to move
                self.distance = (self.distances[self.current_movement] * tile) # get number of spots to move from the distances list
                self.direction = self.directions[self.current_movement] # get next direction from the directions list

        ##### move the enemy every frame #####
        self.prevX = self.trueX
        self.prevY = self.trueY
        self.distance_traveledX = (self.x_velocity * self.speed) # calculate speed from direction to move and speed constant
        self.distance_traveledY = (self.y_velocity * self.speed)
        self.trueX += self.distance_traveledX
        self.trueY += self.distance_traveledY
        self.rect.center = (round(self.trueX),round(self.trueY)) # apply values to sprite.center

        self.total_distance_traveled += ((self.distance_traveledX ** 2) + (self.distance_traveledY ** 2))

        ##### Transparent #####
        self.image.set_colorkey(self.image.get_at((0, 0)))

        self.life_bar.update(self.starting_life, self.life, self.rect.center) # GET A LIFE!!!

        self.update_slowed_state()
                

    
def name_cmp(enemy1, enemy2):
    if enemy1.total_distance_traveled > enemy2.total_distance_traveled:
        return -1
    elif enemy1.total_distance_traveled < enemy2.total_distance_traveled:
        return 1
    else:
        return 0

def sort_enemies_group(enemies):
    new_list = []
    
    for e in enemies:
        current_testing_enemy = 0 # number slot were testing
        found_slot_for_enemy = False
        while found_slot_for_enemy == False:
            if len(new_list) > current_testing_enemy: # if the enemy is even there
                adjust_slot = name_cmp(e, new_list[current_testing_enemy])
                
                if adjust_slot == 1: # if the new enemy has traveled less than already tested enemies
                    current_testing_enemy += 1 # move up in the list to test
                    found_slot_for_enemy = False
                    
                if adjust_slot == 0: # if the new enemy and the tested enemy have traveled the same
                    found_slot_for_enemy = True
                    
                if adjust_slot == -1: # if the new enemy has traveled more than already tested enemies
                    found_slot_for_enemy = True

            else: # there are no more enemies in the new list to check with
                found_slot_for_enemy = True
        new_list.insert(current_testing_enemy, e)

    return new_list
