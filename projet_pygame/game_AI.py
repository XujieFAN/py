import pygame
import game_functions as gf
import game_objects as gobj
import settings as st
import numpy
import time
import roadSearch as rs


class GameAI:
    def __init__(self, Everything, screen):
        self.Everything = Everything
        self.screen = screen


    def do_AI_actions(self):
        self.Everything.AI_moving = 1
        for player in self.Everything.Group_HumainPlayers:
            player.attackable = 1
        for NPC in self.Everything.Group_ComputerPlayers:
            NPC.finished = 0
        self.Everything.refresh_WeightedMap()

        self.do_NPC_OneByOne()
        
        for player in self.Everything.Group_HumainPlayers:
            player.attackable = 0
            player.selected = 0
            player.moved = 0
            player.finished = 0
        self.Everything.AI_moving = 0
        pygame.event.clear()

    
    def getTarget(self):
        player_with_LowerLif = self.Everything.Group_HumainPlayers.sprites()[0]
        for player in self.Everything.Group_HumainPlayers:
            if player_with_LowerLif.life_value > player.life_value:
                player_with_LowerLif = player
        return player_with_LowerLif, player_with_LowerLif.pos


    def check_reachTarget(self, pos, target):
        if (abs(target.pos[0]-pos[0]) // st.Game_Attr.INTERVAL.value + abs(target.pos[1]-pos[1]) // st.Game_Attr.INTERVAL.value) == 1:
            return True
        else: return False


    def do_NPC_OneByOne(self):
        for NPC in self.Everything.Group_ComputerPlayers:
            if NPC.finished == 0:
                target, targetPos = self.getTarget()
                print('target at :',targetPos)
                if self.check_reachTarget(NPC.pos, target):
                    NPC.attack(target)
                else:
                    roadSearch_AStar = rs.roadSearch_AStar(self.Everything.weightedMap, rs.Node(NPC.pos), targetPos)
                    roadSearch_AStar.setWeight_atPos_onWeightedMap(targetPos,1)
                    if roadSearch_AStar.searchRoad():
                        stepNode = roadSearch_AStar.pathList.pop()
                        i = NPC.move_distance
                        while i > 0 and len(roadSearch_AStar.pathList) > 0:
                            stepNode = roadSearch_AStar.pathList.pop()
                            if stepNode.pos != targetPos:
                                NPC.move_one_step(stepNode.pos)
                                i = i - 1
                                
                                self.screen.blit(self.Everything.map, (0,0))
                                self.Everything.draw(self.screen)
                                pygame.display.flip()
                            else:
                                NPC.attack(target)
                                break
                            if self.check_reachTarget(NPC.pos, target):
                                NPC.attack(target)
                        NPC.finished = 1
                    else:print('no road found!')
            self.Everything.refresh_WeightedMap()



if __name__ == "__main__":
    pass
        