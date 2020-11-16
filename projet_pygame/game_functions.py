import pygame
import os
import sys
import settings as st
import json
import game_objects as gobj
from pygameMap import mapElement



def check_event(screen, Everything):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_click(screen, Everything)
        elif event.type == pygame.KEYUP:
            if pygame.key.key_code("r") == pygame.K_r:
                for player in Everything.Group_Players.sprites():
                    player.selected = 0
                    player.moved = 0
                    player.finished = 0



def mouse_click(screen, Group_Everything):
    pos = pygame.mouse.get_pos()
    for player in Group_Everything.Group_Players.sprites():
        print('selected:%d,  moved:%d, finished:%d' %(player.selected, player.moved, player.finished))
        if player.rect.collidepoint(pos) and player.finished == 0 and player.selected == 0:
            if player.finished == 0:
                player.set_pos(pos)
                show_area(Group_Everything, player, screen)
                player.selected = 1
                return
        elif player.rect.collidepoint(pos) and player.selected == 1: 
            return
        elif player.selected == 1 and not player.rect.collidepoint(pos) and is_inArea(player, pos, 'move_area') and not is_inArea(player, pos, 'attack_area'):
            unshow_area(Group_Everything)
            player.move(pos)
            show_area(Group_Everything, player, screen)
            return
        elif player.selected == 1 and not player.rect.collidepoint(pos) and is_inArea(player, pos, 'attack_area'):
            player.attack(pos)
            player.selected = 0
            unshow_area(Group_Everything)
            return
        else:
            #player.selected = 0
            unshow_area(Group_Everything)
            #player.finished = 0
            return


def show_area(Everything, player, screen):
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


def is_inArea(player, pos, type):
    interval = st.Game_Attr.INTERVAL.value
    offset_x = abs(pos[0] - player.pos[0]) // interval
    offset_y = abs(pos[1] - player.pos[1]) // interval
    if type == 'move_area':
        if offset_x + offset_y <= player.move_distance:
            return True
        else:
            return False

    if type == 'attack_area':
        if offset_x + offset_y <= player.attack_distance:
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
    print(-130//50)
    print(30//50)
    print(-30//50)
