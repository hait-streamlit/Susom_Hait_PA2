from .model import *

# combine the minimax and alpha-beta agents into one agent
# add an alpha-beta flag to the constructor
class Agent: 
    def __init__(self, boardmatrix, turn, depth, function, is_alpha_beta=False, type=0):
        self.boardmatrix = boardmatrix
        self.turn = turn
        self.maxdepth = depth
        self.function = function
        self.is_alpha_beta = is_alpha_beta # add boolean check -> activate alpha-beta pruning
        self.type = type
        self.nodes = 0
        self.piece_num = 0

    def max_value(self, state, alpha, beta, depth):
        # recursion base case
        if depth == self.maxdepth or state.isgoalstate() != 0:
            return state.utility(self.turn)
        
        v = MINNUM # init v to min value
        actions = state.available_actions()

        for action in actions:
            v = max(v, self.min_value(state.transfer(action), alpha, beta, depth + 1))
            self.nodes += 1
            
            if self.is_alpha_beta:
                if v >= beta:
                    return v
                alpha = max(alpha, v)
        return v
    
    def min_value(self, state, alpha, beta, depth):
        # recursion base case
        if depth == self.maxdepth or state.isgoalstate() != 0:
            return state.utility(self.turn)
        
        v = MAXNUM # init v to min value
        actions = state.available_actions()

        for action in actions:
            v = min(v, self.max_value(state.transfer(action), alpha, beta, depth + 1))
            self.nodes += 1

            if self.is_alpha_beta:
                if v <= alpha:
                    return v
                beta = min(beta, v)
        return v
    
    def decision(self):
        final_action = None
        initialstate = breakthrough_state(boardmatrix=self.boardmatrix, turn=self.turn, function=self.function, type=self.type)
        
        v = MINNUM
        for action in initialstate.available_actions():
            self.nodes += 1

            new_state = initialstate.transfer(action)
            if new_state.isgoalstate():
                final_action = action
                break
            minresult = self.min_value(new_state, MINNUM, MAXNUM, 1)
            if minresult > v:
                final_action = action
                v = minresult

        if self.turn == 1:
            self.piece_num = initialstate.transfer(final_action).white_num
        elif self.turn == 2:
            self.piece_num = initialstate.transfer(final_action).black_num
        #print(final_action)
        return initialstate.transfer(final_action), self.nodes, self.piece_num