import pygame
import os
import sys
import datetime, time
import settings as st
import json
import game_objects as gobj
import game_AI as AI
from pygameMap import mapElement



def check_event(screen, Everything):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if Everything.AI_moving == 0:
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_click(event.button, screen, Everything)
                return
            if event.type == pygame.KEYUP:
                if pygame.key.key_code("r") == pygame.K_r:
                    for player in Everything.Group_Players.sprites():
                        player.selected = 0
                        player.moved = 0
                        player.finished = 0
                if pygame.key.key_code("a") == pygame.K_a:
                    Game_AI = AI.GameAI(Everything, screen)
                    Game_AI.do_AI_actions()
                    #Game_AI = None     #如何自我销毁？
                return



def mouse_click(button, screen, Group_Everything):
    pos = pygame.mouse.get_pos()

    #click left
    if button == 1:
        if Group_Everything.someone_selected == False:
            for player in Group_Everything.Group_Players.sprites():
                #   juste show area
                if player.rect.collidepoint(pos) and player.finished == 0:
                    show_area(Group_Everything, player, screen)
                    player.selected = 1
                    Group_Everything.set_someone_selected(True, player)
                    return

        if Group_Everything.someone_selected == True:
            player = Group_Everything.selected_one
            #   move !
            if player.moved == 0 and not player.rect.collidepoint(pos) and is_inArea(player, pos, player.move_distance) and not is_inArea(player, pos, player.attack_distance):
                obj_detected, obj_type = detectObj(Group_Everything, pos)
                if obj_type == 0:   #nothing collided
                    player.move(pos)
                    show_area(Group_Everything, player, screen)
                if obj_type == 1:    #detect a player
                    changeFocusedPlayer(Group_Everything, player, obj_detected)
                    show_area(Group_Everything, obj_detected, screen)
                return

            #   attack or move
            if not player.rect.collidepoint(pos) and is_inArea(player, pos, player.attack_distance) and is_inArea(player, pos, player.move_distance):
                obj_detected, obj_type = detectObj(Group_Everything, pos)
                if obj_type == 1:   #attack !
                    player.attack(obj_detected)
                if obj_type == 0 and player.moved == 0:   #move
                    player.move(pos)
                    show_area(Group_Everything, player, screen)
                return
            
            #   juste unshow
            if not player.rect.collidepoint(pos) and not is_inArea(player, pos, player.attack_distance):
                player.selected = 0
                Group_Everything.set_someone_selected(False)
                unshow_area(Group_Everything)
                return

    #click right
    if button == 3:
        show_info(screen, Group_Everything, pos)
        return
    
    return



def changeFocusedPlayer(Group_Everything, thisPlayer, anotherPlayer):
    Group_Everything.set_someone_selected(False)
    thisPlayer.selected = 0
    Group_Everything.set_someone_selected(True, anotherPlayer)
    anotherPlayer.selected = 1
    return


'''
detecteObj return 0 if detect nothing
detecteObj return 1 if detect a player
detecteObj return 2 if detect a map object
detecteObj return 3 if detect any other object
'''
def detectObj(Group_Everything, pos):
    if Group_Everything.Group_Players is not None:
        for another_player in Group_Everything.Group_Players.sprites():
            if another_player.rect.collidepoint(pos):
                return another_player, 1

    '''
    if Group_Everything.Group_map_objs is not None:
        for map_obj in Group_Everything.Group_map_objs.sprites():
            if map_obj.rect.collidepoint(pos):
                return map_obj, 2
    '''
    if Group_Everything.Group_for_infoPanel is not None:
        for SomeObj in Group_Everything.Group_for_infoPanel.sprites():
            if SomeObj.rect.collidepoint(pos):
                return SomeObj, 3

    return None, 0



