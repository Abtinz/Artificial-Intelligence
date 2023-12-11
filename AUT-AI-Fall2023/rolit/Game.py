from Display import Display
from Agents import Agent

import copy 
from typing import List
from operator import add

class GameStateData:
    """
        This class holds the main states of the game. It includes the board, pieces of each player and their total score.
    """

    def __init__(self, prevState=None) -> None:
        
        if prevState is not None:
            self.board = copy.deepcopy(prevState.board)
            self.score = copy.deepcopy(prevState.score)
            self.agentStates = copy.deepcopy(prevState.agentStates)
            self.agentsCount = prevState.agentsCount
            self.isWin = prevState.isWin
            self.isFinished = prevState.isFinished
            self.stepCount = prevState.stepCount
        else:
            self.board = [[-1] * 8 for _ in range(8)]
            self.score = [2, 2]
            self.agentStates = [[(3,3), (4,4)], [(3,4), (4,3)]]
            self.agentsCount = 2
            self.isWin = False
            self.isFinished = False
            self.stepCount = 0

    def initialize(self, agentsCount):

        self.agentsCount = agentsCount
        self.stepCount = 0
        if agentsCount == 2:
            self.score = [2, 2]
            self.agentStates = [[(3,3), (4,4)], [(3,4), (4,3)]]
            self.board[3][3] = self.board[4][4] = 0
            self.board[3][4] = self.board[4][3] = 1
        elif agentsCount == 4:
            self.score = [1, 1, 1, 1]
            self.agentStates = [[(3,3)], [(3,4)], [(4,4)], [(4,3)]]
            self.board[3][3] = 0
            self.board[3][4] = 1
            self.board[4][4] = 2
            self.board[4][3] = 3


