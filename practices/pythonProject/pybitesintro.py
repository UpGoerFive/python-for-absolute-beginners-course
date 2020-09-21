games_won = dict(sara=0, bob=1, tim=5, julian=3, jim=1)


def print_game_stats(games_won):
    for person, wins in games_won.items():
        if wins == 1:
            print(f"{person} has won 1 game")
        else:
            print(f"{person} has won {wins} games")


print_game_stats(games_won)