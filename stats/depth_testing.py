
# measure the best depth within 10 seconds over 10 rounds
# best depth within 10 seconds over 10 rounds ~ 5

import time, math, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from components.model import *
from components.agent import Agent

def make_random_board():
  # split the board in half
  b_half = [1] * 16 + [0] * 16
  w_half = [2] * 16 + [0] * 16

  # scatter the respective pieces throughout each half
  random.shuffle(b_half)
  random.shuffle(w_half)
  full_board = b_half + w_half # combine the halves

  # arrange as a 8x8 matrix and return
  return [full_board[i*8:(i+1)*8] for i in range(8)]

time_limit = 10 # define 10 sec. as an acceptable wait time to make a move
average = 0
for trial in range(10): # average 10 trials using random board configurations
  test_depth = 1
  random_board = make_random_board()

  while True:
    start = time.time()
    board, nodes, piece = Agent(boardmatrix=random_board, turn=1, depth=test_depth, function=2, is_alpha_beta=True, use_memoization=False, type=0).decision()
    end = time.time()

    if end - start > time_limit: # iterate until it takes longer than 10 sec. to make a move
      print(f'trial {trial + 1} depth: {test_depth - 1}')
      average += test_depth - 1
      break
    else:
      test_depth += 1
print(f'average alpha-beta max: {math.floor(average/10)}')