from typing import List
from xml.sax.handler import property_interning_dict

from numpy import true_divide
import Map


# Simple class to keep info about nodes.
class Node:
    def __init__(self, position:list):
        self.position= position
        self.parent = None
        self.children = []
        self.gn = 0 #A nodes weight
        self.hn = 0 #A nodes heuristic value, in this case its Manhattan Distance.
        self.fn = 0 #The total value of a node. gn + hn.

    #Control the heuristic value of a node
    def checkF(self,targetNode):
        dx = abs(targetNode.position[0] - self.position[0])
        dy = abs(targetNode.position[1] - self.position[1])

        self.hn = dx + dy
        self.fn = self.gn + self.hn

    #Discover all child nodes from a specific node,
    def find_children(self, map:Map.Map_Obj):
        children = []
        up = [self.position[0]-1,self.position[1]]
        down = [self.position[0]+1,self.position[1]]
        left = [self.position[0],self.position[1]+1]
        right = [self.position[0],self.position[1]-1]

        dir = [up,down,left,right]
        for d in dir:
            if map.get_cell_value(d) > -1:
                children.append(Node(d))

        return children

#If a new and better path is discovered, it has to be propagated and informed to all other nodes. 
#Therefore it is a recursive function.
def inform_of_better_paths(parent:Node, map: Map.Map_Obj):
    for child in parent.children:
        if parent.gn + map.get_cell_value(child.position) < child.gn:
            child.parent = parent
            attach_and_evaluate(child,parent,map)
            inform_of_better_paths(child,map)

#Checks the heuristic value of a Node and attaches it to the "path"
def attach_and_evaluate(child:Node,parent:Node,map:Map.Map_Obj):
    child.parent = parent
    child.gn = parent.gn + map.get_cell_value(child.position)
    child.checkF(Node(map.get_end_goal_pos()))


    #Method for drawing the shortest path in the map by changing its value and therefore its color 
    #in the visual representation.
def tracePath(node:Node,map:Map.Map_Obj):
    map.set_cell_value(map.get_goal_pos(),6)
    while node.parent is not None:
        if node.position == map.get_goal_pos:
            break
        map.set_cell_value(node.position,5)
        node = node.parent
    map.set_cell_value(map.get_end_goal_pos(),7)
    map.show_map()
    

    #Checks if the current node already has been checked by the agenda loop.
    #If it is a dup. it returns the eldest version. 
def check_if_child_is_created(child:Node,list1:list[Node],list2:list[Node]):
    for node in list1:
        if node.position == child.position:
            return node 

    for node in list2:
        if node.position == child.position:
            return node
    return child

#The actual implementation of the A* algorithm.
def aStar(map:Map.Map_Obj):
    #setup
    print("A* Algorithm activated")
    opened = []
    closed = []
    node = Node(map.get_start_pos())
    opened.append(node)

    #Agenda loop
    while node.position != map.get_goal_pos(): 
        #If there are no more nodes in the Open list, and we are not at the end, A* fails.
        if len(opened) == 0:
            print("Stopped. A* failed")
            return current_node 
        
        current_node = opened.pop()
        closed.append(current_node)

        #If we are at the end goal.
        if(current_node.position == map.get_goal_pos()):
            print("Works!")
            return current_node
        
        #Have to find all children of the current node
        children = current_node.find_children(map)

        #Checks all the children of the current node.
        for child in children:
            new_child = check_if_child_is_created(child,opened,closed)
            #If the node hasn't been checked earlier.
            if new_child not in opened and new_child not in closed:
                attach_and_evaluate(new_child,current_node,map)
                opened.append(new_child)
                #Sort by best values
                opened.sort(key=lambda y: y.fn, reverse=True)
            elif current_node.gn + map.get_cell_value(new_child.position) < new_child.gn:
                attach_and_evaluate(new_child,current_node,map)
                if new_child in closed:
                    inform_of_better_paths(new_child,map)
            


# Main method to make it run.
def main():

    map = Map.Map_Obj(4) # <--- Change this input number to change task
    # x here is the end node.
    x = aStar(map)
    tracePath(x,map)

    
main()


