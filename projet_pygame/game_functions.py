import pygame
import os
import sys
import settings as st
import json
from pygameMap import mapElement



def check_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)



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



def load_map_to_screen(name):
    '''
    There are 2 files for a map : a .png file for background picture, a .json file for objects on map
    '''
    fullname = os.path.join('maps', name)
    fullname_json = os.path.join('maps',name.split('.')[0]+'.json')

    list_mapElements = []
    mapElementsGroup = pygame.sprite.RenderPlain()

    try:
        map = pygame.image.load(fullname)
        f = open(fullname_json, 'r')
        list_mapElements = json.load(f)
        f.close()
    except pygame.error as message:
        print('can not load this map:%s' %fullname)
        raise SystemExit(message)

    map = map.convert()

    for element in list_mapElements:
        spr = mapElement(element[0],(element[1][0],element[1][1]))
        mapElementsGroup.add(spr)
    
    mapElementsGroup.draw(map)

    map_width = map.get_width()
    map_height = map.get_height()
    pygame.display.set_caption(name)
    screen = pygame.display.set_mode((map_width,map_height), pygame.RESIZABLE)
    screen.blit(map,(0,0))

    return screen, map
