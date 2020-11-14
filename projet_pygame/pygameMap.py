import pygame
import game_functions as gf
import json
import os
from settings import Map_Elements



class mapElement(pygame.sprite.Sprite):
    def __init__(self,elementName,pos=(0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.elementName = elementName
        self.image_name = elementName+'.png'
        self.image, self.rect = gf.load_image(self.image_name)
        self.rect.topleft = pos

        if elementName == Map_Elements.LAWN:
            self.reachable = 1
            self.attackable = 1
            self.crossable = 1
        
        if elementName == Map_Elements.MOUNTAIN:
            self.reachable = 0
            self.attackable = 0
            self.crossable = 0

    def get_pos(self):
        return self.rect.topleft

    def addToList(self, list):
        pos = [self.rect.topleft[0], self.rect.topleft[1]]
        list.append([self.elementName,pos])



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



def save_map(name,list,size=(800,600),rgb=(255,255,255)):
    fullname = os.path.join('maps', name)
    mapEleFileName = os.path.join('maps',name.split('.')[0]+'.json')

    mapElementsGroup = pygame.sprite.RenderPlain()

    map = pygame.Surface(size).convert()
    map.fill(rgb)

    try:
        for element in list:
            spr = mapElement(element[0],(element[1][0],element[1][1]))
            mapElementsGroup.add(spr)

        mapElementsGroup.draw(map)

        mapEleFile = open(mapEleFileName,'w')
        json.dump(list,mapEleFile)
        mapEleFile.close()

        pygame.image.save(map,fullname)
    except pygame.error as message:
        print('can not save this map:%s' %fullname)
        raise SystemExit(message)
    except:
        print('Other Error : can not save this map:%s' %fullname)



def show_format():
    List_format = 'The List format for map elements is:\n[\n\t[ "obj_name", [x, y] ],\n]'
    print(List_format)



if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800,600), pygame.RESIZABLE)
    list = [
        ["lawn",[0,0]],
        ["lawn",[100,50]],
        ["lawn",[200,100]],
        ["mountain",[300,100]],
        ["mountain",[400,100]]
    ]
    save_map('map_2.png',list)
    screen, map = load_map_to_screen('map_2.png')
    screen.blit(map,(0,0))
    show_format()
    
    while True:
        gf.check_event()
        screen.blit(map,(0,0))
        pygame.display.flip()