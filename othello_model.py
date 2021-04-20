import random

directions = [-11, -10, -9, -1, 1, 9, 10, 11]
switch = {"o": "@", "@": "o"}
score = {"o": 2, "@": 2}
piece_to_word = {"o": "White", "@": "Black"}  # print statements
all_moves = []


def display_board(board):
    display = ""
    index = 0
    while index < 100:
        display += (board[index] + " ")
        index += 1
        if index % 10 == 0:
            display = display.strip() + "\n"
    print(display)


def possible_moves(board, piece):
    opponent = switch[piece]
    piece_locations = [index for index in range(len(board)) if board[index] == piece]

    moves = set()  # prevents duplicates
    for direction in directions:
        for piece_location in piece_locations:
            board_index = piece_location + direction
            if board[board_index] == opponent:
                while board[board_index] == opponent:
                    board_index += direction
                if board[board_index] == ".":  # prevents from matching a '?'
                    moves.add(board_index)
    return sorted(list(moves))  # sorts in ascending order


def move(board, piece, move):
    opponent = switch[piece]
    board = board[:move] + piece + board[move+1:]
    score[piece] += 1

    for direction in directions:
        board_index = move + direction
        if board[board_index] == opponent:
            flips = []
            while board[board_index] == opponent:
                flips.append(board_index)
                board_index += direction
            if board[board_index] == piece:
                for flip in flips:
                    board = board[:flip] + piece + board[flip+1:]
                    score[piece] += 1
                    score[opponent] -= 1
    return board


def run_game(board, piece):  # recursive
    if "." not in board:
        display_board(board)
        for part in ("o", "@"):
            print("Percent " + piece_to_word[part] + ": " + str(score[part] * 1.0 / (score["o"] + score["@"])))
        print(all_moves)
        return

    display_board(board)
    for part in ("o", "@"):
        print(piece_to_word[part] + ": " + str(score[part]))

    moves = possible_moves(board, piece)

    if len(moves) != 0:
        print(piece_to_word[piece] + " Possible Moves: " + str(moves))
        rand = moves[random.randint(0, len(moves)-1)]
        print("Choose " + str(rand))
        all_moves.append(rand)
        new_board = move(board, piece, rand)
        run_game(new_board, switch[piece])
    else:
        print("Pass")
        all_moves.append(-1)
        run_game(board, switch[piece])


board = "???????????........??........??........??...o@...??...@o...??........??........??........???????????"
run_game(board, "@")
