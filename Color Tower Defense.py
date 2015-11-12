############################################################################################
# Color Tower Defense
# Source Code
# programed by Josh Cockrell.
# 
# contact Josh Cockrell @ MadCloudGames@gmail.com with any comments, questions, or changes
#
# -----This game is a work in progress-----
# This project is released under the GNU General Public License V3
# You dont need to ask to use this code but
# we would love to hear what you think about it!
############################################################################################
################################################################################
# madcloudgames.blogspot.com
############################################################################################
############################################################################################

#"what is art?": any non-functional source of value is art. 
# PEOPLE WHO HELPED
# Eli Benderski for his amazing website
# Dr0id for his tile loader module and help with getting map collisions working
# HydroKirby for help with py2exe/python logic
# EmCeeMayor for help with py2exe
# nClam for save file help/os.path.join help/resource packaging
# exarcun for save file format help
# themissinglint for help with display updates/play testing/balancing
# lolrus for linux testing
# huge thanks to Tess and Tyler for artwork
# HUGE thanks to Tyler for music
# Ryan Brown
'''

BEFORE RELEASE CHECKLIST
    make all the save files new
    make player open maps to default
    fix corrupt images
    turn sound on
    set money to default

 
FEEDBACK:
more emphasis on next wave, pause game, and main menu button.
use game over music for ingame music
arrow on in side of path
build tower mode cancel if you have less than 100 and click
wave life and player life are confusing
income curve is weird.
As soon as I can afford a 2 nature towers, the game gets pretty easy.
But until then I have a really hard time.
make it easier to move towers around
nature/fly/bee is overpowered.
no slow or splash
display next wave info


LIKES:
towers can miss
first ones get 100% back
The variety in towers you have is really sweet.
different from normal tower defense

IN GAME SONG:
strongest part of the song is the part that's just the bassline and drums
And he liked the first synth wash over it.
But to use the synth very sparingly.
the strongest part is the second breakdown.  There is only bass and drumming.. The more simple of the two bass patterns.


os.path.join:
nClam: Yes, to use os.path.join you specify the directories as arguments like ("dir1","dir2","filename.ext")
nClam: You should probably also store the current working directory somewhere so you can do something like if os.path.exists(os.path.join(cwd,"dir1","dir2","filename.ext")): do some code, else: print error file not found

--------------------------------------------------------------------------------   

PRIORITY 1- Urgent!
    balancing (not too hard but still a challenge, no "best" way to play) ALWAYS CURRENT
        different variety of enemies (colors, could help with balancing)

    Fix sell buttons FIXED
    get rid of t (kill all enemies on screen) FIXED 
    infinite money glitch FIXED
    fix mac source code files FIXED
    stop wrong maps from being drawn FIXED
    custom icon - use a resource editor FIXED
    give homing II a name FIXED
    fix pointing arrow FIXED
    rename Hydro DEW to DEW and Voltaic arc to Hydro DEW FIXED
    credits FIXED
    make rotation bool FIXED
    package resources inside of the exe/installer (is this possible???)(not the best way[aClam]) CANCELED
    make difficulty select screen FIXED
    switch over to os.path.join FIXED
    better bee towers (more attack) FIXED
    handle all maps completed (game won) FIXED
    load game menu buttons(delete/save file buttons) FIXED
    scaling (making new basic towers cost more after bought/ making enemies exponentially increase difficuilty) FIXED
    handle single map completed (map complete screen) -FIXED
    save game function (auto) FIXED
    load game function displays after main menu FIXED
    
PRIORITY 2- Needs

    homing V2 are too OP FIXED
    credits include me for art FIXED
    get rid of all sounds except 'Soundeffects','Percs','Chip_Perc_8.wav' FIXED
    galaxy shot more like planet shots FIXED 
    know which direction the enemies come from (arrow maybe) FIXED
    tower replacement mode CANCELED
    tech tower paths FIXED
    orbital shots respawn time -FIXED
    fix delete file button FIXED
    change pygame window header text FIXED
    beam targeting type FIXED
    info box displays not enough money/ other errors...  FIXED
    hotkeys FIXED
    fade out and into game FIXED
    fly tower image FIXED
    fix in game menu buttons FIXED
    fix pause screen image FIXED
    towers more spread out in tower paths (redo paths? too little in nature) -FIXED
    shrink tower placement info box FIXED 
    orbital shots auto destruct after orbital is destroyed FIXED
    orbital shots maximun number FIXED
    orbital shots range issues FIXED
    raise shot kill boarders (homing disapear FIXED
    get rid of prints FIXED
    hotkeys FIXED
    new homingII image (just more flashy homingI) FIXED
    make slows shoot at front of line CANCELED


PRIORITY 3- Would be nice
    in game sounds CURRENT

    make basic text black FIXED
    infinite game loop depth FIXED
    make map.draw, HUDs.draw go faster (performace speed) FIXED
    new shot colors - FIXED
    rotate towers towards target - FIXED
    toggle sound button (ON/OFF) - FIXED
    center and crop all of the tower images FIXED
    flamethrower tower - FIXED
    change wave font - FIXED
    fix in game buttons to be python generated instead of photoshop images -FIXED
    fix while loop lag in mad_cloud_games startup FIXED
    nicer bee tower image (outline/shading?) -Tyler/Chris FIXED
    machine gun tower shoots faster, weaker, and more inaccurate FIXED
    change question marks in select map menu to locks - CANCELED
    better image rotation http://www.leptonica.com/rotation.html - CANCELED
    cant hit enemies off screen CANCELED





Josh Cockrell - Technical Director, Systems Architect, Design, Gameplay, Audio

Tyler Christensen - Music, Art

Tess Bybee - Art

Chris Breinholt - Critical decision choices concerning white colored robots. (Among other things)

Special Thanks - Dr0id, HydroKirby, EmCeeMayor, nClam, Eli Benderski,
exarcun, themissinglint, lolrus

'''



