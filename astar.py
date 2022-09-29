from typing import List
from xml.sax.handler import property_interning_dict

from numpy import true_divide
import Map

class Node:
    def __init__(self, cost=-1, parent = None, position = [0,0]):
        self.position= position
        self.cost = cost
        self.parent = parent
        self.children = []
        self.gn = 0
        self.hn = 0
        self.fn = 0


    def toString(self):
        return str(self.position) + " f: " + str(self.f) + " c: "+ str(self.cost)

    def checkIfSamePos(self,otherNode):
        return self.position == otherNode.position
    
    def checkF(self,target):
        dx = abs(target.position[0] - self.position[0])
        dy = abs(target.position[1] - self.position[1])

        self.hn = dx + dy
        self.fn = self.gn + self.hn
        


def check_if_neighbours(a: Node, b: Node):
    #Check if they are left-right neighbours
    if(a.position[1] == b.position[1]):
        if (a.position[0] == b.position[1] + 1) or (a.position[0] == b.position[0]-1):
            return True
    
    #Check if they are up-down neighbours: 
    if(a.position[0] == b.position[0]):
        if(a.position[1] == b.position[0] +1) or (a.position[1] == b.position[1] -1):
            return True

    # if neither of them run through.
    return False

def inform_of_better_paths(parent:Node):
    for child in parent.children:
        if parent.gn + child.cost < child.gn:
            child.parent = parent
            child.gn = parent.gn + child.cost
            inform_of_better_paths(child)


def aStar(start: Node, target: Node, nodes: List[Node]):
    #setup
    opened = []
    closed = []
    opened.append(start)

    #Agenda loop
    while True: 
        if len(opened) == 0:
            return False 
        
        current_node = opened.pop()
        closed.append(current_node)

        if(current_node == target):
            return True
        
        #Has to find all children of the current node

        for node in nodes:
            if check_if_neighbours(current_node,node):
                current_node.children.append(node)
        
        for child in current_node.children:
            if child not in opened and child not in closed:
                child.parent = current_node
                child.gn = child.parent.gn + child.cost
                child.checkF(target)
                opened.append(child)
            elif current_node.gn + child.cist < child.gn:
                child.parent = current_node
                child.gn = child.parent.gn + child.cost
                child.checkF(target)
                if child in closed:
                    inform_of_better_paths(child)



def main():
    # #Change this variable based on task
    # task = 1

    # map = Map.Map_Obj(task = task)
    # start = map.get_start_pos()
    # target = map.get_end_goal_pos()
    # path = map.fill_critical_positions(task=task)[3]
    # grid = map.read_map(path)[0]
    # startNode = None
    # goalNode = None
    # nodes = []

    # for y in range(len(grid)):
    #     for x in range(len(grid)[0]):
    #         node = Node(cost=grid[y][x],position=[y,x]) 
    #         nodes.append(node)
    #         if node.position == start:


    # Det her er et forsøk på implementasjon inspirert av en annen greie
    # Men det er ikke helt ferdig. 
    # Alt over er sånn standard implementasjon av selve algoritmen 
    # og nodene.


    







