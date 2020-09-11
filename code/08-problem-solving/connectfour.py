# choose players
# make board
# choose starting player
# drop piece
# check for winner
# show board
# change active player

def main():
    print()
    print("Connect Four")
    print()

    board = [[None for x in range(7)] for x in range(6)]

    active_player_index = 0
    players = ["First", "Second"]
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

    print()
    print(f"GAME OVER! {player} has won with the board: ")
    show_board(board)
    print()


def find_winner(board):
    sequences = get_winning_sequences(board)

    for cells in sequences:
        symbol1 = cells[0]
        if symbol1 and all(symbol1 == cell for cell in cells):
            return True

    return False


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


def show_board(board):
    for row in board:
        print("| ", end='')
        for cell in row:
            symbol = cell if cell is not None else "_"
            print(symbol, end=" | ")
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
    else:
        index -= 1
        lowest_empty(column, symbol, index, board)


if __name__ == '__main__':
    main()