##### Imports #####
import pygame
import random
import operator
from general_stats import screen, fps, clock, tile
from load_save_file import save_game

import screenlogo
import screenmain
import screenmapcomplete
import screengamecomplete
import screenmapselection
import screenpause
import screensavedgame
import screengameover

import tiledtmxloader
import HUDs
import EnemySprites
import TurretSprites
from sprite_stats import *
from object_groups import *
from wave_stats import *
from map_directions import *
from tower_range import *
from explosion import *
from life_bar import *
from snap_to_grid import *
from reset_game import *
from vector import *
from music import *



###### main game loop #######
def main():

    music.music_on = True # music on/off
    
    
    ##### Initialize pygame #####
    pygame.init()

    ##### run/open the main menu first thing####

    music.play(music.channel_fx, music.thunder, False)

    running_program = True
    running_main_menu = True
    running_save_file = True
    running_map_select = True

    while running_program:
        running_program = screenlogo.run()
        if running_program == False:
            break
        
        running_main_menu = True
        
        while running_main_menu:
            music.play(music.channel_menu, music.menu_music, True)
            
            running_main_menu = screenmain.run()
            if running_main_menu == False:
                running_main_menu = False
                running_program = False
                break
            running_save_file = True
            while running_save_file:
                #save_file_info = load_save_file()
                save_file_info = screensavedgame.run()

                # if quitting
                if save_file_info[2] == True:
                    running_save_file = False
                    running_main_menu = False
                    running_program = False
                    break
                elif save_file_info[2] == False:
                    player = save_file_info[0]
                    player.save_file_number = save_file_info[1]


                running_map_select = True

                while running_map_select:

                    map_info = screenmapselection.run(player)
                    # if quitting
                    if map_info[1] == True:
                        running_map_select = False
                        running_save_file = False
                        running_main_menu = False
                        running_program = False
                        break
                    elif map_info[1] == False:

                        player.map = map_info[0]
                        reset(player) # reset everything

                        ##### auto add objects to groups that were defined in "object_groups" module #####
                        EnemySprites.Enemy.groups = enemies, all_draw, all_update, all_objects  # auto add Enemy to enemies group
                        TurretSprites.Turret.groups = turrets, all_update, all_draw, all_objects # same as above
                        TurretSprites.Shot.groups = shots, all_draw, all_objects
                        TurretSprites.TurretPlacer.groups = turretplacers, all_draw, all_objects
                        Tower_Range.groups = turret_range, all_draw, all_objects
                        tiledtmxloader.World_map.groups = map_draw
                        HUDs.Fading_Cover.groups = fading_covers, huds
                        HUDs.Info_Bar.groups = huds
                        HUDs.Button.groups = huds, buttons
                        HUDs.Direction_Arrow.groups = huds
                        HUDs.Sound_Toggle.groups = huds
                        HUDs.Pause.groups = huds
                        HUDs.Main_Menu.groups = huds
                        HUDs.Next_Wave.groups = huds
                        HUDs.Build_Turret_Button.groups = huds
                        HUDs.Life.groups = huds
                        HUDs.Wave_Info.groups = huds, wave_info_group
                        HUDs.Money.groups = huds
                        Explosion.groups = explosions, all_draw, all_update, all_objects
                        Life_Bar.groups = all_draw, all_objects

                        
                        ##### reseting #####
                        #clear the groups
                        for h in huds:
                            h.kill()
                            
                        ##### create starting objects #####
                        wave.start_new_map(player.map)
                        game_map = tiledtmxloader.World_map(os.path.join('Resources','Map Data','map' + str(player.map) + '.tmx'))
                        fading_cover = HUDs.Fading_Cover()
                        info_bar = HUDs.Info_Bar()
                        side_bar = HUDs.Side_Bar()
                        in_game_menu = HUDs.In_Game_Menu()
                        direction_arrow = HUDs.Direction_Arrow()
                        sound_toggle_button = HUDs.Sound_Toggle()
                        pause_button = HUDs.Pause()
                        main_menu_button = HUDs.Main_Menu()
                        next_wave_button = HUDs.Next_Wave()
                        HUDs.Wave_Info()
                        build_turret_button = HUDs.Build_Turret_Button()
                        life = HUDs.Life(player)
                        money = HUDs.Money(player.money)

                        direction_arrow.start_new_map(player)


                        ##### general loop values #####
                        faded_in = False
                        first_wave_started = False # used in the direction arrow vanish
                        placing_tower = False # we are not placing a tower
                        turret_selected = None # we have not selected a turret
                        object_clicked = False # we have not clicked on any game objects
                        mouse_over_button = False # used in mouse over events
                        running = True # i dont know if you've heard of "running" as in running a progrom, but its kindof a big deal
                        player.game_over = False # this game is NOT over
                        player.game_won = False
                        GAME_OVER_TIMER = (fps * 2) # two seconds rest after game over
                        game_over_timer = GAME_OVER_TIMER # for reseting

                        if player.difficulty == 'easy':
                            player.money = 350
                        if player.difficulty == 'hard':
                            player.money = 275
                        # player.money = 2750000 # 275
                        player.game_over = False
                        player.game_won = False
                        player.quiting = False
                        quit_reason = ''
                        '''
                        quitting reasons include:
                        'main menu' kicks back to screenmain
                        'full quit' exits program
                        'map select' kick to map selection
                        '''

                        music.stop(music.channel_menu)

                        music.play(music.channel_game, music.game_music, True) # play music

                        game_paused = False
                        
                        ################################################################################
                        while running:
                            clock.tick(30) #setting frame rate

                            game_map.map_collision(pause_button.rect)

                            ##### Events Mouse / Keyboard #####
                            for event in pygame.event.get():

                                ##### Quiting #####
                                if event.type == pygame.QUIT: # click the 'x' to quit
                                    running = False
                                    quit_reason = 'full quit'
                                elif event.type == pygame.KEYDOWN:
                                    click = pygame.mouse.get_pos()

                                    ##### escape / space buttons #####
                                    if event.key in [pygame.K_ESCAPE, pygame.K_SPACE]: # hit escape to exit
                                        
                                        if placing_tower == True: # if we're placing a tower
                                            placing_tower = False # not anymore
                                            turretplacers.sprite.kill() # kill the placer
                                            for t in turret_range:
                                                t.kill() # destroy the turret_range
                                            HUDs.clear_info_menu()
                                                
                                        elif turret_selected: # if a turret is selected
                                            turret_selected = None
                                            HUDs.clear_info_menu() # clear all elements on the info menu
                                            for r in turret_range: # clear the tower range
                                                r.kill()
                                                
                                    elif event.key in [pygame.K_n]:
                                        if wave.wave_done == True: # if the current wave is done
                                            
                                            wave.start_new_wave()
                                            for i in wave_info_group:
                                                i.kill()
                                            HUDs.Wave_Info()
                                            if first_wave_started == False: # check so we only vanish once
                                                first_wave_started = True
                                                direction_arrow.vanish() # go away

                                    elif event.key in [pygame.K_b]:
                                        if not placing_tower:
                                            turret_cost = turret_stats(build_turret_button.turret_type, 'cost') # get the cost
                                            if player.money >= turret_cost:
                                                HUDs.clear_info_menu() # clear all elements on the info menu
                                                for t in turret_range: # clear the tower range
                                                    t.kill()
                                                TurretSprites.TurretPlacer(click, build_turret_button.turret_type)
                                                placing_tower = True
                                                turret_radius = turret_stats(build_turret_button.turret_type, 'radius') # get the radius
                                                Tower_Range(click, turret_radius) # create a range
                                                HUDs.info_menu('turret placement', build_turret_button.turret_type)

                                    #balancers hack
                                    
                                    #elif event.key in [pygame.K_t]:
                                        #for e in enemies:
                                            #e.get_hit(70000, player)

                                        
                                            
                                    elif event.key in [pygame.K_p]:
                                        game_paused = True # pause code is at the bottom of the main loop
                                                                    
                                    elif event.key in [pygame.K_1]:
                                        if turret_selected:
                                            for b in buttons:
                                                if b.slot == 1:
                                                    if b.button_type == 'upgrade': # if its an upgrade button
                                                        if player.money >= b.upgrade_cost: # if we have enough money
                                                            turret_selected.upgrade(b.turret_type, player) # upgrade
                                        
                                    elif event.key in [pygame.K_2]:
                                        if turret_selected:
                                            for b in buttons:
                                                if b.slot == 2:
                                                    if b.button_type == 'upgrade': # if its an upgrade button
                                                        if player.money >= b.upgrade_cost: # if we have enough money
                                                            turret_selected.upgrade(b.turret_type, player) # upgrade

                                    elif event.key in [pygame.K_3]:
                                        if turret_selected:
                                            for b in buttons:
                                                if b.slot == 3:
                                                    if b.button_type == 'upgrade': # if its an upgrade button
                                                        if player.money >= b.upgrade_cost: # if we have enough money
                                                            turret_selected.upgrade(b.turret_type, player) # upgrade

                                    elif event.key in [pygame.K_4, pygame.K_s]:
                                        if not placing_tower:
                                            if turret_selected:
                                                turret_selected.sell(player)
                                                game_map.set_collision(turret_selected.rect.center, 'open') # open the tile
                                                turret_selected = None

                                ##### Clicking on stuff #####
                                elif event.type == pygame.MOUSEBUTTONDOWN: # all the mouse down events

                                    if event.button == 3: # right mouse button
                                        if placing_tower == True: # if we're placing a tower
                                            placing_tower = False # not anymore
                                            turretplacers.sprite.kill() # kill the placer
                                            for t in turret_range:
                                                t.kill() # destroy the turret_range
                                            HUDs.clear_info_menu()
                                                
                                        elif turret_selected: # if a turret is selected
                                            turret_selected = None
                                            HUDs.clear_info_menu() # clear all elements on the info menu
                                            for r in turret_range: # clear the tower range
                                                r.kill()
                                                
                                    elif event.button == 1: # left mouse button
                                        object_clicked = False
                                        click = pygame.mouse.get_pos() # gets position of mouse when clicked
                                        
                                        #####clicking to place a tower #####
                                        if placing_tower:
                                            for t in turretplacers:
                                                if not game_map.map_collision(t.rect): # if there is no collision with the map
                                                    if player.money >= t.get_cost():
                                                        game_map.set_collision(click, 'close') # block the tile
                                                        TurretSprites.Turret(click, t.turret_type, player) # create a turret on that tile
                                                    else:
                                                        info_bar.display_info('You dont have enough money!', 'message', True)

                                                else:
                                                    info_bar.display_info('You cannot place a tower there!', 'message', True)

                                            for b in buttons: # click on a in game menu button
                                                if b.rect.collidepoint(click): # if we click on a button
                                                    object_clicked = True
                                                    if b.button_type == 'cancel placement': # if its an upgrade button
                                                        placing_tower = False # not anymore
                                                        turretplacers.sprite.kill() # kill the placer
                                                        for t in turret_range:
                                                            t.kill() # destroy the turret_range
                                                        HUDs.clear_info_menu() # clear all elements on the info menu

                                        ##### sound on/off button #####             
                                        elif sound_toggle_button.rect.collidepoint(click):
                                            if music.sound_on:
                                                for c in music.channels:
                                                    c.set_volume(0.0)
                                                    music.sound_on = False
                                            else:
                                                for c in music.channels:
                                                    c.set_volume(1.0)
                                                    music.sound_on = True
                                            sound_toggle_button.change_setting(music.sound_on)
                                        ##### pause button #####
                                        elif pause_button.rect.collidepoint(click): # if you click on the pause button
                                            game_paused = True # pause
                                    
                                        ##### main menu button #####
                                        elif main_menu_button.rect.collidepoint(click): # if you click on the main menu button
                                            player.quiting = True
                                            

                                        ##### next wave button #####
                                        elif next_wave_button.rect.collidepoint(click): # if you click on the next wave button
                                            if wave.wave_done == True:
                                                wave.start_new_wave()
                                                for i in wave_info_group:
                                                    i.kill()
                                                HUDs.Wave_Info()
                                                if first_wave_started == False: # check so we only vanish once
                                                    first_wave_started = True
                                                    direction_arrow.vanish() # go away
                                                
                                                
                                        ##### build turret buttons #####
                                        elif build_turret_button.rect.collidepoint(click): # click on the turret
                                            turret_cost = turret_stats(build_turret_button.turret_type, 'cost') # get the cost
                                            if player.money >= turret_cost:
                                                HUDs.clear_info_menu() # clear all elements on the info menu
                                                for t in turret_range: # clear the tower range
                                                    t.kill()
                                                TurretSprites.TurretPlacer(click, build_turret_button.turret_type)
                                                placing_tower = True
                                                turret_radius = turret_stats(build_turret_button.turret_type, 'radius') # get the radius
                                                Tower_Range(click, turret_radius) # create a range
                                                HUDs.info_menu('turret placement', build_turret_button.turret_type)
                                            else:
                                                info_bar.display_info('You dont have enough money!', 'message', True)

                                        ##### check if groups were clicked #####
                                        else:

                                            ##### buttons group #####
                                            for b in buttons: # click on a in game menu button
                                                if b.rect.collidepoint(click): # if we click on a button
                                                    object_clicked = True
                                                    if b.button_type == 'upgrade': # if its an upgrade button
                                                        if player.money >= b.upgrade_cost: # if we have enough money
                                                            turret_selected.upgrade(b.turret_type, player) # upgrade

                                                        else:
                                                            info_bar.display_info('You dont have enough money!', 'message', True)

                                                            
                                                    if b.button_type == 'sell':
                                                        turret_selected.sell(player)
                                                        game_map.set_collision(turret_selected.rect.center, 'open') # open the tile
                                                        turret_selected = None
                                                    if b.button_type == 'info':
                                                        pass

                                            ##### turrets group #####
                                            for t in turrets:
                                                if t.rect.collidepoint(click): # when a turret is clicked on
                                                    object_clicked = True
                                                    turret_selected = t
                                                    HUDs.clear_info_menu() # clear all elements on the info menu
                                                    for r in turret_range: # clear the tower range
                                                        r.kill()
                                                    Tower_Range(t.rect.center, t.range) # create a tower range at the tower center and with tower range
                                                    HUDs.info_menu('turret', t.turret_type) # run the info menu for that tower

                                            if not object_clicked: # if we have not clicked on an object
                                                if turret_selected: # if a turret is selected
                                                    turret_selected = None
                                                    HUDs.clear_info_menu() # clear all elements on the info menu
                                                    for r in turret_range: # clear the tower range
                                                        r.kill()
                                                
                            ##### Mouse over #####
                            mouse = pygame.mouse.get_pos()
                            mouse_over_button = False
                            if len(buttons) > 0:
                                for b in buttons:
                                    if b.button_type == 'upgrade':
                                        if b.rect.collidepoint(mouse):
                                            buttons.get_sprite(0).update_info(b.button_info)
                                            mouse_over_button = True
                                            info_bar.display_info(b.button_info, 'upgrade info', False)

                            if mouse_over_button == False:
                                if build_turret_button.rect.collidepoint(mouse): # click on the turret
                                    mouse_over_button = True
                                    info_bar.display_info(build_turret_button.turret_type, 'upgrade info', False)
                                    
                            if mouse_over_button == False:
                                info_bar.fade_out()
                                if len(buttons) > 0:
                                    buttons.get_sprite(0).reset_info()
                                    

