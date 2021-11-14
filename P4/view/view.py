"""
Afficher les classements
Afficher les appariements
Afficher des statistiques
...
"""

class View:
    def __init__(self, name= None):
        self.name = name

    def display_players_by_name(self, players):
        print("Voici la liste des joueurs d'échecs (par ordre alphabétique")
        print(f"{'Nom':<10} {'Prénom':<10} {'Classement':<15}")
        players.sort(key=lambda x: x[1])
        players.sort(key=lambda x: x[0])
        for player in players:
            print(f"{player[0]:<10} {player[1]:<10} {player[2]:<5}")

    def display_players_by_rank(self, players):
        print("Voici la liste des joueurs d'échecs (par classement")
        print(f"{'Nom':<10} {'Prénom':<10} {'Classement':<15}")
        players.sort(key=lambda x: x[2])
        for player in players:
            print(f"{player[0]:<10} {player[1]:<10} {player[2]:<5}")

    def display_tournament_players_by_name(self, tournament):
        print(f"Voici la liste des joueurs du tournoi {tournament.name} (par ordre alphabétique)")
        print(f"{'Nom':<10} {'Prénom':<10} {'Classement':<15} {'Score':<5}")
        tournament.players.sort(key=lambda x: x.firstname)
        tournament.players.sort(key=lambda x: x.lastname)
        for player in tournament.players:
            print(f"{player.lastname:<10} {player.firstname:<15} {player.rank:<12} {player.score:<5}")

    def display_tournament_players_by_rank(self, tournament):
        print(f"Voici la liste des joueurs du tournoi {tournament.name} (par classement)")
        print(f"{'Nom':<10} {'Prénom':<10} {'Classement':<15} {'Score':<5}")
        tournament.players.sort(key=lambda x: x.rank)
        for player in tournament.players:
            print(f"{player.lastname:<10} {player.firstname:<15} {player.rank:<12} {player.score:<5}")

    def display_tournaments(self, tournaments):
        print(f"{'Nom du tournoi':<25} {'Nom':<10} {'Prénom':<10} {'Classement':<15}")
        for tournament in tournaments:
            print(f"{tournament.name:<25}")
            for player in tournament.players:
                print(f"{'*'*25} {player.lastname:<10} {player.firstname:<13} {player.rank:<15}")