class GameState:
    """
        This class holds the state of the game and provides users with more features through its various methods.
    """

    ###########################################
    ### You may want to take a look at this ###
    ###########################################

    def isGameFinished(self) -> bool:
        """ Determines whether we have a winner or not. If there is no winner and also, no action left, it is a tie. """

        return self.data.isFinished

    def getPieces(self, index=0):
        """ Returns positions of each player's pieces in a list. """

        return self.data.agentStates[index]

    def getCorners(self):
        """ Returns a 4-tuple each with the index of the player who occupies that corner. Returns -1 if it is free. """

        return self.data.board[0][0], self.data.board[0][7], self.data.board[7][0], self.data.board[7][7]
    
    def getScore(self, index=None):
        """ Returns the each player's score, list of their scores if no index is given. """

        if index is None:
            return self.data.score
        
        return self.data.score[index]
    
    def getNumAgents(self):
        """ Returns the number of agents. """

        return self.data.agentsCount
    
    def generateSuccessor(self, agentIndex, action):
        """ Given an action, returns the state to which that action leads and the pieces it will flip. """

        if self.isGameFinished():
            return None
        
        state = GameState(self)

        state.placePiece(agentIndex, action)

        if sum(state.data.score) == 64:
            state.data.isFinished = True

            winner_score = max(state.data.score)
            winner_count = state.data.score.count(winner_score)
            if winner_count == 1 and state.data.score[0] == winner_score: # winning state
                state.data.isWin = True

        return state
    
    def getLegalActions(self, index):
        """ Returns legal actions each player has to decide between. """

        key_string = str(self.data.board) + 'CONSTANT' + str(index)
        hash_string = hash(key_string)

        if hash_string in GameState.next_states:
            return GameState.next_states[hash_string]
        
        action_list = self.getPossibleActions(index)
        if len(action_list) == 0:
            action_list = self.getPossibleActionsSimplified()

        GameState.next_states[hash_string] = action_list

        return action_list
    
    ###########################################
    ###  You probably won't need this part  ###
    ###########################################
    
    next_states = {}

    def __init__(self, prevState=None):
        if prevState is not None:
            self.data = GameStateData(prevState.data)
        else:
            self.data = GameStateData()

    def initialize(self, agentsCount):
        self.data.initialize(agentsCount)

    def isWin(self):
        return self.data.isWin

    def isWithinBorders(self, pos):
        return pos[0] >= 0 and pos[0] < len(self.data.board) and pos[1] >= 0 and pos[1] < len(self.data.board[0])
    
    def nextUnoccupiedPos(self, index, init_pos, dir):
        # either an empty place, out of border, or same index piece
        if dir not in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            return None
        
        pos = (init_pos[0] + dir[0], init_pos[1] + dir[1])

        # check the position immediately after, if empty or same color or out of bound then there's no legal action
        if not self.isWithinBorders(pos) or self.data.board[pos[0]][pos[1]] == -1 or self.data.board[pos[0]][pos[1]] == index:
            return None
        
        while self.isWithinBorders(pos := (pos[0] + dir[0], pos[1] + dir[1])):
            current_index = self.data.board[pos[0]][pos[1]]
            if current_index == index:
                return None # same color piece
            if current_index == -1:
                return pos
            
        return None # out of bounds
    
    def getPieceActions(self, index, pos):
        actions = []

        for dir in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            if action := self.nextUnoccupiedPos(index, pos, dir):
                actions.append(action)
        
        return actions
    
    def getPossibleActions(self, index):
        current_pieces = []

        current_pieces = self.getPieces(index)

        legal_actions = []

        for current_piece in current_pieces:
            actions_for_piece = self.getPieceActions(index, current_piece)
            legal_actions += actions_for_piece

        return legal_actions
    
    def getPossibleActionsSimplified(self):
        current_pieces = []

        for agentState in self.data.agentStates:
            for pos in agentState:
                current_pieces.append(pos)

        legal_actions = set()
        for piece in current_pieces:
            for dir in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                pos = (piece[0] + dir[0], piece[1] + dir[1])
                if self.isWithinBorders(pos) and self.data.board[pos[0]][pos[1]] == -1:
                    legal_actions.add(pos)
        
        return sorted(list(legal_actions))
    
    def placePiece(self, index, pos):

        if not self.isWithinBorders(pos):
            print('Game.placePiece: out of board position!')
            return
        
        if self.data.board[pos[0]][pos[1]] != -1:
            print('Game.placePiece: already played position!')
            return
        
        flip_list = []
        for dir in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            temp_list = []
            current_pos = pos
            while (current_pos := (current_pos[0] + dir[0], current_pos[1] + dir[1])):
                if not self.isWithinBorders(current_pos):
                    break # out of bound
                if self.data.board[current_pos[0]][current_pos[1]] == index:
                    flip_list += temp_list 
                    break # the two ends of a line is found
                elif self.data.board[current_pos[0]][current_pos[1]] == -1:
                    break # disconnected
                else:
                    temp_list.append(current_pos)
        
        change_list = [0] * self.data.agentsCount

        self.data.board[pos[0]][pos[1]] = index
        change_list[index] = 1 + len(flip_list)
        self.data.agentStates[index].append(pos)

        for flip_pos in flip_list:
            old_index = self.data.board[flip_pos[0]][flip_pos[1]]
            self.data.board[flip_pos[0]][flip_pos[1]] = index
            change_list[old_index] -= 1
            self.data.agentStates[old_index].remove(flip_pos)
            self.data.agentStates[index].append(flip_pos)

        self.data.score = list(map(add, self.data.score, change_list))
        return flip_list
    
    def getStep(self):
        return self.data.stepCount
    
    def doStep(self):
        self.data.stepCount += 1
        return self.data.stepCount
    
import pickle

class Game:
    """
        This class defines the main game loop.
    """

    def __init__(self, agents: List[Agent], display: Display, state: GameState) -> None:
        self.agents = agents
        self.display = display
        self.state = state
        self.moveHistory = []
        self.gameOver = False

    def run(self):
        """
            In this function which is basically the outer loop of the game, each player takes its turn to choose an action and then,
            the game state is updated using that action. This continues until the game finishes.
        """
        
        # initialize the display if necessary
        agentCount = len(self.agents)
        steps = self.state.getStep()
        self.display.initialize(self.state.data.board, agentCount, steps)

        # check if already finished
        if self.state.isGameFinished():
            self.printResults(self.state.isWin(), self.state.data.score)
            self.gameOver = True

        # main loop, until the game is over
        while not self.gameOver:

            # pick agent
            agent = self.agents[steps % agentCount]

            # pick solicit action
            action = agent.getAction(self.state)

            # add action to the action list
            self.moveHistory.append(action)

            # update the state
            self.state = self.state.generateSuccessor(steps % agentCount, action)

            # update the display
            self.display.update(self.state.data.board)

            # check if finished
            if self.state.isGameFinished():
                self.printResults(self.state.isWin(), self.state.data.score)
                self.gameOver = True

            steps = self.state.doStep()

    def printResults(self, isWin, scores):
        if isWin:
            print(f"you won scoring {scores[0]}.")
        else:
            print(f"you did not win! your score was {scores[0]}.")

        print("other agents' results:")
        for agentNum, score in enumerate(scores[1:], start=1):
            print(f'Agent #{agentNum} scored {score}.')