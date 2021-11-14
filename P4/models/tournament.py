"""
Gestion d'un tournoi
"""

import random
from models.match import Match


class Tournament:
    def __init__(self, name, location):
        """initialise un nouveau tournoi"""
        self.name = name
        self.location = location  # lieu du tournoi
        self.date = None  # date du tournoi. 1 jour habituellement mais potentiellement plusieurs
        self.nb_rounds = 4  # nombre de rondes du tournoi
        self.rounds = []  # liste des instances rondes
        self.players = []  # liste des instances joueur
        self.control_time = []  # bullet, blitz ou coup rapide
        self.description = ""  # remarques du directeur du tournoi
        self.first_half = []
        self.second_half = []

    def __str__(self):
        return str([f"{player[0]} {player[1]}" for player in self.players])

    def add_date(self, date):
        self.date = date

    def add_player(self, player):
        if player not in self.players:
            self.players.append(player)

    def sort_players(self):
        self.players.sort(key=lambda x: x.rank)  # tri des joueurs par classement
        self.players.sort(key=lambda x: x.score, reverse=True)  # tri des joueurs par score
        return self.players

    def first_round_sort_players(self):
        # répartition des joueurs en deux moitiés : les x premiers et les x derniers
        self.first_half = self.players.copy()
        while len(self.first_half) > len(self.second_half):
            self.second_half.append(self.first_half.pop())

        # tri des joueurs de la seconde moitié par classement
        self.second_half.sort(key=lambda x: x.rank)

    def first_matchs(self):
        matchs = []
        for player1, player2 in zip(self.first_half, self.second_half):
            match = Match(player1, player2)
            matchs.append(match)
        return matchs

    def generate_round(self, newround):
        self.rounds.append(newround)
        print(f"{newround.name} : prochains matchs")
        for match in newround.matchs:
            print(match, match.player1.score, "-", match.player2.score, "\n")

    @staticmethod
    def generate_results(currentround):
        print(f"{currentround.name} : résultats")
        for match in currentround.matchs:
            print(f"Match opposant {match.player1} et {match.player2}")
            ecart = match.player2.rank - match.player1.rank
            maxrank = 30
            chance_draw = 0.33 - 0.66 * (ecart / (2 * maxrank))
            chance_win = 0.33 + 0.66 * (ecart / maxrank)
            seuil1 = int(1000 * chance_win)
            seuil2 = 1000 - int(1000 * chance_draw)
            result = random.randrange(1, 1000)
            if result <= seuil1:
                print(f"Victoire de {match.player1} \n")
                match.score1 += 1
                match.player1.score += 1
            elif result >= seuil2:
                print(f"Victoire de {match.player2} \n")
                match.score2 += 1
                match.player2.score += 1
            else:
                print(f"Match nul entre {match.player1} et {match.player2} \n")
                match.score1 += 0.5
                match.score2 += 0.5
                match.player1.score += 0.5
                match.player2.score += 0.5

    def display_scores(self):
        for player in self.players:
            print(player, player.score)
        print("________\n")

    def other_matchs(self):
        matchs = []
        first_players = list(self.players)
        second_players = list(self.players)

        while first_players:
            second_players.remove(second_players[0])
            x = 0
            appairing = 0
            match = None

            while appairing == 0:
                flag = 0
                match = Match(first_players[0], second_players[x])
                for myround in self.rounds:
                    for past_match in myround.matchs:
                        if match.player1 == past_match.player1 and match.player2 == past_match.player2 \
                                or match.player1 == past_match.player2 and match.player2 == past_match.player1:
                            if len(first_players) > 2:
                                x += 1
                                flag = 1
                                break
                if flag == 0:
                    appairing = 1

            matchs.append(match)
            first_players.remove(first_players[0])
            first_players.remove(second_players[x])
            second_players.remove(second_players[x])
        return matchs
