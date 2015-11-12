import pygame
import random
import math

import HUDs
from general_stats import *
from sprite_stats import *
from snap_to_grid import *
from tower_range import *
from explosion import *
from object_groups import *
from vector import *
from music import *

class Turret(pygame.sprite.Sprite):
    def __init__(self, position, turret_type, player):
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.current_angle = 0

        self.turret_type = turret_type
        self.stats = turret_stats(turret_type, 'basic_stats')
        self.orginal_image = self.stats[0]
        self.image = self.orginal_image # holds rotated image
        self.rotatable = self.stats[1] # can the tower be rotated?
        self.range = self.stats[2] # range in pixels
        self.SHOOTING_TIMER = self.stats[3] # time between shots
        self.cost = self.stats[4]
        self.targeting_type = self.stats[5] # useful for targeting
        self.bullet_limit = self.stats[6]
        self.shoots_at_front = self.stats[6]
        '''
        self.image1 = pygame.image.load("Images/Towers/new towers/basic gun1.png").convert()
        self.image2 = pygame.image.load("Images/Towers/new towers/basic gun2.png").convert()
        self.image3 = pygame.image.load("Images/Towers/new towers/basic gun3.png").convert()
        self.image4 = pygame.image.load("Images/Towers/new towers/basic gun4.png").convert()
        self.image5 = pygame.image.load("Images/Towers/new towers/basic gun5.png").convert()
        self.image6 = pygame.image.load("Images/Towers/new towers/basic gun6.png").convert()
        self.image7 = pygame.image.load("Images/Towers/new towers/basic gun7.png").convert()
        self.image8 = pygame.image.load("Images/Towers/new towers/basic gun8.png").convert()
        self.image9 = pygame.transform.rotate(self.image1, 90)
        self.image10 = pygame.transform.rotate(self.image2, 90)
        self.image11 = pygame.transform.rotate(self.image3, 90)
        self.image12 = pygame.transform.rotate(self.image4, 90)
        self.image13 = pygame.transform.rotate(self.image5, 90)
        self.image14 = pygame.transform.rotate(self.image6, 90)
        self.image15 = pygame.transform.rotate(self.image7, 90)
        self.image16 = pygame.transform.rotate(self.image8, 90)
        self.image17 = pygame.transform.rotate(self.image1, 180)
        self.image18 = pygame.transform.rotate(self.image2, 180)
        self.image19 = pygame.transform.rotate(self.image3, 180)
        self.image20 = pygame.transform.rotate(self.image4, 180)
        self.image21 = pygame.transform.rotate(self.image5, 180)
        self.image22 = pygame.transform.rotate(self.image6, 180)
        self.image23 = pygame.transform.rotate(self.image7, 180)
        self.image24 = pygame.transform.rotate(self.image8, 180)
        self.image25 = pygame.transform.rotate(self.image1, 270)
        self.image26 = pygame.transform.rotate(self.image2, 270)
        self.image27 = pygame.transform.rotate(self.image3, 270)
        self.image28 = pygame.transform.rotate(self.image4, 270)
        self.image29 = pygame.transform.rotate(self.image5, 270)
        self.image30 = pygame.transform.rotate(self.image6, 270)
        self.image31 = pygame.transform.rotate(self.image7, 270)
        self.image32 = pygame.transform.rotate(self.image8, 270)
        '''
        self.rect = self.image.get_rect() # get it, just get it

        grid_position = snap_to_grid(position)
        self.rect.center = (grid_position) # where shall i go dear slavelord
        self.shooting_timer = 0 # start at 0 so we are loaded when tower is placed
            
        player.money -= self.cost # were you expecting a free high tech weapon?
        
        self.current_target = 0 # the target is the one FIX THIS
        self.target = None # actual target
        self.shots = []

    def get_rotation_direction(self):
        '''
        Function:
            gets direction to face
        '''
        x = vec2d(self.rect.centerx, self.rect.centery) # define where the shot is located at (x, y)
        y = vec2d(self.target.rect.centerx, self.target.rect.centery) # define the target location (x, y)
        self.total_dist = y - x # calculate total distance from shot to target using above values
        direction = self.total_dist.normalize() # normalizes the distance so we only move one pixel per update (* speed)

        dist_x = self.total_dist[0] # gets the x from the dist tuple
        dist_y = self.total_dist[1] # gets the y from the dist tuple
        radians = math.atan2(dist_y,dist_x) # convert vector to radians
        degrees = radians / 0.0174532 #convert to degrees
        degrees *= -1

        return degrees
    
    def rotate(self):
        self.old_center = self.rect.center  
        self.get_rotation_direction()  
        self.image = pygame.transform.rotate(self.orginal_image, self.get_rotation_direction()) 
        self.rect = self.image.get_rect()
        self.rect.center = self.old_center
        
    def shoot(self, target):

        self.current_angle += 137.5
        current_radians = self.current_angle * 0.0174532
        radians = current_radians
        
        self.target = target
        self.shooting_timer = self.SHOOTING_TIMER # reset the timer       
        self.shot = Shot(self.rect.center, self.target, self.turret_type, screen, radians) # creates a shot at turret location

        if self.rotatable == True: # if we can rotate the image
            self.rotate() # rotate towards the target
        
        if self.targeting_type == 'orbital':
            self.shots.append(self.shot)
        #music.play(music.channel_basic, music.basic_shot, False)
            
    def upgrade(self, turret_type, player):
        
        self.turret_type = turret_type
        
        self.stats = turret_stats(turret_type, 'basic_stats')
        self.image = self.stats[0]
        self.orginal_image = self.image
        self.rotatable = self.stats[1]
        self.range = self.stats[2] # range in pixels
        self.SHOOTING_TIMER = self.stats[3] # time between shots
        self.cost = self.stats[4]
        self.targeting_type = self.stats[5] # useful for targeting
        self.bullet_limit = self.stats[6]
        self.shoots_at_front = self.stats[7]

        player.money -= self.cost # were you expecting a free highly technologically advanced state of the art upgrade?

        HUDs.clear_info_menu()
        HUDs.info_menu('turret', self.turret_type) # run the info menu for that tower

        for t in turret_range:
            t.kill()

        if self.targeting_type =='orbital':
            for s in self.shots:
                s.destroy()

        Tower_Range(self.rect.center, self.range) # create a range

    def sell(self, player):
        self.kill()
        player.money += (self.cost * 1) #.75
        for r in turret_range:
            r.kill()
        for b in buttons:
            b.kill()
        if self.targeting_type =='orbital':
            for s in self.shots:
                s.destroy()

    def update_shot_list(self): #clears dead shots from the list
        for s in self.shots:
            if not s.is_alive:
                self.shots.remove(s) # if dead remove from shots group

    def update(self, player):
        pass


