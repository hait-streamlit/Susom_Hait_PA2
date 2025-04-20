import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import time, copy

from components.model import eight_by_eight, five_by_ten
from components.agent import Agent

class GUI:
    def __init__(self):
        self.init_board()
        self.animation_speed = 0.3
    
    def init_board(self):
        fig, ax = plt.subplots(1, 1)
        ax.set_aspect('equal')

        plt.grid(True, color='black')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.tick_params(tick1On=False)

        fig.set_facecolor('none')
        ax.set_facecolor('none')

        self.fig = fig
        self.ax = ax

    def draw_square(self, x, y, size, color):
        rect = patches.Rectangle((x, y), size, size, linewidth=0, edgecolor=color, facecolor=color, zorder=1)
        self.ax.add_patch(rect)
    
    def draw_circle(self, x, y, size, color):
        circle = patches.Circle((x, y), size, linewidth=0, edgecolor=color, facecolor=color, zorder=1)
        self.ax.add_patch(circle)

    def update_fig(self, rows, cols, matrix):
        self.ax.clear()
        self.ax.set_xticks(np.arange(cols + 1))
        self.ax.set_yticks(np.arange(rows + 1))
        self.ax.set_xlim(0, cols)
        self.ax.set_ylim(0, rows)

        # add the board coordinates
        self.ax.set_xticks(np.arange(cols) + 0.5)
        self.ax.set_yticks(np.arange(rows) + 0.5)
        self.ax.set_xticklabels([str(i) for i in range(1, cols + 1)])
        self.ax.set_yticklabels([chr(i + 97) for i in range(rows)])
        self.ax.tick_params(axis='both', colors='white')

        for i in range(rows):
            for j in range(cols):
                color = '#eab676' if (i+j) % 2 == 0 else '#873e23'
                self.draw_square(j, i, 1, color)

                if matrix[i][j] == 1:
                    self.draw_circle(j + 0.5, i + 0.5, 0.3, 'black')
                elif matrix[i][j] == 2:
                    self.draw_circle(j + 0.5, i + 0.5, 0.3, 'white')

    def fetch_board_data(self):
        if st.session_state.part == "Part 1.1":
            self.update_fig(8, 8, eight_by_eight)
        elif st.session_state.part == "Part 1.2":
            if "type" not in st.session_state:
                st.session_state.type = "5x10 Board"

            if st.session_state.type == "5x10 Board":
                self.update_fig(5, 10, five_by_ten)
            else:
                self.update_fig(8, 8, eight_by_eight)

    def flip_turn(self, turn):
        return 2 if turn == 1 else 1
    
    def select_functions(self):
        match st.session_state.game:
            case "MM O1 vs AB O1":
                return 2, 2
            case "AB O2 vs AB D1":
                return 4, 1
            case "AB D2 vs AB O1":
                return 3, 2
            case "AB O2 vs AB O1":
                return 4, 2
            case "AB D2 vs AB D1":
                return 3, 1
            case "AB O2 vs AB D2":
                return 4, 3

    # run the search and store the data so it can be animated
    def play_selected(self):
        self.black_expanded = 0
        self.white_expanded = 0

        self.black_move_time = 0
        self.white_move_time = 0

        self.black_move_count = 0
        self.white_move_count = 0
        
        if st.session_state.part == "Part 1.1" or st.session_state.part == "Part 1.2":
            current_board = copy.deepcopy(eight_by_eight)
            game_type = 0
            if st.session_state.part == "Part 1.2":
                if st.session_state.type == "5x10 Board":
                    current_board = copy.deepcopy(five_by_ten)
                elif st.session_state.type == "3 Worker Game":
                    game_type = 1
            turn = 1

            black_function, white_function = self.select_functions()
            
            while True:
                start_time = time.time()
                if turn == 1:
                    if st.session_state.game == "MM O1 vs AB O1":
                        board, nodes, piece = Agent(
                            boardmatrix=current_board, 
                            turn=turn, depth=3, 
                            function=black_function, 
                            is_alpha_beta=False, 
                            type=game_type
                        ).decision()

                        current_board = board.getMatrix()
                        self.black_expanded += nodes
                        self.black_move_count += 1
                        self.black_move_time += time.time() - start_time
                    else:
                        board, nodes, piece = Agent(
                            boardmatrix=current_board, 
                            turn=turn, depth=5, 
                            function=black_function, 
                            is_alpha_beta=True, 
                            type=game_type
                        ).decision()

                        current_board = board.getMatrix()
                        self.black_expanded += nodes
                        self.black_move_count += 1
                        self.black_move_time += time.time() - start_time
                else:
                    board, nodes, piece = Agent(
                        boardmatrix=current_board, 
                        turn=turn, depth=5, 
                        function=white_function, 
                        is_alpha_beta=True, 
                        type=game_type
                    ).decision()

                    current_board = board.getMatrix()
                    self.white_expanded += nodes
                    self.white_move_count += 1
                    self.white_move_time += time.time() - start_time
                    
                if st.session_state.part == "Part 1.2" and st.session_state.type == "5x10 Board":
                    self.update_fig(5, 10, current_board)
                else:
                    self.update_fig(8, 8, current_board)

                self.board.pyplot(self.fig)
                time.sleep(self.animation_speed)

                if board.isgoalstate() != 0:
                    self.load_final_statistics("Black" if turn == 1 else "White", board)
                    break
                turn = self.flip_turn(turn)
            

    def load_final_statistics(self, winner, winning_board):
        with st.expander(f":green[{winner} Won in a {(self.black_move_time + self.white_move_time):.2f} second game with {self.black_move_count + self.white_move_count} total moves]"):
            st.write(f"Black Moves: {self.black_move_count}")
            st.write(f"Black Nodes Expanded: {self.black_expanded}")
            st.write(f"Black Average Expansion Per Move: {(self.black_expanded / self.black_move_count):.2f}")
            st.write(f"Black Average Move Time: {(self.black_move_time / self.black_move_count):.2f} seconds")
            st.write(f"Black Captured: {winning_board.width * 2 - winning_board.white_num}")

            st.divider()
            
            st.write(f"White Moves: {self.white_move_count}")
            st.write(f"White Nodes Expanded: {self.white_expanded}")
            st.write(f"White Average Expansion Per Move: {(self.white_expanded / self.white_move_count):.2f}")
            st.write(f"White Average Move Time: {(self.white_move_time / self.white_move_count):.2f} seconds")
            st.write(f"White Captured: {winning_board.height * 2 - winning_board.black_num}")
    
    def run(self):
        st.title("PA2 - Game")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            self.part = st.selectbox("Select assignment part", ["Part 1.1", "Part 1.2"], on_change=self.fetch_board_data, key="part")
        with col2:
            match st.session_state.part:
                case "Part 1.1":
                    self.game = st.selectbox("Select a game", [
                        "MM O1 vs AB O1", 
                        "AB O2 vs AB D1",
                        "AB D2 vs AB O1",
                        "AB O2 vs AB O1",
                        "AB D2 vs AB D1",
                        "AB O2 vs AB D2",
                    ], key="game")
                case "Part 1.2":
                    self.game = st.selectbox("Select a game", [
                        "MM O1 vs AB O1", 
                        "AB O2 vs AB D1",
                        "AB D2 vs AB O1",
                        "AB O2 vs AB O1",
                        "AB D2 vs AB D1",
                        "AB O2 vs AB D2",
                    ], key="game")
        with col3:
            match st.session_state.part:
                case "Part 1.2":
                    self.type = st.selectbox("Select type", ["5x10 Board", "3 Worker Game"], on_change=self.fetch_board_data, key="type")

        self.fetch_board_data()
        self.board = st.pyplot(self.fig)

        self.status = st.empty()
        if st.button("Play"):
            self.play_selected()
            try:
                pass
            except Exception as e:
                st.warning(f"No solution found for {st.session_state.game} on {st.session_state.maze} maze")
            
        
        