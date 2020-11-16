import pygame
import os
import sys
import settings as st
import json
from pygameMap import mapElement



def check_event(screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        else:
            pos = pygame.mouse.get_pos()




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

