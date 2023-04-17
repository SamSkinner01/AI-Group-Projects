class TicTacToe:
    def __init__(self):
        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        self.play()

    def print_board(self):
        for row in self.board:
            print(row)

    def get_move(self):
        row = int(input("Enter row: "))
        col = int(input("Enter column: "))
        return row, col

    def make_move(self, row, col):
        if self.board[row][col] == '-' and self.player == 'X':
            self.board[row][col] = 'X'
            return True
        elif self.board[row][col] == '-' and self.player == 'O':    
            self.board[row][col] = 'O'
            return True
        else:
            print("Invalid move")
            return False
        
    def check_win(self):
        winning_combos = [
            [self.board[0][0], self.board[0][1], self.board[0][2]],
            [self.board[1][0], self.board[1][1], self.board[1][2]],
            [self.board[2][0], self.board[2][1], self.board[2][2]],
            [self.board[0][0], self.board[1][0], self.board[2][0]],
            [self.board[0][1], self.board[1][1], self.board[2][1]],
            [self.board[0][2], self.board[1][2], self.board[2][2]],
            [self.board[0][0], self.board[1][1], self.board[2][2]],
            [self.board[0][2], self.board[1][1], self.board[2][0]]
        ]
        for combo in winning_combos:
            if combo == ['X', 'X', 'X']:
                return -1
            if combo == ['O', 'O', 'O']:
                return 1
        return False
    
    def check_tie(self):
        for row in self.board:
            for col in row:
                if col == '-':
                    return False
        return True


    def switch_player(self):
        if self.player == 'X':
            self.player = 'O'
        else:
            self.player = 'X'
    
    def play(self):
        self.player = 'X'
        while True:
            print('----------------')
            if self.player == 'X':
                print("Player X's turn")
            else:
                print("Player O's turn")
            self.print_board()
            if self.player == 'X':
                row, col = self.get_move()
            else:
                row, col = self.get_cpu_move() 
            if self.make_move(row, col):
                if self.check_win():
                    print("Player {} wins!".format(self.player))
                    break
                if self.check_tie():
                    print("Tie!")
                    break
                self.switch_player()
        self.print_board()

    def get_cpu_move(self):
        value, row, col = self.max(float('-inf'), float('inf'))
        print(value)
        return row, col
    
    def terminal(self):
        if self.check_win() or self.check_tie():
            if self.check_win() == -1:
                return -10
            elif self.check_win() == 1:
                return 10
            else:
                return 0
        else:
            return False
    
    def max(self, alpha, beta):
        # Checking the terminal states
        is_terminal = self.terminal()
        if is_terminal:
            return is_terminal, None, None
        
        # Define value v
        v = float('-inf')
        move_row, move_col = None, None

        # For every action possible
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '-':
                    # Make move
                    self.board[row][col] = 'O'
                    # Get the value of the move
                    value, _, _ = self.min(alpha, beta)
                    # Undo the move
                    self.board[row][col] = '-'
                    # If the value is greater than v, update v
                    if value > v:
                        v, move_row, move_col = value, row, col
                    alpha = max(alpha, v)
                    if v >= beta:
                        print(v)
                        return v, move_row, move_col
        return v, move_row, move_col

    

    def min(self, alpha, beta):
        # Checking the terminal states
        is_terminal = self.terminal()
        if is_terminal:
            return is_terminal, None, None
        
        # Define value v
        v = float('inf')
        move_row, move_col = None, None

        # For every action possible
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '-':
                    # Make move
                    self.board[row][col] = 'O'

                    # Get the value of the move
                    value, _, _ = self.min(alpha, beta)
                    # Undo the move
                    self.board[row][col] = '-'
                    # If the value is greater than v, update v
                    if value < v:
                        v, move_row, move_col = value, row, col
                    beta = max(beta, v)
                    if v <= alpha:
                        #print(v)
                        return v, move_row, move_col
        return v, move_row, move_col