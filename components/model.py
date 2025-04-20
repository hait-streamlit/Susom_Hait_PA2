import random # use random to break ties

# rename the original 8x8 board template
eight_by_eight = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2],
]

# add the new 5x10 board template
five_by_ten = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]


MAXNUM = float("inf")
MINNUM = -float("inf")
MAXTUPLE = (MAXNUM, MAXNUM)
MINTUPLE = (MINNUM, MINNUM)

# direction: 1 -> left, 2 -> middle, 3 -> right
def single_move(initial_pos, direction, turn):
    if turn == 1:
        if direction == 1:
            return initial_pos[0] + 1, initial_pos[1] - 1
        elif direction == 2:
            return initial_pos[0] + 1, initial_pos[1]
        elif direction == 3:
            return initial_pos[0] + 1, initial_pos[1] + 1
    elif turn == 2:
        if direction == 1:
            return initial_pos[0] - 1, initial_pos[1] - 1
        elif direction == 2:
            return initial_pos[0] - 1, initial_pos[1]
        elif direction == 3:
            return initial_pos[0] - 1, initial_pos[1] + 1

# flip the turns (B -> W or W -> B)
def alterturn(turn):
    if turn == 1:
        return 2
    if turn == 2:
        return 1

class Action:
    def __init__(self, coordinate, direction, turn):
        self.coordinate = coordinate
        self.direction = direction
        self.turn = turn
    def __str__(self):
        return f"{self.coordinate} {self.direction} {self.turn}"
    def getCoordinate_x(self):
        return self.coordinate[0]

# slight modifications made to the original State class
class State:
    def __init__(self, boardmatrix=None, black_position=None, white_position=None, black_num=0, white_num=0, turn=1, function=0, height=None, width=None, type=0):
        self.width = len(boardmatrix[0]) if width is None else width
        self.height = len(boardmatrix) if height is None else height
        self.type = type

        if black_position is None:
            self.black_positions = []
        else:
            self.black_positions = black_position
        if white_position is None:
            self.white_positions = []
        else:
            self.white_positions = white_position
        self.black_num = black_num
        self.white_num = white_num
        self.turn = turn
        self.function = function
        if boardmatrix is not None:
            for i in range(self.height):
                for j in range(self.width):
                    if boardmatrix[i][j] == 1:
                        self.black_positions.append((i, j))
                        self.black_num += 1
                    if boardmatrix[i][j] == 2:
                        self.white_positions.append((i, j))
                        self.white_num += 1

    # State.transfer(action), given an action, return a resultant state
    def transfer(self, action):
        black_pos = list(self.black_positions)
        white_pos = list(self.white_positions)

        # black move
        if action.turn == 1:
            if action.coordinate in self.black_positions:
                index = black_pos.index(action.coordinate)
                new_pos = single_move(action.coordinate, action.direction, action.turn)
                black_pos[index] = new_pos
                if new_pos in self.white_positions:
                    white_pos.remove(new_pos)
            else:
                print("Invalid action!")

        # white move
        elif action.turn == 2:
            if action.coordinate in self.white_positions:
                index = white_pos.index(action.coordinate)
                new_pos = single_move(action.coordinate, action.direction, action.turn)
                white_pos[index] = new_pos
                if new_pos in self.black_positions:
                    black_pos.remove(new_pos)
            else:
                print("Invalid action!")

        state = State(black_position=black_pos, white_position=white_pos, black_num=self.black_num, white_num=self.white_num, turn=alterturn(action.turn), function=self.function, height=self.height, width=self.width)
        return state

    def available_actions(self):
        available_actions = []
        if self.turn == 1:
            for pos in sorted(self.black_positions, key=lambda p: (p[0], -p[1]), reverse=True):
                # ======Caution!======
                if pos[0] != self.height - 1 and pos[1] != 0 and (pos[0] + 1, pos[1] - 1) not in self.black_positions:
                    available_actions.append(Action(pos, 1, 1))
                if pos[0] != self.height - 1 and (pos[0] + 1, pos[1]) not in self.black_positions and (pos[0] + 1, pos[1]) not in self.white_positions:
                    available_actions.append(Action(pos, 2, 1))
                if pos[0] != self.height - 1 and pos[1] != self.width - 1 and (pos[0] + 1, pos[1] + 1) not in self.black_positions:
                    available_actions.append(Action(pos, 3, 1))

        elif self.turn == 2:
            for pos in sorted(self.white_positions, key=lambda p: (p[0], p[1])):
                # ======Caution!======
                if pos[0] != 0 and pos[1] != 0 and (pos[0] - 1, pos[1] - 1) not in self.white_positions:
                    available_actions.append(Action(pos, 1, 2))
                if pos[0] != 0 and (pos[0] - 1, pos[1]) not in self.black_positions and (pos[0] - 1, pos[1]) not in self.white_positions:
                    available_actions.append(Action(pos, 2, 2))
                if pos[0] != 0 and pos[1] != self.width - 1 and (pos[0] - 1, pos[1] + 1) not in self.white_positions:
                    available_actions.append(Action(pos, 3, 2))

        return available_actions

    def getMatrix(self):
        matrix = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for item in self.black_positions:
            matrix[item[0]][item[1]] = 1
        for item in self.white_positions:
            matrix[item[0]][item[1]] = 2
        return matrix
    
