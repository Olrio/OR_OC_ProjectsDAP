"""
Création d'un tournoi
"""

def get_info_tournament():
    name = "Europe Grandmasters"
    location = "New York"
    return (name, location)

def choose_players(players):
    players_for_tournament = []
    choice = "0"
    for player in players:
        while choice != "y" and choice != "n":
            choice = input(f"Inclure le joueur {player} (y/n) ? : ")
        if choice == "y":
            players_for_tournament.append(player)
            choice = "0"
        else:
            choice = "0"

    return players_for_tournament


