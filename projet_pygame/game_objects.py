import pygame
import game_functions as gf
import settings as st
from pygame.sprite import Sprite
from pygame.sprite import Group
from pygame.sprite import LayeredUpdates


class Group_Everything(LayeredUpdates):
    def __init__(self):
        LayeredUpdates.__init__(self)
        self.Group_Players = None
        self.Group_Grids_move_area = None
        self.Group_Grids_attack_area = None
    
    def set_Group_Players(self, Group_Players):
        self.Group_Players = Group_Players

    def set_Group_Grids(self, Group_Grids, type):
        if type == 'move_area':
            self.Group_Grids_move_area = Group_Grids
        elif type == 'attack_area':
            self.Group_Grids_attack_area = Group_Grids




class Entity(Sprite):
    def __init__(self, profil, screen, pos=(0, 0)):
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
        self.move_distance = profil['Move_distance_default']
        self.attack_distance = profil['Attack_distance_default']
        self.selected = 0
        self.moved = 0
        self.finished = 0

    def set_pos(self,pos):
        interval = st.Game_Attr.INTERVAL.value
        Pos_x_grid = (pos[0]//interval)*interval
        Pos_y_grid = (pos[1]//interval)*interval
        self.rect.topleft = (Pos_x_grid,Pos_y_grid)
        self.pos = (Pos_x_grid,Pos_y_grid)

    def move(self,pos):
        self.set_pos(pos)
        self.moved = 1

    def attack(self,pos):
        print('attack the postion : (%d, %d)' %(pos[0],pos[1]))
        self.moved = 1
        self.finished = 1



class EntityOfPlayer(Entity):
    def __init__(self, profil, screen, pos=(0, 0)):
        Entity.__init__(self, profil, screen, pos)

    def update(self):
        #pos = pygame.mouse.get_pos()
        #self.rect.topleft = pos
        #self.rect.move_ip(0,0)
        #self.show_Pos_In_Grid()
        pass
        


class EntityOfComputer(Entity):
    def __init__(self, profil, screen, pos=(0, 0)):
        Entity.__init__(self, profil, screen, pos)

    def update(self):
        pass



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