# extend State to define the components needed for 1.1
class breakthrough_state(State):
    # override the transfer function to work with new state
    def transfer(self, action):
        black_pos = list(self.black_positions)
        white_pos = list(self.white_positions)

        # black move
        if action.turn == 1:
            if action.coordinate in self.black_positions:
                index = black_pos.index(action.coordinate)
                new_pos = single_move(action.coordinate, action.direction, action.turn)
                black_pos[index] = new_pos
                if new_pos in self.white_positions:
                    white_pos.remove(new_pos)
            else:
                print("Invalid action!")

        # white move
        elif action.turn == 2:
            if action.coordinate in self.white_positions:
                index = white_pos.index(action.coordinate)
                new_pos = single_move(action.coordinate, action.direction, action.turn)
                white_pos[index] = new_pos
                if new_pos in self.black_positions:
                    black_pos.remove(new_pos)
            else:
                print("Invalid action!")

        state = breakthrough_state(black_position=black_pos, white_position=white_pos, black_num=self.black_num, white_num=self.white_num, turn=alterturn(action.turn), function=self.function, height=self.height, width=self.width, type=self.type)
        return state

    # new goal check, good for 3 worker game and classic game
    def isgoalstate(self):
        if self.type == 0:
            if 0 in [item[0] for item in self.white_positions] or len(self.black_positions) == 0:
                return 2
            if self.height - 1 in [item[0] for item in self.black_positions] or len(self.white_positions) == 0:
                return 1
            return 0
        elif self.type == 1:
            if sum(1 for x in self.white_positions if x[0] == 0) >= 3 or len(self.black_positions) < 3:
                return 2
            last_row = self.height - 1
            if sum(1 for x in self.black_positions if x[0] == last_row) >= 3 or len(self.white_positions) < 3:
                return 1
            return 0
    
    # new utility and leaf evaluation functions
    def utility(self, turn):
        if self.function == 0:
            return 0
        elif self.function == 1:
            return self.defensive_heuristic_one(turn)
        elif self.function == 2:
            return self.offensive_heuristic_one(turn)
        elif self.function == 3:
            return self.defensive_heuristic_two(turn)
        elif self.function == 4:
            return self.offensive_heuristic_two(turn)
    
    # given -> 2 * (# own pieces) + random()
    def defensive_heuristic_one(self, turn):
        if turn == 1:
            return 2 * len(self.black_positions) + random.random()
        else:
            return 2 * len(self.white_positions) + random.random()

    # given -> 2 * (30 - # of opp pieces) + random()
    def offensive_heuristic_one(self, turn):
        if turn == 1:
            return 2 * (30 - len(self.white_positions)) + random.random()
        else:
            return 2 * (30 - len(self.black_positions)) + random.random()
        
    # beat offensive heuristic one
    def defensive_heuristic_two(self, turn):
        if turn == 1:
            our_pieces = len(self.black_positions) ** 2
            capture_award = (self.width - len(self.white_positions))
            lethargy_penalty = sum([(self.height - 1 - item[0]) ** 2 for item in self.black_positions])
            oppoent_advancement_penalty = sum([(self.height - 1 - item[0]) ** 2 for item in self.white_positions])
            return 2 * our_pieces + capture_award - 0.5 * lethargy_penalty - 0.5 * oppoent_advancement_penalty
        else:
            our_pieces = len(self.white_positions) ** 2
            capture_award = (self.width - len(self.black_positions))
            lethargy_penalty = sum([(item[0]) ** 2 for item in self.white_positions])
            oppoent_advancement_penalty = sum([(item[0]) ** 2 for item in self.black_positions])
            return 2 * our_pieces + capture_award - 0.5 * lethargy_penalty - 0.5 * oppoent_advancement_penalty

    # beat defensive heuristic one
    def offensive_heuristic_two(self, turn):
        if turn == 1:
            advancement_value = sum([item[0] ** 2 for item in self.black_positions]) # prioritize moving pieces far up on the board
            loss_penalty = (self.width - len(self.black_positions)) ** 2 # harshly penalize losing many pieces
            return 2 * (30 - len(self.white_positions)) + advancement_value - 2 * loss_penalty
        else:
            advancement_value = sum([self.height - 1 - item[0] for item in self.white_positions]) # prioritize moving pieces far down on the board
            loss_penalty = (self.width - len(self.white_positions)) ** 2 # harshly penalize losing many pieces (penalty ramps up as pieces are lost)
            return 2 * (30 - len(self.black_positions)) + advancement_value - 2 * loss_penalty
