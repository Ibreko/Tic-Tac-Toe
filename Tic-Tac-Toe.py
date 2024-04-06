import os
import random

def display_board(board):
    size = int(len(board) ** 0.5)
    for i in range(size):
        print(" | ".join(board[i*size : (i+1)*size]))
        if i < size - 1:
            print("-" * (size*4 - 1))

def player_input():
    player1 = input("Please pick a marker 'X' or 'O': ").upper()
    while player1 not in ['X', 'O']:
        player1 = input("Please pick a marker 'X' or 'O': ").upper()
    player2 = 'O' if player1 == 'X' else 'X'
    print("Player 1 chose " + player1 + ". Player 2 will be " + player2)
    return player1, player2

def place_marker(board, mark, position):
    board[position-1] = mark

def win_check(board, mark, win_size):
    size = int(len(board) ** 0.5)
    for i in range(size):
        row = board[i*size : (i+1)*size]
        if all(cell == mark for cell in row):
            return True
    for i in range(size):
        col = [board[j*size + i] for j in range(size)]
        if all(cell == mark for cell in col):
            return True
    diagonal1 = [board[i*size + i] for i in range(size)]
    diagonal2 = [board[i*size + size - 1 - i] for i in range(size)]
    if all(cell == mark for cell in diagonal1) or all(cell == mark for cell in diagonal2):
        return True
    return False

def choose_first():
    return random.choice(['Player 1', 'Player 2'])

def space_check(board, position):
    return board[position-1] == ' '

def full_board_check(board):
    return ' ' not in board

def player_choice(board):
    size = int(len(board) ** 0.5)
    while True:
        try:
            position = int(input(f'Choose square (1-{len(board)}): '))
            if position in range(1, len(board)+1) and space_check(board, position):
                return position
            else:
                print('Invalid input. Please choose an available square.')
        except ValueError:
            print('Invalid input. Please enter a valid integer.')


def replay():
    return input('Do you want to play again? Enter Yes or No: ').capitalize().startswith('Y')

def update_statistics(outcome, stats):
    if outcome == 'win':
        stats['wins'] += 1
    elif outcome == 'loss':
        stats['losses'] += 1
    else:
        stats['draws'] += 1

def print_leaderboard(leaderboard):
    print("Leaderboard:")
    for idx, (player, wins) in enumerate(leaderboard, start=1):
        print(f"{idx}. {player}: {wins} wins")

def update_leaderboard(player, leaderboard):
    for idx, (name, wins) in enumerate(leaderboard):
        if name == player:
            leaderboard[idx] = (name, wins + 1)
            break
    else:
        leaderboard.append((player, 1))
    leaderboard.sort(key=lambda x: x[1], reverse=True)

def get_player_stats(player, stats):
    return f"Player {player}: Wins - {stats['wins']}, Losses - {stats['losses']}, Draws - {stats['draws']}"

print('Welcome to Tic Tac Toe!')

leaderboard = []
stats_player1 = {'wins': 0, 'losses': 0, 'draws': 0}
stats_player2 = {'wins': 0, 'losses': 0, 'draws': 0}

while True:
    size = int(input("Enter the size of the board (e.g., 3 for 3x3, 4 for 4x4, etc.): "))
    board = [' ']*size*size
    player1_marker, player2_marker = player_input()

    turn = choose_first()
    print(turn + ' will go first.')

    game_on = True

    while game_on:
        display_board(board)
        position = player_choice(board)

        if turn == 'Player 1':
            place_marker(board, player1_marker, position)
            if win_check(board, player1_marker, size):
                display_board(board)
                print('Player 1 wins!')
                update_statistics('win', stats_player1)
                update_leaderboard('Player 1', leaderboard)
                game_on = False
            elif full_board_check(board):
                display_board(board)
                print('It\'s a draw!')
                update_statistics('draw', stats_player1)
                update_statistics('draw', stats_player2)
                game_on = False
            else:
                turn = 'Player 2'
        else:
            place_marker(board, player2_marker, position)
            if win_check(board, player2_marker, size):
                display_board(board)
                print('Player 2 wins!')
                update_statistics('win', stats_player2)
                update_leaderboard('Player 2', leaderboard)
                game_on = False
            elif full_board_check(board):
                display_board(board)
                print('It\'s a draw!')
                update_statistics('draw', stats_player1)
                update_statistics('draw', stats_player2)
                game_on = False
            else:
                turn = 'Player 1'

    print(get_player_stats('1', stats_player1))
    print(get_player_stats('2', stats_player2))
    print_leaderboard(leaderboard)

    if not replay():
        break
