import os
import pygame
from load_sliced_sprites import *

def turret_stats(turret_type, which_stats): # used to get the stats of a certain tower.

    '''
    Function:
        Very Very useful so we can keep all tower the stats in one place
        and they can be retrieved by calling this function


    _________________TOWER PATHS_________________
    |Tier 1|Tier 2   |Tier 3      |Tier 4        |
    |      |         |            |              |
    |      |         | Machine    -> Rambo       |
    |      | Army    < Splash     -> Bomb        |
    |      |         | Homing     ->             |
    |      |         |            |              |
    |      |         | Fly        -> Bee         |
    |Basic < Nature  < Fire       -> Volcano     |
    |      |         | Earth      -> Galaxy      |
    |      |         |            |              |
    |      |         | Slow       -> Freeze      |
    |      | Science < Hydro DEW  -> Voltaic Arc |
    |      |         | Pulse Beam -> Gaussian    |
    |      |         |            |              |
    |______|_________|____________|______________|
    
    supported turrets:
    max 12 characters (about)
    basic
    army
    homing
    homingII -
    machine
    rambo
    nature
    fly
    bee
    orbital -
    orbitalII -


    needed images:
    bee
    fly
    homing1 better
    homing2
    explosions transparent
    '''
    # needs:
    # street
    # rambo
    # gum?
    # flamethrower
    # slowing
    # orbitalII (area damage)
    '''
    supported targeting:
    cruise
    homing
    orbital
    '''
    # needs:
    # maybe area effect?/flamethrower?
    '''
    supported turret_menus:
    basic
    army
    homing
    homingII
    machine
    rambo
    nature
    fly
    bee
    orbital
    '''
    
    if turret_type == 'Basic':
        description = 'Sell and replace quickly to keep the enemies in range.'
        #image = pygame.image.load("Resources/Images/Sprites/Towers/base_circle.png").convert() # get image
        #image = pygame.image.load(os.path.join(os.path.expanduser("~"), "Resources/Images/Sprites/Towers/base_circle.png"))
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','base_circle.png')).convert() # get image
        rotatable = True # can the tower rotate to shoot?
        radius = 125.0 # range in pixels # MUST HAVE DECIMAL
        speed = 25.0 # time between shots # MUST HAVE DECIMAL 25
        cost = 100 # cost of turret
        attack_image = pygame.image.load(os.path.join('Resources','Images','Sprites','Ammo','bullet black.png')).convert()
        bullet_speed = 10 # speed of shots 10
        bullet_damage = 5 # read what it said you ratard
        targeting = 'cruise' # the attack homes in on the target
        multiple_targets = False # does the shot pick a new target after the previous one has died?
        bullet_limit = None # how many shots can be on the screen at a time
        shot_error = 3 # how much error in degrees is possible
        distance_till_kill = None # how far before the shot self destructs
        hit_target_only = False
        hit_kills_shot = True # dies after only one hit
        exploding_bullet = False # does it go boom?
        rotatable_shot = False # can the shot rotate when its moving?
        timer = None # time between update direction
        timer1 = None
        beam_color = None
        beam_width = None
        has_splash_attacks = False
        splash_radius = None
        splash_damage = None
        has_slowing_attacks = False
        slow_percentage = None
        slow_duration = None
        shoots_at_front = False

    if turret_type == 'Army':
        description = 'sends explosive rounds into your enemies'
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','base_triangle_yellow.png')).convert() # get image
        rotatable = True # can the tower rotate to shoot?
        radius = 175.0 # range in pixels # MUST HAVE DECIMAL
        speed = 25.0 # time between shots # MUST HAVE DECIMAL
        cost = 200 # cost of turret
        attack_image = pygame.image.load(os.path.join('Resources','Images','Sprites','Ammo','bullet dark green.png')).convert()
        bullet_speed = 10 # speed of shots
        bullet_damage = 21 # read what it said you ratard
        targeting = 'cruise' # the attack homes in on the target
        multiple_targets = False # does the shot pick a new target after the previous one has died?
        bullet_limit = None # how many shots can be on the screen at a time
        shot_error = 3 # how much error in degrees is possible
        distance_till_kill = None # how far before the shot self destructs
        hit_target_only = False
        hit_kills_shot = True # dies after only one hit
        exploding_bullet = True
        rotatable_shot = False # can the shot rotate when its moving?
        timer = None # time between update direction
        timer1 = None
        beam_color = None
        beam_width = None
        has_splash_attacks = False
        splash_radius = None
        splash_damage = None
        has_slowing_attacks = False
        slow_percentage = None
        slow_duration = None
        shoots_at_front = False

    if turret_type == 'Machine':
        description = 'sends a blur of bullets flying towards your enemy'
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','base_square_red.png')).convert() # get image
        rotatable = True # can the tower rotate to shoot?
        radius = 125.0 # MUST HAVE DECIMAL
        speed = 7.0 # time between shots # MUST HAVE DECIMAL
        cost = 750
        attack_image = pygame.image.load(os.path.join('Resources','Images','Sprites','Ammo','bullet red.png')).convert()
        bullet_speed = 8 # speed of shots
        bullet_damage = 20
        targeting = 'cruise' # picks target when shot is created
        multiple_targets = False # does the shot pick a new target after the previous one has died?
        bullet_limit = None # how many shots can be on the screen at a time
        shot_error = 20 # how much error in degrees is possible
        distance_till_kill = None # how far before the shot self destructs
        hit_target_only = False
        hit_kills_shot = True # dies after only one hit
        exploding_bullet = False
        rotatable_shot = False # can the shot rotate when its moving?
        timer = None
        timer1 = None
        beam_color = None
        beam_width = None
        has_splash_attacks = False
        splash_radius = None
        splash_damage = None
        has_slowing_attacks = False
        slow_percentage = None
        slow_duration = None
        shoots_at_front = False

    if turret_type == 'Rambo':
        description = 'call in the experts'
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','base_square_gold.png')).convert() # get image
        rotatable = True # can the tower rotate to shoot?
        radius = 225.0 # MUST HAVE DECIMAL
        speed = 8.0 # time between shots # MUST HAVE DECIMAL
        cost = 9000
        attack_image = pygame.image.load(os.path.join('Resources','Images','Sprites','Ammo','bullet red.png')).convert()
        bullet_speed = 10 # speed of shots
        bullet_damage = 72
        targeting = 'cruise' # picks target when shot is created
        multiple_targets = False # does the shot pick a new target after the previous one has died?
        bullet_limit = None # how many shots can be on the screen at a time
        shot_error = 10 # how much error in degrees is possible
        distance_till_kill = None # how far before the shot self destructs
        hit_target_only = False
        hit_kills_shot = True # dies after only one hit
        exploding_bullet = True
        rotatable_shot = False # can the shot rotate when its moving?
        timer = 5
        timer1 = None
        beam_color = None
        beam_width = None
        has_splash_attacks = False
        splash_radius = None
        splash_damage = None
        has_slowing_attacks = False
        slow_percentage = None
        slow_duration = None
        shoots_at_front = False

    if turret_type == 'Splash':
        description = 'Damages all units in the area of explosion'
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','base_octogon_orange.png')).convert() # get image
        rotatable = True # can the tower rotate to shoot?
        radius = 175.0 # range in pixels # MUST HAVE DECIMAL
        speed = 20.0 # time between shots # MUST HAVE DECIMAL
        cost = 800 # cost of turret
        attack_image = pygame.image.load(os.path.join('Resources','Images','Sprites','Ammo','bullet dark green.png')).convert()
        bullet_speed = 10 # speed of shots
        bullet_damage = 45 # read what it said you ratard
        targeting = 'cruise' # the attack homes in on the target
        multiple_targets = False # does the shot pick a new target after the previous one has died?
        bullet_limit = None # how many shots can be on the screen at a time
        shot_error = 3 # how much error in degrees is possible
        distance_till_kill = None # how far before the shot self destructs
        hit_target_only = False
        hit_kills_shot = True # dies after only one hit
        exploding_bullet = True
        rotatable_shot = False # can the shot rotate when its moving?
        timer = None # time between update direction
        timer1 = None
        beam_color = None
        beam_width = None
        has_splash_attacks = True
        splash_radius = 100
        splash_damage = 30
        has_slowing_attacks = False
        slow_percentage = None
        slow_duration = None
        shoots_at_front = False

    if turret_type == 'Bomb':
        description = 'Even MORE explosion. Heavy damage to groups'
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','octogon_dark_base.png')).convert() # get image
        rotatable = True # can the tower rotate to shoot?
        radius = 175.0 # range in pixels # MUST HAVE DECIMAL
        speed = 20.0 # time between shots # MUST HAVE DECIMAL
        cost = 7800 # cost of turret
        attack_image = pygame.image.load(os.path.join('Resources','Images','Sprites','Ammo','bullet dark green.png')).convert()
        bullet_speed = 10 # speed of shots
        bullet_damage = 480 # read what it said you ratard
        targeting = 'cruise' # the attack homes in on the target
        multiple_targets = False # does the shot pick a new target after the previous one has died?
        bullet_limit = None # how many shots can be on the screen at a time
        shot_error = 3 # how much error in degrees is possible
        distance_till_kill = None # how far before the shot self destructs
        hit_target_only = False
        hit_kills_shot = True # dies after only one hit
        exploding_bullet = True
        rotatable_shot = False # can the shot rotate when its moving?
        timer = None # time between update direction
        timer1 = None
        beam_color = None
        beam_width = None
        has_splash_attacks = True
        splash_radius = 100
        splash_damage = 400
        has_slowing_attacks = False
        slow_percentage = None
        slow_duration = None
        shoots_at_front = False
        
    if turret_type == 'Homing':
        description = 'shoots a tracking bullet that follows the target'
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','homing2.png')).convert() # get image
        rotatable = True # can the tower rotate to shoot?
        radius = 225.0 # range in pixels # MUST HAVE DECIMAL
        speed = 50.0 # time between shots # MUST HAVE DECIMAL
        cost = 800 # cost of turret
        attack_image = pygame.image.load(os.path.join('Resources','Images','Sprites','Ammo','bullet dark blue.png')).convert()
        bullet_speed = .26 # speed of shots
        bullet_damage = 110 # read what it said you ratard
        targeting = 'homing' # the attack homes in on the target
        multiple_targets = False # does the shot pick a new target after the previous one has died?
        bullet_limit = None # how many shots can be on the screen at a time
        shot_error = None # how much error in degrees is possible
        distance_till_kill = None # how far before the shot self destructs
        hit_target_only = True
        hit_kills_shot = True # dies after only one hit
        exploding_bullet = True
        rotatable_shot = False # can the shot rotate when its moving?
        timer = 5 # time between update direction
        timer1 = None
        beam_color = None
        beam_width = None
        has_splash_attacks = False
        splash_radius = None
        splash_damage = None
        has_slowing_attacks = False
        slow_percentage = None
        slow_duration = None
        shoots_at_front = False

    if turret_type == 'Homing V2':
        description = 'picks a new target when the previous one has died'
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','homing_white.png')).convert() # get image
        rotatable = True # can the tower rotate to shoot?
        radius = 275.0 # range in pixels # MUST HAVE DECIMAL
        speed = 25.0 # time between shots # MUST HAVE DECIMAL
        cost = 6000 # cost of turret
        attack_image = pygame.image.load(os.path.join('Resources','Images','Sprites','Ammo','bullet light blue.png')).convert()
        bullet_speed = .26 # speed of shots
        bullet_damage = 220 # read what it said you ratard
        targeting = 'homing' # the attack homes in on the target
        multiple_targets = True # does the shot pick a new target after the previous one has died?
        bullet_limit = None # how many shots can be on the screen at a time
        shot_error = None # how much error in degrees is possible
        distance_till_kill = None # how far before the shot self destructs
        hit_target_only = True
        hit_kills_shot = True # dies after only one hit
        exploding_bullet = True
        rotatable_shot = False # can the shot rotate when its moving?
        timer = 5 # time between update direction
        timer1 = None
        beam_color = None
        beam_width = None
        has_splash_attacks = False
        splash_radius = None
        splash_damage = None
        has_slowing_attacks = False
        slow_percentage = None
        slow_duration = None
        shoots_at_front = False

    if turret_type == 'Nature':
        description = 'harness the power of nature!'
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','base_triangle_green.png')).convert() # get image
        rotatable = True # can the tower rotate to shoot?
        radius = 175.0 # range in pixels # MUST HAVE DECIMAL
        speed = 15.0 # time between shots # MUST HAVE DECIMAL
        cost = 350 # cost of turret
        attack_image = pygame.image.load(os.path.join('Resources','Images','Sprites','Ammo','bullet green.png')).convert()
        bullet_speed = 10 # speed of shots
        bullet_damage = 18 # read what it said you ratard
        targeting = 'cruise' # the attack homes in on the target
        multiple_targets = False # does the shot pick a new target after the previous one has died?
        bullet_limit = None # how many shots can be on the screen at a time
        shot_error = None # how much error in degrees is possible
        distance_till_kill = None # how far before the shot self destructs
        hit_target_only = False
        hit_kills_shot = True # dies after only one hit
        exploding_bullet = False # does it go boom?
        rotatable_shot = False # can the shot rotate when its moving?
        timer = None # time between update direction
        timer1 = None
        beam_color = None
        beam_width = None
        has_splash_attacks = False
        splash_radius = None
        splash_damage = None
        has_slowing_attacks = False
        slow_percentage = None
        slow_duration = None
        shoots_at_front = False

    if turret_type == 'Fly':
        description = 'releases a swarm of flies to bite at your enemies. Damage over time.'
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','new_fly.png')).convert() # get image
        rotatable = False # can the tower rotate to shoot?
        radius = 125.0 # range in pixels # MUST HAVE DECIMAL
        speed = 30.0 # time between shots # MUST HAVE DECIMAL
        cost = 500 # cost of turret
        attack_image = pygame.image.load(os.path.join('Resources','Images','Sprites','Ammo','fly new.png')).convert()
        bullet_speed = 1 # speed of shots
        bullet_damage = 12 # read what it said you ratard
        targeting = 'bee' # the attack homes in on the target
        multiple_targets = False # does the shot pick a new target after the previous one has died?
        bullet_limit = None # how many shots can be on the screen at a time
        shot_error = None # how much error in degrees is possible
        distance_till_kill = None # how far before the shot self destructs
        hit_target_only = True
        hit_kills_shot = False # dies after only one hit
        exploding_bullet = False
        rotatable_shot = True # can the shot rotate when its moving?
        timer = 5 # time between update direction
        timer1 = 7 # time between attacks
        beam_color = None
        beam_width = None
        has_splash_attacks = False
        splash_radius = None
        splash_damage = None
        has_slowing_attacks = False
        slow_percentage = None
        slow_duration = None
        shoots_at_front = False

    if turret_type == 'Bee':
        description = 'ultimate stinging power!'
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','new_bee.png')).convert() # get image
        rotatable = False # can the tower rotate to shoot?
        radius = 175.0 # range in pixels # MUST HAVE DECIMAL
        speed = 15.0 # time between shots # MUST HAVE DECIMAL
        cost = 6000 # cost of turret
        attack_image = pygame.image.load(os.path.join('Resources','Images','Sprites','Ammo','bee.png')).convert()
        bullet_speed = 1 # speed of shots 10
        bullet_damage = 37 # read what it said you ratard
        targeting = 'bee' # the attack homes in on the target
        multiple_targets = False # does the shot pick a new target after the previous one has died?
        bullet_limit = None # how many shots can be on the screen at a time
        shot_error = 5 # how much error in degrees is possible
        distance_till_kill = None # how far before the shot self destructs
        hit_target_only = True
        hit_kills_shot = False # dies after only one hit
        exploding_bullet = False
        rotatable_shot = True # can the shot rotate when its moving?
        timer = 5 # time between update direction
        timer1 = 6 # time between attacks
        beam_color = None
        beam_width = None
        has_splash_attacks = False
        splash_radius = None
        splash_damage = None
        has_slowing_attacks = False
        slow_percentage = None
        slow_duration = None
        shoots_at_front = False

    if turret_type == 'Fire':
        description = 'short range quick firing.'
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','base_triangle_red.png')).convert() # get image
        rotatable = True # can the tower rotate to shoot?
        radius = 160.0 # range in pixels # MUST HAVE DECIMAL
        speed = 5.0 # time between shots # MUST HAVE DECIMAL
        cost = 700 # cost of turret
        attack_image = pygame.image.load(os.path.join('Resources','Images','Sprites','Ammo','bullet dark red.png')).convert()
        bullet_speed = 3 # speed of shots
        bullet_damage = 15 # read what it said you ratard
        targeting = 'cruise' # the attack homes in on the target
        multiple_targets = False # does the shot pick a new target after the previous one has died?
        bullet_limit = None # how many shots can be on the screen at a time
        shot_error = 5 # how much error in degrees is possible
        distance_till_kill = radius # how far before the shot self destructs
        hit_target_only = False
        hit_kills_shot = True # dies after only one hit
        exploding_bullet = True # does it go boom?
        rotatable_shot = False # can the shot rotate when its moving?
        timer = None # time between update direction
        timer1 = None
        beam_color = None
        beam_width = None
        has_splash_attacks = False
        splash_radius = None
        splash_damage = None
        has_slowing_attacks = False
        slow_percentage = None
        slow_duration = None
        shoots_at_front = False
        
    if turret_type == 'Volcano':
        description = 'erupts in random directions damaging all who come near'
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','volcano.png')).convert() # get image
        rotatable = False # can the tower rotate to shoot?
        radius = 110.0 # MUST HAVE DECIMAL
        #radius = 800.0 # MUST HAVE DECIMAL for testing fibinachi
        speed = 2.0 # time between shots # MUST HAVE DECIMAL
        speed = 1.0 # time between shots # MUST HAVE DECIMAL
        cost = 8000
        attack_image = pygame.image.load(os.path.join('Resources','Images','Sprites','Ammo','bullet red.png')).convert()
        bullet_speed = 1 # speed of shots
        bullet_damage = 100
        targeting = 'cruise' # picks target when shot is created
        multiple_targets = False # does the shot pick a new target after the previous one has died?
        bullet_limit = None # how many shots can be on the screen at a time
        shot_error = 360 # how much error in degrees is possible
        distance_till_kill = radius # how far before the shot self destructs
        distance_till_kill = radius * 4 # how far before the shot self destructs
        hit_target_only = False
        hit_kills_shot = True # dies after only one hit
        exploding_bullet = True
        rotatable_shot = False # can the shot rotate when its moving?
        timer = None
        timer1 = None
        beam_color = None
        beam_width = None
        has_splash_attacks = False
        splash_radius = None
        splash_damage = None
        has_slowing_attacks = False
        slow_percentage = None
        slow_duration = None
        shoots_at_front = False

    if turret_type == 'Planet':
        description = 'fires moons in an orbit around the tower. Max 3 at a time'
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','earth.png')).convert() # get image
        rotatable = False # can the tower rotate to shoot?
        radius = 200.0 # range in pixels # MUST HAVE DECIMAL
        speed = 200.0 # time between shots # MUST HAVE DECIMAL
        cost = 1500 # cost of turret
        attack_image = pygame.image.load(os.path.join('Resources','Images','Sprites','Ammo','moon.png')).convert()
        bullet_speed = 1 # speed of shots
        bullet_damage = 390 # read what it said you ratard
        targeting = 'orbital' # the attack homes in on the target
        multiple_targets = False # does the shot pick a new target after the previous one has died?
        bullet_limit = 3 # how many shots can be on the screen at a time 3
        shot_error = None # how much error in degrees is possible
        distance_till_kill = None # how far before the shot self destructs
        hit_target_only = False
        hit_kills_shot = True # dies after only one hit
        exploding_bullet = True
        rotatable_shot = False # can the shot rotate when its moving?
        timer = None # time between update direction
        timer1 = 5 # time in seconds till maximum orbit radius
        beam_color = None
        beam_width = None
        has_splash_attacks = False
        splash_radius = None
        splash_damage = None
        has_slowing_attacks = False
        slow_percentage = None
        slow_duration = None
        shoots_at_front = False

    if turret_type == 'Galaxy':
        description = 'more gravitational firepower. Max 5 shots at a time'
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','galaxy.png')).convert() # get image
        rotatable = False # can the tower rotate to shoot?
        radius = 200.0 # range in pixels # MUST HAVE DECIMAL
        speed = 200.0 # time between shots # MUST HAVE DECIMAL
        cost = 30000 # cost of turret
        attack_image = pygame.image.load(os.path.join('Resources','Images','Sprites','Ammo','planet.png')).convert()
        bullet_speed = 1 # speed of shots
        bullet_damage = 500 # read what it said you ratard
        targeting = 'orbital' # the attack homes in on the target
        multiple_targets = False # does the shot pick a new target after the previous one has died?
        bullet_limit = 5 # how many shots can be on the screen at a time
        shot_error = None # how much error in degrees is possible
        distance_till_kill = None # how far before the shot self destructs
        hit_target_only = False
        hit_kills_shot = True # dies after only one hit
        exploding_bullet = True
        rotatable_shot = False # can the shot rotate when its moving?
        timer = None # time between update direction
        timer1 = 5 # time in seconds till maximum orbit radius
        beam_color = None
        beam_width = None
        has_splash_attacks = False
        splash_radius = None
        splash_damage = None
        has_slowing_attacks = False
        slow_percentage = None
        slow_duration = None
        shoots_at_front = False
    
    if turret_type == 'Science':
        description = 'Instant hit! Never miss a shot again!'
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','base_triangle_blue.png')).convert() # get image
        rotatable = True # can the tower rotate to shoot?
        radius = 125.0 # MUST HAVE DECIMAL
        speed = 10.0 # time between shots # MUST HAVE DECIMAL
        cost = 300
        attack_image = None
        bullet_speed = None # speed of shots
        bullet_damage = 10
        targeting = 'beam' # 
        multiple_targets = False # does the shot pick a new target after the previous one has died?
        bullet_limit = None # how many shots can be on the screen at a time
        shot_error = None # how much error in degrees is possible
        distance_till_kill = None # how far before the shot self destructs
        hit_target_only = True
        hit_kills_shot = True # dies after only one hit
        exploding_bullet = False
        rotatable_shot = False # can the shot rotate when its moving?
        timer = 16 # fade out speed
        timer1 = None
        beam_color = (115,8,38)
        beam_width = 3
        has_splash_attacks = False
        splash_radius = None
        splash_damage = None
        has_slowing_attacks = False
        slow_percentage = None
        slow_duration = None
        shoots_at_front = False

    if turret_type == 'Slow':
        description = 'Lower the speed of targets to 70%'
        #image = pygame.image.load("Resources/Images/Sprites/Towers/base_circle.png").convert() # get image
        #image = pygame.image.load(os.path.join(os.path.expanduser("~"), "Resources/Images/Sprites/Towers/base_circle.png"))
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','slow.png')).convert() # get image
        rotatable = True # can the tower rotate to shoot?
        radius = 125.0 # range in pixels # MUST HAVE DECIMAL
        speed = 30.0 # time between shots # MUST HAVE DECIMAL 25
        cost = 700 # cost of turret
        attack_image = pygame.image.load(os.path.join('Resources','Images','Sprites','Ammo','bullet dark blue.png')).convert()
        bullet_speed = 10 # speed of shots 10
        bullet_damage = 1 # read what it said you ratard
        targeting = 'cruise' # the attack homes in on the target
        multiple_targets = False # does the shot pick a new target after the previous one has died?
        bullet_limit = None # how many shots can be on the screen at a time
        shot_error = 3 # how much error in degrees is possible
        distance_till_kill = None # how far before the shot self destructs
        hit_target_only = False
        hit_kills_shot = True # dies after only one hit
        exploding_bullet = False # does it go boom?
        rotatable_shot = False # can the shot rotate when its moving?
        timer = None # time between update direction
        timer1 = None
        beam_color = None
        beam_width = None
        has_splash_attacks = False
        splash_radius = None
        splash_damage = None
        has_slowing_attacks = True
        slow_percentage = .6
        slow_duration = 70
        shoots_at_front = False

    if turret_type == 'Freeze':
        description = 'Slows the enemies down to a crawl of 40%'
        #image = pygame.image.load("Resources/Images/Sprites/Towers/base_circle.png").convert() # get image
        #image = pygame.image.load(os.path.join(os.path.expanduser("~"), "Resources/Images/Sprites/Towers/base_circle.png"))
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','freeze.png')).convert() # get image
        rotatable = True # can the tower rotate to shoot?
        radius = 125.0 # range in pixels # MUST HAVE DECIMAL
        speed = 10.0 # time between shots # MUST HAVE DECIMAL 25
        cost = 25000 # cost of turret
        attack_image = pygame.image.load(os.path.join('Resources','Images','Sprites','Ammo','bullet dark blue.png')).convert()
        bullet_speed = 10 # speed of shots 10
        bullet_damage = 1 # read what it said you ratard
        targeting = 'cruise' # the attack homes in on the target
        multiple_targets = False # does the shot pick a new target after the previous one has died?
        bullet_limit = None # how many shots can be on the screen at a time
        shot_error = 3 # how much error in degrees is possible
        distance_till_kill = None # how far before the shot self destructs
        hit_target_only = False
        hit_kills_shot = True # dies after only one hit
        exploding_bullet = False # does it go boom?
        rotatable_shot = False # can the shot rotate when its moving?
        timer = None # time between update direction
        timer1 = None
        beam_color = None
        beam_width = None
        has_splash_attacks = False
        splash_radius = None
        splash_damage = None
        has_slowing_attacks = True
        slow_percentage = .4
        slow_duration = 120
        shoots_at_front = False

    if turret_type == 'DEW':
        description = 'A quick firing Directed-Energy Weapon that does not miss.'
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','base_octogon_blue.png')).convert() # get image
        rotatable = True # can the tower rotate to shoot?
        radius = 125.0 # MUST HAVE DECIMAL
        speed = 5.0 # time between shots # MUST HAVE DECIMAL
        cost = 900
        attack_image = None
        bullet_speed = None # speed of shots
        bullet_damage = 10
        targeting = 'beam' # 
        multiple_targets = False # does the shot pick a new target after the previous one has died?
        bullet_limit = None # how many shots can be on the screen at a time
        shot_error = None # how much error in degrees is possible
        distance_till_kill = None # how far before the shot self destructs
        hit_target_only = True
        hit_kills_shot = True # dies after only one hit
        exploding_bullet = False
        rotatable_shot = False # can the shot rotate when its moving?
        timer = 18 # fade out speed
        timer1 = None
        beam_color = (18,200,244)
        beam_width = 3
        has_splash_attacks = False
        splash_radius = None
        splash_damage = None
        has_slowing_attacks = False
        slow_percentage = None
        slow_duration = None
        shoots_at_front = False

    if turret_type == 'Hydro DEW':
        description = 'Hydrogen powered for extreme damage!'
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','base_square_light_blue.png')).convert() # get image
        rotatable = True # can the tower rotate to shoot?
        radius = 125.0 # MUST HAVE DECIMAL
        speed = 3.0 # time between shots # MUST HAVE DECIMAL
        cost = 14000
        attack_image = None
        bullet_speed = None # speed of shots
        bullet_damage = 40
        targeting = 'beam' # 
        multiple_targets = False # does the shot pick a new target after the previous one has died?
        bullet_limit = None # how many shots can be on the screen at a time
        shot_error = None # how much error in degrees is possible
        distance_till_kill = None # how far before the shot self destructs
        hit_target_only = True
        hit_kills_shot = True # dies after only one hit
        exploding_bullet = False
        rotatable_shot = False # can the shot rotate when its moving?
        timer = 18 # fade out speed
        timer1 = None
        beam_color = (232,240,10)
        beam_width = 5
        has_splash_attacks = False
        splash_radius = None
        splash_damage = None
        has_slowing_attacks = False
        slow_percentage = None
        slow_duration = None
        shoots_at_front = False

    if turret_type == 'Pulse Beam':
        description = 'Charged high energy beams allow for slow, long range, high damage attacks'
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','base_square_light_green.png')).convert() # get image
        rotatable = True # can the tower rotate to shoot?
        radius = 235.0 # MUST HAVE DECIMAL
        speed = 55.0 # time between shots # MUST HAVE DECIMAL
        cost = 1100
        attack_image = None
        bullet_speed = None # speed of shots
        bullet_damage = 180
        targeting = 'beam' # 
        multiple_targets = False # does the shot pick a new target after the previous one has died?
        bullet_limit = None # how many shots can be on the screen at a time
        shot_error = None # how much error in degrees is possible
        distance_till_kill = None # how far before the shot self destructs
        hit_target_only = True
        hit_kills_shot = True # dies after only one hit
        exploding_bullet = False
        rotatable_shot = False # can the shot rotate when its moving?
        timer = 13 # fade out speed
        timer1 = None
        beam_color = (18,200,244)
        beam_width = 3
        has_splash_attacks = False
        splash_radius = None
        splash_damage = None
        has_slowing_attacks = False
        slow_percentage = None
        slow_duration = None
        shoots_at_front = False

    if turret_type == 'Robot':
        description = 'The ultimate in technology. Huge range and tons of damage.'
        image = pygame.image.load(os.path.join('Resources','Images','Sprites','Towers','robot.png')).convert() # get image
        rotatable = False # can the tower rotate to shoot?
        radius = 235.0 # MUST HAVE DECIMAL
        speed = 55.0 # time between shots # MUST HAVE DECIMAL
        cost = 24200
        attack_image = None
        bullet_speed = None # speed of shots
        bullet_damage = 800
        targeting = 'beam' # 
        multiple_targets = False # does the shot pick a new target after the previous one has died?
        bullet_limit = None # how many shots can be on the screen at a time
        shot_error = None # how much error in degrees is possible
        distance_till_kill = None # how far before the shot self destructs
        hit_target_only = True
        hit_kills_shot = True # dies after only one hit
        exploding_bullet = False
        rotatable_shot = False # can the shot rotate when its moving?
        timer = 13 # fade out speed
        timer1 = None
        beam_color = (18,200,244)
        beam_width = 3
        has_splash_attacks = False
        splash_radius = None
        splash_damage = None
        has_slowing_attacks = False
        slow_percentage = None
        slow_duration = None
        shoots_at_front = False
    
        
    image.set_colorkey(image.get_at((0, 0))) # transparent
    if attack_image:
        attack_image.set_colorkey(attack_image.get_at((0, 0))) # transparent
    if shot_error:
        shot_error *= 0.0174532 # convert to radians

    stats = [] # create an empty list for the stats
    if which_stats == 'all_stats': # if we want all the stats
        #is this used anymore??????
        stats.extend([image, rotatable, radius, speed, cost, attack_image,
                      bullet_speed, bullet_damage, targeting, multiple_targets,
                      bullet_limit, timer, timer1]) # add stuff to the stats list
        return stats # send the stats to TurretSprites.Shot.__init__()
    if which_stats == 'image':
        return image
    if which_stats == 'radius':
        return radius 
    if which_stats == 'cost':
        return cost
    if which_stats == 'basic_stats':
        stats.extend([image, rotatable, radius, speed, cost, targeting, bullet_limit, shoots_at_front])
        return stats
    if which_stats == 'attack_stats':
        stats.extend([radius, attack_image, bullet_speed, bullet_damage,
                      targeting, multiple_targets, bullet_limit, shot_error,
                      distance_till_kill, hit_target_only, hit_kills_shot,
                      exploding_bullet, rotatable_shot, timer, timer1,
                      beam_color, beam_width, has_splash_attacks,
                      splash_radius, splash_damage, has_slowing_attacks,
                      slow_percentage, slow_duration])
        return stats
    if which_stats == 'info_stats': # used in the ingame menu
        stats.extend([description, image, cost, radius, speed, bullet_damage])
        return stats
    

         # send the stats



