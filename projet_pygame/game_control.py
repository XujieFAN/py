import pygame
import os
import game_functions as gf

def newGame():
    pass

def saveGameTo(file):
    pass

def loadGameFrom(file):
    pass

def purchase():
    pass

def beginGame():
    autoSave = os.path.join('saves', 'autosave.txt')
    if os.path.exists(autoSave):
        file = open(autoSave,'r')
        loadGameFrom(file)
    else:
        newGame()
