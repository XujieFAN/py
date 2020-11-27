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



class Group_Everything(LayeredUpdates):
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
        self.weightedMap = None
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
        self.Group_Everything = Everything
        self.attackable = 0
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

    def move(self,pos):
        self.set_pos(pos)
        self.moved = 1
        return

    def attack(self,target):
        if target.attackable == 1:
            print('%s attack %s at the postion : (%d, %d)' %(self.profil['name'], target.profil['name'], target.pos[0],target.pos[1]))
            self.moved = 1
            self.finished = 1
            self.selected = 0
            self.Group_Everything.set_someone_selected(False)
            gf.unshow_area(self.Group_Everything)
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
            pygame.draw.rect(self.image,(200,200,0),(5,1,40*percentage_restLife,4))
        if percentage_restLife <= 0.3:
            pygame.draw.rect(self.image,(255,255,255),(5,1,40,4))
            pygame.draw.rect(self.image,(255,0,0),(5,1,40*percentage_restLife,4))
        

    def update(self):
        self.showLifeValue()




class EntityOfPlayer(Entity):
    def __init__(self, Everything, profil, screen, pos=(0, 0)):
        Entity.__init__(self, Everything, profil, screen, pos)
        self.attackable = 0

    def update(self):
        Entity.update(self)

    def attack(self,target):
        target.life_value = target.life_value - self.attack_value - self.damage_value
        print(target.life_value, target.life_value - self.attack_value - self.damage_value)
        self.exp_value, self.level = Entity.changeExpAndLevel(self,[target])
        Entity.attack(self,target)
        if target.life_value <= 0:
            target.playerDie()

    def playerDie(self):
        self.Group_Everything.Group_HumainPlayers.remove(self)
        self.Group_Everything.Group_Players.remove(self)
        self.Group_Everything.remove(self)
        


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
        self.Group_Everything.Group_ComputerPlayers.remove(self)
        self.Group_Everything.Group_Players.remove(self)
        self.Group_Everything.remove(self)



class GridUnit(Sprite):
    def __init__(self, screen, rgb=(255,255,255), pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((st.Game_Attr.INTERVAL.value, st.Game_Attr.INTERVAL.value),pygame.RLEACCEL)
        self.image.set_alpha(20)
        self.image.fill(rgb)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.rgb = rgb
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
        self.Group_Everything = Everything
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
    pygame.init()

    screen_setting = st.Settings()
    screen = pygame.display.set_mode((screen_setting.screen_width, screen_setting.screen_height), pygame.RESIZABLE)
    pygame.display.set_caption(screen_setting.caption)
    
    screen, map = gMap.load_map_to_screen('map_2.png')

    Everything = gc.beginGame(screen, map)

    #gf.load_bg_sound('AITheme0.mp3')

    while True:
        gf.check_event(screen, Everything)
        
        
        screen.blit(map, (0,0))
        Everything.update()
        player = Everything.Group_HumainPlayers.sprites()[0]
        player.showLifeValue()
        screen.blit(player.image, (0,0))

        pygame.display.flip()