class TurretPlacer(pygame.sprite.Sprite): # hmm
    def __init__(self, position, turret_type) : # gets location and the kind of tower
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.turret_type = turret_type
        self.image = turret_stats(turret_type, 'image') # get the image
        
        self.image.set_alpha(175) # make the image see through 255 is most visible
        self.rect = self.image.get_rect()

        grid_position = snap_to_grid(position) # put the position in the grid form
        self.rect.center = (grid_position)

        self.radius = turret_stats(turret_type, 'radius') # get the radius of the turret

    def get_cost(self):
        return turret_stats(self.turret_type, 'cost')
    
    def move(self, position):
        grid_position = snap_to_grid(position)
        self.rect.center = (grid_position)





class Shot(pygame.sprite.Sprite):
    
    def __init__(self, position, target, tower_type, screen, current_angle):
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.current_angle = current_angle

        self.position = position
        self.target = target # target we are shooting at
        self.current_target = -1 # used to get a new target
        self.target_test = None # holds what target we are testing
        self.tower_type = tower_type
        self.screen = screen
        self.is_alive = True
        
        self.stats = turret_stats(self.tower_type, 'attack_stats')
        self.range = self.stats[0]
        self.orginal_image = self.stats[1]
        self.image = self.orginal_image
        self.speed = self.stats[2] # how fast does the shot travel
        self.damage = self.stats[3] # how much damage does the shot do
        self.targeting_type = self.stats[4] # what targeting does the shot use
        self.multiple_targets = self.stats[5]
        self.bullet_limit = self.stats[6]
        self.shot_error = self.stats[7]
        self.distance_till_kill = self.stats[8] # how far the shot travels before it is killed
        self.hit_target_only = self.stats[9] # can the shot hit others besides the target
        self.hit_kills_shot = self.stats[10] # does the shot die after hitting an enemy
        self.exploding = self.stats[11] # do the bullets explode?
        self.rotatable_shot = self.stats[12]
        self.extra_timer = self.stats[13] # timer for targeting
        self.extra_timer1 = self.stats[14] # extra timer between attacks (bee)
        self.beam_color = self.stats[15]
        self.beam_width = self.stats[16]
        self.has_splash_attacks = self.stats[17]
        self.radius = self.stats[18] # radius of the splash attack
        self.splash_damage = self.stats[19]
        self.has_slowing_attacks = self.stats[20]
        self.slow_percentage = self.stats[21]
        self.slow_duration = self.stats[22]

        self.distance_traveledX = 0 # we have not traveled anywhere yet
        self.distance_traveledY = 0
        self.total_distance_traveled = 0
        self.timer = 0 # starts at 0
        self.timer1 = 0 # starts at 0
        self.direction_change = 0 # so we can reset the value
        self.speedX = 0 # the speed in x/y directions
        self.speedY = 0
        self.alpha_value = 255
        self.image_width = None
        self.image_height = None
        self.damage_done = False # we have not done damage with this shot yet
    
        self.direction = self.first_shot_direction()
        
        if self.targeting_type == 'beam':
            self.image_width = self.total_dist[0]
            self.image_height = self.total_dist[1]
            
            if not self.image_width:
                self.image_width = self.beam_width
            if not self.image_height:
                self.image_height = self.beam_width
                
                
            self.image = pygame.Surface((math.fabs(self.image_width), math.fabs(self.image_height)))
            self.image.fill((255, 255, 255)) # fill the image with RGB
            self.image.set_colorkey((255, 255, 255)) # make the white transparent


        self.rect = self.image.get_rect()
        self.rect.center = (position)
        self.trueX = self.rect.centerx # create true stats to hold decimal values
        self.trueY = self.rect.centery

        if self.targeting_type == 'orbital': # special orbital shot type
            self.seconds = 5
            self.frames = self.seconds * fps
            self.direction = (1,0)
            self.speedX = 3.333 # the speed in x/y directions
            self.speedY = 0
            self.trueY -= 10
            self.speed_multiplier = 1.01 # multiplied by the speed every frame to move the shot outwards
            self.speed_multiplier_difference = 0.0000117857142 # 0.0000117857142 whats subtracted from the speed multiplier to slow the outward speed down
            #self.speed_multiplier_difference = self.speed_multiplier / self.frames

        if self.targeting_type == 'beam':
            self.line_positions = self.get_line_positions(self.target.rect.center, position, abs(self.image_width), abs(self.image_height))
            pygame.draw.line(self.image, self.beam_color, self.line_positions[0], self.line_positions[1], self.beam_width)
            self.trueX = self.rect.centerx # create true stats to hold decimal values
            self.trueY = self.rect.centery
        
        self.total_dist = None
        self.RAND_DIR_TIMER = self.extra_timer
        self.rand_dir_timer = 100 # random direction timer

    def destroy(self):
        
        self.kill() # self destruct
        self.is_alive = False
        
        if self.exploding: # if the shot type uses explosions
            Explosion(self.rect.center) # run explosion at center of shot that exploded

    def first_shot_direction(self):
        # for when the start is not the center of the tower
        '''
        Function:
            Calculates shot direction using vectors from the current
            shot location to the target 
            
            the direction is then normalized(divided by its length)
            to get a constant speed in any direction
            
            the direction is then returned to be used for movement of
            a sprite
        '''
        if self.targeting_type == 'homing' or 'cruise' or 'orbital':
            x = vec2d(self.position[0], self.position[1]) # define where the shot is located at (x, y)
            y = vec2d(self.target.rect.centerx, self.target.rect.centery) # define the target location (x, y)
            self.total_dist = y - x # calculate total distance from shot to target using above values
            direction = self.total_dist.normalize() # normalizes the distance so we only move one pixel per update (* speed)

            if self.shot_error: # if the shot has a shot error variable
                dist_x = self.total_dist[0] # gets the x from the dist tuple
                dist_y = self.total_dist[1] # gets the y from the dist tuple
                radians = math.atan2(dist_y,dist_x) # convert vector to radians
                
                #radians = self.current_angle 
                
                radians += ((random.random() * self.shot_error) * random.choice([-1,1])) # apply randomness
                direction_x = math.cos(radians) # convert back to a vector
                direction_y = math.sin(radians) # convert back to a vector
                direction = (direction_x, direction_y)

            
        return direction # send the stats
        
    def shot_direction(self): # used to get the direction to move.
        '''
        Function:
            Calculates shot direction using vectors from the current
            shot location to the target
            
            the direction is then normalized(divided by its length)
            to get a constant speed in any direction
            
            the direction is then returned to be used for movement of
            a sprite
        '''
    
        if self.targeting_type == 'homing' or 'cruise' or 'orbital':
            x = vec2d(self.rect.centerx, self.rect.centery) # define where the shot is located at (x, y)
            y = vec2d(self.target.rect.centerx, self.target.rect.centery) # define the target location (x, y)
            self.total_dist = y - x # calculate total distance from shot to target using above values
            direction = self.total_dist.normalize() # normalizes the distance so we only move one pixel per update (* speed)

            if self.shot_error: # if the shot has a shot error variable
                dist_x = self.total_dist[0] # gets the x from the dist tuple
                dist_y = self.total_dist[1] # gets the y from the dist tuple
                radians = math.atan2(dist_y,dist_x) # convert vector to radians
                radians += ((random.random() * self.shot_error) * random.choice([-1,1])) # apply randomness
                direction_x = math.cos(radians) # convert back to a vector
                direction_y = math.sin(radians) # convert back to a vector
                direction = (direction_x, direction_y)

            
        return direction # send the stats


    def get_direction(self, target, enemies, player):

        if self.targeting_type in ['homing', 'bee']: # pick a direction about every few frames
            # extra code for bees
            if self.targeting_type in ['bee']:
                self.rand_dir_timer -= 1 # time until next random direction
                if self.rand_dir_timer <= 0: # when time is up
                    if enemies.has(self.target): # if the target is alive
                        self.rand_dir_timer = self.RAND_DIR_TIMER # reset timer 
                    else:
                        self.rand_dir_timer = (self.RAND_DIR_TIMER * 3) # more time between random direction change
                                                                        # (this helps get it off the screen)
                    self.direction = (random.random()* random.choice((-1,1)),(random.random() * random.choice((-1,1)))) # pick a random direction

            if enemies.has(self.target): # if the target is alive
                self.timer -= 1 # count down till next direction pick
                if self.timer <= 0: # if time to pick a new direction
                    self.direction = self.shot_direction() # get the direction
                    self.timer = self.extra_timer # reset the timer
            else:
                if self.multiple_targets == True:
                    self.target = self.get_new_target(enemies)
                 
        if self.targeting_type == 'orbital':
            self.direction = self.shot_direction() # get the direction
            
        
        if self.targeting_type == 'beam':
            self.direction = None
        self.move(self.direction, player) # move the shot in the drection

    def get_rotation_direction(self, direction):
        '''
        Function:
            gets direction to face
        '''

        dist_x = direction[0] # gets the x from the dist tuple
        dist_y = direction[1] # gets the y from the dist tuple
        radians = math.atan2(dist_y,dist_x) # convert vector to radians
        degrees = radians / 0.0174532 #convert to degrees
        degrees *= -1

        return degrees

    def rotate_towards_target(self, direction):
        self.old_center = self.rect.center  
        self.image = pygame.transform.rotate(self.orginal_image, self.get_rotation_direction(direction)) 
        self.rect = self.image.get_rect()
        self.rect.center = self.old_center
        

    def get_new_target(self, enemies):

        if len(enemies) > 0: # if there are enemies on the screen
            return enemies.get_sprite(0)
        else:
            return None

    def get_line_positions(self, enemy_position, position, image_width, image_height):

        '''
        this gets the start of the line and the end of the line
        that will be used in drawing the line from the tower to the
        enemy.
        this is needed because we are drawing the lines on the local
        surface instead of the entire screen. So we must use local coordinates
        '''
        if self.rect.centerx < enemy_position[0]:
            if self.rect.centery < enemy_position[1]:
                #then its topleft
                start_corner = 'topleft'
                self.rect.topleft = (position)
                line_start_position = (0,0)
                line_end_position = (image_width, image_height)
                
            elif self.rect.centery > enemy_position[1]:
                #then its botleft
                start_corner = 'botleft'
                self.rect.bottomleft = (position)
                line_start_position = (0,image_height)
                line_end_position = (image_width, 0)
                
            elif self.rect.centery == enemy_position[1]:
                start_corner = 'midleft'
                self.rect.midleft = (position)
                line_start_position = (0,(image_height / 2))
                line_end_position = (image_width,(image_height / 2))

        elif self.rect.centerx > enemy_position[0]:
            if self.rect.centery < enemy_position[1]:
                #then its topright
                start_corner = 'topright'
                self.rect.topright = (position)
                line_start_position = (image_width,0)
                line_end_position = (0,image_height)
                
            elif self.rect.centery > enemy_position[1]:
                #then its botright
                start_corner = 'botright'
                self.rect.bottomright = (position)
                line_start_position = (image_width, image_height)
                line_end_position = (0,0)

            elif self.rect.centery == enemy_position[1]:
                #then its midright
                start_corner = 'midright'
                self.rect.midright = (position)
                line_start_position = (image_width,(image_height / 2))
                line_end_position = (0,(image_height / 2))

        elif self.rect.centerx == enemy_position[0]:
            if self.rect.centery > enemy_position[1]:
                #then its midbottom
                start_corner = 'midbottom'
                self.rect.midbottom = (position)
                line_start_position = ((image_width / 2), image_height)
                line_end_position = ((image_width / 2), 0)
                
            elif self.rect.centery < enemy_position[1]:
                #then its midtop
                start_corner = 'midtop'
                self.rect.midtop = (position)
                line_start_position = ((image_width / 2), 0)
                line_end_position = ((image_width / 2), image_height)

            elif self.rect.centery == enemy_position[1]:
                #then the enemy is directly on top of the tower
                start_corner = 'center'
                self.rect.center = (position)
                line_start_position = ((image_width / 2),(image_height / 2))
                line_end_position = ((image_width / 2),(image_height / 2))

        return (line_start_position, line_end_position)

    
    def move(self, dist, player): # move in a certain direction        
        # boundaries
        if (self.rect.left < (0 - (tile * 4))or
        self.rect.right > (self.screen.get_width() + (tile * 4)) or
        self.rect.top < (0 - (tile * 4)) or
        self.rect.bottom > (self.screen.get_height() + (tile * 4))):
            self.destroy()
        else:

            ##### collisions with enemies #####
            # beams have their own targeting type
            if self.targeting_type == 'beam':
                if self.damage_done == False:
                    self.damage_done = True
                    self.target.get_hit(self.damage, player)

            if len(enemies) >= 1:

                if self.damage != 0: # if the shot actually hurts stuff
                    if self.targeting_type != 'beam':
                    
                        if self.hit_target_only: # if it only hits its target
                            if self.timer1 != None: # if there is a delay between attacks (bee)
                                self.timer1 -= 1 # countdown until next attack
                                if self.timer1 <= 0: # if its time to attack
                                    self.timer1 = self.extra_timer1 # reset the attack timer
                                    hitTarget = pygame.sprite.collide_rect(self, self.target)
                                    if hitTarget:
                                        self.target.get_hit(self.damage, player)
                                        if self.hit_kills_shot:
                                            self.destroy()
                            else: # if there is no delay between attacks
                                hitTarget = pygame.sprite.collide_rect(self, self.target)
                                if hitTarget:
                                    self.target.get_hit(self.damage, player)
                                    if self.hit_kills_shot:
                                        self.destroy()

                        else: # if it can hit any enemy
                            enemy_hit = pygame.sprite.spritecollideany(self, enemies)
                            if enemy_hit:
                                enemy_hit.get_hit(self.damage, player)
                                if self.hit_kills_shot:
                                    self.destroy()
                                if self.has_splash_attacks: # if they do splash damage
                                    for e in enemies:
                                        splash_collision = pygame.sprite.collide_circle(self, e)
                                        if splash_collision: # if enemies are in range of the splash damage
                                            e.get_hit(self.splash_damage, player)
                                if self.has_slowing_attacks:
                                    enemy_hit.get_slowed(self.slow_percentage, self.slow_duration, player)
                                
                                        

            self.dist = dist

            ##### apply the speed/direction to the position #####
            if self.targeting_type == 'homing':
                self.speedX += (self.dist[0] * self.speed)
                self.speedY += (self.dist[1] * self.speed)
                self.speedX *= .98
                self.speedY *= .98
                self.trueX += self.speedX
                self.trueY += self.speedY

            if self.targeting_type == 'orbital':
                self.speedX += (self.dist[0] * self.speed)
                self.speedY += (self.dist[1] * self.speed)
                self.speedX *= self.speed_multiplier
                self.speedY *= self.speed_multiplier
                self.trueX += self.speedX
                self.trueY += self.speedY
                if self.speed_multiplier >= 1:
                    self.speed_multiplier -= self.speed_multiplier_difference
                 
            if self.targeting_type == 'cruise':
                self.trueX += (self.dist[0] * self.speed)
                self.trueY += (self.dist[1] * self.speed)
            

            # for fibinachi sequence volcano
            '''
            if self.targeting_type == 'cruise':
                self.speedX += (self.dist[0] * self.speed)
                self.speedY += (self.dist[1] * self.speed)
                self.speedX *= .2
                self.speedY *= .2
                self.trueX += self.speedX
                self.trueY += self.speedY
            '''

            if self.targeting_type == 'bee':
                self.speedX += (self.dist[0] * self.speed)
                self.speedY += (self.dist[1] * self.speed)
                self.speedX *= .95
                self.speedY *= .95
                self.trueX += self.speedX
                self.trueY += self.speedY

            if self.targeting_type == 'beam':
                self.alpha_value -= self.extra_timer
                self.image.set_alpha(self.alpha_value)
                if self.alpha_value <= 0:
                    self.destroy()

            if self.targeting_type != 'beam':
                self.distance_traveledX += self.dist[0] * self.speed
                self.distance_traveledY += self.dist[1] * self.speed

            self.total_distance_traveled = (self.distance_traveledX ** 2) + (self.distance_traveledY ** 2)
            if self.distance_till_kill: # if it explodes after a certain distance
                if self.total_distance_traveled > (self.distance_till_kill ** 2):
                    self.destroy()
                
            if self.rotatable_shot: # if the shot can rotate
                self.rotate_towards_target(dist)
            self.rect.center = (round(self.trueX),round(self.trueY))
