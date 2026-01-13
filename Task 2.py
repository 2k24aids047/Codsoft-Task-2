# tic_tac_toe_ai.py
import math
import random

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # 3x3 board
        self.current_winner = None
    
    def print_board(self):
        print("\n")
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
        print("\n")
    
    def print_board_nums(self):
        # Shows which number corresponds to which box
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')
    
    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    
    def empty_squares(self):
        return ' ' in self.board
    
    def num_empty_squares(self):
        return self.board.count(' ')
    
    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False
    
    def winner(self, square, letter):
        # Check row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        
        # Check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        
        # Check diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        
        return False

class AI:
    def __init__(self, letter):
        self.letter = letter
        self.human_letter = 'O' if letter == 'X' else 'X'
    
    def get_move(self, game):
        if len(game.available_moves()) == 9:
            # First move - choose random corner
            square = random.choice([0, 2, 6, 8])
        else:
            # Use minimax algorithm
            square = self.minimax(game, self.letter)['position']
        return square
    
    def minimax(self, state, player, alpha=-math.inf, beta=math.inf):
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'
        
        # Base cases
        if state.current_winner == other_player:
            return {
                'position': None,
                'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player 
                        else -1 * (state.num_empty_squares() + 1)
            }
        elif not state.empty_squares():
            return {'position': None, 'score': 0}
        
        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}
        
        for possible_move in state.available_moves():
            # Try the move
            state.make_move(possible_move, player)
            
            # Simulate game after making that move
            sim_score = self.minimax(state, other_player, alpha, beta)
            
            # Undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move
            
            # Update best score
            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
                alpha = max(alpha, best['score'])
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
                beta = min(beta, best['score'])
            
            # Alpha-beta pruning
            if beta <= alpha:
                break
        
        return best

def play_game():
    print("\n=== TIC-TAC-TOE AI ===\n")
    print("Positions on the board:")
    
    game = TicTacToe()
    game.print_board_nums()
    
    # Let human choose X or O
    human_letter = ''
    while human_letter not in ['X', 'O']:
        human_letter = input("Choose X or O: ").upper()
    
    ai_letter = 'O' if human_letter == 'X' else 'X'
    ai = AI(ai_letter)
    
    # Determine who goes first
    current_player = 'X' if random.random() < 0.5 else 'O'
    print(f"\n{current_player} goes first!\n")
    
    while game.empty_squares():
        if current_player == human_letter:
            # Human's turn
            game.print_board()
            valid_square = False
            
            while not valid_square:
                try:
                    square = int(input(f"Enter your move (0-8) for {human_letter}: "))
                    if square not in game.available_moves():
                        raise ValueError
                    valid_square = True
                except ValueError:
                    print("Invalid square. Try again.")
            
            game.make_move(square, human_letter)
        
        else:
            # AI's turn
            square = ai.get_move(game)
            game.make_move(square, ai_letter)
            print(f"AI ({ai_letter}) plays at position {square}")
        
        # Check for winner
        if game.current_winner:
            game.print_board()
            if game.current_winner == human_letter:
                print("Congratulations! You win! 🎉")
            else:
                print("AI wins! Better luck next time! 🤖")
            break
        
        # Switch player
        current_player = human_letter if current_player == ai_letter else ai_letter
    
    if not game.current_winner:
        game.print_board()
        print("It's a tie! 🤝")

if __name__ == "__main__":
    while True:
        play_game()
        play_again = input("\nPlay again? (y/n): ").lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break