################################################################################
                            # done with user events #


                            ##### controls turret: range/targeting/shooting #####
                            #put inside a function eventually

                            enemies_by_dist_traveled = EnemySprites.sort_enemies_group(enemies)
                            
                            for t in turrets:
                                t.shooting_timer -= 1 # count down till next shot
                                if t.targeting_type != 'orbital':
                                    if not t.shoots_at_front: # if the tower doesnt shoot at the front of the line
                                        if len(enemies) > 0: # if there are enemies on the screen
                                            if t.current_target >= len(enemies): # if we are at the end of the enemies list
                                                t.current_target = 0 # rese5t the target that we are testing
                                                
                                            t.target = enemies.get_sprite(t.current_target) # pick which enemy we are testing
                                            if not enemies.has(t.target): # if the target is dead
                                                    t.current_target += 1 # pick a new target
                                                    
                                            else: # if the target lives
                                                # here we get distance from the tower to the target
                                                dist = (math.sqrt((t.target.rect.centerx-t.rect.centerx)**2+(t.target.rect.centery-t.rect.centery)**2))
                                                if dist > t.range: # if the target is not in range
                                                    t.current_target += 1 # test a new target
                                                    
                                                else: # if the target is in range
                                                    if t.shooting_timer <= 0: # if its time to shoot
                                                        t.shoot(t.target) # shoot at the target
                                                        t.shooting_timer = t.SHOOTING_TIMER # reset timer for next shot

                                    else: # if the tower shoots at the front of the line
                                        if len(enemies_by_dist_traveled) > 0: # if there are enemies on the screen
                                            print t.current_target
                                            if t.current_target < 0:
                                                t.current_target = (len(enemies_by_dist_traveled) -1)
                                            t.target = enemies_by_dist_traveled[t.current_target] # pick which enemy we are testing
            
                                            # here we get distance from the tower to the target
                                            dist = (math.sqrt((t.target.rect.centerx-t.rect.centerx)**2+(t.target.rect.centery-t.rect.centery)**2))
                                            if dist > t.range: # if the target is not in range
                                                t.current_target -= 1 # test a new target
                                                
                                            else: # if the target is in range
                                                if t.shooting_timer <= 0: # if its time to shoot
                                                    t.shoot(t.target) # shoot at the target
                                                    t.shooting_timer = t.SHOOTING_TIMER # reset timer for next shot

                                else: #controls orbital targeting
                                    t.update_shot_list()
                                    if len(t.shots) <= (t.bullet_limit - 1):
                                        if t.shooting_timer <= 0: # if its time to shoot
                                            t.shoot(t) # shoot at itself
                                            t.shooting_timer = t.SHOOTING_TIMER # reset timer for next shot
                            

                            ##### control the shots #####
                            for s in shots: # tell every shot which direction to shoot
                                s.get_direction(s.target, enemies, player)

                            
                            ##### creating a new wave #####
                            if wave.update(player): # run the wave update and if it returns true:
                                EnemySprites.Enemy(wave.wave_type, player) # create the enemy

                                    
                            ##### when we run out of life #####
                            if player.life <= 0:
                                player.game_over = True # think about it THINK REAL HARD.

                            ##### control game overs #####
                            if player.game_over:
                                if faded_in == True:
                                    info_bar.display_info('GAME OVER', 'message', True)
                                    if fading_cover.faded_out():
                                        faded_in = False
                                        # the game is now over
                                        music.channel_game.stop()
                                        music.play(music.channel_end, music.end_music, True)
                                        running = screengameover.run() # start the gameover menu
                                        music.stop(music.channel_end)
                                        
                                        running = False # does some wierd stuff
                                        quit_reason = 'map select'

                            if player.game_won:
                                if faded_in == True:
                                    if fading_cover.faded_out():
                                        faded_in = False
                                        game_over_timer = GAME_OVER_TIMER # reset the timer
                                        music.channel_game.stop()
                                        music.play(music.channel_end, music.end_music, True)

                                        #if we beat the game
                                        if len(player.open_maps) == (player.map + 1):
                                            screengamecomplete.run()
                                            running = False # does some wierd stuff
                                            reset(player) # reset all game elements
                                            quit_reason = 'main menu'
                                        else:
                                            player.open_new_map()
                                            save_game(player, player.save_file_number)
                                            screenmapcomplete.run() # start the gameover menu
                                            running = False # does some wierd stuff
                                            reset(player) # reset all game elements
                                            quit_reason = 'map select'
                                        music.stop(music.channel_end)
                                        music.play(music.channel_menu, music.menu_music, True)

                            if player.quiting:
                                if faded_in == True:
                                    if fading_cover.faded_out():
                                        faded_in = False
                                        music.channel_game.stop()
                                        running = False # quits the whole game and returns you to main menu.
                                        reset(player) # run the reset
                                        quit_reason = 'main menu'
