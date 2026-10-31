
import math

# Create Tic-Tac-Toe board
board = [" "] * 9

HUMAN = "X"
AI = "O"


# Display board
def display_board():
    print()
    for i in range(0, 9, 3):
        print(" | ".join(board[i:i+3]))
        if i < 6:
            print("--+---+--")
    print()


# Check winner
def check_winner(player):

    win_positions = [
        [0, 1, 2], [3, 4, 5],
        [6, 7, 8], [0, 3, 6],
        [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    for pos in win_positions:
        if all(board[i] == player for i in pos):
            return True

    return False


# Check draw
def is_draw():
    return " " not in board


# Minimax with Alpha-Beta Pruning
def minimax(is_maximizing, alpha, beta):

    if check_winner(AI):
        return 1

    if check_winner(HUMAN):
        return -1

    if is_draw():
        return 0

    if is_maximizing:

        best_score = -math.inf

        for i in range(9):
            if board[i] == " ":

                board[i] = AI

                score = minimax(False, alpha, beta)

                board[i] = " "

                best_score = max(best_score, score)
                alpha = max(alpha, best_score)

                if beta <= alpha:
                    break

        return best_score

    else:

        best_score = math.inf

        for i in range(9):
            if board[i] == " ":

                board[i] = HUMAN

                score = minimax(True, alpha, beta)

                board[i] = " "

                best_score = min(best_score, score)
                beta = min(beta, best_score)

                if beta <= alpha:
                    break

        return best_score


# Find best move for AI
def best_move():

    best_score = -math.inf
    move = -1

    for i in range(9):
        if board[i] == " ":

            board[i] = AI

            score = minimax(False, -math.inf, math.inf)

            board[i] = " "

            if score > best_score:
                best_score = score
                move = i

    return move


# Main game
print("TIC-TAC-TOE AI")
print("You are X and AI is O")
print("Enter positions from 1 to 9")

while True:

    display_board()

    # Human turn
    try:
        pos = int(input("Enter your position (1-9): ")) - 1

        if pos < 0 or pos > 8 or board[pos] != " ":
            print("Invalid position! Try again.")
            continue

    except ValueError:
        print("Please enter a valid number.")
        continue

    board[pos] = HUMAN

    if check_winner(HUMAN):
        display_board()
        print("Congratulations! You Win!")
        break

    if is_draw():
        display_board()
        print("Game Draw!")
        break

    # AI turn
    print("AI is thinking...")

    move = best_move()
    board[move] = AI

    if check_winner(AI):
        display_board()
        print("AI Wins!")
        break

    if is_draw():
        display_board()
        print("Game Draw!")
        break
