"""
Accepter les données de l'utilisateur
Produire les résultats des matchs
Lancer de nouveaux tournois
...
"""

from models.data import Data
from models.round import Round
from models.player import Player
from models.tournament import Tournament
from view.view import View
from view.createplayer import get_players
from view.createtournament import get_info_tournament, choose_players


class Controller:
    def __init__(self):
        """ Create a controller for the application """
        self.db = Data()
        self.view = View()

    def run(self):
        self.data_players = get_players()  # récupération des infos sur les 8 joueurs du tournoi
        for data_player in self.data_players:
            player = Player(data_player)  # création de chaque joueur
            self.db.add_players(player)  # ajout de chaque joueur à la liste globale des joueurs
        self.db.save_players()  # enregistrement de la liste des joueurs dans un fichier

        self.data_tournament = get_info_tournament()  # récupération des infos sur le tournoi
        self.mytournament = Tournament(self.data_tournament[0], self.data_tournament[1])  # création du tournoi

        self.players = choose_players(self.db.get_players())
        for player in self.players:
            self.mytournament.add_player(player)

        self.db.add_tournament(self.mytournament)  # ajout du tournoi à la liste des tournois
        self.db.save_tournaments()  # enregistrement de la liste des tournois dans un fichier
        for num_round in range(1, self.mytournament.nb_rounds + 1):
            if num_round == 1:
                self.mytournament.sort_players()
                self.mytournament.first_round_sort_players()
                self.matchs = self.mytournament.first_matchs()
                self.mytournament.generate_round(Round("Round 1", self.matchs))
                self.mytournament.generate_results(self.mytournament.rounds[0])
                self.mytournament.sort_players()
                self.mytournament.display_scores()
            else:
                self.matchs = self.mytournament.other_matchs()
                self.mytournament.generate_round(Round(f"Round {num_round}", self.matchs))
                self.mytournament.generate_results(self.mytournament.rounds[num_round-1])
                self.mytournament.sort_players()
                self.mytournament.display_scores()
