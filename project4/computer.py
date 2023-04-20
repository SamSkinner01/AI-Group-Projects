import copy

class Minimax:
    def __init__(self, board, current_player):
        # Initialize the current state, passed in as a parameter in the game
        self.board = board
        self.current_player = current_player

    def is_game_over(self, board):
        """
        Check if game is in a terminal state
        """
        
        # Check if there is a winner
        win_conditions = [
            # Horizontal
            [board[0][0], board[0][1], board[0][2]],
            [board[1][0], board[1][1], board[1][2]],
            [board[2][0], board[2][1], board[2][2]],
            # Vertical
            [board[0][0], board[1][0], board[2][0]],
            [board[0][1], board[1][1], board[2][1]],
            [board[0][2], board[1][2], board[2][2]],
            # Diagonal
            [board[0][0], board[1][1], board[2][2]],
            [board[0][2], board[1][1], board[2][0]]
        ]

        for condition in win_conditions:
            if condition[0] == condition[1] == condition[2] != '-':
                return -1 if condition[0] == 'X' else 1
        
        # Check if there is a tie
        ct = 0
        for row in  board:
            for col in row:
                if col == '-':
                    ct += 1
        if ct == 0:
            return 0
        
        # Not terminal state
        return -2

    def get_move(self):
        """
        Returns the best move for the current player
        """
        value, row, col = self.max(self.board, float('-inf'), float('inf'))
        return row, col
        
    def max(self, board, alpha, beta):
        # Check terminal state
        if self.is_game_over(board) <= 1 and self.is_game_over(board) >= -1:
            return self.is_game_over(board), None, None

        v = float('-inf')

        move_row = None
        move_col = None

        for row in range(3):
            for col in range(3):
                
                if board[row][col] == '-':
                    send_board = copy.deepcopy(board)
                    send_board[row][col] = 'O'
                    v2, r, c = self.min(send_board, alpha, beta)
                    del send_board
                    if v2 > v:
                        v = v2
                        move_row = row
                        move_col = col
                        alpha = max(alpha, v)
                    if v >= beta:
                        return v, move_row, move_col
        return v, move_row, move_col

    def min(self, board, alpha, beta):
        # Check terminal state
        if self.is_game_over(board) <= 1 and self.is_game_over(board) >= -1:
            return self.is_game_over(board), None, None

        v = float('inf')

        move_row = None
        move_col = None

        for row in range(3):
            for col in range(3):
                if board[row][col] == '-':
                    send_board = copy.deepcopy(board)
                    send_board[row][col] = 'X'
                    v2, r2, c2 = self.max(send_board, alpha, beta)
                    del send_board
                    if v2 < v:
                        v = v2
                        move_row = row
                        move_col = col
                        beta = min(beta, v)
                    if v <= alpha:
                        return v, move_row, move_col
        return v, move_row, move_col