def enemy_stats(enemy_type, which_stats):

    #stores all of the info for the enemies!@!$!@$#^&
    stats = []
    images = []
    base_life = 0 # we need to send SOMETHING to the wave info in HUDs
    
    if enemy_type == 'basic':
        images.append(pygame.image.load(os.path.join('Resources','Images','Sprites','Enemies','basic.png')).convert())
        base_life = 4
        speed = 2.5
        reward = 10
        wave_ammount = 10 # ammount of enemies per wave

    if enemy_type == 'fast':
        images.append(pygame.image.load(os.path.join('Resources','Images','Sprites','Enemies','fast.png')).convert())
        base_life = 3
        speed = 3.5
        reward = 10
        wave_ammount = 10
        
    if enemy_type == 'slow':
        images.append(pygame.image.load(os.path.join('Resources','Images','Sprites','Enemies','slow.png')).convert())
        base_life = 8
        speed = 1.3
        reward = 10
        wave_ammount = 10


    if enemy_type == 'boss':
        images.append(pygame.image.load(os.path.join('Resources','Images','Sprites','Enemies','boss.png')).convert())
        base_life = 85
        speed = 1.0
        reward = 100
        wave_ammount = 1

    if enemy_type == 'zombie':
        images = load_sliced_sprites(30, 30, os.path.join('Resources','Images','Sprites','Enemies','zombie tile set.png'))
        base_life = 200
        speed = 0.7
        reward = 200
        wave_ammount = 1

    if which_stats == 'all_stats':
        stats.extend([images, base_life, speed, reward])
        return stats

    if which_stats == 'life':
        return base_life

    if which_stats == 'wave_stats':
        return wave_ammount
    

