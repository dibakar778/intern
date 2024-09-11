import math

# Print the Tic-Tac-Toe board
def print_board(board):
    for row in board:
        print("|".join(row))
        print("-" * 5)

# Check if there are empty spots on the board
def is_moves_left(board):
    for row in board:
        if "_" in row:
            return True
    return False

# Check for a winner
def evaluate(board):
    # Check rows for victory
    for row in board:
        if row[0] == row[1] == row[2]:
            if row[0] == 'X':
                return -10
            elif row[0] == 'O':
                return 10

    # Check columns for victory
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col]:
            if board[0][col] == 'X':
                return -10
            elif board[0][col] == 'O':
                return 10

    # Check diagonals for victory
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == 'X':
            return -10
        elif board[0][0] == 'O':
            return 10

    if board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] == 'X':
            return -10
        elif board[0][2] == 'O':
            return 10

    # No winner yet
    return 0

# Minimax function to evaluate the best move for AI
def minimax(board, depth, is_maximizing):
    score = evaluate(board)

    # If AI has won, return score
    if score == 10:
        return score

    # If Human has won, return score
    if score == -10:
        return score

    # If there are no more moves, return 0 for a draw
    if not is_moves_left(board):
        return 0

    # Maximizer's move (AI, 'O')
    if is_maximizing:
        best = -math.inf

        # Traverse all cells
        for i in range(3):
            for j in range(3):
                if board[i][j] == "_":
                    # Make the move
                    board[i][j] = 'O'
                    best = max(best, minimax(board, depth + 1, False))
                    # Undo the move
                    board[i][j] = "_"
        return best

    # Minimizer's move (Human, 'X')
    else:
        best = math.inf

        # Traverse all cells
        for i in range(3):
            for j in range(3):
                if board[i][j] == "_":
                    # Make the move
                    board[i][j] = 'X'
                    best = min(best, minimax(board, depth + 1, True))
                    # Undo the move
                    board[i][j] = "_"
        return best

# Function to find the best move for the AI
def find_best_move(board):
    best_val = -math.inf
    best_move = (-1, -1)

    # Traverse all cells to evaluate the best move
    for i in range(3):
        for j in range(3):
            if board[i][j] == "_":
                # Make the move
                board[i][j] = 'O'

                # Call minimax to compute the move's value
                move_val = minimax(board, 0, False)

                # Undo the move
                board[i][j] = "_"

                # Update the best move if the current move is better
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

    return best_move

# Function to check if the game is over
def is_game_over(board):
    if evaluate(board) != 0 or not is_moves_left(board):
        return True
    return False

# Main function to play the game
def play_game():
    board = [
        ["_", "_", "_"],
        ["_", "_", "_"],
        ["_", "_", "_"]
    ]
    
    print("Welcome to Tic-Tac-Toe! You are 'X' and the AI is 'O'.")
    print_board(board)
    
    while True:
        # Human's turn
        while True:
            try:
                row = int(input("Enter the row (0, 1, or 2): "))
                col = int(input("Enter the column (0, 1, or 2): "))
                if board[row][col] == "_":
                    board[row][col] = 'X'
                    break
                else:
                    print("Cell already occupied! Try again.")
            except (ValueError, IndexError):
                print("Invalid input! Please enter a valid row and column.")
        
        print("Your move:")
        print_board(board)

        if is_game_over(board):
            break

        # AI's turn
        print("AI is making a move...")
        ai_move = find_best_move(board)
        board[ai_move[0]][ai_move[1]] = 'O'
        print_board(board)

        if is_game_over(board):
            break

    # Check result
    result = evaluate(board)
    if result == 10:
        print("AI wins!")
    elif result == -10:
        print("You win!")
    else:
        print("It's a draw!")

# Play the game
play_game()
