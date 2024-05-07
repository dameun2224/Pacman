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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

# Q1: Reflex Agent - solved #
class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore] # bestScore의 index 선택
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        #print("\n---getAction---")
        #print("legalMoves: ", legalMoves)
        #print("bestScore: ", bestScore)
        #print("chosenIndex: ", chosenIndex)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex] # besScore의 인덱스 action

    def evaluationFunction(self, currentGameState: GameState, action):
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

        #print("\n---evaluationFunction---")
        #print("successorGameState: ", successorGameState)
        #print("newPos: ", newPos)
        #print("newFood: ", newFood)
        #print("newGhostStates: ", newGhostStates)
        #print("newScaredTimes: ", newScaredTimes)
        #print("successorGameState.getScore(): ", successorGameState.getScore())

        "*** YOUR CODE HERE ***"
        # getAction 함수에서 호출됨. action에 대한 점수를 리턴함.

        newScore = successorGameState.getScore()

        # ghost에 대한 처리
        # ghost와 거리가 멀다면 높은 점수
        # -> 따로 처리가 없어도 맞아서 구현하지 않음.

        # food에 대한 처리
        # food와 거리가 가깝다면 높은 점수
        foods = newFood.asList()
        dis = 1e9
        for food in foods:
            dis = min(dis, util.manhattanDistance(newPos, food))
        
        newScore += 1 / dis 

        return newScore

def scoreEvaluationFunction(currentGameState: GameState):
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

# Q2: minimax - unsolved #
class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
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
        # Collect legal moves and successor states
        
        result = self.minimax(gameState, 0, 0)
        action = result[1]

        return action

    def minimax(self, gameState: GameState, depth, agentIndex):
        # 마지막 ghost 라면
        if agentIndex == gameState.getNumAgents():
            depth += 1
            agentIndex = 0
            
        # 종료조건
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return (self.evaluationFunction(gameState), None)
        
        # 종료 조건 확인 문제로 답이 달라 위로 올림
        # if agentIndex == gameState.getNumAgents():
        #     depth += 1
        #     agentIndex = 0

        # max or min
        if agentIndex == 0: # max
            legalMoves = gameState.getLegalActions(agentIndex)
            list = []
            for action in legalMoves:
                list.append((self.minimax(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)[0], action)) # 노드 생성
            return max(list)
        else: # min
            legalMoves = gameState.getLegalActions(agentIndex)
            list = []
            for action in legalMoves:
                list.append((self.minimax(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)[0], action)) # 노드 생성
            return min(list)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction