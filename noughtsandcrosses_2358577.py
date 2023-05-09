import random  #to choose computer random choice
import os.path #to check the directory or path of file exists or not
import json    #for storing and exchanging the data(leaderboard)

random.seed()


def draw_board(board):
    # This function prints the board into 3*3 matrix with dashes(-) & pipes(|)
    print('-------------')
    for row in board:  # iterates over rows in board
        temp = '| '
        for mark in row:  # iterates over every mark in row
            temp += mark + ' | '
        print(temp)
        print('-------------')

def welcome(board):  #this is a welcome function which display welcome message
    print("Welcome to Tic-Tac-Toe!")
    print("Here's the current board:")
    draw_board(board)


def initialise_board(board): #setting all elements of the board to one space ' ' and return board
    board = [[' ' for j in range(3)] for i in range(3)]
    return board


def get_player_move(board):
    '''
    Prompts user to input row and column number.
    Checks if user's choice is empty or not
    '''
    while True:
        try:
            row = int(input("Enter the row number (1-3): ")) - 1
            col = int(input("Enter the column number (1-3): ")) - 1
            if board[row][col] == ' ':
                return row, col
            else:
                print("That cell is already taken. Please choose another one.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a row and column number between 1 and 3.")


def choose_computer_move(board):
    """
    This is choose_computer_move.
    Randomly generate computer's move in a list of all empty spaces.
    Return row and column.
        """
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
    row, col = random.choice(empty_cells)
    return row, col


def check_for_win(board, mark):
    """
    This function Checks for rows,
    columns ,diagonals & Returns if won or not.
    """
    # Check rows for a win
    for i in range(3):
        if board[i] == [mark] * 3:
            return True
    # Check columns for a win
    for j in range(3):
        if [board[i][j] for i in range(3)] == [mark] * 3:
            return True
    # Check diagonals for a win
    if [board[i][i] for i in range(3)] == [mark] * 3:
        return True
    if [board[i][2 - i] for i in range(3)] == [mark] * 3:
        return True
    return False


def check_for_draw(board):
    """
    This define function Checks for all mark and if any mark is ' '.
    Returns is_drawn.
    """
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                return False
    return True


def play_game(board):
    """
    define play_game function.
    Main game is played here.
    Return 1 if player won, -1 if computer won, 0 if game is drawn.
    """
    # calls the initialise_board function
    board = initialise_board(board)
    # calls the draw_board function
    draw_board(board)

    # Defining the player and computer marks
    player_mark = 'X'
    computer_mark = 'O'

    # Define the current player (player who goes first)
    current_player = 'player'

    #  The game loop starts
    for turn in range(9):
        # Get the current player's move
        if current_player == 'player':
            row, col = get_player_move(board)
            mark = player_mark
        else:
            row, col = choose_computer_move(board)
            mark = computer_mark

        # Update the board with the current player's move
        board[row][col] = mark

        # Draw the updated board
        draw_board(board)

        # Check for a win
        if check_for_win(board, mark):
            if current_player == 'player':
                # When the Player wins
                return 1
            else:
                # when the computer wins
                return -1

        # conditional statement to check draw
        if check_for_draw(board):
            # Draw
            return 0

        # Switch to the other player
        if current_player == 'player':
            current_player = 'computer'
        else:
            current_player = 'player'

    # If the for loop completes without a win or draw, it means it's a tie
    return 0


def menu():
    # prompt user for input and validate it
    while True:
        choice = input("Enter a choice (1 to play, 2 to save score, 3 to display leaderboard, or q to quit): ")
        if choice in ['1', '2', '3', 'q']:
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or q.")

    return choice


def load_scores():
    # Check if the file exists or not
    if not os.path.isfile('leaderboard.txt'):
        return {}

    # file handling for leaderboard
    with open('leaderboard.txt', 'r') as file:
        scores_json = file.read()

    # It Parse the JSON string into a dictionary
    scores = json.loads(scores_json)

    return scores


import json


def save_score(score):
    '''
    The sav_score function saves the score that we play in the game
    '''
    # Take a input from the player for their names.
    name = input("Enter your name: ")

    # If file is found then its load the exisitng scores from the file.
    try:
        with open('leaderboard.txt', 'r') as f:
            scores_json = f.read()
            scores = json.loads(scores_json)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty, start with an empty dict
        scores = {}

    # It Update the scores dictinary with the new score
    scores[name] = score

    # Save the scores to the file in json format
    with open('leaderboard.txt', 'w') as f:
        f.write(json.dumps(scores))

    # Print a confirmation message for the score to be saved
    print(f"Score of {score} saved successfully for {name}!")


def display_leaderboard(leaders):
    '''
    Its displays the leaderboard score in the console
    '''
    print("LEADERBOARD OF THE GAME")
    for name, score in leaders.items():
        print(f"{name}: {score}")