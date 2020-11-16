from enum import Enum



class Settings():
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.caption = 'Warlord'



class Profils():
    WIZARD = {'OrderID':1, 'Move_distance_default':3, 'Attack_distance_default':2, 'image_name':'WIZARD.png'}
    WARRIOR = {'OrderID':2, 'Move_distance_default':3, 'Attack_distance_default':1, 'image_name':'WARRIOR.png'}
    KNIGHT = {'OrderID':3, 'Move_distance_default':4, 'Attack_distance_default':1, 'image_name':'KNIGHT.png'}
    ARCHER = {'OrderID':4, 'Move_distance_default':3, 'Attack_distance_default':3, 'image_name':'ARCHER.png'}
    ARTILLERY = {'OrderID':5, 'Move_distance_default':2, 'Attack_distance_default':4, 'image_name':'ARTILLERY.png'}

    ENEMY_1 = {'OrderID':51, 'Move_distance_default':3, 'Attack_distance_default':1, 'image_name':'ENEMY_1.png'}
    ENEMY_2 = {'OrderID':52, 'Move_distance_default':3, 'Attack_distance_default':2, 'image_name':'ENEMY_2.png'}

    List = [WIZARD,WARRIOR,KNIGHT,ARCHER,ARTILLERY,ENEMY_1,ENEMY_2]



class Map_Elements():
    LAWN = 'lawn'
    MOUNTAIN = 'mountain'



class Game_Attr(Enum):
    INTERVAL = 50