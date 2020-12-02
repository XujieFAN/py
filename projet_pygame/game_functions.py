import pygame
import os
import sys
import datetime, time
import settings as st
import json
import game_objects as gobj
import game_AI as AI
from pygameMap import mapElement
import roadSearch as rs
import numpy



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
                if event.key == pygame.K_r:
                    for player in Everything.Group_Players.sprites():
                        player.selected = 0
                        player.moved = 0
                        player.finished = 0
                if event.key == pygame.K_a:
                    Game_AI = AI.GameAI(Everything, screen)
                    Game_AI.do_AI_actions()
                    #Game_AI = None     #如何自我销毁？
                if event.key == pygame.K_t:
                    pass
                return



def mouse_click(button, screen, Everything):
    pos = pygame.mouse.get_pos()

    #click left
    if button == 1:
        if Everything.someone_selected == False:
            for player in Everything.Group_HumainPlayers.sprites():
                #   juste show area
                if player.rect.collidepoint(pos) and player.finished == 0:
                    show_area(Everything, player, screen)
                    player.selected = 1
                    Everything.set_someone_selected(True, player)
                    return

        if Everything.someone_selected == True:
            player = Everything.selected_one
            #   move !
            if player.moved == 0 and not player.rect.collidepoint(pos) and is_inArea(player, pos, player.move_distance) and not is_inArea(player, pos, player.attack_distance):
                obj_detected, obj_type = detectObj(Everything, pos)
                if obj_type == 0:   #nothing collided
                    player.smooth_move(pos)
                    show_area(Everything, player, screen)
                if obj_type == 1 and obj_detected in Everything.Group_HumainPlayers:    #detect a player
                    changeFocusedPlayer(Everything, player, obj_detected)
                    show_area(Everything, obj_detected, screen)
                return

            #   attack or move
            if not player.rect.collidepoint(pos) and is_inArea(player, pos, player.attack_distance):
                obj_detected, obj_type = detectObj(Everything, pos)
                if obj_type == 1:   #attack !
                    player.smooth_attack(obj_detected)
                if obj_type == 0 and player.moved == 0 and is_inArea(player, pos, player.move_distance):   #move
                    player.smooth_move(pos)
                    show_area(Everything, player, screen)
                return
            '''
            if not player.rect.collidepoint(pos) and is_inArea(player, pos, player.attack_distance) and is_inArea(player, pos, player.move_distance):
                obj_detected, obj_type = detectObj(Everything, pos)
                if obj_type == 1:   #attack !
                    player.smooth_attack(obj_detected)
                if obj_type == 0 and player.moved == 0:   #move
                    player.smooth_move(pos)
                    show_area(Everything, player, screen)
                return
            '''
            
            #   juste unshow
            if not player.rect.collidepoint(pos) and not is_inArea(player, pos, player.attack_distance):
                player.selected = 0
                Everything.set_someone_selected(False)
                unshow_area(Everything)
                return

    #click right
    if button == 3:
        show_info(screen, Everything, pos)
        return
    
    return



def changeFocusedPlayer(Everything, thisPlayer, anotherPlayer):
    Everything.set_someone_selected(False)
    thisPlayer.selected = 0
    Everything.set_someone_selected(True, anotherPlayer)
    anotherPlayer.selected = 1
    return


'''
detecteObj return 0 if detect nothing
detecteObj return 1 if detect a player
detecteObj return 2 if detect a map object
detecteObj return 3 if detect any other object
'''
def detectObj(Everything, pos):
    if Everything.Group_Players is not None:
        for another_player in Everything.Group_Players.sprites():
            if another_player.rect.collidepoint(pos):
                return another_player, 1

    '''
    if Everything.Group_map_objs is not None:
        for map_obj in Everything.Group_map_objs.sprites():
            if map_obj.rect.collidepoint(pos):
                return map_obj, 2
    '''
    if Everything.Group_for_infoPanel is not None:
        for SomeObj in Everything.Group_for_infoPanel.sprites():
            if SomeObj.rect.collidepoint(pos):
                return SomeObj, 3

    return None, 0



