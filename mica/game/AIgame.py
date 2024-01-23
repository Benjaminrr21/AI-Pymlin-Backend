import math
import sys

sys.setrecursionlimit(10**6)  # Set a higher limit if needed

SET_STONE = 'set'
MOVE_STONE = 'move'
REMOVE_STONE = 'remove'

WHITE = 1
BLACK = -1

MOVE_TYPE = 0
MOVE_COLOR = 1
MOVE_X = 2
MOVE_Y = 3
MOVE_Z = 4

def is_end(state):
    return state['white_remaining'] == 0 and state['black_remaining'] == 0 and (state['white_count'] <= 2 or state['black_count'] <= 2)

def getAvailableMovesAI(matrix):
    moves = []
    for i in range(0, 3):
        for j in range(0, 8):
            if matrix[i][j] == 0:
                moves.append(matrix[i][j])
    return moves

def count_open_mills(state, player):
    matrix = state['stones']
    count = 0
    for i in range(0, 3):
        for j in range(0, 7, 2):
            if j != 6:
                if matrix[i][j] + matrix[i][j + 1] + matrix[i][j + 2] == player * 3:
                    count += 1
            else:
                if matrix[i][j] + matrix[i][j + 1] + matrix[i][0] == player * 3:
                    count += 1
    k = 0
    for i in range(1, 8, 2):
        if matrix[k][i] + matrix[k + 1][i] + matrix[k + 2][i] == player * 3:
            count += 1

    return count

def evaluateE(state):
    matrix = state['stones']
    white_pieces = 0
    black_pieces = 0
    for i in range(0, 3):
        for j in range(0, 8):
            if matrix[i][j] == 1:
                white_pieces += 2 if j % 2 != 0 else 1
                white_pieces += count_open_mills(state, 1) / 5
            elif matrix[i][j] == -1:
                black_pieces += 2 if j % 2 != 0 else 1
                black_pieces += 1
                black_pieces += count_open_mills(state, -1) / 10

    evaluation = 100 * (white_pieces - black_pieces) + 10 * white_pieces

    return evaluation

def checkpossiblemill(mat, i, j):
    if mat[i][j + 1] + mat[i][j + 2] == 2:
        return 1000
    elif mat[i][j] % 2 == 0:
        return 700
    elif mat[i][j + 2] % 2 != 0:
        return 100
    return 500

def evaluateM(state):
    board = state['stones']
    player_pieces = sum(row.count(1) for row in board)
    ai_pieces = sum(row.count(-1) for row in board)
    piece_count_score = player_pieces - ai_pieces

    player_mobility = sum(row.count(0) for row in board if 1 in row)
    ai_mobility = sum(row.count(0) for row in board if -1 in row)
    mobility_score = player_mobility - ai_mobility

    player_open_mills = count_open_mills(state, 1)
    ai_open_mills = count_open_mills(state, -1)
    open_mills_score = player_open_mills - ai_open_mills

    total_score = 2 * piece_count_score + mobility_score + 3 * open_mills_score

    return total_score

def evaluateH(state):
    matrix = state['stones']
    counter = 0
    aiMoves = getAvailableMovesAI(matrix)
    counter += len(aiMoves)
    white_pieces = 0
    black_pieces = 0
    for i in range(0, 3):
        for j in range(0, 8):
            if matrix[i][j] == 1:
                white_pieces += 1
            elif matrix[i][j] == -1:
                black_pieces += 1

    evaluation = 0
    if counter == 0:
        evaluation = math.inf
    else:
        evaluation = (
            150 * white_pieces - 10 * black_pieces +
            500 / counter +
            position_bonus(matrix, 1) - position_bonus(matrix, -1)
        )
    return evaluation

def position_bonus(matrix, player):
    bonus = 0
    for i in range(0, 3):
        for j in range(0, 8):
            if matrix[i][j] == player:
                bonus += center_bonus(i, j)
    return bonus

def center_bonus(row, col):
    center_rows = [0, 1, 1, 1, 2]
    center_cols = [3, 2, 3, 4, 3]
    if (row, col) in zip(center_rows, center_cols):
        return 50
    else:
        return 0

