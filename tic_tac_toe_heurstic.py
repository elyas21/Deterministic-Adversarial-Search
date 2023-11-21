
class Game:
    def __init__(self):
        self.board = {1: ' ', 2: ' ', 3: ' ',
                      4: ' ', 5: ' ', 6: ' ',
                      7: ' ', 8: ' ', 9: ' '}
        self.tic_tac_toe = TicTacToe(self.board)
        self.human_player = HumanPlayer('O', self.tic_tac_toe)
        self.ai_player = AIPlayer('X', self.tic_tac_toe)

    def run(self):
        print("Computer goes first! Good luck.")
        print("Positions are as follow:")
        print("1, 2, 3 ")
        print("4, 5, 6 ")
        print("7, 8, 9 ")
        print("\n")

        while not self.tic_tac_toe.check_for_win():
            self.ai_player.make_move()
            self.human_player.make_move()


class TicTacToe:
    def __init__(self, board):
        self.board = board

    def print_board(self):
        print(self.board[1] + '|' + self.board[2] + '|' + self.board[3])
        print('-+-+-')
        print(self.board[4] + '|' + self.board[5] + '|' + self.board[6])
        print('-+-+-')
        print(self.board[7] + '|' + self.board[8] + '|' + self.board[9])
        print("\n")

    def space_is_free(self, position):
        return self.board[position] == ' '

    def insert_letter(self, letter, position):
        if self.space_is_free(position):
            self.board[position] = letter
            self.print_board()
            if self.check_for_win():
                if letter == 'X':
                    print("Bot wins!")
                else:
                    print("Player wins!")
                exit()
            if self.check_draw():
                print("Draw!")
                exit()
        else:
            print("Can't insert there!")
            position = int(input("Please enter new position:  "))
            self.insert_letter(letter, position)

    def check_for_win(self):

        if (self.board[1] == self.board[2] and self.board[1] == self.board[3] and self.board[1] != ' '):
            return True
        elif (self.board[4] == self.board[5] and self.board[4] == self.board[6] and self.board[4] != ' '):
            return True
        elif (self.board[7] == self.board[8] and self.board[7] == self.board[9] and self.board[7] != ' '):
            return True
        elif (self.board[1] == self.board[4] and self.board[1] == self.board[7] and self.board[1] != ' '):
            return True
        elif (self.board[2] == self.board[5] and self.board[2] == self.board[8] and self.board[2] != ' '):
            return True
        elif (self.board[3] == self.board[6] and self.board[3] == self.board[9] and self.board[3] != ' '):
            return True
        elif (self.board[1] == self.board[5] and self.board[1] == self.board[9] and self.board[1] != ' '):
            return True
        elif (self.board[7] == self.board[5] and self.board[7] == self.board[3] and self.board[7] != ' '):
            return True
        else:
            return False

    def checkWhichMarkWon(self, mark):
        if self.board[1] == self.board[2] and self.board[1] == self.board[3] and self.board[1] == mark:
            return True
        elif (self.board[4] == self.board[5] and self.board[4] == self.board[6] and self.board[4] == mark):
            return True
        elif (self.board[7] == self.board[8] and self.board[7] == self.board[9] and self.board[7] == mark):
            return True
        elif (self.board[1] == self.board[4] and self.board[1] == self.board[7] and self.board[1] == mark):
            return True
        elif (self.board[2] == self.board[5] and self.board[2] == self.board[8] and self.board[2] == mark):
            return True
        elif (self.board[3] == self.board[6] and self.board[3] == self.board[9] and self.board[3] == mark):
            return True
        elif (self.board[1] == self.board[5] and self.board[1] == self.board[9] and self.board[1] == mark):
            return True
        elif (self.board[7] == self.board[5] and self.board[7] == self.board[3] and self.board[7] == mark):
            return True
        else:
            return False

    def check_draw(self):
        for key in self.board.keys():
            if self.board[key] == ' ':
                return False
        return True


class HumanPlayer:
    def __init__(self, letter, tic_tac_toe):
        self.letter = letter
        self.tic_tac_toe = tic_tac_toe

    def make_move(self):
        position = int(input(f"Enter the position for '{self.letter}':  "))
        self.tic_tac_toe.insert_letter(self.letter, position)


