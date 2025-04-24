# statistic for AB Offensive 1 vs AB Defensive 1
# over 20 rounds, greedy won 0% of the time

import sys, os, multiprocessing, copy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from components.model import *
from components.agent import Agent
from components.greedy import greedy_decision

def play_single_round(round_index):
    current_board = copy.deepcopy(eight_by_eight)
    turn = 1
    b_nodes = 0
    w_nodes = 0

    while True:
        board, game_over = greedy_decision(current_board)
        current_board = board
        
        if game_over:
            print(f'round {round_index + 1}')
            print('Black Won')
            return "black"

        board, nodes, piece = Agent(boardmatrix=current_board, turn=2, depth=5, function=3, is_alpha_beta=True, type=0).decision()
        current_board = board.getMatrix()
        w_nodes += nodes

        if board.isgoalstate() != 0:
            print(f'round {round_index + 1}')
            print('White Won')
            return "white"

def main():
    rounds = 20
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(play_single_round, range(rounds))

    black_wins = results.count("black")
    white_wins = results.count("white")
    
    print(f'black winrate: {black_wins / rounds * 100}%')
    print(f'white winrate: {white_wins / rounds * 100}%')

if __name__ == '__main__':
    main()
