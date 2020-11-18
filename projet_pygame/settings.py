from enum import Enum



class Settings():
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.caption = 'Warlord'



class Profils():
    WIZARD = {'OrderID':1, 'name':'WIZARD', 'Move_distance_default':3, 'Attack_distance_default':2, 'image_name':'WIZARD.png',
                'attack_value':10, 'damage_value':0, 'defense_value':1, 'life_value':20, 'exp_value':0, 'level':1, 'abilites':['attack',]}

    WARRIOR = {'OrderID':2, 'name':'WARRIOR', 'Move_distance_default':3, 'Attack_distance_default':1, 'image_name':'WARRIOR.png',
                'attack_value':15, 'damage_value':0, 'defense_value':15, 'life_value':50, 'exp_value':0, 'level':1, 'abilites':['attack',]}

    KNIGHT = {'OrderID':3, 'name':'KNIGHT', 'Move_distance_default':4, 'Attack_distance_default':1, 'image_name':'KNIGHT.png',
                'attack_value':15, 'damage_value':0, 'defense_value':10, 'life_value':50, 'exp_value':0, 'level':1, 'abilites':['attack',]}

    ARCHER = {'OrderID':4, 'name':'ARCHER', 'Move_distance_default':3, 'Attack_distance_default':3, 'image_name':'ARCHER.png',
                'attack_value':10, 'damage_value':0, 'defense_value':5, 'life_value':30, 'exp_value':0, 'level':1, 'abilites':['attack',]}

    ARTILLERY = {'OrderID':5, 'name':'ARTILLERY', 'Move_distance_default':2, 'Attack_distance_default':4, 'image_name':'ARTILLERY.png',
                'attack_value':20, 'damage_value':0, 'defense_value':1, 'life_value':30, 'exp_value':0, 'level':1, 'abilites':['attack',]}

    ENEMY_1 = {'OrderID':51, 'name':'ENEMY_1', 'Move_distance_default':3, 'Attack_distance_default':1, 'image_name':'ENEMY_1.png',
                'attack_value':10, 'damage_value':0, 'defense_value':1, 'life_value':30, 'exp_value':0, 'level':1, 'abilites':['attack',]}

    ENEMY_2 = {'OrderID':52, 'name':'ENEMY_2', 'Move_distance_default':3, 'Attack_distance_default':2, 'image_name':'ENEMY_2.png',
                'attack_value':10, 'damage_value':0, 'defense_value':1, 'life_value':30, 'exp_value':0, 'level':1, 'abilites':['attack',]}

    List = [WIZARD,WARRIOR,KNIGHT,ARCHER,ARTILLERY,ENEMY_1,ENEMY_2]



class Map_Elements():
    LAWN = 'lawn'
    MOUNTAIN = 'mountain'



class Game_Attr(Enum):
    INTERVAL = 50