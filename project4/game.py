from computer import Minimax

class TicTacToe:
    def __init__(self):
        # Will store the current state
        # of the board
        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        
        # Will store the current player
        self.current_player = 'X'

    def print_board(self, board):
        """
        Prints the board
        """
        for row in board:
            print(row)

    def get_users_move(self):
        """
        Gets the users move
        """
        while True:
            row = int(input('Enter row: '))
            col = int(input('Enter col: '))
            if self.is_valid_move(row, col, self.board):
                break
        return row, col
    
    def get_computers_move(self):
        """
        Gets the computers move
        """
        computer = Minimax(self.board, self.current_player)
        move = computer.get_move()
        return move
    
    def is_valid_move(self, row, col, board):
        """
        Checks if the move is valid
        """
        return board[row][col] == '-'
    
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
    
    def play(self):
        """
        Plays the game
        """
        while True:
            # Print the board
            self.print_board(self.board)
            
            # Get the users move
            row, col = self.get_users_move()
            
            # Update the board
            self.board[row][col] = 'X'

            #self.print_board(self.board)
            
            # Check if the game is over
            if self.is_game_over(self.board) == 1 or self.is_game_over(self.board) == -1 or self.is_game_over(self.board) == 0:
                self.print_board(self.board)
                print('Game over')
                break
            
            
            # Get the computers move
            row, col = self.get_computers_move()
            
            # Update the board
            self.board[row][col] = 'O'
            
            # Check if the game is over
            if self.is_game_over(self.board) == 1 or self.is_game_over(self.board) == -1 or self.is_game_over(self.board) == 0:
                self.print_board(self.board)
                print('Game over')
                break