import pygame
from pygame.locals import *
import settings as st
import game_functions as gf
import game_objects as gobj
#import time
import game_control as gc
import pygameMap as gMap


def main():
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
        Everything.refresh_WeightedMap()
        Everything.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()