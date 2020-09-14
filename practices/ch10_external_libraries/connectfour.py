import datetime
from colorama import init
from colorama import Fore, Back, Style
import json
import os
init()


def main():
    print()
    print("Connect Four")
    print()
    log("Game started.")

    show_leaders()

    board = [[None for x in range(7)] for x in range(6)]

    active_player_index = 0
    players = get_players()
    colors = ["Y", "R"]
    player = players[active_player_index]

    while not find_winner(board):
        # SHOW THE BOARD
        player = players[active_player_index]
        symbol = colors[active_player_index]

        announce_turn(player)
        show_board(board)
        if not choose_column(board, symbol):
            print("That column is full.")
            continue

        # TOGGLE ACTIVE PLAYER
        active_player_index = (active_player_index + 1) % len(players)

    record_win(player)
    print()
    print(f"GAME OVER! {player} has won with the board: ")
    show_board(board)
    print()


def get_players():
    player1 = input("What is your name? ")
    player2 = input("What is your opponent's name? ")
    log(f"Players are: {player1} and {player2}")

    return player1, player2


def find_winner(board):
    sequences = get_winning_sequences(board)

    for cells in sequences:
        symbol1 = cells[0]
        if symbol1 and all(symbol1 == cell for cell in cells):
            return True

    return False


def show_leaders():
    leaders = load_leaders()

    sorted_leaders = list(leaders.items())
    sorted_leaders.sort(key=lambda l: l[1], reverse=True)

    print()
    print("---------------------------")
    print("LEADERS:")
    for name, wins in sorted_leaders[0:5]:
        print(f"{wins:,} -- {name}")
    print("---------------------------")
    print()


def load_leaders():
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'leaderboard.json')

    if not os.path.exists(filename):
        return {}

    with open(filename, 'r', encoding='utf-8') as fin:
        return json.load(fin)


def record_win(winner_name):
    leaders = load_leaders()
    log(f"{winner_name} wins.")

    if winner_name in leaders:
        leaders[winner_name] += 1
    else:
        leaders[winner_name] = 1

    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'leaderboard.json')

    with open(filename, 'w', encoding='utf-8') as fout:
        json.dump(leaders, fout)


def get_winning_sequences(board):
    sequences = []

    # Win by rows
    for row_num in board:
        row1 = row_num[0:4]
        row2 = row_num[1:5]
        row3 = row_num[2:6]
        row4 = row_num[3:7]
        sequences.append(row1)
        sequences.append(row2)
        sequences.append(row3)
        sequences.append(row4)

    # Win by columns
    for col_idx in range(7):
        col1 = [board[x][col_idx] for x in range(0, 4)]
        col2 = [board[x][col_idx] for x in range(1, 5)]
        col3 = [board[x][col_idx] for x in range(2, 6)]
        sequences.append(col1)
        sequences.append(col2)
        sequences.append(col3)

    # Win by diagonals

    sequences.extend([[board[x][x] for x in range(y, (y + 4))] for y in range(0, 3)])
    sequences.extend([[board[x + 1][x] for x in range(y, (y + 4))] for y in range(0, 2)])
    sequences.extend([[board[x + 2][x] for x in range(0, 4)]])
    sequences.extend([[board[x][x + 1] for x in range(y, (y + 4))] for y in range(0, 3)])
    sequences.extend([[board[x][x + 2] for x in range(y, (y + 4))] for y in range(0, 2)])
    sequences.extend([[board[x][x + 3] for x in range(0, 4)]])
    sequences.extend([[board[x][6 - x] for x in range(y, (y + 4))] for y in range(0, 3)])
    sequences.extend([[board[x + 1][6 - x] for x in range(y, (y + 4))] for y in range(0, 2)])
    sequences.extend([[board[x + 2][6 - x] for x in range(0, 4)]])
    sequences.extend([[board[x][5 - x] for x in range(y, (y + 4))] for y in range(0, 3)])
    sequences.extend([[board[x][4 - x] for x in range(y, (y + 4))] for y in range(0, 2)])
    sequences.extend([[board[x][3 - x] for x in range(0, 4)]])
    return sequences


def announce_turn(player):
    print()
    print(f"It's {player}'s turn. Here's the board:")
    print()
    log(f"{player}'s turn.")


def show_board(board):
    for row in board:
        print(Fore.LIGHTBLUE_EX + '| ', end='')
        for cell in row:
            symbol = cell if cell is not None else "_"
            if symbol == "Y":
                print(Fore.YELLOW + 'O', Fore.RESET, end=" | ")
            elif symbol == "R":
                print(Fore.Red + 'O', Fore.RESET, end=" | ")
            else:
                print(symbol, Fore.RESET)
        print()


def choose_column(board, symbol):
    column = int(input("Choose a column: "))

    column -= 1

    if column < 0 or column >= len(board[0]):
        return False

    top_cell = board[0][column]
    if top_cell is not None:
        return False

    lowest_empty(column, symbol, 5, board)
    return True


def lowest_empty(column, symbol, index, board):
    cell = board[index][column]

    if cell is None:
        board[index][column] = symbol
        log(f"{symbol} is dropped in column: {column}")
    else:
        index -= 1
        lowest_empty(column, symbol, index, board)


def log(msg):
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'rps.log')

    with open(filename, 'a', encoding='utf-8') as fout:
        fout.write(f"[{datetime.datetime.now().date().isoformat()}] ")
        fout.write(msg)
        fout.write('\n')


if __name__ == '__main__':
    main()
