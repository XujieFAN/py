import pygame
import game_functions as gf
import settings as st
import sys
import time
from pygame.sprite import Sprite
from pygame.sprite import Group
from pygame.sprite import LayeredUpdates
import game_control as gc
import pygameMap as gMap
import game_AI as AI
import numpy
import animations as AM



class Everything(LayeredUpdates):
    def __init__(self, map):
        LayeredUpdates.__init__(self)
        self.Group_Players = None
        self.Group_HumainPlayers = None
        self.Group_ComputerPlayers = None
        self.Group_Grids_move_area = None
        self.Group_Grids_attack_area = None
        self.someone_selected = False
        self.selected_one = None
        self.Group_for_infoPanel = None
        self.AI_moving = 0
        map_width = map.get_width() // st.Game_Attr.INTERVAL.value
        map_heighth = map.get_height() // st.Game_Attr.INTERVAL.value
        weightedMap = numpy.ones((map_heighth,map_width))
        self.weightedMap = weightedMap
        self.map = map
    
    def set_Group_Players(self, Group_Players):
        self.Group_Players = Group_Players

    def set_Group_HumainPlayers(self, Group_HumainPlayers):
        self.Group_HumainPlayers = Group_HumainPlayers

    def set_Group_ComputerPlayers(self, Group_ComputerPlayers):
        self.Group_ComputerPlayers = Group_ComputerPlayers

    def set_Group_Grids(self, Group_Grids, type):
        if type == 'move_area':
            self.Group_Grids_move_area = Group_Grids
        elif type == 'attack_area':
            self.Group_Grids_attack_area = Group_Grids

    def set_someone_selected(self, boolean, selected_one=None):
        if boolean == True and selected_one == None:
            sys.quit(self)
        self.someone_selected = boolean
        self.selected_one = selected_one

    def refresh_WeightedMap(self):
        map_width = self.map.get_width() // st.Game_Attr.INTERVAL.value
        map_heighth = self.map.get_height() // st.Game_Attr.INTERVAL.value
        self.weightedMap = numpy.ones((map_heighth,map_width))

        for player in self.Group_Players:
            rowNumber = player.pos[1] // st.Game_Attr.INTERVAL.value
            colNumber = player.pos[0] // st.Game_Attr.INTERVAL.value
            self.weightedMap[rowNumber][colNumber] = 500

        '''
        for mapElement in self.Group_MapElements:
            rowNumber = mapElement.pos[1] // st.Game_Attr.INTERVAL.value
            colNumber = mapElement.pos[0] // st.Game_Attr.INTERVAL.value
            self.weightedMap[rowNumber][colNumber] = mapElement.weight
        '''



