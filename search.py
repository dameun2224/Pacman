# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

# Q1: 깊이 우선 탐색 #
def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    if(problem.isGoalState(problem.getStartState())):
        return []

    from util import Stack
    stack = Stack() # (x, y), ['dir1', 'dir2', ...]
    stack.push((problem.getStartState(), []))

    visited = [] # [(x1, y1), (x2, y2), ...]
    visited.append(problem.getStartState())

    #print("stack:", stack)
    #print("visited:", visited)

    # stack이 비어 있지 않은 동안 반복
    while(not stack.isEmpty()):
        currLotation, path = stack.pop() # (x, y), ['dir1', 'dir2', ...]
        visited.append(currLotation)
        #print("currLotation:", currLotation)
        #print("path:", paht)

        # 종료 조건 - 목표 지점이라면 path를 반환하고 종료
        if problem.isGoalState(currLotation):
            #print("path:", path)
            return path
        
        succ = problem.getSuccessors(currLotation) # succ = [succ1, succ2, ...], succ1 = [((nx, ny), 'Dir', 1)]

        #print("succ:", succ)

        for nxtLotation, nxtDir, nxtCost in succ: # nxtSucc = [(nx, ny), 'Dir', 1]
            if nxtLotation in visited:
                continue
            stack.push((nxtLotation, path + [nxtDir]))

    return []
    
    #util.raiseNotDefined()
    


# Q2: 넓이 우선 탐색 #
def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    if(problem.isGoalState(problem.getStartState())):
        return []

    from util import Queue
    queue = Queue() # (x, y)
    queue.push((problem.getStartState(), []))

    visited = [] # (x1, y1), (x2, y2), ...
    visited.append(problem.getStartState())

    # queue가 비어 있지 않은 동안 반복
    while(not queue.isEmpty()):
        currLotation, path = queue.pop()

        if(problem.isGoalState(currLotation)):
            return path
        
        succ = problem.getSuccessors(currLotation)
        for nxtLotation, nxtDir, nxtCost in succ:
            if nxtLotation in visited:
                continue
            visited.append(nxtLotation)
            queue.push((nxtLotation, path + [nxtDir]))

    return []

    #util.raiseNotDefined()

# Q3: 비용 함수 변경
def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# Q4: A* 탐색
def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
