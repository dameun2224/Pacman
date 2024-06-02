# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

"""
discount: 낮을수록 가까운 보상
noise: 행동의 불확실성
living reward: 살아있는 동안 받는 보상. 음수라면 빨리 끝내려하고, 양수라면 오래 남아있으려한다.
"""

# Q2 - Solved #
def question2():
    answerDiscount = 0.9
    answerNoise = 0
    return answerDiscount, answerNoise

# Q3(3a ~ 3e) #

# 절벽(-10)의 위험을 감수하면서 가까운 출구(+1)를 선호하는 유형
def question3a(): 
    answerDiscount = 0.2
    answerNoise = 0
    answerLivingReward = -1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

# 절벽(-10)을 피하는 동시에 가까운 출구(+1)를 선호하는 유형
def question3b():
    answerDiscount = 0.2
    answerNoise = 0.2
    answerLivingReward = -1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

# 절벽(-10)의 위험을 감수하면서 먼 출구(+10)를 선호하는 유형
def question3c():
    answerDiscount = 0.2
    answerNoise = 0
    answerLivingReward = 1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

# 절벽(-10)을 피하는 동시에 먼 출구(+10)를 선호하는 유형
def question3d():
    answerDiscount = 0.8
    answerNoise = 0.2
    answerLivingReward = -0.5
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

# 출구와 절벽을 모두 피하는 유형(즉, 에피소드가 종료되지 않아야 함)
def question3e():
    answerDiscount = 0.2
    answerNoise = 0
    answerLivingReward = 20
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

# Q7 #
def question8():
    return 'NOT POSSIBLE'
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
