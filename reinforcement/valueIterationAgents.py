# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections


# Q1 - Solved #
class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        """
        총 iterations 만큼 반복
        mdp의 각 상태에서, 가능한 모든 action에 대해 Q-값을 계산하고 최댓값을 max_value에 저장
        각 상태의 max_value를 new_value에 저장하고, 각 i마다 values를 new_values로 업데이트
        """

        for i in range(0, self.iterations):
            new_values = util.Counter()
            for state in self.mdp.getStates():
                if self.mdp.isTerminal(state):
                    continue
                max_value = float('-inf')
                for action in self.mdp.getPossibleActions(state):
                    max_value = max(max_value, self.computeQValueFromValues(state, action))
                new_values[state] = max_value
            self.values = new_values

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"

        """
        self.values에 의해 제공된 가치 함수에 따라 (state, action) 쌍의 Qvalue 리턴
        getQValue 함수에서 호출됨

        Q(s,a)=∑s′T(s,a,s′)[R(s,a,s′)+γV(s′)]
        """

        q_value = 0

        # nxt_state = s′, prob = T(s,a,s′)
        # self.mdp.getReward(state, action, nxt_state) = R(s,a,s′), self.discount = γ, self.values[nxt_state] = V(s′)
        for nxt_state, prob in self.mdp.getTransitionStatesAndProbs(state, action): 
            cur_value = self.mdp.getReward(state, action, nxt_state) + self.discount * self.values[nxt_state]
            q_value += prob * cur_value

        return q_value

        #util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        """
        self.values에 의해 제공된 가치 함수에 따라 최적의 action을 계산
        getPolicy, getAction 함수에서 호출됨
        해당 state에서 가능한 모든 action에서 최적의 action 반환
        """

        if self.mdp.isTerminal(state):
            return None

        actions = self.mdp.getPossibleActions(state)
        max_value = float('-inf')
        max_action = None

        for action in actions:
            cur_value = self.getQValue(state, action)
            if(max_value < self.getQValue(state, action)):
                max_value = cur_value
                max_action = action
                
        return max_action
            
        #util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

# Q4 #
class PrioritizedSweepingValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        max_values = util.Counter()
        states = self.mdp.getStates()

        # predecessors 계산
        predecessors = {}
        for state in states:
            predecessors[state] = set()

        for state in states:
            if self.mdp.isTerminal(state):
                continue
            for action in self.mdp.getPossibleActions(state):
                for next_state, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                    if prob > 0:
                        predecessors[next_state].add(state)
                        
        # pq 채우기
        pq = util.PriorityQueue()
        for state in states:
            if self.mdp.isTerminal(state):
                continue
            current_value = self.values[state]
            max_value = max([self.computeQValueFromValues(state, action)
                             for action in self.mdp.getPossibleActions(state)])
            diff = abs(current_value - max_value)
            pq.push(state, -diff)
        
        # iterations 동안 반복
        for i in range(self.iterations):
            if pq.isEmpty():
                break

            state = pq.pop()

            if not self.mdp.isTerminal(state):
                self.values[state] = max([self.computeQValueFromValues(state, action)
                                          for action in self.mdp.getPossibleActions(state)])

            # 전임자 상태 갱신
            for predecessor in predecessors[state]:
                if not self.mdp.isTerminal(predecessor):
                    current_value = self.values[predecessor]
                    max_value = max([self.computeQValueFromValues(predecessor, action)
                                     for action in self.mdp.getPossibleActions(predecessor)])
                    diff = abs(current_value - max_value)
                    if diff > self.theta:
                        pq.update(predecessor, -diff)

                



