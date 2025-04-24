# statistic for AB Defensive 2 vs AB Offensive 1
# black won 90% of the time over 20 rounds

import sys, os, multiprocessing, copy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from components.model import *
from components.agent import Agent

def play_single_round(round_index):
    current_board = copy.deepcopy(eight_by_eight)
    turn = 1
    b_nodes = 0
    w_nodes = 0

    while True:
        if turn == 1:
            board, nodes, piece = Agent(boardmatrix=current_board, turn=turn, depth=5, function=3, is_alpha_beta=True, type=0).decision()
            current_board = board.getMatrix()
            b_nodes += nodes
        else:
            board, nodes, piece = Agent(boardmatrix=current_board, turn=turn, depth=5, function=2, is_alpha_beta=True, type=0).decision()
            current_board = board.getMatrix()
            w_nodes += nodes

        if board.isgoalstate() != 0:
            winner = "black" if turn == 1 else "white"
            print(f'round {round_index + 1}')
            print(f'{winner} won')
            print(f'black expanded {b_nodes} - white expanded {w_nodes}\n')
            return winner
        turn = 2 if turn == 1 else 1

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
