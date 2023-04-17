import random

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
                return True
            if combo == ['O', 'O', 'O']:
                return True
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

    def get_cpu_move(self):
        while True:
            row = random.randint(0, 2)
            col = random.randint(0, 2)
            if self.board[row][col] == '-':
                return row, col
            
