"""
Programme principal
S'exécute dans un environnement virtuel
"""

from models.match import Match
from models.data import DataManager

dm = DataManager()

# loading players, matchs, rounds, tournaments from database
players = dm.get_players(dict())
rounds = dm.get_rounds(dict())
tournaments = dm.get_tournaments(dict())
matchs = dm.get_matchs(dict())

# running tournament
tournaments["1"].add_round(rounds["1"].ident)
# running first round
# sorting players for the first round
rounds["1"].sort_players(players)

# first matchs
halves = rounds["1"].two_halves(players, tournaments["1"])
num_match = 1
for player1, player2 in zip(halves[0], halves[1]):
    rounds["1"].add_match(str(num_match))
    matchs[str(num_match)] = Match()
    matchs[str(num_match)].ident = str(num_match)
    matchs[str(num_match)].data = ([player1, 0], [player2, 0])
    dm.verify_matchs(matchs)
    num_match +=1

if len(rounds["1"].players) % 2 != 0:
    rounds["1"].add_match(str(num_match))
    matchs[str(num_match)] = Match()
    matchs[str(num_match)].ident = str(num_match)
    matchs[str(num_match)].data = ([tournaments["1"].singleton[-1], 0], [None, None])
    num_match +=1


for match in rounds["1"].matchs:
    if not matchs[match].data[1][0]:
        print(f"Match N° {match} : Joueur flottant : {players[matchs[match].data[0][0]]}")
    else:
        print(f"Match N° {match}: {players[matchs[match].data[0][0]]} vs {players[matchs[match].data[1][0]]} ")

print()

for i in range(len(rounds['1'].matchs)):
    matchs[rounds['1'].matchs[i]].random_result(players)
    rounds['1'].scores_update(matchs[rounds['1'].matchs[i]])

rounds["1"].get_end_time()

for player in rounds['1'].scores.items():
    print(players[player[0]], player[1])

for round in rounds:
    print(f"Début de la ronde {rounds[round].name} : {rounds[round].start}")
    for match in matchs:
        if matchs[match].data[1][0]:
            print(f"Round N°{round} - Match N°{match} : {players[matchs[match].data[0][0]]} vs {players[matchs[match].data[1][0]]} {rounds[round].scores[matchs[match].data[0][0]]} pts - {rounds[round].scores[matchs[match].data[1][0]]} pts")
        else:
            print(f"Round N°{round} - Match N°{match} : {players[matchs[match].data[0][0]]} {rounds[round].scores[matchs[match].data[0][0]]} pts")
    print(f"Fin de la ronde {rounds[round].name} : {rounds[round].end}")


