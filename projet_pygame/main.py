import pygame
from pygame.locals import *
import settings as st
import game_functions as gf
import game_objects as gobj
import time
import game_control as gc
import pygameMap as gMap



def main():
    pygame.init()

    screen_setting = st.Settings()
    screen = pygame.display.set_mode((screen_setting.screen_width, screen_setting.screen_height), pygame.RESIZABLE)
    pygame.display.set_caption(screen_setting.caption)
    
    gc.beginGame()

    background = pygame.Surface(screen.get_size()).convert()
    background.fill((250,250,250))
    screen.blit(background,(0,0))

    time.sleep(3)

    screen, map = gMap.load_map_to_screen('map_1.png')

    gf.load_bg_sound('AITheme0.mp3')


    soldier_1 = gobj.Soldier(st.Profils.WIZARD, screen, (10, 10))
    enemy_1 = gobj.Enemy(st.Profils.ENEMY_1, screen, (screen.get_width()-100,10))
    allprofils = pygame.sprite.RenderPlain((soldier_1,enemy_1))

    while True:
        gf.check_event()
        
        allprofils.update()
        screen.blit(map, (0,0))
        allprofils.draw(screen)

        pygame.display.flip()



if __name__ == "__main__":
    main()