class AIPlayer:
    def __init__(self, letter, tic_tac_toe):
        self.letter = letter
        self.symbol = letter  # Add this line to set the symbol
        self.tic_tac_toe = tic_tac_toe
        self.nodes_visited = 0  # Initialize the node count

    def heuristic(self, tic_tac_toe):
        # Check for AI win
        if tic_tac_toe.checkWhichMarkWon(self.symbol):
            return 10
        # Check for opponent (human) win
        elif tic_tac_toe.checkWhichMarkWon('O' if self.symbol == 'X' else 'X'):
            return -10
        else:
            score = 0
            # Check for two in a row for AI
            score += self.evaluate_line(tic_tac_toe, self.symbol)
            # Check for two in a row for opponent
            score += self.evaluate_line(tic_tac_toe,
                                        'O' if self.symbol == 'X' else 'X')
            return score

    def evaluate_line(self, tic_tac_toe, mark):
        score = 0
        # Check rows
        for row in range(1, 8, 3):
            if tic_tac_toe.board[row] == tic_tac_toe.board[row + 1] == mark and tic_tac_toe.space_is_free(row + 2):
                score += 5
            elif tic_tac_toe.board[row] == tic_tac_toe.board[row + 2] == mark and tic_tac_toe.space_is_free(row + 1):
                score += 5
            elif tic_tac_toe.board[row + 1] == tic_tac_toe.board[row + 2] == mark and tic_tac_toe.space_is_free(row):
                score += 5

        # Check columns
        for col in range(1, 4):
            if tic_tac_toe.board[col] == tic_tac_toe.board[col + 3] == mark and tic_tac_toe.space_is_free(col + 6):
                score += 5
            elif tic_tac_toe.board[col] == tic_tac_toe.board[col + 6] == mark and tic_tac_toe.space_is_free(col + 3):
                score += 5
            elif tic_tac_toe.board[col + 3] == tic_tac_toe.board[col + 6] == mark and tic_tac_toe.space_is_free(col):
                score += 5

        # Check diagonals
        if tic_tac_toe.board[1] == tic_tac_toe.board[5] == mark and tic_tac_toe.space_is_free(9):
            score += 5
        elif tic_tac_toe.board[1] == tic_tac_toe.board[9] == mark and tic_tac_toe.space_is_free(5):
            score += 5
        elif tic_tac_toe.board[5] == tic_tac_toe.board[9] == mark and tic_tac_toe.space_is_free(1):
            score += 5

        if tic_tac_toe.board[3] == tic_tac_toe.board[5] == mark and tic_tac_toe.space_is_free(7):
            score += 5
        elif tic_tac_toe.board[3] == tic_tac_toe.board[7] == mark and tic_tac_toe.space_is_free(5):
            score += 5
        elif tic_tac_toe.board[5] == tic_tac_toe.board[7] == mark and tic_tac_toe.space_is_free(3):
            score += 5

        return score

    def make_move(self):
        best_score = -800
        best_move = 0
        self.nodes_visited = 0  # Reset node count before each move

        for key in self.tic_tac_toe.board.keys():
            if self.tic_tac_toe.space_is_free(key):
                self.tic_tac_toe.board[key] = self.letter
                score = self.minimax(self.tic_tac_toe.board, 0, 0, False)
                self.tic_tac_toe.board[key] = ' '

                if score > best_score:
                    best_score = score
                    best_move = key

        self.tic_tac_toe.insert_letter(self.letter, best_move)
        print(f"Nodes visited: {self.nodes_visited}")
        print(f'score          {score} ')

    def minimax(self, board, depth, bestScore, is_maximizing):
        tic_tac_toe = TicTacToe(board)
        tic_tac_toe.board = board
        self.nodes_visited += 1

        if tic_tac_toe.checkWhichMarkWon(self.symbol):
            return 1
        elif tic_tac_toe.checkWhichMarkWon('O' if self.symbol == 'X' else 'X'):
            return -1
        elif tic_tac_toe.check_draw():
            return 0

        if is_maximizing:
            best_score = -10000
            for key in tic_tac_toe.board.keys():
                if tic_tac_toe.space_is_free(key):
                    tic_tac_toe.board[key] = self.symbol
                    score = self.minimax(
                        tic_tac_toe.board, depth + 1, bestScore, False)
                    tic_tac_toe.board[key] = ' '
                    score += self.heuristic(tic_tac_toe)  # Add heuristic score
                    print(f'score max                  {score}')
                    if score > best_score:
                        best_score = score

                    if bestScore < score:
                        break
                    else:
                        bestScore = score
            return best_score

        else:
            best_score = 10000
            for key in tic_tac_toe.board.keys():
                if tic_tac_toe.space_is_free(key):
                    tic_tac_toe.board[key] = 'O' if self.symbol == 'X' else 'X'
                    score = self.minimax(
                        tic_tac_toe.board, depth + 1, bestScore, True)
                    tic_tac_toe.board[key] = ' '
                    score += self.heuristic(tic_tac_toe)  # Add heuristic score
                    print(f'score max                  {score}')

                    if score < best_score:
                        best_score = score

            return best_score


if __name__ == "__main__":
    game = Game()
    game.run()