def show_info(screen, Group_Everything, pos):
    
    print('-'*15+datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')+'-'*15)
    for obj in Group_Everything.sprites():
        print('|  ', obj, 'at ', obj.rect.topleft)
    print('-'*50)
    print('\n')

    unshow_area(Group_Everything)

    for player in Group_Everything.Group_Players.sprites():
        if player.rect.collidepoint(pos):
            print('-'*50)
            print('|  player profil   : %s' %player.profil['name'])
            print('|  player life     : %s' %player.life_value)
            print('|  attackable      : %s' %player.attackable)
            print('|  player selected : %s' %player.selected)
            print('|  player moved    : %s' %player.moved)
            print('|  player finished : %s' %player.finished)
            print('-'*50)
            
            Group_for_infoPanel = pygame.sprite.Group()

            bg_infoPanel = gobj.InfoPanelUnit(Group_Everything,'bg_Panel', (0,0))
            Group_for_infoPanel.add(bg_infoPanel)
            Group_Everything.add(bg_infoPanel,layer=10)

            test_button = gobj.InfoPanelUnit(Group_Everything,'test', (25,25))
            Group_for_infoPanel.add(test_button)
            Group_Everything.add(test_button,layer=11)

            Group_Everything.Group_for_infoPanel = Group_for_infoPanel



def show_area(Everything, player, screen):
    unshow_area(Everything)
    if player.finished == 0:
        show_move_area(Everything, player, screen)
        show_attack_area(Everything, player, screen)



def show_move_area(Everything, player, screen):
    if player.moved == 0:
        list_pos_m, nb_total_grid_m = calculate_area_from_distance(player.pos, player.move_distance)
        Group_grid_move_area = pygame.sprite.RenderPlain()
        for i in range(nb_total_grid_m):
            grid = gobj.GridUnit(screen,(0,255,0),list_pos_m[i])
            Group_grid_move_area.add(grid)
            Everything.add(grid)
            Everything.set_Group_Grids(Group_grid_move_area,'move_area')
        pygame.sprite.groupcollide(Everything.Group_Grids_move_area, Everything.Group_Players, True, False)
        


def show_attack_area(Everything, player, screen):
    if player.moved == 0:
        list_pos_a, nb_total_grid_a = calculate_area_from_distance(player.pos, player.move_distance+player.attack_distance)
    else:
        list_pos_a, nb_total_grid_a = calculate_area_from_distance(player.pos, player.attack_distance)

    Group_grid_attack_area = pygame.sprite.RenderPlain()
    for i in range(nb_total_grid_a):
        grid = gobj.GridUnit(screen,(255,0,0),list_pos_a[i])
        Group_grid_attack_area.add(grid)
        Everything.add(grid)
        Everything.set_Group_Grids(Group_grid_attack_area,'attack_area')



def unshow_area(Everything):
    if Everything.Group_Grids_move_area != None:
        Everything.remove(Everything.Group_Grids_move_area.sprites())
    if Everything.Group_Grids_attack_area != None:
        Everything.remove(Everything.Group_Grids_attack_area.sprites())
    if Everything.Group_for_infoPanel != None:
        Everything.remove(Everything.Group_for_infoPanel.sprites())



def calculate_area_from_distance(pos, distance, interval=st.Game_Attr.INTERVAL.value):
    list_pos = []
    
    pos_init_up = (pos[0],pos[1]-distance*interval)
    for i in range(distance):
        for j in range(-i,i+1):
            pt = (pos_init_up[0]+j*interval, pos_init_up[1]+i*interval)
            list_pos.append(pt)

    for j in range(-distance,distance+1):
        pt = (pos[0]+j*interval, pos[1])
        if pt != pos:
            list_pos.append(pt)

    pos_init_down = (pos[0],pos[1]+distance*interval)
    for i in range(distance):
        for j in range(-i,i+1):
            pt = (pos_init_down[0]+j*interval, pos_init_down[1]-i*interval)
            list_pos.append(pt)
    
    return list_pos, len(list_pos)



def changePosToTopLeft(pos):
    interval = st.Game_Attr.INTERVAL.value
    Pos_x_grid = (pos[0]//interval)*interval
    Pos_y_grid = (pos[1]//interval)*interval
    pos = (Pos_x_grid,Pos_y_grid)
    return pos



def is_inArea(player, pos, distance):
    interval = st.Game_Attr.INTERVAL.value
    pos = changePosToTopLeft(pos)

    offset_x = abs(pos[0] - player.pos[0]) // interval
    offset_y = abs(pos[1] - player.pos[1]) // interval
    if offset_x + offset_y <= distance:
        return True
    else:
        return False



def load_bg_sound(name):
    if not pygame.mixer:
        return

    fullname = os.path.join('sounds', name)

    try:
        pygame.mixer.music.load(fullname)
        pygame.mixer.music.play(-1)
    except pygame.error as message:
        print('can not load sound:%s' %fullname)
        raise SystemExit(message)



def load_action_sound(name):
    if not pygame.mixer:
        return

    fullname = os.path.join('sounds', name)

    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('can not load sound:%s' %fullname)
        raise SystemExit(message)

    return sound



def load_image(name, colorKey=None):
    fullname = os.path.join('images', name)

    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('can not load this image:%s' %fullname)
        raise SystemExit(message)

    image = image.convert()

    if colorKey is not None:
        image.set_colorkey(colorKey, pygame.RLEACCEL)

    return image, image.get_rect()



if __name__ == "__main__":
    pass