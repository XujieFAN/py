import pygame
import game_functions as gf
import settings as St

class Entity(pygame.sprite.Sprite):
    def __init__(self, profil, screen, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.profil = profil
        self.image, self.rect = gf.load_image(profil['image_name'])
        self.area = pygame.display.get_surface().get_rect()
        self.rect.topleft = pos
        self.screen = screen
        self.move_distance = profil['Move_distance_default']
        self.attack_distance = profil['Attack_distance_default']
        self.selected = 0

    def show_Pos_In_Grid(self,interval=St.Game_Attr.INTERVAL.value):
        realPos = self.rect.topleft
        Pos_x_grid = (realPos[0]//interval)*interval
        Pos_y_grid = (realPos[1]//interval)*interval
        self.rect.topleft = (Pos_x_grid,Pos_y_grid)

    def show_reachable_area(self,interval=St.Game_Attr.INTERVAL.value):
        
        self.screen.blit(self.grid,self.rect.center)

    def show_attackable_area(self,interval=St.Game_Attr.INTERVAL.value):
        pass



class Soldier(Entity):
    def __init__(self, profil, screen, pos=(0, 0)):
        Entity.__init__(self, profil, screen, pos)

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.topleft = pos
        self.rect.move_ip(0,0)
        self.show_Pos_In_Grid()
        


class Enemy(pygame.sprite.Sprite):
    def __init__(self, profil, screen, pos=(0, 0)):
        Entity.__init__(self, profil, screen, pos)

    def update(self):
        pass



class GridUnit(pygame.sprite.Sprite):
    def __init__(self, for_Who, screen, rgb=(255,255,255), pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((St.Game_Attr.INTERVAL.value, St.Game_Attr.INTERVAL.value),pygame.RLEACCEL)
        self.image.set_alpha(100)
        self.image.fill(rgb)
        self.rect = self.image.get_rect()
        self.rgb = rgb
        self.screen = screen
        self.for_Who = for_Who