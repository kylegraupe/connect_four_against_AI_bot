import numpy as np
import random
import sys
import pygame
import math

# GLOBAL VARIABLES
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

n_rows = 6
n_cols = 7

human = 0
computer = 1

void = 0
human_piece = 1
computer_piece = 2

square_size = 100
radius = int(square_size / 2 - 5)
width = n_cols * square_size
height = (n_rows + 1) * square_size
window_size = 4
size = (width, height)
screen = pygame.display.set_mode(size)


def initialize_board():
    """
    Initialize the game board
    :return:
    """
    return np.zeros((n_rows, n_cols))


def make_move(board, row, col, piece):
    """
    Make a move on the board
    :param board:
    :param row:
    :param col:
    :param piece:
    :return:
    """
    board[row][col] = piece


def validate_location(board, col):
    """
    Validate location on the game board
    :param board:
    :param col:
    :return:
    """
    return board[n_rows - 1][col] == 0


def find_open_row(board, col):
    """

    :param board:
    :param col:
    :return:
    """
    for r in range(n_rows):
        if board[r][col] == 0:
            return r


def print_game_board(board):
    """
    Output game board to terminal
    :param board:
    :return:
    """
    print(np.flip(board, 0))


def check_good_move(board, piece):
    """
    Checks board locations for a winning move
    :param board:
    :param piece:
    :return:
    """

    for i in range(n_cols - 3):
        for j in range(n_rows):
            if board[j][i] == piece and board[j][i + 1] == piece and board[j][i + 2] == piece and board[j][i + 3] == \
                    piece:
                return True

    for i in range(n_cols):
        for j in range(n_rows - 3):
            if board[j][i] == piece and board[j + 1][i] == piece and board[j + 2][i] == piece and board[j + 3][i] == piece:
                return True

    for i in range(n_cols - 3):
        for j in range(n_rows - 3):
            if board[j][i] == piece and board[j + 1][i + 1] == piece and board[j + 2][i + 2] == piece and board[j + 3][i + 3] == piece:
                return True

    for i in range(n_cols - 3):
        for j in range(3, n_rows):
            if board[j][i] == piece and board[j - 1][i + 1] == piece and board[j - 2][i + 2] == piece and board[j - 3][i + 3] == piece:
                return True


def eval_window(window, piece):
    """
    Evaluate game window
    :param window:
    :param piece:
    :return:
    """
    score = 0
    opp_piece = human_piece
    if piece == human_piece:
        opp_piece = computer_piece

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(void) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(void) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(void) == 1:
        score -= 4

    return score


def position_score(board, piece):
    """
    Find the score for the position
    :param board:
    :param piece:
    :return:
    """
    score = 0

    center_array = [int(i) for i in list(board[:, n_cols // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    for r in range(n_rows):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(n_cols - 3):
            window = row_array[c:c + window_size]
            score += eval_window(window, piece)

    for c in range(n_cols):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(n_rows - 3):
            window = col_array[r:r + window_size]
            score += eval_window(window, piece)

    for r in range(n_rows - 3):
        for c in range(n_cols - 3):
            window = [board[r + i][c + i] for i in range(window_size)]
            score += eval_window(window, piece)

    for r in range(n_rows - 3):
        for c in range(n_cols - 3):
            window = [board[r + 3 - i][c + i] for i in range(window_size)]
            score += eval_window(window, piece)

    return score


def check_end_node(board):
    """
    Validate conditions for the end node to terminate
    :param board:
    :return:
    """
    return check_good_move(board, human_piece) or check_good_move(board, computer_piece) or len(
        find_valid_locations(board)) == 0


def minimax(board, depth, a, b, max_player):
    """
    Minimax objective function
    :param board:
    :param depth:
    :param a:
    :param b:
    :param max_player:
    :return:
    """
    valid_locations = find_valid_locations(board)
    is_terminal = check_end_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if check_good_move(board, computer_piece):
                return (None, 100000000000000)
            elif check_good_move(board, human_piece):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, position_score(board, computer_piece))
    if max_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = find_open_row(board, col)
            b_copy = board.copy()
            make_move(b_copy, row, col, computer_piece)
            new_score = minimax(b_copy, depth - 1, a, b, False)[1]
            if new_score > value:
                value = new_score
                column = col
            a = max(a, value)
            if a >= b:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = find_open_row(board, col)
            b_copy = board.copy()
            make_move(b_copy, row, col, human_piece)
            new_score = minimax(b_copy, depth - 1, a, b, True)[1]
            if new_score < value:
                value = new_score
                column = col
            b = min(b, value)
            if a >= b:
                break
        return column, value


def find_valid_locations(board):
    """
    Check locations for validity
    :param board:
    :return:
    """
    valid_locations = []
    for col in range(n_cols):
        if validate_location(board, col):
            valid_locations.append(col)
    return valid_locations


def best_scoring_move(board, piece):
    """
    Get the move with the highest scores
    :param board:
    :param piece:
    :return:
    """
    valid_locations = find_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = find_open_row(board, col)
        temp_board = board.copy()
        make_move(temp_board, row, col, piece)
        score = position_score(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def display_game_board(board):
    """
    Use the PyGame library to make an interactive GUI
    :param board:
    :return:
    """

    for c in range(n_cols):
        for r in range(n_rows):
            pygame.draw.rect(screen, blue, (c * square_size, r * square_size + square_size, square_size, square_size))
            pygame.draw.circle(screen, black, (
                int(c * square_size + square_size / 2), int(r * square_size + square_size + square_size / 2)), radius)

    for c in range(n_cols):
        for r in range(n_rows):
            if board[r][c] == human_piece:
                pygame.draw.circle(screen, red, (
                    int(c * square_size + square_size / 2), height - int(r * square_size + square_size / 2)), radius)
            elif board[r][c] == computer_piece:
                pygame.draw.circle(screen, yellow, (
                    int(c * square_size + square_size / 2), height - int(r * square_size + square_size / 2)), radius)
    pygame.display.update()


def game_executive():
    """
    Execute game application
    :return:
    """
    board = initialize_board()
    print_game_board(board)
    game_over = False

    pygame.init()

    screen = pygame.display.set_mode(size)
    display_game_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    turn = random.randint(human, computer)

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, black, (0, 0, width, square_size))
                posx = event.pos[0]
                if turn == human:
                    pygame.draw.circle(screen, red, (posx, int(square_size / 2)), radius)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, black, (0, 0, width, square_size))
                if turn == human:
                    posx = event.pos[0]
                    col = int(math.floor(posx / square_size))

                    if validate_location(board, col):
                        row = find_open_row(board, col)
                        make_move(board, row, col, human_piece)

                        if check_good_move(board, human_piece):
                            label = myfont.render("Player 1 wins!!", 1, red)
                            screen.blit(label, (40, 10))
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        print_game_board(board)
                        display_game_board(board)

        if turn == computer and not game_over:

            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

            if validate_location(board, col):
                row = find_open_row(board, col)
                make_move(board, row, col, computer_piece)

                if check_good_move(board, computer_piece):
                    label = myfont.render("Player 2 wins!!", 1, yellow)
                    screen.blit(label, (40, 10))
                    game_over = True

                print_game_board(board)
                display_game_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3000)


if __name__ == "__main__":
    game_executive()