################################################################################
                            if game_paused:
                                music.channel_game.pause()
                                music.play(music.channel_end, music.end_music, True)
                                running = screenpause.run() # runs pause menu
                                # if we quit during the pause screen
                                if not running:
                                    quit_reason = 'full quit'   
                                game_paused = False #hit return to game to end pause menu and go back to game
                                music.stop(music.channel_end)
                                music.channel_game.unpause()
                                
                            ##### update the sprites #####
                            all_update.update(player)
                            huds.update(player)

                            ##### draw everything #####
                            
                            if faded_in == False: # runs at the start of the game
                                if fading_cover.faded_in(): # fade in, if done
                                    faded_in = True
                            

                            
                            map_draw.draw(screen)
                            #map1.draw(screen) # DO WORK SON!

                            all_draw.draw(screen)
                            life_bars.draw(screen)
                            side_bar.draw()
                            screen.blit(in_game_menu.image, in_game_menu.rect.topleft) # post the in game menu bar onto the screen

                            if placing_tower: # here because it must be drawn on top of everything
                                turretplacers.sprite.move(pygame.mouse.get_pos()) # update the turret placer at the mouse location
                                for t in turret_range:
                                    t.move(pygame.mouse.get_pos())
                                    
                            huds.draw(screen)
                            
                            fading_covers.draw(screen)
                            
                            pygame.display.flip()

                        # restarting from certain parts/ full quitting

                        if quit_reason == 'main menu':
                            running_program = True
                            running_main_menu = True
                            running_save_file = False
                            running_map_select = False

                        elif quit_reason == 'full quit':
                            running_program = False
                            running_main_menu = False
                            running_save_file = False
                            running_map_select = False

                        elif quit_reason == 'map select':
                            running_program = True
                            running_main_menu = True
                            running_save_file = True
                            running_map_select = True

                            
                
# End main game loop
if __name__ == "__main__":
    ##### Testing #####
    import cProfile
    #cProfile.run('main()')
    
    main()
    pygame.quit()

