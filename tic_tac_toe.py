
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
            if self.check_draw():
                print("Draw!")
                exit()
            if self.check_for_win():
                if letter == 'X':
                    print("Bot wins!")
                else:
                    print("Player wins!")
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

    def checkWhichMarkWon(self,mark):
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

    def make_move(self):
        best_score = -800
        best_move = 0
        self.nodes_visited = 0  # Reset node count before each move

        for key in self.tic_tac_toe.board.keys():
            if self.tic_tac_toe.space_is_free(key):
                self.tic_tac_toe.board[key] = self.letter
                score = self.minimax(self.tic_tac_toe.board, 0, False)
                self.tic_tac_toe.board[key] = ' '
                if score > best_score:
                    best_score = score
                    best_move = key

        self.tic_tac_toe.insert_letter(self.letter, best_move)
        print(f"Nodes visited: {self.nodes_visited}")


    def minimax(self, board, depth, is_maximizing):
        self.nodes_visited += 1

        tic_tac_toe = TicTacToe(board)
        tic_tac_toe.board = board

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
                    score = self.minimax(tic_tac_toe.board, depth + 1, False)
                    tic_tac_toe.board[key] = ' '

                    if score > best_score:
                        best_score = score

            return best_score

        else:
            best_score = 10000
            for key in tic_tac_toe.board.keys():
                if tic_tac_toe.space_is_free(key):
                    tic_tac_toe.board[key] = 'O' if self.symbol == 'X' else 'X'
                    score = self.minimax(tic_tac_toe.board, depth + 1, True)
                    tic_tac_toe.board[key] = ' '

                    if score < best_score:
                        best_score = score

            return best_score


if __name__ == "__main__":
    game = Game()
    game.run()
