import chess
import chess.engine
import time
import chess.svg
from IPython.display import SVG, display


def stockfish_eval(board_instance, depth):
    # engine = chess.engine.SimpleEngine.popen_uci("./stockfish_13_linux_x64_bmi2")
    move = engine.analyse(board, chess.engine.Limit(time=0.01))
    #print(move)
    return chess.engine.PovScore(move['score'], chess.BLACK).pov(chess.BLACK).relative.score()


def static_eval(board):
    i = 0
    evaluation = 0
    x = True
    try:
        x = bool(board.piece_at(i).color)
    except AttributeError as e:
        x = x
    while i < 63:
        i += 1
        evaluation = evaluation + (get_piece_val(str(board.piece_at(i))) if x else -get_piece_val(str(board.piece_at(i))))
    return evaluation

def get_piece_val(piece):
    if(piece == None):
        return 0
    value = 0
    if piece == "P" or piece == "p":
        value = 10
    if piece == "N" or piece == "n":
        value = 30
    if piece == "B" or piece == "b":
        value = 30
    if piece == "R" or piece == "r":
        value = 50
    if piece == "Q" or piece == "q":
        value = 90
    if piece == 'K' or piece == 'k':
        value = 900
    #value = value if (board.piece_at(place)).color else -value
    return value

def alpha_beta( board_instance, max_depth, current_depth, is_max_player, alpha, beta, nodes_per_depth ):

    # This if else code block is only used for analysis of algorithm, by counting number of nodes explored
    if max_depth-current_depth in nodes_per_depth:
        nodes_per_depth[max_depth-current_depth] += 1
    else:
        nodes_per_depth[max_depth-current_depth] = 1

    if current_depth == 0:
        leaf_node_score = static_eval(board_instance)
        return (leaf_node_score, nodes_per_depth)

    if is_max_player:

        # set absurdly high negative value such that none of the static evaluation result less than this value
        best_score = -100000

        for legal_move in board_instance.legal_moves:
            move =  chess.Move.from_uci(str(legal_move))

            # pusshing the current move to the board
            board_instance.push(move)

            #calculating node score, if the current node will be the leaf node, then score will be calculated by static evaluation;
            #score will be calculated by finding max value between node score and current best score.
            node_score, nodes_per_depth = alpha_beta(board_instance, max_depth, current_depth - 1, False, alpha, beta, nodes_per_depth)

            # calculating best score by finding max value between current best score and node score
            best_score = max(best_score, node_score)

            # undoing the last move, so as to explore new moves while backtracking
            board_instance.pop()

            # calculating alpha for current MAX node
            alpha = max(alpha, best_score)

            # beta cut off
            if beta <= alpha:
                return (best_score, nodes_per_depth)

        return (best_score, nodes_per_depth)
    else:

        # set absurdly high positive value such that none of the static evaluation result more than this value
        best_score = 100000

        for legal_move in board_instance.legal_moves:
            move =  chess.Move.from_uci(str(legal_move))

            # pushing the current move to the board
            board_instance.push(move)

            #calculating node score, if the current node will be the leaf node, then score will be calculated by static evaluation;
            #score will be calculated by finding min value between node score and current best score.
            node_score, nodes_per_depth = alpha_beta(board_instance, max_depth, current_depth - 1, True, alpha, beta, nodes_per_depth)

            # calculating best score by finding min value between current best score and node score
            best_score = min(best_score, node_score)

            # undoing the last move, so as to explore new moves while backtracking
            board_instance.pop()

            # calculating alpha for current MIN node
            beta = min(beta, best_score)

            # beta cut off
            if beta <= alpha:
                return (best_score, nodes_per_depth)

        return (best_score, nodes_per_depth)


def best_move_using_alpha_beta(board_instance, depth, is_max_player, alpha, beta ):
    best_move_score = -1000000
    best_move = None
    for legal_move in board_instance.legal_moves:
        move = chess.Move.from_uci(str(legal_move))
        board_instance.push(move)
        move_score, nodes_per_depth = alpha_beta(board_instance,depth, depth, False, alpha, beta, {} )
        score = max(best_move_score, move_score)
        board_instance.pop()
        if score > best_move_score:
            best_move_score = score
            best_move = move
    return (best_move, nodes_per_depth)

def game_between_two_computer(depth=3, number_of_move_per_player=5):
    board = chess.Board()

    for n in range(0,number_of_move_per_player*2):
        start = time.time()
        if n%2 == 0:
            print("WHITE Turn")
            move, nodes_per_depth = best_move_using_alpha_beta(board, depth, False, -10000, 10000)
        else:

            print("BLACK Turn")
            move, nodes_per_depth = best_move_using_alpha_beta(board, depth, True, -10000, 10000)
        end = time.time()

        print("Move in UCI format:", move)
        print("Nodes per depth:", nodes_per_depth)
        print("Time taken by Move:", end-start)
        board.push(move)
        display(SVG(chess.svg.board(board, size=400)))
        print("\n")

board = chess.Board()


move, nodes_per_depth = best_move_using_alpha_beta(board, 5, True, -100000, 100000)

move

nodes_per_depth

board.push(move)

board

move,nodes_per_depth = best_move_using_alpha_beta(board, 5, False, -100000, 100000)

move

nodes_per_depth

board.push(move)

board

game_between_two_computer(3)