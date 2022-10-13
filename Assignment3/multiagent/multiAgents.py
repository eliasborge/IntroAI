# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

'''
This code is heavily inspired by this github repository: 
https://github.com/lzervos/Berkeley_AI-Pacman_Projects

'''

import math
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        def max_value(gameState,depth):

            #Sjekker spillets nåværende tilstand
            actions=gameState.getLegalActions(0)
            if len(actions)==0 or gameState.isWin() or gameState.isLose() or depth==self.depth:           
                return(self.evaluationFunction(gameState),None)

            #Prøver å implementere begge sider av minimax algoritmen. Maksimum og minimum
            #Setter verdien til -infinity fordi vi skal finne maksimal verdi.
            w=-(float("inf"))                                                                               
            Act=None

            #Leter gjennom alle tilgjengelige trekk, og finner det beste. 
            for action in actions:                                                                         
                successorValue=min_value(gameState.generateSuccessor(0,action),1,depth)                         
                successorValue=successorValue[0]                                                                      
                if(successorValue>w):                                                                            
                    w,Act=successorValue,action
            return(w,Act)

        def min_value(gameState,agentID,depth):
            #Sjekker spillets nåværende tilstand
            Actions=gameState.getLegalActions(agentID)
            if len(Actions) == 0:
                return(self.evaluationFunction(gameState),None)

                #Til forskjell fra maksimum er verdien her satt til uendelig siden vi skal finne minimum
            l=float("inf")                                                                                 
            Act=None
            #Itererer gjennom alle mulige handlinger pacman kan gjøre
            for action in Actions:
                if(agentID !=gameState.getNumAgents() -1):
                    successorValue=min_value(gameState.generateSuccessor(agentID,action),agentID+1,depth)
                else:
                    successorValue=max_value(gameState.generateSuccessor(agentID,action),depth + 1)        
                successorValue=successorValue[0]
                if(successorValue<l):
                    l,Act=successorValue,action
            return(l,Act)
        max_value=max_value(gameState,0)[1]
        return max_value                        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def max_value(gameState,depth,a,b):
            #henter alle mulige handlinger
            Actions = gameState.getLegalActions(0) 
            if len(Actions)==0 or gameState.isWin() or gameState.isLose() or depth==self.depth:
                return (self.evaluationFunction(gameState), None)

            w=-(float("inf"))
            Act=None
                                                                                                            
            #itererer gjennom alle handlinger som er tilgjengelige                                                                                               
            for action in Actions:
                sucsValue=min_value(gameState.generateSuccessor(0,action),1,depth,a,b)
                sucsValue=sucsValue[0]
                if w<sucsValue:
                    w,Act=sucsValue,action
                if w>b:
                    return (w,Act)
                a=max(a,w)
            return (w,Act)

        def min_value(gameState,agentID,depth,a,b):
            
            #Sjekker tilstanden
            Actions=gameState.getLegalActions(agentID) 
            if len(Actions) == 0:
                return (self.evaluationFunction(gameState),None)
                                                                                                            

                                                                                                            
            l = float("inf")
            Act = None
            #Sjekker alle handlinger og finner den mest ideelle.
            for action in Actions:
                if (agentID == gameState.getNumAgents() - 1):
                    sucsValue = max_value(gameState.generateSuccessor(agentID,action),depth + 1,a,b)
                else:
                    sucsValue = min_value(gameState.generateSuccessor(agentID,action),agentID + 1,depth,a,b)
                sucsValue=sucsValue[0]
                if (sucsValue<l):
                    l,Act=sucsValue,action

                if (l<a):
                    return (l,Act)

                b=min(b,l)

            return(l,Act)                                                                                      

        a=-(float("inf"))
        b=float("inf")
        max_value=max_value(gameState,0,a,b)[1]
        return max_value                                                                   

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()
