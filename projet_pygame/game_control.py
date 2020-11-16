import pygame
import os
import game_functions as gf
import game_objects as gobj
import settings as st
from pygame.sprite import Group

def newGame():
    pass

def saveGameTo(file):
    pass

def loadGameFrom(file):
    pass

def purchase():
    pass

def beginGame(screen):
    autoSave = os.path.join('saves', 'autosave.txt')
    if os.path.exists(autoSave):
        file = open(autoSave,'r')
        loadGameFrom(file)
    else:
        newGame()

    Everything = gobj.Group_Everything()
    wizard = gobj.EntityOfPlayer(st.Profils.WIZARD, screen, (300, 300))
    enemy_1 = gobj.EntityOfComputer(st.Profils.ENEMY_1, screen, (screen.get_width()-100,10))
    Everything.add(wizard)
    Everything.add(enemy_1)

    allPlayers = pygame.sprite.Group((wizard,enemy_1))
    Everything.set_Group_Players(allPlayers)

    return Everything