def show_info(screen, Everything, pos):
    
    print('-'*15+datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')+'-'*15)
    for obj in Everything.sprites():
        print('|  ', obj, 'at ', obj.rect.topleft)
    print('-'*50)
    print('\n')

    unshow_area(Everything)

    rowNumber = pos[1] // st.Game_Attr.INTERVAL.value
    colNumber = pos[0] // st.Game_Attr.INTERVAL.value
    print(Everything.weightedMap[rowNumber][colNumber])

    for player in Everything.Group_Players.sprites():
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

            bg_infoPanel = gobj.InfoPanelUnit(Everything,'bg_Panel', (0,0))
            Group_for_infoPanel.add(bg_infoPanel)
            Everything.add(bg_infoPanel,layer=10)

            test_button = gobj.InfoPanelUnit(Everything,'test', (25,25))
            Group_for_infoPanel.add(test_button)
            Everything.add(test_button,layer=11)

            Everything.Group_for_infoPanel = Group_for_infoPanel



def show_area(Everything, player, screen):
    unshow_area(Everything)
    if player.finished == 0:
        show_move_area(Everything, player, screen)
        show_attack_area(Everything, player, screen)



def getNodesInZone_forPos(Everything, pos, zone_scale, border):
    list_pos, nb_pos = calculate_area_from_distance(pos, zone_scale + border)
    list_nodes_InZone = []
    for node in list_pos:
        roadSearch_AStar = rs.roadSearch_AStar(Everything.weightedMap, rs.Node(pos), node)
        if roadSearch_AStar.searchRoad():
            if border == 0:   #All nodes in zone
                if len(roadSearch_AStar.pathList) <= zone_scale + 1:
                    list_nodes_InZone.append([node,roadSearch_AStar.pathList])
            else:   #only nodes in border
                if len(roadSearch_AStar.pathList) > zone_scale + 1 and len(roadSearch_AStar.pathList) <= zone_scale + border + 1:
                    list_nodes_InZone.append([node,roadSearch_AStar.pathList])
    return list_nodes_InZone



def show_move_area(Everything, player, screen):
    if player.moved == 0:
        list = getNodesInZone_forPos(Everything, player.pos, player.move_distance, 0)
        arrayList = numpy.array(list)
        player.zoneMovable = arrayList
        Group_grid_move_area = pygame.sprite.RenderPlain()
        for node in arrayList[:,0]:
            grid = gobj.GridUnit(screen,(0,255,0),node)
            Group_grid_move_area.add(grid)
            Everything.add(grid)
        Everything.set_Group_Grids(Group_grid_move_area,'move_area')
        pygame.sprite.groupcollide(Everything.Group_Grids_move_area, Everything.Group_Players, True, False)
        


def Is_enemyNearby(Everything, pos):
    pos_up = (pos[0], pos[1]-st.Game_Attr.INTERVAL.value)
    pos_down = (pos[0], pos[1]+st.Game_Attr.INTERVAL.value)
    pos_left = (pos[0]-st.Game_Attr.INTERVAL.value, pos[1])
    pos_right = (pos[0]+st.Game_Attr.INTERVAL.value, pos[1])
    for player in Everything.Group_Players.sprites():
        if player.attackable==1 and (player.rect.collidepoint(pos_up) or player.rect.collidepoint(pos_down) or player.rect.collidepoint(pos_left) or player.rect.collidepoint(pos_right)):
            return True
    return False



def get_listPosAttackable_atPos(Everything, pos, distance, flags=None):
    list_pos_a, nb_total_grid_a = calculate_area_from_distance(pos, distance)
    if flags is not None:
        if flags['nearby_on'] == 1:
            if Is_enemyNearby(Everything, pos):
                list_pos_a, nb_total_grid_a = calculate_area_from_distance(pos, 1)
    return list_pos_a



def show_attack_area(Everything, player, screen):
    '''version1 : 攻击范围大时处理得很慢，没有必要
    if player.moved == 0:
        list = getNodesInZone_forPos(Everything, player.pos, player.move_distance, player.attack_distance)
        arrayList = numpy.array(list)
    else:
        list = getNodesInZone_forPos(Everything, player.pos, player.attack_distance, 0)
        arrayList = numpy.array(list)
    Group_grid_attack_area = pygame.sprite.RenderPlain()
    for node in arrayList[:,0]:
        grid = gobj.GridUnit(screen,(255,0,0),node,0)
        Group_grid_attack_area.add(grid)
        Everything.add(grid)
    Everything.set_Group_Grids(Group_grid_attack_area,'attack_area')
    '''
    '''version2 : 无法根据战场情况判断攻击范围
    if player.moved == 0:
        list_pos_a, nb_total_grid_a = calculate_area_from_distance(player.pos, player.move_distance+player.attack_distance)
    else:
        list_pos_a, nb_total_grid_a = calculate_area_from_distance(player.pos, player.attack_distance)
    Group_grid_attack_area = pygame.sprite.RenderPlain()
    for i in range(nb_total_grid_a):
        grid = gobj.GridUnit(screen,(255,0,0),list_pos_a[i],0)
        Group_grid_attack_area.add(grid)
        Everything.add(grid)
    Everything.set_Group_Grids(Group_grid_attack_area,'attack_area')
    '''
    #version3 : 分别判断每一个可走到的点，再汇总
    AllAreaAttackable = set()
    if player.moved == 0: #and not Is_enemyNearby(Everything, player.pos):
        list = getNodesInZone_forPos(Everything, player.pos, player.move_distance, 0)
        arrayList = numpy.array(list)
        for node in arrayList[:,0]:
            areaAttackable = get_listPosAttackable_atPos(Everything, node, player.attack_distance, flags={'nearby_on':1})
            for pos in areaAttackable:
                AllAreaAttackable.add(pos)
    else:
        AllAreaAttackable = get_listPosAttackable_atPos(Everything, player.pos, player.attack_distance, flags={'nearby_on':1})
    Group_grid_attack_area = pygame.sprite.RenderPlain()
    for node in AllAreaAttackable:
        grid = gobj.GridUnit(screen,(255,0,0),node,0)
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