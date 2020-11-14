import pygame
import game_functions as gf

class Soldier(pygame.sprite.Sprite):
    def __init__(self, profil, screen, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.profil = profil
        self.image, self.rect = gf.load_image(profil['image_name'])
        self.area = pygame.display.get_surface().get_rect()
        self.rect.topleft = pos
        self.screen = screen
        self.move_distance = profil['Move_distance_default']
        self.attack_distance = profil['Attack_distance_default']

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        self.rect.move_ip(5,10)



class Enemy(pygame.sprite.Sprite):
    def __init__(self, profil, screen, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.profil = profil
        self.image,self.rect = gf.load_image(profil['image_name'])
        self.area = pygame.display.get_surface().get_rect()
        self.rect.topleft = pos
        self.screen = screen
        self.move_distance = profil['Move_distance_default']
        self.attack_distance = profil['Attack_distance_default']

    def update(self):
        pass