class Entity(Sprite):
    def __init__(self, Everything, profil, screen, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.profil = profil
        self.image, self.rect = gf.load_image(profil['image_name'])
        self.area = pygame.display.get_surface().get_rect()
        self.rect.topleft = pos
        interval = st.Game_Attr.INTERVAL.value
        Pos_x_grid = (pos[0]//interval)*interval
        Pos_y_grid = (pos[1]//interval)*interval
        self.rect.topleft = (Pos_x_grid,Pos_y_grid)
        self.pos = (Pos_x_grid,Pos_y_grid)
        self.screen = screen
        self.selected = 0
        self.moved = 0
        self.finished = 0
        self.Everything = Everything
        self.attackable = 0
        self.zoneMovable = None
        ###################################################
        self.attack_value = profil['attack_value']
        self.damage_value = profil['damage_value']
        self.defense_value = profil['defense_value']
        self.life_value = profil['life_value']
        self.exp_value = profil['exp_value']
        self.level = profil['level']
        self.move_distance = profil['Move_distance_default']
        self.attack_distance = profil['Attack_distance_default']
        self.abilites = profil['abilites']
        ###################################################

    def set_pos(self,pos):
        self.pos = gf.changePosToTopLeft(pos)
        self.rect.topleft = self.pos
        self.Everything.refresh_WeightedMap()

    def move(self,pos):
        self.set_pos(pos)
        self.moved = 1
        return

    def attack(self,target):
        print('Entity.attack')
        if target.attackable == 1:
            print('%s attack %s at the postion : (%d, %d)' %(self.profil['name'], target.profil['name'], target.pos[0],target.pos[1]))
            self.moved = 1
            self.finished = 1
            self.selected = 0
            self.Everything.set_someone_selected(False)
            gf.unshow_area(self.Everything)
        self.selected = 0

    def changeExpAndLevel(self, targets):
        return self.exp_value, self.level

    def showLifeValue(self):
        pygame.draw.rect(self.image,(0,0,0),(4,0,42,6),1)
        percentage_restLife = self.life_value/self.profil['life_value']
        if percentage_restLife >= 0.7:
            pygame.draw.rect(self.image,(255,255,255),(5,1,40,4))
            pygame.draw.rect(self.image,(0,255,0),(5,1,40*percentage_restLife,4))
        if percentage_restLife > 0.3 and percentage_restLife < 0.7:
            pygame.draw.rect(self.image,(255,255,255),(5,1,40,4))
            pygame.draw.rect(self.image,(205,205,0),(5,1,40*percentage_restLife,4))
        if percentage_restLife <= 0.3:
            pygame.draw.rect(self.image,(255,255,255),(5,1,40,4))
            pygame.draw.rect(self.image,(255,0,0),(5,1,40*percentage_restLife,4))
        
    def refresh_image(self):
        self.screen.blit(self.Everything.map, (0,0))
        self.Everything.Group_Players.draw(self.screen)
        pygame.display.flip()

    def update(self):
        self.showLifeValue()




class EntityOfPlayer(Entity):
    def __init__(self, Everything, profil, screen, pos=(0, 0)):
        Entity.__init__(self, Everything, profil, screen, pos)
        self.attackable = 0

    def update(self):
        Entity.update(self)

    def smooth_move(self,pos):
        index = list(self.zoneMovable[:,0]).index(gf.changePosToTopLeft(pos))
        path = list(self.zoneMovable[index,1])
        path.pop()
        path.reverse()
        #增加一个行走方向的判断，以此决定加载那个图片
        am_move = AM.Animation(self,'move')
        images_am_move = am_move.images_move
        nb_frames = am_move.nb_frames
        for step in path:
            current_pos = self.pos
            for i in range(nb_frames):
                next_tmp_pos_x = current_pos[0] + (((step.pos[0] - current_pos[0]) // nb_frames) * (i+1))
                next_tmp_pos_y = current_pos[1] + (((step.pos[1] - current_pos[1]) // nb_frames) * (i+1))
                self.rect.topleft = (next_tmp_pos_x,next_tmp_pos_y)
                self.image = images_am_move[i]
                self.pos = (next_tmp_pos_x,next_tmp_pos_y)
                self.refresh_image()
                time.sleep(0.1)
                current_pos = self.pos
        self.pos = gf.changePosToTopLeft(self.rect.center)
        self.rect.topleft = self.pos
        self.moved = 1
        self.Everything.refresh_WeightedMap()
        return

    def smooth_attack(self,target):
        print('EntityOfPlayer.smooth_attack')
        if target.attackable == 1:
            #增加一个攻击方向的判断，以此决定加载那个图片
            am_attack = AM.Animation(self,'attack')
            images_am_attack = am_attack.images_attack
            nb_frames = am_attack.nb_frames
            for i in range(nb_frames):
                self.image = images_am_attack[i]
                self.refresh_image()
                time.sleep(0.2)
            self.image, self.rect = gf.load_image(self.profil['image_name'])
            self.rect.topleft = self.pos
            target.life_value = target.life_value - self.attack_value - self.damage_value
            self.exp_value, self.level = Entity.changeExpAndLevel(self,[target])
            Entity.attack(self,target)
            if target.life_value <= 0:
                target.playerDie()

    def playerDie(self):
        self.Everything.Group_HumainPlayers.remove(self)
        self.Everything.Group_Players.remove(self)
        self.Everything.remove(self)



class WIZARD(EntityOfPlayer):
    def __init__(self, Everything, profil, screen, pos=(0, 0)):
        EntityOfPlayer.__init__(self, Everything, profil, screen, pos)

    def smooth_attack(self,target):
        print('WIZARD.smooth_attack')
        EntityOfPlayer.smooth_attack(self,target)
        fire = FireObject('wizard_fire1.png',self.Everything,self.screen,self.rect.center)
        fire.moveAtoB(self.rect.center,target.rect.center,3)



class KNIGHT(EntityOfPlayer):
    def __init__(self, Everything, profil, screen, pos=(0, 0)):
        EntityOfPlayer.__init__(self, Everything, profil, screen, pos)



class EntityOfComputer(Entity):
    def __init__(self, Everything, profil, screen, pos=(0, 0)):
        Entity.__init__(self, Everything, profil, screen, pos)
        self.attackable = 1

    def update(self):
        Entity.update(self)

    def move_one_step(self,pos):
        self.set_pos(pos)
        #self.moved = 1
        time.sleep(0.2)

    def attack(self,target):
        target.life_value = target.life_value - self.attack_value - self.damage_value
        print(target.life_value, target.life_value - self.attack_value - self.damage_value)
        Entity.attack(self,target)
        if target.life_value <= 0:
            target.playerDie()

    def playerDie(self):
        self.Everything.Group_ComputerPlayers.remove(self)
        self.Everything.Group_Players.remove(self)
        self.Everything.remove(self)



class FireObject(Sprite):
    def __init__(self, imageName, Everything, screen, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = gf.load_image(imageName)
        self.Everything = Everything
        self.screen = screen
        self.pos = pos

    def moveAtoB(self, posA, posB, nb_frames_per_Grid):
        offset_x = abs(posA[0]-posB[0])
        offset_y = abs(posA[1]-posB[1])
        print(offset_x,offset_y)
        nb_frames = int((numpy.sqrt(numpy.square(offset_x) + numpy.square(offset_y))//st.Game_Attr.INTERVAL.value) * nb_frames_per_Grid)
        print('nb_frames',nb_frames)
        current_pos = posA
        print(current_pos)
        for i in range(nb_frames):
            next_tmp_pos_x = current_pos[0] + (((posB[0] - current_pos[0]) // nb_frames) * (i+1))
            next_tmp_pos_y = current_pos[1] + (((posB[1] - current_pos[1]) // nb_frames) * (i+1))
            print(next_tmp_pos_x, next_tmp_pos_y)
            self.screen.blit(self.image, (next_tmp_pos_x, next_tmp_pos_y))
            pygame.display.flip()
            time.sleep(0.05)
            current_pos = (next_tmp_pos_x, next_tmp_pos_y)
            self.screen.blit(self.Everything.map, current_pos, [next_tmp_pos_x, next_tmp_pos_y, 25, 13])
            self.Everything.draw(self.screen)



class GridUnit(Sprite):
    def __init__(self, screen, rgb=(255,255,255), pos=(0, 0), flag_fill=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((st.Game_Attr.INTERVAL.value, st.Game_Attr.INTERVAL.value),pygame.RLEACCEL)
        self.rgb = rgb
        self.rect = self.image.get_rect()
        if flag_fill == 1:
            self.image.fill(rgb)
            self.image.set_alpha(30)    
        else:
            self.image.fill((255,255,255))
            pygame.draw.rect(self.image,self.rgb,(1,1,48,48),1)
            self.image.set_alpha(100)
        self.rect.topleft = pos
        self.screen = screen
        self.offset = 0

    def set_offset(self,nb):
        self.offset = nb

    def update(self):
        pass



class InfoPanelUnit(Sprite):
    def __init__(self, Everything, type, pos):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.Everything = Everything
        if type == 'bg_Panel':
            bg_infoPanel_image = pygame.Surface((100,pygame.display.get_surface().get_height())).convert()
            bg_infoPanel_image.fill((100,100,200))
            bg_infoPanel_rect = bg_infoPanel_image.get_rect()
            bg_infoPanel_rect.topleft = pos
            self.image = bg_infoPanel_image
            self.rect = bg_infoPanel_rect
        else:
            unit_image = pygame.Surface((50,50)).convert()
            unit_image.fill((0,0,0))
            unit_rect = unit_image.get_rect()
            unit_rect.topleft = pos
            self.image = unit_image
            self.rect = unit_rect

    def update(self):
        pass


if __name__ == "__main__":
    pass