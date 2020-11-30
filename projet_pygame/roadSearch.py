import game_AI as AI
import settings as st
import numpy
import game_functions as gf



class Node:     
    def __init__(self, pos, g = 0, h = 0):  
        self.pos = pos
        self.father = None
        self.g = g
        self.h = h
  

    def manhattan(self, endNodePos):
        offset_x = abs(self.pos[0]-endNodePos[0])//st.Game_Attr.INTERVAL.value
        offset_y = abs(self.pos[1]-endNodePos[1])//st.Game_Attr.INTERVAL.value
        distance = offset_x + offset_y
        self.h = distance
    

    def setG(self, g):
        self.g = g


    def setFather(self, node):
        self.father = node



class roadSearch_AStar:
    def __init__(self, weightedMap, startNode, endNodePos):
        self.openList = []
        self.closeList = []
        self.pathList = []
        self.zone_movable = []
        self.zone_attackable = []
        self.startNode = startNode
        self.endNodePos = endNodePos
        self.currentNode = startNode
        self.weightedMap = weightedMap


    def getMinFNode(self): 
        nodeTemp = self.openList[0]  
        for node in self.openList:  
            if node.g + node.h < nodeTemp.g + nodeTemp.h:  
                nodeTemp = node  
        return nodeTemp


    def nodeInOpenlist(self,node):
        for nodeTmp in self.openList:  
            if nodeTmp.pos == node.pos:
                return True
        return False


    def nodeInCloselist(self,node):
        for nodeTmp in self.closeList:  
            if nodeTmp.pos == node.pos:
                return True
        return False


    def endNodeInOpenList(self):  
        for nodeTmp in self.openList:  
            if nodeTmp.pos == self.endNodePos:
                return True  
        return False


    def getNodeFromOpenList(self,node):  
        for nodeTmp in self.openList:  
            if nodeTmp.pos == node.pos:
                return nodeTmp  
        return None


    def getWeight_atPos_onWeightedMap(self,pos):
        Pwidth = pos[0] // st.Game_Attr.INTERVAL.value
        Pheight = pos[1] // st.Game_Attr.INTERVAL.value

        weight = self.weightedMap[Pheight][Pwidth]
        if weight >= 500:
            return -1   # impassable
        return weight


    def setWeight_atPos_onWeightedMap(self, pos, weight):
        rowNumber = pos[1] // st.Game_Attr.INTERVAL.value
        colNumber = pos[0] // st.Game_Attr.INTERVAL.value
        self.weightedMap[rowNumber][colNumber] = weight
        

    def searchOneNode(self, node):
        if self.nodeInCloselist(node):
            return

        g_node = self.getWeight_atPos_onWeightedMap(node.pos)

        if self.nodeInOpenlist(node) == False:
            node.setG(g_node)
            node.manhattan(self.endNodePos)
            node.setFather(self.currentNode)
            self.openList.append(node)
        else:
            nodeTmp = self.getNodeFromOpenList(node)
            if self.currentNode.g + g_node < nodeTmp.g:
                nodeTmp.g = self.currentNode.g + g_node
                nodeTmp.father = self.currentNode
        return


    def searchNear(self):
        upNodePos = (self.currentNode.pos[0], self.currentNode.pos[1]-st.Game_Attr.INTERVAL.value)
        if upNodePos[1] >= 0:
            g_upNode = self.getWeight_atPos_onWeightedMap(upNodePos)
            if g_upNode > 0:
                self.searchOneNode(Node(upNodePos))

        rightNodePos = (self.currentNode.pos[0]+st.Game_Attr.INTERVAL.value, self.currentNode.pos[1])
        if rightNodePos[0] <= (numpy.shape(self.weightedMap)[1] - 1) * st.Game_Attr.INTERVAL.value:
            g_rightNode = self.getWeight_atPos_onWeightedMap(rightNodePos)
            if g_rightNode > 0:
                self.searchOneNode(Node(rightNodePos))

        downNodePos = (self.currentNode.pos[0], self.currentNode.pos[1]+st.Game_Attr.INTERVAL.value)
        if downNodePos[1] <= (numpy.shape(self.weightedMap)[0] - 1) * st.Game_Attr.INTERVAL.value:
            g_downNode = self.getWeight_atPos_onWeightedMap(downNodePos)
            if g_downNode > 0:
                self.searchOneNode(Node(downNodePos))

        leftNodePos = (self.currentNode.pos[0]-st.Game_Attr.INTERVAL.value, self.currentNode.pos[1])
        if leftNodePos[0] >= 0:
            g_leftNode = self.getWeight_atPos_onWeightedMap(leftNodePos)
            if g_leftNode > 0:
                self.searchOneNode(Node(leftNodePos))


    def searchRoad(self):
        self.startNode.manhattan(self.endNodePos)
        self.startNode.setG(0)
        self.openList.append(self.startNode)

        while True:
            self.currentNode = self.getMinFNode()
            self.closeList.append(self.currentNode)
            self.openList.remove(self.currentNode)

            self.searchNear()

            if self.endNodeInOpenList():
                nodeTmp = self.getNodeFromOpenList(Node(self.endNodePos))
                while True:
                    self.pathList.append(nodeTmp)
                    if nodeTmp.father != None:
                        nodeTmp = nodeTmp.father
                    else:
                        return True
            elif len(self.openList) == 0:
                return False
        return True



if __name__ == '__main__':
    ##构建地图
    WeightedMap = numpy.ones((10,12))
    WeightedMap[2][2] = 500
    WeightedMap[2][3] = 500
    WeightedMap[2][4] = 500
    WeightedMap[2][5] = 500
    WeightedMap[2][6] = 500
    WeightedMap[2][7] = 30
    WeightedMap[3][7] = 30
    WeightedMap[4][7] = 30
    WeightedMap[5][7] = 30
    print(WeightedMap)    
    
    roadSearch_AStar = roadSearch_AStar(WeightedMap, Node((300,50)), (250,150))
    if roadSearch_AStar.searchRoad():
        for Node in roadSearch_AStar.pathList:
            print(Node.pos)
    else:
        print("no way")
    