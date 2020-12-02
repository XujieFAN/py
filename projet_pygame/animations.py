import os
import pygame
import game_objects as gobj
import time



class Animation:
    def __init__(self, player, type):
        #self.player = player
        #self.image = player.image
        #self.rect = player.rect
        #self.type = type
        #self.character = player.profil['name']
        self.character = 'WIZARD'
        self.nb_frames = 3
        self.dir = os.path.join('images', 'animations', self.character)
        if type == 'move':
            self.images_move, self.image_rects_move = self.load_Animation_images('move',self.nb_frames)
        if type == 'attack':
            self.images_attack, self.image_rects_attack = self.load_Animation_images('attack',self.nb_frames)


    def load_Animation_images(self, type, nb_frames):
        images = []
        image_rects = []
        for i in range(nb_frames):
            fullname = os.path.join(self.dir, self.character+'_'+type+str(i+1)+'.png')
            try:
                image = pygame.image.load(fullname)
            except pygame.error as message:
                print('can not load this image:%s' %fullname)
                raise SystemExit(message)
            image = image.convert()
            images.append(image)
            image_rects.append(image.get_rect())
        return images, image_rects



if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((300,200), pygame.RESIZABLE)
    a = Animation('WIZARD')
    print(a.images_move)
    map = pygame.Surface((300,200)).convert()
    map.fill((255,255,255))
    screen.blit(map, (0,0))
    pygame.display.flip()
    time.sleep(0.5)
    screen.blit(a.images_move[0], (0,0))
    pygame.display.flip()
    time.sleep(0.2)
    screen.blit(a.images_move[1], (0,0))
    pygame.display.flip()
    time.sleep(0.2)
    screen.blit(a.images_move[2], (0,0))
    pygame.display.flip()