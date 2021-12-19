import datetime

from models.player import Player
from models.round import Round
from models.tournament import Tournament
from models.match import Match
from data.simulation import players_data, rounds_data, tournaments_data, matchs_data

class DataLoader:
    def __init__(self):
        pass

    def get_players(self, players):
        for player in players_data.items():
            players[player[0]] = Player()
            players[player[0]].ident = player[0]
            players[player[0]].lastname = player[1][0]
            players[player[0]].firstname = player[1][1]
            players[player[0]].rank = player[1][2]
            players[player[0]].birthdate = datetime.date(player[1][3][0], player[1][3][1], player[1][3][2])
            players[player[0]].gender = player[1][4]
        return players

    def verify_players(self, players):
        for player in players.values():
            for attribute in Player().__dict__:
                if type(player.__getattribute__(attribute)) != type(Player().__getattribute__(attribute)):
                    print(f"Erreur pour le {player.get_translation('fr')[attribute]} du joueur {player}")
                    print(f"{player.__getattribute__(attribute)} n'est pas de type {Player().__getattribute__(attribute)}")
                    exit()
            if player.gender not in ["M", "F"]:
                print(f"Le sexe du joueur {player} doit être 'M' ou 'F'")
                exit()

    def get_rounds(self, rounds, matchs, players):
        for round in rounds_data.items():
            rounds[round[0]] = Round()
            rounds[round[0]].ident = round[0]
            rounds[round[0]].name = round[1][0]
            rounds[round[0]].players = [players[x] for x in round[1][1]]
            rounds[round[0]].scores = round[1][2]
            rounds[round[0]].matchs = [matchs[x] for x in round[1][3]]
            rounds[round[0]].start = datetime.datetime(round[1][4][0], round[1][4][1], round[1][4][2], round[1][4][3], round[1][4][4], round[1][4][5])
            for player in round[1][1]:
                rounds[round[0]].add_player_score(player)
        return rounds

    def get_tournaments(self, tournaments, rounds, players):
        for tournament in tournaments_data.items():
            tournaments[tournament[0]] = Tournament()
            tournaments[tournament[0]].ident = tournament[0]
            tournaments[tournament[0]].name = tournament[1][0]
            tournaments[tournament[0]].town = tournament[1][1]
            tournaments[tournament[0]].country = tournament[1][2]
            tournaments[tournament[0]].date_start = datetime.date(tournament[1][3][0], tournament[1][3][1], tournament[1][3][2])
            tournaments[tournament[0]].date_end = datetime.date(tournament[1][4][0], tournament[1][4][1],
                                                                  tournament[1][4][2])
            tournaments[tournament[0]].status = tournament[1][5]
            tournaments[tournament[0]].control_time = tournament[1][6]
            tournaments[tournament[0]].description = tournament[1][7]
            tournaments[tournament[0]].system = tournament[1][8]
            tournaments[tournament[0]].nb_rounds = tournament[1][9]
            tournaments[tournament[0]].rounds = [rounds[x] for x in tournament[1][10]]
            tournaments[tournament[0]].players = [players[x] for x in tournament[1][11]]
            tournaments[tournament[0]].singleton = tournament[1][12]
        return tournaments

    def verify_tournaments(self, tournaments):
        for tournament in tournaments.values():
            for attribute in Tournament().__dict__:
                if type(tournament.__getattribute__(attribute)) != type(Tournament().__getattribute__(attribute)):
                    print(f"Erreur pour le {tournament.get_translation('fr')[attribute]} du tournoi {tournament.name}")
                    print(f"{tournament.__getattribute__(attribute)} n'est pas de type {Tournament().__getattribute__(attribute)}")
                    exit()
                if tournament.status not in ["upcoming", "in progress", "ended"]:
                    print(f"Le statut du tournoi {tournament.name} doit être 'upcoming', 'in progress' ou 'ended'")
                    exit()
                if tournament.control_time not in ["bullet", "blitz", "rapid"]:
                    print(f"Le type de partie du tournoi {tournament.name} doit être 'bullet', 'blitz' ou 'rapid'")
                    exit()

    def get_matchs(self, matchs, players):
        for match in matchs_data.items():
            matchs[match[0]] = Match()
            matchs[match[0]].ident = match[0]
            matchs[match[0]].data = ([players[match[1][0][0]], match[1][0][1]], [players[match[1][1][0]], match[1][1][1]])
        return matchs



