import math, copy
import numpy as np

def greedy_decision(board):
    # choose a greedy move
    def return_moves(current_board):
        # determine if a move is legal -> in bounds and no pieces in the way
        def is_legal(y, x):
            if x < 0 or x > 7 or y < 0 or y > 7:
                return False

            if (current_board[y][x] == 1):
                return False
            return True

        pieces = []
        for i in range(len(current_board)):
            for j in range(len(current_board[i])):
                if current_board[i][j] == 1:
                    pieces.append((i, j))

        pieces = sorted(pieces, key=lambda x: (x[0], x[1]), reverse=True)
        print(pieces)

        best_board = None
        for piece in pieces:
            possible_moves = [piece[1] - 1, piece[1], piece[1] + 1]
            new_y = piece[0] + 1

            for new_x in possible_moves:
                if is_legal(new_y, new_x):
                    best_board = copy.deepcopy(current_board)
                    best_board[piece[0]][piece[1]] = 0
                    best_board[new_y][new_x] = 1

                    if current_board[new_y][new_x] == 2 and new_x != piece[1]:
                        return best_board
        return best_board
    
    def game_complete(current_board):
        return 1 in current_board[7] or sum(line.count(2) for line in current_board) == 0
  
    return_board = return_moves(board)
    return return_board, game_complete(return_board)

def format_print(board):
  for line in board:
      print(line)

if __name__ == "__main__":
    eight_by_eight = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2],
    ]

    board, game_over = greedy_decision(eight_by_eight)
    format_print(board)