def get_neighbouring_empty_places2(state, row, col):
    stones = state['stones']

    if row == 0:
        if col in [2, 4, 6]:
            directions = [(0, -1), (0, 1)]
        if col == 0:
            directions = [(0, 7), (0, 1)]
        if col in [1, 3, 5]:
            directions = [(0, -1), (0, 1), (1, 0)]
        if col == 7:
            directions = [(0, -1), (0, 0), (1, 0)]
    if row == 1:
        if col in [2, 4, 6]:
            directions = [(0, -1), (0, 1)]
        if col == 0:
            directions = [(0, 7), (0, 1)]
        if col in [1, 3, 5]:
            directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        if col == 7:
            directions = [(0, -1), (0, -7), (1, 0), (-1, 0)]
    if row == 2:
        if col in [2, 4, 6]:
            directions = [(0, -1), (0, 1)]
        if col == 0:
            directions = [(0, 7), (0, 1)]
        if col in [1, 3, 5]:
            directions = [(0, -1), (0, 1), (-1, 0)]
        if col == 7:
            directions = [(0, -1), (0, -7), (-1, 0)]

    for dx, dy in directions:
        new_row, new_col = row + dx, col + dy

        if 0 <= new_row < 3 and 0 <= new_col < 8 and stones[new_row][new_col] == 0:
            yield new_row, new_col

def get_neighbouring_empty_places(state, row, col):
    stones = state['stones']

    if col % 2 != 0:
        directions = [(0, -1), (0, 1), ]
    else:
        directions = [(0, -1), (0, 1)]

    empty = []
    for dx, dy in directions:
        new_row, new_col = row + dx, col + dy

        if 0 <= new_row < 3 and 0 <= new_col < 8 and stones[new_row][new_col] == 0:
            empty.append((new_row, new_col))

    return empty

def get_moves(state, player, line_made):
    if line_made:
        for s, square in enumerate(state['stones']):
            for j, element in enumerate(square):
                if element == player * -1:
                    yield REMOVE_STONE, player, s, j

        return

    if state['white_remaining' if player == 1 else 'black_remaining'] > 0:
        for s, square in enumerate(state['stones']):
            for j, element in enumerate(square):
                if element == 0:
                    yield SET_STONE, player, s, j

        return

    for s, square in enumerate(state['stones']):
        for j, element in enumerate(square):
            if element == player:
                for x, y in get_neighbouring_empty_places2(state, s, j):
                    yield MOVE_STONE, player, x, y, s, j

def is_making_line(state, move):
    matrix = state['stones']
    count = 0
    for i in range(0, 3):
        for j in range(0, 7, 2):
            if j != 6:
                if abs(matrix[i][j] + matrix[i][j + 1] + matrix[i][j + 2]) == 3:
                    return True
            else:
                if abs(matrix[i][j] + matrix[i][j + 1] + matrix[i][0]) == 3:
                    return True
    k = 0
    for i in range(1, 8, 2):
        if abs(matrix[k][i] + matrix[k + 1][i] + matrix[k + 2][i]) == 3:
            return True

    return False

def apply_move(state, move):
    stones = state['stones']
    if move[MOVE_TYPE] == SET_STONE:
        _, color, x, y = move
        stones[x][y] = color
        state['white_remaining' if color == WHITE else 'black_remaining'] -= 1
        state['white_count' if color == WHITE else 'black_count'] += 1
    elif move[MOVE_TYPE] == REMOVE_STONE:
        _, color, x, y = move
        stones[x][y] = 0
        state['white_count' if color == WHITE else 'black_count'] -= 1
    elif move[MOVE_TYPE] == MOVE_STONE:
        _, color, to_x, to_y, from_x, from_y = move
        stones[from_x][from_y] = 0
        stones[to_x][to_y] = color

    state['turn'] += 1

