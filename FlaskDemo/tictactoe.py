def print_board(board):
    """
    Prints the current state of the Tic-Tac-Toe board.

    Args:
        board (list of list of str): A 3x3 list representing the game board.
    """
    for row in board:
        print(" | ".join(row))
        print("-" * 5)


#
def check_winner(board, player):
    """
    Checks if the given player has won the game.

    Args:
        board (list of list of str): A 3x3 list representing the game board.
        player (str): The current player's symbol ("X" or "O").

    Returns:
        bool: True if the player has won, otherwise False.
    """
    # Check rows, columns, and diagonals
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False


def is_full(board):
    """
    Checks if the Tic-Tac-Toe board is full.

    Args:
        board (list of list of str): A 3x3 list representing the game board.

    Returns:
        bool: True if the board is full (no empty spaces), otherwise False.
    """
    return all(cell != " " for row in board for cell in row)


def tic_tac_toe():
    """
    Runs a two-player Tic-Tac-Toe game.

    The game alternates turns between players "X" and "O", with inputs taken for
    row and column positions. The game ends when a player wins or the board is full.

    Returns:
        None
    """
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]

    print("Tic-Tac-Toe Game")
    print_board(board)

    for turn in range(9):
        player = players[turn % 2]
        while True:
            try:
                row, col = map(int, input(f"Player {player}, enter row and column (0-2, space-separated): ").split())
                if board[row][col] == " ":
                    board[row][col] = player
                    break
                else:
                    print("Cell already taken. Choose another.")
            except (ValueError, IndexError):
                print("Invalid input. Enter two numbers between 0 and 2.")

        print_board(board)

        if check_winner(board, player):
            print(f"Player {player} wins!")
            return

        if is_full(board):
            print("It's a draw!")
            return

    print("It's a draw!")

if __name__ == '__main__':
    tic_tac_toe()
