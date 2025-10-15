"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count("X") for row in board)
    o_count = sum(row.count("O") for row in board)

    if x_count <= o_count:
        return "X"
    else:
        return "O"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    # Find empty cells in the board
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                moves.add((i, j))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid move")
    # Make a deep copy of the board
    new_board = copy.deepcopy(board)
    i, j = action
    # Assign a move to the copy
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != None:
            return board[i][0]

    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != None:
            return board[0][j]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != None:
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] != None:
        return board[0][2]

    # No winner (tie)
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if someone has won, game is over
    if winner(board) is not None:
        return True

    # Check if there are any empty cells left, game continues
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:  # found an empty cell
                return False

    # Otherwise, it is a tie and game is over
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "X":
        return 1
    elif winner(board) == "O":
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    # Return the best action for player X
    if player(board) == X:
        v = -math.inf
        best_action = None
        for action in actions(board):
            simulated = result(board, action)
            value = min_value(simulated)
            if value > v:
                v = value
                best_action = action
        return best_action

    # Return the best action for player O
    else:
        v = math.inf
        best_action = None
        for action in actions(board):
            simulated = result(board, action)
            value = max_value(simulated)
            if value < v:
                v = value
                best_action = action
        return best_action


# Function to maximize value for X
def max_value(board):
    if terminal(board):
        return utility(board)

    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


# Function to minimize value for O
def min_value(board):
    if terminal(board):
        return utility(board)

    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