def undo_move(state, move):
    stones = state['stones']
    if move[MOVE_TYPE] == SET_STONE:
        _, color, x, y = move
        stones[x][y] = 0
        state['white_remaining' if color == WHITE else 'black_remaining'] += 1
        state['white_count' if color == WHITE else 'black_count'] -= 1
    elif move[MOVE_TYPE] == REMOVE_STONE:
        _, color, x, y = move
        stones[x][y] = color * -1
        state['white_count' if color == WHITE else 'black_count'] += 1
    elif move[MOVE_TYPE] == MOVE_STONE:
        _, color, to_x, to_y, from_x, from_y = move
        stones[from_x][from_y] = color
        stones[to_x][to_y] = 0

    state['turn'] += 1

def minimax(state, depth, player, line_made=False):
    if depth == 0 or is_end(state):
        return evaluateE(state), None

    next_player = player * -1

    if player == WHITE:
        value = -1000000
        best_move = None
        for move in get_moves(state, player, line_made):
            apply_move(state, move)
            if is_making_line(state, move):
                next_player *= -1
                line_made = True
            current_value = minimax(state, depth - 1, next_player, line_made)[0]
            print(f'{depth}:{player}:{current_value=}')
            if current_value > value:
                value = current_value
                best_move = move
            line_made = False
            undo_move(state, move)
        return value, best_move
    else:
        value = 1000000
        best_move = None
        for move in get_moves(state, player, line_made):
            apply_move(state, move)
            if is_making_line(state, move):
                next_player *= -1
                line_made = True
            current_value = minimax(state, depth - 1, next_player, line_made)[0]
            print(f'{depth}:{player}:{current_value=}')
            if current_value < value:
                value = current_value
                best_move = move
            line_made = False
            undo_move(state, move)
        return value, best_move

def alphabetaM(state, depth, a, b, player, line_made=False):
    if depth == 0 or is_end(state):
        return evaluateM(state), None
    
    next_player = player * -1
    
    if player == WHITE:
        value = -1000000
        best_move = None
        for move in get_moves(state, player, line_made):
            apply_move(state, move)
            if is_making_line(state, move):
                next_player *= -1
                line_made = True
            current_value = alphabetaM(state, depth - 1, a, b, next_player, line_made)[0]
           # print(f'{depth}:{player}:{current_value=}')
            if current_value > value:
                value = current_value
                best_move = move
            line_made = False
            undo_move(state, move)
            if value > b:
                break
            a = max(a, value)
        return value, best_move
    else:
        value = 1000000
        best_move = None
        for move in get_moves(state, player, line_made):
            apply_move(state, move)
            if is_making_line(state, move):
                next_player *= -1
                line_made = True
            current_value = alphabetaM(state, depth - 1, a, b, next_player, line_made)[0]
            #print(f'{depth}:{player}:{current_value=}')
            if current_value < value:
                value = current_value
                best_move = move
            line_made = False
            undo_move(state, move)
            if value < a:
                break
            b = min(b, value)
        return value, best_move

def alphabetaH(state, depth, a, b, player, line_made=False):
    if depth == 0 or is_end(state):
        return evaluateH(state), None
    
    next_player = player * -1
    
    if player == WHITE:
        value = -1000000
        best_move = None
        for move in get_moves(state, player, line_made):
            apply_move(state, move)
            if is_making_line(state, move):
                next_player *= -1
                line_made = True
            current_value = alphabetaH(state, depth - 1, a, b, next_player, line_made)[0]
            #print(f'{depth}:{player}:{current_value=}')
            if current_value > value:
                value = current_value
                best_move = move
            line_made = False
            undo_move(state, move)
            if value > b:
                break
            a = max(a, value)
        return value, best_move
    else:
        value = 1000000
        best_move = None
        for move in get_moves(state, player, line_made):
            apply_move(state, move)
            if is_making_line(state, move):
                next_player *= -1
                line_made = True
            current_value = alphabetaH(state, depth - 1, a, b, next_player, line_made)[0]
           # print(f'{depth}:{player}:{current_value=}')
            if current_value < value:
                value = current_value
                best_move = move
            line_made = False
            undo_move(state, move)
            if value < a:
                break
            b = min(b, value)
        return value, best_move


start_state = {
    'turn': 0,
    'white_remaining': 9,
    'black_remaining': 9,
    'white_count': 0,
    'black_count': 0,
    'line_made': False,
    'stones': [
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0]
    ]
}