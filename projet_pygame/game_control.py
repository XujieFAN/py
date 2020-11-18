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
    wizard = gobj.EntityOfPlayer(Everything, st.Profils.WIZARD, screen, (300, 300))
    knight = gobj.EntityOfPlayer(Everything, st.Profils.KNIGHT, screen, (300, 400))
    enemy_1 = gobj.EntityOfComputer(Everything, st.Profils.ENEMY_1, screen, (screen.get_width()-200,50))
    enemy_2 = gobj.EntityOfComputer(Everything, st.Profils.ENEMY_2, screen, (screen.get_width()-200,100))
    Everything.add(wizard)
    Everything.add(knight)
    Everything.add(enemy_1)
    Everything.add(enemy_2)

    allPlayers = pygame.sprite.Group((wizard,knight,enemy_1,enemy_2))
    Everything.set_Group_Players(allPlayers)

    return Everything